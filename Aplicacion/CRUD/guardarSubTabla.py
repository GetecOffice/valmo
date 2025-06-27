from django.shortcuts import render, redirect
from django.contrib import messages

# LLAMAR ARCHIVOS LOCALES
from Aplicacion.forms import *
from Aplicacion.models import *
from Aplicacion.views import agregarDatosTecnicos
from datetime import datetime, date
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< GUARDAR FORMULARIO SubTablas >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# --------------------------------------------------------CLIENTES---------------------------------------------------------
def guardarEstatus(request):
    clave = request.POST['clave']
    Descripcion_v = request.POST['descripcion'].upper()

    clave_int = int(clave)
    formatoClave = 'F-{:06d}'.format(clave_int)

    # tecnicos
    Tecnico_v = request.POST['tecnico'].upper()
    NombreTabla_v = 'Estatus'
    IDFilaTabla_v = formatoClave
    AreaRegistro_v = 'Subtabla'
    IDFila_v = clave
    
    existente = tblEstatus.objects.filter(Descripcion=Descripcion_v).exists()
    if existente:
        errorCol = 'error'
        messages.error(request, f'El esatus "{Descripcion_v}" ya ha sido registrado antreriormente')
        columnas = {'clave': clave, 'errorCol':errorCol}
        return render(request, "SubTablas/Estatus/form.html", columnas)
    else:
        tblEstatus.objects.create(
            Clave = formatoClave, Descripcion=Descripcion_v
        )
        agregarDatosTecnicos(request, Tecnico_v, NombreTabla_v, IDFilaTabla_v, AreaRegistro_v, IDFila_v)
        messages.success(request, f'El estatus "{Descripcion_v}" se ha registrado exitosamente')

    if request.method == 'POST':
        if 'salir' in request.POST:
            return redirect('T-Estatus')
        elif 'agregar' in request.POST:
            return redirect('F-Estatus')
    else:
        return redirect('T-Estatus')

def guardarTipoMaterial(request):
    clave = request.POST['clave']
    Descripcion_v = request.POST['descripcion'].upper()

    clave_int = int(clave)
    formatoClave = 'F-{:06d}'.format(clave_int)

    # tecnicos
    Tecnico_v = request.POST['tecnico'].upper()
    NombreTabla_v = 'Tipo Material'
    IDFilaTabla_v = formatoClave
    AreaRegistro_v = 'Subtabla'
    IDFila_v = clave
    
    existente = tblTipoMaterial.objects.filter(Descripcion=Descripcion_v).exists()
    if existente:
        errorCol = 'error'
        messages.error(request, f'El tipo material "{Descripcion_v}" ya ha sido registrado antreriormente')
        columnas = {'clave': clave, 'errorCol':errorCol}
        return render(request, "SubTablas/TipoMaterial/form.html", columnas)
    else:
        tblTipoMaterial.objects.create(
            Clave = formatoClave, Descripcion=Descripcion_v
        )
        agregarDatosTecnicos(request, Tecnico_v, NombreTabla_v, IDFilaTabla_v, AreaRegistro_v, IDFila_v)
        messages.success(request, f'El tipo material "{Descripcion_v}" se ha registrado exitosamente')

    if request.method == 'POST':
        if 'salir' in request.POST:
            return redirect('T-Tipo-Material')
        elif 'agregar' in request.POST:
            return redirect('F-Tipo-Material')
    else:
        return redirect('T-Tipo-Material')

def guardarTipoMovimiento(request):
    clave = request.POST['clave']
    Descripcion_v = request.POST['descripcion'].upper()

    clave_int = int(clave)
    formatoClave = 'F-{:06d}'.format(clave_int)

    # tecnicos
    Tecnico_v = request.POST['tecnico'].upper()
    NombreTabla_v = 'Tipo Movimiento'
    IDFilaTabla_v = formatoClave
    AreaRegistro_v = 'Subtabla'
    IDFila_v = clave
    
    existente = tblTipoMov.objects.filter(Descripcion=Descripcion_v).exists()
    if existente:
        errorCol = 'error'
        messages.error(request, f'El tipo movimiento "{Descripcion_v}" ya ha sido registrado antreriormente')
        columnas = {'clave': clave, 'errorCol':errorCol}
        return render(request, "SubTablas/TipoMovimiento/form.html", columnas)
    else:
        tblTipoMov.objects.create(
            Clave = formatoClave, Descripcion=Descripcion_v
        )
        agregarDatosTecnicos(request, Tecnico_v, NombreTabla_v, IDFilaTabla_v, AreaRegistro_v, IDFila_v)
        messages.success(request, f'El tipo movimiento "{Descripcion_v}" se ha registrado exitosamente')

    if request.method == 'POST':
        if 'salir' in request.POST:
            return redirect('T-Tipo-Movimiento')
        elif 'agregar' in request.POST:
            return redirect('F-Tipo-Movimiento')
    else:
        return redirect('T-Tipo-Movimiento')

