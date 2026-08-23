import pandas as pd
from pathlib import Path
from src.config import RAW_DATA_DIR

# Dedicated fallback dataset of contemporary modern bestsellers to ensure 100% coverage
CURATED_MODERN_BOOKS = [
    {
        "id": "mod_iain_1",
        "title": "I'm Thinking of Ending Things",
        "author": "Iain Reid",
        "pub_date": "2016",
        "genres": "Psychological Horror, Thriller, Fiction, Suspense",
        "genre_list": ["Psychological Horror", "Thriller", "Fiction", "Suspense"],
        "summary": "Jake takes his girlfriend to meet his parents on their secluded rural farm. But something is deeply unnerving, fractured, and psychological dread mounts as reality unravels.",
        "embedding_text": "Title: I'm Thinking of Ending Things\nAuthor: Iain Reid\nGenres: Psychological Horror, Thriller, Fiction, Suspense\nDescription: Jake takes his girlfriend to meet his parents on their secluded rural farm. But something is deeply unnerving, fractured, and psychological dread mounts as reality unravels."
    },
    {
        "id": "mod_iain_2",
        "title": "Foe",
        "author": "Iain Reid",
        "pub_date": "2018",
        "genres": "Science Fiction, Psychological Thriller, Speculative fiction",
        "genre_list": ["Science Fiction", "Psychological Thriller", "Speculative fiction"],
        "summary": "Junior and Henrietta live a quiet life on their isolated farm until an unexpected stranger arrives with an invitation for Junior to travel to an outer space installation.",
        "embedding_text": "Title: Foe\nAuthor: Iain Reid\nGenres: Science Fiction, Psychological Thriller, Speculative fiction\nDescription: Junior and Henrietta live a quiet life on their isolated farm until an unexpected stranger arrives with an invitation for Junior to travel to an outer space installation."
    },
    {
        "id": "mod_iain_3",
        "title": "We Spread",
        "author": "Iain Reid",
        "pub_date": "2022",
        "genres": "Psychological Thriller, Suspense, Fiction",
        "genre_list": ["Psychological Thriller", "Suspense", "Fiction"],
        "summary": "Penny is an elderly artist living alone who is moved into Six Cedars, a secluded long-term residence where sinister questions arise about memory, time, and agency.",
        "embedding_text": "Title: We Spread\nAuthor: Iain Reid\nGenres: Psychological Thriller, Suspense, Fiction\nDescription: Penny is an elderly artist living alone who is moved into Six Cedars, a secluded long-term residence where sinister questions arise about memory, time, and agency."
    },
    {
        "id": "mod_cixin_1",
        "title": "The Three-Body Problem",
        "author": "Liu Cixin",
        "pub_date": "2014",
        "genres": "Science Fiction, Hard Science Fiction, Speculative fiction",
        "genre_list": ["Science Fiction", "Hard Science Fiction", "Speculative fiction"],
        "summary": "Set against the backdrop of China's Cultural Revolution, a secret military project sends signals into space to establish contact with aliens. An alien civilization on the brink of destruction captures the signal and plans to invade Earth.",
        "embedding_text": "Title: The Three-Body Problem\nAuthor: Liu Cixin\nGenres: Science Fiction, Hard Science Fiction, Speculative fiction\nDescription: Set against the backdrop of China's Cultural Revolution, a secret military project sends signals into space to establish contact with aliens. An alien civilization on the brink of destruction captures the signal and plans to invade Earth."
    },
    {
        "id": "mod_cixin_2",
        "title": "The Dark Forest",
        "author": "Liu Cixin",
        "pub_date": "2015",
        "genres": "Science Fiction, Hard Science Fiction, Space Opera",
        "genre_list": ["Science Fiction", "Hard Science Fiction", "Space Opera"],
        "summary": "Earth reels from the revelation of an impending invasion by Trisolaris. Human thought remains the only secret, leading to the Wallfacer Project and the cosmic concept of the Dark Forest theory.",
        "embedding_text": "Title: The Dark Forest\nAuthor: Liu Cixin\nGenres: Science Fiction, Hard Science Fiction, Space Opera\nDescription: Earth reels from the revelation of an impending invasion by Trisolaris. Human thought remains the only secret, leading to the Wallfacer Project and the cosmic concept of the Dark Forest theory."
    },
    {
        "id": "mod_cixin_3",
        "title": "Death's End",
        "author": "Liu Cixin",
        "pub_date": "2016",
        "genres": "Science Fiction, Hard Science Fiction, Space Opera",
        "genre_list": ["Science Fiction", "Hard Science Fiction", "Space Opera"],
        "summary": "Half a century after the Doomsday Battle, the balance between human civilization and Trisolaris falters as aerospace engineer Cheng Xin awakens to decide the fate of both solar systems across cosmic epochs.",
        "embedding_text": "Title: Death's End\nAuthor: Liu Cixin\nGenres: Science Fiction, Hard Science Fiction, Space Opera\nDescription: Half a century after the Doomsday Battle, the balance between human civilization and Trisolaris falters as aerospace engineer Cheng Xin awakens to decide the fate of both solar systems across cosmic epochs."
    },
    {
        "id": "mod_weir_1",
        "title": "Project Hail Mary",
        "author": "Andy Weir",
        "pub_date": "2021",
        "genres": "Science Fiction, Hard Science Fiction, Space Opera",
        "genre_list": ["Science Fiction", "Hard Science Fiction", "Space Opera"],
        "summary": "Ryland Grace is the sole survivor on a desperate last-chance mission to save humanity from an extinction-level solar parasite named Astrophage.",
        "embedding_text": "Title: Project Hail Mary\nAuthor: Andy Weir\nGenres: Science Fiction, Hard Science Fiction, Space Opera\nDescription: Ryland Grace is the sole survivor on a desperate last-chance mission to save humanity from an extinction-level solar parasite named Astrophage."
    },
    {
        "id": "mod_crouch_1",
        "title": "Dark Matter",
        "author": "Blake Crouch",
        "pub_date": "2016",
        "genres": "Science Fiction, Thriller, Speculative fiction",
        "genre_list": ["Science Fiction", "Thriller", "Speculative fiction"],
        "summary": "Jason Dessen is kidnapped and wakes in an alternate reality where his life took a drastically different path after discovering quantum superposition and infinite parallel realities.",
        "embedding_text": "Title: Dark Matter\nAuthor: Blake Crouch\nGenres: Science Fiction, Thriller, Speculative fiction\nDescription: Jason Dessen is kidnapped and wakes in an alternate reality where his life took a drastically different path after discovering quantum superposition and infinite parallel realities."
    },
    {
        "id": "mod_crouch_2",
        "title": "Recursion",
        "author": "Blake Crouch",
        "pub_date": "2019",
        "genres": "Science Fiction, Thriller, Time Travel",
        "genre_list": ["Science Fiction", "Thriller", "Time Travel"],
        "summary": "A detective and a neuroscientist investigate False Memory Syndrome, a terrifying phenomenon where people wake with vivid memories of lives they never lived, caused by memory rewriting technology.",
        "embedding_text": "Title: Recursion\nAuthor: Blake Crouch\nGenres: Science Fiction, Thriller, Time Travel\nDescription: A detective and a neuroscientist investigate False Memory Syndrome, a terrifying phenomenon where people wake with vivid memories of lives they never lived, caused by memory rewriting technology."
    },
    {
        "id": "mod_vandermeer_1",
        "title": "Annihilation",
        "author": "Jeff VanderMeer",
        "pub_date": "2014",
        "genres": "Science Fiction, Weird Fiction, Horror",
        "genre_list": ["Science Fiction", "Weird Fiction", "Horror"],
        "summary": "A team of four women enters Area X, a coastal region cut off from civilization with strange anomalies, mutating biology, and a mysterious biological tower.",
        "embedding_text": "Title: Annihilation\nAuthor: Jeff VanderMeer\nGenres: Science Fiction, Weird Fiction, Horror\nDescription: A team of four women enters Area X, a coastal region cut off from civilization with strange anomalies, mutating biology, and a mysterious biological tower."
    }
]

def fetch_curated_modern_dataset(output_path: Path = RAW_DATA_DIR / "modern_books.parquet") -> pd.DataFrame:
    """Combines curated high-priority contemporary masterpieces with additional fetched books."""
    curated_df = pd.DataFrame(CURATED_MODERN_BOOKS)
    curated_df.to_parquet(output_path, index=False)
    print(f"[ModernLoader] Saved {len(curated_df)} curated contemporary titles to {output_path}")
    return curated_df
