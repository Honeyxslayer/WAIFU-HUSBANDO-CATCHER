import random
from html import escape 

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler

from Honey import application, PHOTO_URL, SUPPORT_CHAT, UPDATE_CHAT, BOT_USERNAME, db, GROUP_ID
from Honey import pm_users as collection 


async def start(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    first_name = update.effective_user.first_name
    username = update.effective_user.username

    user_data = await collection.find_one({"_id": user_id})

    if user_data is None:
        
        await collection.insert_one({"_id": user_id, "first_name": first_name, "username": username})
        
        await context.bot.send_message(chat_id=GROUP_ID, 
                                       text=f"New user Started The Bot..\n User: <a href='tg://user?id={user_id}'>{escape(first_name)})</a>", 
                                       parse_mode='HTML')
    else:
        
        if user_data['first_name'] != first_name or user_data['username'] != username:
            
            await collection.update_one({"_id": user_id}, {"$set": {"first_name": first_name, "username": username}})

    

    if update.effective_chat.type== "private":
        
        
        caption = f"""
        ***ʜᴇʏ...ʙᴀʙʏ👀😎***

***ɪ ᴀᴍ ᴀɴ...
🌸˹ɪɴsᴀɴᴇ ᴡᴀɪғᴜ ɢꝛᴀʙʙᴇꝛ˼❄️
𝐀ᴅᴅ 𝐌ᴇ 𝐈ɴ 𝐘ᴏᴜʀ 𝐆ʀᴏᴜᴘ 𝐀ɴᴅ 𝐈 𝐖ɪʟʟ 𝐒ᴇɴᴅ 𝐑ᴀɴᴅᴏᴍ 𝐂ʜᴀʀᴇᴄᴛᴇʀs 𝐀ғᴛᴇʀ.. 𝐄ᴠᴇʀʏ 25 𝐌ᴇsᴀɢᴇss 𝐈ɴ 𝐆ʀᴏᴜᴘ... 𝐔sᴇ /guess 𝐓ᴏ.. 𝐂ᴏʟʟᴇᴄᴛ 𝐓ʜᴀᴛ 𝐂ʜᴀʀᴇᴄᴛᴇʀs 𝐈ɴ 𝐘ᴏᴜʀ 𝐂ᴏʟʟᴇᴄᴛɪᴏɴ.. 𝐀ɴᴅ 𝐒ᴇᴇ 𝐂ᴏʟʟᴇᴄᴛɪᴏɴ 𝐁ʏ 𝐔sɪɴɢ /harem... 𝐒ᴏ 𝐀ᴅᴅ 𝐈ɴ 𝐘ᴏᴜʀ 𝐆ʀᴏᴜᴘs 𝐀ɴᴅ 𝐂ᴏʟʟᴇᴄᴛ 𝐘ᴏᴜʀ 𝐇ᴀʀᴇᴍ***
        """
        
        keyboard = [
            [InlineKeyboardButton("sᴜᴍᴍᴏ ᴍᴇ", url=f'http://t.me/{BOT_USERNAME}?startgroup=new')],
            [InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", url=f'https://t.me/{SUPPORT_CHAT}'),
            InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇs", url=f'https://t.me/{UPDATE_CHAT}')],
            [InlineKeyboardButton("ᴄᴏᴍᴍᴀɴᴅs", callback_data='help')],
            [InlineKeyboardButton("ᴏᴡɴᴇʀ", url=f'https://t.me/OgHoneyy')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        photo_url = random.choice(PHOTO_URL)

        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo_url, caption=caption, reply_markup=reply_markup, parse_mode='markdown')

    else:
        photo_url = random.choice(PHOTO_URL)
        keyboard = [
            [InlineKeyboardButton("sᴜᴍᴍᴏ ᴍᴇ", url=f'http://t.me/{BOT_USERNAME}?startgroup=new')],
            [InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", url=f'https://t.me/{SUPPORT_CHAT}'),
            InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇs", url=f'https://t.me/{UPDATE_CHAT}')],
            [InlineKeyboardButton("ᴄᴏᴍᴍᴀɴᴅs", callback_data='help')],
            [InlineKeyboardButton("ᴏᴡɴᴇʀ", url=f'https://t.me/OgHoneyy')]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo_url, caption="🎴Alive!?... \n connect to me in PM For more information ",reply_markup=reply_markup )

async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'help':
        help_text = """
    ***Help Section:***
    
***/guess: To Guess character (only works in group)***
***/fav: Add Your fav***
***/trade : To trade Characters***
***/gift: Give any Character from Your Collection to another user.. (only works in groups)***
***/collection: To see Your Collection***
***/topgroups : See Top Groups.. Ppl Guesses Most in that Groups***
***/top: Too See Top Users***
***/ctop : Your ChatTop***
***/changetime: Change Character appear time (only works in Groups)***
   """
        help_keyboard = [[InlineKeyboardButton("⤾ Bᴀᴄᴋ", callback_data='back')]]
        reply_markup = InlineKeyboardMarkup(help_keyboard)
        
        await context.bot.edit_message_caption(chat_id=update.effective_chat.id, message_id=query.message.message_id, caption=help_text, reply_markup=reply_markup, parse_mode='markdown')

    elif query.data == 'back':

        caption = f"""
        ***ʜᴇʏ...ʙᴀʙʏ👀😎*** ✨

***ɪ ᴀᴍ ᴀɴ...
🌸˹ɪɴsᴀɴᴇ ᴡᴀɪғᴜ ɢꝛᴀʙʙᴇꝛ˼❄️
𝐀ᴅᴅ 𝐌ᴇ 𝐈ɴ 𝐘ᴏᴜʀ 𝐆ʀᴏᴜᴘ 𝐀ɴᴅ 𝐈 𝐖ɪʟʟ 𝐒ᴇɴᴅ 𝐑ᴀɴᴅᴏᴍ 𝐂ʜᴀʀᴇᴄᴛᴇʀs 𝐀ғᴛᴇʀ.. 𝐄ᴠᴇʀʏ 25 𝐌ᴇsᴀɢᴇss 𝐈ɴ 𝐆ʀᴏᴜᴘ... 𝐔sᴇ /guess 𝐓ᴏ.. 𝐂ᴏʟʟᴇᴄᴛ 𝐓ʜᴀᴛ 𝐂ʜᴀʀᴇᴄᴛᴇʀs 𝐈ɴ 𝐘ᴏᴜʀ 𝐂ᴏʟʟᴇᴄᴛɪᴏɴ.. 𝐀ɴᴅ 𝐒ᴇᴇ 𝐂ᴏʟʟᴇᴄᴛɪᴏɴ 𝐁ʏ 𝐔sɪɴɢ /harem... 𝐒ᴏ 𝐀ᴅᴅ 𝐈ɴ 𝐘ᴏᴜʀ 𝐆ʀᴏᴜᴘs 𝐀ɴᴅ 𝐂ᴏʟʟᴇᴄᴛ 𝐘ᴏᴜʀ 𝐇ᴀʀᴇᴍ***
        """

        
        keyboard = [
            [InlineKeyboardButton("sᴜᴍᴍᴏ ᴍᴇ", url=f'http://t.me/{BOT_USERNAME}?startgroup=new')],
            [InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", url=f'https://t.me/{SUPPORT_CHAT}'),
            InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇs", url=f'https://t.me/{UPDATE_CHAT}')],
            [InlineKeyboardButton("ᴄᴏᴍᴍᴀɴᴅs", callback_data='help')],
            [InlineKeyboardButton("ᴏᴡɴᴇʀ", url=f'https://t.me/OgHoneyy')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await context.bot.edit_message_caption(chat_id=update.effective_chat.id, message_id=query.message.message_id, caption=caption, reply_markup=reply_markup, parse_mode='markdown')


application.add_handler(CallbackQueryHandler(button, pattern='^help$|^back$', block=False))
start_handler = CommandHandler('start', start, block=False)
application.add_handler(start_handler)
