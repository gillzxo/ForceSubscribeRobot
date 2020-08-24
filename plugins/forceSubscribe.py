import time
from Config import Config
from pyrogram import Client as app
import sql_helpers.forceSubscribe_sql as sql
from pyrogram import Filters, ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant, UsernameNotOccupied, ChatAdminRequired, PeerIdInvalid


@app.on_callback_query(Filters.regex("^onButtonPress$"))
def onButtonPress(client, cb):
  user_id = cb.from_user.id
  chat_id = cb.message.chat.id
  cws = sql.fs_settings(chat_id)
  if cws:
    channel = cws.channel
    if client.get_chat_member(chat_id, user_id).restricted_by.id == (client.get_me()).id:
      try:
        client.get_chat_member(channel, user_id)
        client.unban_chat_member(chat_id, user_id)
      except UserNotParticipant:
        client.answer_callback_query(cb.id, text="ℹ Join The Channel And Press The Button Again.")
    else:
      client.answer_callback_query(cb.id, text="ℹ You Are Muted By Admins For Other Reasons.", show_alert=True)


@app.on_message(Filters.text & ~Filters.private & ~Filters.edited, group=1)
def SendMsg(client, message):
  cws = sql.fs_settings(message.chat.id)
  if cws:
    user_id = message.from_user.id
    if not client.get_chat_member(message.chat.id, user_id).status in ("administrator", "creator") and not user_id in Config.SUDO_USERS:
      first_name = message.from_user.first_name
      channel = cws.channel
      try:
        client.get_chat_member(channel, user_id)
      except UserNotParticipant:
        try:
          sent_message = message.reply_text(
              "ℹ [{}](tg://user?id={}), You Are **Not Subscribed** To My [Channel](https://t.me/{}) Yet. Please 👉 [Join](https://t.me/{}) And **Press The Button Below** [👇](https://telegra.ph/file/e058c8f4a2a8355ccf4fa.jpg) To Unmute Yourself.".format(first_name, user_id, channel, channel),
              disable_web_page_preview=True,
              reply_markup=InlineKeyboardMarkup(
                  [[InlineKeyboardButton("🔔 UnMute Me 🔕", callback_data="onButtonPress")]]
              )
          )
          client.restrict_chat_member(message.chat.id, user_id, ChatPermissions(can_send_messages=False))
        except ChatAdminRequired:
          sent_message.edit("❗ **I'm Not An Admin In Here.**\nMake Me Admin With Ban User Permission Or Turn Off ForceSubscribe.")
      except ChatAdminRequired:
        client.send_message(message.chat.id, text=f"❗ **I'm Not An Admin In @{channel}**\nMake Me Admin In The Channel Or Turn Of ForceSubscribe.")


@app.on_message(Filters.command(["forcesubscribe", "fsub"]) & ~Filters.private)
def config(client, message):
  user = client.get_chat_member(message.chat.id, message.from_user.id)
  if user.status is "creator" or user.user.id in Config.SUDO_USERS:
    chat_id = message.chat.id
    if len(message.command) > 1:
      input_str = message.command[1]
      input_str = input_str.replace("@", "")
      if input_str.lower() in ("off", "no", "disable"):
        sql.disapprove(chat_id)
        message.reply_text("❌ **Force Subscribe is Disabled Successfully.**")
      elif input_str.lower() in ('clear'):
        sent_message = message.reply_text('**🔔 Unmuting All Members Who is Muted By Me...**')
        try:
          for chat_member in client.get_chat_members(message.chat.id, filter="restricted"):
            if chat_member.restricted_by.id == (client.get_me()).id:
                client.unban_chat_member(chat_id, chat_member.user.id)
                time.sleep(1)
          sent_message.edit('✅ **UnMuted All Members Which Are Muted By Me.**')
        except ChatAdminRequired:
          sent_message.edit('❗ **I Am Not An Admin In This Chat.**\nI Can not Unmute Members Because I Am Not An Admin in This Chat, Make Me.')
      else:
        try:
          client.get_chat_member(input_str, "me")
          sql.add_channel(chat_id, input_str)
          message.reply_text(f"✅ **Force Subscribe is Enabled**\nForce Subscribe is Enabled, All The Group Members Have To Subscribe This [channel](https://t.me/{input_str}) in Order To Send Messages In This Group.", disable_web_page_preview=True)
        except UserNotParticipant:
          message.reply_text(f"❗ **Not An Admin in The Channel**\nI'm Not An Admin in The [channel](https://t.me/{input_str}). Add Me As A Admin In Order To Enable ForceSubscribe.", disable_web_page_preview=True)
        except (UsernameNotOccupied, PeerIdInvalid):
          message.reply_text(f"❗ **Invalid Channel Username.**")
        except Exception as err:
          message.reply_text(f"❗ **ERROR:** ```{err}```")
    else:
      if sql.fs_settings(chat_id):
        message.reply_text(f"✅ **Force Subscribe is Enabled in This Chat.**\nFor This [Channel](https://t.me/{sql.fs_settings(chat_id).channel})", disable_web_page_preview=True)
      else:
        message.reply_text("❌ **Force Subscribe is Disabled in This Chat.**")
  else:
      message.reply_text("❗ **Group Creator Required**\nYou Have To Be The Group Creator To Do That.")
