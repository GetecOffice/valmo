from django.shortcuts import redirect
from django.contrib import messages
from datetime import datetime, timedelta
from django.utils import timezone
# LLAMAR ARCHIVOS LOCALES
from Aplicacion.forms import *
from Aplicacion.models import *
from Aplicacion.views import editarDatosTecnicos
from django.db.models import Sum
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< ACTUALIZAR DATOS PROCESOS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# --------------------------------------------------SERVIDOS MANUALES---------------------------------------------------------
def actualizarEntradaMateriaPrima(request):
    tipoMov_v = request.POST['tipoMov']
    if tipoMov_v == '1':
        id_v = request.POST['id']
        folio_v = request.POST['folio']
        proveedor_v = request.POST['proveedor']
        almacen_v = request.POST['almacen']
        presentacion_v = request.POST['presentacion']
        materiaPrima_v = request.POST['materiaPrima']
        cantidad_v = request.POST['cantidad']
        referencia_v = request.POST['referencia']
        fecha_v = request.POST['fecha']
        notas_v = request.POST['notas']

        # tecnicos
        TecnicoEditor_v = request.POST['tecnico'].upper()
        NombreTabla_v = 'Entrada Materias Primas'
        IDFilaTabla_v = id_v
        if referencia_v == '':
            referencia_v = 0
        EntradaMateriaPrimas = tblEntradaMP.objects.get(ID=id_v)
        Presentacion_instancia = tblTipoPresentacion.objects.get(ID=presentacion_v)
        Materia_instancia = tblMateriaPrima.objects.get(ID=materiaPrima_v)
        Proveedor_instancia = tblProveedores.objects.get(ID=proveedor_v)
        almacen_instancia = tblContenedoresMateriaPrima.objects.get(ID=almacen_v)

        EntradaMateriaPrimas.IDProveedor = Proveedor_instancia
        EntradaMateriaPrimas.IDPresentacion = Presentacion_instancia
        EntradaMateriaPrimas.IDMateriaPrima = Materia_instancia
        EntradaMateriaPrimas.IDAlmacen = almacen_instancia
        EntradaMateriaPrimas.cantidad = cantidad_v
        EntradaMateriaPrimas.referencia = referencia_v
        EntradaMateriaPrimas.fecha = fecha_v
        EntradaMateriaPrimas.notas = notas_v
        EntradaMateriaPrimas.save()
        try:
            editarDatosTecnicos(request, TecnicoEditor_v, NombreTabla_v, IDFilaTabla_v)
        except Exception as e:
            print(e)
        messages.success(request, f'La Entrada de Materia Prima "{folio_v}" se ha actualizado exitosamente.')
        return redirect('T-Ent-Materia-Prima')

def actualizarSalidaMateriaPrima(request):
    id_v = request.POST['id']
    folio_v = request.POST['folio']
    cliente_v = request.POST['cliente']
    almacen_v = request.POST['almacen']
    presentacion_v = request.POST['presentacion']
    materiaPrima_v = request.POST['materia']
    cantidad_v = request.POST['cantidad']
    referencia_v = request.POST['referencia']
    fecha_v = request.POST['fecha']
    notas_v = request.POST['notas']

    if referencia_v == '':
        referencia_v = 0
    # tecnicos
    TecnicoEditor_v = request.POST['tecnico'].upper()
    NombreTabla_v = 'Salidas Materias Primas'
    IDFilaTabla_v = id_v

    SalidaMateriaPrimas = tblSalidaMP.objects.get(ID=id_v)
    Presentacion_instancia = tblTipoPresentacion.objects.get(ID=presentacion_v)
    Materia_instancia = tblMateriaPrima.objects.get(ID=materiaPrima_v)
    Cliente_instancia = tblClientes.objects.get(ID=cliente_v)
    Almacen_instancia = tblContenedoresMateriaPrima.objects.get(ID=almacen_v)

    SalidaMateriaPrimas.IDCliente = Cliente_instancia
    SalidaMateriaPrimas.IDPresentacion = Presentacion_instancia
    SalidaMateriaPrimas.IDMateriaPrima = Materia_instancia
    SalidaMateriaPrimas.IDAlmacen = Almacen_instancia
    SalidaMateriaPrimas.cantidad = cantidad_v
    SalidaMateriaPrimas.referencia = referencia_v
    SalidaMateriaPrimas.fecha = fecha_v
    SalidaMateriaPrimas.notas = notas_v
    SalidaMateriaPrimas.save()

    try:
        editarDatosTecnicos(request, TecnicoEditor_v, NombreTabla_v, IDFilaTabla_v)
    except Exception as e:
        print(e)

    messages.success(request, f'La Sálida de Materia Prima "{folio_v}" se ha actualizado exitosamente.')
    return redirect('T-Sal-Materia-Prima')

