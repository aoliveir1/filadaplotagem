import time
import datetime
import os
import json
import bottle
from bottle import route, run, SimpleTemplate, template
from splinter import Browser
from bs4 import BeautifulSoup
import threading
import datetime

app = bottle.default_app()

protocolos = []

atualizado = datetime.datetime.now().strftime('%d/%m/%Y %H:%M')

def get_pendentes():
    global protocolos
    global atualizado
    
    while True:
        protocolos.clear()
        
        browser = Browser('chrome', executable_path = 'C:/Plotagem/webdriver/win_7/chromedriver.exe', headless = True)
        browser.visit(URL_LOGIN)
        browser.fill('username', USERNAME)
        browser.fill('password', PASSWORD)
        browser.find_by_name('login_copista').click()
        browser.visit(URL_PENDENTES)

        if 'Nenhum protocolo encontrado.' not in browser.html:
            soup = BeautifulSoup(browser.html, 'html.parser')
            plots = soup.find_all('div', attrs={'class': 'titulo'})

            for i, plot in enumerate(plots):
                if i > 0:
                    plot = str(plot.text.strip())
                    data = datetime.datetime.strptime(plot[:16].strip(), '%d/%m/%Y %H:%M').strftime('%d/%m/%Y %H:%M')
                    protocolo = plot[21:31]
                    arquivo = plot[36:].replace(' - ', '-').replace(' ', '-').replace('(', '').replace(')','').replace('.pdf', '').replace('.', '').replace('?','').replace('ã','a').replace('ó','o')
                    plotagem = {'data': data, 'protocolo':protocolo, 'arquivo':arquivo[:8].upper()}
                    protocolos.append(plotagem)

        atualizado = datetime.datetime.now().strftime('%d/%m/%Y %H:%M')     
        browser.quit()
        time.sleep(20*60)

t = threading.Thread(target=get_pendentes)
t.daemon = True
t.start()

@route('/', 'GET')
def pendentes():
    global protocolos
    global atualizado
    return template('t', protocolos=protocolos, atualizado=atualizado)

run(host='localhost', port=8080)
