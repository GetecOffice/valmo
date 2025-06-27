from django.shortcuts import render
from django.db.models import Q
from django.db.models import Sum
# LLAMAR ARCHIVOS LOCALES
from Aplicacion.forms import *
from Aplicacion.models import *
from Aplicacion.views import grupo_user
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< EDITAR FORMULARIO CATALOGOS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# --------------------------------------------------------CLIENTES---------------------------------------------------------
def editarCliente(request, ID):
    grupos = grupo_user(request)
    TECliente = tblClientes.objects.get(ID=ID)
    return render(request, "Catalogos/Cliente/edit.html",{'grupos': grupos,'TECliente': TECliente})


# -------------------------------------------------------PROVEEDORES-------------------------------------------------------
def editarProveedor(request, ID):
    grupos = grupo_user(request)
    TEProveedor= tblProveedores.objects.get(ID=ID)
    return render(request, "Catalogos/Proveedor/edit.html",{'grupos': grupos,'TEProveedor': TEProveedor})

# -------------------------------------------------------OPERADORES--------------------------------------------------------
def editarOperador(request, ID):
    grupos = grupo_user(request)
    TEOperador = tblOperadores.objects.get(ID=ID)
    Estatus = TEOperador.IDEstatus.ID
    FiltradoEstatus= tblEstatus.objects.get(ID=Estatus)
    FEEstatus = tblEstatus.objects.filter(ID__lte=2).order_by('Descripcion')
    return render(request, "Catalogos/Operador/edit.html",{'grupos': grupos,'TEOperador': TEOperador,'FiltradoEstatus': FiltradoEstatus,'FEEstatus': FEEstatus})

# -----------------------------------------------------MATERIAS PRIMAS-----------------------------------------------------
def editarMateriaPrima(request, ID):
    grupos = grupo_user(request)
    TEMateriaPrima = tblMateriaPrima.objects.get(ID=ID)
    Estatus = TEMateriaPrima.IDEstatus.ID
    Unidad = TEMateriaPrima.IDUnidadMedida.ID
    FiltradoEstatus= tblEstatus.objects.get(ID=Estatus)
    FiltradoUnidad= tblUnidades.objects.get(ID=Unidad)
    FEEstatus = tblEstatus.objects.filter(ID__lte=2).order_by('Descripcion')
    FEUnidad = tblUnidades.objects.all().order_by('Descripcion')
    return render(request, "Catalogos/Materia Prima/edit.html",{'grupos': grupos,'TEMateriaPrima': TEMateriaPrima,'FiltradoEstatus': FiltradoEstatus,'FiltradoUnidad': FiltradoUnidad,'FEEstatus': FEEstatus,'FEUnidad': FEUnidad})

# --------------------------------------------------------PRODUCTOS--------------------------------------------------------
def editarProducto(request, ID):
    grupos = grupo_user(request)
    TEProductos = tblProductos.objects.get(ID=ID)
    Estatus = TEProductos.IDEstatus.ID
    Unidad = TEProductos.IDUnidadMedida.ID
    FiltradoEstatus= tblEstatus.objects.get(ID=Estatus)
    FiltradoUnidad= tblUnidades.objects.get(ID=Unidad)
    FEEstatus = tblEstatus.objects.filter(ID__lte=2).order_by('Descripcion')
    FEUnidad = tblUnidades.objects.all().order_by('Descripcion')
    return render(request, "Catalogos/Producto/edit.html",{'grupos': grupos,'TEProductos': TEProductos,'FiltradoEstatus': FiltradoEstatus,'FiltradoUnidad': FiltradoUnidad,'FEEstatus': FEEstatus,'FEUnidad': FEUnidad})

def editarProductoReceta(request, ID):
    grupos = grupo_user(request)
    TRecetas= tblProductosMateriaPrima.objects.get(ID=ID)
    proporcion = TRecetas.Porcentaje
    folio = TRecetas.IDProductos
    animal = TRecetas.IDMateriaPrima.ID
    FiltradoMateriaPrima = tblMateriaPrima.objects.get(ID=animal)
    FEMateriaPrima = tblMateriaPrima.objects.all()
    # Filtra los registros basados en IDProductos y suma la columna 'Porcentaje'
    total_porcentaje = tblProductosMateriaPrima.objects.filter(IDProductos=folio).aggregate(Sum('Porcentaje'))

    # Verifica si el valor de la suma es None y maneja ese caso
    if total_porcentaje['Porcentaje__sum'] is None:
        total = 0
    else:
        total = total_porcentaje['Porcentaje__sum']  - proporcion
    print(total)
    return render(request, "Catalogos/Producto/editReceta.html",{'grupos': grupos, 'total':total, 
    'TRecetas': TRecetas, 'FiltradoMateriaPrima': FiltradoMateriaPrima, 'FEMateriaPrima': FEMateriaPrima })

