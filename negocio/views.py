import json
from django.shortcuts import render
from django.conf import settings

def inicio(request):
    return render(request, 'inicio.html')

def catalogo(request):
    ruta = settings.BASE_DIR / 'datos_negocio.json'
    with open(ruta, 'r', encoding='utf-8') as f:
        datos = json.load(f)
    return render(request, 'catalogo.html', {'datos': datos})