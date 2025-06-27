from django.shortcuts import render
from datetime import datetime, date
from django.utils import timezone
# LLAMAR ARCHIVOS LOCALES
from Aplicacion.forms import *
from Aplicacion.models import *
from Aplicacion.views import servicioActivo, grupo_user
from django.db.models import Q

def FormularioEntradaMateriasPrimas(request):
    grupos = grupo_user(request)
    ultimo_contacto = tblEntradaMP.objects.order_by('-ID').first()
    if ultimo_contacto:
        ultimo_folio = ultimo_contacto.ID + 1
    else:
        ultimo_folio = 1
    FProveedor = tblProveedores.objects.exclude(ID=0).all().order_by('Nombre')
    FAlmacen = tblContenedoresMateriaPrima.objects.all().order_by('Cliente')
    FAnimal = tblAnimalesTipo.objects.all().order_by('Descripcion')
    FMateriaPrima = tblMateriaPrima.objects.all().order_by('Descripcion')
    FPresentacion= tblTipoPresentacion.objects.all().order_by('Descripcion')
    FTipoMov= tblTipoMov.objects.all().order_by('Descripcion')
    FOperadores = tblOperadores.objects.all().order_by('Descripcion')
    FTransporteMP = tblOtrosDatosMovMP.objects.all()
    FTransporte = tblOtrosDatosSalXBas.objects.all()
    FechaDeHoy = timezone.localtime(timezone.now()).strftime('%Y-%m-%d %H:%M')

    ServiciosWeb = servicioActivo()
    return render(request, 'Procesos/EntradasMateriasPrimas/form.html',{'grupos': grupos, 'ServiciosWeb': ServiciosWeb, 
    'ultimo_folio': ultimo_folio, 'FProveedor': FProveedor, 'FAlmacen': FAlmacen, 'FAnimal': FAnimal,'FechaDeHoy':FechaDeHoy,
    'FMateriaPrima': FMateriaPrima, 'FPresentacion': FPresentacion, 'FTipoMov': FTipoMov, 'FOperadores':FOperadores,
    'FTransporte':FTransporte, 'FTransporteMP':FTransporteMP})

def FormularioOperadorEntradaMateriaPrima(request, ID):
    grupos = grupo_user(request)
    tblOperador = tblOtrosDatosMovMP.objects.get(IDMovMP=ID)
    usuario = tblOperador.IDOperador.id
    usuarioOperador= User.objects.get(id=usuario)
    
    ServiciosWeb = servicioActivo()
    return render(request, "Procesos/EntradasMateriasPrimas/agregar.html",{'grupos': grupos, 'ServiciosWeb': ServiciosWeb, 
    'usuarioOperador':usuarioOperador, 'tblOperador': tblOperador})

def FormularioSalidaMateriasPrimas(request):
    grupos = grupo_user(request)
    ultimo_contacto = tblSalidaMP.objects.order_by('-ID').first()
    if ultimo_contacto:
        ultimo_folio = ultimo_contacto.ID + 1
    else:
        ultimo_folio = 1
    FCliente = tblClientes.objects.exclude(ID=1).all().order_by('Nombre')
    FAlmacen = tblContenedoresMateriaPrima.objects.all().order_by('Cliente')
    FAnimal = tblAnimalesTipo.objects.all().order_by('Descripcion')
    FMateriaPrima = tblMateriaPrima.objects.all().order_by('Descripcion')
    FPresentacion= tblTipoPresentacion.objects.all().order_by('Descripcion')
    FTipoMov= tblTipoMov.objects.all().order_by('Descripcion')
    FOperadores = tblOperadores.objects.all().order_by('Descripcion')
    FTransporte = tblOtrosDatosSalXBas.objects.all()
    FechaDeHoy = timezone.localtime(timezone.now()).strftime('%Y-%m-%d %H:%M')

    ServiciosWeb = servicioActivo()
    return render(request, 'Procesos/SalidasMateriasPrimas/form.html',{'grupos': grupos, 'ServiciosWeb': ServiciosWeb, 
    'ultimo_folio': ultimo_folio, 'FCliente': FCliente, 'FAlmacen': FAlmacen, 'FAnimal': FAnimal,'FechaDeHoy':FechaDeHoy,
    'FMateriaPrima': FMateriaPrima, 'FPresentacion': FPresentacion, 'FTipoMov': FTipoMov, 'FOperadores':FOperadores,
    'FTransporte':FTransporte})

