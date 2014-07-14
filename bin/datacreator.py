import socket
import string
import sys
import sqlite3
import time, datetime
import wx
from collections import OrderedDict

def ask(parent=None, message=''):
        app = wx.App()
        dlg = wx.TextEntryDialog(parent, message)
        dlg.ShowModal()
        result = dlg.GetValue()
        dlg.Destroy()
        app.MainLoop()
        return result

info= ask(message = 'What is the channel name?')
HOST="irc.twitch.tv"
PORT=6667
NICK=""
IDENT="USERNAME"
REALNAME="USERNAME"
CHANNEL = "#"+ info
PASSWORD="oauth:" #From http://twitchapps.com/tmi/
readbuffer=""
s=socket.socket( )
s.connect((HOST, PORT))
s.send("PASS %s\r\n" % PASSWORD)
s.send("NICK %s\r\n" % NICK)
s.send("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME))
s.send("JOIN %s\r\n" % CHANNEL)
entry = 1
sqlite_file = '/Users/nicholasrosso/Desktop/Programs/RoR/twitch_app/db/development.sqlite3'

def clear_database(sqlite_file):
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    c.execute('''DELETE FROM messages ''')
    conn.commit()
    conn.close()
    print "Database Cleared"

def write_data(entry, info):
    #removes unwanted symbols
    symbols = ["@", "!", ".tmi.twitch.tv", ":"]
    for symbol in symbols:
        said[0] =said[0].replace(symbol, "")
    said[0] = "".join(OrderedDict.fromkeys(said[0]))
    said[1] = said[1].replace(':', "")
    username = []
    username.append(said[0])
    del said[0]
    chatmsg = ' '.join(said)
    sqlchatmsg = unicode(chatmsg,'utf-8')
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts)
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    c.execute('''INSERT INTO messages (id, content,created_at, username, channel) VALUES(?,?,?,?,?)''',(entry,sqlchatmsg,st, username[0],info,))
    conn.commit()
    conn.close()

clear_database(sqlite_file)
print "Connecting To Server"
while True:
    readbuffer=readbuffer+s.recv(1024)
    temp=string.split(readbuffer, "\n")
    readbuffer=temp.pop( )
    said = []
    for line in temp:
        line=string.rstrip(line)
        line=string.split(line)
        
        if line[1] =="PRIVMSG" and line[0] != ':jtv!jtv@jtv.tmi.twitch.tv':
            end = len(line)
            said.append(line[0])
            username = said[0]
            for item in line[3:end]:
                said.append(item)
            write_data(entry, info)
            entry += 1
            print "Message %s Stored" % entry

        if(line[0]=="PING"):
            s.send("PONG %s\r\n" % line[1])
            print "PONG Sent"   