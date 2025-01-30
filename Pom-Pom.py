import asyncio
import hashlib
import uuid
import json
import os
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import UserNotParticipant
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Tuple
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot configuration
API_ID = os.getenv('API_ID', '')  
API_HASH = os.getenv('API_HASH', '')
BOT_TOKEN = os.getenv('BOT_TOKEN', '')
GROUP_INVITE_LINK = os.getenv('GROUP_INVITE_LINK', '')
TARGET_GROUP_ID = os.getenv('TARGET_GROUP_ID', '')
CHANNEL_USERNAME = os.getenv('CHANNEL_USERNAME', '')
LOGGER_CHANNEL_ID = os.getenv('LOGGER_CHANNEL_ID', '')
MONGO_URL = os.getenv('MONGO_URL', '')
GIF_STORE_FILE = 'gifstore.json'
VIDEO_STORE_FILE = 'videostore.json'
DELETE_DELAY = 600

mongo_client = AsyncIOMotorClient(MONGO_URL)
db = mongo_client["Pom-Pom"]
users_collection = db["users"]

# Add list of admin user IDs
ADMIN_USER_IDS = [
    1949883614
]

# Create Pyrogram client
app = Client("video_share_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

async def store_user(user):
    """Store user information in MongoDB."""
    try:
        user_data = {
            "user_id": user.id,
            "username": user.username
        }
        
        await users_collection.update_one(
            {"user_id": user.id},
            {"$set": user_data},
            upsert=True
        )
    except Exception as e:
        print(f"Error storing user data: {e}")

async def log_to_channel(message: str):
    """Send log messages to the logger channel."""
    try:
        await app.send_message(LOGGER_CHANNEL_ID, message)
    except Exception as e:
        print(f"Error sending log to channel: {e}")

async def is_admin(user_id: int) -> bool:
    """Check if user is an admin."""
    return user_id in ADMIN_USER_IDS

async def delete_message_later(message: Message, delay: int = DELETE_DELAY):
    """Delete a message after specified delay."""
    try:
        warning = await message.reply_text("➥ 𝚃𝚑𝚒𝚜 𝙼𝚊𝚜𝚜𝚊𝚐𝚎 𝚆𝚒𝚕𝚕 𝙱𝚎 𝙳𝚎𝚕𝚎𝚝𝚎𝚍 𝙸𝚗 10 𝙼𝚒𝚗𝚞𝚝𝚎𝚜.")
        await asyncio.sleep(delay)
        await message.delete()
        await warning.delete()
    except Exception as e:
        print(f"Error in delete_message_later: {e}")

def create_membership_markup():
    """Create keyboard markup for channel membership buttons."""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "✅ Join Channel",
                url=f"https://t.me/{CHANNEL_USERNAME}"
            )
        ],
        [
            InlineKeyboardButton(
                "🔄 Refresh",
                callback_data="check_membership"
            )
        ]
    ])

async def check_user_membership(client, user_id):
    """Check if user is a member of the required channel."""
    try:
        member = await client.get_chat_member(f"@{CHANNEL_USERNAME}", user_id)
        return member.status in [enums.ChatMemberStatus.MEMBER, 
                               enums.ChatMemberStatus.ADMINISTRATOR, 
                               enums.ChatMemberStatus.OWNER]
    except UserNotParticipant:
        return False
    except Exception as e:
        print(f"Error checking membership: {e}")
        return False

def load_media_store(file_path):
    """Load media store from JSON file."""
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return json.load(f)
        return {}
    except Exception as e:
        print(f"Error loading media store from {file_path}: {e}")
        return {}

def save_media_store(media_store, file_path):
    """Save media store to JSON file."""
    try:
        with open(file_path, 'w') as f:
            json.dump(media_store, f, indent=4)
    except Exception as e:
        print(f"Error saving media store to {file_path}: {e}")

# Load media stores on startup
GIF_MEDIA_STORE = load_media_store(GIF_STORE_FILE)
VIDEO_MEDIA_STORE = load_media_store(VIDEO_STORE_FILE)

def generate_unique_link(media_details):
    """Generate a unique link for media."""
    unique_string = f"{media_details.file_unique_id}_{uuid.uuid4().hex[:4]}"
    return hashlib.md5(unique_string.encode()).hexdigest()[:16]

