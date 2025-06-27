from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime, date
from django.utils import timezone
from django.db.models import Sum
from django.db.models import Q
# LLAMAR ARCHIVOS LOCALES
from Aplicacion.forms import *
from Aplicacion.models import *
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from Aplicacion.views import servicioActivo, grupo_user


def obtener_corrales(request, id):
    print(id)
    cliente = get_object_or_404(tblClientes, pk=id)
    corrales = tblCorrales.objects.filter(IDCliente=cliente)
    corrales_data = [{'ID': corral.ID, 'Descripcion': corral.Descripcion} for corral in corrales]
    return JsonResponse({'corrales': corrales_data})

def obtener_corrales_animales_clientes(request, id):
    try:
        corrales = tblCorrales.objects.filter(IDCliente_id=id).order_by('Descripcion')
        corrales_data = [{'ID': corral.ID, 'Descripcion': corral.Descripcion} for corral in corrales]
        return JsonResponse({'corrales': corrales_data})
    except tblCorrales.DoesNotExist:
        return JsonResponse({'error': "El cliente no tiene corral"})

def obtener_clientes(request, id):
    try:
        corral = tblCorrales.objects.get(ID=id)
        id_cliente = corral.IDCliente.ID
        cliente = tblClientes.objects.get(ID=id_cliente)
        cliente_data = {'ID': cliente.ID, 'Nombre': cliente.Nombre}
        print("HOLa")
        return JsonResponse({'clientes': [cliente_data]})
    except tblCorrales.DoesNotExist:
        return JsonResponse({'error': 'El corral con el ID proporcionado no fue encontrado.'})
    except tblClientes.DoesNotExist:
        return JsonResponse({'error': 'El cliente asociado al corral no fue encontrado.'})

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< TABLAS DE PROCESOS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# ----------------------------------------------MOVIMIENTOS ENTRADA ANMIMALES----------------------------------------------
def TablaEntradaMateriasPrimas(request):
    grupos = grupo_user(request)
    TEntradaMateriasPrimas = tblEntradaMP.objects.values( 
        'ID', 'IDFolio', 'IDProveedor_id__Nombre', 'IDAlmacen_id__Cliente',
        'IDMateriaPrima_id__Descripcion', 'IDPresentacion_id__Descripcion', 'IDPresentacion_id',
        'cantidad', 'referencia', 'fecha', 'notas')

    ServiciosWeb = servicioActivo()
    FTransporteMP = tblOtrosDatosMovMP.objects.all()
    return render(request, 'Procesos/EntradasMateriasPrimas/index.html',{'grupos': grupos,'TEntradaMateriasPrimas': TEntradaMateriasPrimas,
    'ServiciosWeb':ServiciosWeb, 'FTransporteMP':FTransporteMP})

def TablaSalidaMateriasPrimas(request):
    grupos = grupo_user(request)
    TSalidaMateriasPrimas = tblSalidaMP.objects.values( 
        'ID', 'IDFolio', 'IDCliente_id__Nombre', 'IDAlmacen_id__Cliente',
        'IDMateriaPrima_id__Descripcion', 'IDPresentacion_id__Descripcion',   'IDPresentacion_id',
        'cantidad', 'referencia', 'fecha', 'notas'
    )

    ServiciosWeb = servicioActivo()
    FTransporte = tblOtrosDatosSalXBas.objects.all()

    return render(request, 'Procesos/SalidasMateriasPrimas/index.html',{'grupos': grupos,
    'TSalidaMateriasPrimas': TSalidaMateriasPrimas,
    'ServiciosWeb':ServiciosWeb, 'FTransporte':FTransporte})

def TablaEntradaProductos(request):
    grupos = grupo_user(request)
    TEntradaProductos = tblEntradaProductos.objects.values( 
        'ID', 'IDFolio', 'IDProveedor_id__Nombre', 'IDAlmacen_id__Proveedor',
        'IDProductos_id__Descripcion', 'IDPresentacion_id__Descripcion', 'IDPresentacion_id',
        'cantidad', 'referencia', 'fecha', 'notas')

    ServiciosWeb = servicioActivo()
    FTransporteMP = tblOtrosDatosMovMP.objects.all()
    return render(request, 'Procesos/EntradaProductos/index.html',{'grupos': grupos,
    'TEntradaProductos': TEntradaProductos, 'ServiciosWeb':ServiciosWeb, 'FTransporteMP':FTransporteMP})

