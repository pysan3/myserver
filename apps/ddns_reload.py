from time import sleep
import schedule
import requests

def ddns_reload():
    user_dn = 'pysan-myserver'
    user_pw = 'Takuto1101'
    url = f'http://free.ddo.jp/dnsupdate.php?dn={user_dn}.ddo.jp&pw={user_pw}'
    requests.get(url)

schedule.every().monday.at('15:30').do(ddns_reload)
while True:
    schedule.run_pending()
    sleep(100)