def actualizarEntradaProductos(request):
    id_v = request.POST['id']
    folio_v = request.POST['folio']
    cliente_v = request.POST['proveedor']
    almacen_v = request.POST['almacen']
    presentacion_v = request.POST['presentacion']
    producto_v = request.POST['producto']
    cantidad_v = request.POST['cantidad']
    referencia_v = request.POST['referencia']
    fecha_v = request.POST['fecha']
    notas_v = request.POST['notas']

    if referencia_v == '':
        referencia_v = 0

    # tecnicos
    TecnicoEditor_v = request.POST['tecnico'].upper()
    NombreTabla_v = 'Entrada Productos'
    IDFilaTabla_v = id_v

    SalidaProductos = tblEntradaProductos.objects.get(ID=id_v)
    Presentacion_instancia = tblTipoPresentacion.objects.get(ID=presentacion_v)
    Producto_instancia = tblProductos.objects.get(ID=producto_v)
    cliente_instancia = tblProveedores.objects.get(ID=cliente_v)
    almacen_instancia = tblContenedoresProductos.objects.get(ID=almacen_v)
    
    SalidaProductos.IDProveedor = cliente_instancia
    SalidaProductos.IDPresentacion = Presentacion_instancia
    SalidaProductos.IDProductos = Producto_instancia
    SalidaProductos.IDAlmacen = almacen_instancia
    SalidaProductos.cantidad = cantidad_v
    SalidaProductos.referencia = referencia_v
    SalidaProductos.fecha = fecha_v
    SalidaProductos.notas = notas_v
    SalidaProductos.save()
    try:
        editarDatosTecnicos(request, TecnicoEditor_v, NombreTabla_v, IDFilaTabla_v)
    except Exception as e:
        print(e)
    messages.success(request, f'La Entrada de productos "{folio_v}" se ha actualizado exitosamente.')
    return redirect('T-Ent-Productos')

def actualizarSalidaProductos(request):
    id_v = request.POST['id']
    folio_v = request.POST['folio']
    cliente_v = request.POST['cliente']
    almacen_v = request.POST['almacen']
    presentacion_v = request.POST['presentacion']
    materiaPrima_v = request.POST['materia']
    cantidad_v = request.POST['cantidad']
    referencia_v = request.POST['referencia']
    fecha_v = request.POST['fecha']
    notas_v = request.POST['notas']

    if referencia_v == '':
        referencia_v = 0

    # tecnicos
    TecnicoEditor_v = request.POST['tecnico'].upper()
    NombreTabla_v = 'Salidas Productos'
    IDFilaTabla_v = id_v

    SalidaProductos = tblSalidaProductos.objects.get(ID=id_v)
    Presentacion_instancia = tblTipoPresentacion.objects.get(ID=presentacion_v)
    Producto_instancia = tblProductos.objects.get(ID=materiaPrima_v)
    cliente_instancia = tblClientes.objects.get(ID=cliente_v)
    almacen_instancia = tblContenedoresProductos.objects.get(ID=almacen_v)
    
    SalidaProductos.IDCliente = cliente_instancia
    SalidaProductos.IDPresentacion = Presentacion_instancia
    SalidaProductos.IDProductos = Producto_instancia
    SalidaProductos.IDAlmacen = almacen_instancia
    SalidaProductos.cantidad = cantidad_v
    SalidaProductos.referencia = referencia_v
    SalidaProductos.fecha = fecha_v
    SalidaProductos.notas = notas_v
    SalidaProductos.save()
    try:
        editarDatosTecnicos(request, TecnicoEditor_v, NombreTabla_v, IDFilaTabla_v)
    except Exception as e:
        print(e)
    messages.success(request, f'La Sálida de productos "{folio_v}" se ha actualizado exitosamente.')
    return redirect('T-Sal-Productos')

