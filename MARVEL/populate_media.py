import json
import sqlite3
import time
import urllib.error
import urllib.parse
import urllib.request

from config import DATABASE_PATH
from models.database import ensure_database


WIKI_API = "https://en.wikipedia.org/w/api.php"
HEADERS = {"User-Agent": "MarvelVerseExplorer/1.0 (local educational Flask project)"}


CHARACTER_PAGES = {
    "Iron Man": "Iron Man",
    "Spider-Man": "Spider-Man",
    "Thor": "Thor (Marvel Comics)",
    "Hulk": "Hulk",
    "Doctor Strange": "Doctor Strange",
    "Captain America": "Captain America",
    "Black Panther": "Black Panther (character)",
    "Scarlet Witch": "Scarlet Witch",
    "Loki": "Loki (Marvel Comics)",
    "Deadpool": "Deadpool",
    "Wolverine": "Wolverine (character)",
    "Thanos": "Thanos",
    "Daredevil": "Daredevil (Marvel Comics character)",
    "Moon Knight": "Moon Knight",
    "Punisher": "Punisher",
    "Ghost Rider": "Ghost Rider (Johnny Blaze)",
    "Venom": "Venom (character)",
    "Magneto": "Magneto (Marvel Comics)",
    "Jean Grey": "Jean Grey",
    "Silver Surfer": "Silver Surfer",
}


MOVIE_PAGES = {
    "Iron Man": "Iron Man (2008 film)",
    "The Incredible Hulk": "The Incredible Hulk (film)",
    "Iron Man 2": "Iron Man 2",
    "Thor": "Thor (film)",
    "Captain America: The First Avenger": "Captain America: The First Avenger",
    "The Avengers": "The Avengers (2012 film)",
    "Iron Man 3": "Iron Man 3",
    "Thor: The Dark World": "Thor: The Dark World",
    "Captain America: The Winter Soldier": "Captain America: The Winter Soldier",
    "Guardians of the Galaxy": "Guardians of the Galaxy (film)",
    "Avengers: Age of Ultron": "Avengers: Age of Ultron",
    "Ant-Man": "Ant-Man (film)",
    "Captain America: Civil War": "Captain America: Civil War",
    "Doctor Strange": "Doctor Strange (2016 film)",
    "Guardians of the Galaxy Vol. 2": "Guardians of the Galaxy Vol. 2",
    "Spider-Man: Homecoming": "Spider-Man: Homecoming",
    "Thor: Ragnarok": "Thor: Ragnarok",
    "Black Panther": "Black Panther (film)",
    "Avengers: Infinity War": "Avengers: Infinity War",
    "Ant-Man and the Wasp": "Ant-Man and the Wasp",
    "Captain Marvel": "Captain Marvel (film)",
    "Avengers: Endgame": "Avengers: Endgame",
    "Spider-Man: Far From Home": "Spider-Man: Far From Home",
    "Black Widow": "Black Widow (2021 film)",
    "Shang-Chi and the Legend of the Ten Rings": "Shang-Chi and the Legend of the Ten Rings",
    "Eternals": "Eternals (film)",
    "Spider-Man: No Way Home": "Spider-Man: No Way Home",
    "Doctor Strange in the Multiverse of Madness": "Doctor Strange in the Multiverse of Madness",
    "Thor: Love and Thunder": "Thor: Love and Thunder",
    "Black Panther: Wakanda Forever": "Black Panther: Wakanda Forever",
    "Ant-Man and the Wasp: Quantumania": "Ant-Man and the Wasp: Quantumania",
    "Guardians of the Galaxy Vol. 3": "Guardians of the Galaxy Vol. 3",
    "The Marvels": "The Marvels",
    "Deadpool & Wolverine": "Deadpool & Wolverine",
    "Captain America: Brave New World": "Captain America: Brave New World",
    "Thunderbolts*": "Thunderbolts*",
    "The Fantastic Four: First Steps": "The Fantastic Four: First Steps",
    "Spider-Man: Brand New Day": "Spider-Man: Brand New Day",
    "Avengers: Doomsday": "Avengers: Doomsday",
}


