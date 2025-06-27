from django.shortcuts import render
# LLAMAR ARCHIVOS LOCALES
from Aplicacion.forms import *
from Aplicacion.models import *
from Aplicacion.views import grupo_user
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< EDITAR FORMULARIO PROCESOS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# --------------------------------------------------------SERVIDOS--------------------------------------------------------
# --------------------------------------------------------CORRALES---------------------------------------------------------


def editarEntradaMateriaPrima(request, ID):
    grupos = grupo_user(request)
    TEEntradaMateriaPrima= tblEntradaMP.objects.get(ID=ID)
    Presentacion = TEEntradaMateriaPrima.IDPresentacion.ID
    Proveedor = TEEntradaMateriaPrima.IDProveedor.ID
    MateriaPrima = TEEntradaMateriaPrima.IDMateriaPrima.ID
    Alamcen = TEEntradaMateriaPrima.IDAlmacen.ID
    fecha = TEEntradaMateriaPrima.fecha

    FiltradoProveedor= tblProveedores.objects.get(ID=Proveedor)
    FiltradoPresentacion= tblTipoPresentacion.objects.get(ID=Presentacion)
    FiltradoMateriaPria = tblMateriaPrima.objects.get(ID=MateriaPrima)
    FiltradoAlmacen = tblContenedoresMateriaPrima.objects.get(ID=Alamcen)

    FEMateriaPrima = tblMateriaPrima.objects.all().order_by('Descripcion')
    FETipoPresentacion = tblTipoPresentacion.objects.all().order_by('Descripcion')
    FEProveedores = tblProveedores.objects.all().order_by('Nombre')
    FEAlmacen= tblContenedoresMateriaPrima.objects.all().order_by('Cliente')

    return render(request, "Procesos/EntradasMateriasPrimas/edit.html",{'grupos': grupos,
    'TEEntradaMateriaPrima': TEEntradaMateriaPrima, 'FiltradoMateriaPria': FiltradoMateriaPria,
    'FiltradoPresentacion': FiltradoPresentacion, 'fecha':fecha, 'FiltradoProveedor':FiltradoProveedor,
    'FEProveedores': FEProveedores, 'FETipoPresentacion': FETipoPresentacion, 'FEMateriaPrima': FEMateriaPrima, 
    'FiltradoAlmacen':FiltradoAlmacen, 'FEAlmacen':FEAlmacen})

def editarOperadorEntradaMateriaPrima(request, ID):
    grupos = grupo_user(request)
    tblOperador = tblOtrosDatosMovMP.objects.get(IDMovMP=ID)
    usuario = tblOperador.IDOperador.id
    usuarioOperador= User.objects.get(id=usuario)
    return render(request, "Procesos/EntradasMateriasPrimas/editOperador.html",{'grupos': grupos,
    'usuarioOperador':usuarioOperador, 'tblOperador': tblOperador})

def editarSalidaMateriaPrima(request, ID):
    grupos = grupo_user(request)
    TSalidasMateriasPrimas= tblSalidaMP.objects.get(ID=ID)
    Presentacion = TSalidasMateriasPrimas.IDPresentacion.ID
    MateriaPrima = TSalidasMateriasPrimas.IDMateriaPrima.ID
    Cliente = TSalidasMateriasPrimas.IDCliente.ID
    Almacen = TSalidasMateriasPrimas.IDAlmacen.ID
    fecha = TSalidasMateriasPrimas.fecha
    
    FiltradoPresentacion= tblTipoPresentacion.objects.get(ID=Presentacion)
    FiltradoMateriaPrima = tblMateriaPrima.objects.get(ID=MateriaPrima)
    FiltradoCliente = tblClientes.objects.get(ID=Cliente)
    FiltradoAlmacen = tblContenedoresMateriaPrima.objects.get(ID=Almacen)

    FEMateriaPrima = tblMateriaPrima.objects.all().order_by('Descripcion')
    FETipoPresentacion = tblTipoPresentacion.objects.all().order_by('Descripcion')
    FEClientes = tblClientes.objects.exclude(ID=1).order_by('Nombre')
    FEAlmacen = tblContenedoresMateriaPrima.objects.all().order_by('Cliente')
    return render(request, "Procesos/SalidasMateriasPrimas/edit.html",{'grupos': grupos,'TSalidasMateriasPrimas': TSalidasMateriasPrimas,
    'FiltradoPresentacion': FiltradoPresentacion, 'fecha':fecha, 'FiltradoCliente':FiltradoCliente,
    'FiltradoMateriaPrima': FiltradoMateriaPrima, 'FEClientes': FEClientes, 'FiltradoAlmacen':FiltradoAlmacen, 'FEAlmacen':FEAlmacen,
    'FETipoPresentacion': FETipoPresentacion, 'FEMateriaPrima': FEMateriaPrima})

