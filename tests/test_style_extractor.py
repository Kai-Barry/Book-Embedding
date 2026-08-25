import unittest
from src.style_extractor import StyleExtractor

class TestStyleExtractor(unittest.TestCase):
    def test_pov_detection_first_person(self):
        book = {
            "title": "I'm Thinking of Ending Things",
            "summary": "I am on the road with Jake. I keep thinking of ending things. My thoughts are racing as we drive through the blizzard."
        }
        res = StyleExtractor.analyze_book(book)
        self.assertEqual(res["pov"], "First Person")

    def test_pov_detection_third_person(self):
        book = {
            "title": "Dune",
            "summary": "Paul Atreides arrives on Arrakis with his family. The Duke recognizes the trap laid by House Harkonnen."
        }
        res = StyleExtractor.analyze_book(book)
        self.assertEqual(res["pov"], "Third Person")

    def test_pacing_detection(self):
        slow_book = {
            "title": "Slow Contemplation",
            "summary": "A slow-burn psychological study of solitude, memory, grief, and atmospheric silence in winter."
        }
        fast_book = {
            "title": "Action Chase",
            "summary": "A fast-paced thriller featuring adrenaline, explosions, chase sequences, and a countdown clock."
        }
        self.assertIn("Slow-Burn", StyleExtractor.analyze_book(slow_book)["pacing"])
        self.assertIn("Fast-Paced", StyleExtractor.analyze_book(fast_book)["pacing"])

    def test_prose_density_and_tone(self):
        book = {
            "title": "Cosmic Horror",
            "summary": "The eldritch abyss opens in deep space, sending chilling terror and dread into the cosmic void."
        }
        res = StyleExtractor.analyze_book(book)
        self.assertIn("tone", res)
        self.assertIn("prose_style", res)
        self.assertIn("prose_density", res)

if __name__ == "__main__":
    unittest.main()
