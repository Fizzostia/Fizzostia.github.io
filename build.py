"""Builds the Fizzostia site. Run from the site root: python build.py

Every fact here is verified against the live Steam pages or, for RoboSquare: Recharged,
against RoboSquare-2/Marketing/BRAND.md. Verification date in VERIFIED below.
"""
import io, os, re, shutil

VERIFIED = "7 September 2026"
BASE = "https://fizzostia.github.io/"
EMAIL = "fizzostia@gmail.com"
DISCORD = "https://discord.gg/cdSTbrM"
# Unlisted publisher pitches, one per publisher. Each slug is random so it can't be guessed;
# /pitch/ is noindex, disallowed in robots.txt and linked from nowhere on the site.
DECKS = "../RoboSquare-2/Marketing/press-kit/"
PITCHES = [
  dict(src=DECKS + "pitch-deck-aggro-crab.html", slug="pitch/recharged-9c41f7ab"),
  dict(src=DECKS + "pitch-deck-tark.html", slug="pitch/recharged-59ac3f29"),
  dict(src=DECKS + "pitch-deck-generic.html", slug="pitch/recharged-cfec5580"),
]

STEAM = "https://store.steampowered.com/app/"

# Channels shown on the contact page.
#   live=False keeps a row out of the built HTML. Use it for anything not yet confirmed:
#   a wrong handle on a public contact page sends press to a stranger, so confirm first,
#   then flip the flag and rerun the build.
SOCIALS = [
  dict(live=True,  label="Email", handle=EMAIL, url="mailto:" + EMAIL, primary=True,
       note="The fastest way to reach us, and the one we actually check. Press, publishers, "
            "creators, key requests, bug reports, all of it."),
  dict(live=True,  label="Discord", handle="discord.gg/cdSTbrM", url=DISCORD, primary=False,
       note="The community server. Patch notes land here first, and it is the best place to "
            "find people to play RoboSquare with."),
  dict(live=False, label="YouTube", handle="", url="", primary=False,
       note="Trailers and devlogs."),
  dict(live=False, label="Twitter / X", handle="", url="", primary=False,
       note="Short updates and work in progress."),
  dict(live=False, label="Reddit", handle="", url="", primary=False,
       note="Devlogs and longer posts."),
]