def editarOperadorSalidaMateriaPrima(request, ID):
    grupos = grupo_user(request)
    tblOperador = tblOtrosDatosSalXBas.objects.get(IDSalida=ID)
    usuario = tblOperador.IDOperador.id
    usuarioOperador= User.objects.get(id=usuario)
    return render(request, "Procesos/SalidasMateriasPrimas/editOperador.html",{'grupos': grupos,
    'usuarioOperador':usuarioOperador, 'tblOperador': tblOperador})

def editarEntradaProductos(request, ID):
    grupos = grupo_user(request)
    TEEntradaProducto= tblEntradaProductos.objects.get(ID=ID)
    Presentacion = TEEntradaProducto.IDPresentacion.ID
    Proveedor = TEEntradaProducto.IDProveedor.ID
    Producto = TEEntradaProducto.IDProductos.ID
    Almacen = TEEntradaProducto.IDAlmacen.ID
    fecha = TEEntradaProducto.fecha

    FiltradoProveedor= tblProveedores.objects.get(ID=Proveedor)
    FiltradoPresentacion= tblTipoPresentacion.objects.get(ID=Presentacion)
    FiltradoProducto = tblProductos.objects.get(ID=Producto)
    FiltradoAlmacen = tblContenedoresProductos.objects.get(ID=Almacen)

    FEProductos= tblProductos.objects.all().order_by('Descripcion').exclude(ID = 1)
    FETipoPresentacion = tblTipoPresentacion.objects.all().order_by('Descripcion')
    FEProveedores = tblProveedores.objects.all().order_by('Nombre')
    FEAlmacen = tblContenedoresProductos.objects.all().order_by('Proveedor')

    return render(request, "Procesos/EntradaProductos/edit.html",{'grupos': grupos, 'FEAlmacen':FEAlmacen,
    'TEEntradaProducto': TEEntradaProducto, 'FiltradoProducto': FiltradoProducto, 'FiltradoAlmacen':FiltradoAlmacen,
    'FiltradoPresentacion': FiltradoPresentacion, 'fecha':fecha, 'FiltradoProveedor':FiltradoProveedor,
    'FEProveedores': FEProveedores, 'FETipoPresentacion': FETipoPresentacion, 'FEProductos': FEProductos
    })

def editarOperadorEntradaProducto(request, ID):
    grupos = grupo_user(request)
    tblOperador = tblOtrosDatosMovMP.objects.get(IDMovMP=ID)
    usuario = tblOperador.IDOperador.id
    usuarioOperador= User.objects.get(id=usuario)
    return render(request, "Procesos/EntradaProductos/editOperador.html",{'grupos': grupos,
    'usuarioOperador':usuarioOperador, 'tblOperador': tblOperador})

def editarSalidaProductos(request, ID):
    grupos = grupo_user(request)
    TSalidaProductos= tblSalidaProductos.objects.get(ID=ID)
    Producto = TSalidaProductos.IDProductos.ID
    Presentacion = TSalidaProductos.IDPresentacion.ID
    Cliente = TSalidaProductos.IDCliente.ID
    Almacen = TSalidaProductos.IDAlmacen.ID
    fecha = TSalidaProductos.fecha

    FiltradoProducto = tblProductos.objects.get(ID=Producto)
    FiltradoCliente = tblClientes.objects.get(ID=Cliente)
    FiltradoPresentacion = tblTipoPresentacion.objects.get(ID=Presentacion)
    FiltradoAlmacen = tblContenedoresProductos.objects.get(ID=Almacen)

    FEProducto = tblProductos.objects.all().order_by('Descripcion')
    FETipoPresentacion = tblTipoPresentacion.objects.all().order_by('Descripcion')
    FEClientes = tblClientes.objects.exclude(ID=1).all().order_by('Nombre')
    FEAlmacen = tblContenedoresProductos.objects.all().order_by('Proveedor')

    return render(request, "Procesos/SalidasProductos/edit.html",{'grupos': grupos,'TSalidaProductos': TSalidaProductos,
    'FiltradoPresentacion': FiltradoPresentacion, 'FiltradoProducto': FiltradoProducto, 'FiltradoCliente':FiltradoCliente, 'fecha':fecha, 
    'FEClientes': FEClientes, 'FETipoPresentacion': FETipoPresentacion, 'FEProducto': FEProducto, 'FiltradoAlmacen':FiltradoAlmacen, 'FEAlmacen':FEAlmacen})

