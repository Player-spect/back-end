import json
from django.shortcuts import render
from django.conf import settings

def inventario(request):
    ruta = settings.BASE_DIR / 'datos_bodega.json'
    with open(ruta, 'r', encoding='utf-8') as f:
        datos = json.load(f)
    return render(request, 'inventario.html', {'datos': datos})

def reportes(request):
    ruta = settings.BASE_DIR / 'datos_bodega.json'
    with open(ruta, 'r', encoding='utf-8') as f:
        datos = json.load(f)

    total_items = len(datos['inventario'])
    criticos = 0
    for item in datos['inventario']:
        if item['estado'] == 'CRÍTICO' or item['estado'] == 'BAJO':
            criticos += 1

    return render(request, 'reportes.html', {
        'datos': datos,
        'total_items': total_items,
        'criticos': criticos
    })