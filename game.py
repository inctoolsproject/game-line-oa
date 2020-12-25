from linepy import *
from akad.ttypes import Message
from liff.ttypes import LiffChatContext, LiffContext, LiffSquareChatContext, LiffNoneContext, LiffViewRequest
from akad.ttypes import ContentType as Type
from akad.ttypes import TalkException
from KhieBots.thrift.protocol import TCompactProtocol
from KhieBots.thrift.transport import THttpClient
from KhieBots.ttypes import LoginRequest
from datetime import datetime, timedelta
from time import sleep
from bs4 import BeautifulSoup
from humanfriendly import format_timespan, format_size, format_number, format_length
from gtts import gTTS
from threading import Thread
from io import StringIO
from multiprocessing import Pool
from googletrans import Translator
from urllib.parse import urlencode
from wikiapi import WikiApi
from tmp.MySplit import *
from zalgo import zalgoname
from random import randint
from shutil import copyfile
from youtube_dl import YoutubeDL
import LineService
import subprocess, youtube_dl, humanize, traceback
import subprocess as cmd
import time, random, sys, json, null, codecs, html5lib ,shutil ,threading, glob, re, base64, string, os, requests, six, ast, pytz, wikipedia, urllib, urllib.parse, atexit, asyncio, traceback
_session = requests.session()
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
#==================    
    

client = LINE("",appName="IOS\t10.1.1\tIOS\t13.3.1")

clientMID = client.profile.mid
oepoll = OEPoll(client)
quest = []
temp_flood = {}
admin = "u90eb5253cbd367c607d231acbe30fa16"

try:
    with open("data.json", "r", encoding="utf_8_sig") as fp:
        data = json.loads(fp.read())
except:
    print ("data file not found, data dict default will used")
    data = {}

with open("quest.txt", "r") as file:
     blist = file.readlines()
     quest = [x.strip() for x in blist]
file.close()
group = client.getGroupIdsJoined()

for g in group:
  data[g]={'point':{}}
  data[g]['saklar']=False
  data[g]['quest']=''
  data[g]['asw']=[]
  data[g]['tmp']=[]

def backupData():
    with open("data.json", "w", encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4, separators=(',', ': '))
atexit.register(backupData)

def myhelp():
    helpMessage = "[ Daftar Perintah ]" + "\n" + \
                  " /mulai" + "\n" + \
                  " /reset" + "\n" + \
                  " /next" + "\n" + \
                  " /nyerah" + "\n" + \
                  " /keluar" + "\n" + \
                  " /laporkan" + "\n" + \
                  "[ Cannibal Games ]"
    return helpMessage

def getQuest(to):
	try:
			data[to]['quest'] = ''
			data[to]['asw'] = []
			data[to]['tmp'] = []
			a = random.choice(quest)
			a = a.split('*')
			data[to]['quest'] = a[0]
			for i in range(len(a)):
				data[to]['asw'] += [a[i]]
			data[to]['asw'].remove(a[0])
			for j in range(len(data[to]['asw'])):
				data[to]['tmp'] += [str(j+1)+'. _________']
	except Exception as e:
		print(e)

