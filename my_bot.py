import os
import re
from telethon import TelegramClient, events, Button
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest
from api import add_channel, delete_channel, get_channels, delete_all_channels, add_word, delete_word, get_words, delete_all_words, get_replace, add_replace
from telethon.tl.types import MessageEntityMentionName

print("Starting deployment...")
try:
    api_id = int(os.environ["API_ID"])
    api_hash = os.environ["API_HASH"]
    bot_token = os.environ["BOT_TOKEN"]
    from_channel = int(os.environ["FROM_CHANNEL"])
    to_channel = int(os.environ["TO_CHANNEL"])

except:
    api_id = "20369082"
    api_hash = "070411cae8f4510368f4c94f82903b1a"
    from_channel = int(-1001710050962)
    to_channel = int(-1001460238566)



bot = TelegramClient('botop', api_id, api_hash).start()

wordBlacklist = get_words()
wordReplace = get_replace()
emoj = re.compile("["
                  u"\U0001F600-\U0001F64F"  # emoticons
                  u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                  u"\U0001F680-\U0001F6FF"  # transport & map symbols
                  u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                  u"\U00002500-\U00002BEF"  # chinese char
                  u"\U00002702-\U000027B0"
                  u"\U00002702-\U000027B0"
                  u"\U000024C2-\U0001F251"
                  u"\U0001f926-\U0001f937"
                  u"\U00010000-\U0010ffff"
                  u"\u2640-\u2642"
                  u"\u2600-\u2B55"
                  u"\u200d"
                  u"\u23cf"
                  u"\u23e9"
                  u"\u231a"
                  u"\ufe0f"  # dingbats
                  u"\u3030"
                  "]+", re.UNICODE)


def is_english(text):
    try:
        text = re.sub(emoj, '', text)
        # remove special characters
        text = re.sub(r'[^\w\s]', '', text)
        text.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True


def is_in_blacklist(text):
    # check words
    if words:
        for word in words:
            if word[0] in text:
                return True
    return False


@bot.on(events.NewMessage(pattern="^/start$|hi|hello|hey|HI|HELLO|HEY", func=lambda e: e.is_private))
async def _(event):
    # ok = await bot(GetFullUserRequest(event.sender_id))
    if event.chat_id == 1076120105 or event.chat_id == 747953161:
        # say hi vith name
        sender = await event.get_sender()
        await bot.send_file(sender, 'AnimatedSticker.tgs')
        await event.reply("Hi ," + sender.username + " 👋 !")
        await bot.send_message(sender, "use `/help` to see all commands")
        return
    await event.reply(f"Hi ! I am a bot of Mr. Nisal Chandrasekara,\n please contact @CMNisal to get access to this bot")


@bot.on(events.NewMessage(pattern="^/help$", func=lambda e: e.is_private))
async def help(event):
    if event.chat_id == 1076120105 or event.chat_id == 747953161:
        await event.reply("**Help menu**\n\n😎This bot will send all new posts in one channel to the .😊 \n\n**Commands**\n\n🪛`/add` - Add a channel to the list of channels to be forwarded.\n🪛`/delete` - Delete a channel from the list of channels to be forwarded.\n🪛`/list` - List all channels that are being forwarded.\n`/addword` - Add a word to the blacklist.\n🪛`/delword` - Delete a word from the blacklist.\n🪛`/listwords` - List all words in the blacklist.\n🪛`/deleteallword` - Delete all words from the blacklist.\n🪛`/deleteall` - Delete all channels from the list of channels to be forwarded.\n\n**Note**\n\n🔸This bot will only forward posts from channels that are in English.\n🔸This bot will not forward posts that contain words in the blacklist.\n\n**Support**\n\n🔹If you have any questions, please contact @Leoglarrix")

# use exactly this name /add


