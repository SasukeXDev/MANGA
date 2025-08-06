import random
from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    Message,
    InputMediaPhoto,
)
from utils.db import db
from .handlers import get_sources
from config import ADMINS
from plugins.force_sub import require_join
from utils.filters import require_not_banned

users_coll = db["users"]

PHOTO_URL = [
    "https://img4.teletype.in/files/77/ff/77ff451d-0c8a-4aeb-aa9a-a1ae7ca74069.jpeg",
    "https://img4.teletype.in/files/bb/e9/bbe9e4f6-6226-4764-8169-b7d368e29e8c.jpeg",
    "https://img2.teletype.in/files/d4/b8/d4b806a2-c534-466f-85cb-f05a9e31dc92.jpeg",
    "https://img4.teletype.in/files/b6/aa/b6aab772-1d39-4b7e-bfe5-8d04b57ac31e.jpeg",
    "https://img4.teletype.in/files/f5/c3/f5c3a05e-ecfb-4a8e-b921-2b264d40d0ce.jpeg",
    "https://img4.teletype.in/files/3f/01/3f0102af-352a-4a0a-abbd-f18919c56dc9.jpeg",
    "https://img4.teletype.in/files/7f/f2/7ff228ef-6e74-4baf-a877-b35c016d6c7b.jpeg",
    "https://img1.teletype.in/files/8b/02/8b02924e-4f24-4ace-8b3f-be2f8044b8ec.jpeg",
    "https://img2.teletype.in/files/dc/16/dc1625b2-410c-48da-98c1-1956b87768e1.jpeg",
    "https://img2.teletype.in/files/97/f3/97f31df6-2cca-4f58-8269-97aebb6d9ea7.jpeg",
    "https://img2.teletype.in/files/97/65/9765707e-1855-429b-89ba-03401b734827.jpeg",
    "https://img4.teletype.in/files/f4/53/f45390f3-e1eb-4570-9d67-c4114db18589.jpeg",
    "https://img1.teletype.in/files/81/26/81265a94-68ff-47ed-b409-fad382e7a627.jpeg",
    "https://img1.teletype.in/files/0a/1b/0a1b5f17-095c-4826-84c8-39a8b9b9deef.jpeg",
    "https://img4.teletype.in/files/f5/94/f594fbe2-b52d-489a-86c9-23b2f2dbe4d7.jpeg",
    "https://img3.teletype.in/files/e3/76/e376be29-065b-4c1a-986d-aba69d08208f.jpeg",
    "https://img1.teletype.in/files/8f/e6/8fe67878-43a3-4b3d-851f-63727a6a2b0b.jpeg",
    "https://img2.teletype.in/files/1a/d3/1ad3fa24-c3bf-4ca8-a7ef-a79286b1e37c.jpeg",
    "https://img1.teletype.in/files/80/1a/801a77ad-bf05-4d7a-96c9-2b1cde09d04f.jpeg",
    "https://img4.teletype.in/files/f4/b0/f4b007ec-fc8c-49fd-a1fb-b0d02985120a.jpeg",
    "https://img4.teletype.in/files/f6/3c/f63cee0d-10ff-4b8d-9ccc-943fa80a1344.jpeg",
]

emojis = [
    "💅",
    "🗿",
    "❤️",
    "💋",
    "😱",
    "⚡️",
    "🐳",
    "🔥",
    "😘",
    "😁",
    "🤯",
    "😈",
    "👾",
    "🎉",
    "🕊️",
    "🦄",
    "👻",
]
effects = [5104841245755180586, 5046509860389126442, 5159385139981059251]


def get_main_keyboard():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("👩‍💻 Dev", url="https://t.me/xyroz_mrz"),
                InlineKeyboardButton("ℹ️ Commands", callback_data="commands"),
            ],
            [
                InlineKeyboardButton(
                    "📥 Database", url="https://t.me/+Rt5wOj7NkfU4ZTM9"
                ),
                InlineKeyboardButton(
                    "⚡ Group Chat", url="https://t.me/+Os2R_iM3K1RhMmE1"
                ),
            ],
            [InlineKeyboardButton("Close", callback_data="close")],
        ]
    )


def get_help_keyboard():
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("🔙 Back", callback_data="back")],
            [InlineKeyboardButton("Close", callback_data="close")],
        ]
    )


