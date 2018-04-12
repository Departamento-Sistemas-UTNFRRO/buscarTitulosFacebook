# -*- coding: utf-8 -*-

#    This file is part of buscarTitulosFacebook.
#
#    buscarTitulosFacebook is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#
#    buscarTitulosFacebook is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with buscarTitulosFacebook; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import urllib.request
import bs4
import pandas as pd
import os
import csv


def getHtml(url):
    req = urllib.request.Request(url)
    try:
        resp = urllib.request.urlopen(req)
    except Exception as ex:
        print("ERROR" + str(ex))
        return None
    else:
        html = resp.read()
        soup = bs4.BeautifulSoup(html, 'html.parser')
        return soup


def getHtml2(url):

    req = urllib.request.Request(url)
    try:
        resp = urllib.request.urlopen(req)
    except Exception as ex:
        print("ERROR" + str(ex))
        return None
    else:
        html = resp.read()
        return html


def getTituloFacebook(url):
    html = getHtml2(url)
    titulo = ""
    mencionesLista = []
    hashtagsLista = []

    if (html is not None):
        # El html de facebook viene en una etiqueta "code" comentada y se arma dinamico con Javascript
        # para poder interpretarlo, sacamos el comentario y lo pasamos normalmente al parseador
        # Por ejemplo:
        # <div class="hidden_elem"><code id="u_0_q"><!-- <div class="_5pcb _3z-f"> --></code>

        html = html.replace(b'<!--', b'')  # Apertura comentario
        html = html.replace(b'-->', b'')  # Cierre Comentario
        content = bs4.BeautifulSoup(html, 'lxml')
        # devuelve todos los titulos del los post del html, el que busco esta primero
        a = content.find_all('div', {'class': 'mbs _6m6 _2cnj _5s6c'})

        # Si la lista no esta vacia, tengo un titulo
        if a:
            titulo = a[0].getText()

        # Obtengo el bloque del html del post_message del post buscado
        post_message_html = content.find_all('div', {'class': '_5pbx userContent'})

        for tag in post_message_html:
            menciones = tag.find_all('a', {'class': 'profileLink'})
            for mencion in menciones:
                mencionesLista.append(mencion.getText())
            print(mencionesLista)
            hashtags = tag.find_all('span', {'class': '_58cm'})
            for hashtag in hashtags:
                hashtagsLista.append(hashtag.getText())

    # Devuelvo una tupla con los datos del post
    return (titulo, mencionesLista, hashtagsLista)


def loadCsvIntoDataSet(nombreArchivoEntrada):
    csv = pd.read_csv(nombreArchivoEntrada, header=0, sep=',', quotechar='\"', encoding="utf-8")
    return csv.values


def addColumnaTituloFacebook(nombreArchivoEntrada):
    posts = loadCsvIntoDataSet(nombreArchivoEntrada).tolist()

    for i in range(0, len(posts) - 1):
        try:
            # print(posts[i][2])
            url = posts[i][2]
            datosPost = getTituloFacebook(url)
            posts[i].append(datosPost[0])
            posts[i].append(datosPost[1])
            posts[i].append(datosPost[2])
        except Exception as ex:
            print(ex)
            columnas = len(posts[i]) + 1
            for j in range(columnas, 9):
                posts[i].append("Error exception")
    return posts


def saveInCsv(postsFinal, nombreArchivoSalida):
    columns = ['tipo_post', 'post_id', 'post_link', 'link', 'link_domain', 'titulo_facebook', 'menciones_facebook', 'hashtags_facebook']
    df = pd.DataFrame(data=postsFinal, columns=columns)
    df.to_csv(nombreArchivoSalida, index=False, columns=columns, sep=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)


# programaPrincipal
nombreArchivoEntrada = os.path.join(os.path.dirname(__file__), 'data', 'post_input.csv')
nombreArchivoSalida = os.path.join(os.path.dirname(__file__), 'data', 'post_output.csv')
postsConTitulo = addColumnaTituloFacebook(nombreArchivoEntrada)
saveInCsv(postsConTitulo, nombreArchivoSalida)
