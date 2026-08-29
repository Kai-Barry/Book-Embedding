import pandas as pd
from pathlib import Path
from src.config import RAW_DATA_DIR

# Dedicated comprehensive dataset of contemporary modern bestsellers with rich narrative plot summaries
CURATED_MODERN_BOOKS = [
    {
        "id": "mod_orphan_1",
        "title": "Orphan X",
        "author": "Gregg Hurwitz",
        "pub_date": "2016",
        "genres": "Thriller, Action, Suspense, Espionage",
        "genre_list": ["Thriller", "Action", "Suspense", "Espionage"],
        "summary": (
            "Evan Smoak was taken from a Baltimore group home at age twelve and raised in the covert government "
            "assassination initiative known as the Orphan Program. Trained as Orphan X, he was engineered into the ultimate "
            "black-ops operative until he broke away, utilizing his formidable skills to reinvent himself as the Nowhere Man—an "
            "urban legend who aids desperate individuals with nowhere else to turn.\n\n"
            "[Plot & Core Narrative]: Operating from a fortified high-tech penthouse in Los Angeles, Evan lives by rigid, inviolable "
            "commandments instilled by his mentor Jack Johns. When a routine rescue mission uncovers a rogue conspiracy within the "
            "shattered remnants of the Orphan Program, Evan finds himself hunted by his former handler and a lethal successor operative. "
            "As danger encroaches upon his civilian neighbors, Evan must navigate explosive tactical firefights, surveillance counter-measures, "
            "and his own moral conscience to protect an innocent family."
        ),
        "embedding_text": (
            "Title: Orphan X\nAuthor: Gregg Hurwitz\nGenres: Thriller, Action, Suspense, Espionage\n"
            "Description: Evan Smoak was raised in the covert government Orphan Program as an elite black-ops assassin before breaking away "
            "to become the Nowhere Man, helping desperate people in life-or-death crises while being hunted by rogue operatives."
        )
    },
    {
        "id": "mod_orphan_2",
        "title": "The Nowhere Man",
        "author": "Gregg Hurwitz",
        "pub_date": "2017",
        "genres": "Thriller, Action, Suspense, Crime",
        "genre_list": ["Thriller", "Action", "Suspense", "Crime"],
        "summary": (
            "Spun out of the lethal world of the Orphan Program, Evan Smoak—the Nowhere Man—is ambushed, drugged, and imprisoned in a secluded "
            "mountain fortress by a sadistic syndicate leader who intends to break him and seize his fortune.\n\n"
            "[Plot & Core Narrative]: Stripped of his high-tech weapons and communication gear, Evan must use pure physiological discipline, "
            "tactical improvisation, and psychological endurance to engineer an impossible escape from a sensory-deprivation cell, all while "
            "racing against time to save a young woman who called his emergency line before his abduction."
        ),
        "embedding_text": (
            "Title: The Nowhere Man\nAuthor: Gregg Hurwitz\nGenres: Thriller, Action, Suspense, Crime\n"
            "Description: Evan Smoak is captured in an impenetrable fortress and must rely on raw intellect and tactical combat to escape "
            "while fulfilling a promise to rescue a desperate victim."
        )
    },
    {
        "id": "mod_orphan_3",
        "title": "Hellbent",
        "author": "Gregg Hurwitz",
        "pub_date": "2018",
        "genres": "Thriller, Action, Espionage, Suspense",
        "genre_list": ["Thriller", "Action", "Espionage", "Suspense"],
        "summary": (
            "When Jack Johns, the father figure who recruited and trained Evan Smoak, is ruthlessly murdered by the corrupt head of the Orphan "
            "Program, Jack leaves behind one final, hazardous mission for Evan.\n\n"
            "[Plot & Core Narrative]: Evan must locate and protect Jack's surrogate daughter, an awkward teenage computer hacker who holds "
            "explosive evidence capable of bringing down the entire rogue government apparatus. Evan faces overwhelming military forces in "
            "a relentless pursuit that tests his human vulnerability."
        ),
        "embedding_text": (
            "Title: Hellbent\nAuthor: Gregg Hurwitz\nGenres: Thriller, Action, Espionage, Suspense\n"
            "Description: Evan Smoak seeks vengeance for his fallen mentor while protecting a brilliant young hacker targeted by corrupt government assassins."
        )
    },
    {
        "id": "mod_iain_1",
        "title": "I'm Thinking of Ending Things",
        "author": "Iain Reid",
        "pub_date": "2016",
        "genres": "Psychological Horror, Thriller, Fiction, Suspense",
        "genre_list": ["Psychological Horror", "Thriller", "Fiction", "Suspense"],
        "summary": (
            "A young woman embarks on a winter road trip with her new boyfriend, Jake, to visit his parents on their remote dairy farm, "
            "despite the persistent internal thought that she is thinking of ending their relationship.\n\n"
            "[Plot & Core Narrative]: As snow blankets the landscape, the evening takes a deeply surreal and unnerving turn at the farmhouse. "
            "Jake's parents exhibit erratic, shifting ages, and disturbing childhood relics emerge in the basement. On the drive home through a "
            "raging blizzard, tension escalates into existential dread as Jake makes an inexplicable detour into a deserted high school, blurring "
            "the boundary between psychological delusion, memory, and horrific reality."
        ),
        "embedding_text": (
            "Title: I'm Thinking of Ending Things\nAuthor: Iain Reid\nGenres: Psychological Horror, Thriller, Fiction, Suspense\n"
            "Description: A young woman travels with her boyfriend to his isolated childhood farm, where reality fractures into escalating psychological horror, uncanny time shifts, and existential dread."
        )
    },
    {
        "id": "mod_iain_2",
        "title": "Foe",
        "author": "Iain Reid",
        "pub_date": "2018",
        "genres": "Science Fiction, Psychological Thriller, Speculative fiction",
        "genre_list": ["Science Fiction", "Psychological Thriller", "Speculative fiction"],
        "summary": (
            "Junior and Henrietta live a quiet, solitary existence farming a dying plot of land in a near-future world ravaged by climate collapse. "
            "Their tranquil routine is abruptly shattered when a representative from the aerospace corporation OuterMore arrives with an unsettling announcement.\n\n"
            "[Plot & Core Narrative]: Junior has been selected to travel to a monumental space station orbiting Earth. To ensure Henrietta is not left alone, "
            "the company intends to construct an exact, biomechanical synthetic duplicate of Junior to live with her during his absence. As invasive psychological "
            "assessments begin, paranoia and alienation infect the couple's marriage, culminating in a devastating revelation about identity and companionship."
        ),
        "embedding_text": (
            "Title: Foe\nAuthor: Iain Reid\nGenres: Science Fiction, Psychological Thriller, Speculative fiction\n"
            "Description: A husband on an isolated farm is drafted for a space station mission while a synthetic duplicate is prepared to replace him, sparking intense psychological paranoia."
        )
    },
    {
        "id": "mod_iain_3",
        "title": "We Spread",
        "author": "Iain Reid",
        "pub_date": "2022",
        "genres": "Psychological Thriller, Suspense, Fiction, Mystery",
        "genre_list": ["Psychological Thriller", "Suspense", "Fiction", "Mystery"],
        "summary": (
            "Penny, an elderly artist who has lived alone in her apartment for decades following the death of her long-time partner, is moved into "
            "Six Cedars, a secluded long-term residential facility managed by attentive caretakers.\n\n"
            "[Plot & Core Narrative]: At first, the tranquil environment and artistic encouragement spark a creative renaissance in Penny. However, strange "
            "inconsistencies soon mount: passage of time feels manipulated, fellow residents exhibit uncanny regressions, and Penny's agency begins to erode. "
            "A masterclass in slow-burn existential suspense examining aging, memory, and institutional control."
        ),
        "embedding_text": (
            "Title: We Spread\nAuthor: Iain Reid\nGenres: Psychological Thriller, Suspense, Fiction, Mystery\n"
            "Description: An elderly artist in a secluded residence experiences uncanny shifts in time and memory, raising unsettling questions about aging and autonomy."
        )
    },
    {
        "id": "mod_cixin_1",
        "title": "The Three-Body Problem",
        "author": "Liu Cixin",
        "pub_date": "2014",
        "genres": "Science Fiction, Hard Science Fiction, Speculative fiction, Space Opera",
        "genre_list": ["Science Fiction", "Hard Science Fiction", "Speculative fiction", "Space Opera"],
        "summary": (
            "Against the turbulent backdrop of China's Cultural Revolution, a covert military astrophysics project sends high-powered radio signals into deep space. "
            "A dying extraterrestrial civilization in the Trisolaran three-star system captures the broadcast and prepares a four-hundred-year invasion fleet toward Earth.\n\n"
            "[Plot & Core Narrative]: Decades later in modern Beijing, nanomaterials researcher Wang Miao witnesses unexplained scientific anomalies and a phantom countdown "
            "imprinted on his vision. Investigating the suicides of prominent theoretical physicists, Wang enters the hyper-realistic virtual reality game 'Three Body', uncovering "
            "the chaotic mechanics of the alien homeworld and the emergence of human fifth-column factions divided between welcoming alien salvation and planetary defense."
        ),
        "embedding_text": (
            "Title: The Three-Body Problem\nAuthor: Liu Cixin\nGenres: Science Fiction, Hard Science Fiction, Speculative fiction, Space Opera\n"
            "Description: Humanity establishes contact with an alien civilization residing in a chaotic three-star system, sparking a cosmic crisis across physics, virtual worlds, and planetary survival."
        )
    },
    {
        "id": "mod_cixin_2",
        "title": "The Dark Forest",
        "author": "Liu Cixin",
        "pub_date": "2015",
        "genres": "Science Fiction, Hard Science Fiction, Space Opera",
        "genre_list": ["Science Fiction", "Hard Science Fiction", "Space Opera"],
        "summary": (
            "As Earth prepares for the Trisolaran invasion fleet due to arrive in four centuries, subatomic alien probes called Sophons lock down fundamental physics research "
            "and eavesdrop on all human communications. In response, humanity appoints four individuals as Wallfacers—commanders granted unrestricted power to devise secret defensive strategies.\n\n"
            "[Plot & Core Narrative]: Sociologist Luo Ji, an unassuming academic targeted for assassination by the aliens, unravels the fundamental axioms of Cosmic Sociology: the Dark Forest theory, "
            "which posits that every civilization in the cosmos is an armed hunter lurking in the dark, where exposing planetary coordinates invites instantaneous interstellar annihilation."
        ),
        "embedding_text": (
            "Title: The Dark Forest\nAuthor: Liu Cixin\nGenres: Science Fiction, Hard Science Fiction, Space Opera\n"
            "Description: Humanity battles alien surveillance through the Wallfacer initiative while sociologist Luo Ji discovers the terrifying cosmic sociology of the Dark Forest theory."
        )
    },
    {
        "id": "mod_cixin_3",
        "title": "Death's End",
        "author": "Liu Cixin",
        "pub_date": "2016",
        "genres": "Science Fiction, Hard Science Fiction, Space Opera",
        "genre_list": ["Science Fiction", "Hard Science Fiction", "Space Opera"],
        "summary": (
            "Half a century after the Dark Forest deterrence established a tense peace between Earth and Trisolaris, aerospace engineer Cheng Xin awakens from hibernation to serve "
            "as the new Swordholder responsible for the cosmic broadcast trigger.\n\n"
            "[Plot & Core Narrative]: When deterrence fails, a monumental saga spanning millions of years unfolds across multiple dimensional collapses, solar system vector foil attacks, "
            "lightspeed spacecraft escapes, and the eventual thermal death and rebirth of the universe itself."
        ),
        "embedding_text": (
            "Title: Death's End\nAuthor: Liu Cixin\nGenres: Science Fiction, Hard Science Fiction, Space Opera\n"
            "Description: The sweeping conclusion to the Three-Body trilogy tracing dimensional collapses, lightspeed space travel, and the ultimate fate of human civilization."
        )
    },
    {
        "id": "mod_weir_1",
        "title": "Project Hail Mary",
        "author": "Andy Weir",
        "pub_date": "2021",
        "genres": "Science Fiction, Hard Science Fiction, Space Opera, Adventure",
        "genre_list": ["Science Fiction", "Hard Science Fiction", "Space Opera", "Adventure"],
        "summary": (
            "Ryland Grace is the sole survivor on a desperate, last-chance interstellar mission to save Earth from an extinction-level solar parasite called Astrophage that is dimming the sun.\n\n"
            "[Plot & Core Narrative]: Awakening from a medically induced coma with severe amnesia, Grace must use first-principles scientific deduction, chemistry, and physics to remember his identity "
            "and mission. Arriving in the Tau Ceti star system, he encounters an alien starship piloted by an arachnid-like xenobiologist named Rocky. Together, the two scientists forge an extraordinary "
            "interstellar friendship, combining their engineering ingenuity to devise a cure for both their dying homeworlds."
        ),
        "embedding_text": (
            "Title: Project Hail Mary\nAuthor: Andy Weir\nGenres: Science Fiction, Hard Science Fiction, Space Opera, Adventure\n"
            "Description: An amnesiac astronaut teams up with an intelligent alien engineer to solve a cosmic solar crisis using rigorous scientific problem-solving."
        )
    },
    {
        "id": "mod_michaelides_1",
        "title": "The Silent Patient",
        "author": "Alex Michaelides",
        "pub_date": "2019",
        "genres": "Psychological Thriller, Mystery, Suspense, Crime",
        "genre_list": ["Psychological Thriller", "Mystery", "Suspense", "Crime"],
        "summary": (
            "Alicia Berenson's life is seemingly perfect. A celebrated painter married to an in-demand fashion photographer, she lives in a grand house overlooking a park in London. "
            "One evening, her husband returns home late from a fashion shoot, and Alicia shoots him five times in the face and never speaks another word.\n\n"
            "[Plot & Core Narrative]: Alicia's refusal to talk or offer any explanation turns a domestic tragedy into a global mystery, sending the price of her art skyrocketing. "
            "Confined to The Grove, a secure psychiatric facility in North London, she encounters Theo Faber, a dedicated criminal psychotherapist who becomes obsessed with unlocking her motive. "
            "As Theo delves into Alicia's history, a labyrinthine web of obsession, infidelity, and psychological trauma unravels with a jaw-dropping twist."
        ),
        "embedding_text": (
            "Title: The Silent Patient\nAuthor: Alex Michaelides\nGenres: Psychological Thriller, Mystery, Suspense, Crime\n"
            "Description: A famous painter shoots her husband and never speaks again; a forensic psychotherapist becomes consumed with uncovering her shocking motives."
        )
    },
    {
        "id": "mod_crouch_1",
        "title": "Dark Matter",
        "author": "Blake Crouch",
        "pub_date": "2016",
        "genres": "Science Fiction, Thriller, Speculative fiction",
        "genre_list": ["Science Fiction", "Thriller", "Speculative fiction"],
        "summary": (
            "Jason Dessen is an unassuming Chicago physics professor living a content family life with his wife Daniela and son Charlie. Walking home one evening, he is abducted by a masked stranger, "
            "injected with an unknown compound, and wakes up strapped to a gurney surrounded by scientists in hazmat suits congratulating him on completing an impossible breakthrough.\n\n"
            "[Plot & Core Narrative]: In this alternate reality, Jason never married Daniela and never settled for teaching; instead, he built the Box, a multi-dimensional portal accessing infinite parallel realities. "
            "To return to his true family, Jason must navigate an endless multiverse of alternate versions of his life, battling alternate iterations of himself who will stop at nothing to steal his original reality."
        ),
        "embedding_text": (
            "Title: Dark Matter\nAuthor: Blake Crouch\nGenres: Science Fiction, Thriller, Speculative fiction\n"
            "Description: A physicist is kidnapped into an alternate reality and must navigate a perilous multiverse of parallel dimensions to reclaim his family."
        )
    },
    {
        "id": "mod_crouch_2",
        "title": "Recursion",
        "author": "Blake Crouch",
        "pub_date": "2019",
        "genres": "Science Fiction, Thriller, Time Travel",
        "genre_list": ["Science Fiction", "Thriller", "Time Travel"],
        "summary": (
            "Across the globe, people are falling victim to False Memory Syndrome—a terrifying affliction where victims suddenly awaken with vivid, heartbreaking memories of complete alternative lifetimes they never lived.\n\n"
            "[Plot & Core Narrative]: In New York City, detective Barry Sutton investigates the suicide of an afflicted woman, uncovering a clandestine research laboratory. Meanwhile, neuroscientist Helena Smith "
            "develops a revolutionary neural chair intended to preserve memories for Alzheimer's patients. When weaponized by military interests to rewrite the timeline itself, reality fractures into recursive apocalyptic "
            "loops that threaten the fabric of human history."
        ),
        "embedding_text": (
            "Title: Recursion\nAuthor: Blake Crouch\nGenres: Science Fiction, Thriller, Time Travel\n"
            "Description: A detective and a neuroscientist battle against a memory-mapping technology capable of rewriting timelines and triggering reality-collapsing time loops."
        )
    },
    {
        "id": "mod_kuang_1",
        "title": "Yellowface",
        "author": "R. F. Kuang",
        "pub_date": "2023",
        "genres": "Satire, Psychological Fiction, Literary Fiction, Metafiction",
        "genre_list": ["Satire", "Psychological Fiction", "Literary Fiction", "Metafiction"],
        "summary": (
            "Athena Liu is a literary darling with a multi-book deal, prestigious accolades, and effortless critical acclaim. June Hayward is an overlooked writer whose debut novel barely made a ripple.\n\n"
            "[Plot & Core Narrative]: When June witnesses Athena's freak choking death in a DC apartment, June acts on sudden impulse: she steals Athena's finished masterpiece manuscript about the Chinese Labour Corps during WWI. "
            "Editing the work and rebranding herself with the ethnically ambiguous pseudonym 'Juniper Song', June shoots to the top of the New York Times bestseller list. But as internet sleuths, rival editors, and supernatural guilt "
            "close in, June's stolen fame spirals into psychological mania and public reckoning."
        ),
        "embedding_text": (
            "Title: Yellowface\nAuthor: R. F. Kuang\nGenres: Satire, Psychological Fiction, Literary Fiction, Metafiction\n"
            "Description: A struggling author steals her deceased Asian friend's manuscript and becomes a bestseller under a pseudonym, sparking a razor-sharp satire of publishing and identity."
        )
    },
    {
        "id": "mod_yarros_1",
        "title": "Fourth Wing",
        "author": "Rebecca Yarros",
        "pub_date": "2023",
        "genres": "Fantasy, Romance, High Fantasy, Dragons",
        "genre_list": ["Fantasy", "Romance", "High Fantasy", "Dragons"],
        "summary": (
            "Twenty-year-old Violet Sorrengail was destined for the quiet life of a Scribe at Basgiath War College. However, her formidable mother, the commanding general, orders Violet to join the elite, deadly Riders Quadrant.\n\n"
            "[Plot & Core Narrative]: With brittle bones and smaller stature, Violet enters a brutal academy where dragons do not bond with frail humans—they incinerate them. Facing lethal obstacle courses, scheming rivals, and "
            "the commanding wingleader Xaden Riorson—whose father led the rebellion Violet's mother crushed—Violet must rely on sharp wits, tactical discipline, and forbidden bonds to survive as war erupts across the kingdom."
        ),
        "embedding_text": (
            "Title: Fourth Wing\nAuthor: Rebecca Yarros\nGenres: Fantasy, Romance, High Fantasy, Dragons\n"
            "Description: A scholar is forced into an elite dragon-riding military college where cadets compete in brutal trials to bond with dragons while uncovering kingdom conspiracies."
        )
    },
    {
        "id": "mod_zevin_1",
        "title": "Tomorrow, and Tomorrow, and Tomorrow",
        "author": "Gabrielle Zevin",
        "pub_date": "2022",
        "genres": "Literary Fiction, Romance, Drama, Coming-of-Age",
        "genre_list": ["Literary Fiction", "Romance", "Drama", "Coming-of-Age"],
        "summary": (
            "On a freezing December day during his junior year at Harvard, Sam Masur spots Sadie Green on a crowded subway platform. Rekindling a childhood bond formed over video games in a hospital game room, the two brilliant "
            "friends embark on a creative partnership that transforms them into legendary video game designers before age twenty-five.\n\n"
            "[Plot & Core Narrative]: Spanning thirty years from Cambridge to Venice Beach, their blockbuster video games bring fame, fortune, and profound emotional friction. A multi-layered ode to artistic collaboration, "
            "disability, grief, and the enduring complexity of non-romantic platonic love."
        ),
        "embedding_text": (
            "Title: Tomorrow, and Tomorrow, and Tomorrow\nAuthor: Gabrielle Zevin\nGenres: Literary Fiction, Romance, Drama, Coming-of-Age\n"
            "Description: A rich narrative following two childhood friends who become famous video game designers, exploring creative passion, grief, and thirty years of platonic love."
        )
    }
]

def fetch_curated_modern_dataset(output_path: Path = RAW_DATA_DIR / "modern_books.parquet") -> pd.DataFrame:
    """Combines curated high-priority contemporary masterpieces with additional fetched books."""
    curated_df = pd.DataFrame(CURATED_MODERN_BOOKS)
    curated_df.to_parquet(output_path, index=False)
    print(f"[ModernLoader] Saved {len(curated_df)} curated contemporary titles to {output_path}")
    return curated_df
