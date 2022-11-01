from pyrogram import Client, filters, enums
from api import add_channel,\
    delete_channel, get_channels, \
    delete_all_channels, add_word, \
    delete_word, get_words, \
    delete_all_words, get_replace,\
    add_replace, delete_replace, get_replacements

import re
from convopyro import Conversation
from convopyro import listen_message
import pandas as pd

api_id = 20369082
api_hash = "070411cae8f4510368f4c94f82903b1a"

# app = Client("my_account", api_id=api_id, api_hash=api_hash)
# app.run()

print("Starting deployment...")
app = Client("my_account")
Conversation(app)

wordBlacklist = get_words()
wordReplace = get_replace()
channelList = get_channels()
replaceList ={r"\b{}\b".format(k): v for k, v in get_replacements().items()}
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
to_channel_id = -1001834671869


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
    if wordBlacklist:
        for word in wordBlacklist:
            if word[0] in text:
                return True
    return False


def get_html_emoj(emoji_id):
    return


@app.on_message(filters.command(["help"]))
async def help(client, message):
    chat_id = message.chat.id
    if chat_id == 1076120105 or chat_id == 196536622:
        await message.reply_text("**Help menu**\n\n😎This bot will send all new posts in one channel to the .😊 \n\n" +
                                 "**Commands**\n\n" +
                                 " \t\t**Manage Channels**\n" +
                                 "🪛/add - Add a channel to the list of channels to be forwarded.\n" +
                                 "🪛/delete - Delete a channel from the list of channels to be forwarded.\n" +
                                 "🪛/list - List all channels that are being forwarded.\n" +
                                 "🪛/deleteall - Delete all channels from the list of channels to be forwarded.\n\n" +
                                 "\t\t**Manage Word Blacklist**\n" +
                                 "🪛/addword - Add a word to the blacklist.\n" +
                                 "🪛/delword - Delete a word from the blacklist.\n" +
                                 "🪛/listwords - List all words in the blacklist.\n" +
                                 "🪛/deleteallword - Delete all words from the blacklist.\n\n" +
                                 "\t\t**Manage Word Replace**\n" +
                                 "🪛/addrep - Add a word to the replace list.\n" +
                                 "🪛/delreps - Delete a word from the replace list.\n" +
                                 "🪛/listreps - List all words in the replace list.\n\n" +
                                 "**Note**\n🔸This bot will only forward posts from channels that are in English.\n" +
                                 "🔸This bot will not forward posts that contain words in the blacklist.\n" +
                                 "🔸This bot will replace words in the replace list with the corresponding word in the replace list." +
                                 "\n\n**Support**\n🔹If you have any questions, please contact @CMNisal")


@ app.on_message(filters.command(["add"]))
async def add(client, message):
    chat_id = message.chat.id
    if chat_id == 1076120105 or chat_id == 196536622:
        # start a conversation
        await client.send_message(chat_id, "Please send the **channel id**🆔 or **forward**▶️ a message from the channel you want to add. `/cancel` to cancel the process.")
        answer = await listen_message(client, chat_id, timeout=None)
        if answer.text == "/cancel":
            await client.listen.Cancel(filters.user(chat_id))
            await app.send_message(chat_id, "Cancelled❎")
            return

        if answer.forward_from_chat:
            channel_id = answer.forward_from_chat.id
        else:
            channel_id = answer.text
        channel_name = answer.forward_from_chat.username
        # try to join channel
        try:
            await app.join_chat(channel_id)
        except:
            await app.send_message(chat_id, "I can't join that channel,  Manually join and")
            await add(client, message)
            return
        # ask with button to select all or media  or text
        await app.send_message(chat_id, "Please send letter of the Message Filter you want to add \nA- All\nMT- Media with Text\nM- Media Only\nT- Text Only")

        answer = await listen_message(client, chat_id, timeout=None)
        if answer.text == "/cancel":
            await client.listen.Cancel(filters.user(chat_id))
            await app.send_message(chat_id, "Cancelled❎")
            return

        if answer.text.lower() == "a":
            channel_type = "all"
        elif answer.text.lower() == "mt":
            channel_type = "media_text"
        elif answer.text.lower() == "m":
            channel_type = "media"
        elif answer.text.lower() == "t":
            channel_type = "text"

        await app.send_message(chat_id, "Please send the footer you want to add to the posts")
        answer = await listen_message(client, chat_id, timeout=None)
        if answer.text == "/cancel":
            await client.listen.Cancel(filters.user(chat_id))
            await app.send_message(chat_id, "Cancelled❎")
            return

        channel_footer = answer.text
        if answer.entities:
            for entity in answer.entities:
                if entity.custom_emoji_id:
                    channel_footer = channel_footer.replace(
                        channel_footer[entity.offset], f"<emoji id='{entity.custom_emoji_id}'>🔥</emoji>")

        add_channel(str(channel_id), channel_type,
                    channel_footer, channel_name)
        await app.send_message(chat_id, "✅Channel added successfully  \nuse  `/list` to see the list of channels")
        channelList = get_channels()
        return
        # await message.reply_text("Please send the **channel id**🆔 or **forward**▶️ a message from the channel you want to add. `/cancel` to cancel the process.")

