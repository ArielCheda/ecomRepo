from django.shortcuts import render
import requests
import pandas as pd
import os

# Create your views here.

def leer_ecwid(Url, Params):
    try:
        r=requests.get(url=Url, params=Params)
        js=r.json()
        retorno = pd.DataFrame(js)
    except:
        print('No se pudo leer EC Server')
        retorno = None
    return retorno

def entregasPendientes(request):
    storeId='34512951'
    with open(os.path.join(BASE_DIR, 'EcwidToken.txt')) as f:
        token = f.read().strip()
    
    url='https://app.ecwid.com/api/v3/34512951/orders'
    offset=0
    count=0
    total=100
    limit=100
    df=pd.DataFrame()
        
    while offset < total:
        p={'token':token, 'offset':offset, 'limit':limit}
        df1=leer_ecwid(url, p)
        df=pd.concat([df,df1['items']],ignore_index=True)
        count=df1['count'][0]
        offset=df1['offset'][0]
        limit=df1['limit'][0]
        total=df1['total'][0]
        offset+=count
        df.reset_index(drop=True)

    confirmadosStatusListFilter = ['OUT_FOR_DELIVERY', ]
    statusListFilter = ['AWAITING_PROCESSING', 'PROCESSING', 'OUT_FOR_DELIVERY']
    paymentListFilter = ['PAID', ]
    statusList = ['AWAITING_PROCESSING', 'PROCESSING', 'SHIPPED', 'DELIVERED', 'WILL_NOT_DELIVER', 'RETURNED', 'READY_FOR_PICKUP', 'OUT_FOR_DELIVERY']
    estados = ['En Espera', 'En Preparacion', 'Enviado', 'Entregado', 'No se entregara', 'Devuelto', 'Listo para retirar', 'Listo para enviar']    
    paymentList = ['AWAITING_PAYMENT', 'PAID', 'CANCELLED', 'REFUNDED', 'PARTIALLY_REFUNDED', 'INCOMPLETE']
    pago = ['En espera de pago', 'Pagado', 'Cancelado', 'Reembolsado', 'Parcialmente Reembolsado', 'Incompleto'] 
    pedidosConfirmados = []
    pedidosPendientes = []
    for p in range(len(df)):
        pedido = dict(df.iloc[p,0])
        shippingOption = pedido.get('shippingOption')
        fulfillmentStatus = pedido.get('fulfillmentStatus')
        paymentStatus = pedido.get('paymentStatus')
        
        if (shippingOption):
            if shippingOption.get('fulfillmentType') == 'DELIVERY':
                if (fulfillmentStatus in statusListFilter):
                    pedido['fulfillmentStatus']=estados[statusList.index(fulfillmentStatus)]
                    pedido['paymentStatus']=pago[paymentList.index(paymentStatus)]     
                    shippingMethodName = shippingOption.get('shippingMethodName')
                    methodName = shippingMethodName.lower()
                    i = methodName.find('expreso')
                    if i>=0:
                        expreso = methodName[i:]
                        e=expreso.find("-")
                        if e>=0:
                            expreso = expreso[:e]
                        pedido['expreso'] = expreso.upper()
                    if (fulfillmentStatus in confirmadosStatusListFilter) and (paymentStatus in paymentListFilter):
                        pedidosConfirmados.append(pedido)
                    else:
                        pedidosPendientes.append(pedido)

        
    datos={'pedidosConfirmados': pedidosConfirmados, 'pedidosPendientes': pedidosPendientes}
    return render(request, 'entregas/testEntregas.html', datos)

