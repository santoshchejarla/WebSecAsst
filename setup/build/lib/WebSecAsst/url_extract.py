#! /home/chs/anaconda3/envs/sw/bin/python 
import requests
import re
import tldextract
import whois
from datetime import date,datetime
import urllib
import ssl
import socket
import OpenSSL
from bs4 import BeautifulSoup
import pickle
import xgboost
import numpy as np
import pandas as pd
import sys

def is_ip_check(address):
    return 1 if address.split('.')[-1].isalpha() else -1
def len_check(url):
    if len(url)<54: return 1
    if len(url)<=75: return 0
    return -1

def url_shortner_check(url):
    return -1 if re.search('bit\.ly|tinyurl\.com|goo\.gl|ow\.ly|t\.co|bitly\.com|',url) else 1

def has_at_check(url):
    return -1 if re.search('@',url) else 1

def has_dslash_check(url):
    if url[:7]=="http://":
        url=url[7:]
    else:
        url=url[8:]
    return -1 if re.search('//',url) else 1

def has_dash_check(domain):
    return -1 if re.search('-',domain) else 1

def has_dash_check(domain):
    if re.search('-',domain): return -1
    return 1

def num_sub_domains_check(suffix):
    count=suffix.count('.')
    if count==0:
        return 1
    elif count==1:
        return 0
    return -1

def https_ssl_check(domain,url):
    if url[:5]!='https': return -1
    try:
        context = ssl.create_default_context()
        conn = socket.create_connection((domain, 443))
        sock = context.wrap_socket(conn, server_hostname=domain)
        sock.settimeout(5)
        der_cert = sock.getpeercert(True)
        certificate=ssl.DER_cert_to_PEM_cert(der_cert)
        x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, certificate)
        issuer=str(x509.get_issuer().get_components()[1][1])[2:-1]
        notBefore=datetime.strptime(str(x509.get_notBefore())[2:-1], '%Y%m%d%H%M%SZ')
        notAfter=datetime.strptime(str(x509.get_notAfter())[2:-1], '%Y%m%d%H%M%SZ')
        age=(notAfter-notBefore).days
        trusted=['Comodo','GeoTrust','DigiCert','GlobalSign','Symantec','Thawte','IdenTrust','Entrust','Network Solutions','RapidSSL','GoDaddy','Secom','StartCom','TrustWave','Sectigo','Google']
        if age>365 and re.search('|'.join(trusted),issuer): return 1
        return 0
    except:
        return -1

def domain_reg_len_check(start,end):
    try:
        days_count=(end-start).days
        return -1 if days_count<=365 else 1
    except:
        return -1

def favicon_check(soup,domain):
    icon_link = soup.find("link", rel="shortcut icon")
    if icon_link:
        return 1 if tldextract.extract(icon_link["href"]).domain==domain else -1
    return 1

def http_token_check(url):
    if url[:7]=="http://":
        url=url[7:]
    else:
        url=url[8:]
    if re.search("http|https",url):
        return -1
    return 1

def request_url_check(soup,domain):
    total_domains=0
    same_domain=0
    for image in soup.find_all('img',src=True):
        img_url=image["src"]
        img_domain=tldextract.extract(img_url).domain
        total_domains+=1
        same_domain+= 1 if img_domain==domain else 0
    for audio in soup.find_all('audio',src=True):
        aud_url=audio["src"]
        aud_domain=tldextract.extract(aud_url).domain
        total_domains+=1
        same_domain+= 1 if aud_domain==domain else 0
    for embed in soup.find_all('embed',src=True):
        embed_url=embed["src"]
        embed_domain=tldextract.extract(embed_url).domain
        total_domains+=1
        same_domain+= 1 if embed_domain==domain else 0
    if total_domains==0: return 1
    percent=same_domain/total_domains
    if percent>=0.61: return 1
    elif percent>=0.22: return 0
    return -1

def anchor_check(soup,domain):
    total_domains=0
    unsafe=0
    for a in soup.find_all('a',href=True):
        link_domain=tldextract.extract(a["href"]).domain
        total_domains+=1
        if domain!=link_domain or re.search("#|javascript",a['href'],re.IGNORECASE):
            unsafe+=1
    if total_domains==0: return 1
    percent=unsafe/total_domains
    if percent<0.31: return 1
    if percent<=0.67: return 0
    return -1

