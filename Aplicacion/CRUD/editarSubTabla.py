from django.shortcuts import render
# LLAMAR ARCHIVOS LOCALES
from Aplicacion.forms import *
from Aplicacion.models import *
from Aplicacion.views import grupo_user
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< EDITAR FORMULARIO CATALOGOS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# --------------------------------------------------------CLIENTES---------------------------------------------------------
def editarEstatus(request, ID):
    grupos = grupo_user(request)
    TEEstatus= tblEstatus.objects.get(ID=ID)
    return render(request, "SubTablas/Estatus/edit.html",{'grupos': grupos,'TEEstatus': TEEstatus})

def editarTipoMaterial(request, ID):
    grupos = grupo_user(request)
    TETipoMaterial = tblTipoMaterial.objects.get(ID=ID)
    return render(request, "SubTablas/TipoMaterial/edit.html",{'grupos': grupos,'TETipoMaterial': TETipoMaterial})

def editarTipoMovimiento(request, ID):
    grupos = grupo_user(request)
    TETipoMov = tblTipoMov.objects.get(ID=ID)
    return render(request, "SubTablas/TipoMovimiento/edit.html",{'grupos': grupos,'TETipoMov': TETipoMov})

def editarTipoPresentacion(request, ID):
    grupos = grupo_user(request)
    TETipoPresentacion = tblTipoPresentacion.objects.get(ID=ID)
    unidad = TETipoPresentacion.UdeM.ID
    FiltradoUnidad= tblUnidades.objects.get(ID=unidad)
    FEUnidad = tblUnidades.objects.all().order_by('Descripcion')
    return render(request, "SubTablas/TipoPresentacion/edit.html",{'grupos': grupos,'TETipoPresentacion': TETipoPresentacion,
    'FiltradoUnidad':FiltradoUnidad, 'FEUnidad':FEUnidad})

def editarUnidadMedida(request, ID):
    grupos = grupo_user(request)
    TEUnidadMedida = tblUnidades.objects.get(ID=ID)
    return render(request, "SubTablas/UnidadMedida/edit.html",{'grupos': grupos,'TEUnidadMedida': TEUnidadMedida})

