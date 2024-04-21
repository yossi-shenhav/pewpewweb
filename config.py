import os

# Configuration setting to determine the source of sensitive information
USE_DOCKER_SECRETS = True
BUCKET_URL = 'https://pewpewscanresults.s3.amazonwas.com/'
GMAIL_PASSWORD = 'GMAIL_PASSWORD'
GMAIL_ADDRESS = 'GMAIL_ADDRESS'
RABBIT_MQ = 'RABBIT_MQ'
BASE_URL = 'BASE_URL'
LIST_OF_DOMAINS = 'LIST_OF_DOMAINS'

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
        return os.getenv(secret_name)	#os.environ[secret_name]
        


