from django.shortcuts import render
# LLAMAR ARCHIVOS LOCALES
from Aplicacion.forms import *
from Aplicacion.models import *

from Aplicacion.views import servicioActivo, grupo_user


# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< FORMUALRIO DE CATALOGOS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# --------------------------------------------------------CLIENTES---------------------------------------------------------
def formularioEstatus(request):
    grupos = grupo_user(request)
    ultimo_id = tblEstatus.objects.order_by('-ID').first()
    if ultimo_id:
        ultimo_folio = ultimo_id.ID + 1
    else:
        ultimo_folio = 1
    ServiciosWeb = servicioActivo()
    return render(request, 'SubTablas/Estatus/form.html',{'grupos': grupos,'ServiciosWeb': ServiciosWeb,
    'ultimo_folio': ultimo_folio})

def formularioTipoMaterial(request):
    grupos = grupo_user(request)
    ultimo_id = tblTipoMaterial.objects.order_by('-ID').first()
    if ultimo_id:
        ultimo_folio = ultimo_id.ID + 1
    else:
        ultimo_folio = 1
    ServiciosWeb = servicioActivo()
    return render(request, 'SubTablas/TipoMaterial/form.html',{'grupos': grupos,'ServiciosWeb': ServiciosWeb,
    'ultimo_folio': ultimo_folio})

def formularioTipoMovimiento(request):
    grupos = grupo_user(request)
    ultimo_id = tblTipoMov.objects.order_by('-ID').first()
    if ultimo_id:
        ultimo_folio = ultimo_id.ID + 1
    else:
        ultimo_folio = 1
    ServiciosWeb = servicioActivo()
    return render(request, 'SubTablas/TipoMovimiento/form.html',{'grupos': grupos,'ServiciosWeb': ServiciosWeb,
    'ultimo_folio': ultimo_folio})

def formularioTipoPresentacion(request):
    grupos = grupo_user(request)
    ultimo_id = tblTipoPresentacion.objects.order_by('-ID').first()
    if ultimo_id:
        ultimo_folio = ultimo_id.ID + 1
    else:
        ultimo_folio = 1
    ServiciosWeb = servicioActivo()
    FUnidades = tblUnidades.objects.all()
    return render(request, 'SubTablas/TipoPresentacion/form.html',{'grupos': grupos,'ServiciosWeb': ServiciosWeb,
    'FUnidades':FUnidades, 'ultimo_folio': ultimo_folio})

def formularioUnidadMedida(request):
    grupos = grupo_user(request)
    ultimo_id = tblUnidades.objects.order_by('-ID').first()
    if ultimo_id:
        ultimo_folio = ultimo_id.ID + 1
    else:
        ultimo_folio = 1
    ServiciosWeb = servicioActivo()
    return render(request, 'SubTablas/UnidadMedida/form.html',{'grupos': grupos,'ServiciosWeb': ServiciosWeb,
    'ultimo_folio': ultimo_folio})