def TablaSalidaProductos(request):
    grupos = grupo_user(request)
    TSalidaProductos = tblSalidaProductos.objects.values(
        'ID', 'IDFolio', 'IDCliente_id__Nombre', 'IDAlmacen_id__Proveedor', 
        'IDProductos_id__Descripcion', 'IDPresentacion_id__Descripcion', 'IDPresentacion_id',
        'cantidad', 'referencia','fecha','notas'
    )

    ServiciosWeb = servicioActivo()
    FTransporte = tblOtrosDatosSalXBas.objects.all()
    return render(request, 'Procesos/SalidasProductos/index.html',{'grupos': grupos,'TSalidaProductos': TSalidaProductos,
    'ServiciosWeb':ServiciosWeb, 'FTransporte':FTransporte})

def TablaOperadoresEntradaProductos(request):
    grupos = grupo_user(request)
    IDFolio = request.POST.get('folio', '')
    tblOperador = tblOtrosDatosMovMP.objects.get(IDMovMP=IDFolio)
    usuario = tblOperador.IDOperador.id
    usuarioOperador= User.objects.get(id=usuario)
    ServiciosWeb = servicioActivo()
    return render(request, "Procesos/EntradaProductos/verOperador.html",{'grupos': grupos,
    'usuarioOperador':usuarioOperador, 'ServiciosWeb':ServiciosWeb, 'tblOperador': tblOperador})

def TablaOperadoresSalidaProductos(request):
    grupos = grupo_user(request)
    IDFolio = request.POST.get('folio', '')
    tblOperador = tblOtrosDatosSalXBas.objects.get(IDSalida=IDFolio)
    usuario = tblOperador.IDOperador.id
    usuarioOperador= User.objects.get(id=usuario)
    ServiciosWeb = servicioActivo()
    return render(request, "Procesos/SalidasProductos/verOperador.html",{'grupos': grupos,
    'usuarioOperador':usuarioOperador, 'ServiciosWeb': ServiciosWeb, 'tblOperador': tblOperador})

def TablaOperadoresEntradaMateriasPrimas(request):
    grupos = grupo_user(request)
    IDFolio = request.POST.get('folio', '')
    tblOperador = tblOtrosDatosMovMP.objects.get(IDMovMP=IDFolio)
    usuario = tblOperador.IDOperador.id
    usuarioOperador= User.objects.get(id=usuario)
    ServiciosWeb = servicioActivo()
    return render(request, "Procesos/EntradasMateriasPrimas/verOperadorMP.html",{'grupos': grupos,
    'usuarioOperador':usuarioOperador, 'ServiciosWeb':ServiciosWeb, 'tblOperador': tblOperador})

def TablaOperadoresSalidasMateriasPrimas(request):
    grupos = grupo_user(request)
    IDFolio = request.POST.get('folio', '')
    tblOperador = tblOtrosDatosSalXBas.objects.get(IDSalida=IDFolio)
    usuario = tblOperador.IDOperador.id
    usuarioOperador= User.objects.get(id=usuario)
    ServiciosWeb = servicioActivo()
    return render(request, "Procesos/SalidasMateriasPrimas/verOperador.html",{'grupos': grupos,
    'usuarioOperador':usuarioOperador, 'ServiciosWeb':ServiciosWeb, 'tblOperador': tblOperador})

def AgregarMovimientoAnimales(request, ID):
    grupos = grupo_user(request)
    AgMovimientos = tblMovimientoAnimales.objects.get(Folio=ID)
    folio = AgMovimientos.Folio
    Cliente = AgMovimientos.IDCliente.ID
    Movimiento = AgMovimientos.IDMovimiento.ID
    FiltradoCliente = tblClientes.objects.get(ID=Cliente)
    FiltradoMovimiento = tblTipoMov.objects.get(ID=Movimiento)
    FiltradoCorrales = tblCorrales.objects.filter(IDCliente=Cliente).order_by('Descripcion')
    FTipoAnimal = tblAnimalesTipo.objects.all()
    Detalle = tblDetalleMovAnimales.objects.filter(IDFolio=folio).values('IDFolio', 'IDAnimales_id__Descripcion', 
    'Cantidad', 'PesoPromedio', 'PesoTotal', 'IDCorral_id__Descripcion', 'No_Guia', 'Notas' )
    ServiciosWeb = servicioActivo()
    return render(request, "Procesos/MovimientosAnimales/agregar.html",{'grupos': grupos,'AgMovimientos': AgMovimientos,
    'FiltradoCliente':FiltradoCliente, 'FiltradoMovimiento':FiltradoMovimiento, 'FiltradoCorral':FiltradoCorrales,
    'ServiciosWeb':ServiciosWeb, 'FTipoAnimal':FTipoAnimal, 'Detalle':Detalle})

