import requests 

header= {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'accept:': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'

}

def baixar_foto(url):
    r = requests.get(url).content
    with open('foto.jpg', 'wb') as f:
        f.write(r)
        f.close()
    print('ok')

