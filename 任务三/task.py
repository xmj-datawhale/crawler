import requests
import traceback
import re
import urllib

# req = requests.get('https://www.baidu.com',timeout=60,proxies={'http':'59.173.73.112:3128'})
req = requests.get('https://www.baidu.com',timeout=60,proxies={'socks4/5':'121.63.198.84:6668'})
print(req.content)