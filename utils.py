#!/usr/bin/python
import logging
import sys
import random
import mimetypes

logz=logging
logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
ATTACHMENTS_DIR = '.'

def create_recipients_string(recipients_list):
	recipients = ""
	for recipient in recipients_list[:-1]:
		recipients += recipient + ", "
		recipients += recipients_list[-1]
	return recipients

def get_random(lista):
	if len(lista)==0:
		return 0
	logz.info("Extract a random  from the list")
	random_index = random.randint(0, (len(lista))-1 )
	random_object = lista[random_index]
	logz.info("Random: %s", random_object)
	return random_object


def purgeThisMessageFromTheAttachments(aMessage):
	""" this function is recursive, if the message contains
	multipart message the function is recursively called to
	purge all the attachments"""

	partsToDelete = [] #empty list
	index = 0
	list = aMessage.get_payload()

	#end of recursion, the payload is a string
	if type(list) == type(""):
		return

	for part in list:
		maintype =  part.get_content_maintype()
		print maintype

		#I mark this part for delete, because it is not text
		if ( maintype != "text" and maintype != "multipart" and
			maintype != "message"):
			# Also the message type is a kind of multipart
			partsToDelete.append(index)

		if (maintype == "multipart" or maintype == "message"):
			#recursive call
			purgeThisMessageFromTheAttachments(part)
		index = index + 1

		#I can now delete the parts
		listParts = aMessage.get_payload()
		offset = 0


		for indexToDelete in partsToDelete:
			#print indexToDelete
			indexToDelete = indexToDelete - offset
			#let's save the part that we wish to delete.
			filename = listParts[indexToDelete].get_filename()
			if not filename:
				ext = mimetypes.guess_extension(part.get_type())
				if not ext:
					#generic extension
					ext = ".bin"
					filename = "part-%03d%s" % (indexToDelete, ext)

			fp = open (ATTACHMENTS_DIR + filename, "wb")
			fp.write(listParts[indexToDelete].get_payload(decode=1))
			fp.close()
			del listParts[indexToDelete]
			offset = offset + 1
			#print listParts

#get score of a rule from rules.conf
def getScore(rule_name, data):
	for rule in data.rules:
		str=rule.name+"_"+rule.rule
		if str==rule_name:
			return rule.score
