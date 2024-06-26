#!/usr/bin/env python

import smtplib
import email.mime.text
import os
from firebase import getchecksumSignature


from email.mime.text import MIMEText
#from config import * 
import importlib
from conf import PROD

if PROD:
    config = importlib.import_module("config")
else:
    config = importlib.import_module("config1")



def sendSMTP(to_email, subject, message, pwd=None):
	from_email = config.read_secret(config.GMAIL_ADDRESS)
	#print("##### " + from_email)
	if pwd == None:
		pwd = config.read_secret(config.GMAIL_PASSWORD)  
	print("##### " + pwd)
	msg = MIMEText(message,'html')
	msg['Subject'] = subject
	msg['From'] = from_email
	msg['To'] = to_email
	ret = True
	try:
		s = smtplib.SMTP_SSL('smtp.gmail.com', '465')
		s.login(from_email, pwd)
		s.sendmail(from_email, to_email, msg.as_string())
		s.quit()
		print("Email sent successfully!")
	except Exception as e:
		ret = False
		print("Email sending failed:", e)
		print(f'Email:={from_email},	PWD:={pwd}')	

	return ret
def sendEmail(email, emailid):
	#first we need generate URL
	baseurl = config.read_secret(config.BASE_URL)
	mail = email.replace("+", "%2B") #url encode + sign
	
	checksum = getchecksumSignature(email, emailid)
	print("daniel" + baseurl + checksum)
	url2Send = baseurl + f'/validate?email={mail}&id={emailid}&checksum={checksum}'
	
	
	message = f'<p>Dear PEWPEW user, to validate your email click this <a href="{url2Send}">validation link</a> or copy and paste {url2Send} to your browser.</p>' 
	
	sendSMTP(email, "Ranger Email Validation", message)
	
	
	return 1
