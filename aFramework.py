#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Android Bot Framework
# version 1.0.1
#
#  aFramework.py
#  
#  Copyright 2013 Cobra2
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

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
		self.channel = self.droid.dialogGetInput("Channel", "join which channel?", '#').result
		self.port = 6667
		if (not self.nick):
			self.nick = "IrcDroidB0t"
		elif (not self.server):
			self.server = "irc.hackthissite.org"
		elif (not self.channel):
			self.channel = "#hackthissite"

	def join(self, string):
		#join a channel
    time.sleep(2)
		self.channel = string
		self.s.send('JOIN %s\r\n' % string)
	
	def pong(self):
		self.s.send('PONG ' + self.raw_string.split()[1] + '\r\n')

	def parse(self):
		#irc parser
		self.line = self.s.recv(1024)
		self.raw_string = self.line
		self.raw = self.line.split(":")
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
		return self.raw[1:self.raw.find('!')]
		
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
		except:#errors should be defined
			print "speech error"#why no raise statement here?

if __name__ == '__main__':
	#example bot that can be made using this framework
	myBot = Framework()
	myBot.join(myBot.channel)
	myBot.speakEnabled = False

	while True:
		myBot.parse()
		if myBot.raw_string.startswith('PING'):
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
