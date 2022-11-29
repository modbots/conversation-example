from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyrogram import Client, filters, enums
import os
import asyncio
import psutil
from api import add_channel,\
    delete_channel, get_channels, \
    delete_all_channels, add_word, \
    delete_word, get_words, \
    delete_all_words, get_replace,\
    add_replace, delete_replace, get_replacements,add_setting,get_setting

import re
from convopyro import Conversation
from convopyro import listen_message
import pandas as pd
from random import choice as rand_choice
import requests


def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)


api_id = 20369082
api_hash = "070411cae8f4510368f4c94f82903b1a"
os.environ['NO_PROXY'] = '127.0.0.1'
# app = Client("my_account", api_id=api_id, api_hash=api_hash)
# app.run()


app = Client("my_account")
Conversation(app)

wordBlacklist = get_words()
wordReplace = get_replace()
channelList = get_channels()
channel_ids = [channel[0] for channel in channelList]
admin_chat_ids=[1076120105,196536622]
replaceList = get_replacements()
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



to_channels = {-1001367920373: "@CMNisal", -
               1001414316119: "@CryptoRoomNews", -1001313534745: "@ApeDiamonds"}



async def server_status():
    msg = "Server details : \n"
    msg += "🖥 CPU : "+str(psutil.cpu_percent())+"%\n"
    msg += "🎟 RAM : "+str(psutil.virtual_memory().percent)+"%\n"
    msg += "💾 Disk : "+str(psutil.disk_usage('/').percent)+"%\n"
    sentmsg = await message.reply(msg)
    for chat_id in admin_chat_ids:
        previous_message_id=get_setting(chat_id+"_server_message_id")
        print(previous_message_id)
        if previous_message_id:
            previous_message_id=previous_message_id[0][0]
            await app.edit_message_text(chat_id,previous_message_id,msg)
         

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
    global wordBlacklist
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
    if chat_id in admin_chat_ids:
        await message.reply_text("**Help menu**\n\n😎This bot will send all new posts in one channel to the CMNisal😊 \n\n" +
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
                                 "\t\t**Manage Whatsapp Groups**\n" +
                                 "🪛/whcr - Creates a whatsapp group.\n" +
                                 "🪛/whdel - Delete a whatsapp group.\n" +
                                 "🪛/whlist - List all whatsapp groups.\n\n" +
                                 "\t\t**Manage Server**\n" +
                                 "🪛/server - Check the server status.\n" +
                                 "🪛/restart - Restart the server.\n" +
                                 "🪛/whrst - Restart the whatsapp service.\n" +
                                 "🪛/botrst - Restart the forwarding bot.\n\n" +
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
        channel_name = answer.forward_from_chat.title

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
                        answer.text[entity.offset:entity.offset+entity.length], f"<emoji id='{entity.custom_emoji_id}'>{answer.text[entity.offset:entity.offset+entity.length]}</emoji>")

        add_channel(str(channel_id), channel_type,
                    channel_footer, channel_name)
        await app.send_message(chat_id, "✅Channel added successfully  \nuse  `/list` to see the list of channels")
        global channelList
        global channel_ids
        channelList = get_channels()
        channel_ids = [channel[0] for channel in channelList]

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
                    global channelList
                    global channel_ids
                    channelList = get_channels()
                    channel_ids = [channel[0] for channel in channelList]

            return

        else:
            await message.reply("You haven't added any channel yet !")

# manage whatsapp groups

# create whatsapp group


