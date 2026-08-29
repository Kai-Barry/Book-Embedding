import os
import json
import tarfile
import urllib.request
import pandas as pd
from typing import Optional, List, Dict, Any
from pathlib import Path
from src.config import RAW_DATA_DIR

# CMU Book Summary Dataset URL (standard NLP benchmark dataset)
CMU_DATASET_URL = "http://www.cs.cmu.edu/~dbamman/data/booksummaries.tar.gz"

class BookDataLoader:
    """
    Downloads, parses, cleans, and standardizes book datasets for semantic embedding.
    """
    
    @staticmethod
    def download_cmu_dataset(target_dir: Path = RAW_DATA_DIR) -> Path:
        """Download and extract CMU Book Summary dataset if not already present."""
        tar_path = target_dir / "BookSummaries.tar.gz"
        extracted_txt = target_dir / "booksummaries" / "booksummaries.txt"
        
        if extracted_txt.exists():
            print(f"[DataLoader] Found existing dataset at: {extracted_txt}")
            return extracted_txt
            
        print(f"[DataLoader] Downloading CMU Book Summaries dataset from {CMU_DATASET_URL}...")
        urllib.request.urlretrieve(CMU_DATASET_URL, tar_path)
        print("[DataLoader] Download complete. Extracting...")
        
        with tarfile.open(tar_path, "r:gz") as tar:
            tar.extractall(path=target_dir)
            
        print(f"[DataLoader] Extracted to {extracted_txt}")
        return extracted_txt

    @classmethod
    def load_cmu_books(cls, file_path: Optional[Path] = None, max_records: Optional[int] = None, min_ratings: int = 100) -> pd.DataFrame:
        """
        Parses CMU Book Summaries and merges with Goodreads 100k Popular Verified Reader Dataset and Modern Curated Masterpieces.
        """
        if file_path is None or not Path(file_path).exists():
            file_path = cls.download_cmu_dataset()
            
        records = []
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for i, line in enumerate(f):
                if max_records and i >= max_records:
                    break
                parts = line.strip().split("\t")
                if len(parts) >= 7:
                    wiki_id, fb_id, title, author, pub_date, genres_raw, summary = parts[:7]
                    
                    genres = []
                    if genres_raw and genres_raw.startswith("{"):
                        try:
                            g_dict = json.loads(genres_raw)
                            genres = list(g_dict.values())
                        except Exception:
                            genres = []
                            
                    records.append({
                        "id": f"cmu_{wiki_id}",
                        "title": title.strip(),
                        "author": author.strip() if author else "Unknown Author",
                        "pub_date": pub_date.strip() if pub_date else "Unknown",
                        "genres": ", ".join(genres) if genres else "General",
                        "genre_list": genres,
                        "summary": summary.strip(),
                        "community_rating": 4.1,
                        "ratings_count": 1500
                    })
                    
        df = pd.DataFrame(records)
        
        # 1. Merge Goodreads 100k Popular Books (filtered by reader volume)
        try:
            print(f"[DataLoader] Loading Goodreads 100k Popular Dataset (min_ratings >= {min_ratings})...")
            from datasets import load_dataset
            gr_ds = load_dataset("euclaise/goodreads_100k", split="train")
            gr_records = []
            
            for item in gr_ds:
                t = str(item.get("title") or "").strip()
                a = str(item.get("author") or "Unknown Author").strip()
                d = str(item.get("desc") or "").strip()
                total_ratings = int(item.get("totalratings") or 0)
                rating = float(item.get("rating") or 0.0)
                
                # Popularity filter: minimum ratings threshold & non-empty synopsis
                if total_ratings < min_ratings or len(d) < 80 or not t:
                    continue
                    
                # Clean genres
                raw_genre = str(item.get("genre") or "Fiction")
                genre_tokens = [g.strip() for g in raw_genre.split(",") if g.strip() and g.strip() != "..."]
                unique_genres = list(dict.fromkeys(genre_tokens))[:4]
                if not unique_genres:
                    unique_genres = ["Fiction"]
                    
                # Strip HTML tags from description if present
                import re
                clean_desc = re.sub(r"<[^>]+>", " ", d).strip()
                clean_desc = " ".join(clean_desc.split())
                
                gr_records.append({
                    "id": f"gr_{len(gr_records)}",
                    "title": t,
                    "author": a,
                    "pub_date": "Contemporary",
                    "genres": ", ".join(unique_genres),
                    "genre_list": unique_genres,
                    "summary": clean_desc,
                    "community_rating": rating if rating > 0 else 4.0,
                    "ratings_count": total_ratings
                })
                
            if gr_records:
                gr_df = pd.DataFrame(gr_records)
                df = pd.concat([df, gr_df], ignore_index=True)
                print(f"[DataLoader] Merged {len(gr_df)} verified popular Goodreads books (ratings >= {min_ratings}).")
        except Exception as e:
            print(f"[DataLoader] Goodreads dataset merge skipped: {e}")

        # 2. Merge Modern Curated Masterpieces (Iain Reid, Three-Body Problem, etc.)
        try:
            from src.modern_loader import fetch_curated_modern_dataset
            modern_df = fetch_curated_modern_dataset()
            if not modern_df.empty:
                df = pd.concat([df, modern_df], ignore_index=True)
                print(f"[DataLoader] Merged {len(modern_df)} curated modern titles.")
        except Exception as e:
            print(f"[DataLoader] Modern dataset merge skipped: {e}")

        df = cls.clean_dataframe(df)
        print(f"[DataLoader] Total loaded {len(df)} cleaned popular books with rich synopses.")
        return df

    @staticmethod
    def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
        """Cleans dataframe and constructs unbiased, content-first & style embedding prompts."""
        df = df[df["title"].str.len() > 0]
        df = df[df["summary"].str.len() > 40].copy()
        
        # Deduplicate on title and author
        df = df.drop_duplicates(subset=["title", "author"])
        
        # Unbiased Content & Writing Style Fusion Prompt (strips author to eliminate superficial clustering)
        def create_embedding_text(row):
            parts = [
                f"[Tone, Mood & Atmosphere]: {row['genres']}",
                f"[Narrative Content, Prose & Plot Structure]: {row['summary']}"
            ]
            return "\n".join(parts)
            
        df["embedding_text"] = df.apply(create_embedding_text, axis=1)
        return df.reset_index(drop=True)

    @classmethod
    def load_custom_csv(cls, csv_path: str) -> pd.DataFrame:
        """Loads and normalizes user-provided Goodreads or custom book CSVs."""
        df = pd.read_csv(csv_path)
        # Attempt to map common column names
        rename_map = {
            "Book-Title": "title", "Title": "title", "name": "title",
            "Book-Author": "author", "Author": "author", "authors": "author",
            "Genre": "genres", "Genres": "genres", "categories": "genres",
            "Description": "summary", "Summary": "summary", "Plot": "summary", "plot": "summary",
            "Year-Of-Publication": "pub_date", "PublishedYear": "pub_date", "pub_date": "pub_date"
        }
        df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})
        
        for col in ["title", "author", "genres", "summary", "pub_date"]:
            if col not in df.columns:
                df[col] = "Unknown" if col != "summary" else ""
                
        if "id" not in df.columns:
            df["id"] = [f"book_{i}" for i in range(len(df))]
            
        return cls.clean_dataframe(df)

    _online_book_cache: Dict[str, Dict[str, Any]] = {}

    @classmethod
    def fetch_online_book(cls, query: str) -> Optional[Dict[str, Any]]:
        """
        Dynamically fetches book metadata and plot descriptions from OpenLibrary & Google Books API
        for modern titles not present in historical datasets.
        Supports both natural language search query and direct OpenLibrary IDs (ol_OL... or /works/OL...).
        """
        if not query or not str(query).strip():
            return None

        q_clean = str(query).strip()
        
        # Check in-memory cache
        if q_clean in cls._online_book_cache:
            return cls._online_book_cache[q_clean]
        if q_clean.lower() in cls._online_book_cache:
            return cls._online_book_cache[q_clean.lower()]
            
        import urllib.parse
        import urllib.request
        import json
        import re

        headers = {"User-Agent": "BookEmbeddingResearchEngine/2.0 (kaiba@gmail.com)"}

        # Direct OpenLibrary work key resolution: e.g. ol_OL20883297W or OL20883297W
        ol_key_match = re.match(r"^(?:ol_)?(OL\d+W)$", q_clean, re.IGNORECASE)
        if ol_key_match:
            work_key = ol_key_match.group(1).upper()
            try:
                work_url = f"https://openlibrary.org/works/{work_key}.json"
                req = urllib.request.Request(work_url, headers=headers)
                with urllib.request.urlopen(req, timeout=5) as resp:
                    wdata = json.loads(resp.read().decode("utf-8"))
                    title = wdata.get("title", "").strip()
                    desc_raw = wdata.get("description", "")
                    summary = ""
                    if isinstance(desc_raw, dict):
                        summary = desc_raw.get("value", "")
                    elif isinstance(desc_raw, str):
                        summary = desc_raw
                        
                    authors_list = []
                    for a in wdata.get("authors", []):
                        if isinstance(a, dict) and "author" in a and "key" in a["author"]:
                            try:
                                a_url = f"https://openlibrary.org{a['author']['key']}.json"
                                areq = urllib.request.Request(a_url, headers=headers)
                                with urllib.request.urlopen(areq, timeout=3) as aresp:
                                    adata = json.loads(aresp.read().decode("utf-8"))
                                    if adata.get("name"):
                                        authors_list.append(adata["name"])
                            except Exception:
                                pass
                    author_name = ", ".join(authors_list) if authors_list else "Unknown Author"
                    
                    raw_subjects = wdata.get("subjects", [])
                    subjects = [s.strip() for s in raw_subjects if isinstance(s, str)][:4]
                    genres = ", ".join(subjects) if subjects else "Fiction"
                    
                    if not summary:
                        summary = f"A prominent literary work by {author_name} exploring {genres}."
                        
                    clean_summary = re.sub(r"<[^>]+>", " ", summary).strip()
                    clean_summary = " ".join(clean_summary.split())
                    
                    book_data = {
                        "id": f"ol_{work_key}",
                        "title": title or "Unknown Title",
                        "author": author_name,
                        "pub_date": "Contemporary",
                        "genres": genres,
                        "genre_list": subjects or ["Fiction"],
                        "summary": clean_summary,
                        "embedding_text": f"[Tone, Mood & Atmosphere]: {genres}\n[Narrative Content, Prose & Plot Structure]: {clean_summary}",
                        "community_rating": 4.2,
                        "ratings_count": 2500,
                        "is_dynamic": True
                    }
                    cls._online_book_cache[q_clean] = book_data
                    cls._online_book_cache[book_data["id"]] = book_data
                    cls._online_book_cache[book_data["title"].lower()] = book_data
                    return book_data
            except Exception as e:
                print(f"[DataLoader] Direct OpenLibrary key lookup failed for {work_key}: {e}")

        # 1. Search OpenLibrary API by title / query
        try:
            encoded = urllib.parse.quote(q_clean)
            url = f"https://openlibrary.org/search.json?q={encoded}&limit=1"
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode("utf-8"))
                if "docs" in data and len(data["docs"]) > 0:
                    doc = data["docs"][0]
                    title = doc.get("title", "").strip()
                    authors = ", ".join(doc.get("author_name", ["Unknown Author"]))
                    pub_date = str(doc.get("first_publish_year", "Contemporary"))
                    raw_subj = doc.get("subject", [])
                    subjects = [s.strip() for s in raw_subj if isinstance(s, str)][:4] if isinstance(raw_subj, list) else ["Fiction"]
                    genres = ", ".join(subjects) if subjects else "Fiction"
                    
                    key = doc.get("key", "").replace("/works/", "")
                    summary = ""
                    if key:
                        try:
                            work_url = f"https://openlibrary.org/works/{key}.json"
                            wreq = urllib.request.Request(work_url, headers=headers)
                            with urllib.request.urlopen(wreq, timeout=4) as wres:
                                wdata = json.loads(wres.read().decode("utf-8"))
                                desc_raw = wdata.get("description", "")
                                if isinstance(desc_raw, dict):
                                    summary = desc_raw.get("value", "")
                                elif isinstance(desc_raw, str):
                                    summary = desc_raw
                        except Exception:
                            pass
                    
                    if not summary or len(summary) < 80:
                        first_sentence = doc.get("first_sentence", {}).get("value", "") if isinstance(doc.get("first_sentence"), dict) else (doc.get("first_sentence") if isinstance(doc.get("first_sentence"), str) else "")
                        if first_sentence:
                            summary = first_sentence
                        else:
                            # Query Wikipedia Deep-Plot API for rich authentic plot breakdown
                            try:
                                from src.data_enricher import data_enricher
                                wiki = data_enricher.fetch_wikipedia_metadata(title, authors)
                                if wiki and wiki.get("extract"):
                                    summary = wiki["extract"]
                            except Exception:
                                pass
                        if not summary:
                            summary = f"A novel by {authors} exploring {genres}."
                    
                    if title:
                        clean_summary = re.sub(r"<[^>]+>", " ", summary).strip()
                        clean_summary = " ".join(clean_summary.split())
                        book_id = f"ol_{key}" if key else f"ol_{title.lower().replace(' ', '_')}"
                        book_data = {
                            "id": book_id,
                            "title": title,
                            "author": authors,
                            "pub_date": pub_date,
                            "genres": genres,
                            "genre_list": subjects or ["Fiction"],
                            "summary": clean_summary,
                            "embedding_text": f"[Tone, Mood & Atmosphere]: {genres}\n[Narrative Content, Prose & Plot Structure]: {clean_summary}",
                            "community_rating": float(doc.get("ratings_average", 4.1) or 4.1),
                            "ratings_count": int(doc.get("ratings_count", 1500) or 1500),
                            "is_dynamic": True
                        }
                        cls._online_book_cache[q_clean] = book_data
                        cls._online_book_cache[book_id] = book_data
                        cls._online_book_cache[title.lower()] = book_data
                        return book_data
        except Exception as e:
            print(f"[DataLoader] OpenLibrary fetch failed: {e}")

        # 2. Fallback to Google Books API
        try:
            encoded = urllib.parse.quote(q_clean)
            url = f"https://www.googleapis.com/books/v1/volumes?q={encoded}&maxResults=1"
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=4) as response:
                data = json.loads(response.read().decode("utf-8"))
                if "items" in data and len(data["items"]) > 0:
                    info = data["items"][0]["volumeInfo"]
                    title = info.get("title", "").strip()
                    authors = ", ".join(info.get("authors", ["Unknown Author"]))
                    pub_date = str(info.get("publishedDate", "Contemporary"))[:4]
                    categories = info.get("categories", ["Fiction"])
                    genres = ", ".join(categories)
                    summary = info.get("description", "").strip()
                    
                    if title and len(summary) > 20:
                        clean_summary = re.sub(r"<[^>]+>", " ", summary).strip()
                        clean_summary = " ".join(clean_summary.split())
                        book_id = f"gbook_{data['items'][0]['id']}"
                        book_data = {
                            "id": book_id,
                            "title": title,
                            "author": authors,
                            "pub_date": pub_date,
                            "genres": genres,
                            "genre_list": categories,
                            "summary": clean_summary,
                            "embedding_text": f"[Tone, Mood & Atmosphere]: {genres}\n[Narrative Content, Prose & Plot Structure]: {clean_summary}",
                            "community_rating": float(info.get("averageRating", 4.0) or 4.0),
                            "ratings_count": int(info.get("ratingsCount", 1000) or 1000),
                            "is_dynamic": True
                        }
                        cls._online_book_cache[q_clean] = book_data
                        cls._online_book_cache[book_id] = book_data
                        cls._online_book_cache[title.lower()] = book_data
                        return book_data
        except Exception as e:
            print(f"[DataLoader] Google Books fetch skipped/failed: {e}")

        return None

