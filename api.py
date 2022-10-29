import os
import psycopg2

#if is in heroku
if "DATABASE_URL" in os.environ:
    DATABASE_URL = os.environ['DATABASE_URL']
else:
    DATABASE_URL = "postgres://uablnhutlxmzir:a34362810a1afa26506dcb6dd8dbbd6968e4833171fc4cdd5e60903a362fb916@ec2-34-247-72-29.eu-west-1.compute.amazonaws.com:5432/db13rt0ge6i9ig"


#create connection
conn = psycopg2.connect(DATABASE_URL, sslmode='require')


#create table channels if not exists
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS channels (channel_id TEXT, channel_type TEXT,footer TEXT, PRIMARY KEY (channel_id))")
conn.commit()
cur.close()


def add_channel(channel_id, channel_type, footer):
    cur = conn.cursor()
    #if channel already exists return false
    cur.execute("SELECT * FROM channels WHERE channel_id = %s", (channel_id,))
    if cur.fetchone() is not None:
        return False
    cur.close()
    #else add channel
    cur = conn.cursor()
    cur.execute("INSERT INTO channels (channel_id, channel_type, footer) VALUES (%s, %s, %s)", (channel_id, channel_type, footer))
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
print(get_channels())