def detalleAnimales(request, ID):
    grupos = grupo_user(request)
    AgMovimientos = tblMovimientoAnimales.objects.get(Folio=ID)
    folio = AgMovimientos.Folio
    Detalle = tblDetalleMovAnimales.objects.filter(IDFolio=folio).values('ID', 'IDFolio', 'IDAnimales_id__Descripcion', 'Cantidad',
    'PesoTotal', 'PesoPromedio', 'IDCorral_id__Descripcion', 'No_Guia', 'Notas')
    ServiciosWeb = servicioActivo()
    return render(request, 'Procesos/MovimientosAnimales/verDetalle.html',{'grupos': grupos,'ServiciosWeb': ServiciosWeb,'Detalle': Detalle})

def TablaMovimientoAnimales(request):
    grupos = grupo_user(request)
    Movimiento = request.POST.get('mov', '')
    if Movimiento is not None and Movimiento != '':
        TMovimientoEntradaAnimales = tblMovimientoAnimales.objects.filter(IDMovimiento = Movimiento).values( 'ID',
        'Folio', 'IDCliente_id__Nombre', 'IDMovimiento_id__Descripcion', 
        'Fecha',  'Peso', 'NoPartida'
    )
        if Movimiento == 1 or Movimiento == "1":
            Movimiento = "Entrada"
        else:
            Movimiento = "Sálida"
    else:
         TMovimientoEntradaAnimales = tblMovimientoAnimales.objects.filter(IDMovimiento = 1).values( 'ID',
        'Folio', 'IDCliente_id__Nombre', 'IDMovimiento_id__Descripcion', 'Fecha', 'Peso', 'NoPartida'
    )
         Movimiento  = "Entrada"
    ServiciosWeb = servicioActivo()
    return render(request, 'Procesos/MovimientosAnimales/index.html',{'grupos': grupos, 'Movimiento':Movimiento,
    'ServiciosWeb':ServiciosWeb, 'TMovimientoEntradaAnimales': TMovimientoEntradaAnimales})

# -----------------------------------------------DETALLES ANIMALES----------------------------------------------------
def TablaDetallesAnimales(request):
    grupos = grupo_user(request)
    TDetallesAniamles = tblDetalleAnimales.objects.all()
    ServiciosWeb = servicioActivo()
    return render(request, 'Procesos/DetallesAnimales/index.html',{'grupos': grupos,
    'ServiciosWeb':ServiciosWeb, 'TDetallesAniamles': TDetallesAniamles})

# -------------------------------------------------SERVIDOS ANIMALES---------------------------------------------------
def TablaSolicitudServido(request):
    grupos = grupo_user(request)
    Prioridad = request.POST.get('prioridad', '')
    if Prioridad is not None and Prioridad != '':
        TServidos = tblServido.objects.exclude(IDCliente_id=1).filter(Prioridad = Prioridad, IDEstatus_id = 7).values('ID', 'Folio',
        'IDCliente_id__Nombre', 'IDCorral_id__Descripcion', 'IDProducto_id__Descripcion', 'IDEstatus_id__Descripcion',
        'CantidadSolicitada', 'CantidadServida', 'Prioridad', 'Fecha', 'FechaServida', 'FechaAServir'
    )
    else:
         TServidos = tblServido.objects.exclude(IDCliente_id=1).filter(Q(IDEstatus_id =3) | Q(IDEstatus_id=9)).values('ID', 'Folio',
        'IDCliente_id__Nombre', 'IDCorral_id__Descripcion','IDProducto_id__Descripcion','IDEstatus_id__Descripcion',
        'CantidadSolicitada', 'CantidadServida', 'Prioridad', 'Fecha', 'FechaServida', 'FechaAServir'
    )
    ServiciosWeb = servicioActivo()
    return render(request, 'Procesos/Solicitud Servido/index.html',{'grupos': grupos, 'ServiciosWeb':ServiciosWeb,'TServidos': TServidos })

def TablaServidoCorral(request):
    grupos = grupo_user(request)
    TServidos = tblServido.objects.filter(Q(IDEstatus_id = 10) | Q(IDEstatus_id = 11)).values('ID', 'Folio',
    'IDCliente_id__Nombre', 'IDCorral_id__Descripcion','IDProducto_id__Descripcion','IDEstatus_id__Descripcion',
    'CantidadSolicitada', 'CantidadServida', 'Prioridad', 'Fecha', 'FechaServida', 'FechaAServir'
    )
    ServiciosWeb = servicioActivo()
    return render(request, 'Procesos/ServidosConsolidacion/servido.html',{'grupos': grupos, 'ServiciosWeb':ServiciosWeb,'TServidos': TServidos })