def actualizarPeso(peso, folio):
    suma_peso_total = tblDetalleMovAnimales.objects.filter(IDFolio = folio).aggregate(Sum('PesoTotal'))['PesoTotal__sum']
    # print(suma_peso_total)
    guardarPeso = tblMovimientoAnimales.objects.get(Folio = folio)
    guardarPeso.Peso = suma_peso_total
    guardarPeso.save()

def actualizarCantidadAnimales(request):
    id_v = request.POST['id']
    folio_v = request.POST['folio']
    animal_v = request.POST['animal']
    corral_v = request.POST['corral']
    cantidad_v = request.POST['cantidad']
    pesoTotal_v = request.POST['pesoTotal']
    pesoPromedio = round(float(pesoTotal_v) / float(cantidad_v), 2)

    # tecnicos
    TecnicoEditor_v = request.POST['tecnico'].upper()
    NombreTabla_v = 'Cantidad Movimientos Animales'
    IDFilaTabla_v = id_v
    
    cantidadAnimales = tblDetalleMovAnimales.objects.get(ID=id_v)
    animal_instancia = tblAnimalesTipo.objects.get(ID=animal_v)
    corral_instancia = tblCorrales.objects.get(ID=corral_v)
   
    cantidadAnimales.IDAnimales = animal_instancia
    cantidadAnimales.IDCorral = corral_instancia
    cantidadAnimales.Cantidad = cantidad_v
    cantidadAnimales.PesoPromedio = pesoPromedio
    cantidadAnimales.PesoTotal = pesoTotal_v
    cantidadAnimales.save()

    actualizarPeso(pesoTotal_v, folio_v)

    try:
        editarDatosTecnicos(request, TecnicoEditor_v, NombreTabla_v, IDFilaTabla_v)
    except Exception as e:
        print(e)
    messages.success(request, f'La cantiad de animales "{folio_v}" se ha actualizado exitosamente.')

    return redirect('D-MovAnimales', ID=folio_v)

def actualizarMovimientosAniamales(request):
    id_v = request.POST['id']
    cliente_v = request.POST['cliente']
    fecha_v = request.POST['fecha']


    # tecnicos
    TecnicoEditor_v = request.POST['tecnico'].upper()
    NombreTabla_v = 'Movimientos Animales'
    IDFilaTabla_v = id_v

    movimiento_animales_save = tblMovimientoAnimales.objects.get(ID=id_v)
    Cliente_instancia = tblClientes.objects.get(ID=cliente_v)

    movimiento_animales_save.IDCliente = Cliente_instancia
    movimiento_animales_save.Fecha = fecha_v
    movimiento_animales_save.save()
    try:
        editarDatosTecnicos(request, TecnicoEditor_v, NombreTabla_v, IDFilaTabla_v)
    except Exception as e:
        print(e)
        
    messages.success(request, f'El Movimiento de animales se ha actualizado exitosamente.')
    return redirect('T-MovAnimales')

#   QUEDA INHABILITADO TEMPORALMENTE
def actualizarServidosManual(request):
    id_v = request.POST['id']
    folio_v = request.POST['folio']
    cliente_v = request.POST['cliente']
    corral_v = request.POST['corral']
    producto_v = request.POST['producto']
    estatus_v = request.POST['estatus']
    prioridad_v = request.POST['prioridad']
    cantidadSol_v = request.POST['cantidadSol']
    cantidadSer_v = request.POST['cantidadSer']
    fechaSol_v = request.POST['fechaSol']
    fechaSer_v = request.POST['fechaSer']
    servidos = request.POST['servido']
    
    # tecnicos
    TecnicoEditor_v = request.POST['tecnico'].upper()
    NombreTabla_v = 'Servidos Manuales'
    IDFilaTabla_v = id_v

    servidos_save = tblServido.objects.get(ID=id_v)
    Cliente_instancia = tblClientes.objects.get(ID=cliente_v)
    Corral_instancia = tblCorrales.objects.get(ID=corral_v)
    Producto_instancia = tblProductos.objects.get(ID=producto_v)
    Estatus_instancia = tblEstatus.objects.get(ID=estatus_v)

    servidos_save.IDCliente = Cliente_instancia
    servidos_save.IDEstatus = Estatus_instancia
    servidos_save.IDProducto = Producto_instancia
    servidos_save.IDCorral = Corral_instancia
    servidos_save.Prioridad = prioridad_v
    servidos_save.CantidadSolicitada = cantidadSol_v
    servidos_save.CantidadServida = cantidadSer_v
    servidos_save.Fecha = fechaSol_v
    servidos_save.FechaServida = fechaSer_v
    servidos_save.save()
    try:
        editarDatosTecnicos(request, TecnicoEditor_v, NombreTabla_v, IDFilaTabla_v)
    except Exception as e:
        print(e)
    messages.success(request, f'El Servido se ha actualizado exitosamente.')
    if servidos == '1':
        return redirect('T-Solicitud-Servidos')
    elif servidos == '2':
        return redirect('T-Servidos')
    else:
        return redirect('T-Servidos')
    
