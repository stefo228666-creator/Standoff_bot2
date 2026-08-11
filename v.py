import sqlite3
import random
import time
import asyncio
import shutil
import os
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

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

MINE_MULTIPLIERS = {
    2: 1.1,
    4: 1.2,
    6: 1.4,
    12: 2.0,
    19: 5.0
}

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

DEPOSIT_DATA = {
    50: {"price": 54.38, "pattern": 264},
    100: {"price": 101.69, "pattern": 890},
    150: {"price": 156.25, "pattern": 287},
    200: {"price": 203.93, "pattern": 821}
}

PROMOCODES = {
    "HALYAVA2026": {"type": "balance", "value": 100},
    "SECRETCODE": {"type": "random_balance", "min": 10, "max": 50},
    "RANDOMGUN": {"type": "random_skin", "min": 10, "max": 20},
    "BONUS": {"type": "skin_fixed", "value": 5},
    "THEBESTCODE2026": {"type": "multiple_skins", "count": 3, "value": 20}
}

ACHIEVEMENTS = {
    "first_case": {"name": "🎯 Первый кейс", "desc": "Открыть 1 кейс", "reward": 10, "type": "balance"},
    "cases_10": {"name": "📦 10 кейсов", "desc": "Открыть 10 кейсов", "reward": 50, "type": "balance"},
    "cases_50": {"name": "📦 50 кейсов", "desc": "Открыть 50 кейсов", "reward": 100, "type": "balance"},
    "cases_100": {"name": "📦 100 кейсов", "desc": "Открыть 100 кейсов", "reward": 250, "type": "balance"},
    "spend_3000": {"name": "💸 Транжира", "desc": "Потратить 3000 G на кейсы", "reward": "secret_case", "type": "secret_case"},
    "mines_win_10": {"name": "💣 Победитель мин", "desc": "Выиграть в минах 10 раз", "reward": 50, "type": "balance"},
    "fortune_win_5": {"name": "🎰 Удачник", "desc": "Выиграть в фортуне 5 раз", "reward": 50, "type": "balance"},
    "referral_1": {"name": "👥 Первый друг", "desc": "Привести 1 друга", "reward": 20, "type": "balance"},
    "referral_5": {"name": "👥 Пятеро друзей", "desc": "Привести 5 друзей", "reward": 100, "type": "balance"},
}