def TablaTolvaServido(request, ID, Estatus, Producto):
    servido = tblServido.objects.get(Folio=ID)
    producto = servido.IDProducto
    estatus = Estatus
    Estatus_instancia = tblEstatus.objects.get(ID=estatus)
    servido.IDEstatus = Estatus_instancia
    servido.save()
    return redirect('FT-Consolidacion', Producto)

def TablaTolvaServidoCorral(request):
    estatusSirve = request.POST.get('estatus', '')
    folio = request.POST.get('folio', '')
    IDProd = request.POST.get('IDProd', '')
    tolva = request.POST.get('tolva', '')
    
    if estatusSirve == 7 or estatusSirve == 3 or estatusSirve == '7' or estatusSirve == '3':
        servido = tblServido.objects.get(Folio=folio)
        producto = servido.IDProducto
        estatus = estatusSirve
        Estatus_instancia = tblEstatus.objects.get(ID=estatus)
        servido.IDEstatus = Estatus_instancia
        servido.save()

        ServiciosWeb = servicioActivo()
        grupos = grupo_user(request)
        TServidos = tblServido.objects.filter(IDEstatus_id = tolva).values('ID', 
        'Folio', 'IDCliente_id__Nombre', 'IDCorral_id__Descripcion', 'IDProducto_id__Descripcion', 
        'IDEstatus_id__Descripcion', 'CantidadSolicitada', 'CantidadServida', 'Prioridad', 'Fecha',
        'FechaServida', 'IDProducto_id', 'IDEstatus_id')
        if tolva == '4':
            tolvas = 'EN TOLVA 1'
        elif tolva == '5':
            tolvas = 'EN TOLVA 2'
        elif tolva == '6':
            tolvas = 'EN TOLVA 3'

        if estatusSirve == '3':
            messages.error(request, f'El producto a sido cancelado')  
        elif estatusSirve == '7':
            messages.success(request, f'El producto  a sido servido en el corral')
        
        
    return render(request, 'Procesos/ServidosConsolidacion/tolva.html',{'grupos': grupos,
        'ServiciosWeb': ServiciosWeb, 'TServidos':TServidos})

def TablaTolva(request):
    tolva = request.POST.get('tolva', '')

    if tolva is not None and tolva != '':
        TServidos = tblServido.objects.exclude(IDCliente_id=1).filter(IDTolva_id = tolva).values('ID', 'Folio',
        'IDCliente_id__Nombre', 'IDCorral_id__Descripcion', 'IDProducto_id__Descripcion', 'IDEstatus_id__Descripcion',
        'CantidadSolicitada', 'CantidadServida', 'Prioridad', 'Fecha', 'FechaServida', 'IDProducto_id', 'IDEstatus_id')
        if tolva == '2':
            tolvas = 'EN TOLVA 1'
        elif tolva == '3':
            tolvas = 'EN TOLVA 2'
        elif tolva == '4':
            tolvas = 'EN TOLVA 3'
    else:
        tolvas = 'NO SE SELECCIONO TOLVA'
        TServidos = tblServido.objects.exclude(IDCliente_id=1).values('ID', 'Folio',
        'IDCliente_id__Nombre', 'IDCorral_id__Descripcion', 'IDProducto_id__Descripcion', 'IDEstatus_id__Descripcion',
        'CantidadSolicitada', 'CantidadServida', 'Prioridad', 'Fecha', 'FechaServida', 'IDProducto_id', 'IDEstatus_id')

    ServiciosWeb = servicioActivo()
    grupos = grupo_user(request)
    return render(request, 'Procesos/ServidosConsolidacion/tolva.html',{'grupos': grupos,
        'ServiciosWeb': ServiciosWeb, 'TServidos':TServidos, 'tolva':tolvas})

