import sqlite3
import random
import time
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import asyncio

TOKEN = "8698059562:AAFco5fVhthHvByAzSx1rOfvcKiQcY7HX8o"
DEVELOPER_ID = 6650102723

# ==================== КЕЙСЫ ====================
CASES = {
    "bomzh": {
        "name": "Кейс бомжа",
        "cost": 100,
        "items": [
            {"name": "TEC-9 Tie Dye", "price": 10, "rarity": "Обычный", "type": "Оружие", "weight": 10},
            {"name": "UMP45 Shark", "price": 15, "rarity": "Обычный", "type": "Оружие", "weight": 10},
            {"name": "M110 Transition", "price": 20, "rarity": "Обычный", "type": "Оружие", "weight": 10},
            {"name": "M60 Quantum", "price": 25, "rarity": "Обычный", "type": "Оружие", "weight": 10},
            {"name": "FAMAS Stellar Blitz", "price": 30, "rarity": "Обычный", "type": "Оружие", "weight": 10},
            {"name": "SM1014 Facet", "price": 35, "rarity": "Обычный", "type": "Оружие", "weight": 10},
            {"name": "Sticker Fingerprint", "price": 10, "rarity": "Обычный", "type": "Стикер", "weight": 10},
            {"name": "Sticker Hound of Hades", "price": 40, "rarity": "Обычный", "type": "Стикер", "weight": 10},
            {"name": "Sticker Syndicate", "price": 45, "rarity": "Обычный", "type": "Стикер", "weight": 10},
            {"name": "Charm Hoplit Helmet", "price": 50, "rarity": "Обычный", "type": "Чарм", "weight": 10},
            {"name": "M4A1 Stainless", "price": 40, "rarity": "Обычный", "type": "Оружие", "weight": 10},
            {"name": "Desert Eagle Eclipse", "price": 45, "rarity": "Обычный", "type": "Оружие", "weight": 10},
            {"name": "Akimbo Uzi Zenith", "price": 50, "rarity": "Обычный", "type": "Оружие", "weight": 10},
            {"name": "M9 Bayonet Dark Shiver", "price": 4360, "rarity": "Редкий", "type": "Оружие", "weight": 0.1},
            {"name": "Karambit Widow's Weave", "price": 1740, "rarity": "Редкий", "type": "Оружие", "weight": 0.1},
            {"name": "Butterfly Dragon Glass", "price": 2400, "rarity": "Редкий", "type": "Оружие", "weight": 0.1},
            {"name": "M9 Bayonet Twilight", "price": 5400, "rarity": "Эпический", "type": "Оружие", "weight": 0.05},
            {"name": "Karambit Universe", "price": 6170, "rarity": "Эпический", "type": "Оружие", "weight": 0.05},
            {"name": "AWM Winter Sport", "price": 14444, "rarity": "Эпический", "type": "Оружие", "weight": 0.05},
            {"name": "Butterfly Twilight", "price": 999999, "rarity": "Легендарный", "type": "Оружие", "weight": 0.01},
        ]
    },
    "lyubitel": {
        "name": "Кейс любителя",
        "cost": 250,
        "items": [
            {"name": "Desert Eagle Eclipse", "price": 30, "rarity": "Обычный", "type": "Оружие", "weight": 10},
            {"name": "Akimbo Uzi Zenith", "price": 40, "rarity": "Обычный", "type": "Оружие", "weight": 10},
            {"name": "Sticker Minotaur", "price": 35, "rarity": "Обычный", "type": "Стикер", "weight": 10},
            {"name": "M16 Camouflage", "price": 50, "rarity": "Обычный", "type": "Оружие", "weight": 10},
            {"name": "Sticker Talon Stab", "price": 45, "rarity": "Обычный", "type": "Стикер", "weight": 10},
            {"name": "M60 Grunge", "price": 60, "rarity": "Обычный", "type": "Оружие", "weight": 10},
            {"name": "G22 Reindeer Sweater", "price": 70, "rarity": "Обычный", "type": "Оружие", "weight": 10},
            {"name": "Desert Eagle Blood", "price": 80, "rarity": "Обычный", "type": "Оружие", "weight": 10},
            {"name": "MP7 Ridge", "price": 90, "rarity": "Обычный", "type": "Оружие", "weight": 10},
            {"name": "SPAS Vibe", "price": 100, "rarity": "Обычный", "type": "Оружие", "weight": 10},
            {"name": "SM1014 Arctic", "price": 110, "rarity": "Обычный", "type": "Оружие", "weight": 10},
            {"name": "MP5 Blueprint", "price": 120, "rarity": "Обычный", "type": "Оружие", "weight": 10},
            {"name": "Charm Baby Penguin", "price": 125, "rarity": "Обычный", "type": "Чарм", "weight": 10},
            {"name": "M9 Bayonet Dark Shiver", "price": 4360, "rarity": "Редкий", "type": "Оружие", "weight": 0.1},
            {"name": "Karambit Widow's Weave", "price": 1740, "rarity": "Редкий", "type": "Оружие", "weight": 0.1},
            {"name": "Butterfly Dragon Glass", "price": 2400, "rarity": "Редкий", "type": "Оружие", "weight": 0.1},
            {"name": "M9 Bayonet Twilight", "price": 5400, "rarity": "Эпический", "type": "Оружие", "weight": 0.05},
            {"name": "Karambit Universe", "price": 6170, "rarity": "Эпический", "type": "Оружие", "weight": 0.05},
            {"name": "AWM Winter Sport", "price": 14444, "rarity": "Эпический", "type": "Оружие", "weight": 0.05},
            {"name": "Butterfly Twilight", "price": 999999, "rarity": "Легендарный", "type": "Оружие", "weight": 0.01},
        ]
    },
    "legendy": {
        "name": "Кейс легенды",
        "cost": 500,
        "items": [
            {"name": "MP5 Blueprint", "price": 60, "rarity": "Обычный", "type": "Оружие", "weight": 10},
            {"name": "Charm Baby Penguin", "price": 70, "rarity": "Обычный", "type": "Чарм", "weight": 10},
            {"name": "UMP45 Warchief", "price": 80, "rarity": "Обычный", "type": "Оружие", "weight": 10},
            {"name": "TEC-9 Stickerbomb", "price": 90, "rarity": "Обычный", "type": "Оружие", "weight": 10},
            {"name": "Sticker Frostbite", "price": 100, "rarity": "Обычный", "type": "Стикер", "weight": 10},
            {"name": "M60 Ares", "price": 110, "rarity": "Обычный", "type": "Оружие", "weight": 10},
            {"name": "F/S Camo Storm", "price": 120, "rarity": "Обычный", "type": "Оружие", "weight": 10},
            {"name": "Sticker GigaSAUG", "price": 130, "rarity": "Обычный", "type": "Стикер", "weight": 10},
            {"name": "Sticker Reforged Gold", "price": 140, "rarity": "Обычный", "type": "Стикер", "weight": 10},
            {"name": "TEC-9 Splash", "price": 150, "rarity": "Обычный", "type": "Оружие", "weight": 10},
            {"name": "M16 Accuracy", "price": 160, "rarity": "Обычный", "type": "Оружие", "weight": 10},
            {"name": "M4 Flock", "price": 170, "rarity": "Обычный", "type": "Оружие", "weight": 10},
            {"name": "AWM Poseidon", "price": 180, "rarity": "Обычный", "type": "Оружие", "weight": 10},
            {"name": "M9 Bayonet Dark Shiver", "price": 4360, "rarity": "Редкий", "type": "Оружие", "weight": 0.1},
            {"name": "Karambit Widow's Weave", "price": 1740, "rarity": "Редкий", "type": "Оружие", "weight": 0.1},
            {"name": "Butterfly Dragon Glass", "price": 2400, "rarity": "Редкий", "type": "Оружие", "weight": 0.1},
            {"name": "M9 Bayonet Twilight", "price": 5400, "rarity": "Эпический", "type": "Оружие", "weight": 0.05},
            {"name": "Karambit Universe", "price": 6170, "rarity": "Эпический", "type": "Оружие", "weight": 0.05},
            {"name": "AWM Winter Sport", "price": 14444, "rarity": "Эпический", "type": "Оружие", "weight": 0.05},
            {"name": "Butterfly Twilight", "price": 999999, "rarity": "Легендарный", "type": "Оружие", "weight": 0.01},
        ]
    },
    "voin": {
        "name": "Кейс война",
        "cost": 1000,
        "items": [
            {"name": "AWM Poseidon", "price": 100, "rarity": "Обычный", "type": "Оружие", "weight": 10},
            {"name": "P90 Revenant", "price": 120, "rarity": "Обычный", "type": "Оружие", "weight": 10},
            {"name": "USP Purple Camo", "price": 140, "rarity": "Обычный", "type": "Оружие", "weight": 10},
            {"name": "P350 Gearshift", "price": 160, "rarity": "Обычный", "type": "Оружие", "weight": 10},
            {"name": "FAMAS Snow Storm", "price": 180, "rarity": "Обычный", "type": "Оружие", "weight": 10},
            {"name": "Charm Gene-X", "price": 200, "rarity": "Обычный", "type": "Чарм", "weight": 10},
            {"name": "M4 Kachi", "price": 220, "rarity": "Обычный", "type": "Оружие", "weight": 10},
            {"name": "FN FAL Astral Rift", "price": 240, "rarity": "Обычный", "type": "Оружие", "weight": 10},
            {"name": "M4 Ironclad", "price": 260, "rarity": "Обычный", "type": "Оружие", "weight": 10},
            {"name": "Charm Prey Gold", "price": 280, "rarity": "Обычный", "type": "Чарм", "weight": 10},
            {"name": "Desert Eagle Orochi", "price": 300, "rarity": "Обычный", "type": "Оружие", "weight": 10},
            {"name": "P350 4 Years", "price": 320, "rarity": "Обычный", "type": "Оружие", "weight": 10},
            {"name": "M4 R.O.N.I.N. mk56", "price": 340, "rarity": "Обычный", "type": "Оружие", "weight": 10},
            {"name": "M9 Bayonet Dark Shiver", "price": 4360, "rarity": "Редкий", "type": "Оружие", "weight": 0.1},
            {"name": "Karambit Widow's Weave", "price": 1740, "rarity": "Редкий", "type": "Оружие", "weight": 0.1},
            {"name": "Butterfly Dragon Glass", "price": 2400, "rarity": "Редкий", "type": "Оружие", "weight": 0.1},
            {"name": "M9 Bayonet Twilight", "price": 5400, "rarity": "Эпический", "type": "Оружие", "weight": 0.05},
            {"name": "Karambit Universe", "price": 6170, "rarity": "Эпический", "type": "Оружие", "weight": 0.05},
            {"name": "AWM Winter Sport", "price": 14444, "rarity": "Эпический", "type": "Оружие", "weight": 0.05},
            {"name": "Butterfly Twilight", "price": 999999, "rarity": "Легендарный", "type": "Оружие", "weight": 0.01},
        ]
    },
    "major": {
        "name": "Кейс мажора",
        "cost": 2500,
        "items": [
            {"name": "Desert Eagle Orochi", "price": 100, "rarity": "Обычный", "type": "Оружие", "weight": 10},
            {"name": "P350 4 Years", "price": 120, "rarity": "Обычный", "type": "Оружие", "weight": 10},
            {"name": "M4 R.O.N.I.N. mk56", "price": 140, "rarity": "Обычный", "type": "Оружие", "weight": 10},
            {"name": "Desert Eagle Red Dragon", "price": 160, "rarity": "Обычный", "type": "Оружие", "weight": 10},
            {"name": "UMP45 Arid", "price": 180, "rarity": "Обычный", "type": "Оружие", "weight": 10},
            {"name": "M4 Flex", "price": 200, "rarity": "Обычный", "type": "Оружие", "weight": 10},
            {"name": "M4A1 Serpent", "price": 220, "rarity": "Обычный", "type": "Оружие", "weight": 10},
            {"name": "USP Chameleon", "price": 240, "rarity": "Обычный", "type": "Оружие", "weight": 10},
            {"name": "AKR12 Carving", "price": 260, "rarity": "Обычный", "type": "Оружие", "weight": 10},
            {"name": "M16 Shogun Stripes", "price": 280, "rarity": "Обычный", "type": "Оружие", "weight": 10},
            {"name": "VAL Ronin", "price": 300, "rarity": "Обычный", "type": "Оружие", "weight": 10},
            {"name": "AWM Gear", "price": 320, "rarity": "Обычный", "type": "Оружие", "weight": 10},
            {"name": "M110 Top Secret", "price": 340, "rarity": "Обычный", "type": "Оружие", "weight": 10},
            {"name": "M9 Bayonet Dark Shiver", "price": 4360, "rarity": "Редкий", "type": "Оружие", "weight": 0.1},
            {"name": "Karambit Widow's Weave", "price": 1740, "rarity": "Редкий", "type": "Оружие", "weight": 0.1},
            {"name": "Butterfly Dragon Glass", "price": 2400, "rarity": "Редкий", "type": "Оружие", "weight": 0.1},
            {"name": "M9 Bayonet Twilight", "price": 5400, "rarity": "Эпический", "type": "Оружие", "weight": 0.05},
            {"name": "Karambit Universe", "price": 6170, "rarity": "Эпический", "type": "Оружие", "weight": 0.05},
            {"name": "AWM Winter Sport", "price": 14444, "rarity": "Эпический", "type": "Оружие", "weight": 0.05},
            {"name": "Butterfly Twilight", "price": 999999, "rarity": "Легендарный", "type": "Оружие", "weight": 0.01},
        ]
    }
}