# list


@app.on_message(filters.command(["list"]))
async def list(client, message):
    chat_id = message.chat.id
    if chat_id == 1076120105 or chat_id == 196536622:

        channels = get_channels()
        if channels:
            msg = "Here is the list of channels you have added : \n\n"
            for channel in channels:
                msg += f"🟢 Channel Name : {channel[3]} \nChannel ID : {channel[0]} \nMessage Filter : {channel[1]} \nFooter : {channel[2]} \n\n"

            msg += "`/delete` - Delete a channel from the list of channels to be forwarded.\n"
            await message.reply(msg)
        else:
            await message.reply("You haven't added any channel yet ❗️")


@app.on_message(filters.command(["delete"]))
async def delete(client, message):
    chat_id = message.chat.id
    if chat_id == 1076120105 or chat_id == 196536622:

        channels = get_channels()
        if channels:
            msg = "Here is the list of channels you have added : \n"
            index = 1
            for channel in channels:
                msg += f"{index}. Channel Name : {channel[3]} \nChannel id : {channel[0]} \nChannel type : {channel[1]} \nFooter : {channel[2]} \n\n"
                index += 1
            await message.reply(msg)
            await app.send_message(chat_id, "Please send the indexes of the channels you want to delete separated by a space. \nExample : `1 2 3`")
            answer = await listen_message(client, chat_id, timeout=None)
            if answer.text == "/cancel":
                await app.send_message(chat_id, "Cancelled❎")
                return
            index = answer.text
            indexes = index.split(" ")

            # if indexes are not numbers
            for i in indexes:
                if not i.isdigit():
                    await app.send_message(chat_id, "Please send only numbers separated by a space.")
                    return

            # if indexes are valid
            if not all(int(i) <= len(channels) for i in indexes):
                await app.send_message(chat_id, "Invalid indexes ❗️")
                return

            for index in indexes:

                index = int(index)
                if index > len(channels):
                    await app.send_message(chat_id, "Invalid index : "+index)
                else:
                    channel_id = channels[index-1][0]
                    delete_channel(str(channel_id))
                    # leave channel
                    await app.leave_chat(channel_id, delete=True)
                    await app.send_message(chat_id, "✅Channel "+channel_id+" deleted successfully")
                    channelList = get_channels()
            return

        else:
            await message.reply("You haven't added any channel yet !")

# add word to blacklist


@app.on_message(filters.command(["addword"]))
async def addword(client, message):
    chat_id = message.chat.id
    if chat_id == 1076120105 or chat_id == 196536622:
        await app.send_message(chat_id, "Please send the word you want to add to the blacklist")
        answer = await listen_message(client, chat_id, timeout=None)
        if answer.text == "/cancel":
            await app.send_message(chat_id, "Cancelled❎")
            return
        word = answer.text
        add_word(word)
        await app.send_message(chat_id, "✅Word added successfully")
        words = get_words()

# delete words from blacklist


@app.on_message(filters.command(["delword"]))
async def delword(client, message):

    chat_id = message.chat.id
    if chat_id == 1076120105 or chat_id == 196536622:
        words = get_words()
        if words:
            msg = "Here is the list of words you have added : \n"
            index = 1
            for word in words:
                msg += f"{index}. {word[0]} \n"
                index += 1
            await message.reply(msg)
            await app.send_message(chat_id, "Please send the indexes of the words you want to delete separated by a space. \nExample : `1 2 3`")
            answer = await listen_message(client, chat_id, timeout=None)
            if answer.text == "/cancel":
                await app.send_message(chat_id, "Cancelled❎")
                return
            index = answer.text
            indexes = index.split(" ")

            # if indexes are not numbers
            for i in indexes:
                if not i.isdigit():
                    await app.send_message(chat_id, "Please send only numbers separated by a space.")
                    return

            # if indexes are valid
            if not all(int(i) <= len(words) for i in indexes):
                await app.send_message(chat_id, "Invalid indexes ❗️")
                return

            for index in indexes:
                index = int(index)
                if index > len(words):
                    await capp.send_message(chat_id, "Invalid index : "+index)
                else:
                    word = words[index-1][0]
                    delete_word(word)
                    await app.send_message(chat_id, "✅Word "+word+" deleted successfully")
                    words = get_words()
            return

        else:
            await message.reply("You haven't added any word yet !")