@app.on_message(filters.command(["whcr"]))
async def createwh(client, message):
    chat_id = message.chat.id
    if chat_id == 1076120105 or chat_id == 196536622:
        if " " in message.text:
            group_name = message.text.split(" ", 1)[1]
            # create whatsapp group
            try:
                response = requests.post('http://127.0.0.1:3000/create/group/', json={
                    'groupName': group_name}).json()
                # response contains group name and group chat link
                await app.send_message(chat_id, "✅Group created successfully \nGroup Name : "+response['groupName']+"\nGroup ID : "+response['groupId']+"\nInvite Link : "+response['inviteLink'])
            except:
                await app.send_message(chat_id, "❌Failed to add group")
            return

        await app.send_message(chat_id, "Please send the name of the group you want to create")
        answer = await listen_message(client, chat_id, timeout=None)
        if answer.text == "/cancel":
            await app.send_message(chat_id, "Cancelled❎")
            return
        group_name = answer.text
        await app.send_message(chat_id, "Please send the description of the group you want to create")
        answer = await listen_message(client, chat_id, timeout=None)
        if answer.text == "/cancel":
            await app.send_message(chat_id, "Cancelled❎")
            return
        group_description = answer.text

        try:
            response = requests.post('http://127.0.0.1:3000/create/group/', json={
                                     'groupName': group_name, 'groupDescription': group_description}).json()
            # response contains group name and group chat link
            await app.send_message(chat_id, "✅Group created successfully \nGroup Name : "+response['groupName']+"\nGroup ID : "+response['groupId']+"\nInvite Link : "+response['inviteLink'])
        except:
            await app.send_message(chat_id, "❌Failed to add group")
        global groupList
        global group_ids
        groupList = get_groups()
        group_ids = [group[0] for group in groupList]

        return


@ app.on_message(filters.command(["whlist"]))
async def listwh(client, message):
    chat_id = message.chat.id
    if chat_id == 1076120105 or chat_id == 196536622:
        msg = await app.send_message(chat_id, "Please wait...")
        groups = requests.post('http://127.0.0.1:3000/get/groups/').json()
        if groups:
            newText = "Here is the list of whatsapp groups you have created : \n\n"
            for group in groups:
                newText += f"🟢 Group Name : {group['name']} \nGroup ID : {group['id']} \nInvite Link : {group['inviteLink']} \n\n"

            newText += "`/whdel` - Delete a group from the list of groups to be forwarded.\n"
            await msg.edit(newText)
        else:
            await message.reply("You haven't added any group yet ❗️")


@ app.on_message(filters.command(["whdel"]))
async def deletewh(client, message):
    chat_id = message.chat.id
    if chat_id == 1076120105 or chat_id == 196536622:
        # send message to user to please wait
        msg = await app.send_message(chat_id, "Please wait...")
        groups = requests.post('http://127.0.0.1:3000/get/groups/').json()
        if groups:
            newText = "Here is the list of whatsapp groups you have created : \n"
            index = 1
            for group in groups:
                newText += f"{index}. Group Name : {group['name']} \nGroup ID : {group['id']} \nInvite Link : {group['inviteLink']} \n\n"
                index += 1
            await msg.edit(newText)
            await app.send_message(chat_id, "Please send the indexes of the groups you want to delete separated by a space. \nExample : `1 2 3`")
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
            if not all(int(i) <= len(groups) for i in indexes):
                await app.send_message(chat_id, "Invalid indexes ❗️")
                return

            for index in indexes:

                index = int(index)
                if index > len(groups):
                    await app.send_message(chat_id, "Invalid index : "+index)
                else:
                    group_id = groups[index-1]['id']
                    try:
                        requests.post(
                            'http://127.0.0.1:3000/delete/group/', json={'groupId': group_id})
                        await app.send_message(chat_id, "✅Group "+group_id+" deleted successfully")
                    except:
                        await app.send_message(chat_id, "❌Failed to delete group")

# add word to blacklist


@app.on_message(filters.command(["addword"]))
async def addword(client, message):
    chat_id = message.chat.id
    if chat_id == 1076120105 or chat_id == 196536622:
        global wordBlacklist
        # if is in format /addword hi list;word2;word3
        # remove before first space
        if " " in message.text:
            message.text = message.text.split(" ", 1)[1]
            # then split by ; ignore last one
            words = message.text.split(";", -1)
            for word in words:
                add_word(word)
            await message.reply("✅Word(s) added successfully")
            global wordList
            wordList = get_words()
            return

        await app.send_message(chat_id, "Please send the word you want to add to the blacklist")
        answer = await listen_message(client, chat_id, timeout=None)
        if answer.text == "/cancel":
            await app.send_message(chat_id, "Cancelled❎")
            return
        word = answer.text
        add_word(word)
        await app.send_message(chat_id, "✅Word added successfully")
        wordBlacklist = get_words()