# --------------------------------------------------------CORRALES---------------------------------------------------------
def editarCorral(request, ID):
    grupos = grupo_user(request)
    TECorrales= tblCorrales.objects.get(ID=ID)
    Estatus = TECorrales.IDEstatus.ID
    Cliente = TECorrales.IDCliente.ID
    fecha = TECorrales.FechaAsigna
    FiltradoEstatus= tblEstatus.objects.get(ID=Estatus)
    FiltradoCliente= tblClientes.objects.get(ID=Cliente)
    FEEstatus = tblEstatus.objects.filter(ID__lte=2).order_by('Descripcion')
    FECliente = tblClientes.objects.exclude(ID=0).all().order_by('Nombre')
    return render(request, "Catalogos/Corral/edit.html",{'grupos': grupos,'fecha':fecha, 'TECorrales': TECorrales,'FiltradoEstatus': FiltradoEstatus,'FiltradoCliente': FiltradoCliente,'FEEstatus': FEEstatus,'FECliente': FECliente})

# ------------------------------------------------------TIPO ANIMALES------------------------------------------------------
def editarTipoAnimal(request, ID):
    grupos = grupo_user(request)
    TEAnimalTipo = tblAnimalesTipo.objects.get(ID=ID)
    Estatus = TEAnimalTipo.IDEstatus.ID
    FiltradoEstatus= tblEstatus.objects.get(ID=Estatus)
    FEEstatus = tblEstatus.objects.filter(ID__lte=2).order_by('Descripcion')
    return render(request, "Catalogos/Tipo Animal/edit.html",{'grupos': grupos,'TEAnimalTipo': TEAnimalTipo,'FiltradoEstatus': FiltradoEstatus,'FEEstatus': FEEstatus})

# ----------------------------------------------CONTENEDORES MATERIAS PRIMAS-----------------------------------------------
def editarContenendorMP(request, ID):
    grupos = grupo_user(request)
    TEContenedorMP = tblContenedoresMateriaPrima.objects.get(ID=ID)
    Estatus = TEContenedorMP.IDEstatus.ID
    Cliente = TEContenedorMP.IDCliente.ID
    FiltradoEstatus= tblEstatus.objects.get(ID=Estatus)
    FiltradoCliente= tblClientes.objects.get(ID=Cliente)
    FEEstatus = tblEstatus.objects.filter(ID__lte=2).order_by('Descripcion')
    FECliente = tblClientes.objects.exclude(ID=0).all().order_by('Nombre')
    return render(request, "Catalogos/ContenedorMP/edit.html",{'grupos': grupos,'TEContenedorMP': TEContenedorMP,'FiltradoEstatus': FiltradoEstatus,'FiltradoCliente': FiltradoCliente,'FEEstatus': FEEstatus,'FECliente': FECliente})

# -------------------------------------------------CONTENEDORES PRODUCTOS--------------------------------------------------
def editarContnenedorProducto(request, ID):
    grupos = grupo_user(request)
    TEContenedorProductos = tblContenedoresProductos.objects.get(ID=ID)
    Estatus = TEContenedorProductos.IDEstatus.ID
    Cliente = TEContenedorProductos.IDCliente.ID
    FiltradoEstatus= tblEstatus.objects.get(ID=Estatus)
    FiltradoProveedores = tblProveedores.objects.get(ID=Cliente)
    FEEstatus = tblEstatus.objects.filter(ID__lte=2).order_by('Descripcion')
    FEProveedores = tblProveedores.objects.all().order_by('Nombre')
    return render(request, "Catalogos/ContenedorProducto/edit.html",{'grupos': grupos,'TEContenedorProductos': TEContenedorProductos,'FiltradoEstatus': FiltradoEstatus,'FiltradoProveedores': FiltradoProveedores,'FEEstatus': FEEstatus,'FEProveedores': FEProveedores})

# ------------------------------------------------------TOLVA------------------------------------------------------
def editarTolva(request, ID):
    grupos = grupo_user(request)
    TETolva = tblTolva.objects.get(ID=ID)
    Estatus = TETolva.IDEstatus.ID
    Unidad = TETolva.UdeM.ID
    FiltradoEstatus= tblEstatus.objects.get(ID=Estatus)
    FiltradoUnidad= tblUnidades.objects.get(ID=Unidad)
    FEEstatus = tblEstatus.objects.filter(ID__gte=4, ID__lte=6)
    FEUnidades = tblUnidades.objects.all()
    return render(request, "Catalogos/Tolva/edit.html",{'grupos': grupos, 'FEUnidades':FEUnidades, 
        'TETolva': TETolva,'FiltradoEstatus': FiltradoEstatus,'FEEstatus': FEEstatus, 'FiltradoUnidad':FiltradoUnidad})