# ==================== БАЗА ДАННЫХ ====================
def init_db():
    conn = sqlite3.connect("cases_bot.db", timeout=10)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (telegram_id INTEGER PRIMARY KEY, balance INTEGER DEFAULT 0, reg_date TEXT, last_bonus TIMESTAMP DEFAULT "1970-01-01 00:00:00", username TEXT, referrer_id INTEGER DEFAULT 0, last_promo TIMESTAMP DEFAULT "1970-01-01 00:00:00", total_spent INTEGER DEFAULT 0, cases_opened INTEGER DEFAULT 0, mines_wins INTEGER DEFAULT 0, fortune_wins INTEGER DEFAULT 0, vip_until TIMESTAMP DEFAULT "1970-01-01 00:00:00")''')
    c.execute('''CREATE TABLE IF NOT EXISTS inventory
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, telegram_id INTEGER, item_name TEXT, item_price REAL, item_rarity TEXT, item_type TEXT, case_name TEXT, open_date TEXT, sold INTEGER DEFAULT 0)''')
    c.execute('''CREATE TABLE IF NOT EXISTS referrals
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, referrer_id INTEGER, referral_id INTEGER, date TEXT, bonus_claimed INTEGER DEFAULT 0)''')
    c.execute('''CREATE TABLE IF NOT EXISTS logs
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, telegram_id INTEGER, action TEXT, amount REAL, details TEXT, date TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS achievements
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, telegram_id INTEGER, achievement_id TEXT, claimed INTEGER DEFAULT 0)''')
    c.execute('''CREATE TABLE IF NOT EXISTS promocodes
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, code TEXT UNIQUE, type TEXT, value INTEGER, min INTEGER, max INTEGER, count INTEGER, created_by INTEGER, created_date TEXT)''')
    conn.commit()
    conn.close()

def register_user(telegram_id, username=None, referrer_id=0):
    conn = sqlite3.connect("cases_bot.db", timeout=10)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (telegram_id, reg_date, last_bonus, username, referrer_id, last_promo) VALUES (?, ?, ?, ?, ?, ?)", 
              (telegram_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "1970-01-01 00:00:00", username, referrer_id, "1970-01-01 00:00:00"))
    if username:
        c.execute("UPDATE users SET username = ? WHERE telegram_id = ?", (username, telegram_id))
    conn.commit()
    conn.close()

def get_user_by_username(username):
    conn = sqlite3.connect("cases_bot.db", timeout=10)
    c = conn.cursor()
    c.execute("SELECT telegram_id FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def get_balance(telegram_id):
    conn = sqlite3.connect("cases_bot.db", timeout=10)
    c = conn.cursor()
    c.execute("SELECT balance FROM users WHERE telegram_id = ?", (telegram_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else 0

def update_balance(telegram_id, amount):
    conn = sqlite3.connect("cases_bot.db", timeout=10)
    c = conn.cursor()
    c.execute("UPDATE users SET balance = balance + ? WHERE telegram_id = ?", (amount, telegram_id))
    conn.commit()
    conn.close()

def deduct_balance(telegram_id, amount):
    conn = sqlite3.connect("cases_bot.db", timeout=10)
    c = conn.cursor()
    c.execute("UPDATE users SET balance = balance - ? WHERE telegram_id = ? AND balance >= ?", 
              (amount, telegram_id, amount))
    conn.commit()
    conn.close()

def add_item(telegram_id, item_name, item_price, item_rarity, item_type, case_name):
    conn = sqlite3.connect("cases_bot.db", timeout=10)
    c = conn.cursor()
    c.execute("INSERT INTO inventory (telegram_id, item_name, item_price, item_rarity, item_type, case_name, open_date) VALUES (?, ?, ?, ?, ?, ?, ?)",
              (telegram_id, item_name, item_price, item_rarity, item_type, case_name, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()
    return c.lastrowid

def get_inventory(telegram_id):
    conn = sqlite3.connect("cases_bot.db", timeout=10)
    c = conn.cursor()
    c.execute("SELECT id, item_name, item_price, item_rarity, item_type FROM inventory WHERE telegram_id = ? AND sold = 0 ORDER BY id DESC", 
              (telegram_id,))
    result = c.fetchall()
    conn.close()
    return result

def get_all_inventory(telegram_id):
    conn = sqlite3.connect("cases_bot.db", timeout=10)
    c = conn.cursor()
    c.execute("SELECT item_name, item_price, item_rarity, item_type FROM inventory WHERE telegram_id = ? AND sold = 0", (telegram_id,))
    result = c.fetchall()
    conn.close()
    return result

def get_most_expensive_item(telegram_id):
    conn = sqlite3.connect("cases_bot.db", timeout=10)
    c = conn.cursor()
    c.execute("SELECT item_name, item_price, item_rarity, item_type FROM inventory WHERE telegram_id = ? AND sold = 0 ORDER BY item_price DESC LIMIT 1", 
              (telegram_id,))
    result = c.fetchone()
    conn.close()
    return result

def sell_item(item_id, telegram_id):
    conn = sqlite3.connect("cases_bot.db", timeout=10)
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
    conn = sqlite3.connect("cases_bot.db", timeout=10)
    c = conn.cursor()
    c.execute("SELECT case_name, item_name, open_date FROM inventory WHERE telegram_id = ? ORDER BY id DESC LIMIT ?",
              (telegram_id, limit))
    result = c.fetchall()
    conn.close()
    return result

def get_last_bonus(telegram_id):
    conn = sqlite3.connect("cases_bot.db", timeout=10)
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
    conn = sqlite3.connect("cases_bot.db", timeout=10)
    c = conn.cursor()
    c.execute("UPDATE users SET last_bonus = ? WHERE telegram_id = ?", 
              (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), telegram_id))
    conn.commit()
    conn.close()

def get_last_promo(telegram_id):
    conn = sqlite3.connect("cases_bot.db", timeout=10)
    c = conn.cursor()
    c.execute("SELECT last_promo FROM users WHERE telegram_id = ?", (telegram_id,))
    result = c.fetchone()
    conn.close()
    if result and result[0]:
        try:
            return datetime.strptime(result[0], "%Y-%m-%d %H:%M:%S")
        except:
            return datetime.strptime("1970-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
    return datetime.strptime("1970-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")

def update_last_promo(telegram_id):
    conn = sqlite3.connect("cases_bot.db", timeout=10)
    c = conn.cursor()
    c.execute("UPDATE users SET last_promo = ? WHERE telegram_id = ?", 
              (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), telegram_id))
    conn.commit()
    conn.close()

def add_log(telegram_id, action, amount=0, details=""):
    conn = sqlite3.connect("cases_bot.db", timeout=10)
    c = conn.cursor()
    c.execute("INSERT INTO logs (telegram_id, action, amount, details, date) VALUES (?, ?, ?, ?, ?)",
              (telegram_id, action, amount, details, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def get_user_logs(telegram_id, limit=50):
    conn = sqlite3.connect("cases_bot.db", timeout=10)
    c = conn.cursor()
    c.execute("SELECT action, amount, details, date FROM logs WHERE telegram_id = ? ORDER BY id DESC LIMIT ?",
              (telegram_id, limit))
    result = c.fetchall()
    conn.close()
    return result

def get_all_users():
    conn = sqlite3.connect("cases_bot.db", timeout=10)
    c = conn.cursor()
    c.execute("SELECT telegram_id FROM users")
    result = c.fetchall()
    conn.close()
    return [row[0] for row in result]

def get_referrals(referrer_id):
    conn = sqlite3.connect("cases_bot.db", timeout=10)
    c = conn.cursor()
    c.execute("SELECT referral_id, date, bonus_claimed FROM referrals WHERE referrer_id = ? ORDER BY id DESC", (referrer_id,))
    result = c.fetchall()
    conn.close()
    return result

def get_all_referrals():
    conn = sqlite3.connect("cases_bot.db", timeout=10)
    c = conn.cursor()
    c.execute("SELECT r.referrer_id, u1.username, r.referral_id, u2.username, r.date, r.bonus_claimed FROM referrals r LEFT JOIN users u1 ON r.referrer_id = u1.telegram_id LEFT JOIN users u2 ON r.referral_id = u2.telegram_id ORDER BY r.id DESC")
    result = c.fetchall()
    conn.close()
    return result

def add_referral(referrer_id, referral_id):
    conn = sqlite3.connect("cases_bot.db", timeout=10)
    c = conn.cursor()
    c.execute("INSERT INTO referrals (referrer_id, referral_id, date, bonus_claimed) VALUES (?, ?, ?, 0)",
              (referrer_id, referral_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def check_referral_bonus(referral_id):
    conn = sqlite3.connect("cases_bot.db", timeout=10)
    c = conn.cursor()
    c.execute("SELECT id, referrer_id, bonus_claimed FROM referrals WHERE referral_id = ?", (referral_id,))
    result = c.fetchone()
    conn.close()
    if result:
        return {"id": result[0], "referrer_id": result[1], "bonus_claimed": result[2]}
    return None

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

def backup_db():
    if os.path.exists("cases_bot.db"):
        shutil.copy2("cases_bot.db", f"cases_bot_backup_{datetime.now().strftime('%Y-%m-%d')}.db")
        return True
    return False

# ==================== ДОСТИЖЕНИЯ ====================
def check_achievement(telegram_id, achievement_id):
    conn = sqlite3.connect("cases_bot.db", timeout=10)
    c = conn.cursor()
    c.execute("SELECT * FROM achievements WHERE telegram_id = ? AND achievement_id = ?", (telegram_id, achievement_id))
    result = c.fetchone()
    conn.close()
    return result is not None

def claim_achievement(telegram_id, achievement_id):
    conn = sqlite3.connect("cases_bot.db", timeout=10)
    c = conn.cursor()
    c.execute("INSERT INTO achievements (telegram_id, achievement_id, claimed) VALUES (?, ?, 1)", (telegram_id, achievement_id))
    conn.commit()
    conn.close()

def get_user_achievements(telegram_id):
    conn = sqlite3.connect("cases_bot.db", timeout=10)
    c = conn.cursor()
    c.execute("SELECT achievement_id FROM achievements WHERE telegram_id = ?", (telegram_id,))
    result = c.fetchall()
    conn.close()
    return [row[0] for row in result]

def get_user_stats(telegram_id):
    conn = sqlite3.connect("cases_bot.db", timeout=10)
    c = conn.cursor()
    c.execute("SELECT total_spent, cases_opened, mines_wins, fortune_wins, vip_until FROM users WHERE telegram_id = ?", (telegram_id,))
    result = c.fetchone()
    conn.close()
    if result:
        return {"total_spent": result[0], "cases_opened": result[1], "mines_wins": result[2], "fortune_wins": result[3], "vip_until": result[4]}
    return {"total_spent": 0, "cases_opened": 0, "mines_wins": 0, "fortune_wins": 0, "vip_until": "1970-01-01 00:00:00"}

def update_user_stats(telegram_id, field, value):
    conn = sqlite3.connect("cases_bot.db", timeout=10)
    c = conn.cursor()
    c.execute(f"UPDATE users SET {field} = {field} + ? WHERE telegram_id = ?", (value, telegram_id))
    conn.commit()
    conn.close()

def open_secret_case(telegram_id):
    price = random.randint(10, 500)
    rare_chance = random.random()
    if rare_chance < 0.0005:
        price = price * 50
        rarity = "Легендарный"
    elif rare_chance < 0.001:
        price = price * 20
        rarity = "Эпический"
    else:
        rarity = "Обычный"
    
    item_name = f"🎁 Секретный кейс"
    add_item(telegram_id, item_name, price, rarity, "Кейс", "Секретный кейс")
    update_balance(telegram_id, price)
    return price, rarity

def is_vip(telegram_id):
    stats = get_user_stats(telegram_id)
    try:
        vip_until = datetime.strptime(stats["vip_until"], "%Y-%m-%d %H:%M:%S")
        return vip_until > datetime.now()
    except:
        return False

def get_vip_discount(cost):
    return int(cost * 0.8)

def get_vip_mine_multiplier(base_multiplier):
    return base_multiplier * 1.2

# ==================== КЛАВИАТУРЫ ====================
def main_menu(user_id=None):
    buttons = [
        [InlineKeyboardButton("📦 Открыть кейс", callback_data="open_case"),
         InlineKeyboardButton("👤 Профиль", callback_data="profile")],
        [InlineKeyboardButton("💰 Пополнить баланс", callback_data="deposit_menu"),
         InlineKeyboardButton("🎁 Бесплатный бонус (+20 G)", callback_data="bonus")],
        [InlineKeyboardButton("💣 Мини-игра: Мины", callback_data="mines_menu"),
         InlineKeyboardButton("🎰 Мини-игра: Колесо Фортуны", callback_data="fortune_menu")],
        [InlineKeyboardButton("📜 История", callback_data="history"),
         InlineKeyboardButton("👔 Сотрудничество", callback_data="collab")]
    ]
    if user_id == DEVELOPER_ID:
        buttons.append([InlineKeyboardButton("👑 Админ-панель", callback_data="admin_panel"),
                        InlineKeyboardButton("💰 +10000 G (DEV)", callback_data="add_dev_10000")])
    return InlineKeyboardMarkup(buttons)

def admin_panel_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📋 Логи", callback_data="admin_logs"),
         InlineKeyboardButton("👥 Реф система", callback_data="admin_refs")],
        [InlineKeyboardButton("📢 Сообщение всем", callback_data="admin_broadcast"),
         InlineKeyboardButton("📈 Статистика", callback_data="admin_stats")],
        [InlineKeyboardButton("🛑 Бан пользователя", callback_data="admin_ban"),
         InlineKeyboardButton("🎫 Создать промокод", callback_data="admin_create_promo")],
        [InlineKeyboardButton("🔙 Назад", callback_data="back")]
    ])

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
        [InlineKeyboardButton("📦 Инвентарь", callback_data="inventory"),
         InlineKeyboardButton("💰 Продать скин", callback_data="sell_menu")],
        [InlineKeyboardButton("💎 Вывод скина", callback_data="withdraw_menu"),
         InlineKeyboardButton("👥 Реферальная система", callback_data="referral_system")],
        [InlineKeyboardButton("🎫 Промокод", callback_data="promo_menu"),
         InlineKeyboardButton("🏅 Достижения", callback_data="achievements")],
        [InlineKeyboardButton("💎 VIP-статус", callback_data="vip_menu"),
         InlineKeyboardButton("🛠 Тех. Поддержка", callback_data="support")],
        [InlineKeyboardButton("🔙 Назад", callback_data="back")]
    ])

def vip_menu_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("👑 Купить VIP (500 G/мес)", callback_data="buy_vip")],
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
        [InlineKeyboardButton("🔙 Назад", callback_data="back")]
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
    buttons.append([InlineKeyboardButton("🔙 Назад", callback_data="back")])
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
waiting_for_collab = {}
support_requests = {}
admin_state = {}
waiting_for_promo = {}
waiting_for_transfer = {}
waiting_for_pattern = {}  # {user_id: item_id}
banned_users = set()

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

async def backup_scheduler():
    while True:
        await asyncio.sleep(86400)
        if backup_db():
            print(f"✅ Бэкап создан: cases_bot_backup_{datetime.now().strftime('%Y-%m-%d')}.db")
        else:
            print("❌ Ошибка создания бэкапа")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.username
    
    if user_id in banned_users:
        await update.message.reply_text("🛑 **Вы забанены!**\n\nОбратитесь к администратору.", parse_mode="Markdown")
        return
    
    referrer_id = 0
    if context.args:
        try:
            referrer_id = int(context.args[0])
            if referrer_id == user_id:
                referrer_id = 0
        except:
            pass
    
    register_user(user_id, username, referrer_id)
    
    if referrer_id > 0:
        existing = check_referral_bonus(user_id)
        if not existing:
            add_referral(referrer_id, user_id)
    
    await update.message.reply_text(
        f"🔥 **Добро пожаловать в открытие кейсов «ВЕЗУНЧИК»!**\n\n"
        f"Испытай удачу и выбей топовый скин! 🍀\n\n"
        f"💰 **Твой баланс:** {get_balance(user_id)} G\n\n"
        f"Выбирай действие:",
        reply_markup=main_menu(user_id),
        parse_mode="Markdown"
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    data = query.data

    if user_id in banned_users:
        await query.answer("🛑 Вы забанены!", show_alert=True)
        return

    # === АДМИНКА ===
    if data == "admin_panel":
        if user_id != DEVELOPER_ID:
            await query.answer("⛔ Только для разработчика!", show_alert=True)
            return
        await query.edit_message_text(
            "👑 **Админ-панель**\n\n"
            "Выберите действие:",
            reply_markup=admin_panel_buttons(),
            parse_mode="Markdown"
        )
        return

    if data == "admin_logs":
        if user_id != DEVELOPER_ID:
            await query.answer("⛔ Только для разработчика!", show_alert=True)
            return
        admin_state[user_id] = "logs"
        await query.edit_message_text(
            "📋 **Логи игрока**\n\n"
            "Введите **@username** игрока:",
            reply_markup=back_button(),
            parse_mode="Markdown"
        )
        return

    if data == "admin_refs":
        if user_id != DEVELOPER_ID:
            await query.answer("⛔ Только для разработчика!", show_alert=True)
            return
        refs = get_all_referrals()
        if not refs:
            text = "👥 **Реферальная система**\n\nНет рефералов."
        else:
            text = "👥 **Реферальная система**\n\n"
            for r in refs[:30]:
                referrer = r[1] if r[1] else f"ID{r[0]}"
                referral = r[3] if r[3] else f"ID{r[2]}"
                bonus = "✅" if r[5] else "❌"
                text += f"👤 {referrer} → {referral} {bonus}\n"
            if len(refs) > 30:
                text += f"\n... и ещё {len(refs)-30} записей"
        await query.edit_message_text(
            text,
            reply_markup=back_button(),
            parse_mode="Markdown"
        )
        return

    if data == "admin_broadcast":
        if user_id != DEVELOPER_ID:
            await query.answer("⛔ Только для разработчика!", show_alert=True)
            return
        admin_state[user_id] = "broadcast"
        await query.edit_message_text(
            "📢 **Сообщение всем пользователям**\n\n"
            "Введите текст для рассылки:",
            reply_markup=back_button(),
            parse_mode="Markdown"
        )
        return

    if data == "admin_stats":
        if user_id != DEVELOPER_ID:
            await query.answer("⛔ Только для разработчика!", show_alert=True)
            return
        users = get_all_users()
        total_users = len(users)
        conn = sqlite3.connect("cases_bot.db", timeout=10)
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM inventory")
        total_keys = c.fetchone()[0]
        c.execute("SELECT SUM(balance) FROM users")
        total_gold = c.fetchone()[0] or 0
        conn.close()
        
        top = db_query("SELECT username, balance FROM users ORDER BY balance DESC LIMIT 5", fetchall=True) or []
        top_text = "\n".join([f"• {row[0] or 'Аноним'} — {row[1]} G" for row in top]) if top else "Нет данных"
        
        text = f"📈 **Статистика бота**\n\n"
        text += f"👥 **Всего пользователей:** {total_users}\n"
        text += f"📦 **Открыто кейсов:** {total_keys}\n"
        text += f"💰 **Голда в обороте:** {total_gold} G\n\n"
        text += f"🏆 **Топ-5 игроков:**\n{top_text}"
        
        await query.edit_message_text(
            text,
            reply_markup=back_button(),
            parse_mode="Markdown"
        )
        return

    if data == "admin_ban":
        if user_id != DEVELOPER_ID:
            await query.answer("⛔ Только для разработчика!", show_alert=True)
            return
        admin_state[user_id] = "ban"
        await query.edit_message_text(
            "🛑 **Бан пользователя**\n\n"
            "Введите **@username** игрока, которого хотите забанить или разбанить.\n\n"
            "Если игрок уже в бане — он будет разбанен.",
            reply_markup=back_button(),
            parse_mode="Markdown"
        )
        return

    if data == "admin_create_promo":
        if user_id != DEVELOPER_ID:
            await query.answer("⛔ Только для разработчика!", show_alert=True)
            return
        admin_state[user_id] = "promo_type"
        await query.edit_message_text(
            "🎫 **Создание промокода**\n\n"
            "Выберите тип награды:\n\n"
            "1️⃣ `balance` — фиксированная голда\n"
            "2️⃣ `random_balance` — случайная голда (мин/макс)\n"
            "3️⃣ `random_skin` — случайный скин\n"
            "4️⃣ `skin_fixed` — фиксированный скин\n"
            "5️⃣ `multiple_skins` — несколько скинов\n\n"
            "Введите тип одним словом:",
            reply_markup=back_button(),
            parse_mode="Markdown"
        )
        return

    # === ОТВЕТ В ПОДДЕРЖКУ ===
    if data.startswith("reply_"):
        if user_id != DEVELOPER_ID:
            await query.answer("⛔ Только для разработчика!", show_alert=True)
            return
        target_id = int(data.split("_")[1])
        support_requests[user_id] = {"step": "replying", "target_id": target_id}
        await query.edit_message_text(
            f"✏️ **Напишите ответ** для игрока (ID: {target_id}):\n\n"
            f"Просто отправьте сообщение, и бот перешлёт его игроку.",
            reply_markup=back_button(),
            parse_mode="Markdown"
        )
        return

    # === МИНЫ ===
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

    # === НАВИГАЦИЯ ===
    if data == "back":
        for d in (deposit_timer, dev_add_data, waiting_for_collab, support_requests, admin_state, waiting_for_promo, waiting_for_transfer, waiting_for_pattern):
            d.pop(user_id, None)
        await query.edit_message_text("🔙 **Главное меню**", reply_markup=main_menu(user_id), parse_mode="Markdown")
        return

    if data == "open_case":
        await query.edit_message_text("🎯 **Выбери кейс:**", reply_markup=case_buttons(), parse_mode="Markdown")
        return

    if data == "profile":
        balance = get_balance(user_id)
        most_expensive = get_most_expensive_item(user_id)
        inventory_count = len(get_all_inventory(user_id))
        vip_status = "✅ Активен" if is_vip(user_id) else "❌ Неактивен"
        text = f"👤 **Профиль**\n\n"
        text += f"💰 **Баланс:** {balance} G\n"
        text += f"👑 **VIP-статус:** {vip_status}\n"
        if most_expensive:
            color = RARITY_COLORS.get(most_expensive[2], "⬜")
            text += f"🏆 **Самый дорогой скин:** {color} {most_expensive[0]} ({most_expensive[1]} G)\n"
        else:
            text += f"🏆 **Самый дорогой скин:** нет\n"
        text += f"📦 **Всего предметов:** {inventory_count}\n"
        await query.edit_message_text(text, reply_markup=profile_menu(), parse_mode="Markdown")
        return

    # === VIP-СТАТУС ===
    if data == "vip_menu":
        vip_status = "✅ Активен" if is_vip(user_id) else "❌ Неактивен"
        text = f"💎 **VIP-статус**\n\n"
        text += f"👑 **Текущий статус:** {vip_status}\n\n"
        text += f"**Привилегии VIP:**\n"
        text += f"• 🎁 **50 G** каждый день\n"
        text += f"• 💰 **-20%** на стоимость всех кейсов\n"
        text += f"• ⚡ **Улучшенные множители** в минах (x1.2)\n"
        text += f"• 🎰 **Увеличенные шансы** в фортуне\n\n"
        text += f"💰 **Стоимость:** 500 G / месяц"
        await query.edit_message_text(
            text,
            reply_markup=vip_menu_buttons(),
            parse_mode="Markdown"
        )
        return

    if data == "buy_vip":
        if is_vip(user_id):
            await query.answer("❌ У вас уже есть VIP-статус!", show_alert=True)
            return
        balance = get_balance(user_id)
        if balance < 500:
            await query.answer(f"❌ Не хватает G! Нужно 500, у тебя {balance}", show_alert=True)
            return
        deduct_balance(user_id, 500)
        conn = sqlite3.connect("cases_bot.db", timeout=10)
        c = conn.cursor()
        new_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")
        c.execute("UPDATE users SET vip_until = ? WHERE telegram_id = ?", (new_date, user_id))
        conn.commit()
        conn.close()
        await query.edit_message_text(
            f"✅ **VIP-статус активирован!**\n\n"
            f"👑 VIP активен до {new_date}\n\n"
            f"💰 Снято: 500 G\n"
            f"💳 Баланс: {get_balance(user_id)} G",
            reply_markup=main_menu(user_id),
            parse_mode="Markdown"
        )
        return

    if data == "achievements":
        user_achs = get_user_achievements(user_id)
        stats = get_user_stats(user_id)
        
        text = "🏅 **Достижения**\n\n"
        text += f"📊 **Статистика:**\n"
        text += f"• Потрачено голды: {stats['total_spent']} G\n"
        text += f"• Открыто кейсов: {stats['cases_opened']}\n"
        text += f"• Побед в минах: {stats['mines_wins']}\n"
        text += f"• Побед в фортуне: {stats['fortune_wins']}\n\n"
        
        text += "📋 **Доступные достижения:**\n\n"
        for key, ach in ACHIEVEMENTS.items():
            status = "✅" if key in user_achs else "⬜"
            reward_text = f"{ach['reward']} G" if ach['type'] == "balance" else "🎁 Секретный кейс"
            text += f"{status} {ach['name']}\n"
            text += f"   └ {ach['desc']} — Награда: {reward_text}\n\n"
        
        await query.edit_message_text(
            text,
            reply_markup=back_button(),
            parse_mode="Markdown"
        )
        return

    if data == "referral_system":
        refs = get_referrals(user_id)
        ref_count = len(refs)
        bonus_count = sum(1 for r in refs if r[2] == 1)
        total_earned = bonus_count * 10
        link = f"https://t.me/Standoff2Lucky_bot?start={user_id}"
        text = f"👥 **Реферальная система**\n\n"
        text += f"Приглашай друзей и получай бонусы!\n\n"
        text += f"🔗 **Твоя ссылка:**\n`{link}`\n\n"
        text += f"📊 **Статистика:**\n"
        text += f"• **Приглашено:** {ref_count}\n"
        text += f"• **Получено бонусов:** {bonus_count}\n"
        text += f"• **Заработано:** {total_earned} G\n\n"
        text += f"💡 **Как получить бонус:**\n\n"
        text += f"1️⃣ Друг переходит по ссылке\n\n"
        text += f"2️⃣ Забирает бесплатный бонус (+20 G)\n\n"
        text += f"3️⃣ Играет в мины (1 раз)\n\n"
        text += f"4️⃣ Ты получаешь +10 G! 🎉"
        await query.edit_message_text(
            text,
            reply_markup=back_button(),
            parse_mode="Markdown"
        )
        return

    if data == "promo_menu":
        last_promo = get_last_promo(user_id)
        now = datetime.now()
        diff = now - last_promo
        if diff < timedelta(hours=3):
            remaining = timedelta(hours=3) - diff
            hours = remaining.seconds // 3600
            minutes = (remaining.seconds % 3600) // 60
            await query.edit_message_text(
                f"🎫 **Промокод**\n\n"
                f"Введите промокод в поле ниже.\n\n"
                f"⏳ Следующий промокод можно активировать через:\n"
                f"**{hours} ч {minutes} мин**",
                reply_markup=back_button(),
                parse_mode="Markdown"
            )
            return
        
        waiting_for_promo[user_id] = True
        await query.edit_message_text(
            f"🎫 **Промокод**\n\n"
            f"Введите промокод в поле ниже.\n\n"
            f"⏳ Активация раз в 3 часа!",
            reply_markup=back_button(),
            parse_mode="Markdown"
        )
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
            f"✅ **Пополнено на 10000 G!**\n\n"
            f"💰 **Новый баланс:** {new_balance} G",
            reply_markup=main_menu(user_id),
            parse_mode="Markdown"
        )
        return

    if data == "support":
        support_requests[user_id] = {"step": "question"}
        await query.edit_message_text(
            "🛠 **Тех. Поддержка**\n\n"
            "Напишите ваш вопрос или проблему одним сообщением.\n"
            "ОБЯЗАТЕЛЬНО ОСТАВЬТЕ СВОЙ ЮЗЕРНЕЙМ!!!\n\n"
            "Администрация свяжется с вами в ближайшее время.",
            reply_markup=back_button(),
            parse_mode="Markdown"
        )
        return

    if data == "bonus":
        last_bonus = get_last_bonus(user_id)
        now = datetime.now()
        diff = now - last_bonus
        
        vip_bonus = 50 if is_vip(user_id) else 20
        
        if diff < timedelta(days=3):
            remaining = timedelta(days=3) - diff
            hours = remaining.seconds // 3600
            minutes = (remaining.seconds % 3600) // 60
            await query.edit_message_text(
                f"⏳ **Бонус уже получен!**\n\n"
                f"Следующий бонус будет доступен через:\n"
                f"**{hours} ч {minutes} мин**\n\n"
                f"🎁 Бонус даёт +{vip_bonus} G каждые 3 дня!",
                reply_markup=back_button(),
                parse_mode="Markdown"
            )
            return
        
        update_balance(user_id, vip_bonus)
        update_last_bonus(user_id)
        new_balance = get_balance(user_id)
        
        referral_info = check_referral_bonus(user_id)
        if referral_info and referral_info["bonus_claimed"] == 0:
            conn = sqlite3.connect("cases_bot.db", timeout=10)
            c = conn.cursor()
            c.execute("UPDATE referrals SET bonus_claimed = 1 WHERE referral_id = ?", (user_id,))
            conn.commit()
            conn.close()
        
        await query.edit_message_text(
            f"🎁 **Бонус получен!**\n\n"
            f"💰 **Начислено:** +{vip_bonus} G\n"
            f"💳 **Новый баланс:** {new_balance} G\n\n"
            f"Следующий бонус будет доступен через 3 дня!",
            reply_markup=back_button(),
            parse_mode="Markdown"
        )
        return

    # === ПОПОЛНЕНИЕ ===
    if data == "deposit_menu":
        await query.edit_message_text(
            f"💰 **Выберите способ пополнения:**\n\n"
            f"😘 Учтите, мы рекомендуем пополнять баланс через перевод, "
            f"ибо голдой будет чуть посложнее лично нам — мы вручную выставляем скины и проверяем, купили ли вы скин.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💰 Пополнить голдой", callback_data="deposit_gold")],
                [InlineKeyboardButton("💸 Пополнить переводом", callback_data="deposit_transfer")],
                [InlineKeyboardButton("🔙 Назад", callback_data="back")]
            ]),
            parse_mode="Markdown"
        )
        return

    if data == "deposit_gold":
        await query.edit_message_text(
            f"💰 **Пополнение голдой**\n\n"
            f"Выберите сумму пополнения:\n\n"
            f"К сожалению пополнение через бота доступно только Голдой! Комиссию мы берём на себя♥️",
            reply_markup=deposit_buttons(),
            parse_mode="Markdown"
        )
        return

    if data == "deposit_transfer":
        waiting_for_transfer[user_id] = True
        await query.edit_message_text(
            f"💸 **Пополнение переводом**\n\n"
            f"Введите сумму в рублях (от 10 до 10000 ₽):",
            reply_markup=back_button(),
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
            reply_markup=back_button(),
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

    if data == "collab":
        await query.edit_message_text(
            "👔 **Сотрудничество**\n\n"
            "Здравствуйте, сейчас мы в активных поисках **ПИАР-МЕНЕДЖЕРОВ**!\n\n"
            "Если вы думаете, что хорошо подойдёте на данную должность, пожалуйста, заполните анкету ниже.\n\n"
            "**Ваша задача:**\n"
            "Снимать клипы/нарезки в TikTok либо YouTube Shorts о данном боте, а также играть под ником:\n"
            "• @Standoff2Lucky_bot\n"
            "• Либо @IntersoulShop\n\n"
            "Выбирать можете сами!\n\n"
            "**Оплата за ваш труд:**\n"
            "• Баланс на бота для нового контента\n"
            "• Либо внутриигровая валюта в игре\n\n"
            "📝 **Анкета:**\n\n"
            "👔 Ваше имя:\n"
            "👔 Ваш возраст:\n"
            "👔 Сколько по времени собираетесь сотрудничать:\n"
            "👔 Каким способом предпочитаете получать награду? (Балансом или Внутриигровой валютой)\n"
            "👔 Какой тип контента собираетесь снимать:\n\n"
            "📌 **Пример заполнения:**\n"
            "Александр\n"
            "18\n"
            "Всю жизнь\n"
            "Балансом\n"
            "Различные пути\n\n"
            "✏️ Напишите ответы на вопросы одним сообщением, и я отправлю их разработчику!",
            reply_markup=back_button(),
            parse_mode="Markdown"
        )
        waiting_for_collab[user_id] = True
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
        await fortune_spin_handler(update, context)
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
        conn = sqlite3.connect("cases_bot.db", timeout=10)
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
                f"✅ **Скин продан за {price} G!**\n\n"
                f"💰 **Новый баланс:** {new_balance} G",
                reply_markup=back_button(),
                parse_mode="Markdown"
            )
        else:
            await query.edit_message_text("❌ Ошибка: предмет не найден или уже продан.", reply_markup=back_button())
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
        
        # Проверяем, есть ли уже паттерн у этого скина
        conn = sqlite3.connect("cases_bot.db", timeout=10)
        c = conn.cursor()
        c.execute("SELECT pattern FROM inventory WHERE id = ? AND telegram_id = ? AND sold = 0", (item_id, user_id))
        result = c.fetchone()
        conn.close()
        
        if result and result[0]:
            # Паттерн уже есть — сразу отправляем заявку
            await process_withdraw_request(update, context, user_id, item_id, result[0])
        else:
            # Запрашиваем паттерн
            waiting_for_pattern[user_id] = item_id
            await query.edit_message_text(
                f"🔢 **Введите паттерн скина**\n\n"
                f"Паттерн состоит из 3 цифр.\n"
                f"Пример: `264`",
                reply_markup=back_button(),
                parse_mode="Markdown"
            )
        return

    if data.startswith("quick_sell_"):
        item_id = int(data.split("_")[2])
        price = sell_item(item_id, user_id)
        if price:
            new_balance = get_balance(user_id)
            await query.edit_message_text(
                f"💰 **Скин продан за {price} G!**\n\n"
                f"💳 **Новый баланс:** {new_balance} G",
                reply_markup=back_button(),
                parse_mode="Markdown"
            )
        else:
            await query.edit_message_text("❌ Ошибка при продаже.", reply_markup=back_button())
        return

    if data.startswith("keep_"):
        await query.edit_message_text(
            f"📦 **Скин сохранён в инвентаре!**\n\n"
            f"Ты можешь продать его позже через профиль.",
            reply_markup=back_button(),
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
        cost = case["cost"]
        if is_vip(user_id):
            cost = get_vip_discount(cost)
        if balance < cost:
            await query.answer(f"❌ Не хватает G! Нужно {cost}, у тебя {balance}", show_alert=True)
            return
        case_cache[user_id] = case_key
        selected_box_cache[user_id] = None
        await query.edit_message_text(
            f"🎰 **{case['name']} открывается...**\n"
            f"💰 Стоимость: {cost} G\n\n"
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

    # ==================== ОТКРЫТИЕ КЕЙСА С ПРОГРЕСС-БАРОМ ====================
    if data.startswith("confirm_"):
        parts = data.split("_")
        case_key = parts[1]
        box_num = int(parts[2])
        case = CASES.get(case_key)
        if not case:
            await query.edit_message_text("❌ Ошибка: кейс не найден", reply_markup=main_menu(user_id))
            return
        
        balance = get_balance(user_id)
        cost = case["cost"]
        if is_vip(user_id):
            cost = get_vip_discount(cost)
        
        if balance < cost:
            await query.answer(f"❌ Не хватает G! Нужно {cost}, у тебя {balance}", show_alert=True)
            return
        
        deduct_balance(user_id, cost)
        update_user_stats(user_id, "total_spent", cost)
        update_user_stats(user_id, "cases_opened", 1)
        
        # Прогресс-бар
        msg = await query.edit_message_text(
            f"🎰 **Открываем кейс {case['name']}...**\n\n"
            f"▰▱▱▱▱▱▱▱▱▱ 10%",
            parse_mode="Markdown"
        )
        await asyncio.sleep(0.4)
        await msg.edit_text(
            f"🎰 **Открываем кейс {case['name']}...**\n\n"
            f"▰▰▰▱▱▱▱▱▱▱ 30%",
            parse_mode="Markdown"
        )
        await asyncio.sleep(0.4)
        await msg.edit_text(
            f"🎰 **Открываем кейс {case['name']}...**\n\n"
            f"▰▰▰▰▰▰▱▱▱▱ 60%",
            parse_mode="Markdown"
        )
        await asyncio.sleep(0.4)
        await msg.edit_text(
            f"🎰 **Открываем кейс {case['name']}...**\n\n"
            f"▰▰▰▰▰▰▰▰▰▰ 100%",
            parse_mode="Markdown"
        )
        await asyncio.sleep(0.3)
        
        item_data = weighted_choice(case["items"])
        item_name = item_data["name"]
        item_price = item_data["price"]
        item_rarity = item_data["rarity"]
        item_type = item_data["type"]
        
        color = RARITY_COLORS.get(item_rarity, "⬜")
        item_id = add_item(user_id, item_name, item_price, item_rarity, item_type, case["name"])
        new_balance = get_balance(user_id)
        
        stats = get_user_stats(user_id)
        if stats["total_spent"] >= 3000 and not check_achievement(user_id, "spend_3000"):
            claim_achievement(user_id, "spend_3000")
            add_log(user_id, "Достижение", 0, "spend_3000 -> Секретный кейс")
            
            await msg.edit_text(
                f"🎉 **Ты открыл коробку №{box_num}!**\n\n"
                f"📌 Тип скина: **{item_type}**\n"
                f"{color} Редкость: **{item_rarity}**\n"
                f"🔫 Название: **{item_name}**\n"
                f"💰 Цена: **{item_price} G**\n\n"
                f"💳 **Баланс:** {new_balance} G\n\n"
                f"🏅 **ДОСТИЖЕНИЕ РАЗБЛОКИРОВАНО!**\n"
                f"💸 Транжира — потрать 3000 G\n"
                f"🎁 Награда: Секретный кейс!\n\n"
                f"Нажми на кнопку ниже, чтобы открыть его!",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🎁 Открыть секретный кейс", callback_data=f"secret_case_{user_id}")],
                    [InlineKeyboardButton("🔙 Назад", callback_data="back")]
                ]),
                parse_mode="Markdown"
            )
            return
        
        if stats["cases_opened"] == 1 and not check_achievement(user_id, "first_case"):
            claim_achievement(user_id, "first_case")
            update_balance(user_id, 10)
            await msg.edit_text(
                f"🎉 **Ты открыл коробку №{box_num}!**\n\n"
                f"📌 Тип скина: **{item_type}**\n"
                f"{color} Редкость: **{item_rarity}**\n"
                f"🔫 Название: **{item_name}**\n"
                f"💰 Цена: **{item_price} G**\n\n"
                f"💳 **Баланс:** {new_balance} G\n\n"
                f"🏅 **ДОСТИЖЕНИЕ РАЗБЛОКИРОВАНО!**\n"
                f"🎯 Первый кейс — +10 G!",
                reply_markup=after_open_buttons(item_id, item_price),
                parse_mode="Markdown"
            )
            return
        
        await msg.edit_text(
            f"🎉 **Ты открыл коробку №{box_num}!**\n\n"
            f"📌 Тип скина: **{item_type}**\n"
            f"{color} Редкость: **{item_rarity}**\n"
            f"🔫 Название: **{item_name}**\n"
            f"💰 Цена: **{item_price} G**\n\n"
            f"💳 **Баланс:** {new_balance} G\n\n"
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

    # === ОТКРЫТИЕ СЕКРЕТНОГО КЕЙСА ===
    if data.startswith("secret_case_"):
        user_id_from_callback = int(data.split("_")[2])
        if user_id != user_id_from_callback:
            await query.answer("❌ Это не ваш секретный кейс!", show_alert=True)
            return
        
        if not check_achievement(user_id, "spend_3000"):
            await query.edit_message_text(
                "❌ У вас нет секретного кейса!",
                reply_markup=main_menu(user_id)
            )
            return
        
        # Открываем секретный кейс
        secret_price, secret_rarity = open_secret_case(user_id)
        new_balance = get_balance(user_id)
        
        await query.edit_message_text(
            f"🎁 **Секретный кейс открыт!**\n\n"
            f"💎 Ты получил **{secret_price} G**\n"
            f"⭐ Редкость: **{secret_rarity}**\n\n"
            f"💳 **Баланс:** {new_balance} G",
            reply_markup=main_menu(user_id),
            parse_mode="Markdown"
        )
        add_log(user_id, "Секретный кейс", secret_price, f"Редкость: {secret_rarity}")
        return

# ==================== ФУНКЦИЯ ОБРАБОТКИ ЗАЯВКИ НА ВЫВОД ====================
async def process_withdraw_request(update, context, user_id, item_id, pattern):
    query = update.callback_query
    conn = sqlite3.connect("cases_bot.db", timeout=10)
    c = conn.cursor()
    c.execute("SELECT item_name, item_price, case_name FROM inventory WHERE id = ? AND telegram_id = ? AND sold = 0", 
              (item_id, user_id))
    result = c.fetchone()
    conn.close()
    
    if not result:
        await query.edit_message_text("❌ Ошибка: предмет не найден.", reply_markup=back_button())
        return
    
    item_name = result[0]
    price = result[1]
    case_name = result[2] if result[2] else "Неизвестно"
    
    base_price = price * 1.2
    random_cents = random.randint(1, 99) / 100
    final_price = base_price + random_cents
    final_price = round(final_price, 2)
    
    # ===== ОТПРАВКА ЗАЯВКИ РАЗРАБОТЧИКУ =====
    try:
        user = await context.bot.get_chat(user_id)
        username = user.username if user.username else f"ID{user_id}"
        
        await context.bot.send_message(
            chat_id=DEVELOPER_ID,
            text=f"📩 **ЗАЯВКА НА ВЫВОД СКИНА**\n\n"
                 f"👤 Игрок: @{username}\n"
                 f"🆔 ID: {user_id}\n\n"
                 f"🔫 Скин: **{item_name}**\n"
                 f"📦 Откуда: **{case_name}**\n"
                 f"💰 Цена вывода: **{final_price} G**\n"
                 f"🔢 Паттерн: **{pattern}**\n\n"
                 f"📌 Статус: **Ожидает проверки**\n"
                 f"🔄 Нажмите «Ответить», чтобы связаться с игроком.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✏️ Ответить игроку", callback_data=f"reply_{user_id}")]
            ]),
            parse_mode="Markdown"
        )
    except Exception as e:
        print(f"Ошибка отправки заявки: {e}")
    # ==========================================
    
    await query.edit_message_text(
        f"💎 **Отлично!**\n\n"
        f"Выставляй скин **G22 \"Adam\"** за **{final_price} G** и ожидай!\n"
        f"Не забудь указать паттерн: **{pattern}**\n\n"
        f"🔄 Администрация/бот скоро купит твой скин!",
        reply_markup=back_button(),
        parse_mode="Markdown"
    )

async def fortune_spin_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    
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
            f"💳 **Баланс:** {get_balance(user_id)} G",
            reply_markup=back_button(),
            parse_mode="Markdown"
        )
        del fortune_data[user_id]
        return
    
    if multiplier == 0:
        await msg.edit_text(
            f"🎰 **Результат: {result}**\n\n"
            f"{result} — {FORTUNE_EMOJIS[result]['name']}\n"
            f"💸 Ставка {bet} G сгорела!\n\n"
            f"💳 **Баланс:** {get_balance(user_id)} G",
            reply_markup=back_button(),
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
            f"💳 **Баланс:** {get_balance(user_id)} G",
            reply_markup=back_button(),
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
            f"💳 **Баланс:** {get_balance(user_id)} G",
            reply_markup=back_button(),
            parse_mode="Markdown"
        )
    else:
        await msg.edit_text(
            f"🎰 **Результат: {result}**\n\n"
            f"{result} — {FORTUNE_EMOJIS[result]['name']}\n"
            f"💰 Выигрыш: {win} G\n"
            f"⚡ Множитель: x{multiplier}\n\n"
            f"💳 **Баланс:** {get_balance(user_id)} G",
            reply_markup=back_button(),
            parse_mode="Markdown"
        )
    
    del fortune_data[user_id]

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()
    
    if user_id in banned_users:
        await update.message.reply_text("🛑 **Вы забанены!**\n\nОбратитесь к администратору.", parse_mode="Markdown")
        return
    
    # === ВВОД ПАТТЕРНА ПОСЛЕ ВЫВОДА СКИНА ===
    if user_id in waiting_for_pattern:
        pattern = text.strip()
        if not pattern.isdigit() or len(pattern) != 3:
            await update.message.reply_text("❌ Паттерн должен состоять из 3 цифр!\n\nПример: `264`", parse_mode="Markdown")
            return
        
        item_id = waiting_for_pattern[user_id]
        
        # Сохраняем паттерн в БД
        conn = sqlite3.connect("cases_bot.db", timeout=10)
        c = conn.cursor()
        c.execute("UPDATE inventory SET pattern = ? WHERE id = ? AND telegram_id = ?", (pattern, item_id, user_id))
        conn.commit()
        conn.close()
        
        del waiting_for_pattern[user_id]
        
        # Отправляем заявку
        await process_withdraw_request(update, context, user_id, item_id, pattern)
        return
    
    # === АДМИН: СОЗДАНИЕ ПРОМОКОДА ===
    if user_id == DEVELOPER_ID and admin_state.get(user_id) == "promo_type":
        promo_type = text.strip().lower()
        valid_types = ["balance", "random_balance", "random_skin", "skin_fixed", "multiple_skins"]
        if promo_type not in valid_types:
            await update.message.reply_text(
                f"❌ Неверный тип. Доступные: `balance`, `random_balance`, `random_skin`, `skin_fixed`, `multiple_skins`",
                parse_mode="Markdown"
            )
            return
        admin_state[user_id] = {"step": "promo_code", "type": promo_type}
        await update.message.reply_text(
            f"✅ Тип: `{promo_type}`\n\n"
            f"Теперь введите **код промокода** (латиница, цифры, без пробелов):",
            parse_mode="Markdown"
        )
        return

    if user_id == DEVELOPER_ID and isinstance(admin_state.get(user_id), dict):
        step = admin_state[user_id].get("step")
        promo_type = admin_state[user_id].get("type")
        
        if step == "promo_code":
            promo_code = text.strip().upper()
            if not promo_code.isalnum():
                await update.message.reply_text("❌ Код должен содержать только буквы и цифры!")
                return
            admin_state[user_id]["code"] = promo_code
            
            if promo_type == "balance":
                admin_state[user_id]["step"] = "promo_value"
                await update.message.reply_text("💰 Введите **количество голды** (число):")
            elif promo_type == "random_balance":
                admin_state[user_id]["step"] = "promo_random_min"
                await update.message.reply_text("💰 Введите **минимальную** сумму голды (число):")
            elif promo_type == "random_skin":
                admin_state[user_id]["step"] = "promo_random_min"
                await update.message.reply_text("🎁 Введите **минимальную** цену скина (число):")
            elif promo_type == "skin_fixed":
                admin_state[user_id]["step"] = "promo_value"
                await update.message.reply_text("🎁 Введите **цену** скина (число):")
            elif promo_type == "multiple_skins":
                admin_state[user_id]["step"] = "promo_multiple_count"
                await update.message.reply_text("📦 Введите **количество** скинов (число):")
            return
        
        if step == "promo_value":
            try:
                value = int(text.strip())
                if value <= 0:
                    await update.message.reply_text("❌ Сумма должна быть положительной!")
                    return
                admin_state[user_id]["value"] = value
                save_promo_to_db(update, context, admin_state[user_id])
                del admin_state[user_id]
            except ValueError:
                await update.message.reply_text("❌ Введите число!")
            return
        
        if step == "promo_random_min":
            try:
                min_val = int(text.strip())
                if min_val <= 0:
                    await update.message.reply_text("❌ Минимум должен быть положительным!")
                    return
                admin_state[user_id]["min"] = min_val
                admin_state[user_id]["step"] = "promo_random_max"
                await update.message.reply_text(f"✅ Минимум: {min_val}\n\nТеперь введите **максимальное** значение:")
            except ValueError:
                await update.message.reply_text("❌ Введите число!")
            return
        
        if step == "promo_random_max":
            try:
                max_val = int(text.strip())
                if max_val <= admin_state[user_id].get("min", 0):
                    await update.message.reply_text("❌ Максимум должен быть больше минимума!")
                    return
                admin_state[user_id]["max"] = max_val
                save_promo_to_db(update, context, admin_state[user_id])
                del admin_state[user_id]
            except ValueError:
                await update.message.reply_text("❌ Введите число!")
            return
        
        if step == "promo_multiple_count":
            try:
                count = int(text.strip())
                if count <= 0:
                    await update.message.reply_text("❌ Количество должно быть положительным!")
                    return
                admin_state[user_id]["count"] = count
                admin_state[user_id]["step"] = "promo_value"
                await update.message.reply_text(f"📦 Количество: {count}\n\nТеперь введите **цену** каждого скина (число):")
            except ValueError:
                await update.message.reply_text("❌ Введите число!")
            return

    # === БАН ПОЛЬЗОВАТЕЛЯ ===
    if user_id == DEVELOPER_ID and admin_state.get(user_id) == "ban":
        username = text.strip()
        if username.startswith("@"):
            username = username[1:]
        
        target_id = get_user_by_username(username)
        if not target_id:
            await update.message.reply_text(
                f"❌ Игрок @{username} не найден в базе данных!",
                reply_markup=back_button()
            )
            del admin_state[user_id]
            return
        
        if target_id in banned_users:
            banned_users.remove(target_id)
            status = "✅ **Разбанен**"
        else:
            banned_users.add(target_id)
            status = "🛑 **Забанен**"
        
        await update.message.reply_text(
            f"{status}\n\n"
            f"👤 Игрок: @{username}\n"
            f"🆔 ID: {target_id}",
            reply_markup=admin_panel_buttons()
        )
        del admin_state[user_id]
        return

    # === ПРОМОКОДЫ ===
    if user_id in waiting_for_promo and waiting_for_promo[user_id]:
        promo_code = text.upper()
        
        conn = sqlite3.connect("cases_bot.db", timeout=10)
        c = conn.cursor()
        c.execute("SELECT type, value, min, max, count FROM promocodes WHERE code = ?", (promo_code,))
        promo_data = c.fetchone()
        conn.close()
        
        if not promo_data and promo_code not in PROMOCODES:
            await update.message.reply_text(
                f"❌ **Неверный промокод!**\n\n"
                f"Проверьте написание и попробуйте снова.",
                reply_markup=main_menu(user_id),
                parse_mode="Markdown"
            )
            del waiting_for_promo[user_id]
            return
        
        last_promo = get_last_promo(user_id)
        now = datetime.now()
        diff = now - last_promo
        if diff < timedelta(hours=3):
            remaining = timedelta(hours=3) - diff
            hours = remaining.seconds // 3600
            minutes = (remaining.seconds % 3600) // 60
            await update.message.reply_text(
                f"⏳ **Промокод уже активирован!**\n\n"
                f"Следующий промокод можно активировать через:\n"
                f"**{hours} ч {minutes} мин**",
                reply_markup=main_menu(user_id),
                parse_mode="Markdown"
            )
            del waiting_for_promo[user_id]
            return
        
        if promo_data:
            promo_type, value, min_val, max_val, count = promo_data
            result_text = ""
            if promo_type == "balance":
                update_balance(user_id, value)
                result_text = f"💰 +{value} G"
            elif promo_type == "random_balance":
                amount = random.randint(min_val, max_val)
                update_balance(user_id, amount)
                result_text = f"💰 +{amount} G (рандом)"
            elif promo_type == "random_skin":
                skins = ["TEC-9 Tie Dye", "UMP45 Shark", "M110 Transition", "Sticker Fingerprint", "Charm Hoplit Helmet", "M4A1 Stainless", "Desert Eagle Eclipse", "Akimbo Uzi Zenith", "Sticker Minotaur"]
                skin_name = random.choice(skins)
                price = random.randint(min_val, max_val)
                add_item(user_id, skin_name, price, "Обычный", "Оружие", "Промокод")
                result_text = f"🎁 Получен скин: {skin_name} ({price} G)"
            elif promo_type == "skin_fixed":
                skins = ["TEC-9 Tie Dye", "UMP45 Shark", "M110 Transition", "Sticker Fingerprint", "Charm Hoplit Helmet", "M4A1 Stainless"]
                skin_name = random.choice(skins)
                add_item(user_id, skin_name, value, "Обычный", "Оружие", "Промокод")
                result_text = f"🎁 Получен скин: {skin_name} ({value} G)"
            elif promo_type == "multiple_skins":
                skins_list = []
                skins = ["TEC-9 Tie Dye", "UMP45 Shark", "M110 Transition", "Sticker Fingerprint", "Charm Hoplit Helmet", "M4A1 Stainless"]
                for _ in range(count):
                    skin_name = random.choice(skins)
                    add_item(user_id, skin_name, value, "Обычный", "Оружие", "Промокод")
                    skins_list.append(f"{skin_name} ({value} G)")
                result_text = f"🎁 Получено {count} скина:\n" + "\n".join(skins_list)
        else:
            promo = PROMOCODES[promo_code]
            result_text = ""
            if promo["type"] == "balance":
                update_balance(user_id, promo["value"])
                result_text = f"💰 +{promo['value']} G"
            elif promo["type"] == "random_balance":
                amount = random.randint(promo["min"], promo["max"])
                update_balance(user_id, amount)
                result_text = f"💰 +{amount} G (рандом)"
            elif promo["type"] == "random_skin":
                skins = ["TEC-9 Tie Dye", "UMP45 Shark", "M110 Transition", "Sticker Fingerprint", "Charm Hoplit Helmet", "M4A1 Stainless", "Desert Eagle Eclipse", "Akimbo Uzi Zenith", "Sticker Minotaur"]
                skin_name = random.choice(skins)
                price = random.randint(promo["min"], promo["max"])
                add_item(user_id, skin_name, price, "Обычный", "Оружие", "Промокод")
                result_text = f"🎁 Получен скин: {skin_name} ({price} G)"
            elif promo["type"] == "skin_fixed":
                skins = ["TEC-9 Tie Dye", "UMP45 Shark", "M110 Transition", "Sticker Fingerprint", "Charm Hoplit Helmet", "M4A1 Stainless"]
                skin_name = random.choice(skins)
                add_item(user_id, skin_name, promo["value"], "Обычный", "Оружие", "Промокод")
                result_text = f"🎁 Получен скин: {skin_name} ({promo['value']} G)"
            elif promo["type"] == "multiple_skins":
                skins_list = []
                skins = ["TEC-9 Tie Dye", "UMP45 Shark", "M110 Transition", "Sticker Fingerprint", "Charm Hoplit Helmet", "M4A1 Stainless"]
                for _ in range(promo["count"]):
                    skin_name = random.choice(skins)
                    add_item(user_id, skin_name, promo["value"], "Обычный", "Оружие", "Промокод")
                    skins_list.append(f"{skin_name} ({promo['value']} G)")
                result_text = f"🎁 Получено {promo['count']} скина:\n" + "\n".join(skins_list)
        
        update_last_promo(user_id)
        new_balance = get_balance(user_id)
        
        await update.message.reply_text(
            f"✅ **Промокод активирован!**\n\n"
            f"🎫 Код: `{promo_code}`\n"
            f"📦 Результат: {result_text}\n"
            f"💰 **Баланс:** {new_balance} G\n\n"
            f"⏳ Следующий промокод можно активировать через 3 часа.",
            reply_markup=back_button(),
            parse_mode="Markdown"
        )
        
        add_log(user_id, "Промокод", 0, f"{promo_code} -> {result_text}")
        del waiting_for_promo[user_id]
        return
    
    # === АДМИН: ЛОГИ ===
    if user_id == DEVELOPER_ID and user_id in admin_state and admin_state[user_id] == "logs":
        username = text.strip()
        if username.startswith("@"):
            username = username[1:]
        target_id = get_user_by_username(username)
        if not target_id:
            await update.message.reply_text(
                f"❌ Игрок @{username} не найден в базе данных!",
                reply_markup=back_button()
            )
            del admin_state[user_id]
            return
        logs = get_user_logs(target_id)
        if not logs:
            text = f"📋 **Логи игрока @{username}**\n\nНет записей."
        else:
            text = f"📋 **Логи игрока @{username}**\n\n"
            for action, amount, details, date in logs[:30]:
                text += f"📅 {date}\n{action}"
                if amount:
                    text += f" ({amount} G)"
                if details:
                    text += f" — {details}"
                text += "\n\n"
        await update.message.reply_text(
            text,
            reply_markup=back_button(),
            parse_mode="Markdown"
        )
        del admin_state[user_id]
        return
    
    # === АДМИН: РАССЫЛКА ===
    if user_id == DEVELOPER_ID and user_id in admin_state and admin_state[user_id] == "broadcast":
        broadcast_text = text
        users = get_all_users()
        success = 0
        fail = 0
        
        await update.message.reply_text(
            f"📢 **Начинаю рассылку...**\n\n"
            f"👥 Всего пользователей: {len(users)}\n"
            f"⏳ Это может занять некоторое время.",
            parse_mode="Markdown"
        )
        
        for uid in users:
            try:
                await context.bot.send_message(
                    chat_id=uid,
                    text=f"📢 **Сообщение от администрации:**\n\n"
                         f"{broadcast_text}",
                    parse_mode="Markdown"
                )
                success += 1
            except:
                fail += 1
            await asyncio.sleep(0.05)
        
        await update.message.reply_text(
            f"✅ **Рассылка завершена!**\n\n"
            f"📤 Отправлено: {success}\n"
            f"❌ Не доставлено: {fail}",
            reply_markup=admin_panel_buttons()
        )
        del admin_state[user_id]
        return
    
    # === ПОДДЕРЖКА ===
    if user_id in support_requests and support_requests[user_id].get("step") == "question":
        question_text = text
        username = update.effective_user.username or "без юзернейма"
        
        try:
            await context.bot.send_message(
                chat_id=DEVELOPER_ID,
                text=f"📩 **НОВЫЙ ВОПРОС В ПОДДЕРЖКУ**\n\n"
                     f"👤 От: @{username}\n"
                     f"🆔 ID: {user_id}\n\n"
                     f"📝 **Вопрос:**\n"
                     f"{question_text}",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("✏️ Ответить", callback_data=f"reply_{user_id}")]
                ]),
                parse_mode="Markdown"
            )
            await update.message.reply_text(
                f"✅ **Ваш вопрос отправлен!**\n\n"
                f"Администратор свяжется с вами в ближайшее время. 📩",
                reply_markup=main_menu(user_id)
            )
        except Exception as e:
            await update.message.reply_text(
                f"❌ Ошибка при отправке вопроса. Попробуйте позже.",
                reply_markup=main_menu(user_id)
            )
            print(f"Ошибка отправки вопроса: {e}")
        
        del support_requests[user_id]
        return
    
    if user_id == DEVELOPER_ID and user_id in support_requests and support_requests[user_id].get("step") == "replying":
        target_id = support_requests[user_id]["target_id"]
        reply_text = text
        
        try:
            await context.bot.send_message(
                chat_id=target_id,
                text=f"🛠 **Ответ от администрации:**\n\n"
                     f"{reply_text}",
                parse_mode="Markdown"
            )
            await update.message.reply_text(
                f"✅ **Ответ отправлен!**\n\n"
                f"Сообщение доставлено игроку.",
                reply_markup=main_menu(user_id)
            )
        except Exception as e:
            await update.message.reply_text(
                f"❌ Ошибка при отправке ответа:\n{str(e)}",
                reply_markup=main_menu(user_id)
            )
        
        del support_requests[user_id]
        return
    
    # === КОЛЛАБОРАЦИЯ ===
    if user_id in waiting_for_collab and waiting_for_collab[user_id]:
        try:
            await context.bot.send_message(
                chat_id=DEVELOPER_ID,
                text=f"📩 **НОВАЯ АНКЕТА!**\n\n"
                     f"👤 От: @{update.effective_user.username or 'без юзернейма'}\n"
                     f"🆔 ID: {user_id}\n\n"
                     f"📝 **Ответы:**\n\n"
                     f"{text}",
                parse_mode="Markdown"
            )
            await update.message.reply_text(
                f"✅ **Анкета отправлена!**\n\n"
                f"Спасибо за проявленный интерес! Мы свяжемся с вами в ближайшее время. 🍀",
                reply_markup=main_menu(user_id)
            )
        except Exception as e:
            await update.message.reply_text(
                f"❌ Ошибка при отправке анкеты. Попробуйте позже.",
                reply_markup=main_menu(user_id)
            )
            print(f"Ошибка отправки анкеты: {e}")
        
        del waiting_for_collab[user_id]
        return
    
    # === ПОПОЛНЕНИЕ ПЕРЕВОДОМ ===
    if user_id in waiting_for_transfer and waiting_for_transfer[user_id]:
        try:
            amount = int(text.strip())
            if amount < 10 or amount > 10000:
                await update.message.reply_text(
                    f"❌ Сумма должна быть от 10 до 10000 ₽!",
                    reply_markup=main_menu(user_id)
                )
                del waiting_for_transfer[user_id]
                return
            
            await update.message.reply_text(
                f"💸 **Вы выбрали пополнение баланса переводом**\n\n"
                f"🟢 Переведите пожалуйста **{amount} ₽** на карту:\n"
                f"`2202 2084 4242 2847`\n"
                f"(Андрей Алексеевич Л.)\n\n"
                f"♥️ После перевода ожидайте. В течение 10 минут голда поступит на ваш баланс.",
                reply_markup=back_button(),
                parse_mode="Markdown"
            )
            
            try:
                username = update.effective_user.username or "без юзернейма"
                await context.bot.send_message(
                    chat_id=DEVELOPER_ID,
                    text=f"💳 **ЗАЯВКА НА ПОПОЛНЕНИЕ**\n\n"
                         f"👤 Игрок: @{username}\n"
                         f"💰 Сумма: {amount} ₽\n"
                         f"📌 Способ: Перевод на карту\n"
                         f"⏳ Статус: Ожидает оплаты",
                    parse_mode="Markdown"
                )
            except:
                pass
            
            del waiting_for_transfer[user_id]
            return
            
        except ValueError:
            await update.message.reply_text(
                f"❌ Введите число!",
                reply_markup=main_menu(user_id)
            )
            del waiting_for_transfer[user_id]
            return
    
    # === РАЗРАБОТЧИК: ПОПОЛНИТЬ ИГРОКА ===
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
    
    # === МИНЫ / ФОРТУНА (СТАВКИ) ===
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
        add_log(user_id, "Ставка в мины", bet)
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
        add_log(user_id, "Проигрыш в минах", game["bet"])
        return
    mines_count = game["mines_count"]
    multiplier = MINE_MULTIPLIERS.get(mines_count, 1.0)
    if is_vip(user_id):
        multiplier = get_vip_mine_multiplier(multiplier)
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
    
    add_log(user_id, "Выигрыш в минах", win)
    
    update_user_stats(user_id, "mines_wins", 1)
    
    stats = get_user_stats(user_id)
    if stats["mines_wins"] == 10 and not check_achievement(user_id, "mines_win_10"):
        claim_achievement(user_id, "mines_win_10")
        update_balance(user_id, 50)
        await query.edit_message_text(
            f"💰 **Вы забрали выигрыш!**\n\n"
            f"🏆 Выигрыш: {win} G\n"
            f"💳 Новый баланс: {new_balance} G\n\n"
            f"🏅 **ДОСТИЖЕНИЕ РАЗБЛОКИРОВАНО!**\n"
            f"💣 Победитель мин — +50 G!",
            reply_markup=back_button(),
            parse_mode="Markdown"
        )
        del mines_data[user_id]
        return
    
    referral_info = check_referral_bonus(user_id)
    if referral_info and referral_info["bonus_claimed"] == 1:
        conn = sqlite3.connect("cases_bot.db", timeout=10)
        c = conn.cursor()
        c.execute("SELECT bonus_claimed FROM referrals WHERE referral_id = ? AND bonus_claimed = 1", (user_id,))
        result = c.fetchone()
        conn.close()
        
        if result:
            conn = sqlite3.connect("cases_bot.db", timeout=10)
            c = conn.cursor()
            c.execute("SELECT referrer_id FROM referrals WHERE referral_id = ?", (user_id,))
            ref_result = c.fetchone()
            conn.close()
            
            if ref_result:
                referrer_id = ref_result[0]
                conn = sqlite3.connect("cases_bot.db", timeout=10)
                c = conn.cursor()
                c.execute("SELECT bonus_claimed FROM referrals WHERE referral_id = ? AND bonus_claimed = 2", (user_id,))
                result = c.fetchone()
                conn.close()
                
                if not result:
                    update_balance(referrer_id, 10)
                    conn = sqlite3.connect("cases_bot.db", timeout=10)
                    c = conn.cursor()
                    c.execute("UPDATE referrals SET bonus_claimed = 2 WHERE referral_id = ?", (user_id,))
                    conn.commit()
                    conn.close()
                    
                    try:
                        await context.bot.send_message(
                            chat_id=referrer_id,
                            text=f"🎉 **Реферальный бонус!**\n\n"
                                 f"Ваш друг выполнил условия!\n"
                                 f"💰 Вы получили +10 G!",
                            parse_mode="Markdown"
                        )
                    except:
                        pass
    
    del mines_data[user_id]
    
    await query.edit_message_text(
        f"💰 **Вы забрали выигрыш!**\n\n"
        f"🏆 Выигрыш: {win} G\n"
        f"💳 Новый баланс: {new_balance} G\n\n"
        f"Сыграем ещё?",
        reply_markup=back_button(),
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
            f"✅ **Баланс пополнен на {amount} G.**\n\n"
            f"💰 **Текущий баланс:** {new_balance} G",
            parse_mode="Markdown"
        )
    except (IndexError, ValueError):
        await update.message.reply_text("❌ Использование: /add_balance <сумма>")

def save_promo_to_db(update, context, data):
    code = data["code"]
    promo_type = data["type"]
    
    conn = sqlite3.connect("cases_bot.db", timeout=10)
    c = conn.cursor()
    
    c.execute("SELECT id FROM promocodes WHERE code = ?", (code,))
    if c.fetchone():
        update.message.reply_text(
            f"❌ **Промокод `{code}` уже существует!**\n\n"
            f"Придумайте другой код.",
            reply_markup=admin_panel_buttons(),
            parse_mode="Markdown"
        )
        conn.close()
        return
    
    if promo_type == "balance":
        c.execute("INSERT INTO promocodes (code, type, value, created_by, created_date) VALUES (?, ?, ?, ?, ?)",
                  (code, promo_type, data["value"], update.effective_user.id, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    elif promo_type == "random_balance":
        c.execute("INSERT INTO promocodes (code, type, min, max, created_by, created_date) VALUES (?, ?, ?, ?, ?, ?)",
                  (code, promo_type, data["min"], data["max"], update.effective_user.id, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    elif promo_type == "random_skin":
        c.execute("INSERT INTO promocodes (code, type, min, max, created_by, created_date) VALUES (?, ?, ?, ?, ?, ?)",
                  (code, promo_type, data["min"], data["max"], update.effective_user.id, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    elif promo_type == "skin_fixed":
        c.execute("INSERT INTO promocodes (code, type, value, created_by, created_date) VALUES (?, ?, ?, ?, ?)",
                  (code, promo_type, data["value"], update.effective_user.id, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    elif promo_type == "multiple_skins":
        c.execute("INSERT INTO promocodes (code, type, value, count, created_by, created_date) VALUES (?, ?, ?, ?, ?, ?)",
                  (code, promo_type, data["value"], data["count"], update.effective_user.id, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    
    conn.commit()
    conn.close()
    
    update.message.reply_text(
        f"✅ **Промокод создан!**\n\n"
        f"🎫 Код: `{code}`\n"
        f"📦 Тип: {promo_type}\n"
        f"📌 Создан: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        f"Теперь игроки могут его активировать!",
        reply_markup=admin_panel_buttons(),
        parse_mode="Markdown"
    )

def main():
    init_db()
    print("🚀 Бот запущен...")
    print(f"👤 ID разработчика: {DEVELOPER_ID}")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add_balance", add_balance_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    
    loop = asyncio.get_event_loop()
    loop.create_task(backup_scheduler())
    
    print("✅ Бот готов к работе!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()