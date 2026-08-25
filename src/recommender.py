import re
from typing import List, Dict, Any, Optional
import pandas as pd
from src.embedder import BaseEmbedder, get_embedder
from src.vector_store import BookVectorStore
from src.data_enricher import data_enricher
from src.collaborative import collaborative_engine

class BookRecommender:
    """
    Core Machine Learning Recommendation & Semantic Search Engine.
    """
    def __init__(self, vector_store: BookVectorStore, embedder: Optional[BaseEmbedder] = None):
        self.store = vector_store
        self.embedder = embedder
        self.enricher = data_enricher
        self.collab = collaborative_engine
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
        Deep Machine Learning Explainability: Computes thematic, stylistic, series, and collaborative rationales.
        """
        from src.style_extractor import StyleExtractor
        reasons = []
        
        # 1. Series / Universe Matching
        t_series = target_book.get("series_info")
        c_series = candidate.get("series_info")
        if t_series and c_series and t_series.get("series", "").lower() == c_series.get("series", "").lower():
            reasons.append(f"Series Connection: Both part of '{t_series['series']}' ({c_series.get('volume', '')})")

        # 2. Stylistic & Voice Concordance
        t_style = StyleExtractor.analyze_book(target_book)
        c_style = StyleExtractor.analyze_book(candidate)

        if t_style["pov"] == c_style["pov"] and t_style["pov"] != "Third Person":
            reasons.append(f"Narrative Voice: Both written in {t_style['pov']}")
        if t_style["pacing"] == c_style["pacing"] and t_style["pacing"] != "Moderate Pacing":
            reasons.append(f"Story Pacing: Both feature {t_style['pacing']} structure")
        if t_style["tone"] == c_style["tone"] and t_style["tone"] != "Grounded & Dramatic":
            reasons.append(f"Atmospheric Mood: {t_style['tone']}")

        # 3. Check Genre Overlap
        t_genres = set([g.strip().lower() for g in str(target_book.get("genres", "")).split(",") if g.strip()])
        c_genres = set([g.strip().lower() for g in str(candidate.get("genres", "")).split(",") if g.strip()])
        shared_genres = t_genres.intersection(c_genres)
        if shared_genres:
            top_shared = [g.title() for g in list(shared_genres)[:2]]
            reasons.append(f"Shared Genre: {', '.join(top_shared)}")

        # 4. Extract Narrative Motifs & Specific Tropes
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
        """Returns complete metadata, stylistic profile, series info, community metrics, and 2D coordinates for modal popup."""
        if self.store.df is None:
            return None
            
        match = self.store.df[
            (self.store.df["id"] == book_id_or_title) | 
            (self.store.df["title"].str.lower() == book_id_or_title.lower())
        ]
        if match.empty:
            return None
            
        r = match.iloc[0]
        raw_dict = r.to_dict()
        
        # Bolster metadata using DataEnricher (Series, Ratings, Readability, Fast Cached Data)
        enriched = self.enricher.bolster_book(raw_dict, fetch_online=False)
        
        from src.style_extractor import StyleExtractor
        style = StyleExtractor.analyze_book(enriched)
        subclustered = self.extract_subclustered_motifs(enriched.get("summary", ""), enriched.get("genres", ""))
        concept_kws = self.extract_concept_keywords(enriched.get("summary", ""), enriched.get("genres", ""))
        
        return {
            "id": str(enriched["id"]),
            "title": str(enriched["title"]),
            "author": str(enriched["author"]),
            "pub_date": str(enriched["pub_date"]),
            "genres": str(enriched["genres"]),
            "summary": str(enriched["summary"]),
            "style_profile": style,
            "subclustered_motifs": subclustered,
            "concept_keywords": concept_kws,
            "series_info": enriched.get("series_info"),
            "community_rating": enriched.get("community_rating"),
            "ratings_count": enriched.get("ratings_count"),
            "popularity": enriched.get("popularity"),
            "readability": enriched.get("readability")
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

    def extract_subclustered_motifs(self, text: str, genres: str) -> Dict[str, List[str]]:
        """
        Hierarchically extracts fine-grained thematic, setting, trope, and psychological sub-clusters.
        Returns a structured dictionary mapping sub-cluster categories to specific detected motifs.
        Uses whole-word regex pattern matching to avoid false substring positives.
        """
        combined = (str(text or "") + " " + str(genres or "")).lower()
        
        taxonomy = {
            "World & Setting": [
                ("Cyberpunk Megacity", [r"\bcyberpunk\b", r"\bneon\b", r"\bhacker\b", r"\bmegacorp\b", r"\bcyborg\b", r"\bvirtual reality\b", r"\bai dystopia\b"]),
                ("Deep Space Odyssey", [r"\bdeep space\b", r"\bspaceship\b", r"\bstarship\b", r"\bgalaxy\b", r"\borbit\b", r"\bstarfleet\b", r"\bastronomy\b", r"\bcosmos\b", r"\binterstellar\b"]),
                ("High Fantasy Realm", [r"\bkingdom\b", r"\bmagic\b", r"\bsword\b", r"\bdragon\b", r"\bwizard\b", r"\bsorcery\b", r"\brealm\b", r"\belf\b", r"\bspells\b"]),
                ("Post-Apocalyptic Wasteland", [r"\bpost[- ]apocalyptic\b", r"\bapocalypse\b", r"\bwasteland\b", r"\bfallout\b", r"\bruined earth\b", r"\bcollapse of civilization\b"]),
                ("Gothic Victorian & Manor", [r"\bgothic\b", r"\bvictorian\b", r"\bmanor\b", r"\bhaunted house\b", r"\bcastle\b", r"\bmacabre\b", r"\bancestral home\b"]),
                ("Maritime & Nautical Abyss", [r"\bocean\b", r"\bsea\b", r"\bsailor\b", r"\bship\b", r"\bcaptain\b", r"\bnautical\b", r"\bdeep sea\b", r"\bvoyage\b"]),
                ("Claustrophobic Subterranean", [r"\bunderground\b", r"\bbunker\b", r"\btunnel\b", r"\bsubterranean\b", r"\bcavern\b", r"\bsilo\b", r"\bsealed\b"]),
                ("Feudal Dynasty & Empire", [r"\bdynasty\b", r"\bemperor\b", r"\bempire\b", r"\bimperial\b", r"\bthrone\b", r"\bwarlord\b", r"\bfeudal\b"]),
                ("Dystopian Megastructure", [r"\bdystopia\b", r"\bsurveillance state\b", r"\btotalitarian\b", r"\bauthoritarian regime\b"]),
                ("Urban Supernatural", [r"\burban fantasy\b", r"\bvampire\b", r"\bwerewolf\b", r"\boccult detective\b", r"\bunderworld\b"])
            ],
            "Core Themes": [
                ("Existential Dread & Isolation", [r"\bexistential\b", r"\bsolitude\b", r"\bdread\b", r"\bisolation\b", r"\balienation\b", r"\bmeaning of life\b"]),
                ("Memory & Identity Fracture", [r"\bmemory\b", r"\bmemories\b", r"\bamnesia\b", r"\bidentity\b", r"\bunravel\b", r"\bhallucination\b", r"\bwho am i\b"]),
                ("Cosmic Extinction Crisis", [r"\bextinction\b", r"\balien invasion\b", r"\bcosmic threat\b", r"\buniversal annihilation\b"]),
                ("Loss of Humanity & Transhumanism", [r"\btranshuman\b", r"\bhumanity\b", r"\bconsciousness\b", r"\bsynthetic life\b", r"\bandroid\b", r"\bcyborg soul\b"]),
                ("Moral Decay & Ambiguity", [r"\bcorrupt\b", r"\bmoral ambiguity\b", r"\bcynical\b", r"\bdepravity\b", r"\bmoral compromise\b"]),
                ("Fate vs Free Will", [r"\bprophecy\b", r"\bdestiny\b", r"\bfate\b", r"\bfree will\b", r"\bpredestined\b", r"\boracle\b"]),
                ("Grief, Loss & Redemption", [r"\bgrief\b", r"\bmourning\b", r"\bguilt\b", r"\bredemption\b", r"\btragedy\b", r"\batonement\b"]),
                ("Power & Tyranny", [r"\btyrant\b", r"\boppression\b", r"\babsolute power\b", r"\bcorruption of power\b", r"\bconquest\b"])
            ],
            "Tropes & Conflicts": [
                ("Dystopian Rebellion & Insurgency", [r"\brebellion\b", r"\bresistance movement\b", r"\brevolution\b", r"\binsurgency\b", r"\buprising\b"]),
                ("Court Intrigue & Betrayal", [r"\bcourt intrigue\b", r"\bbetrayal\b", r"\btreason\b", r"\broyal court\b", r"\bscheming nobles\b"]),
                ("Noir Murder Investigation", [r"\bdetective\b", r"\bmurder investigation\b", r"\bserial killer\b", r"\bhomicide\b", r"\bsleuth\b"]),
                ("Heist & Covert Operations", [r"\bheist\b", r"\bcrew\b", r"\bcovert mission\b", r"\binfiltrate\b", r"\boperative\b"]),
                ("First Contact Dilemma", [r"\bfirst contact\b", r"\balien civilization\b", r"\bfermi paradox\b", r"\bxenology\b"]),
                ("Time Loop & Temporal Paradox", [r"\btime travel\b", r"\btime loop\b", r"\btimeline\b", r"\btemporal paradox\b", r"\bmultiverse\b"]),
                ("Cat-and-Mouse Chase", [r"\bcat[- ]and[- ]mouse\b", r"\bmanhunt\b", r"\bfugitive\b", r"\bpursuit\b"]),
                ("Secret Society & Occult Brotherhood", [r"\bsecret society\b", r"\boccult cult\b", r"\billuminati\b", r"\bhidden brotherhood\b", r"\besoteric order\b"])
            ],
            "Psychological Dynamics": [
                ("Unreliable Narrator & Paranoia", [r"\bunreliable narrator\b", r"\bparanoia\b", r"\binsanity\b", r"\bmadness\b", r"\bterror\b", r"\bchilling\b", r"\bdelusion\b"]),
                ("Slow-Burn Meditative Build", [r"\bslow[- ]burn\b", r"\batmospheric dread\b", r"\bmeditative\b", r"\bcreeping\b", r"\bcontemplative\b", r"\blyrical\b", r"\bunease\b", r"\bhaunting\b"]),
                ("Propulsive Page-Turner", [r"\bfast[- ]paced\b", r"\bcliffhanger\b", r"\brelentless pace\b", r"\bpulse[- ]pounding\b", r"\bpage[- ]turner\b", r"\bbreakneck\b"]),
                ("Claustrophobic Tension", [r"\bclaustrophobic\b", r"\btrapped\b", r"\bsuffocating\b", r"\bconfined\b", r"\bno escape\b"]),
                ("Fragmented Non-Linear Mind", [r"\bnon[- ]linear\b", r"\bstream of consciousness\b", r"\bsurreal\b", r"\bdreamlike\b", r"\bdisjointed\b"]),
                ("Dark Satire & Absurdism", [r"\bdark satire\b", r"\babsurdist\b", r"\bironic\b", r"\bblack comedy\b"])
            ]
        }

        extracted_categories = {}
        for category, motif_list in taxonomy.items():
            found = []
            for motif_name, patterns in motif_list:
                for pat in patterns:
                    if re.search(pat, combined):
                        found.append(motif_name)
                        break
            if found:
                # Disambiguate conflicting pacing in Psychological Dynamics
                if category == "Psychological Dynamics" and "Slow-Burn Meditative Build" in found and "Propulsive Page-Turner" in found:
                    slow_count = sum(len(re.findall(p, combined)) for p in [r"\bslow[- ]burn\b", r"\bcreeping\b", r"\bdread\b", r"\bunease\b", r"\bhaunting\b", r"\bmeditative\b"])
                    fast_count = sum(len(re.findall(p, combined)) for p in [r"\bfast[- ]paced\b", r"\bpropulsive\b", r"\baction\b", r"\bthriller\b", r"\bchase\b"])
                    if slow_count >= fast_count:
                        found.remove("Propulsive Page-Turner")
                    else:
                        found.remove("Slow-Burn Meditative Build")
                extracted_categories[category] = found[:3]

        return extracted_categories

    def extract_concept_keywords(self, text: str, genres: str) -> List[str]:
        """Extracts flattened list of top salient concept keywords and micro-clusters."""
        subclusters = self.extract_subclustered_motifs(text, genres)
        flattened = []
        for kws in subclusters.values():
            flattened.extend(kws)
        return flattened[:8]

    def recommend_similar_to_book(
        self, 
        book_id_or_title: str, 
        top_k: int = 10, 
        genre_filter: Optional[str] = None,
        weight_plot: float = 1.0,
        weight_tone: float = 1.0,
        weight_style: float = 1.0,
        weight_pacing: float = 1.0,
        weight_motifs: float = 1.0,
        weight_community: float = 1.0,
        boost_keywords: Optional[List[str]] = None,
        exclude_keywords: Optional[List[str]] = None,
        active_keywords: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Finds books mathematically closest in vector embedding space to a given target book,
        performing a full global vector re-search across all 25,101 books when custom weights/concepts are modified.
        Supports 1-7 priority scale multipliers, 3-state motif filtering, and Item2Vec collaborative taste blending.
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

        # Bolster target book metadata (Series, Ratings, Readability) - fast in-memory
        if target_info:
            target_info = self.enricher.bolster_book(target_info, fetch_online=False)

        # Extract hierarchical sub-clustered motifs
        subclustered_motifs = self.extract_subclustered_motifs(target_info.get("summary", ""), target_info.get("genres", "")) if target_info else {}
        concept_keywords = self.extract_concept_keywords(target_info.get("summary", ""), target_info.get("genres", "")) if target_info else []

        # Handle backward compatibility: active_keywords acts as boost_keywords
        effective_boost_kws = boost_keywords if boost_keywords is not None else (active_keywords if active_keywords is not None else concept_keywords)
        effective_exclude_kws = exclude_keywords if exclude_keywords is not None else []

        # Parse per-motif individual priority weights: e.g. "Cyberpunk Megacity:1.6"
        boost_weights_map: Dict[str, float] = {}
        clean_boost_kws: List[str] = []
        for item in (effective_boost_kws or []):
            item_str = str(item).strip()
            if not item_str:
                continue
            if ":" in item_str:
                parts = item_str.rsplit(":", 1)
                try:
                    name = parts[0].strip()
                    w = float(parts[1])
                    boost_weights_map[name.lower()] = w
                    clean_boost_kws.append(name)
                except ValueError:
                    boost_weights_map[item_str.lower()] = 1.0
                    clean_boost_kws.append(item_str)
            else:
                boost_weights_map[item_str.lower()] = 1.0
                clean_boost_kws.append(item_str)

        # Generate concept query vector if positive boost keywords are active
        concept_vec = None
        if clean_boost_kws and self.embedder:
            concept_text = "Thematic Motifs and Elements: " + ", ".join(clean_boost_kws)
            try:
                concept_vec = self.embedder.embed_texts([concept_text])[0]
            except Exception as e:
                print(f"[Recommender Warning] Could not embed concept text: {e}")

        # Concept search weight modulated by mean motif priority multiplier
        avg_boost_weight = (sum(boost_weights_map.values()) / max(1, len(boost_weights_map))) if boost_weights_map else 1.0
        search_concept_weight = 0.45 * avg_boost_weight if clean_boost_kws else 0.0

        # Full global weighted vector search across all 25,101 books
        candidates = self.store.perform_weighted_search(
            base_vector=base_vector,
            concept_query_vector=concept_vec,
            top_k=min(120, max(top_k * 6, 60)),
            weight_plot=max(0.05, weight_plot),
            weight_concept=search_concept_weight,
            genre_filter=genre_filter
        )

        # Filter out target book itself
        candidates = [c for c in candidates if c["id"] != str(target_info["id"])]

        # Multi-Modal Item2Vec Collaborative Taste Scores
        target_id_str = str(target_info.get("id", "")) if target_info else ""
        candidate_ids = [str(c["id"]) for c in candidates]
        collab_scores = self.collab.get_collaborative_scores(target_id_str, candidate_ids)

        from src.style_extractor import StyleExtractor
        t_style = StyleExtractor.analyze_book(target_info) if target_info else {}
        exclude_kws_set = set([k.lower().strip() for k in effective_exclude_kws if k.strip()])

        # Fine-grained stylistic & collaborative scoring
        for idx_c, item in enumerate(candidates):
            base_sim = item["similarity_score"]
            c_style = StyleExtractor.analyze_book(item)
            
            # Fast in-memory bolster
            item = self.enricher.bolster_book(item, fetch_online=False)
            candidates[idx_c] = item

            tone_match = 1.0 if (t_style.get("tone") == c_style.get("tone") and t_style.get("tone") != "Grounded & Dramatic") else 0.0
            style_match = 1.0 if (t_style.get("pov") == c_style.get("pov") and t_style.get("pov") != "Third Person") else 0.0
            pacing_match = 1.0 if (t_style.get("pacing") == c_style.get("pacing") and t_style.get("pacing") != "Moderate Pacing") else 0.0

            item_subclusters = self.extract_subclustered_motifs(item.get("summary", ""), item.get("genres", ""))
            item["subclustered_motifs"] = item_subclusters
            c_kws = set([k.lower().strip() for k in self.extract_concept_keywords(item.get("summary", ""), item.get("genres", ""))])
            item_text = (str(item.get("summary", "")) + " " + str(item.get("genres", ""))).lower()

            # Per-motif weighted overlap bonus
            matched_weight = 0.0
            matching_motif_names = []
            for kw_name, kw_w in boost_weights_map.items():
                if kw_name in c_kws or any(kw_name in ck for ck in c_kws) or kw_name in item_text:
                    matched_weight += kw_w
                    matching_motif_names.append(kw_name.title())

            kw_overlap_bonus = 0.0
            if boost_weights_map:
                total_w = sum(boost_weights_map.values())
                kw_overlap_bonus = (matched_weight / max(1.0, total_w)) * 0.12 * min(2.5, avg_boost_weight)

            # Negative exclusion penalty
            exclude_penalty = 0.0
            if exclude_kws_set:
                matched_excludes = 0
                for ex in exclude_kws_set:
                    if ex in c_kws or any(ex in ck for ck in c_kws) or ex in item_text:
                        matched_excludes += 1
                if matched_excludes > 0:
                    exclude_penalty = 0.30 * matched_excludes

            # Collaborative Item2Vec taste bonus (scaled by weight_community)
            collab_sim = float(collab_scores[idx_c]) if idx_c < len(collab_scores) else 0.5
            collab_bonus = (collab_sim - 0.50) * 0.10 * weight_community

            # Series match bonus
            t_ser = target_info.get("series_info") if target_info else None
            c_ser = item.get("series_info")
            series_bonus = 0.05 if (t_ser and c_ser and t_ser.get("series", "").lower() == c_ser.get("series", "").lower()) else 0.0

            # Calibrate composite score: baseline cosine similarity + stylistic bonuses + per-motif alignment + collaborative - penalty
            stylistic_bonus = (
                (tone_match * 0.05 * weight_tone) + 
                (style_match * 0.04 * weight_style) + 
                (pacing_match * 0.04 * weight_pacing) +
                kw_overlap_bonus +
                collab_bonus +
                series_bonus
            )
            raw_weighted = item.get("weighted_score", base_sim)
            scaled_plot_weight = 0.85 + (weight_plot * 0.15)
            final_score = (raw_weighted * scaled_plot_weight) + stylistic_bonus - exclude_penalty
            final_score = min(0.98, max(0.30, final_score))
            
            # Visual multi-dimensional match breakdown
            plot_match_pct = round(min(99, max(45, base_sim * 100)))
            theme_match_pct = round(min(99, max(40, (0.50 + kw_overlap_bonus * 3.5) * 100)))
            style_match_pct = round(min(99, max(45, (0.60 + (tone_match * 0.18 + style_match * 0.12 + pacing_match * 0.10)) * 100)))
            collab_match_pct = round(min(99, max(35, collab_sim * 100)))
            composite_pct = round(min(99, max(40, final_score * 100)))

            item["similarity_score"] = float(base_sim)
            item["weighted_score"] = float(final_score)
            item["collaborative_affinity"] = round(collab_sim, 2)
            item["style_profile"] = c_style
            item["match_breakdown"] = {
                "plot_pct": plot_match_pct,
                "theme_pct": theme_match_pct,
                "style_pct": style_match_pct,
                "audience_pct": collab_match_pct,
                "composite_pct": composite_pct
            }
            
            if target_info:
                reasons = self.extract_similarity_reasons(target_info, item)
                if matching_motif_names:
                    reasons.append(f"Motif Alignment: {', '.join(matching_motif_names[:2])}")
                if collab_sim >= 0.72:
                    reasons.append("Reader Co-Taste: High community co-reading affinity")
                item["similarity_reasons"] = reasons
            else:
                item["similarity_reasons"] = [f"Global Dense Vector Match ({final_score*100:.1f}%)"]

        candidates.sort(key=lambda x: x.get("weighted_score", x["similarity_score"]), reverse=True)
        final_results = candidates[:top_k]

        return {
            "target_book": target_info,
            "subclustered_motifs": subclustered_motifs,
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