def FormularioOperadorSalidaMateriaPrima(request, ID):
    grupos = grupo_user(request)
    tblOperador = tblOtrosDatosSalXBas.objects.get(IDSalida=ID)
    usuario = tblOperador.IDOperador.id
    usuarioOperador= User.objects.get(id=usuario)
    
    ServiciosWeb = servicioActivo()
    return render(request, "Procesos/SalidasMateriasPrimas/agregar.html",{'grupos': grupos, 'ServiciosWeb': ServiciosWeb, 
    'usuarioOperador':usuarioOperador, 'tblOperador': tblOperador})

def FormularioEntradaProductos(request):
    grupos = grupo_user(request)
    ultimo_contacto = tblEntradaProductos.objects.order_by('-ID').first()
    if ultimo_contacto:
        ultimo_folio = ultimo_contacto.ID + 1
    else:
        ultimo_folio = 1
 
    FProveedor = tblProveedores.objects.all().order_by('Nombre')
    FMovimiento = tblTipoMov.objects.all().order_by('Descripcion')
    FAlmacen = tblContenedoresProductos.objects.all().order_by('Proveedor')
    FProductos = tblProductos.objects.all().exclude(ID=1).order_by('Descripcion')
    FPresentacion = tblTipoPresentacion.objects.all().order_by('Descripcion')
    FOperadores = tblOperadores.objects.all().order_by('Descripcion')
    FTransporte = tblOtrosDatosMovMP.objects.all()
    ServiciosWeb = servicioActivo()
    FechaDeHoy = timezone.localtime(timezone.now()).strftime('%Y-%m-%d %H:%M')
    
    ServiciosWeb = servicioActivo()
    return render(request, 'Procesos/EntradaProductos/form.html',{'grupos': grupos, 'ServiciosWeb': ServiciosWeb, 
    'ultimo_folio': ultimo_folio,'FProveedor':FProveedor, 'FMovimiento':FMovimiento,'FechaDeHoy':FechaDeHoy,
     'FProductos':FProductos, 'FPresentacion':FPresentacion,'FOperadores':FOperadores, 'FAlmacen':FAlmacen, 
    'FTransporte':FTransporte,'ServiciosWeb':ServiciosWeb})

def FormularioOperadoresEntradaProductos(request, ID):
    grupos = grupo_user(request)
    tblOperador = tblOtrosDatosMovMP.objects.get(IDMovMP=ID)
    usuario = tblOperador.IDOperador.id
    usuarioOperador= User.objects.get(id=usuario)
    
    ServiciosWeb = servicioActivo()
    return render(request, "Procesos/EntradaProductos/agregar.html",{'grupos': grupos, 'ServiciosWeb': ServiciosWeb, 
    'usuarioOperador':usuarioOperador, 'tblOperador': tblOperador})