# delete words from blacklist


@app.on_message(filters.command(["delword"]))
async def delword(client, message):

    chat_id = message.chat.id
    if chat_id == 1076120105 or chat_id == 196536622:
        global wordBlacklist
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
                    wordBlacklist = get_words()
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
        global replaceList
        # if is in format /addrep word1=word2
        if " " in message.text:
            word = message.text.split(" ", 1)[1]
            if "|" in word:
                wordList = word.split("|")
            elif ":" in word:
                wordList = word.split(":")
            elif "=" in word:
                wordList = word.split("=")
            else:
                await app.send_message(chat_id, "Invalid format ❗️")
                return

            if message.entities:
                for entity in message.entities:
                    if entity.custom_emoji_id:
                        wordList[1] = wordList[1].replace(
                            message.text[entity.offset:entity.offset+entity.length], f"<emoji id='{entity.custom_emoji_id}'>{message.text[entity.offset:entity.offset+entity.length]}</emoji>")

            print(wordList[1])
            add_replace(wordList[0], wordList[1])
            await app.send_message(chat_id, "✅Replacement added successfully")
            replaceList = get_replacements()
            return

        await app.send_message(chat_id, "Please send the word with the replacement you want to add to the list of replacements \nuse `|` or `:` or `=` to separate the word and the replacement \n\nExample : 😲=<emoji id='5381855971943389791'>😲</emoji>", parse_mode=enums.ParseMode.HTML)
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
                        word[entity.offset:entity.offset+entity.length], f"<emoji id='{entity.custom_emoji_id}'>{word[entity.offset:entity.offset+entity.length]}</emoji>")

        add_replace(wordList[0], wordList[1])
        await app.send_message(chat_id, "✅Replacement added successfully")
        replaceList = get_replacements()

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
                    global replaceList
                    replaceList = get_replacements()
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

            await message.reply(msg, parse_mode=enums.ParseMode.HTML)
        else:
            await message.reply("You haven't added any replacement yet ❗️")

# server details


@app.on_message(filters.command(["server"]))
async def server(client, message):
    chat_id = message.chat.id
    if chat_id == 1076120105 or chat_id == 196536622:
        # beautiful message
        previous_message_id=get_setting(chat_id+"_server_message_id")
        if previous_message_id:
            #reply to the previous message
            await app.send_message(chat_id, "Here is the server details : ", reply_to_message_id=previous_message_id)
            return

        msg = "Server details : \n"
        msg += "🖥 CPU : "+str(psutil.cpu_percent())+"%\n"
        msg += "🎟 RAM : "+str(psutil.virtual_memory().percent)+"%\n"
        msg += "💾 Disk : "+str(psutil.disk_usage('/').percent)+"%\n"
        sentmsg = await message.reply(msg)
        await sentmsg.pin()
        set_setting(chat_id+"_server_message_id", sentmsg.message_id)


@app.on_message(filters.command(["restart"]))
async def server(client, message):
    chat_id = message.chat.id
    if chat_id == 1076120105 or chat_id == 196536622:
        sentmsg = await message.reply("Restarting the server...")
        os.system("sudo reboot")


# /whrst restart whatsapp
@app.on_message(filters.command(["whrst"]))
async def whrst(client, message):
    chat_id = message.chat.id
    if chat_id == 1076120105 or chat_id == 196536622:
        sentmsg = await message.reply("Restarting whatsapp...")
        sentmsg.delete()
        os.system(
            "systemctl restart wwjs-express.service && systemctl status nisalforwader-bot.service")
        await message.reply("✔️  Whatsapp restarted successfully")

# /botrst restart bot


@app.on_message(filters.command(["botrst"]))
async def botrst(client, message):
    chat_id = message.chat.id
    if chat_id == 1076120105 or chat_id == 196536622:
        sentmsg = await message.reply("Restarting the bot...")
        os.system("systemctl restart bot.service nisalforward.service")
        await sentmsg.edit("✔️ Restarted the bot successfully")


