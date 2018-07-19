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

from pyfbutils.DataSetCSV import DataSetCSV
from pyfbutils.PostFacebook import PostFacebook


def agregarInfoPostFacebook(datasetCSV):
    posts = datasetCSV.dataset

    for i in range(datasetCSV.inicio, datasetCSV.fin):
        try:
            print(i)
            url = posts[i][1]
            postFacebook = PostFacebook(url)
            datosPost = postFacebook.getInfoPostFacebook()
            posts[i].append(datosPost[0])
            posts[i].append(datosPost[1])
            posts[i].append(datosPost[2])
            posts[i].append(datosPost[3])
        except Exception as ex:
            print(ex)
            columnas = len(posts[i]) + 1
            for j in range(columnas, datasetCSV.cantidadColumnas):
                posts[i].append("Error exception")


# programaPrincipal
nombreArchivoEntrada = 'post_input.csv'
nombreArchivoSalida = 'post_output.csv'
columnas = ['post_id', 'post_link', 'titulo_facebook', 'subtitulo_facebook', 'menciones_facebook', 'hashtags_facebook']

inicio = 0
fin = None

datasetCSV = DataSetCSV(nombreArchivoEntrada, nombreArchivoSalida, columnas, inicio, fin)
agregarInfoPostFacebook(datasetCSV)
datasetCSV.guardar()
