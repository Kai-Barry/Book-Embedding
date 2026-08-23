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
    def load_cmu_books(cls, file_path: Optional[Path] = None, max_records: Optional[int] = None) -> pd.DataFrame:
        """
        Parses CMU Book Summaries and merges with Goodreads 10k Must-Reads and Modern Curated Masterpieces.
        """
        if file_path is None or not Path(file_path).exists():
            file_path = cls.download_cmu_dataset()
            
        cols = [
            "wiki_id", "freebase_id", "title", "author", "pub_date", "genres_raw", "summary"
        ]
        
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
                        "summary": summary.strip()
                    })
                    
        df = pd.DataFrame(records)
        
        # 1. Merge Goodreads 10k Dataset
        try:
            print("[DataLoader] Loading Goodreads 10k Must-Reads Dataset from HuggingFace...")
            from datasets import load_dataset
            gr_ds = load_dataset("Eitanli/goodreads", split="train")
            gr_records = []
            for item in gr_ds:
                t = (item.get("Book") or "").strip()
                a = (item.get("Author") or "Unknown Author").strip()
                d = (item.get("Description") or "").strip()
                g_str = item.get("Genres") or "['Fiction']"
                try:
                    g_list = eval(g_str) if isinstance(g_str, str) and g_str.startswith("[") else [g_str]
                except Exception:
                    g_list = ["Fiction"]
                
                if t and len(d) > 40:
                    gr_records.append({
                        "id": f"gr_{len(gr_records)}",
                        "title": t,
                        "author": a,
                        "pub_date": "Contemporary",
                        "genres": ", ".join(g_list[:4]),
                        "genre_list": g_list[:4],
                        "summary": d
                    })
            if gr_records:
                gr_df = pd.DataFrame(gr_records)
                df = pd.concat([df, gr_df], ignore_index=True)
                print(f"[DataLoader] Merged {len(gr_df)} Goodreads books.")
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
        print(f"[DataLoader] Total loaded {len(df)} cleaned books with rich synopses.")
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

    @staticmethod
    def fetch_online_book(query: str) -> Optional[Dict[str, Any]]:
        """
        Dynamically fetches book metadata and plot descriptions from OpenLibrary & Google Books API
        for modern titles not present in historical datasets (e.g. Iain Reid, The Three-Body Problem).
        """
        import urllib.parse
        import urllib.request
        
        # 1. Try OpenLibrary API (fast, reliable, no API key needed)
        try:
            encoded = urllib.parse.quote(query)
            url = f"https://openlibrary.org/search.json?q={encoded}&limit=1"
            req = urllib.request.Request(url, headers={"User-Agent": "BookEmbeddingResearchApp/1.0 (kaiba@gmail.com)"})
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode("utf-8"))
                if "docs" in data and len(data["docs"]) > 0:
                    doc = data["docs"][0]
                    title = doc.get("title", "").strip()
                    authors = ", ".join(doc.get("author_name", ["Unknown Author"]))
                    pub_date = str(doc.get("first_publish_year", "Unknown"))
                    genres = ", ".join(doc.get("subject", ["Fiction"])[:4])
                    
                    # Try to get work description if possible
                    key = doc.get("key", "").replace("/works/", "")
                    summary = ""
                    if key:
                        try:
                            work_url = f"https://openlibrary.org/works/{key}.json"
                            wreq = urllib.request.Request(work_url, headers={"User-Agent": "BookEmbeddingResearchApp/1.0"})
                            with urllib.request.urlopen(wreq, timeout=3) as wres:
                                wdata = json.loads(wres.read().decode("utf-8"))
                                desc = wdata.get("description", "")
                                if isinstance(desc, dict):
                                    summary = desc.get("value", "")
                                elif isinstance(desc, str):
                                    summary = desc
                        except Exception:
                            pass
                    
                    if not summary:
                        first_sentence = doc.get("first_sentence", {}).get("value", "") if isinstance(doc.get("first_sentence"), dict) else ""
                        summary = first_sentence or f"A novel by {authors} exploring {genres}."
                    
                    if title:
                        book_id = f"ol_{key}" if key else f"ol_{title.lower().replace(' ', '_')}"
                        embed_text = f"Title: {title}\nAuthor: {authors}\nGenres: {genres}\nDescription: {summary}"
                        return {
                            "id": book_id,
                            "title": title,
                            "author": authors,
                            "pub_date": pub_date,
                            "genres": genres,
                            "genre_list": doc.get("subject", ["Fiction"])[:4],
                            "summary": summary,
                            "embedding_text": embed_text
                        }
        except Exception as e:
            print(f"[DataLoader] OpenLibrary fetch failed: {e}")

        # 2. Try Google Books API as fallback
        try:
            encoded = urllib.parse.quote(query)
            url = f"https://www.googleapis.com/books/v1/volumes?q={encoded}&maxResults=1"
            req = urllib.request.Request(url, headers={"User-Agent": "BookEmbeddingResearchApp/1.0"})
            with urllib.request.urlopen(req, timeout=4) as response:
                data = json.loads(response.read().decode("utf-8"))
                if "items" in data and len(data["items"]) > 0:
                    info = data["items"][0]["volumeInfo"]
                    title = info.get("title", "").strip()
                    authors = ", ".join(info.get("authors", ["Unknown Author"]))
                    pub_date = info.get("publishedDate", "Unknown")[:4]
                    genres = ", ".join(info.get("categories", ["Fiction"]))
                    summary = info.get("description", "").strip()
                    
                    if title and len(summary) > 20:
                        book_id = f"gbook_{data['items'][0]['id']}"
                        embed_text = f"Title: {title}\nAuthor: {authors}\nGenres: {genres}\nDescription: {summary}"
                        return {
                            "id": book_id,
                            "title": title,
                            "author": authors,
                            "pub_date": pub_date,
                            "genres": genres,
                            "genre_list": info.get("categories", ["Fiction"]),
                            "summary": summary,
                            "embedding_text": embed_text
                        }
        except Exception as e:
            print(f"[DataLoader] Google Books fetch failed: {e}")

        return None