RARITY_COLORS = {
    "Обычный": "⬜",
    "Необычный": "🟦",
    "Редкий": "🔵",
    "Эпический": "🟣",
    "Легендарный": "🩷",
    "Аркана": "❤️"
}

# ==================== МИНЫ ====================
MINE_MULTIPLIERS = {
    2: 1.1,
    4: 1.2,
    6: 1.4,
    12: 2.0,
    19: 5.0
}

# ==================== ФОРТУНА ====================
FORTUNE_EMOJIS = {
    "💣": {"name": "Проигрыш", "desc": "Ставка полностью сгорает", "multiplier": 0},
    "🎁": {"name": "Случайный скин", "desc": "Получи скин до 50 G", "multiplier": "skin"},
    "😬": {"name": "Возврат", "desc": "Ставка возвращается на баланс", "multiplier": 1},
    "🎰": {"name": "Промокод +100%", "desc": "Ставка увеличивается в 2 раза", "multiplier": 2},
    "🤑": {"name": "+20% к ставке", "desc": "Ставка увеличивается на 20%", "multiplier": 1.2},
    "🔥": {"name": "Сгорание с возвратом", "desc": "Ставка сгорает, но возвращается 20%", "multiplier": 0.2}
}

FORTUNE_WEIGHTS = {
    "💣": 30,
    "🎁": 15,
    "😬": 20,
    "🎰": 10,
    "🤑": 15,
    "🔥": 10
}

