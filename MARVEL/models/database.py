import json
import sqlite3
from pathlib import Path

from flask import current_app, g
from werkzeug.security import generate_password_hash

from config import ADMIN_PASSWORD, ADMIN_USERNAME, DATABASE_PATH


def get_db():
    if "db" not in g:
        DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
        g.db = sqlite3.connect(DATABASE_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(_error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_app(app):
    app.teardown_appcontext(close_db)


def execute_schema(db):
    schema_path = Path(__file__).resolve().parent.parent / "database" / "schema.sql"
    db.executescript(schema_path.read_text(encoding="utf-8"))


def to_json(value):
    return json.dumps(value, ensure_ascii=True)


def row_to_dict(row):
    item = dict(row)
    for key, value in item.items():
        if isinstance(value, str) and value.startswith("["):
            try:
                item[key] = json.loads(value)
            except json.JSONDecodeError:
                pass
    return item


def ensure_column(db, table, column, definition):
    columns = {row["name"] for row in db.execute(f"PRAGMA table_info({table})").fetchall()}
    if column not in columns:
        db.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")


def migrate_db(db):
    ensure_column(db, "characters", "image_url", "TEXT")
    ensure_column(db, "movies", "poster_url", "TEXT")
    ensure_column(db, "shows", "poster_url", "TEXT")
    db.commit()


CHARACTERS = [
    {
        "name": "Iron Man",
        "alias": "Tony Stark",
        "category": "Hero",
        "image": "iron-man.svg",
        "tagline": "Armored futurist with a reactor-powered conscience.",
        "origin": "A weapons genius survives captivity by building the first Iron Man armor, then turns his company and his life toward protection instead of profit.",
        "powers": ["Powered armor", "Genius engineering", "Flight", "Repulsor weapons", "AI-assisted tactics"],
        "weaknesses": ["Human vulnerability", "Dependency on technology", "Ego", "PTSD"],
        "teams": ["Avengers", "Illuminati"],
        "enemies": ["Mandarin", "Obadiah Stane", "Whiplash", "Ultron", "Thanos"],
        "arcs": ["Demon in a Bottle", "Extremis", "Armor Wars", "Civil War"],
        "mcu": ["Iron Man", "The Avengers", "Iron Man 3", "Avengers: Endgame"],
        "variants": ["Superior Iron Man", "Iron Lad", "Infamous Iron Man"],
        "timeline": "2008: declares himself Iron Man and launches the modern MCU age.",
        "power_level": 92,
        "bio": "Tony Stark is the collision of celebrity, guilt, brilliance, and sacrifice. His armor turns engineering into superhero myth.",
    },
    {
        "name": "Spider-Man",
        "alias": "Peter Parker / Miles Morales",
        "category": "Hero",
        "image": "spider-man.svg",
        "tagline": "Friendly neighborhood hero with multiverse-sized responsibility.",
        "origin": "A bitten teenager gains spider-like abilities and learns that great power must answer to great responsibility.",
        "powers": ["Wall-crawling", "Spider-sense", "Super agility", "Web shooters", "Enhanced strength"],
        "weaknesses": ["Young age", "Loved ones in danger", "Guilt", "Limited resources"],
        "teams": ["Avengers", "Fantastic Four", "Spider-Army"],
        "enemies": ["Green Goblin", "Doctor Octopus", "Venom", "Kingpin", "Mysterio"],
        "arcs": ["The Night Gwen Stacy Died", "Kraven's Last Hunt", "Spider-Verse", "Ultimate Spider-Man"],
        "mcu": ["Captain America: Civil War", "Spider-Man: Homecoming", "Spider-Man: No Way Home"],
        "variants": ["Miles Morales", "Spider-Gwen", "Spider-Man 2099", "Noir Spider-Man"],
        "timeline": "2016: recruited during the Avengers conflict, then becomes central to multiverse breaches.",
        "power_level": 88,
        "bio": "Spider-Man is Marvel's street-level heart: funny, bruised, overworked, and impossible to keep down.",
    },
    {
        "name": "Thor",
        "alias": "Thor Odinson",
        "category": "Hero",
        "image": "thor.svg",
        "tagline": "God of Thunder, king in exile, cosmic brawler.",
        "origin": "An arrogant Asgardian prince is cast to Earth and learns humility before becoming one of the universe's great defenders.",
        "powers": ["Lightning", "Super strength", "Longevity", "Mjolnir and Stormbreaker", "Cosmic durability"],
        "weaknesses": ["Pride", "Family trauma", "Magic manipulation", "Loss of purpose"],
        "teams": ["Avengers", "Revengers", "Asgardians"],
        "enemies": ["Loki", "Hela", "Malekith", "Gorr", "Surtur"],
        "arcs": ["Ragnarok", "God Butcher", "Siege", "War of the Realms"],
        "mcu": ["Thor", "The Avengers", "Thor: Ragnarok", "Thor: Love and Thunder"],
        "variants": ["Jane Foster Thor", "Beta Ray Bill", "Old King Thor"],
        "timeline": "2011: arrives on Earth, linking mythology to the wider cosmic MCU.",
        "power_level": 96,
        "bio": "Thor carries Marvel's mythic scale, blending ancient tragedy with heroic thunder and a surprisingly tender heart.",
    },
    {
        "name": "Hulk",
        "alias": "Bruce Banner",
        "category": "Hero",
        "image": "hulk.svg",
        "tagline": "The angrier he gets, the stronger he gets.",
        "origin": "Gamma radiation transforms scientist Bruce Banner into a green powerhouse connected to rage, trauma, and survival.",
        "powers": ["Gamma strength", "Regeneration", "Durability", "Thunderclap", "Leaping"],
        "weaknesses": ["Emotional instability", "Mind control", "Collateral damage", "Banner/Hulk conflict"],
        "teams": ["Avengers", "Defenders", "Warbound"],
        "enemies": ["Abomination", "Leader", "Red Hulk", "Maestro"],
        "arcs": ["Planet Hulk", "World War Hulk", "Immortal Hulk", "Future Imperfect"],
        "mcu": ["The Incredible Hulk", "The Avengers", "Thor: Ragnarok", "She-Hulk"],
        "variants": ["Maestro", "Professor Hulk", "Immortal Hulk"],
        "timeline": "2008: gamma incident becomes a major superhuman case before Avengers assemble.",
        "power_level": 95,
        "bio": "Hulk is a monster story, a trauma story, and a superhero story all fighting for the same page.",
    },
    {
        "name": "Doctor Strange",
        "alias": "Stephen Strange",
        "category": "Hero",
        "image": "doctor-strange.svg",
        "tagline": "Master of the Mystic Arts and guardian of impossible doors.",
        "origin": "A brilliant surgeon loses his hands, seeks healing, and discovers a hidden architecture of magic and dimensions.",
        "powers": ["Sorcery", "Astral projection", "Portals", "Time manipulation", "Relic mastery"],
        "weaknesses": ["Arrogance", "Forbidden magic", "Physical limits", "Multiversal temptation"],
        "teams": ["Avengers", "Defenders", "Midnight Sons"],
        "enemies": ["Dormammu", "Baron Mordo", "Nightmare", "Shuma-Gorath"],
        "arcs": ["The Oath", "Triumph and Torment", "Damnation", "Death of Doctor Strange"],
        "mcu": ["Doctor Strange", "Avengers: Infinity War", "Spider-Man: No Way Home", "Multiverse of Madness"],
        "variants": ["Sinister Strange", "Defender Strange", "Supreme Strange"],
        "timeline": "2016: becomes a sorcerer and later watches millions of futures against Thanos.",
        "power_level": 94,
        "bio": "Strange brings occult architecture to Marvel: spells, bargains, relics, and the price of knowing too much.",
    },
    {
        "name": "Captain America",
        "alias": "Steve Rogers / Sam Wilson",
        "category": "Hero",
        "image": "captain-america.svg",
        "tagline": "A shield, a symbol, and a stubborn moral compass.",
        "origin": "A frail volunteer receives the super-soldier serum during World War II and becomes a hero out of conviction, not muscle.",
        "powers": ["Peak human strength", "Shield combat", "Leadership", "Tactical instinct", "Endurance"],
        "weaknesses": ["Human limits", "Idealism exploited", "Time displacement", "Political pressure"],
        "teams": ["Avengers", "Invaders", "Secret Avengers"],
        "enemies": ["Red Skull", "Winter Soldier", "Baron Zemo", "Hydra"],
        "arcs": ["The Winter Soldier", "Civil War", "Secret Empire", "Man Out of Time"],
        "mcu": ["The First Avenger", "The Winter Soldier", "Civil War", "Endgame", "Brave New World"],
        "variants": ["Sam Wilson Captain America", "Nomad", "Captain Carter"],
        "timeline": "1943: fights Hydra, then reawakens decades later into a complicated future.",
        "power_level": 86,
        "bio": "Captain America is Marvel's argument that goodness can still be radical when the world gets cynical.",
    },
    {
        "name": "Black Panther",
        "alias": "T'Challa / Shuri",
        "category": "Hero",
        "image": "black-panther.svg",
        "tagline": "Wakanda's protector, monarch, scientist, and myth.",
        "origin": "The Black Panther mantle is passed through Wakanda's royal line, empowered by the heart-shaped herb and duty to a hidden nation.",
        "powers": ["Enhanced senses", "Vibranium suit", "Martial arts", "Strategy", "Royal resources"],
        "weaknesses": ["National duty", "Political isolation", "Vibranium dependency", "Family grief"],
        "teams": ["Avengers", "Fantastic Four", "Wakandan forces"],
        "enemies": ["Killmonger", "Klaw", "Namor", "Man-Ape"],
        "arcs": ["Who Is the Black Panther?", "Doomwar", "A Nation Under Our Feet", "Intergalactic Empire of Wakanda"],
        "mcu": ["Civil War", "Black Panther", "Infinity War", "Wakanda Forever"],
        "variants": ["Shuri Black Panther", "Star-Lord T'Challa", "King Killmonger"],
        "timeline": "2016: Wakanda steps from secrecy into global and cosmic politics.",
        "power_level": 89,
        "bio": "Black Panther blends monarchy, technology, ancestry, and superhero action into one of Marvel's richest worlds.",
    },
    {
        "name": "Scarlet Witch",
        "alias": "Wanda Maximoff",
        "category": "Hero / Antihero",
        "image": "scarlet-witch.svg",
        "tagline": "Chaos magic wrapped around grief and reality itself.",
        "origin": "Wanda's powers grow from experimentation, loss, and ancient chaos magic that makes her one of Marvel's most dangerous beings.",
        "powers": ["Chaos magic", "Telekinesis", "Reality warping", "Mind manipulation", "Hex fields"],
        "weaknesses": ["Grief", "Darkhold corruption", "Isolation", "Emotional overload"],
        "teams": ["Avengers", "Brotherhood of Mutants"],
        "enemies": ["Agatha Harkness", "Chthon", "Ultron", "Doctor Strange"],
        "arcs": ["House of M", "Avengers Disassembled", "Children's Crusade", "Vision and the Scarlet Witch"],
        "mcu": ["Age of Ultron", "WandaVision", "Multiverse of Madness"],
        "variants": ["Earth-838 Wanda", "Age of Apocalypse Wanda", "No More Mutants Wanda"],
        "timeline": "2015: joins the Avengers; 2023: the Westview hex makes grief a reality event.",
        "power_level": 98,
        "bio": "Wanda is tragic, frightening, and deeply human: a character whose pain can rewrite the panel around her.",
    },
    {
        "name": "Loki",
        "alias": "Loki Laufeyson",
        "category": "Antihero",
        "image": "loki.svg",
        "tagline": "God of mischief, stories, and glorious purpose.",
        "origin": "Raised as an Asgardian prince but born a Frost Giant, Loki becomes a trickster shaped by envy, identity, and survival.",
        "powers": ["Illusions", "Shapeshifting", "Sorcery", "Daggers", "Temporal awareness"],
        "weaknesses": ["Insecurity", "Ambition", "Family wounds", "Trust issues"],
        "teams": ["Asgardians", "TVA", "Young Avengers"],
        "enemies": ["Thor", "Avengers", "Kang variants", "The Void"],
        "arcs": ["Journey Into Mystery", "Agent of Asgard", "Vote Loki", "Loki: Sorcerer Supreme"],
        "mcu": ["Thor", "The Avengers", "Loki", "Infinity War"],
        "variants": ["Sylvie", "Classic Loki", "Kid Loki", "President Loki"],
        "timeline": "2012 variant escapes with the Tesseract, cracking open TVA and multiverse lore.",
        "power_level": 90,
        "bio": "Loki began as a villain and became one of Marvel's finest studies of reinvention.",
    },
    {
        "name": "Deadpool",
        "alias": "Wade Wilson",
        "category": "Antihero",
        "image": "deadpool.svg",
        "tagline": "Regenerating mercenary with a mouth and a meta problem.",
        "origin": "A terminal diagnosis and brutal experiments unlock Wade Wilson's healing factor, leaving him scarred, unstable, and weirdly heroic.",
        "powers": ["Regeneration", "Weapons mastery", "Fourth-wall breaks", "Agility", "Unpredictability"],
        "weaknesses": ["Mental instability", "Recklessness", "Cancer suppressed by healing", "Moral chaos"],
        "teams": ["X-Force", "Mercs for Money", "Thunderbolts"],
        "enemies": ["Ajax", "T-Ray", "Evil Deadpool", "Taskmaster"],
        "arcs": ["Deadpool Kills the Marvel Universe", "The Good, the Bad and the Ugly", "Dead Presidents"],
        "mcu": ["Deadpool & Wolverine"],
        "variants": ["Lady Deadpool", "Dogpool", "Headpool", "Kidpool"],
        "timeline": "2024: jumps into MCU-adjacent continuity through TVA-flavored multiverse chaos.",
        "power_level": 87,
        "bio": "Deadpool is action comedy with a healing factor: bloody, oddly sincere, and allergic to quiet panels.",
    },
    {
        "name": "Wolverine",
        "alias": "Logan / James Howlett",
        "category": "Hero",
        "image": "wolverine.svg",
        "tagline": "Adamantium claws, old wounds, impossible endurance.",
        "origin": "A mutant with bone claws and healing is weaponized by military programs, then spends decades trying to reclaim his humanity.",
        "powers": ["Healing factor", "Adamantium claws", "Enhanced senses", "Combat experience", "Longevity"],
        "weaknesses": ["Berserker rage", "Memory trauma", "Magnetic manipulation", "Adamantium poisoning"],
        "teams": ["X-Men", "X-Force", "Avengers", "Alpha Flight"],
        "enemies": ["Sabretooth", "Omega Red", "Weapon X", "Magneto"],
        "arcs": ["Weapon X", "Old Man Logan", "Enemy of the State", "Death of Wolverine"],
        "mcu": ["Deadpool & Wolverine"],
        "variants": ["Old Man Logan", "Patch", "Age of Apocalypse Logan"],
        "timeline": "Multiverse variants carry Fox-era X-Men history toward the MCU.",
        "power_level": 91,
        "bio": "Wolverine is Marvel's hard-bitten survivor: every fight leaves a scar, even when his body heals.",
    },
    {
        "name": "Thanos",
        "alias": "The Mad Titan",
        "category": "Villain",
        "image": "thanos.svg",
        "tagline": "Cosmic tyrant obsessed with balance and inevitability.",
        "origin": "Born on Titan, Thanos becomes a nihilistic conqueror whose intellect and power make him a universal threat.",
        "powers": ["Titan strength", "Cosmic strategy", "Infinity Stones", "Durability", "War command"],
        "weaknesses": ["Obsession", "Arrogance", "Death fixation", "Emotional blind spots"],
        "teams": ["Black Order", "Infinity Watch"],
        "enemies": ["Avengers", "Guardians of the Galaxy", "Silver Surfer", "Adam Warlock"],
        "arcs": ["Infinity Gauntlet", "Thanos Quest", "Infinity", "The Thanos Imperative"],
        "mcu": ["Guardians of the Galaxy", "Infinity War", "Endgame"],
        "variants": ["King Thanos", "Zombie Thanos", "What If...? Thanos"],
        "timeline": "2018: snaps half of life away, defining the Infinity Saga's climax.",
        "power_level": 99,
        "bio": "Thanos is the blockbuster villain as cosmic philosophy gone rotten.",
    },
    {
        "name": "Daredevil",
        "alias": "Matt Murdock",
        "category": "Hero",
        "image": "daredevil.svg",
        "tagline": "The Devil of Hell's Kitchen hears every lie.",
        "origin": "Blinded by radioactive chemicals, Matt Murdock develops radar-like senses and becomes both lawyer and vigilante.",
        "powers": ["Radar sense", "Acrobatics", "Martial arts", "Enhanced hearing", "Legal expertise"],
        "weaknesses": ["Human durability", "Catholic guilt", "Sonic overload", "Double life"],
        "teams": ["Defenders", "Marvel Knights"],
        "enemies": ["Kingpin", "Bullseye", "The Hand", "Typhoid Mary"],
        "arcs": ["Born Again", "Guardian Devil", "The Man Without Fear", "Shadowland"],
        "mcu": ["Daredevil", "Spider-Man: No Way Home", "Daredevil: Born Again"],
        "variants": ["Shadowland Daredevil", "Earth X Daredevil"],
        "timeline": "Street-level continuity folds into the larger MCU through legal and vigilante crossovers.",
        "power_level": 82,
        "bio": "Daredevil makes superheroics feel close enough to bruise: rooftops, courtrooms, and impossible faith.",
    },
    {
        "name": "Moon Knight",
        "alias": "Marc Spector / Steven Grant / Jake Lockley",
        "category": "Hero",
        "image": "moon-knight.svg",
        "tagline": "Fist of Khonshu, fractured and ferocious.",
        "origin": "Mercenary Marc Spector is left for dead and resurrected as the avatar of the Egyptian moon god Khonshu.",
        "powers": ["Combat skill", "Moon-themed weapons", "Tactical identities", "Divine empowerment", "Pain tolerance"],
        "weaknesses": ["Dissociation", "Khonshu manipulation", "Human injury", "Memory gaps"],
        "teams": ["Midnight Sons", "Secret Avengers"],
        "enemies": ["Bushman", "Arthur Harrow", "Black Spectre", "Sun King"],
        "arcs": ["From the Dead", "The Bottom", "Age of Khonshu", "Moon Knight by Lemire"],
        "mcu": ["Moon Knight"],
        "variants": ["Mr. Knight", "Ultimate Moon Knight", "Age of Khonshu Moon Knight"],
        "timeline": "Modern supernatural branch of the MCU expands through gods beyond Asgard.",
        "power_level": 83,
        "bio": "Moon Knight is a supernatural noir hero where every mask has a voice.",
    },
    {
        "name": "Punisher",
        "alias": "Frank Castle",
        "category": "Antihero",
        "image": "punisher.svg",
        "tagline": "A one-man war with no clean ending.",
        "origin": "After his family is murdered, veteran Frank Castle wages a brutal campaign against organized crime.",
        "powers": ["Military tactics", "Firearms", "Interrogation", "Endurance", "Urban warfare"],
        "weaknesses": ["No powers", "Obsession", "Isolation", "Escalating violence"],
        "teams": ["Marvel Knights", "Thunderbolts"],
        "enemies": ["Jigsaw", "Kingpin", "The Russian", "Barracuda"],
        "arcs": ["Welcome Back, Frank", "Born", "The Slavers", "Punisher MAX"],
        "mcu": ["Daredevil", "The Punisher", "Daredevil: Born Again"],
        "variants": ["Cosmic Ghost Rider", "Franken-Castle", "2099 Punisher"],
        "timeline": "Street-level Marvel explores vigilante extremity through Castle's war.",
        "power_level": 78,
        "bio": "The Punisher is less wish fulfillment than warning label: vengeance stripped of glamour.",
    },
    {
        "name": "Ghost Rider",
        "alias": "Johnny Blaze / Robbie Reyes",
        "category": "Antihero",
        "image": "ghost-rider.svg",
        "tagline": "Hellfire on wheels and judgment in chains.",
        "origin": "A cursed rider bonds with a Spirit of Vengeance and hunts guilty souls across highways and dimensions.",
        "powers": ["Hellfire", "Penance Stare", "Mystic chains", "Demonic vehicle", "Near immortality"],
        "weaknesses": ["Host conflict", "Holy magic", "Demonic bargains", "Innocent blood"],
        "teams": ["Midnight Sons", "Thunderbolts"],
        "enemies": ["Mephisto", "Blackheart", "Zarathos", "Lilith"],
        "arcs": ["Road to Damnation", "Trail of Tears", "Hearts of Darkness", "Damnation"],
        "mcu": ["Agents of SHIELD"],
        "variants": ["Robbie Reyes", "Cosmic Ghost Rider", "Alejandra Jones"],
        "timeline": "Supernatural Marvel widens through demonic pacts and vengeance mythology.",
        "power_level": 93,
        "bio": "Ghost Rider makes every chase scene feel like judgment day with a flaming engine.",
    },
    {
        "name": "Venom",
        "alias": "Eddie Brock / Symbiote",
        "category": "Antihero",
        "image": "venom.svg",
        "tagline": "Alien hunger trying to become a protector.",
        "origin": "A rejected alien symbiote bonds with Eddie Brock, creating a monstrous mirror of Spider-Man.",
        "powers": ["Symbiote strength", "Shapeshifting", "Webbing", "Camouflage", "Regeneration"],
        "weaknesses": ["Sonic attacks", "Fire", "Host conflict", "Hunger"],
        "teams": ["Lethal Protectors", "Guardians of the Galaxy"],
        "enemies": ["Carnage", "Spider-Man", "Knull", "Life Foundation"],
        "arcs": ["Lethal Protector", "Maximum Carnage", "King in Black", "Agent Venom"],
        "mcu": ["Spider-Man: No Way Home mid-credit connection"],
        "variants": ["Agent Venom", "Gwenom", "King Venom"],
        "timeline": "Symbiote mythology brushes MCU reality through multiverse leakage.",
        "power_level": 88,
        "bio": "Venom is body horror with a buddy-comedy heartbeat and a very large appetite.",
    },
    {
        "name": "Magneto",
        "alias": "Erik Lehnsherr / Max Eisenhardt",
        "category": "Villain / Antihero",
        "image": "magneto.svg",
        "tagline": "Master of magnetism, survivor, revolutionary.",
        "origin": "A Holocaust survivor develops magnetic powers and fights for mutant survival through methods that terrify the world.",
        "powers": ["Magnetism", "Metal manipulation", "Flight", "Force fields", "Electromagnetic control"],
        "weaknesses": ["Trauma", "Extremism", "Psychic attack", "Plastic and nonmetal tactics"],
        "teams": ["Brotherhood of Mutants", "X-Men", "Quiet Council"],
        "enemies": ["X-Men", "Sentinels", "Red Skull", "Apocalypse"],
        "arcs": ["God Loves, Man Kills", "Fatal Attractions", "House of X", "Age of Apocalypse"],
        "mcu": ["X-Men legacy continuity"],
        "variants": ["Age of Apocalypse Magneto", "Ultimate Magneto", "House of M Magneto"],
        "timeline": "Mutant history creates a parallel political mythology awaiting wider MCU integration.",
        "power_level": 97,
        "bio": "Magneto is one of Marvel's most complicated antagonists: often wrong, rarely simple.",
    },
    {
        "name": "Jean Grey",
        "alias": "Marvel Girl / Phoenix",
        "category": "Hero",
        "image": "jean-grey.svg",
        "tagline": "A telepath touched by cosmic fire.",
        "origin": "Jean Grey becomes one of Xavier's first students, later bonding with the Phoenix Force and reshaping cosmic mutant destiny.",
        "powers": ["Telepathy", "Telekinesis", "Phoenix Force", "Cosmic resurrection", "Psychic shields"],
        "weaknesses": ["Phoenix corruption", "Emotional overload", "Cosmic possession", "Psychic warfare"],
        "teams": ["X-Men", "X-Factor", "Quiet Council"],
        "enemies": ["Dark Phoenix", "Mister Sinister", "Hellfire Club", "Cassandra Nova"],
        "arcs": ["The Dark Phoenix Saga", "Phoenix Resurrection", "New X-Men", "Inferno"],
        "mcu": ["X-Men legacy continuity"],
        "variants": ["Dark Phoenix", "White Phoenix of the Crown", "Age of Apocalypse Jean"],
        "timeline": "Mutant cosmic stories connect Earth prejudice with universal stakes.",
        "power_level": 99,
        "bio": "Jean Grey is Marvel's brightest flame and one of its most haunting cautionary tales.",
    },
    {
        "name": "Silver Surfer",
        "alias": "Norrin Radd",
        "category": "Hero",
        "image": "silver-surfer.svg",
        "tagline": "Cosmic wanderer on a board of impossible light.",
        "origin": "Norrin Radd sacrifices himself to serve Galactus and save Zenn-La, becoming the Silver Surfer before rediscovering compassion.",
        "powers": ["Power Cosmic", "Faster-than-light travel", "Energy manipulation", "Matter transmutation", "Cosmic senses"],
        "weaknesses": ["Galactus bond", "Isolation", "Cosmic loneliness", "Moral burden"],
        "teams": ["Defenders", "Annihilators", "Heralds of Galactus"],
        "enemies": ["Galactus", "Mephisto", "Thanos", "Annihilus"],
        "arcs": ["Parable", "Requiem", "The Coming of Galactus", "Annihilation"],
        "mcu": ["The Fantastic Four: First Steps"],
        "variants": ["Fallen One", "Keeper", "Shalla-Bal Surfer"],
        "timeline": "Cosmic herald lore connects Fantastic Four mythology to galaxy-level threats.",
        "power_level": 98,
        "bio": "The Silver Surfer turns superhero comics into space opera poetry.",
    },
]


MOVIES = [
    ("Iron Man", "Phase 1", 2008, "Tony Stark builds a suit in captivity and becomes the first public Avenger.", "Tony Stark, Pepper Potts, James Rhodes", "Obadiah Stane / Iron Monger", "Nick Fury introduces the Avengers Initiative.", "2008 after Stark's captivity.", "Launches Stark tech, SHIELD, and the Avengers path.", "Tales of Suspense and Iron Man origin comics.", 94, "https://www.youtube.com/embed/8ugaeA-nMTc"),
    ("The Incredible Hulk", "Phase 1", 2008, "Bruce Banner searches for a cure while hunted by military forces.", "Bruce Banner, Betty Ross, Thunderbolt Ross", "Abomination", "Tony Stark meets Ross in a bar.", "2008, around Iron Man 2.", "Gamma science later returns through Avengers and She-Hulk.", "Hulk origin and Abomination stories.", 67, "https://www.youtube.com/embed/xbqNb2PFKKA"),
    ("Iron Man 2", "Phase 1", 2010, "Stark faces public pressure, poisoning, and enemies weaponizing his legacy.", "Tony Stark, Natasha Romanoff, James Rhodes", "Whiplash and Justin Hammer", "Coulson finds Mjolnir in New Mexico.", "2010 during Fury's Big Week.", "Introduces Black Widow and War Machine.", "Armor Wars and Demon in a Bottle echoes.", 72, "https://www.youtube.com/embed/BoohRoVA9WQ"),
    ("Thor", "Phase 1", 2011, "Thor is banished to Earth and learns humility before reclaiming Mjolnir.", "Thor, Jane Foster, Loki, Odin", "Loki", "Selvig encounters the Tesseract and Loki's influence.", "2010 during Fury's Big Week.", "Brings Asgard and cosmic mythology into the MCU.", "Journey into Mystery Thor mythology.", 77, "https://www.youtube.com/embed/JOddp-nlNvQ"),
    ("Captain America: The First Avenger", "Phase 1", 2011, "Steve Rogers becomes the super-soldier symbol of WWII.", "Steve Rogers, Peggy Carter, Bucky Barnes", "Red Skull", "Steve wakes up in modern New York.", "1943-1945, with modern coda.", "Introduces Tesseract, Hydra, and Steve's displacement.", "Golden Age Captain America stories.", 80, "https://www.youtube.com/embed/JerVrbLldXw"),
    ("The Avengers", "Phase 1", 2012, "Earth's heroes assemble to stop Loki and the Chitauri invasion.", "Iron Man, Captain America, Thor, Hulk, Black Widow, Hawkeye", "Loki and the Chitauri", "Thanos is revealed; shawarma stinger.", "2012 Battle of New York.", "Defines the Avengers as a world-changing force.", "Avengers #1 and Infinity Stone build-up.", 91, "https://www.youtube.com/embed/eOrNdBpGMv8"),
    ("Iron Man 3", "Phase 2", 2013, "Tony Stark confronts trauma and the weaponized Extremis program.", "Tony Stark, Pepper Potts, Rhodey", "Aldrich Killian", "Tony tells the story to Bruce Banner.", "Late 2012 after Battle of New York.", "Explores PTSD after Avengers.", "Extremis by Warren Ellis.", 79, "https://www.youtube.com/embed/Ke1Y3P9D0Bc"),
    ("Thor: The Dark World", "Phase 2", 2013, "Thor battles Malekith as the Aether threatens the Nine Realms.", "Thor, Jane Foster, Loki", "Malekith", "Aether delivered to the Collector; Loki impersonates Odin.", "2013 after Avengers.", "Names the Aether as an Infinity Stone.", "Dark Elves and Thor cosmic lore.", 66, "https://www.youtube.com/embed/npvJ9FTgZbM"),
    ("Captain America: The Winter Soldier", "Phase 2", 2014, "Steve uncovers Hydra inside SHIELD and faces his lost friend Bucky.", "Steve Rogers, Natasha Romanoff, Sam Wilson", "Winter Soldier / Alexander Pierce", "Strucker studies the twins; Bucky visits Smithsonian exhibit.", "2014 after Avengers.", "Destroys SHIELD and introduces Falcon.", "Winter Soldier by Ed Brubaker.", 92, "https://www.youtube.com/embed/7SlILk2WMTI"),
    ("Guardians of the Galaxy", "Phase 2", 2014, "A band of misfits protects the Power Stone from Ronan.", "Star-Lord, Gamora, Drax, Rocket, Groot", "Ronan the Accuser", "Howard the Duck appears in the Collector's ruins.", "2014 cosmic branch.", "Expands the MCU into deep space and Thanos lore.", "Annihilation-era Guardians influences.", 92, "https://www.youtube.com/embed/d96cjJhvlMA"),
    ("Avengers: Age of Ultron", "Phase 2", 2015, "Tony and Bruce's AI peacekeeping plan becomes a global extinction threat.", "Avengers, Wanda Maximoff, Vision", "Ultron", "Thanos takes the Infinity Gauntlet.", "2015 after Hydra clean-up.", "Creates Vision and pushes Avengers toward Civil War.", "Ultron comics and Vision origin.", 76, "https://www.youtube.com/embed/tmeOjFno6Do"),
    ("Ant-Man", "Phase 2", 2015, "Scott Lang becomes a shrinking hero during a heist for Hank Pym.", "Scott Lang, Hope van Dyne, Hank Pym", "Yellowjacket", "Hope receives the Wasp suit; Falcon tracks Scott.", "2015 after Age of Ultron.", "Introduces Quantum Realm technology.", "Ant-Man legacy comics.", 83, "https://www.youtube.com/embed/pWdKf3MneyI"),
    ("Captain America: Civil War", "Phase 3", 2016, "The Avengers fracture over oversight, guilt, and Bucky's past.", "Steve Rogers, Tony Stark, Black Panther, Spider-Man", "Helmut Zemo", "Bucky rests in Wakanda; Peter's Spider-signal appears.", "2016 after Lagos.", "Introduces Black Panther and Spider-Man.", "Civil War by Mark Millar and Steve McNiven.", 90, "https://www.youtube.com/embed/dKrVegVI0Us"),
    ("Doctor Strange", "Phase 3", 2016, "Stephen Strange leaves surgery behind to defend reality with magic.", "Stephen Strange, Christine Palmer, Wong", "Kaecilius / Dormammu", "Strange meets Thor; Mordo begins stripping sorcerers.", "2016-2017.", "Introduces the Time Stone and mystic dimensions.", "Doctor Strange origin and The Oath.", 89, "https://www.youtube.com/embed/HSzx-zryEgM"),
    ("Guardians of the Galaxy Vol. 2", "Phase 3", 2017, "Peter Quill discovers his celestial father and the team becomes family.", "Guardians, Yondu, Mantis, Ego", "Ego", "Multiple stingers include Adam Warlock setup and teen Groot.", "2014 shortly after Vol. 1.", "Deepens cosmic family and Ravager lore.", "Ego and Star-Lord cosmic stories.", 85, "https://www.youtube.com/embed/dW1BIid8Osg"),
    ("Spider-Man: Homecoming", "Phase 3", 2017, "Peter Parker tries to prove himself while facing weapons scavenged from Avengers battles.", "Peter Parker, Tony Stark, MJ, Ned", "Vulture", "Aunt May discovers Peter's secret.", "2016 after Civil War.", "Shows post-Battle-of-New-York consequences.", "Teen Spider-Man and Vulture stories.", 92, "https://www.youtube.com/embed/n9DwoQ7HWvI"),
    ("Thor: Ragnarok", "Phase 3", 2017, "Thor loses his hammer, finds Hulk, and lets Asgard fall to save its people.", "Thor, Loki, Valkyrie, Hulk", "Hela", "Thanos' ship intercepts the Asgardians.", "2017 before Infinity War.", "Launches Thor toward the Infinity War opening.", "Ragnarok and Planet Hulk.", 93, "https://www.youtube.com/embed/ue80QwXMRHg"),
    ("Black Panther", "Phase 3", 2018, "T'Challa's crown is challenged as Wakanda confronts isolation and history.", "T'Challa, Shuri, Nakia, Okoye", "Killmonger", "Wakanda opens outreach; Bucky wakes as White Wolf.", "2016 after Civil War.", "Makes Wakanda central to global MCU politics.", "Who Is the Black Panther? and Killmonger comics.", 96, "https://www.youtube.com/embed/xjDjIWPwcPU"),
    ("Avengers: Infinity War", "Phase 3", 2018, "Thanos hunts the Infinity Stones as heroes fight across Earth and space.", "Avengers, Guardians, Doctor Strange, Black Panther", "Thanos", "Nick Fury pages Captain Marvel after the Snap.", "2018.", "The Snap reshapes every MCU story after it.", "Infinity Gauntlet and Infinity.", 94, "https://www.youtube.com/embed/6ZfuNTqbHE8"),
    ("Ant-Man and the Wasp", "Phase 3", 2018, "Scott, Hope, and Hank rescue Janet from the Quantum Realm.", "Scott Lang, Hope van Dyne, Hank Pym, Janet van Dyne", "Ghost", "The Pyms dust while Scott is trapped in the Quantum Realm.", "2018 before and during the Snap.", "Quantum Realm becomes key to Endgame.", "Wasp legacy and Ghost reimagining.", 87, "https://www.youtube.com/embed/8_rTIAOohas"),
    ("Captain Marvel", "Phase 3", 2019, "Carol Danvers uncovers her past and becomes a cosmic powerhouse.", "Carol Danvers, Nick Fury, Talos", "Yon-Rogg / Supreme Intelligence", "Carol answers Fury's pager; Goose coughs up the Tesseract.", "1995.", "Explains Fury's pager and Kree-Skrull conflict.", "Carol Danvers Captain Marvel era.", 79, "https://www.youtube.com/embed/Z1BCujX3pw8"),
    ("Avengers: Endgame", "Phase 3", 2019, "The surviving heroes attempt a time heist to undo Thanos' Snap.", "Original Avengers, Ant-Man, Captain Marvel", "Thanos", "No traditional post-credit scene; an armor clang tribute closes the saga.", "2023 after five-year Blip.", "Concludes the Infinity Saga and passes several mantles.", "Infinity Gauntlet and Avengers Forever echoes.", 94, "https://www.youtube.com/embed/TcMBFSGVi1c"),
    ("Spider-Man: Far From Home", "Phase 3", 2019, "Peter faces grief, illusion tech, and the burden of Tony's legacy.", "Peter Parker, MJ, Nick Fury, Mysterio", "Mysterio", "Peter is unmasked; Fury is revealed off-world.", "2024 after Endgame.", "Sets up identity crisis and Skrull-space threads.", "Mysterio and post-mentor Spider-Man stories.", 90, "https://www.youtube.com/embed/Nt9L1jCKGnE"),
    ("Black Widow", "Phase 4", 2021, "Natasha confronts the Red Room and her chosen family before Infinity War.", "Natasha Romanoff, Yelena Belova, Red Guardian", "Dreykov / Taskmaster", "Yelena is sent after Hawkeye.", "2016 between Civil War and Infinity War.", "Introduces Yelena and Red Room fallout.", "Black Widow espionage comics.", 79, "https://www.youtube.com/embed/Fp9pNPdNwjI"),
    ("Shang-Chi and the Legend of the Ten Rings", "Phase 4", 2021, "Shang-Chi faces his father and the mystical legacy of the Ten Rings.", "Shang-Chi, Katy, Wenwu, Xialing", "Wenwu", "The rings signal something unknown; Xialing takes over the Ten Rings.", "2024 after Endgame.", "Reframes Ten Rings mythology and mystical artifacts.", "Master of Kung Fu and modern Shang-Chi.", 91, "https://www.youtube.com/embed/8YjFbMbfXaQ"),
    ("Eternals", "Phase 4", 2021, "Ancient immortal beings question their mission after thousands of years on Earth.", "Sersi, Ikaris, Thena, Kingo", "Deviants / Arishem conflict", "Eros appears; Dane Whitman approaches the Ebony Blade.", "Post-Endgame.", "Introduces Celestials and cosmic judgment.", "Jack Kirby's Eternals.", 69, "https://www.youtube.com/embed/x_me3xsvDgk"),
    ("Spider-Man: No Way Home", "Phase 4", 2021, "A spell gone wrong pulls Spider-Man villains and heroes through the multiverse.", "Peter Parker, MJ, Doctor Strange", "Green Goblin", "Venom leaves symbiote matter; Doctor Strange 2 teaser.", "Late 2024.", "Makes multiverse consequences personal and irreversible.", "One More Day and Spider-Verse echoes.", 93, "https://www.youtube.com/embed/JfVOs4VSpmA"),
    ("Doctor Strange in the Multiverse of Madness", "Phase 4", 2022, "Strange protects America Chavez while Wanda hunts multiversal reunion.", "Doctor Strange, America Chavez, Wong, Wanda", "Scarlet Witch", "Clea recruits Strange to fix an incursion; Pizza Poppa is freed.", "After No Way Home and WandaVision.", "Introduces incursions and Earth-838 Illuminati.", "Doctor Strange multiverse and House of M themes.", 74, "https://www.youtube.com/embed/aWzlQ2N6qqg"),
    ("Thor: Love and Thunder", "Phase 4", 2022, "Thor faces Gorr while Jane Foster wields Mjolnir as the Mighty Thor.", "Thor, Jane Foster, Valkyrie, Korg", "Gorr the God Butcher", "Hercules is sent after Thor; Jane reaches Valhalla.", "Post-Endgame cosmic travels.", "Sets up Hercules and Valhalla mythology.", "The Mighty Thor and God Butcher arcs.", 64, "https://www.youtube.com/embed/Go8nTmfrQd8"),
    ("Black Panther: Wakanda Forever", "Phase 4", 2022, "Wakanda grieves T'Challa while conflict with Talokan erupts.", "Shuri, Ramonda, Nakia, Namor", "Namor conflict", "Nakia introduces T'Challa's son.", "2025 after Endgame.", "Introduces Talokan and Shuri as Black Panther.", "Doomwar, Namor, and Wakanda stories.", 84, "https://www.youtube.com/embed/_Z3QKkl1WyM"),
    ("Ant-Man and the Wasp: Quantumania", "Phase 5", 2023, "The Ant-family is pulled into the Quantum Realm and faces Kang.", "Scott Lang, Hope van Dyne, Cassie Lang", "Kang the Conqueror", "Council of Kangs gathers; Loki and Mobius observe Victor Timely.", "Post-Endgame.", "Places Kang variants at the center of multiverse threat.", "Kang and Quantum Realm science fiction.", 62, "https://www.youtube.com/embed/ZlNFpri-Y40"),
    ("Guardians of the Galaxy Vol. 3", "Phase 5", 2023, "Rocket's past drives the Guardians into conflict with the High Evolutionary.", "Guardians, Adam Warlock, High Evolutionary", "High Evolutionary", "Rocket leads a new team; Peter returns to Earth.", "After Holiday Special.", "Closes the original Guardians era.", "Rocket origin and Warlock stories.", 82, "https://www.youtube.com/embed/u3V5KDHRQvk"),
    ("The Marvels", "Phase 5", 2023, "Carol, Monica, and Kamala swap places while fighting a Kree revolutionary.", "Carol Danvers, Monica Rambeau, Kamala Khan", "Dar-Benn", "Monica lands near the X-Men; Kamala starts recruiting young heroes.", "After Ms. Marvel and WandaVision.", "Connects cosmic, mutant, and Young Avengers threads.", "Captain Marvel team-up comics.", 62, "https://www.youtube.com/embed/wS_qbDztgVY"),
    ("Deadpool & Wolverine", "Phase 5", 2024, "Deadpool drags Wolverine through TVA chaos and collapsing timelines.", "Deadpool, Wolverine, TVA figures", "Cassandra Nova", "Legacy and TVA jokes bridge Fox Marvel and MCU multiverse.", "Multiverse Saga branch.", "Brings X-Men legacy characters into MCU conversation.", "Deadpool Corps and Wolverine multiverse stories.", 78, "https://www.youtube.com/embed/73_1biulkYk"),
    ("Captain America: Brave New World", "Phase 5", 2025, "Sam Wilson carries the shield into a political crisis involving global power and old super-soldier shadows.", "Sam Wilson, Joaquin Torres, President Ross", "Leader / Red Hulk conflict", "Sets up geopolitical and gamma consequences.", "Post-Falcon and the Winter Soldier.", "Continues Sam's Captain America mantle.", "Sam Wilson: Captain America and Hulk politics.", 68, "https://www.youtube.com/embed/1pHDWnXmK7Y"),
    ("Thunderbolts*", "Phase 5", 2025, "A team of antiheroes and covert assets collide on a dangerous mission.", "Yelena Belova, Bucky Barnes, Red Guardian, U.S. Agent", "Sentry / covert threat", "Leads toward a new era of uneasy Avengers-level teams.", "After Phase 5 street and spy stories.", "Connects Black Widow, Falcon, and government experiments.", "Thunderbolts and Dark Avengers comics.", 74, "https://www.youtube.com/embed/-sAOWhvheK8"),
    ("The Fantastic Four: First Steps", "Phase 6", 2025, "Marvel's First Family enters a retro-futurist cosmic crisis involving Galactus.", "Reed Richards, Sue Storm, Johnny Storm, Ben Grimm", "Galactus / Silver Surfer", "Cosmic consequences lead toward Avengers-level stakes.", "Separate retro-future universe entering the multiverse saga.", "Introduces Fantastic Four mythos to Marvel Studios continuity.", "Fantastic Four #48-50 and Galactus trilogy.", 82, "https://www.youtube.com/embed/pAsmrKyMqaA"),
    ("Spider-Man: Brand New Day", "Phase 6", 2026, "Upcoming Spider-Man chapter after Peter's erased identity reset.", "Peter Parker and allies to be confirmed", "To be confirmed", "Upcoming film; details subject to studio release.", "After No Way Home.", "Expected to continue street-level and multiverse consequences.", "Brand New Day era and modern Spider-Man comics.", 0, "https://www.youtube.com/embed/"),
    ("Avengers: Doomsday", "Phase 6", 2026, "Upcoming Avengers crossover announced by Marvel Studios.", "Avengers, Fantastic Four, X-Men-related characters", "Doctor Doom threat", "Upcoming film; post-credit details unknown.", "Multiverse Saga climax path.", "Builds toward Secret Wars.", "Doom, Avengers, and multiverse event comics.", 0, "https://www.youtube.com/embed/"),
]


SHOWS = [
    ("Loki", "Disney+", 2, "A Loki variant is pulled into TVA bureaucracy and discovers the fragile machinery of timelines.", "Loki moves from self-preservation to cosmic sacrifice.", "Season 1 breaks open He Who Remains' timeline control. Season 2 turns Loki into the living anchor of branching realities.", "Directly reshapes multiverse rules.", "Kang variants, TVA propaganda, classic Loki callbacks.", "Massive: explains branches, pruning, and temporal control."),
    ("WandaVision", "Disney+", 1, "Wanda creates a sitcom-shaped reality over Westview while grieving Vision.", "Wanda becomes the Scarlet Witch as Monica Rambeau gains powers.", "Each episode channels television eras while revealing the hex.", "Occurs after Endgame and before Multiverse of Madness.", "Agatha, Darkhold, Vision comics, twins Billy and Tommy.", "Major: grief-powered reality warping and Darkhold corruption."),
    ("Moon Knight", "Disney+", 1, "Marc Spector and Steven Grant unravel Egyptian god politics and their shared trauma.", "Marc and Steven negotiate identity, guilt, and Khonshu's control.", "A supernatural mystery builds toward Ammit's release and Jake Lockley's reveal.", "Runs mostly apart from Avengers events.", "Crescent darts, Mr. Knight suit, Egyptian pantheon.", "Moderate: adds divine avatars to MCU cosmology."),
    ("Daredevil", "Netflix / Disney+", 3, "Matt Murdock fights crime as a lawyer by day and masked vigilante by night.", "Matt wrestles with faith, violence, and Kingpin's hold over Hell's Kitchen.", "Season 1 rises against Fisk, Season 2 introduces Punisher and Elektra, Season 3 adapts Born Again themes.", "Street-level cornerstone later folded into MCU.", "Bullseye, The Hand, Catholic imagery, Nelson and Murdock.", "Low cosmic impact, high street-level importance."),
    ("Jessica Jones", "Netflix", 3, "A private investigator with super strength confronts trauma and mind control.", "Jessica rebuilds agency after Kilgrave and navigates family wounds.", "Noir detective seasons focus on survival, addiction, and accountability.", "Part of Defenders-era street continuity.", "Alias comics, Purple Man, Hellcat setup.", "Low multiverse impact, strong character impact."),
    ("Agents of SHIELD", "ABC", 7, "Coulson's team tackles Hydra, Inhumans, space, time travel, and chronicom invasions.", "The agents evolve from SHIELD operatives into a family across eras.", "Spans Hydra uprising, Inhumans, Framework reality, future space, and final time-hopping mission.", "Begins in the shadow of Avengers and Winter Soldier.", "Ghost Rider, LMDs, Kree, Secret Warriors.", "Moderate: alternate timelines and Coulson resurrection lore."),
    ("Punisher", "Netflix", 2, "Frank Castle uncovers conspiracies while continuing his war against violent criminals.", "Frank struggles between vengeance, friendship, and the impossibility of peace.", "Season 1 explores military betrayal; Season 2 pits him against Jigsaw and extremists.", "Street-level after Daredevil Season 2.", "Micro, Jigsaw, Punisher MAX tone.", "Low multiverse impact, high vigilante ethics impact."),
    ("Ms. Marvel", "Disney+", 1, "Kamala Khan discovers a bangle-linked power inheritance and a heroic identity.", "Kamala becomes her own hero while embracing family and community history.", "A coming-of-age superhero season with Partition memory and ClanDestine conflict.", "Before The Marvels.", "Mutant tease, Captain Marvel fandom, Jersey City roots.", "Moderate: introduces mutation language and bangle mystery."),
    ("What If...?", "Disney+", 3, "The Watcher observes alternate realities where familiar Marvel choices go differently.", "The Watcher shifts from observer to reluctant participant.", "Animated anthology branches include Captain Carter, Strange Supreme, zombies, and universe collisions.", "Across the multiverse outside main chronology.", "Classic issue title, Uatu, many variant cameos.", "Huge: visualizes endless branches and variant logic."),
    ("X-Men animated series", "Fox / Disney+", 5, "Mutants fight prejudice, Sentinels, Magneto, Apocalypse, and cosmic Phoenix threats.", "The X-Men operate as family, resistance, and school.", "Adapts major comic arcs including Phoenix, Days of Future Past, and Age of Apocalypse ideas.", "Legacy mutant continuity adjacent to MCU revival interest.", "Theme song, yellow costumes, Savage Land, Shi'ar.", "Important for mutant mythology and nostalgia continuity."),
    ("Hawkeye", "Disney+", 1, "Clint Barton and Kate Bishop get tangled with Tracksuit Mafia and Echo at Christmas.", "Clint confronts Ronin guilt while Kate earns a hero path.", "Holiday street-level story linking Ronin fallout to Kingpin.", "After Endgame in New York.", "Pizza Dog, Kate Bishop, Echo, Kingpin.", "Low cosmic impact, strong Young Avengers setup."),
    ("She-Hulk: Attorney at Law", "Disney+", 1, "Jennifer Walters balances gamma powers, law practice, and superhero celebrity.", "Jen rejects imposed origin drama and defines her own format.", "Legal comedy with fourth-wall bends and Hulk-family reveals.", "After Endgame and Shang-Chi.", "Daredevil cameo, Skaar, GLK&H.", "Low multiverse impact, playful format impact."),
]


COMICS = [
    ("Secret Wars", 1984, "Heroes and villains are transported to Battleworld by the Beyonder.", "Many temporary transformations; huge status shifts.", "Avengers/X-Men/Fantastic Four vs villains; Doom vs Beyonder.", "Inspired the idea of massive crossover events and future MCU Secret Wars speculation.", "Secret Wars #1-12", "Avengers, X-Men, Fantastic Four, Doctor Doom"),
    ("Civil War", 2006, "Superhero registration divides Marvel's heroes after a tragedy.", "Goliath dies; trust across hero teams collapses.", "Iron Man's faction vs Captain America's resistance.", "Inspired Captain America: Civil War.", "Civil War #1-7 plus Front Line and tie-ins.", "Iron Man, Captain America, Spider-Man"),
    ("Infinity Gauntlet", 1991, "Thanos uses the Infinity Gems to become godlike and erase half of life.", "Half the universe vanishes before cosmic restoration.", "Earth heroes and cosmic entities challenge Thanos.", "Core inspiration for Infinity War and Endgame.", "Thanos Quest, Infinity Gauntlet #1-6", "Thanos, Adam Warlock, Silver Surfer"),
    ("House of M", 2005, "Wanda rewrites reality into a mutant-dominated world.", "Mutant population is decimated by 'No more mutants.'", "Heroes uncover reality's false structure.", "Influenced WandaVision and Multiverse of Madness themes.", "House of M #1-8", "Scarlet Witch, Magneto, X-Men"),
    ("Old Man Logan", 2008, "An aged Logan crosses a villain-ruled wasteland future.", "Many heroes are dead before the story begins.", "Logan's final berserker reckoning against Hulk's clan.", "Influenced Logan and multiverse Wolverine stories.", "Wolverine #66-72, Giant-Size Old Man Logan", "Wolverine, Hawkeye, Hulk"),
    ("Planet Hulk", 2006, "Hulk is exiled to Sakaar, becomes gladiator, and rises as king.", "Sakaar's people suffer catastrophic loss.", "Hulk vs Silver Surfer, Red King, imperial forces.", "Elements adapted in Thor: Ragnarok.", "Incredible Hulk #92-105", "Hulk, Warbound, Silver Surfer"),
    ("Spider-Verse", 2014, "Spider-heroes from across realities unite against the Inheritors.", "Several Spider-totems fall in multiversal war.", "Spider-Army vs Inheritors.", "Inspired animated Spider-Verse films and No Way Home energy.", "Edge of Spider-Verse, Amazing Spider-Man #9-15", "Peter Parker, Miles Morales, Spider-Gwen"),
    ("Age of Apocalypse", 1995, "A timeline shift creates a world ruled by Apocalypse.", "Many X-Men die or are radically altered.", "Magneto's X-Men fight Apocalypse's regime.", "Inspired X-Men film and animated alternate timelines.", "Alpha, core X-books, Omega", "Magneto, Apocalypse, X-Men"),
    ("Secret Invasion", 2008, "Skrulls infiltrate Earth by impersonating trusted heroes.", "Trust is the biggest casualty; several characters fall.", "Heroes vs Skrull invasion fleet.", "Adapted loosely as Disney+ Secret Invasion.", "Secret Invasion #1-8 plus New Avengers tie-ins", "Nick Fury, Skrulls, Avengers"),
    ("World War Hulk", 2007, "Hulk returns to Earth to punish the Illuminati for exiling him.", "Major destruction across New York and hero reputations.", "Hulk's Warbound vs Avengers, X-Men, Fantastic Four.", "Potential influence for future Hulk projects.", "World War Hulk #1-5 after Planet Hulk", "Hulk, Illuminati, Warbound"),
    ("Dark Phoenix Saga", 1980, "Jean Grey's Phoenix power turns cosmic and catastrophic.", "A star system dies, and Jean sacrifices herself.", "X-Men vs Imperial Guard; Jean vs herself.", "Adapted in X-Men films and animation.", "Uncanny X-Men #129-138", "Jean Grey, Cyclops, Wolverine"),
    ("Kraven's Last Hunt", 1987, "Kraven defeats and buries Spider-Man to prove superiority.", "Kraven dies by suicide after completing his obsession.", "Spider-Man's survival vs Kraven's psychological victory.", "Influences darker Spider-Man adaptations.", "Web of Spider-Man, Amazing Spider-Man, Spectacular Spider-Man crossover", "Spider-Man, Kraven, Mary Jane"),
    ("Annihilation", 2006, "Annihilus launches a devastating invasion from the Negative Zone.", "Nova Corps and many worlds are devastated.", "Nova, Silver Surfer, and cosmic heroes vs Annihilation Wave.", "Shaped modern Guardians-style cosmic Marvel.", "Annihilation Prologue, minis, Annihilation #1-6", "Nova, Silver Surfer, Annihilus"),
    ("Demon in a Bottle", 1979, "Tony Stark faces alcoholism and corporate pressure.", "Tony's identity and friendships are damaged.", "Iron Man vs Justin Hammer's schemes and himself.", "Inspired parts of Iron Man 2 and Tony's vulnerability.", "Iron Man #120-128", "Iron Man, Bethany Cabe, Justin Hammer"),
    ("Born Again", 1986, "Kingpin destroys Matt Murdock's life after learning his identity.", "Matt loses career, home, and stability.", "Daredevil's recovery vs Kingpin's machinery.", "Major influence on Daredevil TV.", "Daredevil #227-233", "Daredevil, Kingpin, Karen Page"),
]


TIMELINE = [
    ("1943", "Captain America rises during WWII", "main", "super-soldier"),
    ("1995", "Captain Marvel discovers Kree manipulation", "main", "cosmic"),
    ("2008", "Iron Man reveals himself", "main", "tech"),
    ("2012", "Battle of New York", "main", "avengers"),
    ("2014", "Guardians protect the Power Stone", "cosmic", "stone"),
    ("2016", "Civil War fractures the Avengers", "main", "political"),
    ("2018", "Thanos snaps half of life away", "main", "infinity"),
    ("2023", "Time Heist restores the vanished", "main", "time"),
    ("2024", "No Way Home tears open Spider-variants", "multiverse", "spider"),
    ("2025", "Wakanda and Talokan clash", "main", "nation"),
    ("TVA", "Loki becomes guardian of branching timelines", "multiverse", "time"),
    ("Earth-838", "Illuminati universe collides with Wanda's search", "branch", "incursion"),
    ("Quantum Realm", "Kang variants threaten the saga", "branch", "kang"),
    ("Battleworld", "Secret Wars-style collision point", "future", "incursion"),
]


TEAMS = [
    ("Avengers", "Earth's Mightiest Heroes formed after the Battle of New York."),
    ("X-Men", "Mutant heroes fighting for coexistence and survival."),
    ("Fantastic Four", "Marvel's First Family of explorers and cosmic adventurers."),
    ("Guardians of the Galaxy", "Cosmic misfits protecting the galaxy with chaotic heart."),
    ("Defenders", "Street-level and mystical heroes united by local threats."),
    ("Midnight Sons", "Supernatural heroes facing demons, vampires, and occult crises."),
    ("Thunderbolts", "Antiheroes and reformed villains on dangerous missions."),
]


def seed_admin(db):
    db.execute(
        "INSERT INTO users (username, password_hash) VALUES (?, ?)",
        (ADMIN_USERNAME, generate_password_hash(ADMIN_PASSWORD)),
    )


def seed_characters(db):
    for item in CHARACTERS:
        db.execute(
            """
            INSERT INTO characters
            (name, alias, category, image, image_url, tagline, origin, powers, weaknesses, teams, enemies, arcs, mcu, variants, timeline, power_level, bio)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                item["name"],
                item["alias"],
                item["category"],
                item["image"],
                item.get("image_url", ""),
                item["tagline"],
                item["origin"],
                to_json(item["powers"]),
                to_json(item["weaknesses"]),
                to_json(item["teams"]),
                to_json(item["enemies"]),
                to_json(item["arcs"]),
                to_json(item["mcu"]),
                to_json(item["variants"]),
                item["timeline"],
                item["power_level"],
                item["bio"],
            ),
        )


def seed_movies(db):
    for movie in MOVIES:
        db.execute(
            """
            INSERT INTO movies
            (title, phase, release_year, synopsis, cast, villain, post_credit, timeline, connections, comic_inspiration, rating, poster_url, trailer_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (*movie[:11], "", movie[11]),
        )


def seed_shows(db):
    for show in SHOWS:
        db.execute(
            """
            INSERT INTO shows
            (title, platform, seasons, poster_url, plot, character_arcs, season_breakdown, timeline_relevance, easter_eggs, multiverse_impact)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (*show[:3], "", *show[3:]),
        )


def seed_comics(db):
    for comic in COMICS:
        db.execute(
            """
            INSERT INTO comics
            (title, year, summary, major_deaths, important_battles, adaptations, reading_order, key_characters)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            comic,
        )


def seed_timeline(db):
    for event in TIMELINE:
        db.execute(
            "INSERT INTO timeline_events (era, title, branch, event_type) VALUES (?, ?, ?, ?)",
            event,
        )


def seed_teams(db):
    for team in TEAMS:
        db.execute("INSERT INTO teams (name, description) VALUES (?, ?)", team)


def seed_powers(db):
    powers = set()
    for character in CHARACTERS:
        for power in character["powers"]:
            powers.add(power)
    for power in sorted(powers):
        db.execute("INSERT INTO powers (name, description) VALUES (?, ?)", (power, f"{power} appears in MarvelVerse character profiles."))


def init_db():
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(DATABASE_PATH)
    try:
        db.row_factory = sqlite3.Row
        execute_schema(db)
        seed_admin(db)
        seed_characters(db)
        seed_movies(db)
        seed_shows(db)
        seed_comics(db)
        seed_timeline(db)
        seed_teams(db)
        seed_powers(db)
        db.commit()
    finally:
        db.close()


def ensure_database():
    if not DATABASE_PATH.exists():
        init_db()
        return
    db = sqlite3.connect(DATABASE_PATH)
    try:
        exists = db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='characters'").fetchone()
        if not exists:
            init_db()
        else:
            db.row_factory = sqlite3.Row
            migrate_db(db)
    finally:
        db.close()
