"""
routes.py
Handles all application routes, authentication, and email verification.
"""

# ---------------------------------------
# Imports
# ---------------------------------------
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from flask import (
    Blueprint,
    render_template,
    request,
    session,
    url_for,
    redirect,
    flash,
    current_app,
    abort,
)

from app.db import get_db
from app.login import handle_login

from werkzeug.security import generate_password_hash
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired









# ---------------------------------------
# Blueprint Setup
# ---------------------------------------
main = Blueprint("main", __name__)


MYTHS = [
    {
        "id": 1,
        "name": "Bigfoot",
        "short_description": "A legendary ape-like creature roaming forests.",
        "long_description": """
Bigfoot: A Detailed Description of the Urban Myth
Bigfoot—also known as Sasquatch, a name derived from the Halkomelem word sásq’ets used by Coast Salish peoples—is one of the most famous and persistent creatures in North American legend. It is typically portrayed as a large, ape-like, bipedal being that inhabits remote forests, particularly in the Pacific Northwest region of the United States and Canada.
Physical Characteristics
Eyewitness accounts vary, but the creature is almost always described with a consistent core set of traits:
•	Height: Often reported between 7 and 10 feet tall, towering over humans and most known wildlife.
•	Build: Massive and muscular, with broad shoulders and long arms that hang lower than a human’s.
•	Hair: Covered head to toe in dark brown, black, or reddish hair—not fur—leading many to compare it to a giant primate or an oversized woodland ape.
•	Face: A mixture of human and ape features: a pronounced brow ridge, deep-set eyes, a flat or somewhat protruding nose, and a heavy jawline.
•	Footprints: Huge footprints, sometimes up to 24 inches long, with five toes. Casts of these prints are a major part of Bigfoot lore.
•	Odor: Many witnesses claim the creature emits a strong, musky, foul smell, often described as a mix of wet animal, rot, and skunk.
Behavioral Traits
Reports consistently depict Bigfoot as:
•	Elusive and shy, avoiding human encounters.
•	Nocturnal or crepuscular, with most sightings around dawn, dusk, or at night.
•	Capable of long, ground-covering strides, often moving silently for an animal its size.
•	Sometimes associated with wood knocks, whooping vocalizations, and rock throwing, behaviors that enthusiasts liken to primate communication.
Origins of the Myth
The concept of a large, wild, human-like creature is ancient, appearing in Indigenous legends across North America long before modern sightings. Each culture had its own version—wildmen, forest guardians, or giant beings inhabiting the wilderness.
Bigfoot entered mainstream American culture in the late 1950s after loggers in California reported massive footprints near Bluff Creek. The term “Big Foot” (later “Bigfoot”) was coined by newspapers as the story gained traction. The most famous piece of evidence, the 1967 Patterson–Gimlin film, shows a large, hairy figure walking along a creek bed. While widely debated, it remains one of the most iconic images in cryptozoology.
Why the Myth Persists
Bigfoot remains a powerful story for several reasons:
•	Mystery of the wilderness: Dense forests, especially in the Pacific Northwest, still contain vast, unexplored terrain that fuels speculation.
•	Human fascination with the unknown: Bigfoot taps into the same psychological roots as other legendary creatures—hope that something undiscovered is still out there.
•	Cultural storytelling: Movies, books, documentaries, and even tourism continue to keep the legend alive. Entire communities host “Bigfoot festivals,” and researchers (known as cryptozoologists) continue to search for evidence.
•	Ambiguous evidence: Footprints, sound recordings, blurry photos, and anecdotal sightings provide enough to sustain curiosity, but never enough to conclusively prove or disprove the creature’s existence.
Symbolism and Cultural Impact
Beyond being a mere urban myth, Bigfoot has become a symbol of wilderness—a reminder that nature holds secrets humans may never fully understand. In American culture, the creature represents:
•	The wildness and mystery of the natural world
•	A challenge to scientific certainty
•	A modern folk hero, bridging ancient myth with contemporary imagination
Whether viewed as a potential undiscovered primate or simply as folklore passed through generations, Bigfoot remains an enduring figure in the collective imagination.

""",
        "image": "bigfoot.png"
    },
    {
        "id": 2,
        "name": "Jersey Devil",
        "short_description": "A winged creature haunting New Jersey folklore.",
        "long_description": """
The Jersey Devil: A Detailed Overview
Introduction
The Jersey Devil—also called the Leeds Devil—is a legendary creature said to haunt the Pine Barrens, a vast, dark, heavily forested region of southern New Jersey. It is one of the longest-standing American cryptid legends, with reports dating back to the 18th century.
 The creature is described as a terrifying, winged beast that shrieks in the night and lurks deep within the woods.

Origin Story: Mother Leeds and Her 13th Child
The most widely known version of the legend begins in the early 1700s with a woman called Mother Leeds:
1.	She already had 12 children and was struggling to survive in the harsh New Jersey wilderness.
2.	When she learned she was pregnant again, she cursed the unborn child, saying:
“Let this one be the Devil!”
3.	According to lore, when the child was born, it began as a normal baby but quickly transformed into a grotesque, monstrous creature.
4.	It grew wings, hooves, and a long tail, let out a bloodcurdling scream, and flew up the chimney into the Pine Barrens.
In some versions, the creature later returned to attack the family or terrorize local villages.
This story is likely a blend of folklore, old political rivalries, and fear surrounding the Leeds family in colonial New Jersey—but it became the core of the Jersey Devil myth.

Physical Description
Although sightings vary, most depictions of the Jersey Devil share similar features:
Common Characteristics
•	Head of a horse, dog, or goat
•	Long, thin, bony body
•	Two small arms with clawed hands
•	Hooved feet similar to a goat
•	Large, leathery bat-like wings
•	Forked or serpent-like tail
•	Glowing or reflective red eyes
•	Ability to move incredibly fast, on land and in the air
Others describe it as a chimera-like creature with:
•	Kangaroo-like legs
•	Birdlike screeching
•	The ability to leap extraordinary distances

Behavior and Sightings
1. The Shriek
The Jersey Devil is said to emit a horrifying, high-pitched scream, often compared to:
•	A woman wailing
•	A tortured animal
•	A combination of a horse cry and a human scream
Many reported sightings begin with hearing this unsettling noise in the woods.
2. Elusiveness and Speed
Witnesses frequently claim:
•	It moves too fast to track
•	It can vanish into the trees or sky almost instantly
•	It leaves behind bizarre hoofprints in snow or mud
3. Aggressive or Menacing Behavior
Accounts include:
•	Livestock killings and mutilations
•	Terrified horses or farm animals
•	The creature flying over homes and towns
A famous wave of sightings known as “The Jersey Devil Panic of 1909” included hundreds of reported encounters, closed schools, and mass hysteria across New Jersey and Pennsylvania.

Habitat: The Pine Barrens
The Pine Barrens is crucial to the legend:
•	A vast forest of dense, dark, swampy pine wilderness
•	Poor soil, abandoned villages, and centuries-old ruins
•	Misty bogs, hidden wildlife, and little human presence
These conditions create the perfect backdrop for a cryptid legend.
Local residents—called Pineys—have passed down stories for generations, fueling mystery around the creature.

Historical Context & Possible Explanations
Folklorists and historians have suggested several explanations:
1. Misidentified Animals
Possible real animals mistaken for the Devil include:
•	Cranes (especially the sandhill crane)
•	Large owls
•	Deformed livestock
•	Escaped exotic animals
2. Political Propaganda
The Leeds family, linked to the legend, was involved in colonial politics. Rivals may have demonized them (literally) through rumors and pamphlets.
3. Early Settlers’ Fears
Tales may reflect:
•	Anxiety about the harsh Pine Barrens environment
•	Fear of the wilderness and the unknown
•	Superstitions of the early settlers
4. Classic Monster Myth-Making
Like Bigfoot or Mothman, humans create monsters to explain strange sounds, shadows, and eerie environments.

Modern Pop Culture Influence
The Jersey Devil appears in:
•	TV shows (The X-Files, Lost Tapes, Ghost Adventures)
•	Books and horror novels
•	Films and documentaries
•	Video games (The Wolf Among Us, Fallout 76)
•	Cryptid-themed merchandise
•	New Jersey:s own NHL team, the New Jersey Devils
Its status as a cryptid legend has only grown since the rise of the internet and paranormal media.

Symbolism
The Jersey Devil represents:
•	Fear of the unknown wilderness
•	The blend of folklore and early American colonial superstition
•	The power of rumor and oral tradition
•	How legends evolve and adapt over centuries
It also serves as a cultural icon unique to New Jersey, embodying both state pride and eerie mystery.

""",
        "image": "jerseydevil.png"
    },
    {
        "id": 3,
        "name": "Bloody Mary",
        "short_description": "A ghost summoned by mirrors.",
        "long_description": """

Bloody Mary: A Detailed Description of the Urban Legend
Introduction
Bloody Mary is a widespread urban legend—and ritual game—centered around the idea of summoning a violent female spirit through a mirror. Versions of the legend exist across North America, Europe, and beyond, and each culture adds its own twist.
 Despite regional differences, every story shares one core idea:
Bloody Mary is a vengeful, mirror-dwelling apparition who appears when her name is chanted repeatedly in a dark room.
She is one of the most iconic figures in horror folklore, functioning as both a supernatural threat and a symbolic rite of passage for children and teenagers.

Origins and Evolution of the Legend
Folkloric Roots
The most likely origins of Bloody Mary draw from a mix of:
•	Witchcraft fears in early modern Europe
•	The association of mirrors with spirits in Victorian superstition
•	Bloody Queen Mary I of England, though this link is not universal and is mostly added by modern retellings
•	Folk practices of scrying, where young girls gazed into mirrors to see their future husbands
Over time, these elements blended into a darker, more frightening figure.
A Teenage Ritual
By the mid-20th century, the legend became a sleepover dare or bathroom game:
•	Lights off
•	Candle lit
•	Chant “Bloody Mary” three, thirteen, or forty times (variants exist)
•	Stare into the mirror
•	Wait for her to appear
What happens next is the heart of the myth.

Appearance
Bloody Mary’s appearance varies widely depending on the story, but common descriptions include:
1. Pale, Ghostly Woman
•	Skin white as bone, cold and lifeless
•	Dark or hollow eyes that appear sunken or bleeding
•	Long, tangled black or blood-soaked hair
•	A face that shifts between beauty and horror
2. Blood-Covered or Wounded
Some versions emphasize her violent death:
•	A slashed mouth
•	Bleeding eyes
•	Gaping wounds
•	A torn dress soaked in red
3. Mirror Distortion
She may appear first as:
•	A distorted face behind your own
•	A shadowy figure lurking over your shoulder
•	A reflection moving out of sync
In many stories, she is not a clear image but a warped presence emerging through the glass, making the mirror feel alive and predatory.

Behavior and Manifestations
1. Summoning
Bloody Mary typically appears only when invoked. The chant acts as:
•	A summoning ritual
•	A challenge
•	A symbolic breaking of the barrier between the living and the dead
The mirror serves as a portal, reflecting the old belief that reflections can trap or release spirits.
2. The Arrival
Her arrival is often preceded by:
•	The room growing colder
•	Candle flames flickering violently
•	Breathing sounds behind you
•	Your reflection shifting or smiling on its own
•	Whispered words no one else can hear
3. Attack or Confrontation
Many versions claim she attacks:
•	Scratching or clawing at the summoner’s face
•	Dragging them into the mirror
•	Breaking the glass violently, causing accidents
•	Screaming so loudly it causes fainting or hysteria
Sometimes she simply stares, her dead eyes locking with the summoner’s until they look away.
4. Alternative Versions
Not all stories present her as lethal. Variants include:
•	A murdered woman seeking justice
•	A warning spirit revealing secrets
•	A ghost trying to communicate rather than harm
Still, the vast majority of tales portray her as malicious and unstoppable once summoned.

Possible Identities Behind the Legend
The name “Bloody Mary” has been retrospectively linked to several figures, though folklorists agree the legend does not come cleanly from any one person:
Mary I of England (Bloody Mary)
•	Known for executing Protestants
•	Some legends say her spirit is vengeful
Mary Worth
•	A suspected witch
•	A victim of a horrific death
•	Or a child murderer (varies by region)
Mary Whales / Mary White
•	A girl who died tragically
•	Often involving mirrors or vanity
These identifications are later additions used to explain an already-existing mirror ghost tradition.

Symbolism and Psychological Meaning
The Bloody Mary legend persists because it taps into several deep fears:
1. Fear of Mirrors
Mirrors are inherently uncanny—familiar yet not real. Many cultures believe they reflect the soul or act as gateways.
2. Fear of Female Rage
Bloody Mary often symbolizes:
•	Wronged women
•	Dangerous femininity
•	Punishment for vanity or curiosity
3. Childhood Anxiety and Dares
The ritual is a test of bravery:
•	Peer pressure
•	Facing darkness
•	Confronting a supernatural threat
4. The Uncanny Reflection
Seeing something wrong in your reflection is a primal fear—your double turning against you.

Bloody Mary in Modern Culture
Bloody Mary has become an iconic horror figure, appearing in:
•	Movies (e.g., Urban Legends: Bloody Mary, The Legend of Bloody Mary)
•	Paranormal TV shows
•	Internet creepypasta
•	Video games
•	Halloween attractions
•	Countless schoolyard tales
Her myth continues because each new generation reshapes her into something fresh—and terrifying.

""",
        "image": "bloodymary.png"
    },
    {
        "id": 4,
        "name": "Mothman",
        "short_description": "A red-eyed figure seen before disasters.",
        "long_description": """
Mothman: A Detailed Description of the Urban Myth
Introduction
Mothman is a legendary creature associated with strange sightings, mysterious warnings, and eerie paranormal activity centered primarily around Point Pleasant, West Virginia in the 1960s. Part cryptid, part omen, part supernatural entity, Mothman is one of the most enduring figures in American folklore.
The legend blends eyewitness reports, local fear, psychological hysteria, and possible government conspiracy—making it one of the most complex of all modern cryptid myths.

Physical Description
Although sightings vary, most accounts agree on several key features:
1. Humanoid Shape
Mothman typically appears as a broad, tall humanoid figure, standing between 6 to 8 feet tall.
2. Large, Batlike or Mothlike Wings
His wings are usually described as:
•	10–15 feet across
•	Batlike, leathery, or insect-like depending on the witness
•	Folded behind him or snapping open suddenly
•	Capable of silent, rapid flight
Witnesses report he can take off straight from the ground without running, defying normal physics.
3. Glowing Red Eyes
The most iconic feature:
•	Large, glowing red or orange eyes
•	Said to reflect car headlights or glow unnaturally in the dark
•	Witnesses often describe feeling paralyzed, terrified, or hypnotized when seeing them
4. Dark, Shadowy Body
Mothman’s body is often described as:
•	Black or dark charcoal gray
•	Smooth or covered in fine fur
•	Bulky or muscular despite his ability to fly
•	Sometimes lacking distinct arms or head shape
5. No Visible Face
Many witnesses claim that:
•	They could not see a clear face
•	The eyes seemed embedded in the chest or shoulders
•	His head was small, sunken, or absent entirely
This faceless, otherworldly quality adds to the creature’s unnerving presence.

Behavior and Reported Actions
1. Silent Pursuit
Mothman is known for flying:
•	Completely silently
•	Easily keeping pace with speeding cars
•	Hovering or gliding without flapping his wings
Witnesses often report a sense of being watched or followed.
2. Fear Induction
People claim to feel:
•	Sudden, overwhelming dread
•	A sense that something terrible is about to happen
•	Physical symptoms like cold chills or nausea
This emotional effect is one of Mothman’s signature traits.
3. Appearing as an Omen
The legend is heavily associated with the idea that Mothman appears as a warning of impending disaster.
The most famous example is the collapse of the Silver Bridge in 1967, which killed 46 people. Many locals claim Mothman sightings increased right before the tragedy, creating a belief that he was either:
•	Trying to warn humanity, or
•	A harbinger of the disaster itself
This dual interpretation—protector or omen—defines much of Mothman’s mythos.

The Point Pleasant Wave (1966–1967)
The core of Mothman legend comes from a year-long wave of sightings in Point Pleasant.
Key events include:
•	November 15, 1966: Two young couples spotted a large flying creature with glowing red eyes near an abandoned TNT factory outside town. This was the first highly publicized sighting.
•	Following reports described:
o	Creatures pacing cars at high speed
o	Soldiers or locals seeing it perched on buildings
o	Strange lights in the sky
o	Unexplained animal mutilations
Paranormal “Flaps”
At the same time, locals reported:
•	Men in Black encounters
•	UFO sightings
•	Telepathic experiences
•	Odd phone calls
•	Electrical interference
Mothman sightings happened alongside these, creating an atmosphere of paranoia and mystery.

Habitat: The TNT Area
Many sightings cluster around:
The McClintic Wildlife Management Area
Formerly:
•	A WWII munitions facility
•	Filled with underground bunkers and abandoned structures
•	Covered by dense forest and swamp
These eerie conditions made it the perfect place for a creature to hide—and for imagination to run wild.

Explanations and Theories
Various explanations have been offered over the decades:
1. Misidentified Animals
Possibly:
•	A sandhill crane
•	A barred owl
•	Large herons
•	Deformed or oversized birds
Critics argue these explanations fail to match the consistency of sightings.
2. Mass Hysteria
Some anthropologists believe the Mothman flap was:
•	A psychological response to Cold War tension
•	Amplified by media and rumor
•	Fueled by fear of the unknown
3. Government Experiments
Conspiracy theories point to:
•	Secret military activity in the TNT area
•	Experimental aircraft
•	Mutations caused by leftover chemicals
4. Extraterrestrial Entity
Many UFO believers see Mothman as:
•	An alien observer
•	A being from another dimension
•	A scout or messenger
5. Supernatural Omen
The most enduring interpretation:
 Mothman is a prophetic warning sign tied to disaster.

Cultural Impact
Mothman has grown into an international phenomenon:
•	Books, especially John Keel’s The Mothman Prophecies
•	The 2002 movie starring Richard Gere
•	Statues and museums in Point Pleasant
•	Annual festivals that attract thousands
•	Appearances in games, comics, and horror shows
He has become a symbol of mystery, fear, and the thin boundary between the normal and the paranormal.

Symbolism
Mothman represents:
The Fear of the Unknown
His undefined nature allows people to project their deepest fears onto him.
Modern Folklore in Action
A real town, real witnesses, and an unexplained phenomenon combine into a lasting legend.
The Omen Motif
Like the banshee or black dogs of European folklore, Mothman is part of a tradition of creatures tied to disaster.
A Blending of Worlds
The legend merges:
•	Cryptozoology
•	UFOlogy
•	Folklore
•	Psychological phenomena
•	Conspiracy theory
This mix keeps the legend alive and ever-evolving.



""",
        "image": "mothman.png"
    },
    {
        "id": 5,
        "name": "Crooked Man",
        "short_description": "A shadow figure from urban legend.",
        "long_description": """

The Crooked Man: A Detailed Description of the Modern Urban Myth
Origins in Rhyme
The Crooked Man originates loosely from the old English nursery rhyme:
“There was a crooked man, who walked a crooked mile…”
Historically, the original rhyme was harmless, but over time—especially through internet horror, creepypasta, and modern mythmaking—the Crooked Man evolved into a far more sinister figure.
 Instead of a quaint character who lives in a crooked house, he became an unnerving supernatural entity whose entire form and existence embody distortion, imbalance, and wrongness.

Appearance
Descriptions of the Crooked Man vary, but most modern interpretations share the following traits:
Extremely Tall and Unnaturally Thin
•	His body is stretched almost to breaking, like a figure pulled too far by invisible hands.
•	Limbs are elongated, jointed at impossible angles, giving him a sticklike, skeletal silhouette.
Crooked Form
Every aspect of him is bent, twisted, or misaligned:
•	One shoulder much higher than the other
•	A neck that tilts sharply to the side
•	A spine that forms a deep S-curve
•	Legs bent in different directions, as though broken and healed improperly
This exaggerated asymmetry gives him a disturbing, insect-like gait.
Face
His face is the most unsettling element:
•	Hollow, sunken eyes that may glow faintly or appear misty and blank
•	A long jaw that opens too wide when he smiles
•	Teeth crooked like shattered glass inside a warped frame
Some versions say he wears a slanted top hat or ragged Victorian-style coat, adding to his uncanny silhouette.

Movement
One of the most iconic traits of the Crooked Man is his unnatural method of movement:
Jerky, angular motions
He moves like a marionette with cut strings—every step a series of sudden, jarring angles.
Crooked gait
He never walks in straight lines.
 Even when approaching a victim directly, he zigzags or spirals toward them in a disorienting, nausea-inducing rhythm.
Silent until he wants to be heard
He often appears soundlessly, despite his twisted frame scraping the ground. When he does make noise, it’s usually:
•	The creaking of bones
•	A dragging foot
•	A distorted version of the nursery rhyme whispered or sung off-key

Behavior and Mythology
Modern urban legends portray the Crooked Man as an entity that emerges in situations of emotional or psychological imbalance.
1. Attracted to Brokenness
The Crooked Man is drawn to:
•	Households filled with conflict
•	People who are depressed, grieving, or guilt-ridden
•	Environments where something—emotionally or morally—is “crooked”
He feeds on turmoil, twisting people’s lives in ways that mirror his body.
2. Manifestation Through Rhyme
Many stories say that reciting or hearing the nursery rhyme draws his attention.
 In some versions:
•	Whispering the rhyme invites him
•	Hearing it backwards means he is already near
•	The “crooked mile” refers metaphorically to the path he takes from shadow to victim
3. Imitation and Mockery
He is known for:
•	Mimicking voices in warped, strangled tones
•	Repeating victims’ words back to them in a broken rhythm
•	Appearing in reflections slightly “off,” indicating he is about to cross into the physical world
4. Punisher of Disharmony
In many modern interpretations, he "corrects" what he sees as emotional or moral crookedness by twisting:
•	The fate of families
•	The structure of homes
•	The physical bodies of his victims
His interventions tend to escalate:
•	From strange noises
•	To objects placed at odd angles
•	To sightings in corners
•	To direct confrontation

Signs of His Presence
Common warning signs include:
•	Objects bending or a house subtly tilting, as though warping around him
•	Footprints that zigzag or circle instead of going straight
•	Children singing the rhyme without being taught it
•	Mirrors showing a distorted version of one’s reflection
•	Seeing a tall, crooked silhouette at the end of a hallway
He often appears at night, lurking just beyond the edge of flickering light.

Motif and Symbolism
The Crooked Man symbolizes:
Distortion of reality
His bent form reflects how fear can warp perception.
Moral imbalance
Stories portray him as a supernatural judge of broken families or troubled individuals.
Childhood innocence corrupted
A harmless rhyme becomes a vessel of dread—one of the hallmarks of modern horror folklore.
Uncanny asymmetry
Humans instinctively fear things that look almost human but not quite right; the Crooked Man embodies this uncanny valley perfectly.

Presence in Modern Pop Culture
The Crooked Man has appeared or been reimagined in:
•	Creepypasta and internet horror forums
•	Independent films
•	Short stories and online animations
•	Video games like The Crooked Man (2012)
•	Horror cinema (often as a variant or inspiration, though “The Conjuring 2” created a popular depiction)
Each version emphasizes distortion, wrongness, and the violation of human form.

""",
        "image": "crookedman.png"
    }
]