@app.on_message(filters.incoming & ~filters.forwarded & ~filters.poll)
async def onMessage(client, message):

    channel_id = str(message.chat.id)
    # import pickle

    # pickle.dump(message, open("message.pickle", "wb"))

    if channel_id not in channel_ids:
        return
    orginal_text = message.text or message.caption or ""
    if not is_english(orginal_text) or is_in_blacklist(orginal_text):
        return
    entities = message.entities or message.caption_entities
    if entities:
        for entity in entities:
            if entity.type == enums.MessageEntityType.HASHTAG:
                entities.remove(entity)
            if entity.type == enums.MessageEntityType.CASHTAG:
                entities.remove(entity)

    entity_html_dict = {}
    replacing_text = orginal_text
    offset_change = 0
    global before_offset
    before_offset = 0
    # convert all entities to HTML
    if entities:
        for entity in entities:
            before_entity_text = orginal_text[entity.offset:entity.offset + entity.length]
            before_to_entity = orginal_text[before_offset:entity.offset + entity.length]
            key = f"{entity.offset}:{entity.offset + entity.length}"
            if before_entity_text.strip() == '':
                continue
            if entity.type == enums.MessageEntityType.BOLD:
                if key not in entity_html_dict:
                    replacing_part = "<b>" + before_entity_text+"</b>"
                else:
                    replacing_part = "<b>"+entity_html_dict[key][0]+"</b>"
                entity_html_dict[key] = [replacing_part,
                                         before_to_entity, before_entity_text]

            elif entity.type == enums.MessageEntityType.TEXT_LINK:
                if key not in entity_html_dict:
                    replacing_part = "<a href='"+entity.url+"'>" + before_entity_text+"</a>"
                else:
                    replacing_part = "<a href='"+entity.url + \
                        "'>"+entity_html_dict[key][0]+"</a>"
                entity_html_dict[key] = [replacing_part,
                                         before_to_entity, before_entity_text]

            elif entity.type == enums.MessageEntityType.TEXT_MENTION:
                if key not in entity_html_dict:

                    replacing_part = "<a href='tg://user?id=" + \
                        str(entity.user_id)+"'>" + before_entity_text+"</a>"
                else:
                    replacing_part = "<a href='tg://user?id=" + \
                        str(entity.user_id)+"'>" + \
                        entity_html_dict[key][0]+"</a>"
                entity_html_dict[key] = [replacing_part,
                                         before_to_entity, before_entity_text]

            elif entity.type == enums.MessageEntityType.ITALIC:
                if key not in entity_html_dict:

                    replacing_part = "<i>" + before_entity_text+"</i>"
                else:
                    replacing_part = "<i>"+entity_html_dict[key][0]+"</i>"
                entity_html_dict[key] = [replacing_part,
                                         before_to_entity, before_entity_text]

            elif entity.type == enums.MessageEntityType.CODE:
                if key not in entity_html_dict:

                    replacing_part = "<code>" + before_entity_text+"</code>"
                else:
                    replacing_part = "<code>" + \
                        entity_html_dict[key][0]+"</code>"
                entity_html_dict[key] = [replacing_part,
                                         before_to_entity, before_entity_text]

            elif entity.type == enums.MessageEntityType.PRE:
                if key not in entity_html_dict:

                    replacing_part = "<pre>" + before_entity_text+"</pre>"
                else:
                    replacing_part = "<pre>"+entity_html_dict[key][0]+"</pre>"
                entity_html_dict[key] = [replacing_part,
                                         before_to_entity, before_entity_text]

            elif entity.type == enums.MessageEntityType.UNDERLINE:
                if key not in entity_html_dict:

                    replacing_part = "<u>" + before_entity_text+"</u>"
                else:
                    replacing_part = "<u>"+entity_html_dict[key][0]+"</u>"
                entity_html_dict[key] = [replacing_part,
                                         before_to_entity, before_entity_text]

            elif entity.type == enums.MessageEntityType.STRIKETHROUGH:
                if key not in entity_html_dict:

                    replacing_part = "<s>" + before_entity_text+"</s>"
                else:
                    replacing_part = "<s>"+entity_html_dict[key][0]+"</s>"
                entity_html_dict[key] = [replacing_part,
                                         before_to_entity, before_entity_text]

            elif entity.type == enums.MessageEntityType.BOT_COMMAND:
                if key not in entity_html_dict:

                    replacing_part = "<code>" + before_entity_text+"</code>"
                else:
                    replacing_part = "<code>" + \
                        entity_html_dict[key][0]+"</code>"
                entity_html_dict[key] = [replacing_part,
                                         before_to_entity, before_entity_text]

            elif entity.type == enums.MessageEntityType.URL:
                if key not in entity_html_dict:

                    replacing_part = "<a href='" + \
                        before_entity_text+"'>" + before_entity_text+"</a>"
                else:
                    replacing_part = "<a href='" + before_entity_text + \
                        "'>"+entity_html_dict[key][0]+"</a>"
                entity_html_dict[key] = [replacing_part,
                                         before_to_entity, before_entity_text]

            elif entity.type == enums.MessageEntityType.EMAIL:
                if key not in entity_html_dict:

                    replacing_part = "<a href='mailto:" + \
                        before_entity_text+"'>" + before_entity_text+"</a>"
                else:
                    replacing_part = "<a href='mailto:" + before_entity_text + \
                        "'>"+entity_html_dict[key][0]+"</a>"
                entity_html_dict[key] = [replacing_part,
                                         before_to_entity, before_entity_text]

            elif entity.type == enums.MessageEntityType.PHONE_NUMBER:
                if key not in entity_html_dict:

                    replacing_part = "<a href='tel:" + \
                        before_entity_text+"'>" + before_entity_text+"</a>"
                else:
                    replacing_part = "<a href='tel:" + \
                        entity_html_dict[key][0]+"'>"+replacing_part+"</a>"
                entity_html_dict[key] = [replacing_part,
                                         before_to_entity, before_entity_text]

            elif entity.type == enums.MessageEntityType.SPOILER:
                if key not in entity_html_dict:

                    replacing_part = "<code>" + before_entity_text+"</code>"
                else:
                    replacing_part = "<code>" + \
                        entity_html_dict[key][0]+"</code>"
                entity_html_dict[key] = [replacing_part,
                                         before_to_entity, before_entity_text]

            elif entity.type == enums.MessageEntityType.BLOCKQUOTE:
                if key not in entity_html_dict:

                    replacing_part = "<blockquote>" + before_entity_text+"</blockquote>"
                else:
                    replacing_part = "<blockquote>" + \
                        entity_html_dict[key][0]+"</blockquote>"
                entity_html_dict[key] = [replacing_part,
                                         before_to_entity, before_entity_text]

            elif entity.type == enums.MessageEntityType.BANK_CARD:
                if key not in entity_html_dict:

                    replacing_part = "<code>" + before_entity_text+"</code>"
                else:
                    replacing_part = "<code>" + \
                        entity_html_dict[key][0]+"</code>"
                entity_html_dict[key] = [replacing_part,
                                         before_to_entity, before_entity_text]

            elif entity.type == enums.MessageEntityType.CUSTOM_EMOJI:
                if key not in entity_html_dict:

                    replacing_part = "<emoji id='" + \
                        str(entity.custom_emoji_id)+"'>" + \
                        before_entity_text+"</emoji>"
                else:
                    replacing_part = "<emoji id='" + \
                        str(entity.custom_emoji_id) + \
                        "'>"+entity_html_dict[key][0]+"</emoji>"
                entity_html_dict[key] = [replacing_part,
                                         before_to_entity, before_entity_text]
            before_offset = entity.offset + entity.length

    for entity_html_dict_key in entity_html_dict:
        entity_html_dict_value = entity_html_dict[entity_html_dict_key]
        start = int(entity_html_dict_key.split(":")[0])
        end = int(entity_html_dict_key.split(":")[1])
        replace_text = entity_html_dict_value[0]
        # if replace_text is an empty tag, remove it regex
        if re.search("<[A-z]>\s*<\/[A-z]>", replace_text):
            continue
        before_text = entity_html_dict_value[1]
        replacing_part = entity_html_dict_value[2]
        replacing_text = replacing_text.replace(
            before_text, before_text.replace(replacing_part, replace_text))

    #remove @channelusername
    replacing_text = re.sub(r'@([A-Za-z0-9_]+)', '', replacing_text)
    # if ends with multiple new lines remove them
    replacing_text = re.sub(r'\n+$|<[A-z]><\/[A-z]>', '', replacing_text)
    replacing_text = re.sub(r'<[A-z]>\s+<\/[A-z]>', ' ', replacing_text)
    df = pd.DataFrame({"Text": [replacing_text]})
    df["Text"] = df["Text"].replace(replaceList, regex=True)
    replacing_text = df["Text"][0]
    reactionEmojiList = ["👍", "🔥", "😍", "🤯", "🎉", "👏"]

    # get channel tuple from channels list
    channel = [channel for channel in channelList if channel[0] == channel_id][0]
    footer = channel[2]
    for to_channel_id, to_channel_username in to_channels.items():
        await client.send_chat_action(to_channel_id, enums.ChatAction.TYPING)
        nFooter = footer.replace("<username>", to_channel_username)
        caption = replacing_text+"\n\n"+nFooter
        # if channel type is all
        if channel[1] == "all":
            if message.media_group_id:
                sentMessage = await client.copy_media_group(to_channel_id, message.chat.id, message.id, captions=caption)

            elif message.photo:
                sentMessage1 = await client.send_photo(to_channel_id, photo=message.photo.file_id, parse_mode=enums.ParseMode.HTML, caption=caption)
            elif message.video:
                sentMessage1 = await client.send_video(to_channel_id, message.video.file_id, caption=caption, parse_mode=enums.ParseMode.HTML)
            elif message.audio:
                sentMessage1 = await client.send_audio(to_channel_id, message.audio.file_id, caption=caption, parse_mode=enums.ParseMode.HTML)
            elif message.document:
                sentMessage1 = await client.send_document(to_channel_id, message.document.file_id, caption=caption, parse_mode=enums.ParseMode.HTML)
            elif message.text:
                sentMessage1 = await client.send_message(to_channel_id, caption, parse_mode=enums.ParseMode.HTML)

        # if channel type is media_text
        elif channel[1] == "media_text":
            if message.media_group_id:
                sentMessage1 = await client.copy_media_group(to_channel_id, message.chat.id, message.id, captions=caption)
            elif message.photo:
                sentMessage1 = await client.send_photo(to_channel_id, photo=message.photo.file_id, caption=caption, parse_mode=enums.ParseMode.HTML)
            elif message.video:
                sentMessage1 = await client.send_video(to_channel_id, message.video.file_id, caption=caption, parse_mode=enums.ParseMode.HTML)
            elif message.audio:
                sentMessage1 = await client.send_audio(to_channel_id, message.audio.file_id, caption=caption, parse_mode=enums.ParseMode.HTML)
            elif message.document:
                sentMessage1 = await client.send_document(to_channel_id, message.document.file_id, caption=caption, parse_mode=enums.ParseMode.HTML)
        # if channel type is media
        elif channel[1] == "media":
            if message.media_group_id:
                sentMessage1 = await client.copy_media_group(to_channel_id, message.chat.id, message.id, captions=caption)
            elif message.photo:
                sentMessage1 = await client.send_photo(to_channel_id, photo=message.photo.file_id, captions=caption)
            elif message.video:
                sentMessage1 = await client.send_video(to_channel_id, message.video.file_id, captions=caption)
            elif message.audio:
                sentMessage1 = await client.send_audio(to_channel_id, message.audio.file_id, captions=caption)
            elif message.document:
                sentMessage1 = await client.send_document(to_channel_id, message.document.file_id, captions=caption)
        # if channel type is text
        elif channel[1] == "text":
            if message.text:
                sentMessage1 = await client.send_message(to_channel_id, caption, parse_mode=enums.ParseMode.HTML)

        sentMessageId = sentMessage1.id
        # random the rection emoji

        await client.send_reaction(to_channel_id, sentMessageId, rand_choice(reactionEmojiList))
        await app.send_chat_action(to_channel_id, enums.ChatAction.CANCEL)

scheduler = AsyncIOScheduler()
scheduler.add_job(job, "interval", seconds=3)

scheduler.start()
app.run()  # Automatically start() and idle()
