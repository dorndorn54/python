import telebot
from telebot.types import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton
import random

# Replace this with your actual bot token
BOT_TOKEN = '8267299141:AAFNU95X-z4p8gDbV-zuA7AEdHf0SSYA-gk'

bot = telebot.TeleBot(BOT_TOKEN)

value_range = {
    'wxi_yxn' : [90, 100],
    'uniq_chlo' : [80, 90],
    'pandbbear' : [70, 80],
}

# Handle inline queries (when someone types @gaybot in any chat)
@bot.inline_handler(lambda query: True)
def handle_inline_query(inline_query):
    try:
        # Get the user's query text
        user = inline_query.from_user
        username = obtain_username(user)
        query_text = inline_query.query or "Hello"
        
        share_keyboard = InlineKeyboardMarkup()
        share_keyboard.add(
            InlineKeyboardButton("Share your gayness! 🏳️‍🌈", switch_inline_query="")
        )


        results = [
            InlineQueryResultArticle(
                id='1',
                title='How gay are you?',
                description='click to find out how gay you are',
                thumbnail_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRYVjwWcucjURU7AiWxIaK5KkqLDSH9zgO9gg&s',
                thumbnail_width=100,
                thumbnail_height=100,
                input_message_content=InputTextMessageContent(gay_value(username), parse_mode='HTML'),
                reply_markup=share_keyboard
            ),
            InlineQueryResultArticle(
                id='2',
                title='Help',
                description='you dont need to click on this',
                thumbnail_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRYVjwWcucjURU7AiWxIaK5KkqLDSH9zgO9gg&s',
                thumbnail_width=100,
                thumbnail_height=100,
                input_message_content=InputTextMessageContent('Its just a bot, click on the first button')
            )
        ]

        bot.answer_inline_query(inline_query.id, results, cache_time=1)
    except Exception as e:
        print(f"Error handling inline query: {e}")

def obtain_username(user):
    if user.username:
        return user.username
    return user.first_name

def gay_value(username):
    print(f"Checking gay value for: {username}")
    if username in value_range:
        min_val, max_val = value_range[username]
        value = random.randint(min_val, max_val)
    else:
        value = random.randint(0, 100)  # default range for others

    return f"🏳️‍🌈 I am {value}% gay!"

    
# Start polling
bot.polling()