HELP_TEXT = (
    "<blockquote><b>How to use the bot:</b>\n\n"
    "• <b>/search</b> - Search for manga\n"
    "• <b>/queue</b> - View your queue & global queue\n"
    "• <b>/clear_queue</b> - Clear your queue\n"
    "• <b>/subscription</b> - View your subscriptions\n"
    "• <b>/sources</b> - List available sources\n"
    "• <b>/version</b> - Check bot version\n"
    "• <b>/start</b> - Return to this menu\n"
    "\nEnjoy reading! 💖</blockquote>"
)

from pyrogram.enums import ChatType


@Client.on_message(filters.command("start"))
@require_join
@require_not_banned
async def start_command(client, message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name or "Unknown"
    if not users_coll.find_one({"_id": user_id}):
        users_coll.insert_one({"_id": user_id, "name": first_name})

    emoji = random.choice(emojis)
    try:
        await client.send_reaction(
            chat_id=message.chat.id,
            message_id=message.id,
            emoji=emoji,
            big=True,
        )
    except Exception as e:
        print(e)

    ranpic = random.choice(PHOTO_URL)
    caption = (
        f"<blockquote>Welcome <b><a href='tg://user?id={user_id}'>{first_name}</a></b> to <b><i>Granny's Manga DL Bot!</b>\n\n"
        "Start downloading manga/manhwa/manhua/webtoons from multiple sources!!</i>\n\n"
        "<b>Use the buttons below to get started!👇</b></blockquote>"
    )
    eid = random.choice(effects)
    if message.chat.type == ChatType.PRIVATE:
        await client.send_photo(
            chat_id=message.chat.id,
            photo=ranpic,
            caption=caption,
            reply_markup=get_main_keyboard(),
            message_effect_id=eid,
        )
    else:
        await client.send_photo(
            chat_id=message.chat.id,
            photo=ranpic,
            caption=caption,
            reply_markup=get_main_keyboard(),
        )


@Client.on_callback_query(filters.regex("^commands$"))
@require_not_banned
async def help_callback(client, query: CallbackQuery):
    ranpic = random.choice(PHOTO_URL)
    await query.message.edit_media(
        media=InputMediaPhoto(media=ranpic, caption=HELP_TEXT),
        reply_markup=get_help_keyboard(),
    )
    await query.answer()


@Client.on_callback_query(filters.regex("^back$"))
@require_not_banned
async def back_callback(client, query: CallbackQuery):
    ranpic = random.choice(PHOTO_URL)
    await query.message.edit_media(
        media=InputMediaPhoto(
            media=ranpic,
            caption=(
                f"<blockquote>Welcome <b><a href='tg://user?id={query.from_user.id}'>{query.from_user.first_name}</a></b> to <b><i>Granny's Manga DL Bot!</b>\n\n"
                "Start downloading manga/manhwa/manhua/webtoons from multiple sources!!</i>\n\n"
                "<b>Use the buttons below to get started!👇</b></blockquote>"
            ),
        ),
        reply_markup=get_main_keyboard(),
    )
    await query.answer()


@Client.on_callback_query(filters.regex("^close$"))
@require_not_banned
async def close_callback(client, query: CallbackQuery):
    try:
        await query.message.delete()
    except Exception:
        await query.message.edit_reply_markup(reply_markup=None)
    await query.answer()


@Client.on_message(filters.command("sources"))
@require_join
@require_not_banned
async def sources_command(client, message: Message):
    sources = get_sources()
    if not sources:
        await message.reply_text("No sources available.")
        return
    text = "<b>Available sources:</b>\n\n"
    text += "<blockquote>"
    for src_name, src_cls in sources.items():
        if src_name.lower() in ["base", "basesource"]:
            continue
        display = getattr(src_cls, "display_name", src_name)
        url = getattr(src_cls, "url", None)
        if url:
            text += f"• <b>{display}</b>: <a href='{url}'>{url}</a>\n"
        else:
            text += f"• <b>{display}</b>\n"
    text += "</blockquote>"
    await message.reply_text(text.strip(), disable_web_page_preview=True)


@Client.on_message(filters.command("users"))
async def users_command(client, message: Message):
    if message.from_user.id not in ADMINS:
        return
    total_users = users_coll.count_documents({})
    await message.reply_text(
        f"👥 Total registered users: <b>{total_users}</b>"
    )
