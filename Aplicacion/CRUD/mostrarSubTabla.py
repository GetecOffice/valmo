from django.shortcuts import render
# LLAMAR ARCHIVOS LOCALES
from Aplicacion.forms import *
from Aplicacion.models import *

from Aplicacion.views import servicioActivo, grupo_user

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< TABLAS DE CATALOGOS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# --------------------------------------------------------ESTATUS---------------------------------------------------------
def TablaEstatus(request):
    grupos = grupo_user(request)
    TEstatus = tblEstatus.objects.all()
    ServiciosWeb = servicioActivo()
    return render(request, 'SubTablas/Estatus/index.html',{'grupos': grupos,'ServiciosWeb': ServiciosWeb,
    'TEstatus': TEstatus})

def TablaTipoMaterial(request):
    grupos = grupo_user(request)
    TTipoMaterial = tblTipoMaterial.objects.all()
    ServiciosWeb = servicioActivo()
    return render(request, 'SubTablas/TipoMaterial/index.html',{'grupos': grupos,'ServiciosWeb': ServiciosWeb,
    'TTipoMaterial': TTipoMaterial})

def TablaTipoMovimiento(request):
    grupos = grupo_user(request)
    TTipoMovimiento = tblTipoMov.objects.all()
    ServiciosWeb = servicioActivo()
    return render(request, 'SubTablas/TipoMovimiento/index.html',{'grupos': grupos,'ServiciosWeb': ServiciosWeb,
    'TTipoMovimiento': TTipoMovimiento})

def TablaTipoPresentacion(request):
    grupos = grupo_user(request)
    TTipoPresentacion = tblTipoPresentacion.objects.values('ID','Clave','Descripcion','Cantidad',
    'UdeM_id__Descripcion', 'Visible')
    ServiciosWeb = servicioActivo()
    return render(request, 'SubTablas/TipoPresentacion/index.html',{'grupos': grupos,'ServiciosWeb': ServiciosWeb,
    'TTipoPresentacion': TTipoPresentacion})

def TablaUnidadMedida(request):
    grupos = grupo_user(request)
    TUnidadMedida = tblUnidades.objects.all()
    ServiciosWeb = servicioActivo()
    return render(request, 'SubTablas/UnidadMedida/index.html',{'grupos': grupos,'ServiciosWeb': ServiciosWeb,
    'TUnidadMedida': TUnidadMedida})

def TablaConfiguracion(request):
    grupos = grupo_user(request)
    TConfiguracion = tblConfiguracion.objects.all()
    ServiciosWeb = servicioActivo()
    return render(request, 'Configuracion/BaseDeDatos/index.html',{'grupos': grupos,'ServiciosWeb': ServiciosWeb,
    'TConfiguracion': TConfiguracion})