GAMES = [
  dict(
    slug="robosquare-recharged", title="RoboSquare: Recharged", app="4088870",
    art="robosquare-recharged.jpg", featured=True,
    status=("now", "Coming Q1 2027"),
    meta="PC, Steam &middot; $5.99 USD &middot; Not Early Access",
    blurb="An online multiplayer party game about hovering robots and the appalling things they "
          "do to each other. Sixteen players, five randomly chosen minigames back to back, and one "
          "champion at the end. The empty seats fill themselves, so a full sixteen-bot brawl is "
          "always one click away.",
    facts=[("Release", "<b>Q1 2027</b>"), ("Price", "<b>$5.99 USD</b>, premium, not Early Access"),
           ("Platform", "PC (Windows, Steam)"), ("Players", "Up to 16 online"),
           ("Modes", "5: Race, Sumo, King of the Hill, Infection, Capture the Core"),
           ("Arenas", "14"), ("Chaos events", "8, fired mid-round without warning"),
           ("Engine", "Unity with Photon Quantum 3 deterministic rollback netcode"),
           ("Input", "Full controller support (Xbox, DualShock, DualSense) and keyboard"),
           ("Languages", "English plus 30 others"),
           ("Steam features", "Achievements, global leaderboards, Cloud, HDR, Family Sharing"),
           ("Developer", "Fizz, working solo on this game")],
    features=[
      "<b>Sixteen seats, so nobody sits out.</b> Most party games cap at four or eight and somebody "
      "in the group ends up watching. Bring six friends, or twelve, or fifteen.",
      "<b>Three verbs, endless mess.</b> Jump, Dash, Slam. Momentum is your best weapon and your "
      "worst habit.",
      "<b>Eight chaos events fire mid-round, unannounced.</b> Wind picks a direction and commits. "
      "Gravity gets lazy. Bombs fall. A UFO helps itself to whoever is winning.",
      "<b>The lobby is never empty.</b> Any seat nobody is in gets filled, so the game still works "
      "at 3 am, or a year after launch.",
      "<b>Deep bot customization.</b> 13 bodies, 6 hover thrusters, 6 finishes, plus body and "
      "thruster colors.",
      "<b>Accolades and rivalries.</b> Every hit, jump, dash, slam and meter traveled is tracked, "
      "and the game works out who your rival is from how often you two keep crashing into each other.",
    ],
    shots=[("recharged-race.jpg", "Race, lining up the loop with two bombs already in the air."),
           ("recharged-koth.jpg", "King of the Hill. The zone moves, and everyone has noticed."),
           ("recharged-infection.jpg", "Infection. Ten alive, and the whole control scheme sits in "
            "the bottom right corner."),
           ("recharged-capturecore.jpg", "Capture the Core, where one dedicated slammer ruins an "
            "entire strategy."),
           ("recharged-capturecore-wide.jpg", "The same fight from further out, with the goal at "
            "the far end."),
           ("recharged-lobby.jpg", "A full sixteen-bot match, every seat filled."),
           ("recharged-arena-topdown.jpg", "An arena from directly above.")],
  ),
  dict(
    slug="glingdom", title="Glingdom", app="2935750",
    art="glingdom.jpg", featured=False,
    status=("out", "Out now"),
    meta="PC, Steam &middot; $5.99 USD &middot; Released 7 November 2024",
    blurb="A medieval roguelike deckbuilder. Beat waves of enemies and bosses, buy cards and runes "
          "to strengthen your deck between fights, and unlock new units as you go. Over fifty of them.",
    facts=[("Release", "<b>7 November 2024</b>"), ("Price", "<b>$5.99 USD</b>"),
           ("Platform", "PC (Windows, Steam)"), ("Genre", "Roguelike deckbuilder, auto battler"),
           ("Units", "50+ unique units to unlock"),
           ("Steam tags", "Strategy, Roguelike Deckbuilder, Card Battler, Auto Battler, "
                          "Deckbuilding, Medieval, Card Game, 2D, Top-Down"),
           ("Languages", "English"),
           ("Developer", "Fizz"), ("Publisher", "Fizzostia")],
    features=[
      "<b>Waves and bosses.</b> Fight through enemy waves, then something bigger at the end of them.",
      "<b>Buy between fights.</b> Cards and runes, spent on making the next run survivable.",
      "<b>50+ units.</b> Unlocked by playing, mixed into decks that fight on their own once placed.",
    ],
    shots=[],
  ),
  dict(
    slug="robosquare", title="RoboSquare", app="1427760",
    art="robosquare.jpg", featured=False,
    status=("out", "Out now, free"),
    meta="PC, Steam &middot; Free to play &middot; Released 31 December 2021",
    blurb="The first RoboSquare. Free to play, up to sixteen robots, and three modes that all came "
          "down to the same thing: push the other robot off the platform. Nearly 54,000 people "
          "played it. It is still up and still free.",
    facts=[("Release", "<b>31 December 2021</b>, Early Access from 1 January 2021"),
           ("Price", "<b>Free to play</b>"), ("Platform", "PC (Windows, Steam)"),
           ("Players", "Up to 16 online"),
           ("Modes", "3: Sumo, Boss of the Hill, Race"),
           ("Reviews", "<b>77% positive across 249</b> (Mostly Positive)"),
           ("Players reached", "<b>53,926</b> lifetime unique users"),
           ("Languages", "9"), ("Achievements", "26"),
           ("Input", "Partial controller support"),
           ("Developer", "Fizzostia")],
    features=[
      "<b>Three modes.</b> Sumo, Boss of the Hill and Race, all built on shoving other robots off "
      "the arena.",
      "<b>Sixteen players.</b> Online PvP with synchronized hazard events tearing up the arena "
      "mid-match.",
      "<b>Free, and staying free.</b> Four cosmetic DLC bundles exist; nothing in them affects a match.",
    ],
    shots=[],
  ),
  dict(
    slug="sandbox-anything", title="Sandbox Anything", app="1054370",
    art="sandbox-anything.jpg", featured=False,
    status=("out", "Out now, free, Early Access"),
    meta="PC, Steam &middot; Free &middot; Early Access since 18 December 2019",
    blurb="Fizzostia's first Steam release. A physics building game where you throw objects around "
          "to build structures that solve the level. It ships with a level editor, Steam Workshop "
          "support and online multiplayer.",
    facts=[("Release", "<b>18 December 2019</b>, still Early Access"),
           ("Price", "<b>Free</b>"), ("Platform", "PC (Windows, Steam)"),
           ("Reviews", "<b>75% positive across 80</b> (Mostly Positive)"),
           ("Modes", "Single player, online PvP and co-op"),
           ("Steam tags", "Sandbox, Strategy, Multiplayer, Level Editor, Experimental, 2.5D"),
           ("Achievements", "8"),
           ("Extras", "Steam Workshop, built-in level editor, leaderboards, Family Sharing"),
           ("Developer", "Fizzostia")],
    features=[
      "<b>Throw things until the level is solved.</b> Physics-enabled objects, stacked into "
      "structures that hold, or do not.",
      "<b>Built-in level editor and Steam Workshop.</b> Make levels, publish them, play other "
      "people's.",
      "<b>Online multiplayer.</b> PvP and co-op.",
      "<b>A crossover topper.</b> Owning it unlocks a customization topper in RoboSquare.",
    ],
    shots=[],
  ),
]

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
         'family=Archivo+Black&family=IBM+Plex+Mono:wght@400;500&'
         'family=IBM+Plex+Sans:wght@400;500;600&display=swap">')