def actualizarCantidadServidosManual(request):
    if request.method == 'POST':
        id_v = request.POST.getlist('id[]')
        cantidadSer_v = request.POST.getlist('cantidadSer[]')
        estatus_v = 10
        FechaDeHoy = timezone.localtime(timezone.now()).strftime('%Y-%m-%d %H:%M')

        estatus_instancia = tblEstatus.objects.get(ID = estatus_v)
        # tecnicos
        TecnicoEditor_v = request.POST['tecnico'].upper()
        NombreTabla_v = 'Servidos Manuales'
        print(cantidadSer_v)
        
        solicitudes = []
        for i in range(len(cantidadSer_v)):
            if cantidadSer_v[i] and float(cantidadSer_v[i]) != 0:
                solicitud = {
                    'id': id_v[i],
                    'cantidadSer': float(cantidadSer_v[i])
                }
                solicitudes.append(solicitud)

        for solicitud in solicitudes:
            IDFilaTabla_v = solicitud['id']
            servidos_save = tblServido.objects.get(ID = solicitud['id'])
            servidos_save.IDEstatus = estatus_instancia
            servidos_save.CantidadServida = solicitud['cantidadSer']
            servidos_save.FechaServida = FechaDeHoy
            servidos_save.save()
            
        try:
            editarDatosTecnicos(request, TecnicoEditor_v, NombreTabla_v, IDFilaTabla_v)
        except Exception as e:
            print(e)
        messages.success(request, f'El Servido se ha actualizado exitosamente.')
        return redirect('T-Servidos')

def actualizarInventatioInicialMateriaPrima(request):
    id_v = request.POST['id']
    folio_v = request.POST['clave']
    almacen_v = request.POST['almacen']
    materia_v = request.POST['materia']
    fecha_v = request.POST['fecha']
    cantidad_v = request.POST['cantidad']
    notas_v = request.POST['notas']

    # tecnicos
    TecnicoEditor_v = request.POST['tecnico'].upper()
    NombreTabla_v = 'Inventario Materia Prima'
    IDFilaTabla_v = id_v

    inventarioMP_save = tblInventarioInicialesMP.objects.get(ID=id_v)
    Almacen_instancia = tblContenedoresMateriaPrima.objects.get(ID=almacen_v)
    Materia_instancia = tblMateriaPrima.objects.get(ID=materia_v)

    inventarioMP_save.IDContenedor = Almacen_instancia
    inventarioMP_save.IDMateriaPrima = Materia_instancia
    inventarioMP_save.Cantidad = cantidad_v
    inventarioMP_save.Fecha = fecha_v
    inventarioMP_save.Notas = notas_v
 
    inventarioMP_save.save()
    try:
        editarDatosTecnicos(request, TecnicoEditor_v, NombreTabla_v, IDFilaTabla_v)
    except Exception as e:
        print(e)
    messages.success(request, f'El inventario inicial de materia prima se ha actualizado exitosamente.')
    return redirect('T-InventarioMP')

