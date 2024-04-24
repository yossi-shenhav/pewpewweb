import pika
import json
import importlib
from conf import PROD

if PROD:
    config = importlib.import_module("config")
else:
    config = importlib.import_module("config1")

#from config import read_secret, RABBIT_MQ

#RABBITMQ = 'RABBIT_MQ'

class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
   	 if isinstance(obj, UUID):
   		 return str(obj)  # Convert UUID to string
   	 return json.JSONEncoder.default(self, obj)
   	 
def sendMessageToQueue(scantype, scan_id, email, host):
	# Access the CLODUAMQP_URL environment variable and parse it
	url = config.read_secret(config.RABBIT_MQ)


	message = {
	    "type": scantype,
	    "email": email,
	    "url2scan": host,    
	    "tid": scan_id
	    }

	s_body = json.dumps(message, cls=UUIDEncoder)

	params = pika.URLParameters(url)
	connection = pika.BlockingConnection(params)
	channel = connection.channel() # start a channel
	channel.queue_declare(queue='nucleiscans') # Declare a queue
	channel.basic_publish(exchange='',
			  	routing_key='nucleiscans',
			  	body=s_body)

	print("message sent")
	connection.close()
