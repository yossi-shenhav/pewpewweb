import os

# Configuration setting to determine the source of sensitive information
USE_DOCKER_SECRETS = True
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
        return os.getenv(secret_name)	#os.environ[secret_name]
        


