import re
from typing import Dict, Any

class StyleExtractor:
    """
    Extracts structured narrative mechanics, POV, pacing, writing style, and tone
    from book summaries and text using high-precision linguistic heuristics.
    """

    @staticmethod
    def extract_pov(text: str, title: str = "") -> str:
        """Determines Point of View with high precision."""
        text_lower = (text or "").lower()
        title_lower = (title or "").lower()

        # Explicit summary phrases
        if any(p in text_lower for p in ["first-person", "first person", "narrated in the first person", "told in the first person", "narrated by the author", "confessional memoir", "told from my perspective"]):
            return "First Person"
        if any(p in text_lower for p in ["epistolary", "letters and diary", "diary entries", "journal entries", "multiple points of view", "multiple pov", "shifting viewpoints", "alternating narrators", "dual perspectives"]):
            return "Epistolary / Multi-POV"

        # Check for first-person title indicators (e.g., "I'm Thinking of Ending Things", "I, Robot", "My Sister's Keeper", "Call Me By Your Name", "I Am Legend")
        title_first_person = bool(re.search(r"\b(i'm|i am|i|my|me|we|myself)\b", title_lower))

        # Check for first-person pronouns in the text summary
        # Since publisher blurbs describe books in 3rd person, ANY direct first-person usage is a strong signal of 1st-person voice/excerpts
        first_person_pronouns = re.findall(r"\b(i|i'm|my|myself|me)\b", text_lower)
        fp_count = len(first_person_pronouns)

        # Quotes with first-person
        quotes = re.findall(r'["\u201c\u201d\u2018\u2019\']([^"\u201c\u201d\u2018\u2019\']+)["\u201c\u201d\u2018\u2019\']', text or "")
        fp_in_quotes = any(bool(re.search(r"\b(i|i'm|my|me|myself|we|our)\b", q.lower())) for q in quotes)

        if title_first_person or fp_in_quotes or fp_count >= 2:
            return "First Person"

        # Multi-POV / Ensemble Cast cues
        if any(p in text_lower for p in ["ensemble cast", "interweaving lives", "multiple characters", "interlocking stories", "panoramic saga", "cast of characters"]):
            return "Third Person (Multiple POV)"

        return "Third Person"

    @staticmethod
    def extract_pacing(text: str, genres: str = "") -> str:
        """Determines story pacing using word-boundary matching and contextual signals."""
        t_low = (text or "").lower()
        g_low = (genres or "").lower()

        slow_keywords = [
            r"\bslow[- ]burn\b", r"\bcreeping\b", r"\bdread\b", r"\batmospheric\b",
            r"\bmeditative\b", r"\bintrospective\b", r"\bcontemplative\b", r"\bdeliberate\b",
            r"\bcharacter study\b", r"\bphilosophical\b", r"\bunraveling\b", r"\bsolitude\b",
            r"\blingers?\b", r"\bquiet\b", r"\bpastoral\b", r"\bfamily saga\b",
            r"\bgradual\b", r"\bhaunting\b", r"\bbrooding\b", r"\bexistential\b",
            r"\bclaustrophobic\b", r"\bunease\b", r"\bpsychological suspense\b"
        ]

        fast_keywords = [
            r"\bfast[- ]paced\b", r"\bpropulsive\b", r"\bpage[- ]turner\b", r"\brollercoaster\b",
            r"\baction[- ]packed\b", r"\brelentless\b", r"\bbreakneck\b", r"\brace against time\b",
            r"\bcliffhanger\b", r"\bexplosive\b", r"\bheist\b", r"\badrenaline\b",
            r"\bnon[- ]stop\b", r"\bticking clock\b", r"\baction thriller\b", r"\brapid-fire\b"
        ]

        slow_score = sum(1 for pat in slow_keywords if re.search(pat, t_low))
        fast_score = sum(1 for pat in fast_keywords if re.search(pat, t_low))

        # Contextual genre weighting (secondary weight, not dominant)
        if any(g in g_low for g in ["action", "techno-thriller", "military science fiction", "spy thriller"]):
            fast_score += 1
        if any(g in g_low for g in ["literary", "poetry", "philosophy", "gothic", "psychological horror"]):
            slow_score += 1

        if slow_score > fast_score:
            return "Slow-Burn"
        elif fast_score > slow_score:
            return "Fast-Paced"
        else:
            return "Moderate Pacing"

    @staticmethod
    def extract_prose_style(genres: str, summary: str) -> Dict[str, str]:
        """Provides an intuitive, clear explanation of the author's writing style."""
        combined = ((genres or "") + " " + (summary or "")).lower()
        if any(k in combined for k in ["poetry", "poetic", "lyrical", "allegory", "philosophical"]):
            return {
                "label": "Lyrical & Atmospheric",
                "description": "Rich in metaphor, contemplative imagery, and thematic depth"
            }
        elif any(k in combined for k in ["psychological", "dread", "unease", "haunting", "gothic", "isolation", "introspective"]):
            return {
                "label": "Atmospheric & Introspective",
                "description": "Mood-driven psychological depth with haunting, immersive prose"
            }
        elif any(k in combined for k in ["hard science fiction", "technical", "physics", "procedural", "hard sci-fi"]):
            return {
                "label": "Technical & World-Rich",
                "description": "Grounded in speculative detail, high-concept systems, and rigorous logic"
            }
        elif any(k in combined for k in ["fast-paced", "propulsive", "page-turner", "dialogue", "crisp", "thriller", "action"]):
            return {
                "label": "Sharp & Direct",
                "description": "Propulsive, accessible storytelling with brisk narrative velocity"
            }
        elif any(k in combined for k in ["high fantasy", "epic", "mythic", "legend", "kingdom", "saga"]):
            return {
                "label": "Epic & World-Building",
                "description": "Expansive mythology, grand scale world architecture, and formal dialogue"
            }
        else:
            return {
                "label": "Grounded & Narrative",
                "description": "Clear, immersive commercial storytelling focused on character and plot"
            }

    @staticmethod
    def extract_atmospheric_tone(genres: str, summary: str) -> str:
        """Extracts dominant atmospheric tone."""
        combined = ((genres or "") + " " + (summary or "")).lower()
        if any(k in combined for k in ["dread", "psychological", "isolation", "claustrophobic", "terror", "paranoia", "unease"]):
            return "Existential Dread & Tension"
        elif any(k in combined for k in ["space", "cosmic", "galaxy", "universe", "alien", "astronomy", "quantum"]):
            return "Cosmic Wonder & Intellectual Awe"
        elif any(k in combined for k in ["magic", "kingdom", "dragon", "wizard", "quest", "realm", "fantasy"]):
            return "Mythic & Enchanting"
        elif any(k in combined for k in ["murder", "noir", "detective", "crime", "darkness", "gritty"]):
            return "Noir & Gritty Suspense"
        elif any(k in combined for k in ["humor", "comedy", "satire", "parody", "whimsical"]):
            return "Satirical & Witty"
        elif any(k in combined for k in ["romance", "love", "heart", "passion"]):
            return "Emotional & Romantic"
        else:
            return "Grounded & Dramatic"

    @classmethod
    def analyze_book(cls, row: Dict[str, Any]) -> Dict[str, Any]:
        """Extracts complete stylistic profile for a book."""
        text = str(row.get("summary", ""))
        title = str(row.get("title", ""))
        genres = str(row.get("genres", ""))
        prose_info = cls.extract_prose_style(genres, text)
        return {
            "pov": cls.extract_pov(text, title),
            "pacing": cls.extract_pacing(text, genres),
            "prose_style": prose_info["label"],
            "prose_description": prose_info["description"],
            "prose_density": prose_info["label"],
            "tone": cls.extract_atmospheric_tone(genres, text)
        }
