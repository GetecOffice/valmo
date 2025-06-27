from django.shortcuts import render
# LLAMAR ARCHIVOS LOCALES
from Aplicacion.forms import *
from Aplicacion.models import *
from django.db.models import Sum
from Aplicacion.views import servicioActivo,grupo_user

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< TABLAS DE CATALOGOS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# --------------------------------------------------------CLIENTES---------------------------------------------------------
def TablaClientes(request):
    grupos = grupo_user(request)
    TClientes = tblClientes.objects.exclude(ID = 1).all()
    ServiciosWeb = servicioActivo()
    return render(request, 'Catalogos/Cliente/index.html',{'grupos': grupos,'ServiciosWeb': ServiciosWeb,'TClientes': TClientes})

# -------------------------------------------------------PROVEEDORES-------------------------------------------------------
def TablaProveedores(request):
    grupos = grupo_user(request)
    TProveedores = tblProveedores.objects.all()
    ServiciosWeb = servicioActivo()
    return render(request, 'Catalogos/Proveedor/index.html',{'grupos': grupos,'ServiciosWeb': ServiciosWeb,'TProveedores': TProveedores }) 
   
# -------------------------------------------------------OPERADORES--------------------------------------------------------
def TablaOperadores(request):
    grupos = grupo_user(request)
    TOperadores = tblOperadores.objects.values('ID', 'Clave', 'Descripcion', 'IDEstatus_id__Descripcion')
    ServiciosWeb = servicioActivo()
    return render(request, 'Catalogos/Operador/index.html',{'grupos': grupos,'ServiciosWeb': ServiciosWeb,'TOperadores': TOperadores})

# -----------------------------------------------------MATERIAS PRIMAS-----------------------------------------------------
def TablaMateriasPrimas(request):
    grupos = grupo_user(request)
    TMateriasPrimas = tblMateriaPrima.objects.values('ID', 'Clave', 'Descripcion', 'IDEstatus_id__Descripcion',
                                                     'IDUnidadMedida_id__Abreviacion','PrecioUnitario','Merma')
    ServiciosWeb = servicioActivo()
    return render(request, 'Catalogos/Materia Prima/index.html',{'grupos': grupos,'ServiciosWeb': ServiciosWeb,'TMateriasPrimas': TMateriasPrimas})

# --------------------------------------------------------PRODUCTOS--------------------------------------------------------
def AgregarRecetas(request, ID):
    grupos = grupo_user(request)
    AgRecetas = tblProductos.objects.get(ID=ID)
    folio = AgRecetas.ID
    folioID = AgRecetas.Clave
    Estatus = AgRecetas.IDEstatus.ID
    Unidad = AgRecetas.IDUnidadMedida.ID
    FiltradoEstatus = tblEstatus.objects.get(ID=Estatus)
    FiltradoUnidad = tblUnidades.objects.get(ID=Unidad)
    FMateriaPrima = tblMateriaPrima.objects.all().order_by('Descripcion')
    Recetas = tblProductosMateriaPrima.objects.filter(IDProductos=folio).values('IDMateriaPrima_id__Descripcion', 
    'Folio', 'Porcentaje','Merma')

    # Filtra los registros basados en IDProductos y suma la columna 'Porcentaje'
    total_porcentaje = tblProductosMateriaPrima.objects.filter(IDProductos=folio).aggregate(Sum('Porcentaje'))


    # Verifica si el valor de la suma es None y maneja ese caso
    if total_porcentaje['Porcentaje__sum'] is None:
        total = 0
    else:
        total = total_porcentaje['Porcentaje__sum']

    print(total)
    ServiciosWeb = servicioActivo()
    return render(request, "Catalogos/Producto/agregar.html",{'grupos': grupos,'AgRecetas': AgRecetas, 'ServiciosWeb': ServiciosWeb,
    'FiltradoEstatus':FiltradoEstatus, 'FiltradoUnidad':FiltradoUnidad, 'folioID':folioID,
    'FMateriaPrima':FMateriaPrima, 'Recetas':Recetas, 'total':total})

