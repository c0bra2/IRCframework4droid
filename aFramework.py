# Android Bot Framework
# version 1.0.0
# written by c0bra2 (12/27/2012)
# this code is protected under GPL
###################################

import socket, time, android 

class Framework():
	def __init__(self):
		self.droid = android.Android()
		self.getIRC_info()
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.connect((self.server, self.port))
		self.parse()
		self.pong()
		self.s.send('NICK %s\r\n' % self.nick)
		self.parse()
		self.pong()
		self.s.send('USER %s %s no :%s\r\n' % (self.nick, self.server, self.nick))

	def getIRC_info(self):
		self.nick = self.droid.dialogGetInput("Nickname", "what is the bots nickname?").result
		self.server = self.droid.dialogGetInput("Server", "connect to which server?").result
		self.channel = self.droid.dialogGetInput("Channel", "join which channel?").result
		self.port = 6667
		if (self.nick == None) or (self.nick == ''):
			self.nick = "defaultNick"
		elif (self.server == None) or (self.server == ''):
			self.server = "irc.hackthissite.org"
		elif (self.channel == None) or (self.channel == ''):
			self.channel = "#hackthissite"

	def join(self, string):
		#join a channel
		time.sleep(5)
		self.channel = string
		self.s.send('JOIN %s\r\n' % string)
	
	def pong(self):
		self.s.send('PONG ' + self.raw_string.split()[1] + '\r\n')

	def parse(self):
		#irc parser
		self.line = self.s.recv(1024)
		self.raw = self.line
		self.raw_string = self.raw
		self.line = self.line.split(':')
		self.raw = self.raw.split(':')
		if 'comment' in self.raw_string:
			self.comment = self.raw_string.split('comment')[1]
		else:
			self.comment = ' '

		try:
			self.line = self.line[2]
		except:
			self.line = ["Null"]
			self.raw = ["Null","Null"]
			return
		self.line = [i.lstrip() for i in self.line.split()]
		if not len(self.line):
			self.line = ["None"]

	def get_nick(self):
		#get the person who is talking in the channel
		self.res = ''
		try:
			for i in self.raw[1]:
				if i != '!':
					self.res += i
				else:
					return self.res
		except:
			return 'nobody'
	def write(self, string):
		#write something to the channel
		self.s.send('PRIVMSG %s :%s\r\n' % (self.channel, string))

	def put(self, string):
		#send a command to the server
		self.s.send('%s\r\n' % string)

	def say_it(self, aList):
		#say something, text to speech 
		words = ''
		try:
			for i in aList[:]:
				words += (i + ' ')
			self.droid.ttsSpeak(words)
		except:
			print "speech error"

if __name__ == '__main__':
	#example bot that can be made using this framework
	myBot = Framework()
	myBot.join(myBot.channel)
	myBot.speakEnabled = False

	while 1: 
		myBot.parse()
		if 'PING' in myBot.raw_string:
			myBot.pong()

		#bot commands/responding conditions
		if myBot.line[0] == '!quit':
			myBot.write('cya later %s :D' % myBot.get_nick())
			break
		
		if myBot.line[0] == '!sayit': 
			myBot.say_it(myBot.line[1:])
		
		if myBot.line[0] == '!speech':
			if len(myBot.line) > 1:
				if myBot.line[1] == 'disable':
					myBot.speakEnabled = False
					myBot.write("will no longer speak lines from IRC")
				elif myBot.line[1] == 'enable':
					myBot.speakEnabled = True
					myBot.write("will start speaking lines from IRC")

		if myBot.line[0] == '!join':
			if len(myBot.line) > 1:
				myBot.join(myBot.line[1])

		print myBot.raw_string
		if myBot.speakEnabled:
			myBot.say_it([myBot.get_nick()])
			myBot.say_it(myBot.line[:])