def FormularioSalidaProductos(request):
    grupos = grupo_user(request)
    ultimo_contacto = tblSalidaProductos.objects.order_by('-ID').first()
    if ultimo_contacto:
        ultimo_folio = ultimo_contacto.ID + 1
    else:
        ultimo_folio = 1
 
    FCliente = tblClientes.objects.exclude(ID = 1).all().order_by('Nombre')
    FMovimiento = tblTipoMov.objects.all().order_by('Descripcion')
    FAlmacen = tblContenedoresProductos.objects.all().order_by('Proveedor')
    FMateriaPrima = tblMateriaPrima.objects.all().order_by('Descripcion')
    FProductos = tblProductos.objects.all().exclude(ID=1).order_by('Descripcion')
    FPresentacion = tblTipoPresentacion.objects.all().order_by('Descripcion')
    FOperadores = tblOperadores.objects.all().order_by('Descripcion')
    FTransporte = tblOtrosDatosSalXBas.objects.all()
    
    ServiciosWeb = servicioActivo()
    FechaDeHoy = timezone.localtime(timezone.now()).strftime('%Y-%m-%d %H:%M')
    return render(request, 'Procesos/SalidasProductos/form.html',{'grupos': grupos, 'ServiciosWeb': ServiciosWeb, 
    'ultimo_folio': ultimo_folio,'FCliente':FCliente, 'FMovimiento':FMovimiento,'FechaDeHoy':FechaDeHoy,
    'FMateriaPrima':FMateriaPrima, 'FProductos':FProductos, 'FPresentacion':FPresentacion,'FOperadores':FOperadores,
    'FTransporte':FTransporte, 'FAlmacen':FAlmacen})

def FormularioOperadoresSalidaProductos(request, ID):
    grupos = grupo_user(request)
    tblOperador = tblOtrosDatosSalXBas.objects.get(IDSalida=ID)
    usuario = tblOperador.IDOperador.id
    usuarioOperador= User.objects.get(id=usuario)
    
    ServiciosWeb = servicioActivo()
    return render(request, "Procesos/SalidasProductos/agregar.html",{'grupos': grupos, 'ServiciosWeb': ServiciosWeb, 
    'usuarioOperador':usuarioOperador, 'tblOperador': tblOperador})

def FormularioMovimientoAnimales(request):
    grupos = grupo_user(request)
    ultimo_contacto = tblMovimientoAnimales.objects.order_by('-ID').first()
    if ultimo_contacto:
        ultimo_folio = ultimo_contacto.ID + 1
        formatoClave = 'F-{:06d}'.format(ultimo_folio)
    else:
        ultimo_folio = 1
        formatoClave = 'F-{:06d}'.format(ultimo_folio)
    FCliente = tblClientes.objects.exclude(ID = 1).all().order_by('Nombre')
    FCorral = tblCorrales.objects.all().order_by('Descripcion')
    
    FMovimiento = tblTipoMov.objects.filter(ID__in=[1, 2])
    FTipoAnimal = tblAnimalesTipo.objects.all().order_by('Descripcion')
    FechaDeHoy = timezone.localtime(timezone.now()).strftime('%Y-%m-%d')
    
    ServiciosWeb = servicioActivo()
    return render(request, 'Procesos/MovimientosAnimales/form.html',{'grupos': grupos, 'ServiciosWeb': ServiciosWeb,  
    'ultimo_folio': ultimo_folio,'FCliente':FCliente,'FCorral':FCorral,'FMovimiento':FMovimiento,'FechaDeHoy':FechaDeHoy,
    'FTipoAnimal':FTipoAnimal, 'formatoClave':formatoClave})

def FormularioDetallesAnimales(request):
    grupos = grupo_user(request)
    ultimo_contacto = tblDetalleAnimales.objects.order_by('-ID').first()
    if ultimo_contacto:
        ultimo_folio = ultimo_contacto.ID + 1
    else:
        ultimo_folio = 1
    FCliente = tblClientes.objects.exclude(ID = 1).all()
    FCorral = tblCorrales.objects.all()
    FMovimiento = tblTipoMov.objects.all()
    FTipoAnimal = tblAnimalesTipo.objects.all()
    
    ServiciosWeb = servicioActivo()
    return render(request, 'Procesos/DetallesAnimales/form.html',{'grupos': grupos, 'ServiciosWeb': ServiciosWeb, 'ultimo_folio': ultimo_folio,'FCliente':FCliente,'FCorral':FCorral,'FMovimiento':FMovimiento,'FTipoAnimal':FTipoAnimal})

