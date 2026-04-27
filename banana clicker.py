
import tkinter as tk
import random
import json
import os

SAVE_FILE = "save.json"

# =========================
# UTILS
# =========================
def fmt(n):
    if n >= 1_000_000_000:
        return f"{n/1_000_000_000:.2f}B"
    if n >= 1_000_000:
        return f"{n/1_000_000:.2f}M"
    if n >= 1_000:
        return f"{n/1_000:.2f}K"
    return str(int(n))

def clamp(x, a, b):
    return max(a, min(b, x))

# =========================
# STATE
# =========================
fruit = 0
click_power = 1
upgrade_cost = 25

mutation_points = 0
prestige_cost = 250000  # first prestige requirement

click_count = 0
next_roast_at = random.randint(25, 40)

last_action_seconds = 0

banana_types = [
    "basic banana",
    "slightly bruised banana",
    "store-brand banana",
    "factory banana",
    "lab banana",
    "radioactive banana (weak)",
    "cyber banana",
    "banana with existential crisis",
    "illegal banana prototype",
    "banana from another timeline",
]

generators = [
    {"name": "backyard farm", "income": 1, "cost": 60, "owned": 0},
    {"name": "banana shed", "income": 2, "cost": 120, "owned": 0},
    {"name": "small plantation", "income": 4, "cost": 250, "owned": 0},
    {"name": "industrial farm block", "income": 8, "cost": 600, "owned": 0},
    {"name": "mutated greenhouse", "income": 15, "cost": 1500, "owned": 0},
    {"name": "illegal banana ring", "income": 30, "cost": 4000, "owned": 0},
    {"name": "quantum soil reactor", "income": 60, "cost": 10000, "owned": 0},
]

# =========================
# UI
# =========================
root = tk.Tk()
root.geometry("380x700")
root.title("Mutation Fruit 🍌")
root.configure(bg="black")

fruit_label = tk.Label(root, fg="yellow", bg="black", font=("Arial", 16))
fruit_label.pack(pady=5)

mp_label = tk.Label(root, fg="cyan", bg="black", font=("Arial", 12))
mp_label.pack(pady=2)

dialog = tk.Label(
    root,
    text="Welcome to the banana nightmare.",
    fg="white",
    bg="black",
    font=("Courier", 11),
    wraplength=360
)
dialog.pack(pady=10)

click_button = tk.Button(root, text="🍌 CLICK", font=("Arial", 18))
click_button.pack(pady=10)

upgrade_btn = tk.Button(root, font=("Arial", 12))
upgrade_btn.pack(pady=5)

prestige_btn = tk.Button(root, font=("Arial", 12))
prestige_btn.pack(pady=5)

save_btn = tk.Button(root, font=("Arial", 10), text="💾 SAVE")
save_btn.pack(pady=2)

load_btn = tk.Button(root, font=("Arial", 10), text="📂 LOAD")
load_btn.pack(pady=2)

frame = tk.Frame(root, bg="black")
frame.pack(pady=10)

gen_buttons = []
for g in generators:
    b = tk.Button(frame, width=40, font=("Arial", 10))
    b.pack(pady=2)
    gen_buttons.append(b)

# =========================
# DIALOG SYSTEM
# =========================
def say(msg):
    dialog.config(text=msg)

# =========================
# ROAST SYSTEM
# =========================
def roast_click():
    msgs = [
        "still clicking manually… bro this is slow pain farming.",
        "you really chose hand labor in 2026 💀",
        "automation exists but ok go off I guess.",
        "this grind is unnecessarily personal.",
        "you're basically mining bananas with your soul."
    ]
    say(random.choice(msgs))

def roast_upgrade(ok):
    if ok:
        msgs = [
            "upgrade done… still feels slow tho.",
            "you got stronger but progression said 'meh'.",
            "numbers went up, nothing else changed.",
            "this is growth but like… tiny growth."
        ]
    else:
        msgs = [
            "bro you're broke 💀",
            "upgrade menu open with zero budget energy.",
            "you can't afford basic evolution.",
            "financially blocked."
        ]
    say(random.choice(msgs))

def roast_buy(name, ok):
    if ok:
        msgs = [
            f"{name} online. progression slightly less painful now.",
            "automation added… you're slowly becoming irrelevant.",
            "cool, now it runs a bit without you.",
            "you outsourced your entire job again."
        ]
    else:
        msgs = [
            "can't afford it 💀 still early game mindset.",
            "this is way above your current tier.",
            "go grind more, this ain't it.",
            "locked behind poverty wall."
        ]
    say(random.choice(msgs))

def roast_idle():
    msgs = [
        "AFK detected… you abandoned your bananas.",
        "you left. bananas still exist without you.",
        "idle mode activated. you're not needed anyway.",
        "bro went offline. banana economy collapsed emotionally."
    ]
    say(random.choice(msgs))

# =========================
# SAVE / LOAD
# =========================
def save_game():
    data = {
        "fruit": fruit,
        "click_power": click_power,
        "upgrade_cost": upgrade_cost,
        "mutation_points": mutation_points,
        "prestige_cost": prestige_cost,
        "generators": generators
    }

    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)

    say("💾 saved. now go touch grass.")

def load_game():
    global fruit, click_power, upgrade_cost, mutation_points, prestige_cost, generators

    if not os.path.exists(SAVE_FILE):
        say("no save file found. bro you have nothing.")
        return

    with open(SAVE_FILE, "r") as f:
        data = json.load(f)

    fruit = data.get("fruit", 0)
    click_power = data.get("click_power", 1)
    upgrade_cost = data.get("upgrade_cost", 25)
    mutation_points = data.get("mutation_points", 0)
    prestige_cost = data.get("prestige_cost", 250000)

    saved_gens = data.get("generators", [])
    for i in range(len(generators)):
        if i < len(saved_gens):
            generators[i]["owned"] = saved_gens[i].get("owned", 0)
            generators[i]["cost"] = saved_gens[i].get("cost", generators[i]["cost"])

    say("📂 loaded. welcome back to suffering.")
    update_ui()

