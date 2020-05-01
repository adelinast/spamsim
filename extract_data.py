#!/usr/bin/python
import sys
import os
import re
import logging

logz=logging
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

class Data:
	date=None
	rules=None
	header_regex=None
	dnsbl=None
	dnsbl_answer=None
	subject_list=None
	rcpt_list=None
	from_list=None
	plainTexts=None
	
	def __init__(self):
		self.date=[]
		self.rules=[]
		self.header_regex=[]
		self.dnsbl=[]
		self.dnsbl_answer=[]
		self.subject_list=[]
		self.rcpt_list=[]
		self.from_list=[]
		self.plainTexts=[]
		
class Date:
	year=None
	month=None
	day=None
	hour=None
	minute=None
	second=None

class Rule:
	name=None
	rule=None
	description=None
	score=0.0

class HeaderRegex:
	header=None
	regex=None

class DnsblAnswer:
	dnsbl=None
	answer=None
	description=None

class Subject:
	subject=None

class Rcpt:
	rcpt=None

class From:
	mailFrom=None

class Text:
	plainText=None
	htmlText=None
	
def loadConfFile(file, data):
	if not os.path.exists(file):
		logz.error("file %s does not exist", file)
		return
	f = open(file, "r")
	for line in f:
		matchObj = re.match(r"""^(\s*\d+\s*)\| # year
(\s*\d+\s*)\| #month
(\s*\d+\s*)\| #day
(\s*\d+\s*)\| #hour
(\s*\d+\s*)\| #minute
(\s*\d+\s*)$""", line, re.VERBOSE)
		if matchObj:
			"""
			logz.debug("Line: %s" % line)
			logz.debug("matchObj.group() : %s" % matchObj.group())
			logz.debug("matchObj.group(0) : %s" % matchObj.group(0))
			logz.debug("matchObj.group(1) : %s" % matchObj.group(1))
			logz.debug("matchObj.group(2) : %s" % matchObj.group(2))
			logz.debug("matchObj.group(3) : %s" % matchObj.group(3))
			logz.debug("matchObj.group(4) : %s" % matchObj.group(4))
			logz.debug("matchObj.group(5) : %s" % matchObj.group(5))
			logz.debug("matchObj.group(6) : %s" % matchObj.group(6))
			"""
			date=Date()
			date.year=int(matchObj.group(1))
			date.month=int(matchObj.group(2))
			date.day=int(matchObj.group(3))
			date.hour=int(matchObj.group(4))
			date.minute=int(matchObj.group(5))
			date.second=int(matchObj.group(6))
			data.date.append(date)

def loadRulesFile(file, data):
	if not os.path.exists(file):
		logz.error("file %s does not exist", file)
		return
	f = open(file, "r")
	for line in f:
		matchObj = re.match(r"""^(.*?)_(.*?)\|(.*?)\|(.*?) $""", line, re.VERBOSE)
		if matchObj:
			"""
			logz.debug("Line: %s" % line)
			logz.debug("matchObj.group() : %s" % matchObj.group())
			logz.debug("matchObj.group(0) : %s" % matchObj.group(0))
			logz.debug("matchObj.group(1) : %s" % matchObj.group(1))
			logz.debug("matchObj.group(2) : %s" % matchObj.group(2))
			logz.debug("matchObj.group(3) : %s" % matchObj.group(3))
			logz.debug("matchObj.group(4) : %s" % matchObj.group(4))
			"""
			rule=Rule()
			rule.name=matchObj.group(1)
			rule.rule=matchObj.group(2)
			rule.description=matchObj.group(3)
			rule.score=float(matchObj.group(4))
			data.rules.append(rule)

def loadRegexFile(file, data):
	if not os.path.exists(file):
		logz.error("file %s does not exist", file)
		return
	f = open(file, "r")
	for line in f:
		matchObj = re.match(r"""^(.*?)\| (.*?) $""", line, re.VERBOSE)
		if matchObj:
			"""
			logz.debug("Line: %s" % line)
			logz.debug("matchObj.group() : %s" % matchObj.group())
			logz.debug("matchObj.group(0) : %s" % matchObj.group(0))
			logz.debug("matchObj.group(1) : %s" % matchObj.group(1))
			logz.debug("matchObj.group(2) : %s" % matchObj.group(2))
			"""
			header_regex=HeaderRegex()
			header_regex.header=matchObj.group(1)
			header_regex.regex=matchObj.group(2)
			data.header_regex.append(header_regex)

def loadDnsblListFile(file, data):
	if not os.path.exists(file):
		logz.error("file %s does not exist", file)
		return
	f = open(file, "r")
	for line in f:
		matchObj = re.match(r"""^(\w+.*?)$""", line, re.VERBOSE)
		if matchObj:
			"""
			logz.debug("Line: %s" % line)
			logz.debug("matchObj.group() : %s" % matchObj.group())
			logz.debug("matchObj.group(0) : %s" % matchObj.group(0))
			"""
			dnsbl=matchObj.group(0)
			data.dnsbl.append(dnsbl)
			
def loadDnsblAnswerFile(file, data):
	if not os.path.exists(file):
		logz.error("file %s does not exist", file)
		return
	f = open(file, "r")
	for line in f:
		matchObj = re.match(r"""^(.*?)\| (.*?) \| (.*?) $""", line, re.VERBOSE)
		if matchObj:
			"""
			logz.debug("Line: %s" % line)
			logz.debug("matchObj.group() : %s" % matchObj.group())
			logz.debug("matchObj.group(1) : %s" % matchObj.group(1))
			logz.debug("matchObj.group(2) : %s" % matchObj.group(2))
			logz.debug("matchObj.group(3) : %s" % matchObj.group(3))
			"""
			dnsbl_answer=DnsblAnswer()
			dnsbl_answer.dnsbl=matchObj.group(1)
			dnsbl_answer.answer=matchObj.group(2)
			dnsbl_answer.description=matchObj.group(3)
			data.dnsbl_answer.append(dnsbl_answer)

def loadFieldsConfFile(file, data):
	if not os.path.exists(file):
		logz.error("file %s does not exist", file)
		return
	f = open(file, "r")
	for line in f:
		matchObj = re.match(r"""^(.*?)\| # field
(.*?)$""", line, re.VERBOSE)
		if matchObj:
			"""
			logz.debug("Line: %s" % line)
			logz.debug("matchObj.group() : %s" % matchObj.group())
			logz.debug("matchObj.group(0) : %s" % matchObj.group(0))
			logz.debug("matchObj.group(1) : %s" % matchObj.group(1))
			logz.debug("matchObj.group(2) : %s" % matchObj.group(2))
			"""
			if matchObj.group(1).strip()=='subject':
				subject=Subject()
				subject.subject=matchObj.group(2)
				data.subject_list.append(subject)
			elif matchObj.group(1).strip()=='from':
				mailFrom=From()
				mailFrom.mailFrom=matchObj.group(2)
				data.from_list.append(mailFrom)
			elif matchObj.group(1).strip()=='to':
				rcpt=Rcpt()
				rcpt.rcpt=matchObj.group(2)
				data.rcpt_list.append(rcpt)
			elif matchObj.group(1).strip()=='plainText':
				text=Text()
				text.plainText=matchObj.group(2)
				text.htmlText=None
				data.plainTexts.append(text)
			else:
				pass
