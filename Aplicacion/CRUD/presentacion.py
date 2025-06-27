from django.shortcuts import render
# LLAMAR ARCHIVOS LOCALES
from Aplicacion.forms import *
from Aplicacion.models import *
from django.db.models import Sum
from Aplicacion.views import servicioActivo,grupo_user
from django.db.models import Q
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< TABLAS DE CATALOGOS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# --------------------------------------------------------CLIENTES---------------------------------------------------------

def presentacionBascula(request):
    grupos = grupo_user(request)
    ServiciosWeb = servicioActivo()
    return render(request, 'Presentacion/basculas.html',{'grupos': grupos,'ServiciosWeb': ServiciosWeb})    

def presentacionInventario(request):
    grupos = grupo_user(request)
    ServiciosWeb = servicioActivo()
    return render(request, 'Presentacion/inventario.html',{'grupos': grupos,'ServiciosWeb': ServiciosWeb})    

def presentacionServidos(request):
    grupos = grupo_user(request)
    ServiciosWeb = servicioActivo()
    
    PServidosRegistros = tblServido.objects.all()
    registros = PServidosRegistros.count()
    
    PServidosPendientes = tblServido.objects.filter(Q(IDEstatus_id = 3) | Q(IDEstatus_id=9)).all()
    pendientes = PServidosPendientes.count()

    PServidosManual = tblServido.objects.filter(IDEstatus_id = 7).all()
    manuales = PServidosManual.count()

    PServidosConsolidacion = tblServido.objects.filter(IDEstatus_id= 8).all()
    tolva = PServidosConsolidacion.count()
    
    PServidosConsolidacion = tblServido.objects.filter(Q(IDEstatus_id =  10) | Q(IDEstatus_id = 11)).all()
    servidos = PServidosConsolidacion.count()    
 

    return render(request, 'Presentacion/servidos.html',{'grupos': grupos,'ServiciosWeb': ServiciosWeb, 'manuales':manuales, 
                                            'registros':registros, 'pendientes':pendientes, 'servidos':servidos, 'tolva':tolva})
