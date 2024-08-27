# Euro Blog App

## Overview
The Euro Blog App is a lightweight blogging platform designed to share experiences from a trip to Europe in 2024. It utilizes Flask for the web framework, Google Cloud services for data storage, and a Telegram bot for posting updates.

## Features
- **Blogging**: Users can send messages or images via a Telegram bot, which are then posted to the blog.
- **Image Storage**: Images are uploaded to Google Cloud Storage (GCS) and linked to blog posts.
- **Firestore Database**: Posts are stored in Firestore, allowing for easy retrieval and display.
- **Responsive Design**: The web interface is designed to be user-friendly on both desktop and mobile devices.

## Technologies Used
- **Flask**: Web framework for building the application.
- **Google Cloud Firestore**: NoSQL database for storing blog posts.
- **Google Cloud Storage**: For storing images uploaded by users.
- **Telegram Bot API**: For handling user messages and posting them to the blog.
- **HTML/CSS**: For the front-end design.

## Setup Instructions

### Prerequisites
- Python 3.x
- Google Cloud account with Firestore and Storage enabled.
- Telegram Bot Token (set as an environment variable `TELEGRAM_BOT_TOKEN`).
- Webhook to forward Telegram messages to the app.

### Using the Telegram Bot
- Start a chat with your bot on Telegram and send a message or an image.
- The bot will respond with a confirmation that your post has been added to the blog.

### Web Interface
- Navigate to the root URL to view the blog posts.
- Posts will be displayed in reverse chronological order, with images shown if available.

## Code Structure
- `app.py`: Main application file containing routes, bot handlers, and database interactions.
- `models.py`: Defines the database model for blog posts.
- `config.py`: Configuration settings for the application.
- `templates/`: Contains HTML templates for rendering the web pages.
- `static/`: Contains static files like CSS for styling the application.
- `requirements.txt`: Lists the dependencies required to run the application.