def TablaFiltroServido(request):
    grupos = grupo_user(request)
    producto = request.POST.get('producto', '')
    tolva = request.POST.get('tolva', '')
    if producto is not None and producto != '':
        ServiciosWeb = servicioActivo()
        grupos = grupo_user(request)
        FiltroServidos = tblServido.objects.filter(Q(IDProducto_id= producto) & (Q(IDEstatus_id =3) | Q(IDEstatus_id=9))).values('ID', 'Folio',
            'IDCliente_id__Nombre', 'IDCorral_id__Descripcion', 'IDProducto_id__Descripcion',
            'IDEstatus_id__Descripcion', 'CantidadSolicitada', 'CantidadServida', 'Prioridad',
            'Fecha', 'FechaServida','IDProducto_id', 'FechaAServir'
        )
        FiltradoProducto= tblProductos.objects.get(ID=producto)
        unidad_id = FiltradoProducto.IDUnidadMedida.ID
        FiltradoTolva= tblTolva.objects.get(ID=tolva)
        Filtradounidad= tblUnidades.objects.get(ID=unidad_id)
        STolva = tblTolva.objects.exclude(ID = 1).values('ID','IDProducto_id__Descripcion', 'Alias', 'IDProducto_id', 'IDEstatus_id')
        resultados = tblServido.objects.exclude(IDCliente_id=1).filter(Q(IDEstatus_id =3) | Q(IDEstatus_id=9)).values('IDProducto_id__Descripcion','IDProducto_id').annotate(total_cantidad=Sum('CantidadSolicitada')).order_by('IDProducto_id__Descripcion')

        TConsolidacion = []  # Crear una lista vacía para almacenar los resultados

        for resultado in resultados:
            descripcion = resultado['IDProducto_id__Descripcion']
            IDProducto = resultado['IDProducto_id']
            total_cantidad = resultado['total_cantidad']
            TConsolidacion.append({'Producto': descripcion, 'cantidad': total_cantidad, 'IDProducto':IDProducto})  # Agregar cada entrada a la lista
        
        tolva1 = tblServido.objects.filter(IDTolva_id = tolva, IDEstatus_id = 8).values('IDProducto_id__Descripcion').annotate(total_cantidad=Sum('CantidadSolicitada'))
        
        if tolva1.exists():
            print("Resultado existe")
            TTolva1 = []
            for resultado in tolva1:
                descripcion = resultado['IDProducto_id__Descripcion']
                cantidad = resultado['total_cantidad']
                if cantidad is not None and cantidad != 0 and cantidad != '0':
                    total_cantidad = cantidad
                else:
                    total_cantidad = 0
                TTolva1.append({'Producto': descripcion, 'cantidad': total_cantidad})
        else:
            print("Resultado no exite")
            TTolva1 = [{'Producto': 'No se encontraron registros', 'cantidad': 0}]

        productos_tolva1 = tblServido.objects.filter(IDTolva = tolva)
        if productos_tolva1.exists():
            producto_tolva = productos_tolva1.first()
        else:
            producto_tolva = 0

        return render(request, 'Procesos/ServidosConsolidacion/Filtro.html',{'grupos': grupos, 'producto_tolva':producto_tolva,
        'ServiciosWeb': ServiciosWeb, 'FiltroServidos':FiltroServidos, 'STolva':STolva, 'TTolva1':TTolva1, 'Filtradounidad':Filtradounidad, 
        'FiltradoProducto':FiltradoProducto,'FiltradoTolva':FiltradoTolva, 'TConsolidacion': TConsolidacion})
    else:
        FiltradoProducto= tblProductos.objects.filter(ID=1).first()
        FiltradoTolva= tblTolva.objects.filter(ID=2).first()
        STolva = tblTolva.objects.exclude(ID = 1).all()
        FiltroServidos = tblServido.objects.filter(IDProducto_id= 1, IDEstatus_id =3).values('ID', 'Folio',
            'IDCliente_id__Nombre', 'IDCorral_id__Descripcion', 'IDProducto_id__Descripcion', 
            'IDEstatus_id__Descripcion', 'CantidadSolicitada', 'CantidadServida', 'Prioridad',
            'Fecha', 'FechaServida','IDProducto_id', 'FechaAServir' )
    resultados = tblServido.objects.exclude(IDCliente_id=1).filter(Q(IDEstatus_id =3) | Q(IDEstatus_id=9)).values('IDProducto_id__Descripcion','IDProducto_id').annotate(total_cantidad=Sum('CantidadSolicitada')).order_by('IDProducto_id__Descripcion')

    TConsolidacion = []  # Crear una lista vacía para almacenar los resultados

    for resultado in resultados:
        descripcion = resultado['IDProducto_id__Descripcion']
        IDProducto = resultado['IDProducto_id']
        total_cantidad = resultado['total_cantidad']
        TConsolidacion.append({'Producto': descripcion, 'cantidad': total_cantidad, 'IDProducto':IDProducto})  # Agregar cada entrada a la lista
    
    # TRAER LA CANTIDAD DE KILOGRAMOS DE CADA TOLVA Y PRESENTARLO EN EL TEMPLATE
    tolva1 = tblServido.objects.exclude(IDCliente_id=1).filter(IDTolva_id = 2).values('IDProducto_id__Descripcion').annotate(total_cantidad=Sum('CantidadSolicitada'))
    TTolva1 = []
    for resultado in tolva1:
        descripcion = resultado['IDProducto_id__Descripcion']
        total_cantidad = resultado['total_cantidad']
        TTolva1.append({'Producto': descripcion, 'cantidad': total_cantidad})


    ServiciosWeb = servicioActivo()
    return render(request, 'Procesos/ServidosConsolidacion/Filtro.html',{'grupos': grupos,
    'ServiciosWeb': ServiciosWeb, 'FiltroServidos':FiltroServidos, 'TTolva1':TTolva1,  'FiltradoTolva':FiltradoTolva,
    'FiltradoProducto':FiltradoProducto, 'STolva':STolva, 'TConsolidacion': TConsolidacion})

