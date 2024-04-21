#!/usr/bin/env python

import smtplib
import email.mime.text
import os
from firebase import getchecksumSignature


from email.mime.text import MIMEText
from config import * 




def sendSMTP(to_email, subject, message):
	from_email = read_secret(GMAIL_ADDRESS)
	#print("##### " + from_email)
	pwd = read_secret(GMAIL_PASSWORD)  
	print("##### " + pwd)
	msg = MIMEText(message,'html')
	msg['Subject'] = subject
	msg['From'] = from_email
	msg['To'] = to_email
	try:
		s = smtplib.SMTP_SSL('smtp.gmail.com', '465')
		s.login(from_email, pwd)
		s.sendmail(from_email, to_email, msg.as_string())
		s.quit()
		print("Email sent successfully!")
	except Exception as e:
		print("Email sending failed:", e)
		print(f'Email:={from_email},	PWD:={pwd}')	


def sendEmail(email, emailid):
	#first we need generate URL
	baseurl = read_secret(BASE_URL)
	mail = email.replace("+", "%2B") #url encode + sign
	
	checksum = getchecksumSignature(email, emailid)
	print("daniel" + baseurl + checksum)
	url2Send = baseurl + f'/validate?email={mail}&id={emailid}&checksum={checksum}'
	
	
	message = f'<p>Dear PEWPEW user, to validate your email click this <a href="{url2Send}">validation link</a> or copy and paste {url2Send} to your browser.</p>' 
	
	sendSMTP(email, "Ranger Email Validation", message)
	
	
	return 1
