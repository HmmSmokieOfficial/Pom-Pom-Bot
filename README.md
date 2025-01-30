<h1 align="center">
  <a href="https://telegram.me/BotCodeVerse">ᴘᴏᴍ-ᴘᴏᴍ ʙᴏᴛ</a>
</h1>
<img src="https://cdn.glitch.global/115a68e3-597e-445c-9598-4db19dfe4ccb/BotCodeVerse.gif?v=1738204676642"/>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pom-Pom Bot - Telegram Media Sharing Bot</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
        }
        .container {
            background-color: #f8f9fa;
            border-radius: 8px;
            padding: 30px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }
        h2 {
            color: #2980b9;
            margin-top: 25px;
        }
        pre {
            background-color: #f1f1f1;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }
        code {
            font-family: 'Courier New', Courier, monospace;
            background-color: #f1f1f1;
            padding: 2px 5px;
            border-radius: 3px;
        }
        ul {
            padding-left: 20px;
        }
        .feature-list li {
            margin-bottom: 10px;
        }
        .note {
            background-color: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin: 15px 0;
        }
        .important {
            background-color: #f8d7da;
            border-left: 4px solid #dc3545;
            padding: 15px;
            margin: 15px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 ᴘᴏᴍ-ᴘᴏᴍ ʙᴏᴛ</h1>
        <p>A powerful Telegram bot for managing and sharing media content with advanced features and user management capabilities.</p>

        <h2>🌟 Features</h2>
        <ul class="feature-list">
            <li>📱 Supports multiple media types (videos, GIFs, animations)</li>
            <li>🔐 Channel membership verification</li>
            <li>🎯 Unique sharing links generation</li>
            <li>📊 Admin dashboard with media statistics</li>
            <li>📢 Broadcast messaging capability</li>
            <li>📝 Detailed logging system</li>
            <li>🗃️ MongoDB integration for user management</li>
            <li>⚡ Asynchronous operation for better performance</li>
        </ul>

        <h2>⚙️ Requirements</h2>
        <pre>
- Python 3.7 or higher
- MongoDB database
- Telegram Bot Token
- API ID and Hash from Telegram</pre>

        <h2>📥 Installation</h2>
        <ol>
            <li>Clone the repository:
                <pre>git clone https://github.com/yourusername/pom-pom-bot.git
cd pom-pom-bot</pre>
            </li>
            <li>Install required packages:
                <pre>pip install -r requirements.txt</pre>
            </li>
        </ol>

        <h2>🛠️ Configuration</h2>
        <p>Update the following variables in the script:</p>
        <pre>
API_ID = 'your_api_id'
API_HASH = 'your_api_hash'
BOT_TOKEN = 'your_bot_token'
GROUP_INVITE_LINK = "your_group_link"
TARGET_GROUP_ID = "your_group_id"
CHANNEL_USERNAME = 'your_channel_username'
LOGGER_CHANNEL_ID = "your_logger_channel_id"
MONGO_URL = "your_mongodb_url"</pre>

        <div class="important">
            <strong>Important:</strong> Never share your API credentials or Bot Token publicly!
        </div>

        <h2>🚀 Running the Bot</h2>
        <pre>python bot.py</pre>

        <h2>📚 Bot Commands</h2>
        <ul>
            <li><code>/start</code> - Start the bot and check channel membership</li>
            <li><code>/mediacount</code> - Get count of stored media (Admin only)</li>
            <li><code>/clearmedia</code> - Clear all stored media (Admin only)</li>
            <li><code>/broadcast</code> - Send broadcast message to all users (Admin only)</li>
        </ul>

        <h2>👥 Admin Features</h2>
        <ul>
            <li>Media Upload: Admins can upload videos and GIFs</li>
            <li>Media Management: View and clear stored media</li>
            <li>Broadcast Messages: Send messages to all registered users</li>
            <li>Statistics: View media count and storage information</li>
        </ul>

        <div class="note">
            <strong>Note:</strong> Make sure to add admin user IDs in the ADMIN_USER_IDS list to grant administrative privileges.
        </div>

        <h2>🤝 Contributing</h2>
        <p>Contributions are welcome! Please feel free to submit a Pull Request.</p>

        <h2>📄 License</h2>
        <p>This project is licensed under the MIT License - see the LICENSE file for details.</p>
    </div>
</body>
</html>
