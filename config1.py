import os

#this is config for web

# Configuration setting to determine the source of sensitive information
USE_DOCKER_SECRETS = False
BUCKET_URL = 'https://pewpewscanresults.s3.amazonwas.com/'
GMAIL_PASSWORD = 'GMAIL_PASSWORD'
GMAIL_ADDRESS = 'GMAIL_ADDRESS'
RABBIT_MQ = 'RABBIT_MQ'
BASE_URL = 'BASE_URL'

#url = 'amqps://wqeixhdm:R8TtQzBLzIlduXU4sJjpg0GZWnXeXzg4@whale.rmq.cloudamqp.com/wqeixhdm'

def read_secret(secret_name):
	if USE_DOCKER_SECRETS:
		secret_path = '/run/secrets/{}'.format(secret_name)
		try:
			with open(secret_path, 'r') as file:
				secret_value = file.read().strip()
			return secret_value
		except FileNotFoundError:
			print("Secret '{}' not found.".format(secret_name))
			return None
	else:
		# Read from environment variable
		conf = ''

		if secret_name == 'BUCKET_URL':
			conf = 'https://pewpewscanresults.s3.amazonwas.com/'

		match secret_name:
			case 'GMAIL_PASSWORD':
				conf = 'niwd wieb ubou aptl'
			case 'GMAIL_ADDRESS ':
				conf = 'ranger@komodosec.com'
			case 'RABBIT_MQ':
				conf = 'amqps://wqeixhdm:R8TtQzBLzIlduXU4sJjpg0GZWnXeXzg4@whale.rmq.cloudamqp.com/wqeixhdm'
			case 'stupidsecret':
				conf = 'stupidsecret'
			case 'BASE_URL':
				conf = 'https://pewpew.komodosec.com'
	return conf	#os.getenv(secret_name)	#os.environ[secret_name]
        
