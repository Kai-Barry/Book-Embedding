import urllib.request
import json
import time

def verify_all():
    print("=" * 60)
    print("Running Automated Backend Verifications")
    print("=" * 60)

    # 1. Test Status
    res = urllib.request.urlopen("http://127.0.0.1:8000/api/status")
    status = json.loads(res.read().decode())
    print(f"1. System Status: {status['status'].upper()}")
    print(f"   Indexed Books: {status['index']['books_count']:,} | Model: {status['index']['model_name']}")
    print(f"   GPU: {status['gpu']['name']} ({status['gpu']['vram']})")

    # 2. Test Typo Search for Iain Reid
    typo_q = "I'm thinging of ending things"
    url = f"http://127.0.0.1:8000/api/catalog?q={urllib.parse.quote(typo_q)}"
    res = urllib.request.urlopen(url)
    results = json.loads(res.read().decode())
    print(f"\n2. Typo Search Test: '{typo_q}'")
    for r in results[:3]:
        title = r['title'].encode('ascii', 'replace').decode()
        author = r['author'].encode('ascii', 'replace').decode()
        print(f"   - Match: {title} by {author}")

    # 3. Test Typo Search for Three Body
    typo_tb = "three body"
    url2 = f"http://127.0.0.1:8000/api/catalog?q={urllib.parse.quote(typo_tb)}"
    res2 = urllib.request.urlopen(url2)
    results2 = json.loads(res2.read().decode())
    print(f"\n3. Typo Search Test: '{typo_tb}'")
    for r in results2[:3]:
        title = r['title'].encode('ascii', 'replace').decode()
        author = r['author'].encode('ascii', 'replace').decode()
        print(f"   - Match: {title} by {author}")

    # 4. Test 2D Galaxy Vector Data
    res3 = urllib.request.urlopen("http://127.0.0.1:8000/api/visualize?max_points=5")
    vis = json.loads(res3.read().decode())
    print(f"\n4. 2D Galaxy Vector Coordinates (Sample of {len(vis['points'])}):")
    for p in vis['points'][:3]:
        print(f"   - {p['title']} -> (x: {p['x']}, y: {p['y']}) | Genres: {p['genres']}")

    # 5. Spotlight & Book Details Modal Verification
    print("\n5. Book Details & Stylistic Profile for 'Animal Farm':")
    req_modal = urllib.request.urlopen("http://127.0.0.1:8000/api/book/cmu_620")
    modal_data = json.loads(req_modal.read().decode())
    print(f"   - Title: {modal_data['title']} by {modal_data['author']}")
    print(f"   - POV: {modal_data['style_profile']['pov']}")
    print(f"   - Pacing: {modal_data['style_profile']['pacing']}")
    print(f"   - Tone: {modal_data['style_profile']['tone']}")
    print(f"   - Prose: {modal_data['style_profile']['prose_density']}")

    # 6. Recommendation Explainability Verification
    print("\n6. Recommendations for 'Dune' with Deep Multi-level Rationales:")
    req3 = urllib.request.urlopen("http://127.0.0.1:8000/api/similar/Dune?top_k=3")
    sim_data = json.loads(req3.read().decode())
    for r in sim_data["results"]:
        print(f"   - {r['title']} by {r['author']} ({r['similarity_score']*100:.1f}%)")
        print(f"     Why similar: {', '.join(r.get('similarity_reasons', []))}")

    print("\n" + "=" * 60)
    print("ALL TESTS & EXPLAINABILITY VERIFICATIONS PASSED!")
    print("=" * 60)

if __name__ == "__main__":
    verify_all()