# ==================== ПОПОЛНЕНИЕ ====================
DEPOSIT_DATA = {
    50: {"price": 54.38, "pattern": 264},
    100: {"price": 101.69, "pattern": 890},
    150: {"price": 156.25, "pattern": 287},
    200: {"price": 203.93, "pattern": 821}
}

# ==================== БАЗА ДАННЫХ ====================
def init_db():
    conn = sqlite3.connect("cases_bot.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (telegram_id INTEGER PRIMARY KEY, balance INTEGER DEFAULT 0, reg_date TEXT, last_bonus TIMESTAMP DEFAULT "1970-01-01 00:00:00", username TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS inventory
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  telegram_id INTEGER, 
                  item_name TEXT, 
                  item_price REAL, 
                  item_rarity TEXT,
                  item_type TEXT,
                  case_name TEXT, 
                  open_date TEXT, 
                  sold INTEGER DEFAULT 0)''')
    conn.commit()
    conn.close()

def register_user(telegram_id, username=None):
    conn = sqlite3.connect("cases_bot.db")
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (telegram_id, reg_date, last_bonus, username) VALUES (?, ?, ?, ?)", 
              (telegram_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "1970-01-01 00:00:00", username))
    if username:
        c.execute("UPDATE users SET username = ? WHERE telegram_id = ?", (username, telegram_id))
    conn.commit()
    conn.close()

def get_user_by_username(username):
    conn = sqlite3.connect("cases_bot.db")
    c = conn.cursor()
    c.execute("SELECT telegram_id FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def get_balance(telegram_id):
    conn = sqlite3.connect("cases_bot.db")
    c = conn.cursor()
    c.execute("SELECT balance FROM users WHERE telegram_id = ?", (telegram_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else 0

def update_balance(telegram_id, amount):
    conn = sqlite3.connect("cases_bot.db")
    c = conn.cursor()
    c.execute("UPDATE users SET balance = balance + ? WHERE telegram_id = ?", (amount, telegram_id))
    conn.commit()
    conn.close()

def deduct_balance(telegram_id, amount):
    conn = sqlite3.connect("cases_bot.db")
    c = conn.cursor()
    c.execute("UPDATE users SET balance = balance - ? WHERE telegram_id = ? AND balance >= ?", 
              (amount, telegram_id, amount))
    conn.commit()
    conn.close()

def add_item(telegram_id, item_name, item_price, item_rarity, item_type, case_name):
    conn = sqlite3.connect("cases_bot.db")
    c = conn.cursor()
    c.execute("INSERT INTO inventory (telegram_id, item_name, item_price, item_rarity, item_type, case_name, open_date) VALUES (?, ?, ?, ?, ?, ?, ?)",
              (telegram_id, item_name, item_price, item_rarity, item_type, case_name, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()
    return c.lastrowid

def get_inventory(telegram_id):
    conn = sqlite3.connect("cases_bot.db")
    c = conn.cursor()
    c.execute("SELECT id, item_name, item_price, item_rarity, item_type FROM inventory WHERE telegram_id = ? AND sold = 0 ORDER BY id DESC", 
              (telegram_id,))
    result = c.fetchall()
    conn.close()
    return result

def get_all_inventory(telegram_id):
    conn = sqlite3.connect("cases_bot.db")
    c = conn.cursor()
    c.execute("SELECT item_name, item_price, item_rarity, item_type FROM inventory WHERE telegram_id = ? AND sold = 0", (telegram_id,))
    result = c.fetchall()
    conn.close()
    return result

def get_most_expensive_item(telegram_id):
    conn = sqlite3.connect("cases_bot.db")
    c = conn.cursor()
    c.execute("SELECT item_name, item_price, item_rarity, item_type FROM inventory WHERE telegram_id = ? AND sold = 0 ORDER BY item_price DESC LIMIT 1", 
              (telegram_id,))
    result = c.fetchone()
    conn.close()
    return result

def sell_item(item_id, telegram_id):
    conn = sqlite3.connect("cases_bot.db")
    c = conn.cursor()
    c.execute("SELECT item_price FROM inventory WHERE id = ? AND telegram_id = ? AND sold = 0", (item_id, telegram_id))
    result = c.fetchone()
    if result:
        price = result[0]
        c.execute("UPDATE inventory SET sold = 1 WHERE id = ?", (item_id,))
        c.execute("UPDATE users SET balance = balance + ? WHERE telegram_id = ?", (price, telegram_id))
        conn.commit()
        conn.close()
        return price
    conn.close()
    return None

def get_history(telegram_id, limit=20):
    conn = sqlite3.connect("cases_bot.db")
    c = conn.cursor()
    c.execute("SELECT case_name, item_name, open_date FROM inventory WHERE telegram_id = ? ORDER BY id DESC LIMIT ?",
              (telegram_id, limit))
    result = c.fetchall()
    conn.close()
    return result

def get_last_bonus(telegram_id):
    conn = sqlite3.connect("cases_bot.db")
    c = conn.cursor()
    c.execute("SELECT last_bonus FROM users WHERE telegram_id = ?", (telegram_id,))
    result = c.fetchone()
    conn.close()
    if result and result[0]:
        try:
            return datetime.strptime(result[0], "%Y-%m-%d %H:%M:%S")
        except:
            return datetime.strptime("1970-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
    return datetime.strptime("1970-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")

def update_last_bonus(telegram_id):
    conn = sqlite3.connect("cases_bot.db")
    c = conn.cursor()
    c.execute("UPDATE users SET last_bonus = ? WHERE telegram_id = ?", 
              (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), telegram_id))
    conn.commit()
    conn.close()

def weighted_choice(items):
    total_weight = sum(item.get("weight", 1) for item in items)
    rand = random.uniform(0, total_weight)
    for item in items:
        rand -= item.get("weight", 1)
        if rand <= 0:
            return item
    return items[-1]

def fortune_spin():
    emojis = list(FORTUNE_WEIGHTS.keys())
    weights = list(FORTUNE_WEIGHTS.values())
    return random.choices(emojis, weights=weights, k=1)[0]

def get_random_skin():
    skins = [
        "TEC-9 Tie Dye", "UMP45 Shark", "M110 Transition", 
        "Sticker Fingerprint", "Charm Hoplit Helmet", "M4A1 Stainless",
        "Desert Eagle Eclipse", "Akimbo Uzi Zenith", "Sticker Minotaur"
    ]
    price = random.randint(1, 50)
    return random.choice(skins), price

def get_animation_frames():
    emojis = ["🔥", "🤑", "🎰", "😬", "🎁", "💣"]
    frames = []
    for i in range(6):
        frame = emojis[i:] + emojis[:i]
        frames.append(" ".join(frame))
    return frames

# ==================== КЛАВИАТУРЫ ====================
def main_menu(user_id=None):
    buttons = [
        [InlineKeyboardButton("📦 Открыть кейс", callback_data="open_case")],
        [InlineKeyboardButton("👤 Профиль", callback_data="profile")],
        [InlineKeyboardButton("💰 Пополнить баланс", callback_data="deposit_menu")],
        [InlineKeyboardButton("🎁 Бесплатный бонус (+20 G)", callback_data="bonus")],
        [InlineKeyboardButton("💣 Мини-игра: Мины", callback_data="mines_menu")],
        [InlineKeyboardButton("🎰 Мини-игра: Колесо Фортуны", callback_data="fortune_menu")],
        [InlineKeyboardButton("📜 История", callback_data="history")]
    ]
    if user_id == DEVELOPER_ID:
        buttons.append([InlineKeyboardButton("👑 Пополнить игрока", callback_data="dev_add_balance")])
        buttons.append([InlineKeyboardButton("💰 +10000 G (DEV)", callback_data="add_dev_10000")])
    return InlineKeyboardMarkup(buttons)

def case_buttons():
    buttons = []
    for key, case in CASES.items():
        buttons.append([InlineKeyboardButton(f"📦 {case['name']} ({case['cost']} G)", callback_data=f"case_{key}")])
    buttons.append([InlineKeyboardButton("🔙 Назад", callback_data="back")])
    return InlineKeyboardMarkup(buttons)

def back_button():
    return InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Назад", callback_data="back")]])

def profile_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📦 Инвентарь", callback_data="inventory")],
        [InlineKeyboardButton("💰 Продать скин", callback_data="sell_menu")],
        [InlineKeyboardButton("💎 Вывод скина", callback_data="withdraw_menu")],
        [InlineKeyboardButton("🛠 Тех. Поддержка", callback_data="support")],
        [InlineKeyboardButton("🔙 Назад", callback_data="back")]
    ])

def deposit_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("50 G", callback_data="deposit_50"),
         InlineKeyboardButton("100 G", callback_data="deposit_100")],
        [InlineKeyboardButton("150 G", callback_data="deposit_150"),
         InlineKeyboardButton("200 G", callback_data="deposit_200")],
        [InlineKeyboardButton("🔙 Назад", callback_data="back")]
    ])

def deposit_confirm_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Да", callback_data="deposit_yes")],
        [InlineKeyboardButton("❌ Нет", callback_data="deposit_no")],
        [InlineKeyboardButton("⌛ В процессе", callback_data="deposit_wait")]
    ])

def twenty_boxes(case_key):
    buttons = []
    row = []
    for i in range(1, 21):
        row.append(InlineKeyboardButton("📦", callback_data=f"box_{case_key}_{i}"))
        if len(row) == 5:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    buttons.append([InlineKeyboardButton("🔙 Назад", callback_data="back")])
    return InlineKeyboardMarkup(buttons)

def confirm_buttons(case_key, box_num):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Открыть!", callback_data=f"confirm_{case_key}_{box_num}")],
        [InlineKeyboardButton("🔄 Поменять выбор", callback_data=f"change_{case_key}")],
        [InlineKeyboardButton("🔙 Назад", callback_data="back")]
    ])

def inventory_buttons(telegram_id, action):
    inventory = get_inventory(telegram_id)
    if not inventory:
        return None
    buttons = []
    for item_id, item_name, price, rarity, item_type in inventory[:20]:
        color = RARITY_COLORS.get(rarity, "⬜")
        buttons.append([InlineKeyboardButton(f"{color} {item_name} ({price} G)", callback_data=f"{action}_{item_id}")])
    buttons.append([InlineKeyboardButton("🔙 Назад", callback_data="profile")])
    return InlineKeyboardMarkup(buttons)

def after_open_buttons(item_id, price):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(f"💰 Продать за {price} G", callback_data=f"quick_sell_{item_id}")],
        [InlineKeyboardButton("📦 Оставить", callback_data=f"keep_{item_id}")],
        [InlineKeyboardButton("🔙 В меню", callback_data="back")]
    ])

def mines_game_buttons(mines, opened, total_cells=20):
    buttons = []
    row = []
    for i in range(total_cells):
        if i in opened:
            row.append(InlineKeyboardButton("✅", callback_data=f"mines_cell_{i}"))
        else:
            row.append(InlineKeyboardButton("🎁", callback_data=f"mines_cell_{i}"))
        if len(row) == 5:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    buttons.append([InlineKeyboardButton("💰 Забрать выигрыш", callback_data="mines_cashout")])
    buttons.append([InlineKeyboardButton("🔙 Выход", callback_data="back")])
    return InlineKeyboardMarkup(buttons)

def fortune_spin_button():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎰 Крутить!", callback_data="fortune_spin")],
        [InlineKeyboardButton("🔙 Назад", callback_data="back")]
    ])

# ==================== ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ ====================
mines_data = {}
fortune_data = {}
case_cache = {}
selected_box_cache = {}
waiting_for_bet = {}
deposit_timer = {}
dev_add_data = {}

async def schedule_deposit_check(user_id, chat_id, context):
    await asyncio.sleep(60)
    if user_id not in deposit_timer:
        return
    try:
        await context.bot.send_message(
            chat_id=chat_id,
            text="Вы купили скин?💰",
            reply_markup=deposit_confirm_buttons()
        )
    except:
        pass
    if user_id in deposit_timer:
        del deposit_timer[user_id]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.username
    register_user(user_id, username)
    await update.message.reply_text(
        f"🔥 Добро пожаловать в открытие кейсов «ВЕЗУНЧИК»!\n\n"
        f"Испытай удачу и выбей топовый скин! 🍀\n\n"
        f"💰 Твой баланс: {get_balance(user_id)} G\n\n"
        f"Выбирай действие:",
        reply_markup=main_menu(user_id)
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    data = query.data

    if data.startswith("mines_mines_") or data.startswith("mines_cell_") or data == "mines_cashout":
        if data.startswith("mines_mines_"):
            await mines_mines_handler(update, context)
            return
        elif data.startswith("mines_cell_"):
            await mines_cell_handler(update, context)
            return
        elif data == "mines_cashout":
            await mines_cashout_handler(update, context)
            return

    if data == "back":
        if user_id in deposit_timer:
            del deposit_timer[user_id]
        if user_id in dev_add_data:
            del dev_add_data[user_id]
        await query.edit_message_text("🔙 Главное меню", reply_markup=main_menu(user_id))
        return

    if data == "open_case":
        await query.edit_message_text("🎯 Выбери кейс:", reply_markup=case_buttons())
        return

    if data == "profile":
        balance = get_balance(user_id)
        most_expensive = get_most_expensive_item(user_id)
        inventory_count = len(get_all_inventory(user_id))
        text = f"👤 **Профиль**\n\n"
        text += f"💰 Баланс: {balance} G\n"
        if most_expensive:
            color = RARITY_COLORS.get(most_expensive[2], "⬜")
            text += f"🏆 Самый дорогой скин: {color} {most_expensive[0]} ({most_expensive[1]} G)\n"
        else:
            text += f"🏆 Самый дорогой скин: нет\n"
        text += f"📦 Всего предметов: {inventory_count}\n"
        await query.edit_message_text(text, reply_markup=profile_menu(), parse_mode="Markdown")
        return

    if data == "history":
        history = get_history(user_id, 20)
        if not history:
            text = "📭 Ты еще не открывал кейсы."
        else:
            text = "📜 **Твоя история открытий:**\n\n"
            for case, item, date in history:
                text += f"📅 {date}\n📦 {case} → {item}\n\n"
        await query.edit_message_text(text, reply_markup=back_button(), parse_mode="Markdown")
        return

    if data == "add_dev_10000":
        if user_id != DEVELOPER_ID:
            await query.answer("⛔ Только для разработчика!", show_alert=True)
            return
        update_balance(user_id, 10000)
        new_balance = get_balance(user_id)
        await query.edit_message_text(
            f"✅ Пополнено на 10000 G!\n\n"
            f"💰 Новый баланс: {new_balance} G",
            reply_markup=main_menu(user_id)
        )
        return

    if data == "support":
        await query.edit_message_text(
            "🛠 **Тех. Поддержка**\n\n"
            "Напишите ваш вопрос или проблему сюда.\n"
            "ОБЯЗАТЕЛЬНО ОСТАВЬТЕ СВОЙ ЮЗЕРНЕЙМ!!!\n\n"
            "Администрация с вами свяжется.",
            reply_markup=back_button(),
            parse_mode="Markdown"
        )
        return

    if data == "bonus":
        last_bonus = get_last_bonus(user_id)
        now = datetime.now()
        diff = now - last_bonus
        if diff < timedelta(days=3):
            remaining = timedelta(days=3) - diff
            hours = remaining.seconds // 3600
            minutes = (remaining.seconds % 3600) // 60
            await query.edit_message_text(
                f"⏳ **Бонус уже получен!**\n\n"
                f"Следующий бонус будет доступен через:\n"
                f"**{hours} ч {minutes} мин**\n\n"
                f"🎁 Бонус даёт +20 G каждые 3 дня!",
                reply_markup=back_button(),
                parse_mode="Markdown"
            )
            return
        update_balance(user_id, 20)
        update_last_bonus(user_id)
        new_balance = get_balance(user_id)
        await query.edit_message_text(
            f"🎁 **Бонус получен!**\n\n"
            f"💰 Начислено: **+20 G**\n"
            f"💳 Новый баланс: **{new_balance} G**\n\n"
            f"Следующий бонус будет доступен через 3 дня!",
            reply_markup=back_button(),
            parse_mode="Markdown"
        )
        return

    if data == "deposit_menu":
        await query.edit_message_text(
            f"💰 **Пополнение баланса**\n\n"
            f"Выберите сумму пополнения:\n\n"
            f"К сожалению пополнение через бота доступно только Голдой! Комиссию мы берём на себя♥️",
            reply_markup=deposit_buttons(),
            parse_mode="Markdown"
        )
        return

    if data == "deposit_yes":
        amount = deposit_timer.get(user_id, {}).get('amount', 'неизвестно')
        try:
            user = await context.bot.get_chat(user_id)
            username = user.username if user.username else f"ID{user_id}"
        except:
            username = f"ID{user_id}"
        try:
            await context.bot.send_message(
                chat_id=DEVELOPER_ID,
                text=f"💳 **ПОПОЛНЕНИЕ БАЛАНСА**\n\n"
                     f"👤 Игрок: @{username}\n"
                     f"💰 Сумма: {amount} G\n"
                     f"✅ Статус: **Подтверждено**",
                parse_mode="Markdown"
            )
        except:
            pass
        if user_id in deposit_timer:
            del deposit_timer[user_id]
        await query.edit_message_text(
            f"🤑 **Ожидайте!**\n\n"
            f"Бот проверит покупку и голда скоро поступит на баланс!",
            reply_markup=main_menu(user_id),
            parse_mode="Markdown"
        )
        return

    if data == "deposit_no":
        if user_id in deposit_timer:
            del deposit_timer[user_id]
        await query.edit_message_text(
            f"🔙 **Отмена**\n\n"
            f"Возвращаемся в главное меню.",
            reply_markup=main_menu(user_id),
            parse_mode="Markdown"
        )
        return

    if data == "deposit_wait":
        await query.answer("⏳ Ожидаем, после покупки нажмите кнопку «Да✅»", show_alert=True)
        return

    if data.startswith("deposit_"):
        try:
            amount = int(data.split("_")[1])
        except:
            await query.answer("❌ Ошибка!", show_alert=True)
            return
        deposit_info = DEPOSIT_DATA.get(amount)
        if not deposit_info:
            await query.answer("❌ Ошибка!", show_alert=True)
            return
        price = deposit_info["price"]
        pattern = deposit_info["pattern"]
        deposit_timer[user_id] = {
            "amount": amount,
            "chat_id": query.message.chat_id
        }
        await query.edit_message_text(
            f"💎 **Отлично!**\n\n"
            f"На рынке выставлен скин: **USP \"Corrode\"**\n"
            f"за **{price} G** (Паттерн {pattern})\n\n"
            f"Купи этот скин в игре, а затем подтверди покупку.\n"
            f"У тебя есть 1 минута!",
            reply_markup=back_button(),
            parse_mode="Markdown"
        )
        context.application.create_task(
            schedule_deposit_check(user_id, query.message.chat_id, context)
        )
        return

    if data == "dev_add_balance":
        if user_id != DEVELOPER_ID:
            await query.answer("⛔ Только для разработчика!", show_alert=True)
            return
        dev_add_data[user_id] = {"step": "username"}
        await query.edit_message_text(
            f"👑 **Пополнение баланса игрока**\n\n"
            f"Введите **@username** игрока (например, @void4mo):",
            reply_markup=back_button(),
            parse_mode="Markdown"
        )
        return

    if data == "mines_menu":
        await query.edit_message_text(
            "💣 **Мини-игра: Мины**\n\n"
            "💰 Введите сумму ставки (число):",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Назад", callback_data="back")]
            ]),
            parse_mode="Markdown"
        )
        waiting_for_bet[user_id] = "mines"
        return

    if data == "fortune_menu":
        rules = "🎰 **Колесо Фортуны**\n\n"
        rules += "Выпадает один из эмодзи:\n\n"
        for emoji, info in FORTUNE_EMOJIS.items():
            rules += f"{emoji} — **{info['name']}** — {info['desc']}\n"
        rules += "\n\n💰 Введите сумму ставки (число):"
        await query.edit_message_text(
            rules,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Назад", callback_data="back")]
            ]),
            parse_mode="Markdown"
        )
        waiting_for_bet[user_id] = "fortune"
        return

    if data == "fortune_spin":
        if user_id not in fortune_data:
            await query.edit_message_text("❌ Ошибка. Начни заново.", reply_markup=main_menu(user_id))
            return
        game = fortune_data[user_id]
        bet = game["bet"]
        frames = get_animation_frames()
        msg = await query.edit_message_text(
            f"🎰 **Крутим барабан...**\n\n"
            f"{frames[0]}",
            parse_mode="Markdown"
        )
        for frame in frames[1:]:
            await msg.edit_text(
                f"🎰 **Крутим барабан...**\n\n"
                f"{frame}",
                parse_mode="Markdown"
            )
            time.sleep(0.3)
        result = fortune_spin()
        game["result"] = result
        game["spun"] = True
        multiplier = FORTUNE_EMOJIS[result]["multiplier"]
        if multiplier == "skin":
            skin_name, skin_price = get_random_skin()
            add_item(user_id, skin_name, skin_price, "Обычный", "Оружие", "Колесо Фортуны")
            await msg.edit_text(
                f"🎰 **Результат: {result}**\n\n"
                f"{result} — {FORTUNE_EMOJIS[result]['name']}\n"
                f"📦 Ты получил скин: **{skin_name}** ({skin_price} G)!\n\n"
                f"💳 Баланс: {get_balance(user_id)} G",
                reply_markup=main_menu(user_id),
                parse_mode="Markdown"
            )
            del fortune_data[user_id]
            return
        if multiplier == 0:
            await msg.edit_text(
                f"🎰 **Результат: {result}**\n\n"
                f"{result} — {FORTUNE_EMOJIS[result]['name']}\n"
                f"💸 Ставка {bet} G сгорела!\n\n"
                f"💳 Баланс: {get_balance(user_id)} G",
                reply_markup=main_menu(user_id),
                parse_mode="Markdown"
            )
            del fortune_data[user_id]
            return
        if multiplier == 0.2:
            refund = int(bet * 0.2)
            update_balance(user_id, refund)
            await msg.edit_text(
                f"🎰 **Результат: {result}**\n\n"
                f"{result} — {FORTUNE_EMOJIS[result]['name']}\n"
                f"🔥 Ставка {bet} G сгорела!\n"
                f"💵 Возвращено 20%: {refund} G\n\n"
                f"💳 Баланс: {get_balance(user_id)} G",
                reply_markup=main_menu(user_id),
                parse_mode="Markdown"
            )
            del fortune_data[user_id]
            return
        win = int(bet * multiplier)
        update_balance(user_id, win)
        if multiplier == 1:
            await msg.edit_text(
                f"🎰 **Результат: {result}**\n\n"
                f"{result} — {FORTUNE_EMOJIS[result]['name']}\n"
                f"💵 Ставка возвращена: {win} G\n\n"
                f"💳 Баланс: {get_balance(user_id)} G",
                reply_markup=main_menu(user_id),
                parse_mode="Markdown"
            )
        else:
            await msg.edit_text(
                f"🎰 **Результат: {result}**\n\n"
                f"{result} — {FORTUNE_EMOJIS[result]['name']}\n"
                f"💰 Выигрыш: {win} G\n"
                f"⚡ Множитель: x{multiplier}\n\n"
                f"💳 Баланс: {get_balance(user_id)} G",
                reply_markup=main_menu(user_id),
                parse_mode="Markdown"
            )
        del fortune_data[user_id]
        return

    if data == "inventory":
        keyboard = inventory_buttons(user_id, "view")
        if not keyboard:
            await query.edit_message_text("📭 Инвентарь пуст. Открой кейс!", reply_markup=back_button())
            return
        await query.edit_message_text("📦 **Твой инвентарь:**", reply_markup=keyboard, parse_mode="Markdown")
        return

    if data.startswith("view_"):
        item_id = int(data.split("_")[1])
        conn = sqlite3.connect("cases_bot.db")
        c = conn.cursor()
        c.execute("SELECT item_name, item_price, item_rarity, item_type FROM inventory WHERE id = ? AND telegram_id = ? AND sold = 0", 
                  (item_id, user_id))
        result = c.fetchone()
        conn.close()
        if result:
            name, price, rarity, item_type = result
            color = RARITY_COLORS.get(rarity, "⬜")
            await query.edit_message_text(
                f"📌 **Информация о скине**\n\n"
                f"🔫 Название: {name}\n"
                f"{color} Редкость: {rarity}\n"
                f"📋 Тип: {item_type}\n"
                f"💰 Цена: {price} G",
                reply_markup=back_button(),
                parse_mode="Markdown"
            )
        else:
            await query.edit_message_text("❌ Скин не найден.", reply_markup=back_button())
        return

    if data == "sell_menu":
        keyboard = inventory_buttons(user_id, "sell")
        if not keyboard:
            await query.edit_message_text("❌ У тебя нет предметов для продажи.", reply_markup=back_button())
            return
        await query.edit_message_text("💰 **Выбери скин для продажи:**", reply_markup=keyboard, parse_mode="Markdown")
        return

    if data.startswith("sell_"):
        item_id = int(data.split("_")[1])
        price = sell_item(item_id, user_id)
        if price:
            new_balance = get_balance(user_id)
            await query.edit_message_text(
                f"✅ Скин продан за {price} G!\n\n"
                f"💰 Новый баланс: {new_balance} G",
                reply_markup=profile_menu()
            )
        else:
            await query.edit_message_text("❌ Ошибка: предмет не найден или уже продан.", reply_markup=profile_menu())
        return

    if data == "withdraw_menu":
        keyboard = inventory_buttons(user_id, "withdraw")
        if not keyboard:
            await query.edit_message_text("❌ У тебя нет предметов для вывода.", reply_markup=back_button())
            return
        await query.edit_message_text(
            "💎 **Выбери скин для вывода:**\n\n"
            "После выбора ты получишь цену для выставления на рынок.",
            reply_markup=keyboard,
            parse_mode="Markdown"
        )
        return

    if data.startswith("withdraw_"):
        item_id = int(data.split("_")[1])
        conn = sqlite3.connect("cases_bot.db")
        c = conn.cursor()
        c.execute("SELECT item_name, item_price FROM inventory WHERE id = ? AND telegram_id = ? AND sold = 0", 
                  (item_id, user_id))
        result = c.fetchone()
        conn.close()
        if result:
            price = result[1]
            base_price = price * 1.2
            random_cents = random.randint(1, 99) / 100
            final_price = base_price + random_cents
            final_price = round(final_price, 2)
            await query.edit_message_text(
                f"💎 **Отлично!**\n\n"
                f"Выставляй скин **G22 \"Adam\"** за **{final_price} G** и ожидай!\n\n"
                f"🔄 Администрация/бот скоро купит твой скин!",
                reply_markup=profile_menu(),
                parse_mode="Markdown"
            )
        else:
            await query.edit_message_text("❌ Ошибка: предмет не найден.", reply_markup=profile_menu())
        return

    if data.startswith("quick_sell_"):
        item_id = int(data.split("_")[2])
        price = sell_item(item_id, user_id)
        if price:
            new_balance = get_balance(user_id)
            await query.edit_message_text(
                f"💰 **Скин продан за {price} G!**\n\n"
                f"💳 Новый баланс: {new_balance} G",
                reply_markup=main_menu(user_id),
                parse_mode="Markdown"
            )
        else:
            await query.edit_message_text("❌ Ошибка при продаже.", reply_markup=main_menu(user_id))
        return

    if data.startswith("keep_"):
        await query.edit_message_text(
            f"📦 **Скин сохранён в инвентаре!**\n\n"
            f"Ты можешь продать его позже через профиль.",
            reply_markup=main_menu(user_id),
            parse_mode="Markdown"
        )
        return

    if data.startswith("case_"):
        case_key = data.split("_")[1]
        case = CASES.get(case_key)
        if not case:
            await query.edit_message_text("❌ Кейс не найден", reply_markup=main_menu(user_id))
            return
        items_text = "📋 **Возможные скины:**\n\n"
        for item in case["items"]:
            items_text += f"🔥 {item['name']} — {item['price']} G\n"
        await query.edit_message_text(
            f"🎯 **{case['name']}**\n"
            f"💰 Стоимость: {case['cost']} G\n\n"
            f"{items_text}\n\n"
            f"Нажми на кнопку ниже, чтобы открыть:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🎰 Открыть кейс", callback_data=f"open_{case_key}")],
                [InlineKeyboardButton("🔙 Назад", callback_data="back")]
            ]),
            parse_mode="Markdown"
        )
        return

    if data.startswith("open_"):
        case_key = data.split("_")[1]
        case = CASES.get(case_key)
        if not case:
            await query.edit_message_text("❌ Кейс не найден", reply_markup=main_menu(user_id))
            return
        balance = get_balance(user_id)
        if balance < case["cost"]:
            await query.answer(f"❌ Не хватает G! Нужно {case['cost']}, у тебя {balance}", show_alert=True)
            return
        case_cache[user_id] = case_key
        selected_box_cache[user_id] = None
        await query.edit_message_text(
            f"🎰 **{case['name']} открывается...**\n"
            f"💰 Стоимость: {case['cost']} G\n\n"
            f"Выбери одну из 20 коробок:",
            reply_markup=twenty_boxes(case_key),
            parse_mode="Markdown"
        )
        return

    if data.startswith("box_"):
        parts = data.split("_")
        case_key = parts[1]
        box_num = int(parts[2])
        case = CASES.get(case_key)
        if not case:
            await query.edit_message_text("❌ Ошибка: кейс не найден", reply_markup=main_menu(user_id))
            return
        selected_box_cache[user_id] = box_num
        await query.edit_message_text(
            f"📦 **Вы выбрали коробку №{box_num}**\n\n"
            f"Уверены, что хотите её открыть?",
            reply_markup=confirm_buttons(case_key, box_num),
            parse_mode="Markdown"
        )
        return

    if data.startswith("confirm_"):
        parts = data.split("_")
        case_key = parts[1]
        box_num = int(parts[2])
        case = CASES.get(case_key)
        if not case:
            await query.edit_message_text("❌ Ошибка: кейс не найден", reply_markup=main_menu(user_id))
            return
        balance = get_balance(user_id)
        if balance < case["cost"]:
            await query.answer(f"❌ Не хватает G! Нужно {case['cost']}, у тебя {balance}", show_alert=True)
            return
        deduct_balance(user_id, case["cost"])
        item_data = weighted_choice(case["items"])
        item_name = item_data["name"]
        item_price = item_data["price"]
        item_rarity = item_data["rarity"]
        item_type = item_data["type"]
        color = RARITY_COLORS.get(item_rarity, "⬜")
        item_id = add_item(user_id, item_name, item_price, item_rarity, item_type, case["name"])
        new_balance = get_balance(user_id)
        await query.edit_message_text(
            f"🎉 **Ты открыл коробку №{box_num}!**\n\n"
            f"📌 Тип скина: **{item_type}**\n"
            f"{color} Редкость: **{item_rarity}**\n"
            f"🔫 Название: **{item_name}**\n"
            f"💰 Цена: **{item_price} G**\n\n"
            f"💳 Баланс: {new_balance} G\n\n"
            f"Что сделать со скином?",
            reply_markup=after_open_buttons(item_id, item_price),
            parse_mode="Markdown"
        )
        return

    if data.startswith("change_"):
        case_key = data.split("_")[1]
        case = CASES.get(case_key)
        if not case:
            await query.edit_message_text("❌ Ошибка: кейс не найден", reply_markup=main_menu(user_id))
            return
        selected_box_cache[user_id] = None
        await query.edit_message_text(
            f"🔄 **Выбери другую коробку:**",
            reply_markup=twenty_boxes(case_key),
            parse_mode="Markdown"
        )
        return

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()
    
    if user_id in dev_add_data:
        if dev_add_data[user_id]["step"] == "username":
            username = text.strip()
            if username.startswith("@"):
                username = username[1:]
            dev_add_data[user_id]["target_username"] = username
            dev_add_data[user_id]["step"] = "amount"
            await update.message.reply_text(
                f"👑 **Пополнение баланса**\n\n"
                f"Игрок: @{username}\n"
                f"Введите **сумму** для пополнения (число):",
                parse_mode="Markdown"
            )
            return
        elif dev_add_data[user_id]["step"] == "amount":
            try:
                amount = int(text.strip())
                if amount <= 0:
                    await update.message.reply_text("❌ Сумма должна быть положительной!")
                    return
                username = dev_add_data[user_id]["target_username"]
                target_id = get_user_by_username(username)
                if not target_id:
                    await update.message.reply_text(
                        f"❌ Игрок @{username} не найден в базе данных!\n"
                        f"Возможно, он ещё не запускал бота.",
                        parse_mode="Markdown"
                    )
                    del dev_add_data[user_id]
                    return
                update_balance(target_id, amount)
                new_balance = get_balance(target_id)
                await update.message.reply_text(
                    f"✅ **Баланс пополнен!**\n\n"
                    f"👤 Игрок: @{username}\n"
                    f"💰 Начислено: {amount} G\n"
                    f"💳 Новый баланс: {new_balance} G",
                    parse_mode="Markdown"
                )
                try:
                    await context.bot.send_message(
                        chat_id=target_id,
                        text=f"🎉 **Ваш баланс пополнен!**\n\n"
                             f"💰 Начислено: {amount} G\n"
                             f"💳 Новый баланс: {new_balance} G\n\n"
                             f"Удачи в игре! 🍀",
                        parse_mode="Markdown"
                    )
                except:
                    pass
                del dev_add_data[user_id]
                return
            except ValueError:
                await update.message.reply_text("❌ Введите число!")
                return
    
    if user_id not in waiting_for_bet:
        return
    
    game_type = waiting_for_bet[user_id]
    try:
        bet = int(text)
        if bet <= 0:
            await update.message.reply_text("❌ Ставка должна быть положительным числом!")
            return
        balance = get_balance(user_id)
        if bet > balance:
            await update.message.reply_text(f"❌ Не хватает G! Нужно {bet}, у тебя {balance}")
            return
        deduct_balance(user_id, bet)
        if game_type == "mines":
            await update.message.reply_text(
                f"💣 **Мины**\n\n"
                f"💰 Ставка: {bet} G\n"
                f"⚡ Множитель: x1.00\n\n"
                f"Выбери количество мин на поле:",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("2 💣", callback_data="mines_mines_2"),
                     InlineKeyboardButton("4 💣", callback_data="mines_mines_4")],
                    [InlineKeyboardButton("6 💣", callback_data="mines_mines_6"),
                     InlineKeyboardButton("12 💣", callback_data="mines_mines_12")],
                    [InlineKeyboardButton("19 💣", callback_data="mines_mines_19")],
                    [InlineKeyboardButton("🔙 Назад", callback_data="back")]
                ]),
                parse_mode="Markdown"
            )
            mines_data[user_id] = {
                "bet": bet,
                "multiplier": 1.0,
                "opened": [],
                "mines": [],
                "game_over": False
            }
            del waiting_for_bet[user_id]
            return
        elif game_type == "fortune":
            fortune_data[user_id] = {
                "bet": bet,
                "spun": False
            }
            del waiting_for_bet[user_id]
            await update.message.reply_text(
                f"🎰 **Колесо Фортуны**\n\n"
                f"💰 Ставка: {bet} G\n\n"
                f"Нажми на кнопку, чтобы крутить!",
                reply_markup=fortune_spin_button(),
                parse_mode="Markdown"
            )
            return
    except ValueError:
        await update.message.reply_text("❌ Введите число!")

async def mines_mines_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    data = query.data
    if not data.startswith("mines_mines_"):
        return
    mines_count = int(data.split("_")[2])
    if user_id not in mines_data:
        await query.edit_message_text("❌ Ошибка. Начни заново.", reply_markup=main_menu(user_id))
        return
    positions = list(range(20))
    mine_positions = random.sample(positions, mines_count)
    mines_data[user_id]["mines"] = mine_positions
    mines_data[user_id]["mines_count"] = mines_count
    await query.edit_message_text(
        f"💣 **Мины**\n\n"
        f"💰 Ставка: {mines_data[user_id]['bet']} G\n"
        f"💣 Мин на поле: {mines_count}\n"
        f"⚡ Множитель: x1.00\n\n"
        f"Открывай клетки 🎁 и не попади на мину!",
        reply_markup=mines_game_buttons(mines_count, []),
        parse_mode="Markdown"
    )

async def mines_cell_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    data = query.data
    if not data.startswith("mines_cell_"):
        return
    cell = int(data.split("_")[2])
    if user_id not in mines_data:
        await query.edit_message_text("❌ Ошибка. Начни заново.", reply_markup=main_menu(user_id))
        return
    game = mines_data[user_id]
    if game["game_over"]:
        await query.answer("Игра уже окончена!", show_alert=True)
        return
    if cell in game["opened"]:
        await query.answer("Эта клетка уже открыта!", show_alert=True)
        return
    game["opened"].append(cell)
    if cell in game["mines"]:
        game["game_over"] = True
        all_cells = list(range(20))
        buttons = []
        row = []
        for i in all_cells:
            if i in game["mines"]:
                row.append(InlineKeyboardButton("💥", callback_data=f"mines_dead_{i}"))
            elif i in game["opened"]:
                row.append(InlineKeyboardButton("✅", callback_data=f"mines_dead_{i}"))
            else:
                row.append(InlineKeyboardButton("🎁", callback_data=f"mines_dead_{i}"))
            if len(row) == 5:
                buttons.append(row)
                row = []
        if row:
            buttons.append(row)
        buttons.append([InlineKeyboardButton("🔙 Выход", callback_data="back")])
        await query.edit_message_text(
            f"💥 **ВЗРЫВ!**\n\n"
            f"Ты наступил на мину!\n"
            f"💰 Ставка: {game['bet']} G\n"
            f"💸 Потеряно: {game['bet']} G\n\n"
            f"Попробуй снова! 🍀",
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode="Markdown"
        )
        return
    mines_count = game["mines_count"]
    multiplier = MINE_MULTIPLIERS.get(mines_count, 1.0)
    game["multiplier"] *= multiplier
    current_win = round(game["bet"] * game["multiplier"], 2)
    await query.edit_message_text(
        f"💣 **Мины**\n\n"
        f"💰 Ставка: {game['bet']} G\n"
        f"💣 Мин на поле: {mines_count}\n"
        f"⚡ Множитель: x{round(game['multiplier'], 2)}\n"
        f"🏆 Текущий выигрыш: {current_win} G\n\n"
        f"Открывай клетки 🎁 или забирай выигрыш!",
        reply_markup=mines_game_buttons(mines_count, game["opened"]),
        parse_mode="Markdown"
    )

async def mines_cashout_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    if user_id not in mines_data:
        await query.edit_message_text("❌ Ошибка. Начни заново.", reply_markup=main_menu(user_id))
        return
    game = mines_data[user_id]
    if game["game_over"]:
        await query.answer("Игра уже окончена!", show_alert=True)
        return
    if len(game["opened"]) == 0:
        await query.answer("Открой хотя бы одну клетку!", show_alert=True)
        return
    win = round(game["bet"] * game["multiplier"], 2)
    update_balance(user_id, win)
    new_balance = get_balance(user_id)
    del mines_data[user_id]
    await query.edit_message_text(
        f"💰 **Вы забрали выигрыш!**\n\n"
        f"🏆 Выигрыш: {win} G\n"
        f"💳 Новый баланс: {new_balance} G\n\n"
        f"Сыграем ещё?",
        reply_markup=main_menu(user_id),
        parse_mode="Markdown"
    )

async def add_balance_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != DEVELOPER_ID:
        await update.message.reply_text("⛔ У вас нет прав на эту команду.")
        return
    try:
        amount = int(context.args[0])
        if amount <= 0:
            await update.message.reply_text("❌ Сумма должна быть положительной.")
            return
        update_balance(user_id, amount)
        new_balance = get_balance(user_id)
        await update.message.reply_text(
            f"✅ Баланс пополнен на {amount} G.\n\n"
            f"💰 Текущий баланс: {new_balance} G"
        )
    except (IndexError, ValueError):
        await update.message.reply_text("❌ Использование: /add_balance <сумма>")

def main():
    init_db()
    print("🚀 Бот запущен...")
    print(f"👤 ID разработчика: {DEVELOPER_ID}")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add_balance", add_balance_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    print("✅ Бот готов к работе!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