def guardarTipoPresentacion(request):
    clave = request.POST['clave']
    descripcion_v = request.POST['descripcion'].upper()
    cantidad_v = request.POST['cantidad']
    unidad_v = request.POST['unidad']
    visible_v = request.POST['visible']

    clave_int = int(clave)
    formatoClave = 'F-{:06d}'.format(clave_int)

    # tecnicos
    Tecnico_v = request.POST['tecnico'].upper()
    NombreTabla_v = 'Tipo Presentación'
    IDFilaTabla_v = formatoClave
    AreaRegistro_v = 'Subtabla'
    IDFila_v = clave
    
    existente = tblTipoPresentacion.objects.filter(Descripcion=descripcion_v).exists()
    if existente:
        errorCol = 'error'
        FUnidades = tblUnidades.objects.all()
        messages.error(request, f'El tipo presentación "{descripcion_v}" ya ha sido registrado antreriormente')
        columnas = {'clave': clave, 'errorCol':errorCol, 'FUnidades':FUnidades}
        return render(request, "SubTablas/TipoPresentacion/form.html", columnas)
    else:
        tblTipoPresentacion.objects.create(
            Clave = formatoClave, Descripcion=descripcion_v, UdeM_id = unidad_v,
            Cantidad = cantidad_v, Visible =visible_v 
        )
        agregarDatosTecnicos(request, Tecnico_v, NombreTabla_v, IDFilaTabla_v, AreaRegistro_v, IDFila_v)
        messages.success(request, f'El tipo presentación "{descripcion_v}" se ha registrado exitosamente')

    if request.method == 'POST':
        if 'salir' in request.POST:
            return redirect('T-Tipo-Presentacion')
        elif 'agregar' in request.POST:
            return redirect('F-Tipo-Presentacion')
    else:
        return redirect('T-Tipo-Presentacion')
        
def guardarUnidadMedida(request):
    clave = request.POST['clave']
    Descripcion_v = request.POST['descripcion'].upper()
    Abreviacion_v = request.POST['abreviacion']
    
    clave_int = int(clave)
    formatoClave = 'F-{:06d}'.format(clave_int)

    # tecnicos
    Tecnico_v = request.POST['tecnico'].upper()
    NombreTabla_v = 'Unidad Medida'
    IDFilaTabla_v = formatoClave
    AreaRegistro_v = 'Subtabla'
    IDFila_v = clave
    
    existente = tblUnidades.objects.filter(Descripcion=Descripcion_v).exists()
    if existente:
        errorCol = 'error'
        messages.error(request, f'La unidad medida "{Descripcion_v}" ya ha sido registrado antreriormente')
        columnas = {'clave': clave, 'errorCol':errorCol}
        return render(request, "SubTablas/UnidadMedida/form.html", columnas)
    else:
        tblUnidades.objects.create(
            Clave = formatoClave, Descripcion = Descripcion_v, Abreviacion = Abreviacion_v
        )
        agregarDatosTecnicos(request, Tecnico_v, NombreTabla_v, IDFilaTabla_v, AreaRegistro_v, IDFila_v)
        messages.success(request, f'La unidad medida "{Descripcion_v}" se ha registrado exitosamente')

    if request.method == 'POST':
        if 'salir' in request.POST:
            return redirect('T-Unidad-Medida')
        elif 'agregar' in request.POST:
            return redirect('F-Unidad-Medida')
    else:
        return redirect('T-Unidad-Medida')