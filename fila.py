import time
import datetime
import pytz
import os
import threading
import bottle
from bottle import response, route, run, template
from splinter import Browser
from bs4 import BeautifulSoup

app = bottle.default_app()
temp = []
protocolos = []
tz = pytz.timezone('America/Sao_Paulo')
atualizado = datetime.datetime.now(tz=tz).strftime('%d/%m/%Y %H:%M')

def get_pendentes():
    global protocolos
    global atualizado
    global temp
      
    while True:    
        browser = Browser('chrome', headless = True)
        browser.visit(os.environ.get('URL_LOGIN'))
        browser.fill('username', os.environ.get('USERNAME'))
        browser.fill('password', os.environ.get('PASSWORD'))
        browser.find_by_name('login_copista').click()
        browser.visit(os.environ.get('URL_PENDENTES'))

        temp = []
        if 'Nenhum protocolo encontrado.' not in browser.html:
            soup = BeautifulSoup(browser.html, 'html.parser')
            plots = soup.find_all('div', attrs={'class': 'titulo'})

            for i, plot in enumerate(plots):
                if i > 0:
                    plot = str(plot.text.strip())
                    data = datetime.datetime.strptime(plot[:16].strip(), '%d/%m/%Y %H:%M').strftime('%d/%m/%Y %H:%M')
                    protocolo = plot[21:31]
                    try:
                        #login = plot[36:].rstrip('_')
                        pos = plot[36:].find('_')
                        login = plot[36:36+pos]
                        login = (login[:3]+'..'+login[len(login)-1:]).upper()
                    except:
                        login = 'nao-indentificado'

                    browser.visit(f'https://ucsvirtual.ucs.br/impressoes/plotista/{protocolo}')
                    soup = BeautifulSoup(browser.html, 'html.parser')
                    folha = soup.find_all('table')
                    folha = str(folha)
                    pos = folha.find('Tipo de folha:')                
                    a = folha.find('A', pos)
                    folha = folha[a:a+2]               

                    plotagem = {'data': data, 'protocolo':protocolo, 'login':login, 'folha':folha}                    
                    temp.append(plotagem)                    

        browser.quit()

        protocolos = temp 
        atualizado = datetime.datetime.now(tz=tz).strftime('%d/%m/%Y %H:%M')

        if datetime.datetime.now(tz=tz).hour >= 8 & datetime.datetime.now(tz=tz).hour <= 22:
            time.sleep(60*5)
        if datetime.datetime.now(tz=tz).hour >= 7 & datetime.datetime.now(tz=tz).hour <= 23:
            time.sleep(60*10)
        else:
            time.sleep(60*20)
            

t = threading.Thread(target=get_pendentes)
t.start()

@route('/', 'GET')
def pendentes():
    global protocolos
    global atualizado
    return template('t', protocolos=protocolos, atualizado=atualizado)

run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