def TablaConsolidacionServido(request):
    grupos = grupo_user(request)

    resultados = tblServido.objects.exclude(IDCliente_id=1).filter(IDEstatus_id =3).values('IDProducto_id__Descripcion','IDProducto_id').annotate(total_cantidad=Sum('CantidadSolicitada'))

    TConsolidacion = []  # Crear una lista vacía para almacenar los resultados

    for resultado in resultados:
        descripcion = resultado['IDProducto_id__Descripcion']
        IDProducto = resultado['IDProducto_id']
        total_cantidad = resultado['total_cantidad']
        TConsolidacion.append({'Producto': descripcion, 'cantidad': total_cantidad, 'IDProducto':IDProducto})  # Agregar cada entrada a la lista
    
    STolva = tblTolva.objects.exclude(ID = 1).all()
    
    # TRAER LA CANTIDAD DE KILOGRAMOS DE CADA TOLVA Y PRESENTARLO EN EL TEMPLATE
    tolva1 = tblServido.objects.exclude(IDCliente_id=1).filter(IDTolva_id =2).values('IDProducto_id__Descripcion').annotate(total_cantidad=Sum('CantidadSolicitada'))
    tolva2 = tblServido.objects.exclude(IDCliente_id=1).filter(IDTolva_id =3).values('IDProducto_id__Descripcion').annotate(total_cantidad=Sum('CantidadSolicitada'))
    tolva3 = tblServido.objects.exclude(IDCliente_id=1).filter(IDTolva_id =4).values('IDProducto_id__Descripcion').annotate(total_cantidad=Sum('CantidadSolicitada'))
    TTolva1 = []
    for resultado in tolva1:
        descripcion = resultado['IDProducto_id__Descripcion']
        total_cantidad = resultado['total_cantidad']
        TTolva1.append({'Producto': descripcion, 'cantidad': total_cantidad})

    TTolva2 = []
    for resultado in tolva2:
        descripcion = resultado['IDProducto_id__Descripcion']
        total_cantidad = resultado['total_cantidad']
        TTolva2.append({'Producto': descripcion, 'cantidad': total_cantidad})

    TTolva3 = []
    for resultado in tolva3:
        descripcion = resultado['IDProducto_id__Descripcion']
        total_cantidad = resultado['total_cantidad']
        TTolva3.append({'Producto': descripcion, 'cantidad': total_cantidad})

    FiltroServidos = tblServido.objects.filter(IDEstatus_id =3).values('ID', 'Folio',
            'IDCliente_id__Nombre', 'IDCorral_id__Descripcion', 'IDProducto_id__Descripcion', 
            'IDEstatus_id__Descripcion', 'CantidadSolicitada', 'CantidadServida', 'Prioridad',
            'Fecha', 'FechaServida','IDProducto_id' )
            
    ServiciosWeb = servicioActivo()
    return render(request, 'Procesos/ServidosConsolidacion/index.html', {'grupos': grupos,
    'TConsolidacion': TConsolidacion, 'ServiciosWeb': ServiciosWeb, 'TTolva1':TTolva1, 
    'TTolva2':TTolva2, 'TTolva3':TTolva3, 'STolva': STolva, 'FiltroServidos':FiltroServidos})