def FormularioSolicitudServido(request):
    grupos = grupo_user(request)
    ultimo_contacto = tblServido.objects.order_by('-ID').first()
    if ultimo_contacto:
        ultimo_folio = ultimo_contacto.ID + 1
    else:
        ultimo_folio = 1
    FClientes = tblClientes.objects.exclude(ID = 1).all().order_by('Nombre')
    FECorrales = tblCorrales.objects.exclude(Q(IDCliente= 1)).order_by('Descripcion')
    FEProductos = tblProductos.objects.all().exclude(ID=1).order_by('Descripcion')
    FEstatus = tblEstatus.objects.filter(ID__lte=2).order_by('Descripcion')
    FechaDeHoy = timezone.localtime(timezone.now()).strftime('%Y-%m-%d %H:%M')

    ServiciosWeb = servicioActivo()
    return render(request, 'Procesos/Solicitud Servido/form.html',{'grupos': grupos, 'ServiciosWeb': ServiciosWeb,  'FECorrales': FECorrales, 'ultimo_folio':ultimo_folio,
    'FechaDeHoy':FechaDeHoy, 'FClientes': FClientes, 'FEstatus': FEstatus, 'FEProductos':FEProductos})

def FormularioServidoAnimales(request):
    grupos = grupo_user(request)
    ultimo_contacto = tblServido.objects.order_by('-ID').first()
    if ultimo_contacto:
        ultimo_folio = ultimo_contacto.ID + 1
    else:
        ultimo_folio = 1
    FClientes = tblClientes.objects.exclude(ID = 1).all().order_by('Nombre')
    FECorrales = tblCorrales.objects.exclude(IDCliente = 1).all().order_by('Descripcion')
    FEProductos = tblProductos.objects.all().exclude(ID=1).order_by('Descripcion')
    FEstatus = tblEstatus.objects.filter(ID__lte=2).order_by('Descripcion')
    FechaDeHoy = timezone.localtime(timezone.now()).strftime('%Y-%m-%d %H:%M')
    
    ServiciosWeb = servicioActivo()
    return render(request, 'Procesos/Servido Manual/form.html',{'grupos': grupos, 'ServiciosWeb': ServiciosWeb,  'FECorrales': FECorrales, 'ultimo_folio':ultimo_folio,
    'FechaDeHoy':FechaDeHoy, 'FClientes': FClientes, 'FEstatus': FEstatus, 'FEProductos':FEProductos})

def FormularioInventarioMateriaPrima(request):
    grupos = grupo_user(request)
    ultimo_contacto = tblInventarioInicialesMP.objects.order_by('-ID').first()
    if ultimo_contacto:
        ultimo_folio = ultimo_contacto.ID + 1
    else:
        ultimo_folio = 1
    FMateriaPrima = tblMateriaPrima.objects.all().order_by('Descripcion')
    FAlmacen = tblContenedoresMateriaPrima.objects.all().order_by('Cliente')
    FechaDeHoy = timezone.localtime(timezone.now()).strftime('%Y-%m-%d %H:%M')

    ServiciosWeb = servicioActivo()
    return render(request, 'Procesos/InventarioMateriaPrima/form.html',{'grupos': grupos, 'ServiciosWeb': ServiciosWeb, 'FAlmacen': FAlmacen,
    'ultimo_folio': ultimo_folio, 'FechaDeHoy':FechaDeHoy, 'FMateriaPrima': FMateriaPrima })

def FormularioInventarioProducto(request):
    grupos = grupo_user(request)
    ultimo_contacto = tblInventarioInicialesProductos.objects.order_by('-ID').first()
    if ultimo_contacto:
        ultimo_folio = ultimo_contacto.ID + 1
    else:
        ultimo_folio = 1
    FProductos= tblProductos.objects.all().order_by('Descripcion')
    FAlmacen = tblContenedoresProductos.objects.all().order_by('Proveedor')
    FechaDeHoy = timezone.localtime(timezone.now()).strftime('%Y-%m-%d %H:%M')

    ServiciosWeb = servicioActivo()
    return render(request, 'Procesos/InventarioProductos/form.html',{'grupos': grupos, 'ServiciosWeb': ServiciosWeb, 'FAlmacen': FAlmacen,
    'ultimo_folio': ultimo_folio, 'FechaDeHoy':FechaDeHoy, 'FProductos': FProductos })
