from django.shortcuts import render

import pandas as pd
import requests
import json
from datetime import datetime 

# Create your views here.

def uno(request):
	return render(request, 'pedidos/dos.html', {'titulo': 'test del titulo'})
def IntroPage(request):
	return render(request, 'pedidos/IntroPage.html', {'titulo': 'test del titulo'})
def LongList(request):
    storeId='34512951'
    token = "secret_tSfDmS4d1jsqZKYmJXMhRMW1RdcwsE11"
    url='https://app.ecwid.com/api/v3/34512951/orders?'
    p={'limit':20, 'token':token}
    r=requests.get(url,params=p)
    js=r.json()
    df=pd.DataFrame(js)
    listaDePedidos=df['items']
    
    paymentStatusList = ['AWAITING_PAYMENT', 'PAID', 'CANCELLED', 'REFUNDED,PARTIALLY', 'REFUNDED,INCOMPLETE']
    paymentStatusList2= ['A la espera de pago', 'PAGADO', 'CANCELADO', 'DEVOLUCION TOTAL', 'DEVOLUCION PARCIAL', 'INCOMPLETO']
    
    dS = ['Domingo', 'Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado']
    mA = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    for p, pedido in enumerate(listaDePedidos):
        paymentStatus = listaDePedidos[p].get('paymentStatus')
        i = paymentStatusList.index(paymentStatus)
        listaDePedidos[p]['paymentStatus'] = paymentStatusList2[i]
        if pedido['shippingOption'].get('isPickup'):
            f = datetime.strptime(pedido['extraFields'].get('ecwid_order_pickup_time'), '%Y-%m-%d %H:%M:%S %z')
            d=int(f.strftime('%w'))
            mes=int(f.strftime('%m'))-1
            formato = dS[d] + ' %d de ' + mA[mes] + ' a las %H:%M'
            dia = f.strftime(formato)
            listaDePedidos[p]['extraFields']['ecwid_order_pickup_time'] = dia


    datos={'pedidos':listaDePedidos}
    print(listaDePedidos)
    #return render(request, 'pedidos/LongList.html', datos)
    return render(request, 'pedidos/ll.html', datos)