def TablaServidoAnimales(request):
    grupos = grupo_user(request)
    Prioridad = request.POST.get('prioridad', '')
    if Prioridad is not None and Prioridad != '':
        TServidos = tblServido.objects.exclude(IDCliente_id=1).filter(Q(Prioridad = Prioridad) & Q(IDEstatus_id = 7)).values('ID', 'Folio',
        'IDCliente_id__Nombre', 'IDCorral_id__Descripcion', 'IDProducto_id__Descripcion', 'IDEstatus_id__Descripcion', 'IDTolva_id__Alias',
        'CantidadSolicitada', 'CantidadServida', 'Prioridad', 'Fecha', 'FechaServida'
    )
    else:
         TServidos = tblServido.objects.exclude(IDCliente_id=1).filter(IDEstatus_id = 7).values('ID', 'Folio','IDTolva_id__Alias',
        'IDCliente_id__Nombre', 'IDCorral_id__Descripcion','IDProducto_id__Descripcion','IDEstatus_id__Descripcion',
        'CantidadSolicitada', 'CantidadServida', 'Prioridad', 'Fecha', 'FechaServida'
    )
    ServiciosWeb = servicioActivo()
    return render(request, 'Procesos/Servido Manual/index.html',{'grupos': grupos, 'ServiciosWeb':ServiciosWeb,'TServidos': TServidos })

def TablaInventarioMateriaPrima(request):
    grupos = grupo_user(request)
    TInventarioMateriaPrima = tblInventarioInicialesMP.objects.values(
        'ID', 'Folio', 'IDContenedor_id__Cliente', 'IDMateriaPrima_id__Descripcion', 
        'Cantidad', 'Fecha', 'Notas'
    )

    ServiciosWeb = servicioActivo()
    return render(request, 'Procesos/InventarioMateriaPrima/index.html',{'grupos': grupos, 'ServiciosWeb':ServiciosWeb, 'TInventarioMateriaPrima': TInventarioMateriaPrima,
    'ServiciosWeb':ServiciosWeb})

