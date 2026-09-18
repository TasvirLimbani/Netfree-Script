import os
import logging
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Setup logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("8073994749:AAHGjnut8yM3567w5dixVBggn9BEaFHkHiQ")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "👋 Hi! Send me any **Instagram Reel or Post link**, and I will download and send you the MP4 video."
    )

async def handle_instagram_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    url = update.message.text.strip()
    
    if "instagram.com" not in url:
        await update.message.reply_text("⚠️ Please send a valid Instagram link.")
        return

    status_message = await update.message.reply_text("📥 Downloading Instagram Reel, please wait...")

    output_template = "downloads/%(id)s.%(ext)s"
    ydl_opts = {
        'format': 'mp4/best',
        'outtmpl': output_template,
        'quiet': True,
    }

    try:
        os.makedirs("downloads", exist_ok=True)
        
        # Download video using yt-dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)

        # Send the video file back to the user
        with open(file_path, 'rb') as video_file:
            await update.message.reply_video(video=video_file, caption="Here is your reel! 🎬")

        # Clean up local file
        if os.path.exists(file_path):
            os.remove(file_path)
            
        await status_message.delete()

    except Exception as e:
        logger.error(f"Error downloading reel: {e}")
        await status_message.edit_text("❌ Failed to download this reel. Make sure the account/post is public.")

def main() -> None:
    if not TOKEN:
        logger.error("No TELEGRAM_BOT_TOKEN found!")
        return

    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_instagram_link))

    application.run_polling()

if __name__ == "__main__":
    main()