# ---------------------------------------
# Helper Functions
# ---------------------------------------
def get_serializer():
    """Return a serializer used for generating/verifying tokens."""
    return URLSafeTimedSerializer(
        secret_key=current_app.config["SECRET_KEY"],
        salt=current_app.config.get("SECURITY_PASSWORD_SALT", "email-confirm"),
    )


def send_verification_email(to_email: str, token: str):
    """Send account verification email."""
    verify_url = url_for("main.verify_email", token=token, _external=True)

    html_body = render_template("verify_email.html", verify_url=verify_url)
    text_body = f"Please verify your account by visiting: {verify_url}"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Verify your Urban Myths account"
    msg["From"] = current_app.config["MAIL_USERNAME"]
    msg["To"] = to_email

    msg.attach(MIMEText(text_body, "plain"))
    msg.attach(MIMEText(html_body, "html"))

    try:
        with smtplib.SMTP(
            current_app.config["MAIL_SERVER"],
            current_app.config["MAIL_PORT"]
        ) as server:

            if current_app.config.get("MAIL_USE_TLS", False):
                server.starttls()

            server.login(
                current_app.config["MAIL_USERNAME"],
                current_app.config["MAIL_PASSWORD"]
            )

            server.sendmail(msg["From"], [msg["To"]], msg.as_string())

    except Exception as e:
        print("Error sending email:", e)