def actualizarInventatioInicialProducto(request):
    id_v = request.POST['id']
    folio_v = request.POST['clave']
    almacen_v = request.POST['almacen']
    materia_v = request.POST['materia']
    fecha_v = request.POST['fecha']
    cantidad_v = request.POST['cantidad']
    notas_v = request.POST['notas']

    # tecnicos
    TecnicoEditor_v = request.POST['tecnico'].upper()
    NombreTabla_v = 'Inventario Productos'
    IDFilaTabla_v = id_v

    inventarioMP_save = tblInventarioInicialesMP.objects.get(ID=id_v)
    Almacen_instancia = tblContenedoresMateriaPrima.objects.get(ID=almacen_v)
    Materia_instancia = tblMateriaPrima.objects.get(ID=materia_v)

    inventarioMP_save.IDContenedor = Almacen_instancia
    inventarioMP_save.IDMateriaPrima = Materia_instancia
    inventarioMP_save.Cantidad = cantidad_v
    inventarioMP_save.Fecha = fecha_v
    inventarioMP_save.Notas = notas_v
 
    inventarioMP_save.save()
    try:
        editarDatosTecnicos(request, TecnicoEditor_v, NombreTabla_v, IDFilaTabla_v)
    except Exception as e:
        print(e)
    messages.success(request, f'El inventario inicial de productos se ha actualizado exitosamente.')
    return redirect('T-InventarioMP')

# << OPERADORES DE MATERIAS PRIMAS Y PRODUCTOS >>
def actualizarOperadoresEntradaProducto(request):
    id_v = request.POST['id']
    chofer_v = request.POST['chofer']
    camion_v = request.POST['camion']
    placas_v = request.POST['placas'] 
    costo_v = request.POST['costo']
    flete_v = request.POST['flete']
    maniobra_v = request.POST['maniobra']

    if costo_v == '':
        costo_v = 0.0
    if flete_v == '':
        flete_v = 0.0
    if maniobra_v == '':
        maniobra_v = 0.0

    operadoresBasculas_save = tblOtrosDatosMovMP.objects.get(ID=id_v)
    operadoresBasculas_save.Chofer = chofer_v
    operadoresBasculas_save.Camion = camion_v
    operadoresBasculas_save.Placas = placas_v
    operadoresBasculas_save.Costo = costo_v
    operadoresBasculas_save.Flete = flete_v
    operadoresBasculas_save.Maniobra = maniobra_v
    operadoresBasculas_save.save()

    messages.success(request, f'El Operador se ha actualizado exitosamente.')
    return redirect('T-Ent-Productos')

def actualizarOperadoresSalidaProducto(request):
    id_v = request.POST['id']
    chofer_v = request.POST['chofer']
    camion_v = request.POST['camion']
    placas_v = request.POST['placas'] 

    operadoresBasculas_save = tblOtrosDatosSalXBas.objects.get(ID=id_v)
    operadoresBasculas_save.Chofer = chofer_v
    operadoresBasculas_save.Camion = camion_v
    operadoresBasculas_save.Placas = placas_v

    operadoresBasculas_save.save()
    
    messages.success(request, f'El Operador se ha actualizado exitosamente.')
    return redirect('T-Sal-Productos')

def actualizarOperadoresEntradaMateriasPrimas(request):
    id_v = request.POST['id']
    chofer_v = request.POST['chofer']
    camion_v = request.POST['camion']
    placas_v = request.POST['placas'] 
    costo_v = request.POST['costo']
    flete_v = request.POST['flete']
    maniobra_v = request.POST['maniobra']

    if costo_v == '':
        costo_v = 0.0
    if flete_v == '':
        flete_v = 0.0
    if maniobra_v == '':
        maniobra_v = 0.0

    operadoresBasculas_save = tblOtrosDatosMovMP.objects.get(ID=id_v)
    operadoresBasculas_save.Chofer = chofer_v
    operadoresBasculas_save.Camion = camion_v
    operadoresBasculas_save.Placas = placas_v
    operadoresBasculas_save.Costo = costo_v
    operadoresBasculas_save.Flete = flete_v
    operadoresBasculas_save.Maniobra = maniobra_v
    operadoresBasculas_save.save()

    messages.success(request, f'El Operador se ha actualizado exitosamente.')
    return redirect('T-Ent-Materia-Prima')

def actualizarOperadoresSalidaMateriasPrimas(request):
    id_v = request.POST['id']
    chofer_v = request.POST['chofer']
    camion_v = request.POST['camion']
    placas_v = request.POST['placas'] 

    operadoresBasculas_save = tblOtrosDatosSalXBas.objects.get(ID=id_v)
    operadoresBasculas_save.Chofer = chofer_v
    operadoresBasculas_save.Camion = camion_v
    operadoresBasculas_save.Placas = placas_v

    operadoresBasculas_save.save()

    messages.success(request, f'El Operador se ha actualizado exitosamente.')
    return redirect('T-Sal-Materia-Prima')

