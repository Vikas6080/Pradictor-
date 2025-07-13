import os
import logging
import telebot
from telebot import types
from predictor import predict_safe_cells
from ocr_utils import extract_board_from_image
from feedback_handler import handle_feedback

BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_TOKEN_HERE")
bot = telebot.TeleBot(BOT_TOKEN)
logging.basicConfig(level=logging.INFO)

# Store predictions per user
user_predictions = {}

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        with open("latest_image.jpg", 'wb') as new_file:
            new_file.write(downloaded_file)

        board = extract_board_from_image("latest_image.jpg")
        safe_cells, pattern_id = predict_safe_cells(board)

        grid_output = ""
        for row in range(5):
            line = ""
            for col in range(5):
                cell = chr(65 + row) + str(col + 1)
                emoji = "💎" if cell in safe_cells else "💣"
                line += f"{emoji} "
            grid_output += line.strip() + "\n"

        response = f"🔮 *Prediction Result*\n\n"
        response += f"`Pattern ID:` {pattern_id}\n"
        response += f"`Safe Cells:` {', '.join(safe_cells)}\n\n"
        response += grid_output

        markup = types.InlineKeyboardMarkup()
        markup.row(
            types.InlineKeyboardButton("✅ Correct", callback_data=f"correct_{pattern_id}"),
            types.InlineKeyboardButton("❌ Wrong", callback_data=f"wrong_{pattern_id}")
        )

        bot.send_message(message.chat.id, response, parse_mode="Markdown", reply_markup=markup)
        user_predictions[message.chat.id] = pattern_id

    except Exception as e:
        bot.reply_to(message, f"Error processing image: {e}")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data.startswith("correct_") or call.data.startswith("wrong_"):
        feedback_type, pattern_id = call.data.split("_")
        correct = feedback_type == "correct"
        handle_feedback(pattern_id, correct)
        bot.answer_callback_query(call.id, "Thanks for the feedback!")

bot.polling()