@bot.on(events.NewMessage(pattern="^/add$"))
async def add(event):
    if event.chat_id == 1076120105 or event.chat_id == 747953161:

        sender = await event.get_sender()
        SENDER = sender.id

        # Start a conversation and /cancel it
        async with bot.conversation(await event.get_chat(), exclusive=True) as conv:
            # ask for channel id
            await conv.send_message("Please send the **channel id**🆔 or **forward**▶️ a message from the channel you want to add. `/cancel` to cancel the process.")
            response = await conv.get_response()
            if response.text == "/cancel":
                await conv.send_message("Cancelled❎")
                return

            try:
                channel_id = int(response.text)
            except:
                channel_id = - \
                    (response.fwd_from.from_id.channel_id+1000000000000)

            if channel_id == to_channel:
                await conv.send_message("You can't add this channel.")
                return

            # try to join channel
            try:
                await bot(JoinChannelRequest(channel_id))
            except:
                # join to channel by invite link
                await conv.send_message("Please send the **invite link**🔗 of the channel you want to add.")
                response = await conv.get_response()
                if response.text == "/cancel":
                    await conv.send_message("Cancelled❎")
                    return
                await conv.send_message("I can't join that channel,  Manually join and")
                await add(event)
                return

            # ask with button to select all or media  or text
            await conv.send_message("Please send letter of the Message Filter you want to add \nA- All\nMT- Media with Text\nM- Media Only\nT- Text Only")
            response = await conv.get_response()
            if response.text == "/cancel":
                # leave channel
                await bot(LeaveChannelRequest(channel_id))
                await conv.send_message("Cancelled❎")
                return
            if response.text.lower() == "a":
                channel_type = "all"
            elif response.text.lower() == "mt":
                channel_type = "media_text"
            elif response.text.lower() == "m":
                channel_type = "media"
            elif response.text.lower() == "t":
                channel_type = "text"

            await conv.send_message("Please send the footer you want to add to the posts")
            response = await conv.get_response()
            if response.text == "/cancel":
                # leave channel
                await bot(LeaveChannelRequest(channel_id))
                await conv.send_message("Cancelled❎")
                return
            footer = response.text

            # join channel
            try:
                # join channel and get channel id
                add_channel(str(channel_id), channel_type, footer)
                await conv.send_message("✅Channel added successfully  \nuse  `/list` to see the list of channels")
            except:
                await conv.send_message("I can't join that channel,  Manually join and try to add again")
                await add(event)
                return


@bot.on(events.NewMessage(pattern="^/list$"))
async def list_channels(event):
    if event.chat_id == 1076120105 or event.chat_id == 747953161:

        sender = await event.get_sender()
        SENDER = sender.id
        channels = get_channels()
        channels_list = {}
        async for d in bot.iter_dialogs():
            if d.is_channel:
                channels_list[-(d.entity.id+1000000000000)] = d.name
        if channels:
            msg = "Here is the list of channels you have added : \n\n"
            for channel in channels:
                msg += f"🟢 Channel Name : {channels_list[int(channel[0])]} \nChannel ID : {channel[0]} \nMessage Filter : {channel[1]} \nFooter : {channel[2]} \n\n"

            msg += "`/delete` - Delete a channel from the list of channels to be forwarded.\n"
            await event.reply(msg)
        else:
            await event.reply("You haven't added any channel yet ❗️")


@bot.on(events.NewMessage(pattern="^/delete$"))
async def delete(event):
    if event.chat_id == 1076120105 or event.chat_id == 747953161:

        sender = await event.get_sender()
        SENDER = sender.id
        channels = get_channels()
        channels_list = {}
        async for d in bot.iter_dialogs():
            if d.is_channel:
                channels_list[-(d.entity.id+1000000000000)] = d.name
        if channels:
            msg = "Here is the list of channels you have added : \n"
            index = 1
            for channel in channels:
                msg += f"{index}. Channel Name : {channels_list[int(channel[0])]} \nChannel id : {channel[0]} \nChannel type : {channel[1]} \nFooter : {channel[2]} \n\n"
                index += 1
            await event.reply(msg)
            async with bot.conversation(await event.get_chat(), exclusive=True) as conv:
                await conv.send_message("Please send the indexes of the channels you want to delete separated by a space. \nExample : `1 2 3`")
                response = await conv.get_response()
                if response.text == "/cancel":
                    await conv.send_message("Cancelled❎")
                    return
                index = response.text
                indexes = index.split(" ")

                # if indexes are not numbers
                for i in indexes:
                    if not i.isdigit():
                        await conv.send_message("Please send only numbers separated by a space.")
                        return

                # if indexes are valid
                if not all(int(i) <= len(channels) for i in indexes):
                    await conv.send_message("Invalid indexes ❗️")
                    return

                for index in indexes:

                    index = int(index)
                    if index > len(channels):
                        await conv.send_message("Invalid index : "+index)
                    else:
                        channel_id = channels[index-1][0]
                        delete_channel(str(channel_id))
                        # leave channel
                        await bot(LeaveChannelRequest(int(channel_id)))
                        await conv.send_message("✅Channel "+channel_id+" deleted successfully")
                return

        else:
            await event.reply("You haven't added any channel yet !")

# add word to blacklist


