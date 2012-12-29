**********************************************
*	IRC Framework for Android
*	VERSION 1.0.0
*	Written by c0bra2; project started (2012)
*	This code is protected under the GPL


This Project was started as a Framework class which can be used to make IRC bots
quickly and easily while also implementing features unique to the Android API.
The Framework was written in python and impemented using scripting layer 4 android
(sl4a). 

********************
*Using the features*
********************
The class provides useful class methods to parse data, to interface with IRC, and
with the Android api; an example bot has been provided with the source code to 
demonstrate some of these. In general a line of irc information will be split into 
a list structure and accessed using an instance of the class and ".line[n]"; for 
example myBot.line[0] would be the first element of the list and is often a good 
place for bot commands which can be tested using a statement such as 

if myBot.line[0] == '!command':

line[] elements that are > 0 can be used for command arguments, for example
if (myBot.line[0] == '!command') and (myBot.line[1] == 'commandarg1')

however you should always test to see that the length of line[] is as long
as the subscript you are trying to use otherwise you will get an IndexError: 
Index out of range. and your bot will crash.

*************************
*ToDo for future version*
*************************
*	bug fixes (connectivity issues etc)
*	clean up the code
*	add more methods to the Framework which add additional API and IRC features
