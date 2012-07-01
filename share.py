# coding:utf-8

import feedparser
import random
import urllib
from urllib2 import urlopen
import subprocess


def encurtar_link(link):
    url_encurtador = 'http://is.gd/create.php?'
    params = dict(format='simple', url=link)
    q = urllib.urlencode(params)
    pagina = urlopen(url_encurtador + q)
    for i in pagina:
        link_encurtado = i
    return link_encurtado


def listar_tags(tags):
    QUANT = 4

    l = []
    for tag in tags:
        if tag.term != 'slide':
            l.append('#%s' % tag.term.replace(' ', ''))
    selecao = []
    numero_tags = len(l)

    if numero_tags < QUANT:
        for t in range(numero_tags):
            selecao.append(l[t])
    else:
        for t in range(QUANT):
            selecao.append(l[t])

    lista = ' '.join(selecao)
    return lista


def contar_caracteres(twitt):
    qtd_caracteres = len(twitt)
    return qtd_caracteres


def sortear_post(entradas):
    post = random.choice(entradas)
    link_encurtado = encurtar_link(post['link'])
    lista_tags = listar_tags(post['tags'])
    post['link_encurtado'] = link_encurtado
    post['tags'] = lista_tags
    return post


def gerar_mensagem(entradas):
    post = sortear_post(entradas)
    twitt = '#releia %(titulo)s => %(link_encurtado)s %(tags)s' % post
    qtd_caracteres = contar_caracteres(twitt)

    while qtd_caracteres > 140:
        print 'maior que 140 caracteres'
        gerar_mensagem(entradas)

    return (twitt)


def twittar(twitt):
    comando_twitt = './twitter-bot.sh "%s"' % twitt
    subprocess.call(comando_twitt, shell=True)
    return

# coloque o endereço do Feed/RSS (ex. http://tech4noobs.agenciax4.com.br/feed)
url_feed = ''
feed = feedparser.parse(url_feed)
entradas = [{'titulo':i.title, 'link': i.link, 'tags': i.tags} for i in feed['entries']]
mensagem = gerar_mensagem(entradas)
twittar(mensagem)
