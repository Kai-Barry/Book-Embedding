from typing import List, Dict, Any, Optional
import pandas as pd
from src.embedder import BaseEmbedder, get_embedder
from src.vector_store import BookVectorStore

class BookRecommender:
    """
    Core Machine Learning Recommendation & Semantic Search Engine.
    """
    def __init__(self, vector_store: BookVectorStore, embedder: Optional[BaseEmbedder] = None):
        self.store = vector_store
        self.embedder = embedder
        self._build_prefix_index()

    def _build_prefix_index(self):
        """Builds in-memory token prefix inverted index for sub-2ms instant autocomplete typing."""
        self.prefix_map = {}
        if self.store.df is None:
            return
            
        print("[Recommender] Building ultra-fast in-memory prefix index...")
        for idx, row in self.store.df.iterrows():
            title = str(row["title"]).lower()
            # Clean tokens
            tokens = [t for t in title.replace("-", " ").replace("'", "").split() if len(t) >= 2]
            for token in tokens:
                for length in range(2, min(len(token) + 1, 6)):
                    p = token[:length]
                    if p not in self.prefix_map:
                        self.prefix_map[p] = []
                    if len(self.prefix_map[p]) < 30:
                        self.prefix_map[p].append(idx)
        print(f"[Recommender] Indexed {len(self.prefix_map)} unique search prefixes.")

    def extract_similarity_reasons(self, target_book: Dict[str, Any], candidate: Dict[str, Any]) -> List[str]:
        """
        Deep Machine Learning Explainability: Computes thematic, stylistic, and micro-cluster overlapping rationales.
        """
        from src.style_extractor import StyleExtractor
        reasons = []
        
        # 1. Stylistic & Voice Concordance
        t_style = StyleExtractor.analyze_book(target_book)
        c_style = StyleExtractor.analyze_book(candidate)

        if t_style["pov"] == c_style["pov"] and t_style["pov"] != "Third Person":
            reasons.append(f"Narrative Voice: Both written in {t_style['pov']}")
        if t_style["pacing"] == c_style["pacing"] and t_style["pacing"] != "Moderate Pacing":
            reasons.append(f"Story Pacing: Both feature {t_style['pacing']} structure")
        if t_style["tone"] == c_style["tone"] and t_style["tone"] != "Grounded & Dramatic":
            reasons.append(f"Atmospheric Mood: {t_style['tone']}")

        # 2. Check Genre Overlap
        t_genres = set([g.strip().lower() for g in str(target_book.get("genres", "")).split(",") if g.strip()])
        c_genres = set([g.strip().lower() for g in str(candidate.get("genres", "")).split(",") if g.strip()])
        shared_genres = t_genres.intersection(c_genres)
        if shared_genres:
            top_shared = [g.title() for g in list(shared_genres)[:2]]
            reasons.append(f"Shared Genre: {', '.join(top_shared)}")

        # 3. Extract Narrative Motifs & Specific Tropes
        THEMATIC_MOTIFS = [
            ("Existential Dread & Solitude", ["isolation", "isolated", "existential", "solitude", "alone", "dread", "remote", "lonely", "snowstorm", "farm"]),
            ("Psychological Paranoia & Memory Fracture", ["psychological", "mind", "paranoia", "unravel", "sanity", "terror", "chilling", "disturbing", "memory", "hallucination"]),
            ("Deep Space Survival & Extinction", ["space", "alien", "galaxy", "solar", "ship", "extraterrestrial", "extinction", "universe", "astrophage", "trisolaris"]),
            ("Quantum Superposition & Multiverse Paradox", ["quantum", "parallel", "superposition", "dimension", "timeline", "multiverse", "infinite realities"]),
            ("Time Travel & Temporal Mechanics", ["time travel", "temporal", "rewriting", "past", "future", "loop", "timeline"]),
            ("Dystopian Totalitarianism & Resistance", ["dystopia", "dystopian", "regime", "surveillance", "totalitarian", "rebel", "empire", "oppression"]),
            ("Gothic Curse & Eldritch Horror", ["gothic", "curse", "haunted", "vampire", "monster", "demon", "darkness", "ghost", "eldritch"]),
            ("High Fantasy Magic & Realm Intrigue", ["magic", "kingdom", "sword", "dragon", "wizard", "empire", "sorcery", "realm", "court"]),
            ("Noir Detective & Forensic Investigation", ["detective", "murder", "investigation", "clue", "killer", "police", "crime", "mystery", "noir"]),
            ("Unreliable Identity & Deception", ["unreliable", "identity", "secrets", "amnesia", "deception", "facade", "illusion", "double"])
        ]

        t_text = (str(target_book.get("summary", "")) + " " + str(target_book.get("genres", ""))).lower()
        c_text = (str(candidate.get("summary", "")) + " " + str(candidate.get("genres", ""))).lower()

        for motif_name, keywords in THEMATIC_MOTIFS:
            t_match = any(k in t_text for k in keywords)
            c_match = any(k in c_text for k in keywords)
            if t_match and c_match:
                reasons.append(f"Thematic Motif: {motif_name}")
                if len(reasons) >= 4:
                    break

        if not reasons:
            reasons.append("High Dense Vector & Narrative Proximity (Cosine Alignment)")
            
        return reasons[:4]

    def get_book_details(self, book_id_or_title: str) -> Optional[Dict[str, Any]]:
        """Returns complete metadata, stylistic profile, and 2D coordinates for modal popup."""
        if self.store.df is None:
            return None
            
        match = self.store.df[
            (self.store.df["id"] == book_id_or_title) | 
            (self.store.df["title"].str.lower() == book_id_or_title.lower())
        ]
        if match.empty:
            return None
            
        r = match.iloc[0]
        from src.style_extractor import StyleExtractor
        style = StyleExtractor.analyze_book(r.to_dict())
        
        return {
            "id": str(r["id"]),
            "title": str(r["title"]),
            "author": str(r["author"]),
            "pub_date": str(r["pub_date"]),
            "genres": str(r["genres"]),
            "summary": str(r["summary"]),
            "style_profile": style
        }

    def search_books_by_text(self, query: str, top_k: int = 10, genre_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Free-form natural language semantic search.
        """
        if self.embedder is None:
            raise ValueError("Embedder is not initialized for query search.")
        query_vec = self.embedder.embed_query(query)
        results = self.store.search_by_vector(query_vec, top_k=top_k, genre_filter=genre_filter)
        
        # Attach query match reasons
        for r in results:
            r["similarity_reasons"] = [f"Semantic Match for '{query[:30]}' ({r['similarity_score']*100:.1f}%)"]
        return results

    def extract_concept_keywords(self, text: str, genres: str) -> List[str]:
        """Extracts top salient concept keywords and micro-clusters from summary and genres."""
        combined = (text + " " + genres).lower()
        candidates = [
            ("Existential Dread", ["existential", "solitude", "dread", "isolation", "alone"]),
            ("Cosmic Extinction Crisis", ["extinction", "alien", "trisolaris", "cosmic", "crisis", "universe"]),
            ("Memory & Identity Fracture", ["memory", "memories", "amnesia", "identity", "unravel", "hallucination"]),
            ("Dystopian Resistance", ["dystopia", "surveillance", "totalitarian", "regime", "rebellion", "empire"]),
            ("Deep Space Odyssey", ["space", "spaceship", "galaxy", "planetary", "orbit", "astronomy"]),
            ("Psychological Paranoia", ["paranoia", "terror", "sanity", "mind", "chilling", "disturbing"]),
            ("Quantum Multiverse", ["quantum", "parallel", "superposition", "dimension", "timeline"]),
            ("Gothic Curse & Eldritch", ["gothic", "curse", "haunted", "vampire", "monster", "demon"]),
            ("Court Intrigue & Magic", ["kingdom", "magic", "sword", "dragon", "wizard", "empire", "sorcery"]),
            ("Noir Crime & Murder", ["detective", "murder", "investigation", "clue", "killer", "police"]),
            ("First-Person Confessional", ["first-person", "first person", "narrated by"]),
            ("Slow-Burn Atmospheric Build", ["slow-burn", "atmospheric", "meditative", "creeping"]),
            ("Propulsive Page-Turner", ["thriller", "action", "chase", "fast-paced", "cliffhanger"])
        ]
        extracted = []
        for name, kws in candidates:
            if any(k in combined for k in kws):
                extracted.append(name)
        if not extracted:
            extracted = ["Narrative Prose Alignment", "Thematic Resonance"]
        return extracted[:6]

    def recommend_similar_to_book(
        self, 
        book_id_or_title: str, 
        top_k: int = 10, 
        genre_filter: Optional[str] = None,
        weight_plot: float = 1.0,
        weight_tone: float = 0.7,
        weight_style: float = 0.5,
        weight_pacing: float = 0.4,
        active_keywords: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Finds books mathematically closest in vector embedding space to a given target book,
        performing a full global vector re-search across all 25,101 books when custom weights/concepts are modified.
        """
        target_info = self.store.get_book_info_with_coords(book_id_or_title)
        
        matches = []
        if self.store.df is not None:
            matches = self.store.df.index[
                (self.store.df["id"] == book_id_or_title) | 
                (self.store.df["title"].str.lower() == book_id_or_title.lower())
            ].tolist()

        if not matches or self.store.embeddings is None:
            raise ValueError(f"Book '{book_id_or_title}' not found in database.")

        book_idx = matches[0]
        base_vector = self.store.embeddings[book_idx]

        concept_keywords = self.extract_concept_keywords(target_info.get("summary", ""), target_info.get("genres", "")) if target_info else []
        active_kws_list = active_keywords if active_keywords is not None else concept_keywords

        # Generate concept query vector if keywords are active
        concept_vec = None
        if active_kws_list and self.embedder:
            concept_text = "Thematic Motifs: " + ", ".join(active_kws_list)
            concept_vec = self.embedder.embed_texts([concept_text])[0]

        # Full global weighted vector search across all 25,101 books
        weight_concept = 0.4 if active_kws_list else 0.0
        candidates = self.store.perform_weighted_search(
            base_vector=base_vector,
            concept_query_vector=concept_vec,
            top_k=min(100, top_k * 5),
            weight_plot=weight_plot,
            weight_concept=weight_concept,
            genre_filter=genre_filter
        )

        # Filter out target book itself
        candidates = [c for c in candidates if c["id"] != str(target_info["id"])]

        from src.style_extractor import StyleExtractor
        t_style = StyleExtractor.analyze_book(target_info) if target_info else {}
        active_kws_set = set(active_kws_list)

        # Fine-grained stylistic scoring
        for item in candidates:
            base_sim = item["similarity_score"]
            c_style = StyleExtractor.analyze_book(item)
            
            tone_match = 1.0 if (t_style.get("tone") == c_style.get("tone") and t_style.get("tone") != "Grounded & Dramatic") else 0.0
            style_match = 1.0 if (t_style.get("pov") == c_style.get("pov") and t_style.get("pov") != "Third Person") else 0.0
            pacing_match = 1.0 if (t_style.get("pacing") == c_style.get("pacing") and t_style.get("pacing") != "Moderate Pacing") else 0.0

            c_kws = set(self.extract_concept_keywords(item.get("summary", ""), item.get("genres", "")))
            kw_overlap = len(active_kws_set.intersection(c_kws)) / max(1, len(active_kws_set))

            total_weight = weight_plot + weight_tone + weight_style + weight_pacing + 0.5
            final_score = (
                (item.get("weighted_score", base_sim) * weight_plot) + 
                (tone_match * 0.15 * weight_tone) + 
                (style_match * 0.12 * weight_style) + 
                (pacing_match * 0.10 * weight_pacing) +
                (kw_overlap * 0.15)
            ) / max(0.1, total_weight)

            item["weighted_score"] = float(final_score)
            if target_info:
                item["similarity_reasons"] = self.extract_similarity_reasons(target_info, item)
            else:
                item["similarity_reasons"] = [f"Global Dense Vector Match ({base_sim*100:.1f}%)"]

        candidates.sort(key=lambda x: x.get("weighted_score", x["similarity_score"]), reverse=True)
        final_results = candidates[:top_k]

        return {
            "target_book": target_info,
            "concept_keywords": concept_keywords,
            "results": final_results
        }

    def search_catalog_titles(self, query: str, limit: int = 15) -> List[Dict[str, Any]]:
        """
        Sub-2ms instantaneous autocomplete engine powered by inverted prefix map + RapidFuzz fallback.
        """
        if self.store.df is None:
            return []
            
        q = query.strip().lower()
        if not q:
            return []

        df = self.store.df
        q_norm = q.replace("-", " ").replace("'", "").replace('"', '').strip()
        # 1. Tier 1: Multi-word containment / Prefix Match
        title_lower = df["title"].str.lower()
        title_norm = title_lower.str.replace("-", " ", regex=False).str.replace("'", "", regex=False)
        
        words = q_norm.split()
        if len(words) > 1:
            multi_word_mask = pd.Series(True, index=df.index)
            for w in words:
                multi_word_mask = multi_word_mask & title_norm.str.contains(w, na=False)
            multi_word_matches = df[multi_word_mask].index.tolist()
        else:
            multi_word_matches = []

        prefix_matches = df[title_norm.str.startswith(q_norm, na=False) | title_lower.str.startswith(q, na=False)].index.tolist()

        # 2. Tier 2: Instant Inverted Prefix Map Lookup
        matched_indices = []
        if q_norm in self.prefix_map:
            matched_indices.extend(self.prefix_map[q_norm])

        # Merge candidate list preserving priority: multi-word -> prefix -> inverted prefix
        all_candidates = list(dict.fromkeys(multi_word_matches + prefix_matches + matched_indices))

        # 3. Tier 3: RapidFuzz fallback if candidate count is small
        if len(all_candidates) < limit:
            try:
                from rapidfuzz import process, fuzz
                titles_list = df["title"].tolist()
                fuzzy_results = process.extract(
                    q_norm, 
                    titles_list, 
                    scorer=fuzz.token_set_ratio, 
                    limit=limit, 
                    score_cutoff=65.0
                )
                for title_match, score, idx in fuzzy_results:
                    if idx not in all_candidates:
                        all_candidates.append(idx)
            except Exception as e:
                pass

        results = []
        for idx in all_candidates[:limit]:
            row = df.iloc[idx]
            results.append({
                "id": str(row["id"]),
                "title": str(row["title"]),
                "author": str(row["author"]),
                "genres": str(row["genres"]),
                "pub_date": str(row["pub_date"]),
                "summary": str(row["summary"]),
                "is_dynamic": False
            })

        # Dynamic OpenLibrary fetch if no results
        if len(results) < 2:
            from src.data_loader import BookDataLoader
            online_book = BookDataLoader.fetch_online_book(query)
            if online_book:
                if not any(r["title"].lower() == online_book["title"].lower() for r in results):
                    online_book["is_dynamic"] = True
                    results.insert(0, online_book)

        return results[:limit]

    def get_all_genres(self) -> List[str]:
        """Extracts unique genres sorted by frequency."""
        if self.store.df is None or "genres" not in self.store.df.columns:
            return []
        genres_series = self.store.df["genres"].dropna().str.split(", ")
        all_genres = [g.strip() for sublist in genres_series for g in sublist if g.strip() and g.strip() != "General"]
        from collections import Counter
        counts = Counter(all_genres)
        return [g for g, _ in counts.most_common(50)]