def detalleRecetas(request, ID):
    grupos = grupo_user(request)
    AgMovimientos = tblProductos.objects.get(ID=ID)
    folio = AgMovimientos.Clave
    Recetas = tblProductosMateriaPrima.objects.filter(Folio=folio).values('ID', 'Folio',
    'IDMateriaPrima_id__Descripcion', 'Merma', 'Porcentaje')
    ServiciosWeb = servicioActivo()
    return render(request, 'Catalogos/Producto/verDetalle.html',{'grupos': grupos,'ServiciosWeb': ServiciosWeb,'Recetas': Recetas})

def TablaProductos(request):
    grupos = grupo_user(request)
    TProductos = tblProductos.objects.values('ID', 'Clave', 'Descripcion', 'IDEstatus_id__Descripcion',
                                            'IDUnidadMedida_id__Abreviacion','PrecioUnitario','SeSirve').exclude(ID=1)
    ServiciosWeb = servicioActivo()
    return render(request, 'Catalogos/Producto/index.html',{'grupos': grupos,'ServiciosWeb': ServiciosWeb,'TProductos': TProductos})

# --------------------------------------------------------CORRALES---------------------------------------------------------
def TablaCorrales(request):
    grupos = grupo_user(request)
    TCorrales = tblCorrales.objects.values('ID', 'Clave', 'Descripcion', 'IDCliente_id__Nombre',
                                            'IDEstatus_id__Descripcion','Capacidad','FechaAsigna').exclude(IDCliente_id = 1)
    ServiciosWeb = servicioActivo()
    return render(request, 'Catalogos/Corral/index.html',{'grupos': grupos,'ServiciosWeb': ServiciosWeb,
    'TCorrales': TCorrales})

# ------------------------------------------------------TIPO ANIMALES------------------------------------------------------
def TablaTipoAnimales(request):
    grupos = grupo_user(request)
    TTipoAnimales = tblAnimalesTipo.objects.values('ID', 'Clave', 'Descripcion', 'IDEstatus_id__Descripcion')
    ServiciosWeb = servicioActivo()
    return render(request, 'Catalogos/Tipo Animal/index.html',{'grupos': grupos,'ServiciosWeb': ServiciosWeb,'TTipoAnimales': TTipoAnimales})

# ----------------------------------------------CONTENEDORES MATERIAS PRIMAS-----------------------------------------------
def TablaContenedoresMateriasPrimas(request):
    grupos = grupo_user(request)
    TContenedoresMP = tblContenedoresMateriaPrima.objects.values('ID', 'Clave', 'Cliente', 'IDEstatus_id__Descripcion',
                                                                 'Capacidad','IDCliente_id__Nombre')
    ServiciosWeb = servicioActivo()
    return render(request, 'Catalogos/ContenedorMP/index.html',{'grupos': grupos,'ServiciosWeb': ServiciosWeb,'TContenedoresMP': TContenedoresMP})

# -------------------------------------------------CONTENEDORES PRODUCTOS--------------------------------------------------
def TablaContenedoresProductos(request):
    grupos = grupo_user(request)
    ultimo_contacto = tblContenedoresProductos.objects.order_by('-ID').first()
    if ultimo_contacto:
        ultimo_folio = ultimo_contacto.ID + 1
    else:
        ultimo_folio = 1

    TContenedoresProductos = tblContenedoresProductos.objects.values('ID', 'Clave', 'Proveedor', 'IDEstatus_id__Descripcion',
                                                                 'Capacidad','IDCliente_id__Nombre')
    ServiciosWeb = servicioActivo()
    return render(request, 'Catalogos/ContenedorProducto/index.html',{'grupos': grupos,'ServiciosWeb': ServiciosWeb,'TContenedoresProductos': TContenedoresProductos})

def TablaTolva(request):
    grupos = grupo_user(request)
    TTolva = tblTolva.objects.exclude(ID = 1).values('ID', 'Clave', 'Marca', 'Modelo', 'UdeM_id__Abreviacion', 
            'Capacidad', 'IDEstatus_id__Descripcion', 'Alias')
    ServiciosWeb = servicioActivo()
    return render(request, 'Catalogos/Tolva/index.html',{'grupos': grupos,
    'ServiciosWeb': ServiciosWeb,'TTolva': TTolva})