FAVICON = ('<link rel="icon" href="data:image/svg+xml,'
           "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E"
           "%3Ctext y='26' font-size='26'%3E%F0%9F%A4%96%3C/text%3E%3C/svg%3E\">")


def page(path, title, desc, body, nav_here="", noindex=False):
    """Writes one page. `path` is relative to the site root, e.g. 'press/glingdom.html'."""
    depth = path.count("/")
    up = "../" * depth
    def cur(name):
        return ' aria-current="page"' if name == nav_here else ""
    robots = '<meta name="robots" content="noindex, nofollow">\n' if noindex else ""
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="dark light">
<title>{title}</title>
<meta name="description" content="{desc}">
{robots}<link rel="canonical" href="{BASE}{path if path != 'index.html' else ''}">
{FAVICON}
{FONTS}
<link rel="stylesheet" href="{up}assets/style.css">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Fizzostia">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{BASE}{path if path != 'index.html' else ''}">
<meta property="og:image" content="{BASE}assets/img/social.jpg">
<meta name="twitter:card" content="summary_large_image">
</head>
<body>
<header class="site-head">
  <div class="wrap">
    <a class="brand" href="{up}index.html">Fizz<em>ostia</em></a>
    <nav>
      <a href="{up}index.html"{cur('home')}>Studio</a>
      <a href="{up}games.html"{cur('games')}>Games</a>
      <a href="{up}press/index.html"{cur('press')}>Press</a>
      <a href="{up}contact.html"{cur('contact')}>Contact</a>
    </nav>
  </div>
</header>

<main class="page">
  <div class="wrap">
{body}
  </div>
</main>

<footer class="site-foot">
  <div class="wrap">
    <span>Fizzostia &middot; <a href="mailto:{EMAIL}">{EMAIL}</a></span>
    <span>Facts verified {VERIFIED}</span>
  </div>