save_btn.config(command=save_game)
load_btn.config(command=load_game)

# =========================
# MUTATION BONUS
# =========================
def click_bonus():
    return 1 + (mutation_points * 0.15)

def income_bonus():
    return 1 + (mutation_points * 0.10)

# =========================
# CLICK + CRIT SYSTEM
# =========================
def click():
    global fruit, click_count, next_roast_at, last_action_seconds

    last_action_seconds = 0

    crit_chance = clamp(0.08 + mutation_points * 0.01, 0.08, 0.25)
    crit_mult = 5

    gained = click_power * click_bonus()

    if random.random() < crit_chance:
        gained *= crit_mult
        say(f"💥 CRITICAL CLICK! +{fmt(gained)} fruit")

    fruit += gained
    click_count += 1

    if click_count % 25 == 0:
        say(f"discovered: {random.choice(banana_types)}")

    if click_count >= next_roast_at:
        roast_click()
        next_roast_at = click_count + random.randint(25, 45)

    update_ui()

click_button.config(command=click)

# =========================
# UPGRADE
# =========================
def upgrade():
    global fruit, click_power, upgrade_cost, last_action_seconds

    last_action_seconds = 0

    if fruit >= upgrade_cost:
        fruit -= upgrade_cost
        click_power += 1
        upgrade_cost = int(upgrade_cost * 1.8)
        roast_upgrade(True)
    else:
        roast_upgrade(False)

    update_ui()

upgrade_btn.config(command=upgrade)

# =========================
# GENERATORS
# =========================
def buy(i):
    global fruit, last_action_seconds

    last_action_seconds = 0

    g = generators[i]

    if fruit >= g["cost"]:
        fruit -= g["cost"]
        g["owned"] += 1
        g["cost"] = int(g["cost"] * 1.65)
        roast_buy(g["name"], True)
    else:
        roast_buy(g["name"], False)

    update_ui()

for i in range(len(gen_buttons)):
    gen_buttons[i].config(command=lambda i=i: buy(i))

# =========================
# RANDOM EVENTS
# =========================
def random_event():
    global fruit

    # small chance each 15 seconds
    if random.random() < 0.35:
        event_type = random.randint(1, 5)

        if event_type == 1:
            bonus = int(200 * income_bonus() + random.randint(50, 250))
            fruit += bonus
            say(f"🍀 banana blessing happened. +{fmt(bonus)} fruit")

        elif event_type == 2:
            loss = int(fruit * 0.05)
            fruit -= loss
            say(f"🦹 banana thief stole {fmt(loss)} fruit. skill issue.")

        elif event_type == 3:
            bonus = int(500 * income_bonus() + random.randint(0, 500))
            fruit += bonus
            say(f"⚡ quantum banana glitch. +{fmt(bonus)} fruit")

        elif event_type == 4:
            bonus = int(fruit * 0.02)
            fruit += bonus
            say(f"📈 banana market pump. +{fmt(bonus)} fruit")

        elif event_type == 5:
            say("🌪 banana storm. nothing happened. still miserable.")

        update_ui()

    root.after(15000, random_event)

# =========================
# PRESTIGE SYSTEM
# =========================
def prestige():
    global fruit, click_power, upgrade_cost, mutation_points, prestige_cost, generators, click_count

    if fruit < prestige_cost:
        say(f"not enough fruit for mutation reset. need {fmt(prestige_cost)}.")
        return

    gained_mp = max(1, int(fruit / prestige_cost))
    mutation_points += gained_mp

    fruit = 0
    click_power = 1
    upgrade_cost = 25
    click_count = 0

    for g in generators:
        g["owned"] = 0
        g["cost"] = int(g["cost"] * 0.75)  # slight help after prestige

    prestige_cost = int(prestige_cost * 2.2)

    say(f"🧬 MUTATION RESET! +{gained_mp} mutation points gained.")
    update_ui()

prestige_btn.config(command=prestige)

# =========================
# PASSIVE INCOME
# =========================
def passive():
    global fruit, last_action_seconds

    last_action_seconds += 1

    total = sum(g["income"] * g["owned"] for g in generators)
    total = int(total * income_bonus())

    fruit += total

    update_ui()
    root.after(1000, passive)

# =========================
# IDLE CHECK
# =========================
def idle_check():
    # Only roast if player is truly idle
    if last_action_seconds > 12:
        if random.random() < 0.4:
            roast_idle()

    root.after(12000, idle_check)

# =========================
# UI UPDATE
# =========================
def update_ui():
    fruit_label.config(text=f"FRUIT: {fmt(fruit)}")
    mp_label.config(text=f"MUTATION POINTS: {mutation_points} | Click Bonus x{click_bonus():.2f} | Income Bonus x{income_bonus():.2f}")

    upgrade_btn.config(text=f"UPGRADE CLICK (+1) Cost: {fmt(upgrade_cost)}")
    prestige_btn.config(text=f"🧬 PRESTIGE (Need {fmt(prestige_cost)})")

    for i, g in enumerate(generators):
        gen_buttons[i].config(
            text=f"{g['name']} | Owned: {g['owned']} | Cost: {fmt(g['cost'])} | +{g['income']}/s"
        )

# =========================
# START
# =========================
update_ui()
passive()
idle_check()
random_event()

root.mainloop()