SHOW_PAGES = {
    "Loki": "Loki (TV series)",
    "WandaVision": "WandaVision",
    "Moon Knight": "Moon Knight (TV series)",
    "Daredevil": "Daredevil (TV series)",
    "Jessica Jones": "Jessica Jones (TV series)",
    "Agents of SHIELD": "Agents of S.H.I.E.L.D.",
    "Punisher": "The Punisher (TV series)",
    "Ms. Marvel": "Ms. Marvel (miniseries)",
    "What If...?": "What If...? (TV series)",
    "X-Men animated series": "X-Men: The Animated Series",
    "Hawkeye": "Hawkeye (miniseries)",
    "She-Hulk: Attorney at Law": "She-Hulk: Attorney at Law",
}


def fetch_thumbnail(page_title, size=900):
    og_image = fetch_open_graph_image(page_title)
    if og_image:
        return og_image

    params = {
        "action": "query",
        "format": "json",
        "redirects": "1",
        "prop": "pageimages",
        "piprop": "thumbnail",
        "pithumbsize": str(size),
        "titles": page_title,
    }
    url = f"{WIKI_API}?{urllib.parse.urlencode(params)}"
    request = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(request, timeout=15) as response:
        payload = json.loads(response.read().decode("utf-8"))
    pages = payload.get("query", {}).get("pages", {})
    for page in pages.values():
        thumbnail = page.get("thumbnail", {})
        source = thumbnail.get("source")
        if source:
            return source
    return ""


def fetch_open_graph_image(page_title):
    path = urllib.parse.quote(page_title.replace(" ", "_"), safe="._()")
    url = f"https://en.wikipedia.org/wiki/{path}"
    request = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(request, timeout=15) as response:
        html = response.read().decode("utf-8", errors="ignore")

    marker = '<meta property="og:image" content="'
    start = html.find(marker)
    if start != -1:
        start += len(marker)
        end = html.find('"', start)
        if end != -1:
            return html[start:end]

    return first_article_image(html)


def first_article_image(html):
    blocked_fragments = (
        "Symbol_",
        "Semi-protection",
        "OOjs",
        "Commons-logo",
        "Wikidata",
        "Wikiquote",
        "Wiktionary",
        "Flag_of_",
        "Edit-clear",
        "Question_book",
        "Ambox",
    )
    cursor = 0
    while True:
        start = html.find("<img", cursor)
        if start == -1:
            return ""
        src_marker = 'src="'
        src_start = html.find(src_marker, start)
        if src_start == -1:
            cursor = start + 4
            continue
        src_start += len(src_marker)
        src_end = html.find('"', src_start)
        if src_end == -1:
            return ""
        src = html[src_start:src_end]
        cursor = src_end
        if "upload.wikimedia.org" not in src:
            continue
        if any(fragment in src for fragment in blocked_fragments):
            continue
        if src.startswith("//"):
            src = f"https:{src}"
        return src


def update_media(table, key_column, image_column, mapping):
    updated = 0
    skipped = []
    with sqlite3.connect(DATABASE_PATH) as db:
        for item_name, page_title in mapping.items():
            try:
                image_url = fetch_thumbnail(page_title)
                time.sleep(0.35)
            except urllib.error.HTTPError as error:
                if error.code == 429:
                    time.sleep(3)
                    try:
                        image_url = fetch_thumbnail(page_title)
                    except Exception as retry_error:
                        skipped.append((item_name, f"fetch failed: {retry_error}"))
                        continue
                else:
                    skipped.append((item_name, f"fetch failed: {error}"))
                    continue
            except Exception as error:
                skipped.append((item_name, f"fetch failed: {error}"))
                continue

            if not image_url:
                skipped.append((item_name, "no thumbnail found"))
                continue

            cursor = db.execute(
                f"UPDATE {table} SET {image_column} = ? WHERE {key_column} = ?",
                (image_url, item_name),
            )
            if cursor.rowcount:
                updated += 1
            else:
                skipped.append((item_name, "not found in database"))
        db.commit()
    return updated, skipped


def main():
    ensure_database()
    jobs = [
        ("characters", "name", "image_url", CHARACTER_PAGES),
        ("movies", "title", "poster_url", MOVIE_PAGES),
        ("shows", "title", "poster_url", SHOW_PAGES),
    ]
    for table, key_column, image_column, mapping in jobs:
        updated, skipped = update_media(table, key_column, image_column, mapping)
        print(f"{table}: updated {updated}/{len(mapping)}")
        for name, reason in skipped:
            print(f"  - {name}: {reason}")


if __name__ == "__main__":
    main()
