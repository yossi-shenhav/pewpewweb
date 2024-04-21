import firebase_admin
import uuid
import hashlib
import os
import json
from firebase_admin import credentials
from firebase_admin import db
from config import read_secret

# Initialize Firebase Admin SDK

#shai - you should change to secret again
mounted_directory = 'cred/erviceAccountKey.json' #'/container/app/erviceAccountKey.json'

cred = credentials.Certificate(mounted_directory)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://pewpew-7387e-default-rtdb.firebaseio.com/' 
})



        
def getScanData(scanid, scantype):
	ref = db.reference(f'pewpew/reports/{scanid}')
	scan_data = ref.get()

	if scan_data:
		
		rs = json.dumps(scan_data)
		hostname = scan_data.get('hostname', '')
		scantyperesults = scan_data.get(scantype, {})
		if not scantyperesults:
			return None
		else:
			print(scantyperesults)
			#results = scantyperesults["results"]
			#return {'hostname': hostname, 'scantype': scantype, 'results': results}
			return {'hostname': hostname, 'scantype': scantype, 'results': scantyperesults}
	else:
		return None
  

        

# Function to check if an email exists in the database
def isEmailExist(email):
	ref = db.reference('pewpew/emails')
	email_ref = ref.child(email)
	return email_ref.get() is not None

# Function to check if an email is validated
def isEmailValidated(email):
	ref = db.reference('pewpew/emails/' + email + '/details')
	details = ref.get()
	if details:
		return details.get('validated', True)	#need to test
	return False

# Function to add a new email
def addNewEmail(email, email_id, url, scan_type, scan_id):
    email_ref = db.reference('pewpew/emails/' + email)
    email_details_ref = email_ref.child('details')
    email_details_ref.set({
        'emailid': email_id,
        'validated': False
    })
    first_scan_ref = email_ref.child('firstscan')
    first_scan_ref.set({
        'url': url,
        'scantype': scan_type,
        'scan_id': scan_id
    })
        

def isemailRegistered(email):
    # Check if email exists
    if isEmailExist(email):
        #check if validated
        if isEmailValidated(email):
            return 1
        else:
            return -1
    else:
    	#return 0
    	return 0


def getFirstScan(email):
	email_ref = db.reference('pewpew/emails/' + email)

	first_scan_ref = email_ref.child('firstscan')
	data = first_scan_ref.get()
	print(data)

	return data["scan_id"], data["scantype"], data["url"]
	



def getchecksumSignature(email, emailid):
	#same function should be used on /validate
	#Shai more secret to deal with
	secret = read_secret("stupidsecret")	
	str2hash = f'email={email}&emailid={emailid}&secret={secret}' 
	
	print(f'str2hash := {str2hash}')

	# Create a SHA1 hash object
	sha1_hash = hashlib.sha1()

	# Update the hash object with the input string
	sha1_hash.update(str2hash.encode('utf-8'))

	# Get the hexadecimal representation of the hash
	return sha1_hash.hexdigest()

def get_scans_by_hostname(hostname):
	reports_ref = db.reference('pewpew/reports')
	uuid_list = {}
	reports = reports_ref.get()
	if reports:
		for uuid, data in reports.items():
			if data.get('hostname') == hostname:
				for child_name in data.keys():
					path = f"/reports/{uuid}/{child_name}"
					uuid_list[child_name] = path

	return {'hostname': hostname, 'scantype': 'blank', 'results': uuid_list}



# Example usage:
#if __name__ == "__main__":
#	email = 'example@example.com'
#	encoded_email = email.replace('.', ',')
#
#	email_id = uuid.uuid4().hex
#	url = 'https://example.com'
#	scan_type = 'xss'
#	scan_id = uuid.uuid4().hex


	#here is our logic
#	isRegistred = isemailRegistered(encoded_email)
#	if isRegistred == 1:
#		#send message to Q
#		sendMessage2Q(email, url, scantype, scan_id)
#		print("Email is validated. Message sent to Q")
#	else:
#		if isRegistred == 0:
#			#we need to create new email
#			addNewEmail(email, email_id, url, scan_type, scan_id)
#			print("Email added successfully.")
#			sendEmail(email, email_id)
#			print("we send an email... please verify your email for the scan to begin")
#		if isRegistred == -1:
#			print("we send an email... please verify your email for the scan to begin")
