# =========================================
# SNAKE ENGINE PREMIUM SHOP BOT
# CLEAN ADVANCED VERSION
# PYTHON TELEGRAM BOT v21+
# =========================================

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    ConversationHandler,
    filters
)

import warnings

from telegram.warnings import PTBUserWarning

warnings.filterwarnings(
    action="ignore",
    message=r".*CallbackQueryHandler.*",
    category=PTBUserWarning
)

import json
import os
import qrcode

from io import BytesIO

# =========================================
# BOT SETTINGS
# =========================================

BOT_TOKEN = "8765454987:AAEqYrQijpMveIn4lKQsf9WsId4FPcAKgEU"

ADMIN_ID = 8515307600

UPI_ID = "mdmaruf009@fam"

BOT_USERNAME = "@snakeeengine_bot"

DATA_FILE = "users.json"

# =========================================
# CONVERSATION STATES
# =========================================

WAIT_CUSTOM_AMOUNT = 1
WAIT_UTR = 2

ADD_AMOUNT = 3
ADD_KEYS = 4

# =========================================
# LOAD / SAVE SYSTEM
# =========================================

def load_data():

    if not os.path.exists(DATA_FILE):

        return {}

    try:

        with open(DATA_FILE, "r") as f:

            return json.load(f)

    except:

        return {}

def save_data(data):

    with open(DATA_FILE, "w") as f:

        json.dump(data, f, indent=4)

# =========================================
# LOAD DATABASE
# =========================================

users = load_data()

# =========================================
# KEY DATABASE
# =========================================

KEYS = {

    "8BP": {
        "3": [],
        "10": [],
        "30": [],
        "90": []
    },

    "Carrom": {
        "3": [],
        "10": [],
        "30": [],
        "90": []
    },

    "Soccer": {
        "3": [],
        "10": [],
        "30": [],
        "90": []
    }

}

# =========================================
# PRICES
# =========================================

PRICES = {

    "8BP": {
        "3": 400,
        "10": 1000,
        "30": 2000,
        "90": 3500
    },

    "Carrom": {
        "3": 180,
        "10": 380,
        "30": 850,
        "90": 1900
    },

    "Soccer": {
        "3": 140,
        "10": 340,
        "30": 600,
        "90": 1500
    }

}

# =========================================
# CREATE USER
# =========================================

def create_user(user):

    uid = str(user.id)

    if uid not in users:

        users[uid] = {

            "balance": 0,
            "referrals": 0,
            "keys_bought": 0,
            "history": []

        }

        save_data(users)
        
        # =========================================
# MAIN MENU
# =========================================

def main_menu(user_id):

    keyboard = [

        [
            InlineKeyboardButton(
                "💰 Deposit",
                callback_data="deposit"
            ),

            InlineKeyboardButton(
                "💳 Balance",
                callback_data="balance"
            )
        ],

        [
            InlineKeyboardButton(
                "👥 Referral",
                callback_data="refer"
            ),

            InlineKeyboardButton(
                "🛒 Buy Key",
                callback_data="buy"
            )
        ],

        [
            InlineKeyboardButton(
                "👤 Profile",
                callback_data="profile"
            ),

            InlineKeyboardButton(
                "📦 Stock",
                callback_data="stock"
            )
        ],

        [
            InlineKeyboardButton(
                "📥 Download",
                callback_data="download"
            ),

            InlineKeyboardButton(
                "🆘 Support",
                callback_data="support"
            )
        ]

    ]

    # ADMIN BUTTONS
    if user_id == ADMIN_ID:

        keyboard.append([

            InlineKeyboardButton(
                "➕ Add Keys",
                callback_data="admin_add"
            )

        ])

        keyboard.append([

            InlineKeyboardButton(
                "📊 Dashboard",
                callback_data="dashboard"
            )

        ])

    return InlineKeyboardMarkup(keyboard)

# =========================================
# START
# =========================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    create_user(user)

    text = f"""
🔥 WELCOME TO SNAKE ENGINE 🔥

👤 Name :
{user.first_name}

🆔 User ID :
{user.id}

⚡ PREMIUM KEY SHOP
"""

    await update.message.reply_text(
        text,
        reply_markup=main_menu(user.id)
    )