def links_check(soup,domain):
    total_domains=0
    unsafe=0
    for link in soup.find_all('link',href=True):
        link_domain=tldextract.extract(link['href']).domain
        total_domains+=1
        if domain!=link_domain:
            unsafe+=1
    for script in soup.find_all('script',src=True):
        script_domain=tldextract.extract(script['src'])
        total_domains+=1
        if script_domain!=domain:
            unsafe+=1
    if total_domains==0: return 1
    percent=unsafe/total_domains
    if percent>0.81: return -1
    elif percent>=17: return 0
    return 1 

def sfh_check(soup,domain):
    for form in soup.find_all('form',action=True):
        if re.search('about:blank',form['action'],re.IGNORECASE) or form['action']=="":
            return -1
        form_domain=tldextract.extract(form['action']).domain
        if form_domain!=domain:
            return 0
    return 1

def mail_check(soup):
    for form in soup.find_all('form',action=True):
        if re.search('mail:to',form['action'],re.IGNORECASE):
            return -1
    return 1

def abnormal_check(url,domain):
    try:
        return -1 if domain!=whois.query(tldextract.extract(url).registered_domain).name else 1
    except:
        return -1

def redirect_check(url):
    r=requests.get(url,allow_redirects=True)
    if len(r.history)<=1:
        return 1
    elif len(r.history)<4:
        return 0
    return -1

def right_click_check(page):
    if re.search('contextmenu',page,re.IGNORECASE): return -1
    return 1

def iframe_check(soup):
    for frame in soup.find_all('iframe'):
        if frame.get('frameborder') and frame['frameborder']=="0": return -1
    return 1

def age_check(start):
    try:
        today=datetime.now()
        diff=((today-start).days)/30
        return 1 if diff>=6 else -1
    except:
        return -1

def dns_check(whois_data):
    if whois_data: return 1
    return -1

def alexa_top_check(domain):
    try:
        rank=BeautifulSoup(requests.get("http://data.alexa.com/data?cli=10&dat=s&url="+ domain).text, "xml").find("REACH")['RANK']
        return 1 if rank<100000 else 0
    except:
        return -1

def google_index_check(url):
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
    headers = { 'User-Agent' : user_agent}
    try:
        query="https://www.google.com/search?q=site:"+url
        r=requests.get(query,headers=headers)
        soup = BeautifulSoup(str(r.content), "html.parser")
        for link in soup.find("div", {"class": "g"}).find_all("link",href=True):
            if re.search(url,link['href']): return 1
        return -1
    except:
        return -1

url=sys.argv[1]
domain_data=tldextract.extract(url)
try:
    whois_data=whois.query(domain_data.registered_domain)
except:
    whois_data=None
page=requests.get(url)
soup=BeautifulSoup(page.content,'html.parser')
checks=[]
checks.append(is_ip_check(domain_data.domain))
checks.append(len_check(url))
checks.append(url_shortner_check(url))
checks.append(has_at_check(url))
checks.append(has_dslash_check(url))
checks.append(has_dash_check(domain_data.domain))
checks.append(num_sub_domains_check(domain_data.suffix))
checks.append(https_ssl_check(domain_data.registered_domain,url))
if whois_data:
    checks.append(domain_reg_len_check(whois_data.creation_date,whois_data.expiration_date))
else:
    checks.append(-1)
checks.append(favicon_check(soup,domain_data.domain))
checks.append(http_token_check(url))
checks.append(request_url_check(soup,domain_data.domain))
checks.append(anchor_check(soup,domain_data.domain))
checks.append(links_check(soup,domain_data.domain))
checks.append(sfh_check(soup,domain_data.domain))
checks.append(mail_check(soup))
checks.append(abnormal_check(url,domain_data.domain))
checks.append(redirect_check(url))
checks.append(right_click_check(page.text))
checks.append(iframe_check(soup))
if whois_data:
    checks.append(age_check(whois_data.creation_date))
    checks.append(dns_check(whois_data))
else:
    checks.append(-1)
    checks.append(-1)
checks.append(alexa_top_check(domain_data.registered_domain))
checks.append(google_index_check(url))


columns=['having_IP_Address','URL_Length','Shortining_Service','having_At_Symbol',
'double_slash_redirecting','Prefix_Suffix','having_Sub_Domain','SSLfinal_State',
'Domain_registeration_length','Favicon','HTTPS_token','Request_URL','URL_of_Anchor',
'Links_in_tags','SFH','Submitting_to_email','Abnormal_URL','Redirect','RightClick',
'Iframe','age_of_domain','DNSRecord','web_traffic','Google_Index']
df=[]
df.append(checks)
df=pd.DataFrame(df,columns=columns)
model=pickle.load(open('xgbmodel.pkl',"rb"))
if model.predict(df)[0]==1:
    print("SAFE")
else:
    print("MALICIOUS")