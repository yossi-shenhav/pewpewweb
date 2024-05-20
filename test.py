
from firebase import *

host = 'xss.challenge.training.hacq.me'

result = get_scans_by_hostname(host)
print(result)
