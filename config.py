import os
from google.cloud import secretmanager 

# Configuration setting to determine the source of sensitive information
USE_DOCKER_SECRETS = True
DEBUG = True
ALLOWED_TYPES = ['XSS', 'subdomain', 'PortScan', 'LFI', 'SSLScan', 'FullScan', 'hiddendir', 'FastPortScan']

BUCKET_URL = 'BUCKET_URL'	#'https://pewpewscanresults.s3.amazonwas.com/'
GMAIL_PASSWORD = 'GMAIL_PASSWORD'
GMAIL_ADDRESS = 'GMAIL_ADDRESS'
RABBIT_MQ = 'RABBIT_MQ'
BASE_URL = 'BASE_URL'
LIST_OF_DOMAINS = 'LIST_OF_DOMAINS'
project_id = 'pewpew-421014'



def read_secret(secret_id):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode('UTF-8') 
        