# =========================================
# BACK MAIN MENU
# =========================================

async def back(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    await query.message.edit_text(
        "🏠 MAIN MENU",
        reply_markup=main_menu(query.from_user.id)
    )

# =========================================
# DEPOSIT MENU
# =========================================

async def deposit(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    text = """
💰 DEPOSIT BALANCE

✅ Minimum : ₹10
✅ Maximum : ₹5000

Select Amount Below
"""

    keyboard = [

        [
            InlineKeyboardButton(
                "₹100",
                callback_data="pay_100"
            ),

            InlineKeyboardButton(
                "₹200",
                callback_data="pay_200"
            )
        ],

        [
            InlineKeyboardButton(
                "₹500",
                callback_data="pay_500"
            ),

            InlineKeyboardButton(
                "₹1000",
                callback_data="pay_1000"
            )
        ],

        [
            InlineKeyboardButton(
                "💵 Custom Amount",
                callback_data="custom_amount"
            )
        ],

        [
            InlineKeyboardButton(
                "🔙 Back",
                callback_data="back"
            )
        ]

    ]

    await query.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    
    # =========================================
# GENERATE QR
# =========================================

async def generate_qr(message, amount):

    upi_link = (
        f"upi://pay?pa={UPI_ID}"
        f"&pn=SnakeEngine"
        f"&am={amount}"
        f"&cu=INR"
    )

    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5
    )

    qr.add_data(upi_link)

    qr.make(fit=True)

    img = qr.make_image(
        fill_color="black",
        back_color="white"
    )

    bio = BytesIO()

    bio.name = "payment.png"

    img.save(bio, "PNG")

    bio.seek(0)

    keyboard = [

        [
            InlineKeyboardButton(
                "✅ Confirm Payment",
                callback_data=f"confirm_{amount}"
            )
        ],

        [
            InlineKeyboardButton(
                "🔙 Back",
                callback_data="deposit"
            )
        ]

    ]

    caption = f"""
💳 PAYMENT QR

💰 Amount :
₹{amount}

📲 Scan & Pay

⚠️ After Payment Click Confirm
"""

    await message.reply_photo(
        photo=bio,
        caption=caption,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# =========================================
# PAYMENT BUTTONS
# =========================================

async def pay_100(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    await generate_qr(query.message, 100)

async def pay_200(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    await generate_qr(query.message, 200)

async def pay_500(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    await generate_qr(query.message, 500)

async def pay_1000(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    await generate_qr(query.message, 1000)

# =========================================
# CUSTOM AMOUNT
# =========================================

async def custom_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    await query.message.reply_text(
        """
💵 SEND CUSTOM AMOUNT

Example:
350
"""
    )

    return WAIT_CUSTOM_AMOUNT

# =========================================
# RECEIVE CUSTOM AMOUNT
# =========================================

async def custom_amount_receive(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

        amount = int(update.message.text)

    except:

        await update.message.reply_text(
            "❌ SEND VALID NUMBER"
        )

        return WAIT_CUSTOM_AMOUNT

    if amount < 10 or amount > 5000:

        await update.message.reply_text(
            "❌ LIMIT ₹10 - ₹5000"
        )

        return WAIT_CUSTOM_AMOUNT

    await generate_qr(update.message, amount)

    return ConversationHandler.END
    
    # =========================================
# CONFIRM PAYMENT
# =========================================

async def confirm_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    amount = query.data.split("_")[1]

    context.user_data["deposit_amount"] = amount

    await query.message.reply_text(
        """
🧾 SEND YOUR UTR NUMBER

Example:
324567891234
"""
    )

    return WAIT_UTR

# =========================================
# RECEIVE UTR
# =========================================

async def receive_utr(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    utr = update.message.text.strip()

    amount = context.user_data.get("deposit_amount")

    if not amount:

        await update.message.reply_text(
            "❌ SESSION EXPIRED"
        )

        return ConversationHandler.END

    await update.message.reply_text(
        """
✅ PAYMENT SUBMITTED

⏳ WAIT FOR ADMIN APPROVAL
"""
    )

    admin_text = f"""
💰 NEW PAYMENT REQUEST

👤 Name :
{user.first_name}

🆔 User ID :
{user.id}

💵 Amount :
₹{amount}

🧾 UTR :
{utr}
"""

    keyboard = [

        [
            InlineKeyboardButton(
                "✅ APPROVE",
                callback_data=f"approve_{user.id}_{amount}"
            )
        ]

    ]

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=admin_text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

    return ConversationHandler.END

# =========================================
# APPROVE PAYMENT
# =========================================

async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    try:

        data = query.data.split("_")

        user_id = str(data[1])

        amount = int(data[2])

        # CREATE USER
        if user_id not in users:

            users[user_id] = {

                "balance": 0,
                "referrals": 0,
                "keys_bought": 0,
                "history": []

            }

        users[user_id]["balance"] += amount

        users[user_id]["history"].append(
            f"Deposit ₹{amount}"
        )

        save_data(users)

        # SEND USER MESSAGE
        await context.bot.send_message(
            chat_id=int(user_id),
            text=f"""
✅ PAYMENT APPROVED

💰 Added :
₹{amount}

💳 Wallet Updated
"""
        )

        # EDIT ADMIN MESSAGE
        await query.message.edit_text(
            f"""
✅ PAYMENT APPROVED

👤 User :
{user_id}

💰 Amount :
₹{amount}
"""
        )

    except Exception as e:

        print(e)

        await query.message.edit_text(
            f"❌ ERROR\n\n{e}"
        )
        
        # =========================================
# BALANCE
# =========================================

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    uid = str(query.from_user.id)

    bal = users[uid]["balance"]

    text = f"""
💳 YOUR BALANCE

💰 Balance :
₹{bal}
"""

    keyboard = [

        [
            InlineKeyboardButton(
                "🔙 Back",
                callback_data="back"
            )
        ]

    ]

    await query.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# =========================================
# PROFILE
# =========================================

async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    uid = str(query.from_user.id)

    data = users[uid]

    history = "\n".join(
        data["history"][-5:]
    )

    if history == "":

        history = "NO HISTORY"

    text = f"""
👤 PROFILE

🆔 ID :
{query.from_user.id}

👤 Name :
{query.from_user.first_name}

💰 Balance :
₹{data['balance']}

👥 Referrals :
{data['referrals']}

🛒 Keys Bought :
{data['keys_bought']}

📜 RECENT HISTORY

{history}
"""

    keyboard = [

        [
            InlineKeyboardButton(
                "🔙 Back",
                callback_data="back"
            )
        ]

    ]

    await query.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# =========================================
# BUY MENU
# =========================================

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    keyboard = [

        [
            InlineKeyboardButton(
                "🎱 8 Ball Pool",
                callback_data="game_8BP"
            )
        ],

        [
            InlineKeyboardButton(
                "🎯 Carrom",
                callback_data="game_Carrom"
            )
        ],

        [
            InlineKeyboardButton(
                "⚽ Soccer",
                callback_data="game_Soccer"
            )
        ],

        [
            InlineKeyboardButton(
                "🔙 Back",
                callback_data="back"
            )
        ]

    ]

    await query.message.edit_text(
        "🎮 SELECT GAME",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    
    # =========================================
# GAME MENU
# =========================================

async def game_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    game = query.data.replace("game_", "")

    keyboard = [

        [
            InlineKeyboardButton(
                f"3 Days ₹{PRICES[game]['3']}",
                callback_data=f"buykey_{game}_3"
            )
        ],

        [
            InlineKeyboardButton(
                f"10 Days ₹{PRICES[game]['10']}",
                callback_data=f"buykey_{game}_10"
            )
        ],

        [
            InlineKeyboardButton(
                f"30 Days ₹{PRICES[game]['30']}",
                callback_data=f"buykey_{game}_30"
            )
        ],

        [
            InlineKeyboardButton(
                f"90 Days ₹{PRICES[game]['90']}",
                callback_data=f"buykey_{game}_90"
            )
        ],

        [
            InlineKeyboardButton(
                "🔙 Back",
                callback_data="buy"
            )
        ]

    ]

    await query.message.edit_text(
        f"""
🎮 {game}

📦 SELECT PLAN
""",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# =========================================
# BUY KEY
# =========================================

async def buy_key(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    data = query.data.split("_")

    game = data[1]

    days = data[2]

    uid = str(query.from_user.id)

    # PRICE
    price = PRICES[game][days]

    # USER BALANCE
    balance = users[uid]["balance"]

    # CHECK BALANCE
    if balance < price:

        await query.message.reply_text(
            "❌ INSUFFICIENT BALANCE"
        )

        return

    # CHECK STOCK
    if len(KEYS[game][days]) == 0:

        await query.message.reply_text(
            "❌ OUT OF STOCK"
        )

        return

    # GET KEY
    key = KEYS[game][days].pop(0)

    # CUT BALANCE
    users[uid]["balance"] -= price

    # UPDATE DATA
    users[uid]["keys_bought"] += 1

    # SAVE HISTORY
    users[uid]["history"].append(
        f"Bought {game} {days} Days Key"
    )

    # SAVE DATABASE
    save_data(users)

    # SEND KEY
    await query.message.reply_text(
        f"""
✅ PURCHASE SUCCESSFUL

🎮 GAME :
{game}

📅 VALIDITY :
{days} Days

🔑 YOUR KEY :

`{key}`

⚠️ DON'T SHARE THIS KEY
""",
        parse_mode="Markdown"
    )
    
    # =========================================
# STOCK STATUS
# =========================================

async def stock(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    text = f"""
📦 LIVE STOCK

🎱 8BP
3 Days : {len(KEYS['8BP']['3'])}
10 Days : {len(KEYS['8BP']['10'])}
30 Days : {len(KEYS['8BP']['30'])}
90 Days : {len(KEYS['8BP']['90'])}

🎯 Carrom
3 Days : {len(KEYS['Carrom']['3'])}
10 Days : {len(KEYS['Carrom']['10'])}
30 Days : {len(KEYS['Carrom']['30'])}
90 Days : {len(KEYS['Carrom']['90'])}

⚽ Soccer
3 Days : {len(KEYS['Soccer']['3'])}
10 Days : {len(KEYS['Soccer']['10'])}
30 Days : {len(KEYS['Soccer']['30'])}
90 Days : {len(KEYS['Soccer']['90'])}
"""

    keyboard = [

        [
            InlineKeyboardButton(
                "🔙 Back",
                callback_data="back"
            )
        ]

    ]

    await query.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# =========================================
# ADMIN ADD KEYS
# =========================================

async def admin_add(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    if query.from_user.id != ADMIN_ID:
        return

    keyboard = [

        [
            InlineKeyboardButton(
                "🎱 8 Ball Pool",
                callback_data="add_8BP"
            )
        ],

        [
            InlineKeyboardButton(
                "🎯 Carrom",
                callback_data="add_Carrom"
            )
        ],

        [
            InlineKeyboardButton(
                "⚽ Soccer",
                callback_data="add_Soccer"
            )
        ]

    ]

    await query.message.edit_text(
        "🎮 SELECT GAME",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# =========================================
# SELECT GAME
# =========================================

async def select_add_game(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    game = query.data.replace("add_", "")

    context.user_data["add_game"] = game

    keyboard = [

        [
            InlineKeyboardButton(
                "3 Days",
                callback_data="days_3"
            )
        ],

        [
            InlineKeyboardButton(
                "10 Days",
                callback_data="days_10"
            )
        ],

        [
            InlineKeyboardButton(
                "30 Days",
                callback_data="days_30"
            )
        ],

        [
            InlineKeyboardButton(
                "90 Days",
                callback_data="days_90"
            )
        ]

    ]

    await query.message.edit_text(
        f"""
🎮 GAME :
{game}

📅 SELECT VALIDITY
""",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    
    # =========================================
# SELECT DAYS
# =========================================

async def select_days(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    days = query.data.replace("days_", "")

    context.user_data["add_days"] = days

    await query.message.reply_text(
        """
📦 HOW MANY KEYS YOU WANT TO ADD?

Example:
10
20
50
"""
    )

    return ADD_AMOUNT

# =========================================
# RECEIVE AMOUNT
# =========================================

async def receive_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

        amount = int(update.message.text)

    except:

        await update.message.reply_text(
            "❌ SEND VALID NUMBER"
        )

        return ADD_AMOUNT

    context.user_data["add_amount"] = amount

    await update.message.reply_text(
        f"""
✅ NOW SEND {amount} KEYS

⚠️ ONE KEY PER LINE

Example:

KEY-111
KEY-222
KEY-333
"""
    )

    return ADD_KEYS

# =========================================
# RECEIVE KEYS
# =========================================

async def receive_keys(update: Update, context: ContextTypes.DEFAULT_TYPE):

    game = context.user_data.get("add_game")

    days = context.user_data.get("add_days")

    amount = context.user_data.get("add_amount")

    text = update.message.text.strip()

    keys = text.splitlines()

    # CHECK COUNT
    if len(keys) != amount:

        await update.message.reply_text(
            f"""
❌ WRONG KEY COUNT

📦 REQUIRED :
{amount}

📥 SENT :
{len(keys)}
"""
        )

        return ADD_KEYS

    # ADD KEYS
    KEYS[game][days].extend(keys)

    total = len(KEYS[game][days])

    await update.message.reply_text(
        f"""
✅ KEYS ADDED

🎮 Game :
{game}

📅 Validity :
{days} Days

📦 Added :
{len(keys)}

📦 Total Stock :
{total}
"""
    )

    return ConversationHandler.END
    
    # =========================================
# DOWNLOAD
# =========================================

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    keyboard = [

        [
            InlineKeyboardButton(
                "📥 DOWNLOAD APP",
                url="https://t.me/SnakeEngine"
            )
        ],

        [
            InlineKeyboardButton(
                "🔙 Back",
                callback_data="back"
            )
        ]

    ]

    await query.message.edit_text(
        """
📥 DOWNLOAD APP

CLICK BUTTON BELOW
""",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# =========================================
# SUPPORT
# =========================================

async def support(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    keyboard = [

        [
            InlineKeyboardButton(
                "📞 CONTACT SUPPORT",
                url="https://t.me/Helpsupport123456"
            )
        ],

        [
            InlineKeyboardButton(
                "🔙 Back",
                callback_data="back"
            )
        ]

    ]

    await query.message.edit_text(
        """
🆘 HELP & SUPPORT

• Payment Problem
• Key Problem
• Other Problem
""",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# =========================================
# REFERRAL
# =========================================

async def refer(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    uid = query.from_user.id

    ref_link = f"https://t.me/{BOT_USERNAME}?start={uid}"

    keyboard = [

        [
            InlineKeyboardButton(
                "🔙 Back",
                callback_data="back"
            )
        ]

    ]

    await query.message.edit_text(
        f"""
👥 REFERRAL PROGRAM

🎁 INVITE FRIENDS & EARN

🔗 YOUR REFERRAL LINK

{ref_link}
""",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    
    # =========================================
# ADMIN DASHBOARD
# =========================================

async def dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    if query.from_user.id != ADMIN_ID:
        return

    total_users = len(users)

    total_balance = 0

    total_keys = 0

    for uid in users:

        total_balance += users[uid]["balance"]

        total_keys += users[uid]["keys_bought"]

    text = f"""
📊 ADMIN DASHBOARD

👥 Total Users :
{total_users}

💰 Total Wallet Balance :
₹{total_balance}

🛒 Total Keys Sold :
{total_keys}

📦 LIVE STOCK

🎱 8BP :
{sum(len(KEYS['8BP'][d]) for d in KEYS['8BP'])}

🎯 Carrom :
{sum(len(KEYS['Carrom'][d]) for d in KEYS['Carrom'])}

⚽ Soccer :
{sum(len(KEYS['Soccer'][d]) for d in KEYS['Soccer'])}
"""

    keyboard = [

        [
            InlineKeyboardButton(
                "➕ Add Keys",
                callback_data="admin_add"
            )
        ],

        [
            InlineKeyboardButton(
                "🔙 Back",
                callback_data="back"
            )
        ]

    ]

    await query.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# =========================================
# ERROR HANDLER
# =========================================

async def error_handler(update, context):

    print("ERROR:")
    print(context.error)

# =========================================
# CREATE BOT
# =========================================

app = ApplicationBuilder().token(BOT_TOKEN).build()

# =========================================
# COMMAND HANDLERS
# =========================================

app.add_handler(
    CommandHandler(
        "start",
        start
    )
)

# =========================================
# BUTTON HANDLERS
# =========================================

app.add_handler(
    CallbackQueryHandler(
        back,
        pattern="^back$"
    )
)

app.add_handler(
    CallbackQueryHandler(
        deposit,
        pattern="^deposit$"
    )
)

app.add_handler(
    CallbackQueryHandler(
        pay_100,
        pattern="^pay_100$"
    )
)

app.add_handler(
    CallbackQueryHandler(
        pay_200,
        pattern="^pay_200$"
    )
)

app.add_handler(
    CallbackQueryHandler(
        pay_500,
        pattern="^pay_500$"
    )
)

app.add_handler(
    CallbackQueryHandler(
        pay_1000,
        pattern="^pay_1000$"
    )
)

app.add_handler(
    CallbackQueryHandler(
        approve,
        pattern="^approve_"
    )
)

app.add_handler(
    CallbackQueryHandler(
        balance,
        pattern="^balance$"
    )
)

app.add_handler(
    CallbackQueryHandler(
        buy,
        pattern="^buy$"
    )
)

app.add_handler(
    CallbackQueryHandler(
        game_menu,
        pattern="^game_(8BP|Carrom|Soccer)$"
    )
)

app.add_handler(
    CallbackQueryHandler(
        buy_key,
        pattern="^buykey_"
    )
)

app.add_handler(
    CallbackQueryHandler(
        profile,
        pattern="^profile$"
    )
)

app.add_handler(
    CallbackQueryHandler(
        stock,
        pattern="^stock$"
    )
)

app.add_handler(
    CallbackQueryHandler(
        download,
        pattern="^download$"
    )
)

app.add_handler(
    CallbackQueryHandler(
        support,
        pattern="^support$"
    )
)

app.add_handler(
    CallbackQueryHandler(
        refer,
        pattern="^refer$"
    )
)

app.add_handler(
    CallbackQueryHandler(
        dashboard,
        pattern="^dashboard$"
    )
)

app.add_handler(
    CallbackQueryHandler(
        admin_add,
        pattern="^admin_add$"
    )
)

app.add_handler(
    CallbackQueryHandler(
        select_add_game,
        pattern="^add_"
    )
)

# =========================================
# CUSTOM AMOUNT CONVERSATION
# =========================================

custom_conv = ConversationHandler(

    entry_points=[

        CallbackQueryHandler(
            custom_amount,
            pattern="^custom_amount$"
        )

    ],

    states={

        WAIT_CUSTOM_AMOUNT: [

            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                custom_amount_receive
            )

        ]

    },

    fallbacks=[]

)

app.add_handler(custom_conv)

# =========================================
# PAYMENT CONVERSATION
# =========================================

utr_conv = ConversationHandler(

    per_message=True,

    entry_points=[

        CallbackQueryHandler(
            confirm_payment,
            pattern="^confirm_"
        )

    ],

    states={

        WAIT_UTR: [

            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                receive_utr
            )

        ]

    },

    fallbacks=[]

)

app.add_handler(utr_conv)

# =========================================
# ADMIN ADD KEYS CONVERSATION
# =========================================

admin_conv = ConversationHandler(

    entry_points=[

        CallbackQueryHandler(
    select_days,
    pattern="^days_(3|10|30|90)$"
)

    ],

    states={

        ADD_AMOUNT: [

            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                receive_amount
            )

        ],

        ADD_KEYS: [

            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                receive_keys
            )

        ]

    },

    fallbacks=[]

)

app.add_handler(admin_conv)

# =========================================
# ERROR HANDLER
# =========================================

app.add_error_handler(error_handler)

# =========================================
# START BOT
# =========================================

print("BOT RUNNING...")

app.run_polling()