def actualizarServidosATolsva(request):
    if request.method == 'POST':
        id_v = request.POST['id']
        tolva_v = request.POST['tolva']
        idproducto_v = request.POST['idproducto']
        EnTolva = 8
        NombreTolva_v = request.POST['NombreTolva']
        seleccionado_v = request.POST.get('seleccionado')  # Utiliza request.POST.get() para obtener el valor del checkbox

        servido = tblServido.objects.get(ID=id_v)

        Tolva_instancia = tblTolva.objects.get(ID=tolva_v)
        Estatus_instancia = tblEstatus.objects.get(ID=EnTolva)
        
        # Verifica si el checkbox está marcado (seleccionado)
        if seleccionado_v == 'on':

            servido.IDEstatus = Estatus_instancia
            servido.IDTolva = Tolva_instancia
            servido.save()
            messages.success(request, f'El Servido se ha asignado correctamente a la tolva "{NombreTolva_v}".')
    return redirect('T-Consolidacion')

def actualizarServidosATolva(request):
    if request.method == 'POST':
        if 'tolva' in request.POST:
            tolva_v = request.POST['tolva']
            if tolva_v != "" or tolva_v != None:
                EnTolva = 8
                EnOperacion = 4
                NombreTolva_v = request.POST['NombreTolva']
                producto_v = request.POST['idproducto']
                
                # Obtén la instancia de la Tolva y el Estatus una sola vez
                Tolva_instancia = tblTolva.objects.get(ID=tolva_v)
                Estatus_instancia = tblEstatus.objects.get(ID=EnTolva)
                Estatus_operacion = tblEstatus.objects.get(ID=EnOperacion)
                Producto_instancia = tblProductos.objects.get(ID=producto_v)

                tolva_save = tblTolva.objects.get(ID=tolva_v)
                tolva_save.IDProducto = Producto_instancia
                tolva_save.IDEstatus = Estatus_operacion
                tolva_save.save()  
                
                # Itera a través de los IDs seleccionados y actualiza los registros correspondientes
                for key, value in request.POST.items():
                    if key.startswith('seleccionado_'):
                        servido_id = key.split('seleccionado_')[1]
                        # Verifica si el checkbox está marcado
                        servido = tblServido.objects.get(ID=servido_id)
                        servido.IDEstatus = Estatus_instancia
                        servido.IDTolva = Tolva_instancia
                        servido.save()

                messages.success(request, f'Se han asignado los Servidos a la tolva "{NombreTolva_v}" correctamente.')
        
    return redirect('FT-Consolidacion')

# ------------------------------------------------------TIPO ANIMALES------------------------------------------------------
def actualizarCancelarTolva(request):
    idTolva = request.POST['id']
    dataInput = request.POST.get('cargamento-tolva', '')
    if dataInput == "Terminado":
        EstatusServido = 7
    elif dataInput == "Cancelado":
        EstatusServido = 3
    else :
        return redirect('T-Cargamento-Tolva')
    EstatusTolva = 6
    ProductoTolva = 1
    servidotolva = 1

    servido_save = tblServido.objects.filter(IDTolva_id=idTolva, IDEstatus_id = 8)
    Estatus_instancia = tblEstatus.objects.get(ID=EstatusServido)
    Estatus_Tolva_instancia = tblEstatus.objects.get(ID=EstatusTolva)
    Producto_instancia = tblProductos.objects.get(ID=ProductoTolva)
    Tolva_instancia = tblTolva.objects.get(ID=servidotolva)

    tolva_save = tblTolva.objects.get(ID=idTolva)
    tolva = tolva_save.Alias

    for servido_instancia in servido_save:
        servido_instancia.IDEstatus = Estatus_instancia
        servido_instancia.IDTolva = Tolva_instancia  
        servido_instancia.save()


    tolva_save.IDEstatus = Estatus_Tolva_instancia
    tolva_save.IDProducto = Producto_instancia
    tolva_save.save()

    messages.success(request, f'La tolva "{tolva}" se ha actualizado exitosamente.')
    return redirect('T-Cargamento-Tolva')
