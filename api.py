import os
import psycopg2
import re
#if is in heroku
if "DATABASE_URL" in os.environ:
    DATABASE_URL = os.environ['DATABASE_URL']
else:
    DATABASE_URL = "postgres://tjcrbtchxjetna:ffb450747d26895a29d3a3b6c5a6f1a6619d6870131c04afba453d54cca98e6a@ec2-54-76-43-89.eu-west-1.compute.amazonaws.com:5432/dfsf5klh4quf4q"


#create connection
conn = psycopg2.connect(DATABASE_URL, sslmode='require')


#create table channels if not exists
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS channels (channel_id TEXT, channel_type TEXT,footer TEXT,channel_name  TEXT,PRIMARY KEY (channel_id))")
conn.commit()
cur.close()


def add_channel(channel_id, channel_type, footer, channel_name):
   
    cur = conn.cursor()
    #if channel already exists return false
    cur.execute("SELECT * FROM channels WHERE channel_id = %s", (channel_id,))
    if cur.fetchone() is not None:
        return False
    cur.close()
    #else add channel
    cur = conn.cursor()
    cur.execute("INSERT INTO channels (channel_id, channel_type, footer, channel_name) VALUES (%s, %s, %s, %s)", (channel_id, channel_type, footer, channel_name))
    conn.commit()
    cur.close()
    return True

def get_channels():
    cur = conn.cursor()
    cur.execute("SELECT * FROM channels")
    rows = cur.fetchall()
    cur.close()
    return rows

def delete_channel(channel_id):
    cur = conn.cursor()
    cur.execute("DELETE FROM channels WHERE channel_id = %s", (channel_id,))
    conn.commit()
    cur.close()
    return True
    

def delete_all_channels():
    cur = conn.cursor()
    cur.execute("DELETE FROM channels")
    conn.commit()
    cur.close()

#create table for word blacklist
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS blacklist (word TEXT, PRIMARY KEY (word))")
conn.commit()
cur.close()

def add_word(word):
    cur = conn.cursor()
    #if word already exists return false
    cur.execute("SELECT * FROM blacklist WHERE word = %s", (word,))
    if cur.fetchone() is not None:
        return False
    cur.close()
    #else add word
    cur = conn.cursor()
    cur.execute("INSERT INTO blacklist (word) VALUES (%s)", (word,))
    conn.commit()
    cur.close()
    return True

def get_words():
    cur = conn.cursor()
    cur.execute("SELECT * FROM blacklist")
    rows = cur.fetchall()
    cur.close()
    return rows

def delete_word(word):
    cur = conn.cursor()
    cur.execute("DELETE FROM blacklist WHERE word = %s", (word,))
    conn.commit()
    cur.close()
    return True

def delete_all_words():
    cur = conn.cursor()
    cur.execute("DELETE FROM blacklist")
    conn.commit()
    cur.close()


# delete_channel("-1001446018493"")

#add word replace
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS replace (word TEXT, replace TEXT,PRIMARY KEY (word))")
conn.commit()
cur.close()

def add_replace(word, replace):
    cur = conn.cursor()
    #if word already exists return false
    cur.execute("SELECT * FROM replace WHERE word = %s", (word,))
    if cur.fetchone() is not None:
        cur.execute("UPDATE replace SET replace = %s WHERE word = %s", (replace, word))
        conn.commit()
        cur.close()
        return True
    #else add word
    cur = conn.cursor()
    cur.execute("INSERT INTO replace (word, replace) VALUES (%s, %s)", (word, replace))
    conn.commit()
    cur.close()
    return True

def get_replace():
    cur = conn.cursor()
    cur.execute("SELECT * FROM replace")
    rows = cur.fetchall()
    cur.close()
    return rows

def delete_replace(word):
    cur = conn.cursor()
    cur.execute("DELETE FROM replace WHERE word = %s", (word,))
    conn.commit()
    cur.close()
    return True

def delete_all_replace():
    cur = conn.cursor()
    cur.execute("DELETE FROM replace")
    conn.commit()
    cur.close()

def get_replacements():
    cur = conn.cursor()
    cur.execute("SELECT * FROM replace")
    rows = cur.fetchall()
    #send as dict
    replacements = {}
    for row in rows:
        replacements[row[0]] = row[1]
    cur.close()
    return replacements

#create table for server settings
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS settings ( server_name TEXT, value TEXT, PRIMARY KEY (server_name))")
conn.commit()

def add_setting(server_name, value):
    cur = conn.cursor()
    #if word already exists return false
    cur.execute("SELECT * FROM settings WHERE server_name = %s", (server_name,))
    if cur.fetchone() is not None:
        cur.execute("UPDATE settings SET value = %s WHERE server_name = %s", (value, server_name))
        conn.commit()
        cur.close()
        return True
    #else add word
    cur = conn.cursor()
    cur.execute("INSERT INTO settings (server_name, value) VALUES (%s, %s)", (server_name, value))
    conn.commit()
    cur.close()
    return True

def get_setting(server_name):
    cur = conn.cursor()
    cur.execute("SELECT * FROM settings WHERE server_name = %s", (server_name,))
    row = cur.fetchone()
    cur.close()
    return row