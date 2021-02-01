import requests,time,random,csv,json,re,traceback
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

fake_ua = UserAgent()
headers = {
    'User-Agent': fake_ua.random,
    'cookie': '__cfduid=d5c82b411f95a76705c2a567b3ff195b51600223977; I2KBRCK=1; SERVER=WZ6myaEXBLEFIVkvFByAkw==; MAID=hzKUaBXRVAeUcHsp+kjSVg==; MACHINE_LAST_SEEN=2020-09-15T19%3A39%3A37.748-07%3A00; JSESSIONID=aaakNa24FS9zLcPbReusx; AMCVS_1B6E34B85282A0AC0A490D44%40AdobeOrg=1; _sdsat_MCID=51962543759387168032561036465097876736; randomizeUser=0.15535768675624095; AMCV_1B6E34B85282A0AC0A490D44%40AdobeOrg=-1303530583%7CMCIDTS%7C18522%7CMCMID%7C51962543759387168032561036465097876736%7CMCAAMLH-1600828780%7C11%7CMCAAMB-1600828780%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1600231180s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C3.3.0; s_cc=true; _ga=GA1.2.1744520988.1600223981; _gid=GA1.2.1936407291.1600223981; __gads=ID=e94c1636b908eed3:T=1600223981:S=ALNI_MZLGcZapY4_OvjqQ092tzmRYHSeOA; s_sq=%5B%5BB%5D%5D; _gat_wolga=1'
}

def read_file():   #读取文件
    spinger_mode = r'https?://.*?/.*?/.*?/?.*?/?(\d+)/?.*'
    spinger_urls = []
    with open('./springer_url.csv','r') as fp:
        for line in fp:
            line = line.strip()
            print(line)    # 删除
            journal_id = regulize_process(spinger_mode,line)
            print(journal_id)   #删除
            url = 'https://link.springer.com/journal/{}/volumes-and-issues'.format(journal_id)
            spinger_urls.append(url)
    return spinger_urls

def regulize_process(mode,str):  # 获取专辑页面
    pattern = re.compile(mode)
    regulize_resp = pattern.match(str).group(1)
    return regulize_resp



def get_volume_urls(spinger_url):  #获取每一个期刊所有专辑的url
    global headers
    resp = requests.get(spinger_url,headers = headers)
    text = resp.text
    soup = BeautifulSoup(text,'lxml')
    volume_urls = ['https://www.springer.com' + volume_url.attrs['href'] for volume_url in soup.find_all('a',class_="u-interface-link u-text-sans-serif u-text-sm") if volume_url.string.find('2020') >= 0]
    return volume_urls


def get_article_url(volume_url):  #获取一个专辑中的所有文章的url
    global headers
    resp = requests.get(volume_url,headers = headers)
    text = resp.text
    soup = BeautifulSoup(text,'lxml')
    article_urls = [article_url.attrs['href'] for article_url in soup.find_all('a',itemprop="url")]



spinger_url = read_file()