def sendMention(to, mid, firstmessage='', lastmessage=''):
    try:
        arrData = ""
        text = "%s " %(str(firstmessage))
        arr = []
        mention = "@x "
        slen = str(len(text))
        elen = str(len(text) + len(mention) - 1)
        arrData = {'S':slen, 'E':elen, 'M':mid}
        arr.append(arrData)
        text += mention + str(lastmessage)
        client.sendMessage(to, text, {'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0)
    except Exception as error:
        print(error)

def delExpire():
    if temp_flood != {}:
        for tmp in temp_flood:
            if temp_flood[tmp]["expire"] == True:
                if time.time() - temp_flood[tmp]["time"] >= 3*10:
                    temp_flood[tmp]["expire"] = False
                    temp_flood[tmp]["time"] = time.time()
                    try:
                        client.sendMessage(tmp, "Cannibal Kuis kembali aktif")
                    except Exception as error:
                        print(error)
                        
def restart_program():
	backupData()
	time.sleep(5)
	python = sys.executable
	os.execl(python, python, * sys.argv)

def clientBot(op):
    try:
        if op.type == 0:
            print ("[0] END OF OPERATION")
            return
#------------------NOTIFIED_INVITE_INTO_ROOM-------------
        if op.type == 22:
            client.leaveRoom(op.param1)
            print ("[22] NOTIFIED INVITE INTO ROOM")
#--------------------INVITE_INTO_ROOM--------------------
        if op.type == 21:
            client.leaveRoom(op.param1)
            print ("[21] NOTIFIED INVITE INTO ROOM")
        if op.type == 5:
            print ("[5] NOTIFIED ADD CONTACT")
            client.findAndAddContactsByMid(op.param1)
            client.sendMessage(op.param1, "Halo {}, terimakasih telah menambahkan saya sebagai teman 😊\nJangan lupa Add Owner kami di bawah ini :".format(str(client.getContact(op.param1).displayName)))
            client.sendContact(op.param1, "ua3e46be368346a83c7c961bc6c23937e")
        if op.type == 13:
            print ("[13] NOTIFIED INVITE INTO GROUP")
            group = client.getGroup(op.param1)
            contact = client.getContact(op.param2)
            if clientMID in op.param3:
            	client.acceptGroupInvitation(op.param1)
            	client.sendMessage(op.param1, "Halo kak, terima kasih telah mengundang saya 😊")
            	client.sendMessage(op.param1, "Jangan lupa Add Owner kami di bawah ini :")
            	client.sendContact(op.param1, "ua3e46be368346a83c7c961bc6c23937e")
            	client.sendMessage(op.param1, "Ketik Help di group ini untuk bantuan.")
            	data[op.param1] = {
                        "point": {},
                        "saklar": False,
                        "quest": "",
                        "tmp": [],
                        "asw": []
                }
                
        if op.type in [26, 25]:
            if op.type == 26: print ("[26] RECEIVE MESSAGE")
            else: print ("[25] SEND MESSAGE")
            msg = op.message
            text = msg.text
            receiver = msg.to
            sender = msg._from
            to = receiver
            try:
                if msg.contentType == 0:
                    if msg.toType == 2:
                    	contactlist = client.getAllContactIds()
                    	kontak = [cont.mid for cont in client.getContacts(contactlist)]
                    	for i in range(len(data[to]['asw'])):
                            if text.lower() == data[to]['asw'][i].lower() and sender not in clientMID and data[to]['saklar'] == True:
                                if sender in kontak:
                                    wnr = client.getContact(sender).displayName
                                    wna = client.getContact(sender)
                                    if wnr in data[to]['point']:
                                        data[to]['point'][wnr] += 1
                                    else:
                                        data[to]['point'][wnr] = 1
                                    if i != len(data[to]['asw']):
                                        data[to]['tmp'][i] = str(i+1)+'. '+data[to]['asw'][i]+' (1)'+' ['+wnr+']'
                                        data[to]['asw'][i] = data[to]['asw'][i]+' (*)'
                                    else:
                                        data[to]['tmp'].remove(str(data[to]['tmp'][i]))
                                        data[to]['tmp'].append(str(i+1)+'. '+data[to]['asw'][i]+' (1)'+' ['+wnr+']')
                                        data[to]['asw'].remove(str(data[to]['asw'][i]))
                                        data[to]['tmp'].append(data[to]['asw'][i]+' (*)')
                                    rsl,rnk = '',''
                                    for j in data[to]['tmp']:
                                        rsl += j+'\n'
                                    for k in data[to]['point']:
                                        rnk += ' '+k+' : '+str(data[to]['point'][k])+'\n'
                                    if '_________' in str(data[to]['tmp']):
                                        isi = str(data[to]['quest'])+'\n'+rsl
                                        client.sendMessage(to, isi)
                                    else:
                                        data[to]['saklar'] = False
                                        isi = str(data[to]['quest'])+'\n'+rsl
                                        client.sendMessage(to, isi)
                                        client.sendMessage(to, 'Papan Poin :\n'+rnk)
                                        client.sendMessage(to, 'Ketik /mulai untuk Pertanyaan Lainnya.')
                                else:
                                    sendMention(to, sender, '', 'Anda belum menambahkan Cannibal Kuis sebagai teman, Untuk ikut bermain silahkan tambahkan Cannibal Kuis sebagai teman.')
            except Exception as e:
                client.log("[RECEIVE_MESSAGE] ERROR : " + str(e))
                traceback.print_tb(e.__traceback__)
            if msg.toType == 0 and sender != clientMID:
                to = sender
            else:
            	to = receiver
            if receiver in temp_flood:
                if temp_flood[receiver]["expire"] == True:
                    if temp_flood[receiver]["expire"] >= 20:
                        temp_flood[receiver]["expire"] = False
                        temp_flood[receiver]["time"] = time.time()
                        client.sendMessage(to, "merana games kembali aktif.")
                    return
                elif time.time() - temp_flood[receiver]["time"] <= 5:
                    temp_flood[receiver]["flood"] += 1
                    if temp_flood[receiver]["flood"] >= 20:
                        temp_flood[receiver]["flood"] = 0
                        temp_flood[receiver]["expire"] = True
                        ret_ = "Spam terdeteksi, Cannibal Kuis akan silent selama 30 detik pada ruangan ini atau ketik Open untuk mengaktifkan kembali."
                        client.sendMessage(to, str(ret_))
                else:
                     temp_flood[receiver]["flood"] = 0
                     temp_flood[receiver]["time"] = time.time()
            else:
                temp_flood[receiver] = {
    	            "time": time.time(),
    	            "flood": 0,
    	            "expire": False
                }
            if text is None: return
            if text.lower() == "/mulai" and sender not in clientMID:
                if data[to]['saklar'] == False:
                    data[to]['saklar'] = True
                    getQuest(to)
                    aa = ''
                    for aswr in data[to]['tmp']:
                        aa += aswr+'\n'
                        q = data[to]['quest']+'\n'+aa
                    client.sendMessage(to, q)
                else:
                    aa = '' 
                    for aswr in data[to]['tmp']:
                        aa += aswr+'\n'
                    q = data[to]['quest']+'\n'+aa
                    client.sendMessage(to, q)
                    client.sendMessage(to, 'Ketik /nyerah untuk mengakhiri pertanyaan ini.')
            elif text.lower() == '/nyerah' and sender not in clientMID:
                if data[to]['saklar'] == True:
                    rnk,asd = '',''
                    data[to]['saklar'] = False
                    for j in range(len(data[to]['tmp'])):
                        if '_________' in data[to]['tmp'][j]:
                            if j != len(data[to]['tmp']):
                                data[to]['tmp'][j] = str(j+1)+'. '+data[to]['asw'][j]+' (*system)'
                            else:
                                data[to]['tmp'][j].remove(str(data[to]['tmp'][j]))
                                data[to]['tmp'][j].append(str(j+1)+'. '+data[to]['asw'][j]+' (*system)')
                    for m in data[to]['tmp']:
                        asd += m+'\n'
                    for k in data[to]['point']:
                        rnk += ' '+k+' : '+str(data[to]['point'][k])+'\n'
                    client.sendMessage(to, str(data[to]['quest'])+'\n'+asd)
                    client.sendMessage(to, 'Papan Poin :\n'+rnk)
                    client.sendMessage(to, 'Ketik /mulai untuk Pertanyaan Lainnya')
                else:
                    client.sendMessage(to, 'Game belum di mulai, tidak dapat menyerah.')
                    client.sendMessage(to, 'Ketik /mulai untuk memulai permainan.')
            elif text.lower() == "/next" and sender not in clientMID:
            	if data[to]['saklar'] == True:
            		getQuest(to)
            		aa = ''
            		for aswr in data[to]['tmp']:
            			aa += aswr+'\n'
            			q = data[to]['quest']+'\n'+aa
            		client.sendMessage(to, q)
            	else:
            		client.sendMessage(to, 'Permainan belum di mulai, tidak dapat berpindah ke soal berikutnya.')
            elif text.lower() == '/reset' and sender not in clientMID:
                data[to]['point'] = {}
                data[to]['saklar'] = False
                client.sendMessage(to, 'Permainan telah di reset.')
                client.sendMessage(to, 'Ketik /mulai untuk memulai permainan.')
            elif text.lower() == '/keluar' and sender not in clientMID:
                if msg.toType == 2:
                    if data[to]['saklar'] == True:
                        client.sendMessage(to, "Game belum di selesaikan, ketik /nyerah untuk menyelesaikan game dan bot akan keluar 😊")
                    else:
                        client.sendMessage(to, "Oke, See you next time 😊")
                        client.leaveGroup(to)
            elif text.lower() == '/laporkan' and sender in admin:
                client.sendMessage(to, "Untuk melaporkan masalah yang di alami atau ingin memberikan saran, kalian bisa langsung menghubungi admin melalui kontak dibawah ini :")
                client.sendContact(to, "ua3e46be368346a83c7c961bc6c23937e")
            elif text.lower() == 'help' and sender not in clientMID:
                helpMessage = myhelp()
                client.sendMessage(to, str(helpMessage))
            elif text.lower() == 'restart' and sender in admin:
                client.sendMessage(to, 'Sukses merestart Bot')
                restart_program()
            elif text.lower().startswith('add ') and sender in admin:
            	targets = []
            	key = eval(msg.contentMetadata["MENTION"])
            	key["MENTIONEES"] [0] ["M"]
            	for x in key["MENTIONEES"]:
            		targets.append(x["M"])
            	for target in targets:
            		try:
            			client.findAndAddContactsByMid(target)
            			client.sendMessage(to, 'Done.')
            		except Exception as error:
            			client.sendMessage(to, str(error))

    except Exception as e:
    	client.log("[RECEIVE_MESSAGE] ERROR : " + str(e))
    	traceback.print_tb(e.__traceback__)

def run():
    while True:
        try:
        	delExpire()
        	ops = oepoll.singleTrace(count=50)
        	if ops != None:
        		for op in ops:
        			thread = Thread(target=clientBot(op))
        		#	thread.daemon = daemon
        			thread.start()
        			oepoll.setRevision(op.revision)
        except Exception as e:
        	print(e)

if __name__ == "__main__":
    run()