# ---------------------------------------
# Public Routes
# ---------------------------------------
@main.route("/")
def index():
    return render_template("index.html")


@main.route("/about")
def about():
    return render_template("about.html")


@main.route("/feedback", methods=["GET", "POST"])
def feedback():
    if request.method == "POST":
        message = request.form.get("message")
        print("FEEDBACK RECEIVED:", message)  # Temporary logging

    return render_template("feedback.html")


# ---------------------------------------
# Registration
# ---------------------------------------
@main.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if len(username) < 5:
            flash("Username must be at least 5 characters.", "danger")
            return render_template("register.html")

        if not email or not password:
            flash("Email and password are required.", "danger")
            return render_template("register.html")

        conn = get_db()
        if conn is None:
            flash("Database connection error. Could not connect to MySQL.", "danger")
            return render_template("register.html")

        cur = conn.cursor(dictionary=True)

        # Check if email is already registered
        cur.execute("SELECT id FROM users WHERE email = %s", (email,))
        if cur.fetchone():
            flash("Email is already registered.", "danger")
            cur.close()
            return render_template("register.html")

        password_hash = generate_password_hash(password)

        # Insert user, not yet verified
        cur.execute(
            """
            INSERT INTO users (username, email, password_hash, is_verified)
            VALUES (%s, %s, %s, %s)
            """,
            (username, email, password_hash, 0),
        )
        conn.commit()
        cur.close()

        # Generate verification token
        s = get_serializer()
        token = s.dumps(email)

        # For debugging
        verify_url = url_for("main.verify_email", token=token, _external=True)
        print("\n✅ VERIFICATION LINK (FOR TESTING):\n", verify_url, "\n")

        # Send email
        send_verification_email(email, token)

        flash("Account created! Check your email to verify your account.", "success")
        return redirect(url_for("main.login"))

    return render_template("register.html")