# list words


@app.on_message(filters.command(["listwords"]))
async def listwords(client, message):
    chat_id = message.chat.id
    if chat_id == 1076120105 or chat_id == 196536622:
        words = get_words()
        if words:
            msg = "Here is the list of words you have added : \n\n"
            for word in words:
                msg += f"🟢   {word[0]} \n"
            msg += "`/delword` - Delete a word from the list of words to be filtered.\n"
            await message.reply(msg)
        else:
            await message.reply("You haven't added any word yet ❗️")

# add replacement


@app.on_message(filters.command(["addrep"]))
async def addrep(client, message):
    chat_id = message.chat.id
    if chat_id == 1076120105 or chat_id == 196536622:

        await app.send_message(chat_id, "Please send the word with the replacement you want to add to the list of replacements \nuse `|` or `:` or `=` to separate the word and the replacement \n\nExample : 😲=<emoji id='5381855971943389791'>🔥</emoji>", parse_mode=enums.ParseMode.HTML)
        answer = await listen_message(client, chat_id, timeout=None)

        if answer.text == "/cancel":
            await app.send_message(chat_id, "Cancelled❎")
            return

        word = str(answer.text)
        if "|" in word:
            wordList = word.split("|")
        elif ":" in word:
            wordList = word.split(":")
        elif "=" in word:
            wordList = word.split("=")
        else:
            await app.send_message(chat_id, "Invalid format ❗️")
            return
        if len(wordList) != 2:
            await app.send_message(chat_id, "Invalid format ❗️")
            return
        # replace emojis in text with custom emoji id in message.entities
        #"Lalaalla <emoji id=\""+str(ent.custom_emoji_id)+"\">🔥</emoji>"
        if answer.entities:
            for entity in answer.entities:
                if entity.custom_emoji_id:
                    wordList[1] = wordList[1].replace(
                        word[entity.offset-1], f"<emoji id='{entity.custom_emoji_id}'>🔥</emoji>")
        print(wordList)

        add_replace(wordList[0], wordList[1])
        await app.send_message(chat_id, "✅Replacement added successfully")
        replaceList = {r"\b{}\b".format(k): v for k, v in get_replacements().items()}

# delete replacement


@app.on_message(filters.command(["delreps"]))
async def delrep(client, message):
    chat_id = message.chat.id
    if chat_id == 1076120105 or chat_id == 196536622:
        replacements = get_replace()
        if replacements:
            msg = "Here is the list of replacements you have added : \n"
            index = 1
            for replacement in replacements:
                msg += f"{index}. {replacement[0]} ➡️ {replacement[1]} \n\n"
                index += 1
            await message.reply(msg)
            await app.send_message(chat_id, "Please send the indexes of the replacements you want to delete separated by a space. \nExample : `1 2 3`")
            answer = await listen_message(client, chat_id, timeout=None)
            if answer.text == "/cancel":
                await app.send_message(chat_id, "Cancelled❎")
                return
            index = answer.text
            indexes = index.split(" ")

            # if indexes are not numbers
            for i in indexes:
                if not i.isdigit():
                    await app.send_message(chat_id, "Please send only numbers separated by a space.")
                    return

            # if indexes are valid
            if not all(int(i) <= len(replacements) for i in indexes):
                await app.send_message(chat_id, "Invalid indexes ❗️")
                return

            for index in indexes:
                index = int(index)
                if index > len(replacements):
                    await app.send_message(chat_id, "Invalid index : "+index)
                else:
                    replacement = replacements[index-1][0]
                    delete_replace(replacement)
                    await app.send_message(chat_id, "✅Replacement "+replacement+" deleted successfully")
                    replaceList = {r"\b{}\b".format(k): v for k, v in get_replacements().items()}
            return

        else:
            await message.reply("You haven't added any replacement yet !")

