from django.shortcuts import redirect
from django.contrib import messages
# LLAMAR ARCHIVOS LOCALES
from Aplicacion.forms import *
from Aplicacion.models import *
from Aplicacion.views import editarDatosTecnicos
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< ACTUALIZAR DATOS CATALOGOS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# --------------------------------------------------------CLIENTES---------------------------------------------------------
def actualizarEstatus(request):
    id = request.POST['id']
    clave = request.POST['clave']
    descripcion = request.POST['descripcion'].upper().strip()

   # tecnicos
    TecnicoEditor_v = request.POST['tecnico'].upper()
    NombreTabla_v = 'Estatus'
    IDFilaTabla_v = id

    nombre_existente = tblEstatus.objects.filter(Descripcion=descripcion).exclude(ID=id).exists()
    if nombre_existente:
        messages.error(request, f'El Estatus "{descripcion}" ya ha sido registrado anteriormente.')
        IDNumber = int(id)
        return redirect('E-Estatus', IDNumber)
    else:
        estatus = tblEstatus.objects.get(ID=id)
        estatus.Descripcion = descripcion
        estatus.save()
        try:
            editarDatosTecnicos(request, TecnicoEditor_v, NombreTabla_v, IDFilaTabla_v)
        except Exception as e:
            print(e)
        messages.success(request, f'El Estatus "{descripcion}" se ha actualizado exitosamente.')

    return redirect('T-Estatus')

def actualizarTipoMaterial(request):
    id = request.POST['id']
    clave = request.POST['clave']
    descripcion = request.POST['descripcion'].upper().strip()

   # tecnicos
    TecnicoEditor_v = request.POST['tecnico'].upper()
    NombreTabla_v = 'Tipo Material'
    IDFilaTabla_v = id

    nombre_existente = tblTipoMaterial.objects.filter(Descripcion=descripcion).exclude(ID=id).exists()
    if nombre_existente:
        messages.error(request, f'El tipo de material "{descripcion}" ya ha sido registrado anteriormente.')
        IDNumber = int(id)
        return redirect('E-Tipo-Material', IDNumber)
    else:
        TipoMaterial = tblTipoMaterial.objects.get(ID=id)
        TipoMaterial.Descripcion = descripcion
        TipoMaterial.save()
        try:
            editarDatosTecnicos(request, TecnicoEditor_v, NombreTabla_v, IDFilaTabla_v)
        except Exception as e:
            print(e)
        messages.success(request, f'El tipo de material "{descripcion}" se ha actualizado exitosamente.')

    return redirect('T-Tipo-Material')

def actualizarTipoMovmimiento(request):
    id = request.POST['id']
    clave = request.POST['clave']
    descripcion = request.POST['descripcion'].upper().strip()

   # tecnicos
    TecnicoEditor_v = request.POST['tecnico'].upper()
    NombreTabla_v = 'Tipo Movimiento'
    IDFilaTabla_v = id

    nombre_existente = tblTipoMov.objects.filter(Descripcion=descripcion).exclude(ID=id).exists()
    if nombre_existente:
        messages.error(request, f'El tipo de movimiento "{descripcion}" ya ha sido registrado anteriormente.')
        IDNumber = int(id)
        return redirect('E-Tipo-Movimiento', IDNumber)
    else:
        TipoMovimiento = tblTipoMov.objects.get(ID=id)
        TipoMovimiento.Descripcion = descripcion
        TipoMovimiento.save()
        try:
            editarDatosTecnicos(request, TecnicoEditor_v, NombreTabla_v, IDFilaTabla_v)
        except Exception as e:
            print(e)
        messages.success(request, f'El tipo de movimiento "{descripcion}" se ha actualizado exitosamente.')
    return redirect('T-Tipo-Movimiento')

def actualizarTipoPresentacion(request):
    id = request.POST['id']
    clave = request.POST['clave']
    descripcion = request.POST['descripcion'].upper().strip()
    cantidad = request.POST['cantidad']
    visible = request.POST['visible']
    unidad = request.POST['unidad']

   # tecnicos
    TecnicoEditor_v = request.POST['tecnico'].upper()
    NombreTabla_v = 'Tipo Presentación'
    IDFilaTabla_v = id

    nombre_existente = tblTipoPresentacion.objects.filter(Descripcion=descripcion).exclude(ID=id).exists()
    if nombre_existente:
        messages.error(request, f'El tipo de presentación "{descripcion}" ya ha sido registrado anteriormente.')
        IDNumber = int(id)
        return redirect('E-Tipo-Presentacion', IDNumber)
    else:
        TipoPresentacion = tblTipoPresentacion.objects.get(ID=id)
        Unidad_instancia = tblUnidades.objects.get(ID=unidad)
        TipoPresentacion.Descripcion = descripcion
        TipoPresentacion.Cantidad = cantidad
        TipoPresentacion.Visible = visible
        TipoPresentacion.UdeM = Unidad_instancia
        TipoPresentacion.save()
        try:
            editarDatosTecnicos(request, TecnicoEditor_v, NombreTabla_v, IDFilaTabla_v)
        except Exception as e:
            print(e)
        messages.success(request, f'El tipo de presentación "{descripcion}" se ha actualizado exitosamente.')
    return redirect('T-Tipo-Presentacion')

def actualizarUnidadMedida(request):
    id = request.POST['id']
    clave = request.POST['clave']
    descripcion = request.POST['descripcion'].upper().strip()
    abreviacion = request.POST['abreviacion']
   # tecnicos
    TecnicoEditor_v = request.POST['tecnico'].upper()
    NombreTabla_v = 'Unidad Medida'
    IDFilaTabla_v = id

    nombre_existente = tblUnidades.objects.filter(Descripcion=descripcion).exclude(ID=id).exists()
    if nombre_existente:
        messages.error(request, f'La unidad de medida "{descripcion}" ya ha sido registrado anteriormente.')
        IDNumber = int(id)
        return redirect('E-Unidad-Medida', IDNumber)
    else:
        unidades = tblUnidades.objects.get(ID=id)
        unidades.Descripcion = descripcion
        unidades.Abreviacion = abreviacion
        unidades.save()
        try:
            editarDatosTecnicos(request, TecnicoEditor_v, NombreTabla_v, IDFilaTabla_v)
        except Exception as e:
            print(e)
        messages.success(request, f'La unidad de medida "{descripcion}" se ha actualizado exitosamente.')
    return redirect('T-Unidad-Medida')