# ---------------------------------------
# Email Verification
# ---------------------------------------
@main.route("/verify/<token>")
def verify_email(token):
    s = get_serializer()

    try:
        email = s.loads(token, max_age=3600)  # 1 hour expiration
    except SignatureExpired:
        flash("The verification link has expired.", "danger")
        return redirect(url_for("main.login"))
    except BadSignature:
        flash("Invalid verification link.", "danger")
        return redirect(url_for("main.login"))

    conn = get_db()
    if conn is None:
        flash("Database connection error.", "danger")
        return redirect(url_for("main.login"))

    cur = conn.cursor()
    cur.execute("UPDATE users SET is_verified = 1 WHERE email = %s", (email,))
    conn.commit()
    cur.close()

    flash("Email verified! You can now log in.", "success")
    return redirect(url_for("main.login"))


# ---------------------------------------
# Login, Logout & Dashboard
# ---------------------------------------
@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        success, message = handle_login(email, password)

        if success:
            flash(message, "success")
            return redirect(url_for("main.dashboard"))
        else:
            flash(message, "danger")
            return render_template("login.html")

    return render_template("login.html")

@main.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    return render_template(
        "dashboard.html",
        myths=MYTHS,
        username=session.get("username")
    )
    
    query = request.args.get("q")
    if query:
        myths = [
        myth for myth in myths
        if query.lower() in myth["name"].lower()
        or query.lower() in myth["short_description"].lower()
        ]
    
    return render_template(
        "dashboard.html",
        username=session.get("username"),
        myths=myths
    )


@main.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("main.login"))



@main.route("/myth/<int:myth_id>")
def myth_detail(myth_id):
    myth = next((m for m in MYTHS if m["id"] == myth_id), None)

    if myth is None:
        abort(404)

    return render_template("myth.html", myth=myth)