async def process_media(client, message):
    """Process media and generate a shareable link."""
    try:
        if message.video:
            media_details = message.video
            media_type = "video"
            media_store = VIDEO_MEDIA_STORE
            store_file = VIDEO_STORE_FILE
        elif message.animation or (
            message.document and (
                message.document.mime_type == "video/mp4" or 
                message.document.mime_type == "image/gif"
            )
        ):
            media_details = message.animation or message.document
            media_type = "gif"
            media_store = GIF_MEDIA_STORE
            store_file = GIF_STORE_FILE
        else:
            return None

        media_link = generate_unique_link(media_details)
        bot_username = (await client.get_me()).username
        share_link = f"https://t.me/{bot_username}?start={media_link}"

        media_store[media_link] = {
            "file_id": media_details.file_id,
            "type": media_type,
            "share_link": share_link
        }

        save_media_store(media_store, store_file)
        
        await client.send_message(
            chat_id=TARGET_GROUP_ID,
            text=share_link,
        )
        
        return True
    except Exception as e:
        print(f"Error in process_media: {e}")
        return False
    
def create_welcome_markup():
    """Create keyboard markup for welcome message with channel and group buttons."""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "📢 Join Channel",
                url=f"https://t.me/{CHANNEL_USERNAME}"
            ),
            InlineKeyboardButton(
                "👥 Join Group",
                url=GROUP_INVITE_LINK
            )
        ]
    ])

@app.on_message(filters.command("start"))
async def start_command(client, message):
    """Handle start command with media sharing and membership check."""
    user = message.from_user
    user_mention = f"[{user.first_name}](tg://user?id={user.id})"
    
    # Store user data in MongoDB
    await store_user(user)
    
    if len(message.command) == 1:
        # Log new user starting the bot
        log_message = f"🆕 New User Started Bot\n👤 User: {user_mention}\n🆔 ID: `{user.id}`"
        await log_to_channel(log_message)
        
        await client.send_photo(
            chat_id=message.chat.id,
            photo="https://cdn.glitch.global/075bb590-115b-430c-bcfb-943195fd6f98/photo_2025-01-30_05-09-38.jpg?v=1738194316999",
            caption="ᴍʏ ɴᴀᴍᴇ ɪꜱ ᴘᴏᴍ-ᴘᴏᴍ ʙᴏᴛ . ɪ ᴄᴀɴ ᴘʀᴏᴠɪᴅᴇ ᴋɪɴᴅ ᴏꜰ ᴄᴏɴᴛᴇɴᴛ ᴛᴏ ᴏᴜʀ ᴍᴇᴍʙᴇʀꜱ ᴡɪᴛʜᴏᴜᴛ ᴀɴʏ ᴄᴏꜱᴛ. ᴊᴜꜱᴛ ᴠɪꜱɪᴛ ᴛʜᴇ ɢʀᴏᴜᴘ ᴀɴᴅ ᴄʟɪᴄᴋ ᴏɴ ʟɪɴᴋꜱ ᴀɴᴅ ɢᴇᴛ ᴛʜᴇ ꜱᴘɪᴄʏ ᴠɪᴅᴇᴏ 🤤...",
            reply_markup=create_welcome_markup()
        )
        return

    try:
        is_member = await check_user_membership(client, message.from_user.id)
        if not is_member:
            reply = await message.reply_text(
                "🔒 𝗖𝗵𝗮𝗻𝗻𝗲𝗹 𝗠𝗲𝗺𝗯𝗲𝗿𝘀𝗵𝗶𝗽 𝗥𝗲𝗾𝘂𝗶𝗿𝗲𝗱\n\n"
                f"- ᴊᴏɪɴ {CHANNEL_USERNAME} ᴛᴏ ᴜꜱᴇ ᴛʜᴇ ʙᴏᴛ\n"
                "- ᴄʟɪᴄᴋ \"✅ ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ\" ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ ᴛᴏ ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ\n"
                "- ᴀꜰᴛᴇʀ ᴊᴏɪɴɪɴɢ, ᴄʟɪᴄᴋ ᴏɴ \"🔄 Refresh\" ʙᴜᴛᴛᴏɴ",
                reply_markup=create_membership_markup()
            )
            asyncio.create_task(delete_message_later(reply))
            return

        media_link = message.command[1]
        media_info = (
            GIF_MEDIA_STORE.get(media_link) or 
            VIDEO_MEDIA_STORE.get(media_link)
        )
        
        if media_info:
            # Log media access to channel
            log_message = (
                f"📥 Media Accessed\n"
                f"👤 User: {user_mention}\n"
                f"🆔 ID: `{user.id}`\n"
                f"🔗 Link: {media_info['share_link']}\n"
                f"📋 Type: {media_info['type']}"
            )
            await log_to_channel(log_message)
            
            if media_info["type"] == "video":
                sent_message = await client.send_video(
                    chat_id=message.chat.id,
                    video=media_info["file_id"],
                    reply_to_message_id=message.id,
                    protect_content=1,
                    supports_streaming=True
                )
                asyncio.create_task(delete_message_later(sent_message))
                
            elif media_info["type"] == "gif":
                if "animation" in str(media_info["file_id"]).lower():
                    sent_message = await client.send_animation(
                        chat_id=message.chat.id,
                        animation=media_info["file_id"],
                        reply_to_message_id=message.id,
                        protect_content=1
                    )
                else:
                    sent_message = await client.send_document(
                        chat_id=message.chat.id,
                        document=media_info["file_id"],
                        reply_to_message_id=message.id,
                        protect_content=1
                    )
                asyncio.create_task(delete_message_later(sent_message))
        else:
            error_message = await message.reply_text("Invalid or expired media link.")
            asyncio.create_task(delete_message_later(error_message))
            
            # Log invalid media access attempt to channel
            log_message = (
                f"⚠️ Invalid Media Access Attempt\n"
                f"👤 User: {user_mention}\n"
                f"🆔 ID: `{user.id}`\n"
                f"🔗 Attempted Link: {media_link}"
            )
            await log_to_channel(log_message)
            
    except Exception as e:
        print(f"Error in start command: {e}")
        error_message = await message.reply_text("Sorry, there was an error processing your request.")
        asyncio.create_task(delete_message_later(error_message))