@bot.on(events.NewMessage(pattern="^/addword$"))
async def addword(event):
    if event.chat_id == 1076120105 or event.chat_id == 747953161:

        sender = await event.get_sender()
        SENDER = sender.id
        async with bot.conversation(await event.get_chat(), exclusive=True) as conv:
            await conv.send_message("Please send the word you want to add to the blacklist")
            response = await conv.get_response()
            if response.text == "/cancel":
                await conv.send_message("Cancelled❎")
                return
            word = response.text
            add_word(word)
            await conv.send_message("✅Word added successfully")
            words = get_words()

# delete word from blacklist


@bot.on(events.NewMessage(pattern="^/delword$"))
async def delword(event):
    if event.chat_id == 1076120105 or event.chat_id == 747953161:

        sender = await event.get_sender()
        SENDER = sender.id
        words = get_words()
        if words:
            msg = "Here is the list of words you have added : \n"
            index = 1
            for word in words:
                msg += f"{index}. {word[0]} \n"
                index += 1
            await event.reply(msg)
            async with bot.conversation(await event.get_chat(), exclusive=True) as conv:
                await conv.send_message("Please send the indexes of the words you want to delete separated by a space. \nExample : `1 2 3`")
                response = await conv.get_response()
                if response.text == "/cancel":
                    await conv.send_message("Cancelled❎")
                    return
                index = response.text
                indexes = index.split(" ")

                # if indexes are not numbers
                for i in indexes:
                    if not i.isdigit():
                        await conv.send_message("Please send only numbers separated by a space.")
                        return

                # if indexes are valid
                if not all(int(i) <= len(words) for i in indexes):
                    await conv.send_message("Invalid indexes ❗️")
                    return

                for index in indexes:

                    index = int(index)
                    if index > len(words):
                        await conv.send_message("Invalid index : "+index)
                    else:
                        word = words[index-1][0]
                        delete_word(word)
                        await conv.send_message("✅Word "+word+" deleted successfully")
                        words = get_words()
                return

        else:
            await event.reply("You haven't added any word yet !")

# list words


@bot.on(events.NewMessage(pattern="^/listwords$"))
async def listwords(event):
    if event.chat_id == 1076120105 or event.chat_id == 747953161:

        sender = await event.get_sender()
        SENDER = sender.id
        words = get_words()
        if words:
            msg = "Here is the list of words you have added : \n\n"
            for word in words:
                msg += f"🟢 {word[0]} \n"

            msg += "`/delword` - Delete a word from the list of words to be filtered.\n"
            await event.reply(msg)
        else:
            await event.reply("You haven't added any word yet ❗️")

# add replacement


@bot.on(events.NewMessage(pattern="^/addrep$"))
async def addrep(event):
    if event.chat_id == 1076120105 or event.chat_id == 747953161:

        sender = await event.get_sender()
        SENDER = sender.id
        async with bot.conversation(await event.get_chat(), exclusive=True) as conv:
            await conv.send_message("Please send the word with the replacement you want to add to the list of replacements \nuse `|` or `:` or `=` to separate the word and the replacement \nExample : `word|replacement` or `word:replacement` or `word=replacement`")
            response = await conv.get_response()
            if response.text == "/cancel":
                await conv.send_message("Cancelled❎")
                return
            word = response.text
            if "|" in word:
                word = word.split("|")
            elif ":" in word:
                word = word.split(":")
            elif "=" in word:
                word = word.split("=")
            else:
                await conv.send_message("Invalid format ❗️")
                return
            if len(word) != 2:
                await conv.send_message("Invalid format ❗️")
                return
            add_replacement(word[0], word[1])
            await conv.send_message("✅Replacement added successfully")


