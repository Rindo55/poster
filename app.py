import os
from wantedposter.wantedposter import WantedPoster
from PIL import Image
from pyrogram import Client, filters
from pyrogram.types import Message

# Initialize your bot with your API ID and API Hash
API_ID = 3845818
API_HASH = "95937bcf6bc0938f263fc7ad96959c6d"
BOT_TOKEN = "7289437881:AAFkUiGgL4091LZgsek1AR1OorzDVFVFyrM"

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# State variables to hold user input
user_data = {}

@app.on_message(filters.command("start"))
def start(client, message: Message):
    message.reply("Welcome! Please enter the first name:")
    user_data[message.from_user.id] = {"step": "first_name"}

@app.on_message(filters.text & filters.private)
def handle_input(client, message: Message):
    user_id = message.from_user.id
    
    if user_id not in user_data:
        return
    
    step = user_data[user_id]["step"]

    if step == "first_name":
        user_data[user_id]["first_name"] = message.text
        user_data[user_id]["step"] = "last_name"
        message.reply("Please enter the last name:")
    
    elif step == "last_name":
        user_data[user_id]["last_name"] = message.text
        user_data[user_id]["step"] = "bounty"
        message.reply("Please enter the bounty amount (e.g., 3000000000):")
    
    elif step == "bounty":
        try:
            bounty_amount = int(message.text)
            user_data[user_id]["bounty"] = bounty_amount
            user_data[user_id]["step"] = "image"
            message.reply("Please upload an image:")
        except ValueError:
            message.reply("Invalid bounty amount. Please enter a valid number.")
    
    elif step == "image":
        # Handle image upload
        if message.photo:
            # Save the photo
            file_path = f"img/{user_id}_image.jpg"
            message.download(file_path)
            
            # Generate wanted poster
            first_name = user_data[user_id]["first_name"]
            last_name = user_data[user_id]["last_name"]
            bounty_amount = user_data[user_id]["bounty"]

            wanted_poster = WantedPoster(file_path, first_name, last_name, bounty_amount)
            poster_path = wanted_poster.generate()

            # Send the generated poster back to the user
            app.send_photo(user_id, poster_path)

            # Clean up temporary files
            os.remove(file_path)
            os.remove(poster_path)

            # Reset user data
            del user_data[user_id]
        else:
            message.reply("Please upload a valid image.")

if __name__ == "__main__":
    app.run()