@app.on_callback_query(filters.regex("^check_membership$"))
async def handle_membership_check(client, callback_query):
    """Handle membership check callback."""
    try:
        is_member = await check_user_membership(client, callback_query.from_user.id)
        if is_member:
            await callback_query.message.delete()
            await start_command(client, callback_query.message)
        else:
            await callback_query.answer("You haven't joined the channel yet!", show_alert=True)
    except Exception as e:
        print(f"Error in membership check callback: {e}")
        await callback_query.answer("Error checking membership. Please try again.", show_alert=True)

@app.on_message(filters.video | filters.animation | filters.document)
async def handle_media(client, message):
    """Handle incoming media in any group or private chat."""
    try:
        # Check if user is admin
        if not await is_admin(message.from_user.id):
            error_message = await message.reply_text("⚠️ Only administrators can upload media.")
            asyncio.create_task(delete_message_later(error_message))
            return

        success = await process_media(client, message)
        if not success and not (message.document and message.document.mime_type not in ["video/mp4", "image/gif"]):
            print("Failed to process media")
    except Exception as e:
        print(f"Error in handle_media: {e}")

@app.on_message(filters.command("mediacount"))
async def media_count(client, message):
    """Return the count of stored media."""
    # Check if user is admin
    if not await is_admin(message.from_user.id):
        error_message = await message.reply_text("⚠️ Only administrators can view media count.")
        asyncio.create_task(delete_message_later(error_message))
        return

    await message.reply_text(
        f"Total GIF media stored: {len(GIF_MEDIA_STORE)}\n" +
        f"Total Video media stored: {len(VIDEO_MEDIA_STORE)}"
    )

@app.on_message(filters.command("clearmedia"))
async def clear_media(client, message):
    """Clear all stored media."""
    # Check if user is admin
    if not await is_admin(message.from_user.id):
        error_message = await message.reply_text("⚠️ Only administrators can clear media storage.")
        asyncio.create_task(delete_message_later(error_message))
        return

    global GIF_MEDIA_STORE, VIDEO_MEDIA_STORE
    GIF_MEDIA_STORE.clear()
    VIDEO_MEDIA_STORE.clear()
    save_media_store(GIF_MEDIA_STORE, GIF_STORE_FILE)
    save_media_store(VIDEO_MEDIA_STORE, VIDEO_STORE_FILE)
    await message.reply_text("All media links cleared.")

