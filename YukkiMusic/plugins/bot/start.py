from YukkiMusic import app
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from config import SUPPORT_GROUP, SUPPORT_CHANNEL, OWNER, START_IMG_URL
from strings.filters import command

# دالة وهمية
async def add_served_user(user_id: int):
    pass

new_start_message = None
change_start_msg = False  # متغير للتحقق مما إذا كان المطور يرغب في تغيير الكليشة

@app.on_message(command("⦗ تغيير كليشة ستارت ⦘") & filters.user(OWNER))
async def change_start_message(_, message: Message):
    global change_start_msg
    change_start_msg = True
    await message.reply("مرحبا عزيزي المطور الأساسي \nارسل الآن كليشة ستارت الجديدة.")

@app.on_message(filters.private & filters.user(OWNER))
async def set_new_start_message(_, message: Message):
    global new_start_message, change_start_msg
    if change_start_msg:
        new_start_message = message.text
        change_start_msg = False
        await message.reply("- تم بنجاح تغيير كليشة الستارت.")

@app.on_message(filters.command(["start", "help"]) & filters.private)
async def start_(c: Client, message: Message):
    global new_start_message
    user_id = message.from_user.id
    await add_served_user(user_id)

    if new_start_message:
        start_text = new_start_message
    else:
        start_text = f"""أهلاً بك عزيزي في بوت تشغيل الميديا الصوتية في المجموعات والقنوات مع دعم ميزات كثيرة يمكنك التحقق منها عن طريق استخدام الأزرار أدناه.\n⎯ ⎯ ⎯ ⎯"""

    await message.reply_photo(
        photo=START_IMG_URL,
        caption=start_text,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="⦗ اوامر البوت ⦘", callback_data="command_list")
                ],
                [
                    InlineKeyboardButton(text="⦗ قناة السورس ⦘", url=SUPPORT_CHANNEL),
                    InlineKeyboardButton(text="⦗ قناة التحديثات ⦘", url=SUPPORT_GROUP),
                ],
                [
                    InlineKeyboardButton(text="⦗ مطور البوت ⦘", url=f"https://t.me/{OWNER}"),
                ],
            ]
        )
    )

@app.on_callback_query(filters.regex("command_list"))
async def commands_set(_, query: CallbackQuery):
    await query.answer("تم فتح لوحة التشغيل")
    global new_start_message
    start_text = new_start_message if new_start_message else f"""أهلاً بك عزيزي في بوت تشغيل الميديا الصوتية في المجموعات والقنوات مع دعم ميزات كثيرة يمكنك التحقق منها عن طريق استخدام الأزرار أدناه.\n⎯ ⎯ ⎯ ⎯"""
    await query.edit_message_text(
        start_text,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⦗ أوامر التشغيل ⦘", callback_data="user_command"),
                ],
                [
                    InlineKeyboardButton("⦗ الرجوع ⦘", callback_data="home_start"),
                    InlineKeyboardButton("⦗ التالي ⦘", callback_data="next"),
                ],
            ]
        )
    )

@app.on_callback_query(filters.regex("home_start"))
async def start_set(_, query: CallbackQuery):
    await query.answer("قائمة التحكم")
    global new_start_message
    start_text = new_start_message if new_start_message else f"""أهلاً بك عزيزي في بوت تشغيل الميديا الصوتية في المجموعات والقنوات مع دعم ميزات كثيرة يمكنك التحقق منها عن طريق استخدام الأزرار أدناه.\n⎯ ⎯ ⎯ ⎯"""
    await query.edit_message_text(
        start_text,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⦗ اوامر البوت ⦘", callback_data="command_list")
                ],
                [
                    InlineKeyboardButton("⦗ قناة السورس ⦘", url=SUPPORT_CHANNEL),
                    InlineKeyboardButton("⦗ قناة التحديثات ⦘", url=SUPPORT_GROUP),
                ],
                [
                    InlineKeyboardButton("⦗ مطور البوت ⦘", url=f"https://t.me/{OWNER}"),
                ],
            ]
        )
    )

@app.on_callback_query(filters.regex("next"))
async def commands_set(_, query: CallbackQuery):
    await query.answer("تم فتح لوحة الأدمن")
    await query.edit_message_text(
        f"""- تم فتح لوحة التحكم ↓
 – – – – – – 
⦗ تستطيع التحكم عن طريق الأزرار أدناه ⦘""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⦗ أوامر الأدمن ⦘", callback_data="developer_commands"),
                ],
                [
                    InlineKeyboardButton("⦗ الرجوع ⦘", callback_data="command_list"),
                    InlineKeyboardButton("⦗ التالي ⦘", callback_data="ghaith"),
                ],
            ]
        )
    )

@app.on_callback_query(filters.regex("ghaith"))
async def commands_set(_, query: CallbackQuery):
    await query.answer("تم فتح لوحة المطور")
    await query.edit_message_text(
        f"""- تم فتح لوحة التحكم ↓
 – – – – – – 
⦗ تستطيع التحكم عن طريق الأزرار أدناه ⦘""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⦗ اوامر المطور ⦘", callback_data="owner_commands"),
                ],
                [
                    InlineKeyboardButton("⦗ الرجوع ⦘", callback_data="home_start"),
                    InlineKeyboardButton("⦗ التالي ⦘", callback_data="command_list"),
                ],
            ]
        )
    )

@app.on_callback_query(filters.regex("user_command"))
async def user_commands_set(_, query: CallbackQuery):
    await query.answer("تم فتح اوامر التشغيل")
    await query.edit_message_text(
        f"""هذا هي أوامر التشغيل
شغل 
تشغيل 

""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⦗ التالي ⦘", callback_data="next")
                ],
            ]
        ),
    )

@app.on_callback_query(filters.regex("developer_commands"))
async def developer_commands_set(_, query: CallbackQuery):
    await query.answer("تم فتح اوامر الأدمن")
    await query.edit_message_text(
        f"""هذه هيه اوامر المالك
        
        
منضر اوامر المالك

""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⦗ التالي ⦘", callback_data="ghaith")
                ],
            ]
        ),
    )