</footer>
</body>
</html>
"""
    full = os.path.join(*path.split("/"))
    os.makedirs(os.path.dirname(full) or ".", exist_ok=True)
    io.open(full, "w", encoding="utf-8", newline="\n").write(html)
    return path


def game_row(g, up=""):
    kind, label = g["status"]
    links = [f'<a href="{STEAM}{g["app"]}/">Steam page</a>',
             f'<a href="{up}press/{g["slug"]}.html">Press kit</a>']
    return f"""      <article class="game{' featured' if g['featured'] else ''}">
        <img class="game-art" src="{up}assets/img/{g['art']}" alt="{g['title']} store art"
             width="460" height="215" loading="lazy">
        <div class="game-body">
          <div class="game-title">
            <h2>{g['title']}</h2>
            <span class="tag {kind}">{label}</span>
          </div>
          <p class="game-meta">{g['meta']}</p>
          <p>{g['blurb']}</p>
          <p class="game-links">{' &middot; '.join(links)}</p>
        </div>
      </article>"""


def facts_table(g):
    rows = "\n".join(f"          <tr><th scope=\"row\">{k}</th><td>{v}</td></tr>" for k, v in g["facts"])
    return f"""      <div class="tablewrap">
        <table>
          <tbody>
{rows}
          </tbody>
        </table>
      </div>"""


# ---------------------------------------------------------------- home
home_games = "\n".join(game_row(g) for g in GAMES)
page("index.html", "Fizzostia",
     "Fizzostia is a small independent game studio. Four games on Steam, including "
     "RoboSquare: Recharged, a 16-player online party game about hovering robots.",
     f"""    <div class="stack">

      <section class="stack-tight">
        <span class="eyebrow">Independent game studio</span>
        <h1>We make small games about physics going wrong</h1>
        <p class="lede">Fizzostia started as two college friends studying by day and making games
          at night. Four games on Steam since then, most of them involving objects hitting other
          objects harder than anyone intended.</p>
      </section>

      <hr class="rule">

      <section class="stack-tight">
        <h3>The games</h3>
        <div class="games">
{home_games}
        </div>
      </section>

      <section class="cols">
        <div class="prose">
          <h2>Who does this</h2>
          <p>Fizzostia was founded by two friends at college. The first Steam release was
            <a href="games.html">Sandbox Anything</a> in 2019, then
            <a href="{STEAM}1427760/">RoboSquare</a> on New Year's Eve 2021, which reached nearly
            54,000 players and holds a Mostly Positive rating.</p>
          <p>The co-founder has since moved on to building App Store apps that solve real-world
            problems. <strong>RoboSquare: Recharged is built by Fizz alone</strong>, after work,
            since January 2024.</p>
        </div>
        <div class="prose">
          <h2>Get in touch</h2>
          <p>Press, publishers, creators and anyone who wants a key: email is the fastest way, and
            it is read by the person who made the games rather than an inbox.</p>
          <p>Permission is granted to use any screenshots, footage or trailer material from any
            Fizzostia game in videos, articles and streams, including monetized ones. No need to
            ask first.</p>
        </div>
      </section>

      <section class="stack-tight">
        <h3>Contact</h3>
        <div class="contact-grid">
          <div><dt>Email</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd></div>
          <div><dt>Discord</dt><dd><a href="{DISCORD}">discord.gg/cdSTbrM</a></dd></div>
          <div><dt>Press kits</dt><dd><a href="press/index.html">One per game</a></dd></div>
        </div>
      </section>

    </div>""", nav_here="home")

# ---------------------------------------------------------------- games
games_rows = "\n".join(game_row(g) for g in GAMES)
page("games.html", "Games by Fizzostia",
     "Every game Fizzostia has released: RoboSquare: Recharged, Glingdom, RoboSquare "
     "and Sandbox Anything.",
     f"""    <div class="stack">
      <section class="stack-tight">
        <span class="eyebrow">Everything we have shipped</span>
        <h1>Games</h1>
        <p class="lede">Four games on Steam, newest first. Three are out; one arrives in Q1 2027.
          Two of them are free.</p>
      </section>

      <div class="games">
{games_rows}
      </div>

      <section class="prose">
        <h2>A note on the free ones</h2>
        <p><a href="{STEAM}1427760/">RoboSquare</a> and
          <a href="{STEAM}1054370/">Sandbox Anything</a> are both still up and both still free.
          RoboSquare is where the audience for Recharged came from, and Sandbox Anything is where
          all of this started. Neither is being actively developed any more; the work goes into
          Recharged.</p>
      </section>
    </div>""", nav_here="games")

# ---------------------------------------------------------------- press hub
press_list = "\n".join(game_row(g, up="../") for g in GAMES)
page("press/index.html", "Press Kits",
     "Press kits for every Fizzostia game, with fact sheets, descriptions, links and "
     "contact details. Coverage permission granted in advance.",
     f"""    <div class="stack">
      <section class="stack-tight">
        <span class="eyebrow">For press, creators and curators</span>
        <h1>Press kits</h1>
        <p class="lede">One per game. Every figure on these pages is verified against the live
          Steam pages or the build, and dated. If a number cannot be confirmed, it is not here.</p>
      </section>

      <div class="note">
        <b>Coverage permission, granted in advance.</b> You may use any screenshots, footage or
        trailer material from any Fizzostia game in videos, articles and streams, including
        monetized ones. You do not need to ask. If you want keys, a build, raw capture or a
        specific screenshot, email <a href="mailto:{EMAIL}">{EMAIL}</a> and you will get a reply
        from the person who made the game.
      </div>

      <div class="games">
{press_list}
      </div>

      <section class="stack-tight">
        <h3>Contact</h3>
        <div class="contact-grid">
          <div><dt>Press email</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd></div>
          <div><dt>Discord</dt><dd><a href="{DISCORD}">discord.gg/cdSTbrM</a></dd></div>
          <div><dt>Studio</dt><dd><a href="../index.html">Fizzostia</a></dd></div>
        </div>
      </section>
    </div>""", nav_here="press")

# ---------------------------------------------------------------- one press kit per game
for g in GAMES:
    feats = "\n".join(f"        <li>{f}</li>" for f in g["features"])
    shots = ""
    if g["shots"]:
        figs = "\n".join(
            f"""          <figure><img src="../assets/img/{f}" alt="{c}" loading="lazy">
            <figcaption>{c}</figcaption></figure>""" for f, c in g["shots"])
        shots = f"""
      <section class="stack-tight">
        <h3>Screenshots</h3>
        <div class="shots">
{figs}
        </div>
        <p class="game-meta">Full-resolution versions, the trailer and additional captures are
          available on request.</p>
      </section>"""

    page(f"press/{g['slug']}.html", f"{g['title']} Press Kit",
         f"Press kit for {g['title']} by Fizzostia: fact sheet, description, features, "
         f"links and press contact.",
         f"""    <div class="stack">
      <section class="stack-tight">
        <span class="eyebrow">Press kit &middot; {g['status'][1]}</span>
        <h1>{g['title']}</h1>
        <p class="lede">{g['blurb']}</p>
        <p class="game-links"><a href="{STEAM}{g['app']}/">Steam page</a> &middot;
          <a href="mailto:{EMAIL}">Request a key</a> &middot;
          <a href="index.html">All press kits</a></p>
      </section>

      <section class="stack-tight">
        <h3>Fact sheet</h3>
{facts_table(g)}
      </section>

      <section class="stack-tight">
        <h3>Key features</h3>
        <ul class="bullets">
{feats}
        </ul>
      </section>
{shots}
      <div class="note">
        <b>Coverage permission, granted in advance.</b> Use any screenshots, footage or trailer
        material from {g['title']} in videos, articles and streams, including monetized ones.
        No need to ask. For keys, builds, raw capture, logos or specific screenshots, email
        <a href="mailto:{EMAIL}">{EMAIL}</a>.
      </div>

      <section class="stack-tight">
        <h3>Contact</h3>
        <div class="contact-grid">
          <div><dt>Press email</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd></div>
          <div><dt>Discord</dt><dd><a href="{DISCORD}">discord.gg/cdSTbrM</a></dd></div>
          <div><dt>Steam</dt><dd><a href="{STEAM}{g['app']}/">App {g['app']}</a></dd></div>
        </div>
      </section>
    </div>""", nav_here="press")

print("built:", ", ".join(sorted(
    os.path.join(r, f).replace("\\", "/") for r, _, fs in os.walk(".")
    for f in fs if f.endswith(".html") and "pitch" not in r)))


# ---------------------------------------------------------------- contact
rows = []
for c in SOCIALS:
    if not c["live"]:
        continue
    link = f'<a href="{c["url"]}">{c["handle"]}</a>'
    rows.append(f"""        <div class="channel{' primary' if c['primary'] else ''}">
          <h2>{c['label']}</h2>
          <p class="channel-handle">{link}</p>
          <p>{c['note']}</p>
        </div>""")
channels = chr(10).join(rows)

page("contact.html", "Contact Fizzostia",
     "How to reach Fizzostia: email, Discord and socials. Press keys, coverage "
     "permission and publisher enquiries all go to the same inbox.",
     f"""    <div class="stack">
      <section class="stack-tight">
        <span class="eyebrow">Two people, one inbox</span>
        <h1>Contact</h1>
        <p class="lede">There is no support desk and no press agency. Everything below reaches
          the people who make the games, so you will get a real answer rather than a form
          response.</p>
      </section>

      <section class="stack-tight">
        <h3>Where to find us</h3>
        <div class="channels">
{channels}
        </div>
      </section>

      <hr class="rule">

      <section class="cols">
        <div class="prose">
          <h2>Press and creators</h2>
          <p>There are <a href="press/index.html">press kits</a> for every game, with fact sheets,
            descriptions and links. If you need something that is not on them, a key, a build, raw
            capture, logos or a specific screenshot, email and say what you are working on.</p>
          <p><strong>You do not need permission to cover our games.</strong> Use any screenshots,
            footage or trailer material in videos, articles and streams, including monetized ones.
            No need to ask first.</p>
        </div>
        <div class="prose">
          <h2>Publishers and business</h2>
          <p>Publisher, porting and platform enquiries go to the same address. Say which game and
            what you have in mind, and you will get a straight answer about whether it is a fit.</p>
          <h2>Bugs and support</h2>
          <p>Discord is faster than email for anything broken in a live game, because other players
            are usually there too. Email works if you would rather not join a server.</p>
        </div>
      </section>

    </div>""", nav_here="contact")


# ---------------------------------------------------------------- hidden pitch decks
# Each deck is authored as a fragment (it doubles as a Claude artifact, where the host
# supplies the doctype and head). Wrap it for a real static host here.

def build_pitch(src, out_dir, base_url):
    frag = io.open(src, encoding="utf-8").read()
    t = re.search(r"<title>(.*?)</title>", frag)
    frag = frag.replace(t.group(0), "", 1)
    links = re.findall(r'<link\b[^>]*>', frag)
    for l in links:
        frag = frag.replace(l, "", 1)
    desc = ("Publishing pitch for RoboSquare: Recharged, a 16-player online party game about "
            "hovering robots. Five modes, deterministic rollback netcode, built solo.")
    head = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t.group(1)}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex, nofollow">
<meta name="color-scheme" content="dark">
{FAVICON}
<meta property="og:type" content="website">
<meta property="og:site_name" content="Fizzostia">
<meta property="og:title" content="RoboSquare: Recharged, publishing pitch">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{base_url}">
<meta property="og:image" content="{BASE}assets/img/social.jpg">
<meta name="twitter:card" content="summary_large_image">
{chr(10).join(links)}
<style>html{{color-scheme:dark}}img{{max-width:100%}}</style>
</head>
<body>
"""
    os.makedirs(out_dir, exist_ok=True)
    io.open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8", newline="\n").write(
        head + frag.strip() + "\n</body>\n</html>\n")

for p in PITCHES:
    if os.path.exists(p["src"]):
        build_pitch(p["src"], os.path.join(*p["slug"].split("/")), BASE + p["slug"] + "/")
        print("pitch:", BASE + p["slug"] + "/")
    else:
        print("pitch SKIPPED, deck not found at", p["src"])