def editarOperadoresSalidaProductos(request, ID):
    grupos = grupo_user(request)
    tblOperador = tblOtrosDatosSalXBas.objects.get(IDSalida=ID)
    usuario = tblOperador.IDOperador.id
    usuarioOperador= User.objects.get(id=usuario)
    return render(request, "Procesos/SalidasProductos/editOperador.html",{'grupos': grupos,
    'usuarioOperador':usuarioOperador, 'tblOperador': tblOperador})

def editarCantidadMovimientosAnimales(request, ID):
    grupos = grupo_user(request)
    TCantidadMovimientoAnimales = tblDetalleMovAnimales.objects.get(ID=ID)
    animal = TCantidadMovimientoAnimales.IDAnimales.ID
    corral = TCantidadMovimientoAnimales.IDCorral.ID
    FiltradoAnimales = tblAnimalesTipo.objects.get(ID=animal)
    FiltradoCorral = tblCorrales.objects.get(ID=corral)
    FEAnimal = tblAnimalesTipo.objects.all().order_by('Descripcion')
    FECorral = tblCorrales.objects.all().order_by('Descripcion')

    return render(request, "Procesos/MovimientosAnimales/editCantAni.html",{'grupos': grupos,
    'TCantidadMovimientoAnimales': TCantidadMovimientoAnimales, 'FiltradoCorral':FiltradoCorral,
    'FiltradoAnimales': FiltradoAnimales, 'FEAnimal': FEAnimal, 'FECorral':FECorral })

def editarMovimientosAnimales(request, ID):
    grupos = grupo_user(request)
    TMovimientoAnimales= tblMovimientoAnimales.objects.get(ID=ID)
    Cliente = TMovimientoAnimales.IDCliente.ID
    fecha = TMovimientoAnimales.Fecha
    FiltradoCliente = tblClientes.objects.get(ID=Cliente)
    FECliente = tblClientes.objects.all().exclude(ID=0).order_by('Nombre')
    FECorral = tblCorrales.objects.all().order_by('Descripcion')
    return render(request, "Procesos/MovimientosAnimales/edit.html",{'grupos': grupos,'TMovimientoAnimales': TMovimientoAnimales,
    'FiltradoCliente': FiltradoCliente, 'fecha':fecha,
    'FECliente': FECliente, 'FECorral': FECorral})

def editarSolicitudServidos(request, ID):
    grupos = grupo_user(request)
    TEServidos= tblServido.objects.get(ID=ID)
    Cliente = TEServidos.IDCliente.ID
    Estatus = TEServidos.IDEstatus.ID
    Producto = TEServidos.IDProducto.ID
    Corral = TEServidos.IDCorral.ID
    fecha = TEServidos.Fecha
    fechaServida = TEServidos.FechaServida
    FiltradoEstatus= tblEstatus.objects.get(ID=Estatus)
    FiltradoCliente= tblClientes.objects.get(ID=Cliente)
    FiltradoProducto= tblProductos.objects.get(ID=Producto)
    FiltradoCorral= tblCorrales.objects.get(ID=Corral)
    FECorral = tblCorrales.objects.all().order_by('Descripcion')
    FEProducto = tblProductos.objects.all().order_by('Descripcion')
    FEEstatus = tblEstatus.objects.filter(ID=3).order_by('Descripcion')
    FECliente = tblClientes.objects.exclude(ID=0).all().order_by('Nombre')
    return render(request, "Procesos/Solicitud Servido/edit.html",{'grupos': grupos,'TEServidos': TEServidos, 'fecha':fecha,
    'FiltradoEstatus': FiltradoEstatus,'FiltradoCliente': FiltradoCliente,'FiltradoProducto': FiltradoProducto,
    'FiltradoCorral': FiltradoCorral,'FECorral': FECorral,'FEProducto': FEProducto, 'fechaServida':fechaServida,
    'FEEstatus': FEEstatus,'FECliente': FECliente})

