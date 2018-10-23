import time
import datetime
import pytz
import os
import threading
import bottle
from bottle import route, run, template
from splinter import Browser
from bs4 import BeautifulSoup

app = bottle.default_app()
protocolos = []
tz = pytz.timezone('America/Sao_Paulo')
atualizado = datetime.datetime.now(tz=tz).strftime('%d/%m/%Y %H:%M')

def get_pendentes():
    global protocolos
    global atualizado
    
    while True:
        browser = Browser('chrome', headless = True)
        browser.visit(os.environ.get('URL_LOGIN'))
        browser.fill('username', os.environ.get('USERNAME'))
        browser.fill('password', os.environ.get('PASSWORD'))
        browser.find_by_name('login_copista').click()
        browser.visit(os.environ.get('URL_PENDENTES'))
 
        if 'Nenhum protocolo encontrado.' not in browser.html:
            soup = BeautifulSoup(browser.html, 'html.parser')
            plots = soup.find_all('div', attrs={'class': 'titulo'})

            temp = []
            for i, plot in enumerate(plots):
                if i > 0:
                    plot = str(plot.text.strip())
                    data = datetime.datetime.strptime(plot[:16].strip(), '%d/%m/%Y %H:%M').strftime('%d/%m/%Y %H:%M')
                    protocolo = plot[21:31]
                    arquivo = plot[36:46].upper()
                    plotagem = {'data': data, 'protocolo':protocolo, 'arquivo':arquivo}
                    temp.append(plotagem)
                    
        browser.quit()
        protocolos = temp 
        atualizado = datetime.datetime.now(tz=tz).strftime('%d/%m/%Y %H:%M')
        time.sleep(120)

t = threading.Thread(target=get_pendentes)
t.daemon = True
t.start()

@route('/', 'GET')
def pendentes():
    global protocolos
    global atualizado
    return template('t', protocolos=protocolos, atualizado=atualizado)

run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
