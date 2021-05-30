import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import pyrogram
from pyrogram import filters
from bot import autocaption
from config import Config
from translation import Translation
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
 

#all buttons 

#start buttons 

start_button=InlineKeyboardMarkup(
        [
              [
                  InlineKeyboardButton("📄 BOT STATUS", callback_data = "status_data")
              ], 
              [
                  InlineKeyboardButton("📫 UPDATES", url = "https://t.me/Ts_bots"), 
                  InlineKeyboardButton("📕 ABOUT", callback_data = "about_data")
              ], 
              [
                  InlineKeyboardButton("💡 HELP", callback_data = "help_data"), 
                  InlineKeyboardButton("🔐 CLOSE", callback_data = "close_data")
              ] 
        ]
)

# help buttons

help_button=InlineKeyboardMarkup(
        [
              [
                InlineKeyboardButton("ABOUT MARKDOWN", callback_data = "markdown_data")
              ], 
              [
                  InlineKeyboardButton("⬇️ BACK", callback_data = "back_data"), 
                  InlineKeyboardButton("🔐 CLOSE", callback_data = "close_data")
              ]
        ]
)
 
# about button 

about_button=InlineKeyboardMarkup(
        [
              [
                  InlineKeyboardButton("⬇️ BACK", callback_data = "back_data"), 
                  InlineKeyboardButton("🔐 CLOSE", callback_data = "close_data")
              ]
        ]
) 


@autocaption.on_message(filters.command("start") & filters.private)
async def start(bot, cmd):
      await bot.send_message(
          chat_id = cmd.chat.id,
          text = Translation.START_TEXT.format(cmd.from_user.first_name, Config.ADMIN_USERNAME), 
          reply_to_message_id = cmd.message_id,
          parse_mode = "markdown",
          disable_web_page_preview = True, 
          reply_markup = start_button
      )


@autocaption.on_message(filters.command("help") & filters.private)
async def help(bot, cmd):
      await bot.send_message(
          chat_id = cmd.chat.id,
          text = Translation.HELP_TEXT, 
          reply_to_message_id = cmd.message_id,
          parse_mode = "html",
          disable_web_page_preview = True,
          reply_markup = help_button           
      )


@autocaption.on_message(filters.command("about") & filters.private)
async def about(bot, cmd):
      await bot.send_message(
          chat_id = cmd.chat.id,
          text = Translation.ABOUT_TEXT, 
          reply_to_message_id = cmd.message_id,
          parse_mode = "markdown",
          disable_web_page_preview = True, 
          reply_markup = about_button
      )   


@autocaption.on_message(filters.command("set_caption") & filters.private)
async def set_caption(bot, cmd):
    if len(m.command) == 1:
        await cmd.reply_text(
            "Send me the caption in the format `/set_caption your caption`"
        )
    else:
        command, caption = cmd.text.split(' ', 1)
        await update_caption(cmd.from_user.id, caption)
        await cmd.reply_text(f"**--Your Caption--:**\n\n{caption}", quote=True)


@autocaption.on_message(filters.command("caption") & filters.private)
async def caption(bot, cmd):
    caption = await get_caption(cmd.from_user.id)
    if caption != None:
        text = f"**--Your custom caption:--**\n\n{caption}"
    else:
        text = "You didn't set any caption yet. Please set that by /set_caption and use this command to check your caption"
    await cmd.reply_text(text, quote=True)


# call_backs 

@autocaption.on_callback_query()
async def button(bot, cmd: CallbackQuery):
    cb_data = cmd.data
    if "about_data" in cb_data:
        await cmd.message.edit(
             text = Translation.ABOUT_TEXT,
             parse_mode="markdown", 
             disable_web_page_preview=True, 
             reply_markup=InlineKeyboardMarkup(
                 [
                     [
                      InlineKeyboardButton("⬇️ BACK", callback_data="back_data"),
                      InlineKeyboardButton("🔐 CLOSE", callback_data="close_data")
                     ]
 
                 ] 
             ) 
        )
    elif "help_data" in cb_data:
          await cmd.message.edit(
               text=Translation.HELP_TEXT,
               parse_mode="html", 
               disable_web_page_preview=True, 
               reply_markup=InlineKeyboardMarkup(
                   [
                       [
                        InlineKeyboardButton("ABOUT MARKDOWN", callback_data = "markdown_data")
                       ],
                       [
                        InlineKeyboardButton("⬇️ BACK", callback_data="back_data"),
                        InlineKeyboardButton("🔐 CLOSE", callback_data="close_data")
                       ]
 
                   ] 
               ) 
          )
    elif "back_data" in cb_data:
          await cmd.message.edit(
               text=Translation.START_TEXT.format(cmd.from_user.first_name, Config.ADMIN_USERNAME),
               parse_mode="markdown", 
               disable_web_page_preview=True, 
               reply_markup=InlineKeyboardMarkup(
                   [
                      
                       [
                        InlineKeyboardButton("📄 BOT STATUS", callback_data = "status_data")
                       ], 
                       [
                        InlineKeyboardButton("📫 UPDATES", url="https://t.me/ts_bots"),
                        InlineKeyboardButton("📕 ABOUT ME", callback_data="about_data")
                       ],
                       [
                        InlineKeyboardButton("💡 HELP", callback_data="help_data"),
                        InlineKeyboardButton("🔐 CLOSE", callback_data="close_data")
                       ]
                   ]
               )
          )
    elif "close_data" in cb_data:
          await cmd.message.delete()
          await cmd.message.reply_to_message.delete()

    elif "markdown_data" in cb_data:
          await cmd.message.edit(
               text=Translation.MARKDOWN_TEXT,
               parse_mode="html", 
               disable_web_page_preview=True, 
               reply_markup=InlineKeyboardMarkup(
                   [
                       [
                        InlineKeyboardButton("⬇️ BACK", callback_data="help_data"),
                        InlineKeyboardButton("🔐 CLOSE", callback_data="close_data")
                       ]
 
                   ] 
               ) 
          )
    elif "status_data" in cb_data:
          if Config.ADMIN_ID == int(cmd.message.chat.id):
             await cmd.message.edit(
                  text=Translation.STATUS_DATA.format(Config.CAPTION_TEXT, Config.CAPTION_POSITION),
                  parse_mode="html", 
                  disable_web_page_preview=True, 
                  reply_markup=InlineKeyboardMarkup(
                      [
                          [
                           InlineKeyboardButton("⬇️ BACK", callback_data="back_data"),
                           InlineKeyboardButton("🔐 CLOSE", callback_data="close_data")
                          ]
 
                      ] 
                  ) 
             )
          else:
             await cmd.message.edit(
                  text=Translation.NOT_ADMIN_TEXT,
                  parse_mode="html", 
                  disable_web_page_preview=True, 
                  reply_markup=InlineKeyboardMarkup(
                      [
                          [
                           InlineKeyboardButton("⬇️ BACK", callback_data="back_data"),
                           InlineKeyboardButton("🔐 CLOSE", callback_data="close_data")
                          ]
 
                      ] 
                  ) 
             )
 
