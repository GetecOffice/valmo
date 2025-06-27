from django.shortcuts import render
from django.db.models import Q
from datetime import datetime
from django.utils import timezone
# LLAMAR ARCHIVOS LOCALES
from Aplicacion.forms import *
from Aplicacion.models import *

from Aplicacion.views import servicioActivo, estadoPago, registrarPago, grupo_user

from django.http import JsonResponse
from django.shortcuts import get_object_or_404

timezone.activate("America/Hermosillo")
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< FORMUALRIO DE CATALOGOS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# --------------------------------------------------------CLIENTES---------------------------------------------------------
def FormualrioClientes(request):
    grupos = grupo_user(request)
    ultimo_id = tblClientes.objects.order_by('-ID').first()
    if ultimo_id:
        ultimo_folio = ultimo_id.ID + 1
    else:
        ultimo_folio = 1
    ServiciosWeb = servicioActivo()
    return render(request, 'Catalogos/Cliente/form.html',{'grupos': grupos,'ServiciosWeb': ServiciosWeb,
    'ultimo_folio': ultimo_folio})

def FormualrioProveedores(request):
    grupos = grupo_user(request)
    ultimo_id = tblProveedores.objects.order_by('-ID').first()
    if ultimo_id:
        ultimo_folio = ultimo_id.ID + 1
    else:
        ultimo_folio = 1
    ServiciosWeb = servicioActivo()
    return render(request, 'Catalogos/Proveedor/form.html',{'grupos': grupos,'ServiciosWeb': ServiciosWeb,
    'ultimo_folio': ultimo_folio})

def FormualrioOperadores(request):
    grupos = grupo_user(request)
    ultimo_id = tblOperadores.objects.order_by('-ID').first()
    if ultimo_id:
        ultimo_folio = ultimo_id.ID + 1
    else:
        ultimo_folio = 1
    ServiciosWeb = servicioActivo()
    FEstatus = tblEstatus.objects.filter(ID__lte=2).order_by('Descripcion')
    return render(request, 'Catalogos/Operador/form.html',{'grupos': grupos,'ServiciosWeb': ServiciosWeb,
    'FEstatus': FEstatus,'ultimo_folio': ultimo_folio})

def FormualrioMateriasPrimas(request):
    grupos = grupo_user(request)
    ultimo_id = tblMateriaPrima.objects.order_by('-ID').first()
    if ultimo_id:
        ultimo_folio = ultimo_id.ID + 1
    else:
        ultimo_folio = 1
    ServiciosWeb = servicioActivo()
    FEstatus=tblEstatus.objects.filter(ID__lte=2).order_by('Descripcion')
    FUnidadMedida=tblUnidades.objects.all().order_by('Descripcion')
    return render(request, 'Catalogos/Materia Prima/form.html',{'grupos': grupos,'ServiciosWeb': ServiciosWeb,
    'ultimo_folio': ultimo_folio, 'FEstatus': FEstatus, 'FUnidadMedida': FUnidadMedida})

def FormualrioProductos(request):
    grupos = grupo_user(request)
    ultimo_id = tblProductos.objects.order_by('-ID').first()
    if ultimo_id:
        ultimo_folio = ultimo_id.ID + 1
    else:
        ultimo_folio = 1
    ServiciosWeb = servicioActivo()
    FEstatus=tblEstatus.objects.filter(ID__lte=2).order_by('Descripcion')
    FUnidadMedida=tblUnidades.objects.all().order_by('Descripcion')
    return render(request, 'Catalogos/Producto/form.html',{'grupos': grupos,'ServiciosWeb': ServiciosWeb,
    'ultimo_folio': ultimo_folio, 'FEstatus': FEstatus, 'FUnidadMedida': FUnidadMedida})

def FormualrioCorrales(request):
    grupos = grupo_user(request)
    ultimo_id = tblCorrales.objects.order_by('-ID').first()
    if ultimo_id:
        ultimo_folio = ultimo_id.ID + 1
    else:
        ultimo_folio = 1
    FEstatus = tblEstatus.objects.filter(ID__lte=2).order_by('Descripcion')
    FClientes = tblClientes.objects.all().exclude(ID=1).order_by('Nombre')
    FechaDeHoy = timezone.localtime(timezone.now()).strftime('%Y-%m-%d %H:%M')
    ServiciosWeb = servicioActivo()
    return render(request, 'Catalogos/Corral/form.html',{'grupos': grupos,'ServiciosWeb': ServiciosWeb,
    'ultimo_folio': ultimo_folio, 'FechaDeHoy':FechaDeHoy, 'FClientes': FClientes, 'FEstatus': FEstatus})

def FormualrioTipoAnimaless(request):
    grupos = grupo_user(request)
    ultimo_id = tblAnimalesTipo.objects.order_by('-ID').first()
    if ultimo_id:
        ultimo_folio = ultimo_id.ID + 1
    else:
        ultimo_folio = 1
    ServiciosWeb = servicioActivo()
    FEstatus = tblEstatus.objects.filter(ID__lte=2).order_by('Descripcion')
    return render(request, 'Catalogos/Tipo Animal/form.html',{'grupos': grupos,'ServiciosWeb': ServiciosWeb,
    'ultimo_folio': ultimo_folio,'FEstatus': FEstatus})

def FormualrioContnendoresMateriasPrimas(request):
    grupos = grupo_user(request)
    ultimo_id = tblContenedoresMateriaPrima.objects.order_by('-ID').first()
    if ultimo_id:
        ultimo_folio = ultimo_id.ID + 1
    else:
        ultimo_folio = 1
    ServiciosWeb = servicioActivo()
    FEstatus = tblEstatus.objects.filter(ID__lte=2).order_by('Descripcion')
    FClientes = tblClientes.objects.exclude(ID=1).all().order_by('Nombre')
    return render(request, 'Catalogos/ContenedorMP/form.html',{'grupos': grupos,'ServiciosWeb': ServiciosWeb,
    'ultimo_folio': ultimo_folio, 'FEstatus': FEstatus, 'FClientes': FClientes})

def FormualrioContenedoresProductos(request):
    grupos = grupo_user(request)
    ultimo_id = tblContenedoresProductos.objects.order_by('-ID').first()
    if ultimo_id:
        ultimo_folio = ultimo_id.ID + 1
    else:
        ultimo_folio = 1
    ServiciosWeb = servicioActivo()
    FEstatus = tblEstatus.objects.filter(ID__lte=2).order_by('Descripcion')
    FProveedores = tblProveedores.objects.all().order_by('Nombre')
    return render(request, 'Catalogos/ContenedorProducto/form.html',{'grupos': grupos,'ServiciosWeb': ServiciosWeb, 
    'ultimo_folio': ultimo_folio,'FEstatus':FEstatus,'FProveedores':FProveedores})

def FormualrioTolva(request):
    grupos = grupo_user(request)
    ultimo_id = tblTolva.objects.order_by('-ID').first()
    if ultimo_id:
        ultimo_folio = ultimo_id.ID + 1
    else:
        ultimo_folio = 1
    ServiciosWeb = servicioActivo()
    FUnidadMedida=tblUnidades.objects.all().order_by('Descripcion')
    FEstatus = tblEstatus.objects.filter(ID__gte=4, ID__lte=6).order_by('Descripcion')
    return render(request, 'Catalogos/Tolva/form.html',{'grupos': grupos,'ServiciosWeb': ServiciosWeb,
    'ultimo_folio': ultimo_folio,'FEstatus': FEstatus, 'FUnidadMedida': FUnidadMedida})