# list replacements


@app.on_message(filters.command(["listreps"]))
async def listreps(client, message):
    chat_id = message.chat.id
    if chat_id == 1076120105 or chat_id == 196536622:
        replacements = get_replace()
        if replacements:
            msg = "Here is the list of replacements you have added : \n\n"
            for replacement in replacements:
                msg += f"🟢 {replacement[0]} ➡️ {replacement[1]} \n\n"
            msg += "`/delreps` - Delete a replacement from the list of replacements.\n"
            print(msg)
            await message.reply(msg, parse_mode=enums.ParseMode.HTML)
        else:
            await message.reply("You haven't added any replacement yet ❗️")


@app.on_message(filters.incoming & ~filters.private & ~filters.forwarded & ~filters.poll)
async def onMessage(client, message):
    # add reaction to the sent message
    await client.send_chat_action(to_channel_id, enums.ChatAction.TYPING)
    chat_id = message.chat.id

    channels = channelList
    channel_ids = [channel[0] for channel in channels]
    # if channel is not in the list of channels
    channel_id = str(chat_id)
    if channel_id not in channel_ids:
        return

    if message.caption or message.text:
        text = message.caption or message.text
        if is_in_blacklist(text) or not is_english(text):
            return
        #remove @channelusername
        text = re.sub(r'@([A-Za-z0-9_]+)', '', text)
        # if ends with multiple new lines remove them
        text = re.sub(r'\n+$', '', text)
        df = pd.DataFrame({"Text": [text]})
        df["Text"] = df["Text"].replace(replaceList, regex=True)
        text=df["Text"][0]
    else:
        text = ""

    print(text)

    # get channel tuple from channels list
    channel = [channel for channel in channels if channel[0] == channel_id][0]
    footer = channel[2]
    caption = text+"\n\n"+footer
    # if channel type is all
    if channel[1] == "all":
        if message.media_group_id:
            await client.copy_media_group(to_channel_id, message.chat.id, message.id, captions=caption)
        elif message.photo:
            await client.send_photo(to_channel_id, photo=message.photo.file_id, caption=caption, parse_mode=enums.ParseMode.HTML)
        elif message.video:
            await client.send_video(to_channel_id, message.video.file_id, caption=caption, parse_mode=enums.ParseMode.HTML)
        elif message.audio:
            await client.send_audio(to_channel_id, message.audio.file_id, caption=caption, parse_mode=enums.ParseMode.HTML)
        elif message.document:
            await client.send_document(to_channel_id, message.document.file_id, caption=caption, parse_mode=enums.ParseMode.HTML)
        elif message.text:
            await client.send_message(to_channel_id, text, parse_mode=enums.ParseMode.HTML, entities=message.entities, disable_web_page_preview=True)

    # if channel type is media_text
    elif channel[1] == "media_text":
        if message.media_group_id:
            await client.copy_media_group(to_channel_id, message.chat.id, message.id, captions=caption)
        elif message.photo:
            await client.send_photo(to_channel_id, photo=message.photo.file_id, caption=caption, parse_mode=enums.ParseMode.HTML)
        elif message.video:
            await client.send_video(to_channel_id, message.video.file_id, caption=caption, parse_mode=enums.ParseMode.HTML)
        elif message.audio:
            await client.send_audio(to_channel_id, message.audio.file_id, caption=caption, parse_mode=enums.ParseMode.HTML)
        elif message.document:
            await client.send_document(to_channel_id, message.document.file_id, caption=caption, parse_mode=enums.ParseMode.HTML)
    # if channel type is media
    elif channel[1] == "media":
        if message.media_group_id:
            await client.copy_media_group(to_channel_id, message.chat.id, message.id, captions=caption)
        elif message.photo:
            await client.send_photo(to_channel_id, photo=message.photo.file_id, captions=caption)
        elif message.video:
            await client.send_video(to_channel_id, message.video.file_id, captions=caption)
        elif message.audio:
            await client.send_audio(to_channel_id, message.audio.file_id, captions=caption)
        elif message.document:
            await client.send_document(to_channel_id, message.document.file_id, captions=caption)
    # if channel type is text
    elif channel[1] == "text":
        if message.text:
            await client.send_message(to_channel_id, text, parse_mode=enums.ParseMode.HTML, entities=message.entities, disable_web_page_preview=True)
    await app.send_chat_action(to_channel_id, enums.ChatAction.CANCEL)

app.run()  # Automatically start() and idle()
