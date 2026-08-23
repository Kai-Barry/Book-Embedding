import re
from typing import Dict, Any

class StyleExtractor:
    """
    Extracts structured narrative mechanics, POV, pacing, and tone
    from book summaries and text using linguistic heuristics.
    """

    @staticmethod
    def extract_pov(text: str) -> str:
        """Determines Point of View (First Person, Third Person, etc.)."""
        lower = text.lower()
        # Check for first-person narrative cues
        first_person_cues = len(re.findall(r"\b(i|my|me|myself|we|our|us)\b", lower))
        third_person_cues = len(re.findall(r"\b(he|she|his|her|him|they|their|them)\b", lower))
        
        # Explicit summary phrases
        if "first-person" in lower or "first person" in lower or "narrated by" in lower:
            return "First Person"
        if "third-person" in lower or "third person" in lower:
            return "Third Person"
        if first_person_cues > 8 and first_person_cues > third_person_cues * 0.4:
            return "First Person"
        if "epistolary" in lower or "letters" in lower or "diary" in lower:
            return "Epistolary / Multi-POV"
        return "Third Person"

    @staticmethod
    def extract_pacing(text: str, genres: str) -> str:
        """Determines story pacing (Slow Burn vs Fast-Paced)."""
        combined = (text + " " + genres).lower()
        fast_keywords = ["thriller", "action", "chase", "race against time", "cliffhanger", "propulsive", "fast-paced", "explosive", "heist", "battle"]
        slow_keywords = ["slow-burn", "meditative", "character study", "philosophical", "creeping", "atmosphere", "contemplative", "quiet", "pastoral", "family saga"]
        
        fast_score = sum(1 for k in fast_keywords if k in combined)
        slow_score = sum(1 for k in slow_keywords if k in combined)
        
        if fast_score > slow_score:
            return "Fast-Paced"
        elif slow_score > fast_score:
            return "Slow-Burn"
        else:
            return "Moderate Pacing"

    @staticmethod
    def extract_prose_density(genres: str, summary: str) -> str:
        """Infers prose density & stylistic voice."""
        combined = (genres + " " + summary).lower()
        if any(k in combined for k in ["poetry", "literary", "philosophical", "poetic", "lyrical", "allegory"]):
            return "Lyrical & Literary"
        elif any(k in combined for k in ["hard science fiction", "technical", "physics", "military", "procedural"]):
            return "Hard & Technical"
        elif any(k in combined for k in ["horror", "gothic", "psychological", "noir", "dread"]):
            return "Atmospheric & Psychological"
        else:
            return "Direct & Accessible"

    @staticmethod
    def extract_atmospheric_tone(genres: str, summary: str) -> str:
        """Extracts dominant atmospheric tone."""
        combined = (genres + " " + summary).lower()
        if any(k in combined for k in ["dread", "psychological", "isolation", "claustrophobic", "terror", "paranoia"]):
            return "Existential Dread & Tension"
        elif any(k in combined for k in ["space", "cosmic", "galaxy", "universe", "alien", "astronomy", "quantum"]):
            return "Cosmic Wonder & Intellectual Awe"
        elif any(k in combined for k in ["magic", "kingdom", "dragon", "wizard", "quest", "realm"]):
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
    def analyze_book(cls, row: Dict[str, Any]) -> Dict[str, str]:
        """Extracts complete stylistic profile for a book."""
        text = str(row.get("summary", ""))
        genres = str(row.get("genres", ""))
        return {
            "pov": cls.extract_pov(text),
            "pacing": cls.extract_pacing(text, genres),
            "prose_density": cls.extract_prose_density(genres, text),
            "tone": cls.extract_atmospheric_tone(genres, text)
        }
