import pika
import json
from config import read_secret

RABBITMQ = 'RABBITMQPW'

class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
   	 if isinstance(obj, UUID):
   		 return str(obj)  # Convert UUID to string
   	 return json.JSONEncoder.default(self, obj)
   	 
def sendMessageToQueue(scantype, scan_id, email, host):
	# Access the CLODUAMQP_URL environment variable and parse it
	url = read_secret(RABBITMQ)


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
