<h1 align="center">
  <a href="https://telegram.me/BotCodeVerse">🤖 ᴘᴏᴍ-ᴘᴏᴍ ʙᴏᴛ</a>
</h1>
A powerful Telegram bot for managing and sharing media content with advanced features and user management capabilities.
<img src="https://cdn.glitch.global/115a68e3-597e-445c-9598-4db19dfe4ccb/BotCodeVerse.gif?v=1738204676642"/>
## 🌟 Features

* 📱 Supports multiple media types (videos, GIFs, animations)
* 🔐 Channel membership verification
* 🎯 Unique sharing links generation
* 📊 Admin dashboard with media statistics
* 📢 Broadcast messaging capability
* 📝 Detailed logging system
* 🗃️ MongoDB integration for user management
* ⚡ Asynchronous operation for better performance

## ⚙️ Requirements

* Python 3.7 or higher
* MongoDB database
* Telegram Bot Token
* API ID and Hash from Telegram

## 📥 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/pom-pom-bot.git
cd pom-pom-bot
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## 🛠️ Configuration

Update the following variables in the script:

```python
API_ID = 'your_api_id'
API_HASH = 'your_api_hash'
BOT_TOKEN = 'your_bot_token'
GROUP_INVITE_LINK = "your_group_link"
TARGET_GROUP_ID = "your_group_id"
CHANNEL_USERNAME = 'your_channel_username'
LOGGER_CHANNEL_ID = "your_logger_channel_id"
MONGO_URL = "your_mongodb_url"
```

> ⚠️ **Important:** Never share your API credentials or Bot Token publicly!

## 🚀 Running the Bot

```bash
python bot.py
```

## 📚 Bot Commands

* `/start` - Start the bot and check channel membership
* `/mediacount` - Get count of stored media (Admin only)
* `/clearmedia` - Clear all stored media (Admin only)
* `/broadcast` - Send broadcast message to all users (Admin only)

## 👥 Admin Features

* **Media Upload:** Admins can upload videos and GIFs
* **Media Management:** View and clear stored media
* **Broadcast Messages:** Send messages to all registered users
* **Statistics:** View media count and storage information

> 📝 **Note:** Make sure to add admin user IDs in the ADMIN_USER_IDS list to grant administrative privileges.

## 💡 How It Works

1. **User Registration:**
   * Users start the bot using the `/start` command
   * Bot verifies channel membership
   * User data is stored in MongoDB

2. **Media Sharing:**
   * Admins upload media files
   * Bot generates unique sharing links
   * Media is stored with metadata
   * Users can access media through generated links

3. **Administration:**
   * Admins can monitor media statistics
   * Broadcast messages to all users
   * Manage stored media content
   * View user engagement metrics

## 🔒 Security Features

* Channel membership verification
* Protected content sharing
* Admin-only media uploads
* Secure user data storage
* Rate limiting and spam protection

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support, join our [Telegram Group](your_support_group_link) or create an issue in the repository.

---
Made with ❤️ by [Your Name]
