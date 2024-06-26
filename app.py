
# publish.py
import uuid
import json
import re
from uuid import UUID
from flask import Flask, render_template, request, redirect, jsonify
from firebase import *
from validate import *
from smtp_c import sendEmail, sendSMTP
from sendQ import sendMessageToQueue
import logging
import importlib
from conf import PROD

if PROD:
    config = importlib.import_module("config")
else:
    config = importlib.import_module("config1")

	

app = Flask(__name__)
#executor = ThreadPoolExecutor()
app.config['DEBUG'] = config.DEBUG	#True  # Enable debug mode
if config.DEBUG:
	logging.basicConfig(level=logging.DEBUG)
    
       	 

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        scan_domain = request.form['scan_domain']
        scan_type = request.form['scan_type']

        # Run the async function in a separate thread
        print(scan_type)
        executor.submit(run_async_task, scan_domain, scan_type)
        return redirect(f"/scan/{scan_domain}", code=302) 

                
    return render_template('index.html')

@app.route('/scan', methods=['GET', 'POST'])
def scan():
	scan_id = uuid.uuid4().hex
	scantype = request.form['scan_type']	
	email = request.form["email"]
	host = request.form["scan_domain"]

	
	if validate_email(email) and validate_domain(host) and validate_type(scantype):
        	# cool. continue
        	print('valid data')
	else:
        	# If email is invalid, redirect to home page
        	return render_template('index.html')
	
	
	encoded_email = email.replace('.', ',')
	email_id = uuid.uuid4().hex
	
	#here is our logic
	isRegistred = isemailRegistered(encoded_email)
	if isRegistred == 1:
		#send message to Q
		sendMessageToQueue(scantype, scan_id, email, host)
		print("Email is validated. Message sent to Q")
		msg = "Email is validated. Message sent to Q"
	else:
		if isRegistred == 0:
			#we need to create new email
			addNewEmail(encoded_email, email_id, host, scantype, scan_id)
			print("Email added successfully.")
			msg = "Email added successfully."
			
			validateUrl = sendEmail(email, email_id)
			print("we sent an email... please verify your email for the scan to begin")
			msg = f"we sent an email to: {email} please verify your email for the scan to begin"
		if isRegistred == -1:
			print("maybe an error... not sure")
			msg = "maybe an error... not sure"	
	
	return render_template('register.html', msg = msg )


@app.route('/sendmail', methods=['GET'])
def sendMail():
	email = request.args.get("email")
	message = request.args.get("msg")
	subject = request.args.get("subject")
	pwd = request.args.get("pwd")
	
	success = sendSMTP(email, subject, message, pwd)
	if success:
		return jsonify({'message': 'Success'}), 200
	else:	
		return jsonify({'message': 'Internal Server Error'}), 500
	



	
@app.route('/validate', methods=['GET'])
def validate():
	#'email={email}&emailid={emailid}&secret={secret}'
	email = request.args.get("email")
	email_id = request.args.get("id")
	checksum = request.args.get("checksum")
	encoded_email = email.replace('.', ',')
	
	
	print("*******************************************\r\n")
	print (email, email_id, checksum)

	#scan_id, scan_type, url  = "a", "a", "b"
	if validateEmailwithChecksum(email, email_id, checksum):
		print("Validate Email function here !!!")
		validateEmailFirebase(encoded_email, email_id)
		scan_id, scan_type, url = getFirstScan(encoded_email)
		sendMessageToQueue(scan_type, scan_id, email, url)
		#sendMessageToQueue(email, url, scan_type, scan_id)
		msg = "Email was validate correctly.\t Your scan has been sent to Q. \tYou will be notifed by email when scan is completed."
	else:
		msg = 'validate failed'
			
	return render_template('validate.html', msg = msg )



@app.route('/reports/<string:scan_id>/<string:scan_type>', methods=['GET'])
def get_reports(scan_id, scan_type):
	print("******scanid:=" + scan_id)
	#sid = "01888888"
	
	result = getScanData(scan_id, scan_type)
			
	print(result)
	if result is None:
		return jsonify({'message': 'Resource not found'}), 404	
	#build report
	scandata = json.dumps(result)
	print("#######  scandata:=" + scandata)
	return render_template('report.html', insetedJson = scandata )



@app.route('/reports/list', methods=['GET'])
def get_url_list():
	pwd = request.args.get('pwd')
	host = request.args.get('domain')
	result = None
	if (pwd == config.read_secret('LIST_OF_DOMAINS')):
		result = get_scans_by_hostname(host)
			
	print(result)
	if result is None:
		return jsonify({'message': 'Resource not found'}), 404	
	#build report
	scandata = json.dumps(result)
	print("#######  scandata:=" + scandata)
	return render_template('report.html', insetedJson = scandata )



def validate_email(email):  
	# Regular expression for validating email addresses
	print(email)
	pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

	# Check if the email matches the pattern and does not contain <, >, or /
	if re.match(pattern, email) and '<' not in email and '>' not in email and '/' not in email:
		return True
	else:
		return False


def validate_domain(domain):
	print(domain)
	# Regular expression for validating email addresses
	pattern = r'^[a-zA-Z0-9.]+$'

	# Check if the email matches the pattern
	if re.match(pattern, domain):
		return True
	else:
		return False
        
def validate_type(input_type):
    allowed_types = config.ALLOWED_TYPES	#['XSS', 'subdomain', 'FullScan', 'LFI']
    
    return input_type in allowed_types
       	




if __name__ == '__main__':
    app.run(debug=True)