async def broadcast_message(client, message: Message, user_id: int) -> Tuple[bool, str]:
    """Broadcast a message to a specific user."""
    try:
        caption = message.caption
        reply_markup = message.reply_markup
        
        if message.text:
            await client.send_message(
                chat_id=user_id,
                text=message.text,
                entities=message.entities,
                reply_markup=reply_markup,
                disable_notification=True
            )
        elif message.photo:
            await client.send_photo(
                chat_id=user_id,
                photo=message.photo.file_id,
                caption=caption,
                caption_entities=message.caption_entities,
                reply_markup=reply_markup,
                disable_notification=True
            )
        elif message.video:
            await client.send_video(
                chat_id=user_id,
                video=message.video.file_id,
                caption=caption,
                caption_entities=message.caption_entities,
                reply_markup=reply_markup,
                disable_notification=True
            )
        elif message.audio:
            await client.send_audio(
                chat_id=user_id,
                audio=message.audio.file_id,
                caption=caption,
                caption_entities=message.caption_entities,
                reply_markup=reply_markup,
                disable_notification=True
            )
        elif message.document:
            await client.send_document(
                chat_id=user_id,
                document=message.document.file_id,
                caption=caption,
                caption_entities=message.caption_entities,
                reply_markup=reply_markup,
                disable_notification=True
            )
        elif message.animation:
            await client.send_animation(
                chat_id=user_id,
                animation=message.animation.file_id,
                caption=caption,
                caption_entities=message.caption_entities,
                reply_markup=reply_markup,
                disable_notification=True
            )
        elif message.sticker:
            await client.send_sticker(
                chat_id=user_id,
                sticker=message.sticker.file_id,
                reply_markup=reply_markup,
                disable_notification=True
            )
        elif message.voice:
            await client.send_voice(
                chat_id=user_id,
                voice=message.voice.file_id,
                caption=caption,
                caption_entities=message.caption_entities,
                reply_markup=reply_markup,
                disable_notification=True
            )
        elif message.video_note:
            await client.send_video_note(
                chat_id=user_id,
                video_note=message.video_note.file_id,
                reply_markup=reply_markup,
                disable_notification=True
            )
        return True, ""
    except Exception as e:
        logger.error(f"Broadcast failed for user")
        return False, str(e)
    
@app.on_message(filters.command("broadcast") & filters.user(ADMIN_USER_IDS))
async def broadcast_command(client, message: Message):
    """Handle broadcast command from admin users."""
    try:
        # Check if there's a message to broadcast
        if not message.reply_to_message:
            await message.reply_text("Please reply to a message to broadcast it.")
            return

        # Get all users from the database
        users_cursor = users_collection.find({}, {"user_id": 1})
        total_users = await users_collection.count_documents({})
        
        if total_users == 0:
            await message.reply_text("No users found in database.")
            return

        # Send initial status message
        status_msg = await message.reply_text(
            f"Starting broadcast to {total_users} users..."
        )

        success_count = 0
        failed_count = 0
        blocked_count = 0
        
        # Start time for tracking
        start_time = datetime.now()

        async for user in users_cursor:
            success, error = await broadcast_message(
                client, 
                message.reply_to_message, 
                user["user_id"]
            )
            
            if success:
                success_count += 1
            else:
                if error == "user_blocked":
                    blocked_count += 1
                failed_count += 1

            # Update status every 20 users
            if (success_count + failed_count) % 20 == 0:
                await status_msg.edit_text(
                    f"Broadcast in progress...\n"
                    f"✅ Success: {success_count}\n"
                    f"❌ Failed: {failed_count}\n"
                    f"🚫 Blocked: {blocked_count}\n"
                    f"📊 Progress: {((success_count + failed_count) / total_users) * 100:.1f}%"
                )

        # Calculate duration
        duration = datetime.now() - start_time
        
        # Send final status
        await status_msg.edit_text(
            f"✅ Broadcast Completed!\n\n"
            f"Total users: {total_users}\n"
            f"✅ Successful: {success_count}\n"
            f"❌ Failed: {failed_count}\n"
            f"🚫 Blocked: {blocked_count}\n"
            f"⏱ Duration: {duration.seconds} seconds"
        )

        # Log broadcast completion
        await log_to_channel(
            f"📢 Broadcast Completed\n"
            f"👤 By: {message.from_user.mention}\n"
            f"📊 Stats:\n"
            f"- Total: {total_users}\n"
            f"- Success: {success_count}\n"
            f"- Failed: {failed_count}\n"
            f"- Blocked: {blocked_count}\n"
            f"⏱ Duration: {duration.seconds}s"
        )

    except Exception as e:
        logger.error(f"Broadcast command error: {str(e)}")
        await message.reply_text(f"❌ Error during broadcast: {str(e)}")

# Start the bot
app.run()
