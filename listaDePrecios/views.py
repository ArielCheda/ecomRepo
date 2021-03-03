from django.shortcuts import render
import pandas as pd
import requests
import json
from datetime import datetime 
import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

# Create your views here.

def leer_ecwid(Url, Params):
    try:
        r=requests.get(url=Url, params=Params)
        js=r.json()
        retorno = pd.DataFrame(js)
    except:
        print('No se pudo leer ECWID, ', r )
        retorno = None
    return retorno

def makePriceList(request):
    storeId='34512951'
    token = "secret_Yf46Vv9LArAPrF9BJUG7TEBJHknsmUz8"
    url='https://app.ecwid.com/api/v3/34512951/categories'
    categoryPriceListRoot = 70591335
    offset=0
    count=0
    total=100
    limit=100
    df=pd.DataFrame()
    while offset < total:
        p={'token':token, 'offset':offset, 'limit':limit, 'parent':categoryPriceListRoot , 'hidden_categories':1, 'productIds':1}
        df1=leer_ecwid(url, p)
        df=pd.concat([df,df1['items']],ignore_index=True)
        count=df1['count'][0]
        offset=df1['offset'][0]
        limit=df1['limit'][0]
        total=df1['total'][0]
        offset+=count
        df.reset_index(drop=True)

    categorias = []
    for c in range(len(df)):
        categoria = dict(df.iloc[c,0])
        
        if categoria.get('parentId') == categoryPriceListRoot: 
            categoryId = categoria.get('id')
            categoryDescription = categoria.get('description')
            if '[mix]' in categoryDescription:
                categoria['formato'] = 'formatoMultiple.html'
            elif '[sinFoto]' in categoryDescription:
                categoria['formato'] = 'formatoSinFoto.html'
            else:
                categoria['formato'] = 'formatoUnico.html'
            productIds = categoria.get('productIds')
            url='https://app.ecwid.com/api/v3/34512951/products'
            p={'category':categoryId, 'sortBy':'DEFINED_BY_STORE_OWNER', 'token':token}
            df2=leer_ecwid(url, p)
            df3=df2['items']
            productos = df3
            categoria['productos'] = productos
            categorias.append(categoria)
            
    datos={'categorias': categorias}
    return render(request, 'listaDePrecios/generarListaDePrecios.html', datos)
    


def link_callback1(uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        result = finders.find(uri)
        print (result)
        if result:
                if not isinstance(result, (list, tuple)):
                        result = [result]
                result = list(os.path.realpath(path) for path in result)
                path=result[0]
        else:
                sUrl = settings.STATIC_URL        # Typically /static/
                sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
                mUrl = settings.MEDIA_URL         # Typically /media/
                mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

                print ('sUrl: ', sUrl)
                print ('sRoot: ', sRoot)
                print ('mUrl: ', mUrl)
                print ('mRoot: ', mRoot)
                if uri.startswith(mUrl):
                        path = os.path.join(mRoot, uri.replace(mUrl, ""))
                elif uri.startswith(sUrl):
                        path = os.path.join(sRoot, uri.replace(sUrl, ""))
                else:
                        return uri

        # make sure that file exists
        if not os.path.isfile(path):
                raise Exception(
                        'media URI must start with %s or %s' % (sUrl, mUrl)
                )
        return path

def renderPDF1(request):
    storeId='34512951'
    token = "secret_tSfDmS4d1jsqZKYmJXMhRMW1RdcwsE11"
    url='https://app.ecwid.com/api/v3/34512951/categories'
    categoryPriceListRoot = 70591335
    offset=0
    count=0
    total=100
    limit=100
    df=pd.DataFrame()
    while offset < total:
        p={'token':token, 'offset':offset, 'limit':limit, 'parent':categoryPriceListRoot , 'hidden_categories':1, 'productIds':1}
        df1=leer_ecwid(url, p)
        df=pd.concat([df,df1['items']],ignore_index=True)
        count=df1['count'][0]
        offset=df1['offset'][0]
        limit=df1['limit'][0]
        total=df1['total'][0]
        offset+=count
        df.reset_index(drop=True)

    categorias = []
    for c in range(len(df)):
        categoria = dict(df.iloc[c,0])
        
        if categoria.get('parentId') == categoryPriceListRoot: 
            categoryId = categoria.get('id')
            categoryDescription = categoria.get('description')
            if '[mix]' in categoryDescription:
                categoria['formato'] = 'formatoMultiple.html'
            elif '[sinFoto]' in categoryDescription:
                categoria['formato'] = 'formatoSinFoto.html'
            else:
                categoria['formato'] = 'formatoUnico.html'
            productIds = categoria.get('productIds')
            url='https://app.ecwid.com/api/v3/34512951/products'
            p={'category':categoryId, 'sortBy':'DEFINED_BY_STORE_OWNER', 'token':token}
            df2=leer_ecwid(url, p)
            df3=df2['items']
            productos = df3
            categoria['productos'] = productos
            categorias.append(categoria)
            
    datos={'categorias': categorias}
    template_path = 'listaDePrecios/generarListaDePrecios.html'
    response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'filename="report.pdf"'
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    template = get_template(template_path)
    html = template.render(datos)
    #pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

