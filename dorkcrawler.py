# Google dorking automation tool
# @R00TUS3R

import sys, requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup

print(r"""
  ____          _   _____               _
 |    \ ___ ___| |_|     |___ ___ _ _ _| |___ ___ 
 |  |  | . |  _| '_|   --|  _| .'| | | | | -_|  _|
 |____/|___|_| |_,_|_____|_| |__,|_____|_|___|_|

""", file=sys.stderr)

def usage():
    print("""[*] Usage: python dorkcrawler.py <dork> <proxy: on/off>\n[*] Ex: python dorkcrawler.py "inurl:/index.php" off\n""", file=sys.stderr)
    sys.exit(1)

def stop():
    print("\n[!] Search finished\n", file=sys.stderr)
    sys.exit()

def load_proxy(num):
    with open('proxy.txt', 'r') as file:
        lines = file.readlines()
        proxy = lines[num].replace("\n", "")
    scheme = urlparse(proxy).scheme

    return {scheme: proxy}

def search(query, proxy_state):
    start = 0
    proxy_num = 0
    proxy_len = len(open('proxy.txt', 'r').readlines())

    while True:
        url = f"https://www.google.com/search?q={query}&start={start}&num=100"
        try:
            if (proxy_num == proxy_len): proxy_num = 0
            proxy = load_proxy(proxy_num)
            proxy_num += 1

            if (proxy_state == "on"): response = requests.get(url, proxies=proxy)
            elif (proxy_state == "off"): response = requests.get(url)

            if ("""<span class="r0bn4c rQMQod"> - did not match any documents.""" in response.text): stop()
            elif ("""Our systems have detected unusual traffic from your computer network.  This page checks to see if it&#39;s really you sending the requests, and not a robot.  <a href="#" onclick="document.getElementById('infoDiv').style.display='block';">Why did this happen?</a>""" in response.text):
                print("[!] Google detected unusual traffic.\n[!] Change your ip or use proxy list.\n")
                exit()
            else:
                soup = BeautifulSoup(response.text, 'html.parser')
                tags = soup.find_all('a', href=True)
                links = []
                for tag in tags:
                    href = tag['href']
                    if "url?q=" in href:
                        links.append(href.split('url?q=')[1].split('&')[0])
                links = links[:-2]
                for link in links: print(link)
            
            start += 100

        except KeyboardInterrupt:
            stop()
        except Exception as err:
            print("[-] " + str(err), file=sys.stderr)

if __name__ == "__main__":
    if (len(sys.argv) < 3):
        usage()
    else:
        if (sys.argv[2].lower() == "on" or sys.argv[2].lower() == "off"):
            query = sys.argv[1]
            search(query, sys.argv[2].lower())
        else:
            usage()
