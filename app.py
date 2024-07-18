from flask import Flask, request, render_template
from google.cloud import firestore
from google.cloud import storage
from telegram import Update, Bot
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
import logging
import datetime
import os
from io import BytesIO
import uuid
# import pytz

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Initialize Firestore client
db = firestore.Client()

# Telegram bot token and dispatcher
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot, None, workers=0, use_context=True)

def upload_to_gcs(file, bucket_name):
    try:
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(file.filename)
        blob.upload_from_file(file, content_type='image/jpeg')
        logging.info(f"Uploaded file to GCS: {blob.public_url}")
        return blob.public_url
    except Exception as e:
        logging.error(f"Error uploading to GCS: {e}")
        return None

def add_post(content, image_url=None):
    try:
        doc_ref = db.collection('posts').document()
        timestamp = datetime.datetime.utcnow().isoformat() + 'Z'  # Store in UTC
        doc_ref.set({
            'content': content,
            'image_url': image_url,
            'timestamp': timestamp
        })
        logging.info(f"Added post to Firestore: {content}, {image_url}")
    except Exception as e:
        logging.error(f"Error adding post to Firestore: {e}")

def start(update, context):
    update.message.reply_text('Hi! Send me a message and I\'ll add it to the blog!')

def handle_message(update, context):
    content = update.message.caption if update.message.caption else update.message.text
    image_url = None

    if update.message.photo:
        file = context.bot.get_file(update.message.photo[-1].file_id)
        image_data = file.download_as_bytearray()
        image_file = BytesIO(image_data)
        image_file.filename = f"{uuid.uuid4()}.jpg"
        image_url = upload_to_gcs(image_file, 'europe_image_bucket')
        logging.info(f"Uploaded image to {image_url}")

    add_post(content, image_url)
    logging.info("Post added to Firestore")
    update.message.reply_text("Your post has been added to the blog!")

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text | Filters.photo, handle_message))

@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return 'ok'

@app.route('/')
def index():
    posts_ref = db.collection('posts').order_by('timestamp', direction=firestore.Query.DESCENDING)
    posts = posts_ref.stream()
    post_list = []
    for post in posts:
        post_dict = post.to_dict()
        post_dict['timestamp'] = post_dict['timestamp']  # Ensure timestamp is passed as string
        post_list.append(post_dict)
    return render_template('index.html', posts=post_list)

if __name__ == '__main__':
    app.run(debug=True)
