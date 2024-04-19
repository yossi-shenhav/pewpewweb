import firebase_admin
import uuid
import hashlib
from firebase_admin import credentials
from firebase_admin import db
from firebase import getchecksumSignature

# Initialize Firebase Admin SDK
#cred = credentials.Certificate('cred/erviceAccountKey.json')
#firebase_admin.initialize_app(cred, {
#    'databaseURL': 'https://pewpew-7387e-default-rtdb.firebaseio.com/' 
#})


# Function to check if an email is validated
def validateEmailFirebase(email, emailid):
	ref = db.reference('pewpew/emails/' + email + '/details' )
	details = ref.get()
	validate = False
	if details:
		# Iterate over the attributes and print them
		for key, value in details.items():
			if (key=='emailid') and (value==emailid):
				validate = True
	if (validate == True):
		#update validated
		ref.update({
		'validated': True,
		})

# Function to retrive first scan details 
def getfirstScan(email):
	ref = db.reference('pewpew/emails/' + email + '/firstscan' )
	scan = ref.get()
	
	print(scan)
	scan_id = scan["scan_id"]
	scan_type = scan["scantype"]
	url = scan["url"]
	print (f"id={scan_id}, type={scan_type}, url={url}")
	

	return scan_id, scan_type, url	

 
def validateEmailwithChecksum(email, emailid, checksum):
	print(f'email:={email}\r\n')
	checksum1 = getchecksumSignature(email, emailid)
	if (checksum1==checksum):
		print (f'{checksum}:={checksum1}value=true')
	else:
		print (f'{checksum}:={checksum1}value=false')
			
	return (checksum == checksum1)
	
		
		    		
	
# Example usage:
if __name__ == "__main__":
	email = 'example@example.com'
	encoded_email = email.replace('.', ',')

	#email_id = from url
	#checksum = from url
	
	getfirstScan(encoded_email)

	#here is our logic
	#if validate(email, emailid, checksum):
	#	validateEmail(encoded_email, emailid)
	#	#now read firstscan data from firebase and send to Q