@bot.on(events.NewMessage(incoming=True))
async def op(event):

    # get unencoded message
    message = event.raw_text
    print(message)

    # replace emojis with custom emojis
    message = emoji.demojize(message)
    message = message.replace(":thumbs_up_sign:", "👍")
    message = message.replace(":thumbs_down_sign:", "👎")
    message = message.replace(":white_heavy_check_mark:", "✅")
    # await bot.send_message(user_id, )

    # unpickle
    #event = pickle.load(open("event.pickle", "rb"))
    if event.fwd_from or event.poll or not is_english(event.text) or is_in_blacklist(event.text):
        return
    channels = get_channels()
    channel_ids = [channel[0] for channel in channels]
    # if channel is not in the list of channels
    channel_id = str(event.chat_id)
    if channel_id not in channel_ids:
        return
    # get channel tuple from channels list
    channel = [channel for channel in channels if channel[0] == channel_id][0]
    footer = channel[2]
    text = event.text
    #remove @channelusername
    text = re.sub(r'@([A-Za-z0-9_]+)', '', text)
    # if ends with multiple new lines remove them
    text = re.sub(r'\n+$', '', text)

    # if channel type is all
    if channel[1] == "all":
        if event.photo:
            try:
                photo = event.media.photo
                await bot.send_file(to_channel, photo,  caption=text+'\n\n'+footer, link_preview=False)
            except:
                await bot.send_message(to_channel, text+'\n\n'+footer, link_preview=False)
        elif event.media:
            try:
                if event.media.webpage:
                    await bot.send_message(to_channel, text+'\n\n'+footer, link_preview=False)
                    return
            except:
                media = event.media.document
                await bot.send_file(to_channel, media, caption=text+'\n\n'+footer, link_preview=False)
                return
        else:
            await bot.send_message(to_channel, text+'\n\n'+footer, link_preview=False)
    # if channel type is media_text
    elif channel[1] == "media_text":
        if event.photo:
            photo = event.media.photo
            await bot.send_file(to_channel, photo,  caption=text+'\n\n'+footer, link_preview=False)
        elif event.media:
            try:
                if event.media.webpage:
                    await bot.send_message(to_channel, text+'\n\n'+footer, link_preview=False)
                    return
            except:
                media = event.media.document
                await bot.send_file(to_channel, media, caption=text+'\n\n'+footer, link_preview=False)
                return
    # if channel type is media
    elif channel[1] == "media":
        if event.photo:
            photo = event.media.photo
            await bot.send_file(to_channel, photo,  caption=footer, link_preview=False)
        elif event.media:
            try:
                if event.media.webpage:
                    return
            except:
                media = event.media.document
                await bot.send_file(to_channel, media, caption=footer, link_preview=False)
                return
    # if channel type is text
    elif channel[1] == "text":
        if event.photo:
            return
        elif event.media:
            try:
                if event.media.webpage:
                    await bot.send_message(to_channel, text+'\n\n'+footer, link_preview=False)
                    return
            except:
                return
        else:
            await bot.send_message(to_channel, text+'\n\n'+footer, link_preview=False)


# @bot.on(events.NewMessage(incoming=True, chats=[cryptomemes]))
# async def nn(event):
# if not event.is_private:
#         try:
            # if event.poll:
            #     return
#             if event.photo:
#                 photo = event.media.photo
#                 await bot.send_file(to_channel, photo, caption='#Crypto_Memes \n🔰Join us: @CryptoLeoNews', link_preview=False)
#             elif event.media:
#                 try:
#                     if event.media.webpage:
#                         await bot.send_message(to_channel, event.text+'\n\n#Crypto_Memes \n🔰Join us: @CryptoLeoNews', link_preview=False)
#                         return
#                 except:
#                     media = event.media.document
#                     await bot.send_file(to_channel, media, caption=event.text+'\n\n#Crypto_Memes \n🔰Join us: @CryptoLeoNews', link_preview=False)
#                     return
#         except:
#             print(
#                 "TO_CHANNEL ID is wrong or I can't send messages there (make me admin).")


# @bot.on(events.NewMessage(incoming=True, chats=[from_channel_testing]))
# async def cc(event):
#     if not event.is_private:
#         try:
            # if event.fwd_from:
            #     return
#             if event.poll:
#                 return
        #     if event.photo:
        #         photo = event.media.photo
        #         await bot.send_file(to_channel, photo,  caption='#Crypto_Memes \n🔰Join us: @CryptoLeoNews', link_preview=False)
        #     elif event.media:
        #         try:
        #             if event.media.webpage:
        #                 await bot.send_message(to_channel, event.text, link_preview=False)
        #                 return
        #         except:
        #             media = event.media.document
        #             await bot.send_file(to_channel, media, caption=event.text, link_preview=False)
        #             return
        #     else:
        #         await bot.send_message(to_channel, event.text, link_preview=False)
        # except:
        #     print(
        #         "TO_CHANNEL ID is wrong or I can't send messages there (make me admin).")
# messages=get_messages("https://t.me/s/catalystofficial")

# #send messages to channel
# for message in messages:
#     bot.send_message(to_channel, message)


async def main():
    # Now you can use all client methods listed below, like for example...
    await bot.send_message(to_channel, 'Hello to myself!')


# print("Bot has been deployed.")
bot.run_until_disconnected()