def TablaInventarioProducto(request):
    grupos = grupo_user(request)
    TInventarioProducto = tblInventarioInicialesProductos.objects.values(
        'ID', 'Folio', 'IDContenedor_id__Proveedor', 'IDProducto_id__Descripcion', 
        'Cantidad', 'Fecha', 'Notas'
    )

    ServiciosWeb = servicioActivo()
    return render(request, 'Procesos/InventarioProductos/index.html',{'grupos': grupos, 'ServiciosWeb':ServiciosWeb, 'TInventarioProducto': TInventarioProducto,
    'ServiciosWeb':ServiciosWeb})
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< LIBERAR O ASIGNAR CORRALES >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# ------------------------------------------------------LIBERAR CORRAL------------------------------------------------------
def asignacionCorral(request):
    grupos = grupo_user(request)
    FClientes = tblClientes.objects.exclude(ID = 1).all().order_by('Nombre')
    ServiciosWeb = servicioActivo()
    ClienteID = request.POST.get('cliente', '')
 
    if ClienteID is not None and ClienteID != '':
        Cliente_Select = tblClientes.objects.get(ID=ClienteID)
        clientePost = [{'ClienteID': Cliente_Select.ID, 'Nombre': Cliente_Select.Nombre}]
    else:
        clientePost = [{'ClienteID': ''}]
    
    if ClienteID is not None and ClienteID != '':
        TClienteCorrales = tblCorrales.objects.filter(IDCliente_id = ClienteID).values('ID', 'IDCliente_id', 'IDCliente_id__Nombre', 'Descripcion')
        TCorralesLibres = tblCorrales.objects.filter(IDCliente_id=1).values('ID', 'IDCliente_id', 'Clave','IDCliente_id__Nombre', 'Descripcion', 'IDEstatus_id__Descripcion')
    else:
        TClienteCorrales = tblCorrales.objects.exclude(IDCliente_id=1).values('ID', 'IDCliente_id', 'IDCliente_id__Nombre', 'Descripcion')
        TCorralesLibres = tblCorrales.objects.filter(IDCliente_id=1).values('ID', 'IDCliente_id', 'Clave','IDCliente_id__Nombre', 'Descripcion', 'IDEstatus_id__Descripcion')
    
    # Obtener el último folio
    if tblAsignaCorrales.objects.exists():
        ultimo_folio_str = tblAsignaCorrales.objects.latest('ID').Clave
        ultimo_folio = int(ultimo_folio_str.split('-')[-1])
    else:
        ultimo_folio = 0
            
    asignar = request.POST.get('asignar', '')
    if asignar is not None and asignar != '':
        liberar_seleccionados = request.POST.getlist('ID')
        for id_a_liberar in liberar_seleccionados:
            ultimo_folio += 1
            formatoClave = 'F-{:06d}'.format(ultimo_folio)
            id = id_a_liberar
            corral = request.POST['corral']
            capacidad = 0
            clienteAsigna = request.POST['cliente']
            Fecha =  timezone.localtime(timezone.now()).strftime('%Y-%m-%d %H:%M')
            Clientes_instancia = tblClientes.objects.get(ID=clienteAsigna)
            Nombre = Clientes_instancia.Nombre
            
            corral = tblCorrales.objects.get(ID=id)
            corral.IDCliente = Clientes_instancia
            corral.Capacidad = capacidad
            corral.FechaAsigna = Fecha
            Corral = corral.Descripcion
            corral.save()
            
            TipoMov = 3
            tblAsignaCorrales.objects.create(
                Clave = formatoClave, IDCorral_id = id, IDCliente_id = clienteAsigna, Fecha = Fecha, TipoMov_id = TipoMov
            )    
        messages.success(request, f'El Corral "{Corral}" ha sido asignado al cliente "{Nombre}" correctamente')
        return render(request, 'Procesos/AsignarCorrales/index.html',{'grupos': grupos,
        'ServiciosWeb':ServiciosWeb, 'TClienteCorrales': TClienteCorrales, 'TCorralesLibres':TCorralesLibres,
        'FClientes':FClientes, 'clientePost': clientePost})
    

    liberar = request.POST.get('liberar', '')
    if liberar is not None and liberar != '':
        liberar_seleccionados = request.POST.getlist('ID')
        for id_a_liberar in liberar_seleccionados:
            ultimo_folio += 1
            formatoClave = 'F-{:06d}'.format(ultimo_folio)
            id = id_a_liberar
            clienteCero = 1
            clienteAsigna = request.POST['cliente']
            corral = request.POST['corral']
            capacidad = request.POST['capacidad']
            Fecha =  timezone.localtime(timezone.now()).strftime('%Y-%m-%d %H:%M')
            Clientes_Cero = tblClientes.objects.get(ID=clienteCero)
            
            Clientes_instancia = tblClientes.objects.get(ID=clienteAsigna)
            Nombre = Clientes_instancia.Nombre
    
            corral = tblCorrales.objects.get(ID=id)
            corral.IDCliente = Clientes_Cero
            corral.Capacidad = capacidad
            corral.FechaAsigna = Fecha
            Corral = corral.Descripcion

            corral.save()
            
            TipoMov = 4
            tblAsignaCorrales.objects.create(
                Clave = formatoClave, IDCorral_id = id, IDCliente_id = clienteAsigna, Fecha = Fecha, TipoMov_id = TipoMov
            )    
        messages.success(request, f'El Corral "{Corral}" del cliente "{Nombre}" ha sido liberado correctamente')
        return render(request, 'Procesos/AsignarCorrales/index.html',{'grupos': grupos, 'ServiciosWeb':ServiciosWeb, 'TClienteCorrales': TClienteCorrales, 'TCorralesLibres':TCorralesLibres, 'FClientes':FClientes, 'clientePost': clientePost})
   
    return render(request, 'Procesos/AsignarCorrales/index.html',{'grupos': grupos, 'ServiciosWeb':ServiciosWeb, 'TClienteCorrales': TClienteCorrales, 'TCorralesLibres':TCorralesLibres, 'FClientes':FClientes, 'clientePost': clientePost})

def TablaHistorialAsignacionCorral(request):
    grupos = grupo_user(request)
    THistorial = tblAsignaCorrales.objects.values(
        'Clave', 'IDCliente_id__Nombre', 'IDCorral_id__Descripcion', 'TipoMov_id__Descripcion', 'Fecha'
    )
    ServiciosWeb = servicioActivo()
    return render(request, 'Procesos/AsignarCorrales/historial.html',{'grupos': grupos, 'ServiciosWeb':ServiciosWeb,
    'THistorial':THistorial})

def TablaCargamentoTolva(request):
    grupos = grupo_user(request)
    TTolva = tblTolva.objects.exclude(ID=1).values('ID', 'Alias', 'IDProducto_id__Descripcion', 'IDEstatus_id__Descripcion', 'IDProducto_id')
    TServido = tblServido.objects.filter(IDEstatus = 8).values('ID', 'Folio',
    'IDCliente_id__Nombre', 'IDCorral_id__Descripcion','IDProducto_id','IDEstatus_id__Descripcion',
    'CantidadSolicitada', 'CantidadServida', 'Prioridad', 'Fecha', 'FechaServida', 'IDTolva_id'
    )
    ServiciosWeb = servicioActivo()
    return render(request, 'Procesos/Tolva/index.html',{'grupos': grupos, 'ServiciosWeb':ServiciosWeb,'TTolva': TTolva, 'TServido':TServido })