def editarServidosManuales(request, ID):
    grupos = grupo_user(request)
    TEServidos= tblServido.objects.get(ID=ID)
    Cliente = TEServidos.IDCliente.ID
    Estatus = TEServidos.IDEstatus.ID
    Producto = TEServidos.IDProducto.ID
    Corral = TEServidos.IDCorral.ID
    fecha = TEServidos.Fecha
    fechaServida = TEServidos.FechaServida
    FiltradoEstatus= tblEstatus.objects.get(ID=Estatus)
    FiltradoCliente= tblClientes.objects.get(ID=Cliente)
    FiltradoProducto= tblProductos.objects.get(ID=Producto)
    FiltradoCorral= tblCorrales.objects.get(ID=Corral)
    FECorral = tblCorrales.objects.all().order_by('Descripcion')
    FEProducto = tblProductos.objects.all().order_by('Descripcion')
    FEEstatus = tblEstatus.objects.filter(ID=3).order_by('Descripcion')
    FECliente = tblClientes.objects.exclude(ID=0).all().order_by('Nombre')
    return render(request, "Procesos/Servido Manual/edit.html",{'grupos': grupos,'TEServidos': TEServidos, 'fecha':fecha,
    'FiltradoEstatus': FiltradoEstatus,'FiltradoCliente': FiltradoCliente,'FiltradoProducto': FiltradoProducto,
    'FiltradoCorral': FiltradoCorral,'FECorral': FECorral,'FEProducto': FEProducto, 'fechaServida':fechaServida,
    'FEEstatus': FEEstatus,'FECliente': FECliente})

def editarInventarioInicialMateriaPrima(request, ID):
    grupos = grupo_user(request)
    TEInventario= tblInventarioInicialesMP.objects.get(ID=ID)
    ContenedorMP = TEInventario.IDContenedor.ID
    MateriaPrima = TEInventario.IDMateriaPrima.ID
    fecha = TEInventario.Fecha

    FiltradoContenedorMP= tblContenedoresMateriaPrima.objects.get(ID=ContenedorMP)
    FiltradoMateriaPrima= tblMateriaPrima.objects.get(ID=MateriaPrima)

    FEContenedorMP = tblContenedoresMateriaPrima.objects.all().order_by('Cliente')
    FEMateriaPrima = tblMateriaPrima.objects.all().order_by('Descripcion')

    return render(request, "Procesos/InventarioMateriaPrima/edit.html",{'grupos': grupos,
    'TEInventario': TEInventario,  'FiltradoContenedorMP': FiltradoContenedorMP,
    'FiltradoMateriaPrima': FiltradoMateriaPrima,'FEContenedorMP': FEContenedorMP,
    'FEMateriaPrima': FEMateriaPrima, 'fecha':fecha})

def editarInventarioInicialProducto(request, ID):
    grupos = grupo_user(request)
    TEInventario= tblInventarioInicialesProductos.objects.get(ID=ID)
    Contenedor = TEInventario.IDContenedor.ID
    productos = TEInventario.IDProducto.ID
    fecha = TEInventario.Fecha

    FiltradoContenedorProductos= tblContenedoresProductos.objects.get(ID=Contenedor)
    FiltradoProductos= tblProductos.objects.get(ID=productos)

    FEContenedorProducto = tblContenedoresProductos.objects.all().order_by('Proveedor')
    FEProductos = tblProductos.objects.all().order_by('Descripcion')

    return render(request, "Procesos/InventarioProductos/edit.html",{'grupos': grupos,
    'TEInventario': TEInventario,  'FiltradoContenedorProductos': FiltradoContenedorProductos,
    'FiltradoProductos': FiltradoProductos,'FEContenedorProducto': FEContenedorProducto,
    'FEProductos': FEProductos, 'fecha':fecha})