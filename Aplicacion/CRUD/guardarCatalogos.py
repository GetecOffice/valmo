from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Sum
# LLAMAR ARCHIVOS LOCALES
from Aplicacion.forms import *
from Aplicacion.models import *
from Aplicacion.views import agregarDatosTecnicos
from datetime import datetime, date
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< GUARDAR FORMULARIO CATALOGOS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# --------------------------------------------------------CLIENTES---------------------------------------------------------
def guardarCliente(request):
    # PARAMETROS ENVIADOS DESDE EL FORMULARIO
    clave = request.POST['clave']
    nombre = request.POST['nombre'].upper()
    contacto = request.POST['contacto'].upper()
    direccion = request.POST['direccion'].upper()
    ciudad = request.POST['ciudad'].upper()
    rfc = request.POST['rfc']
    email = request.POST['email']
    numero = request.POST['numero']

    # AQUI SE CREAR EL FOLIO PARA LAS TABLAS
    clave_int = int(clave)
    formatoClave = 'F-{:06d}'.format(clave_int)

    if request.method == 'POST':
        if request.method == 'POST':
            if 'guardar-datos' in request.POST:
                guardar = True
            else:
                guardar = False
    else:
        guardar = False

    # PARAMENTROS PARA ALMACENAR AL USUARIO QUE HA AGREGADO DATOS 
    Tecnico_v = request.POST['tecnico'].upper()
    NombreTabla_v = 'Cliente'
    IDFilaTabla_v = formatoClave
    AreaRegistro_v = 'Catalogos'
    IDFila_v = clave

    nombre_Existe = tblClientes.objects.filter(Nombre=nombre).exists()
    if nombre_Existe:
        errorCliente = 'error'
        messages.error(request, f'El Cliente "{nombre}" ya ha sido registrado antreriormente')
        columnas = {'clave':clave, 'contacto':contacto, 'direccion':direccion, 'ciudad':ciudad,
                    'nombre': nombre, 'rfc':rfc, 'email':email, 'numero':numero,
                     'errorCliente':errorCliente, 'guardar':guardar
        }
        return render(request, "Catalogos/Cliente/form.html", columnas)
    else:
        tblClientes.objects.create(
            Clave = formatoClave, Nombre = nombre, Direccion = direccion, Ciudad = ciudad, RFC = rfc, Email = email,
            Contacto = contacto, TelefonoContacto = numero
        )
        agregarDatosTecnicos(request, Tecnico_v, NombreTabla_v, IDFilaTabla_v, AreaRegistro_v, IDFila_v)
        messages.success(request, f'El Cliente {nombre} se ha registrado exitosamente')
    
    ultimo_id = tblClientes.objects.order_by('-ID').first()
    if ultimo_id:
        ultimo_folio = ultimo_id.ID + 1
    else:
        ultimo_folio = 1

    if request.method == 'POST':
        if 'salir' in request.POST:
            return redirect('T-Cliente')
        elif 'agregar' in request.POST:
            if 'guardar-datos' in request.POST: 
                guardar = True
                columnas = {'clave':ultimo_folio, 'contacto':contacto, 'direccion':direccion,
                            'ciudad':ciudad, 'rfc':rfc, 'email':email, 'numero':numero, 
                            'nombre':nombre, 'guardar': guardar
                }
                return render(request, "Catalogos/Cliente/form.html", columnas)
            else:
                return redirect('F-Cliente')
    else:
        return redirect('T-Cliente')
    
# -------------------------------------------------------PROVEEDORES-------------------------------------------------------
def guardarProveedor(request):
    clave = request.POST['clave']
    nombre = request.POST['nombre'].upper()
    contacto = request.POST['contacto'].upper()
    direccion = request.POST['direccion'].upper()
    ciudad = request.POST['ciudad'].upper()
    rfc = request.POST['rfc']
    email = request.POST['email']
    numero = request.POST['numero']

    clave_int = int(clave)
    formatoClave = 'F-{:06d}'.format(clave_int)

    if request.method == 'POST':
        if request.method == 'POST':
            if 'guardar-datos' in request.POST:
                guardar = True
            else:
                guardar = False
    else:
        guardar = False

    # tecnicos
    Tecnico_v = request.POST['tecnico'].upper()
    NombreTabla_v = 'Proveedor'
    IDFilaTabla_v = formatoClave
    AreaRegistro_v = 'Catalogos'
    IDFila_v = clave

    existente = tblProveedores.objects.filter(Nombre=nombre).exists()
    if existente:
        errorProveedor = 'error'
        messages.error(request, f'El Proveedor {nombre} ya ha sido registrado antreriormente')
        columnas = {'clave':clave, 'nombre':nombre, 'contacto':contacto, 'direccion':direccion, 'ciudad':ciudad, 'rfc':rfc, 
                    'email':email, 'numero':numero,'errorProveedor':errorProveedor, 'guardar':guardar
        }
        return render(request, "Catalogos/Proveedor/form.html", columnas)
    else:
        tblProveedores.objects.create(
            Clave = formatoClave, Nombre = nombre, Direccion = direccion, Ciudad = ciudad, RFC = rfc, Email = email,
            Contacto = contacto, TelefonoContacto = numero
        )
        agregarDatosTecnicos(request, Tecnico_v, NombreTabla_v, IDFilaTabla_v, AreaRegistro_v, IDFila_v)
        messages.success(request, f'El Proveedor {nombre} se ha registrado exitosamente')

    ultimo_id = tblProveedores.objects.order_by('-ID').first()
    if ultimo_id:
        ultimo_folio = ultimo_id.ID + 1
    else:
        ultimo_folio = 1

    # SE VERIFICA EL POST Y DEPENDIENDO DEL PARAMETRO DEL FORMULARIO
    if request.method == 'POST':
        if 'salir' in request.POST:
            return redirect('T-Proveedor')
        elif 'agregar' in request.POST:
            if 'guardar-datos' in request.POST: 
                guardar = True
                columnas = {'clave':ultimo_folio, 'contacto':contacto, 'direccion':direccion,
                            'ciudad':ciudad, 'rfc':rfc, 'email':email, 'numero':numero, 
                            'nombre':nombre, 'guardar': guardar
                }
                return render(request, "Catalogos/Proveedor/form.html", columnas)
            else:
                return redirect('F-Proveedor')
    else:
        return redirect('T-Proveedor')

# -------------------------------------------------------OPERADORES--------------------------------------------------------
def guardarOperador(request):
    clave = request.POST['clave']
    nombre = request.POST['nombre'].upper()
    estatus = request.POST['estatus']

    clave_int = int(clave)
    formatoClave = 'F-{:06d}'.format(clave_int)

    # tecnicos
    Tecnico_v = request.POST['tecnico'].upper()
    NombreTabla_v = 'Operador'
    IDFilaTabla_v = formatoClave
    AreaRegistro_v = 'Catalogos'
    IDFila_v = clave

    existente = tblOperadores.objects.filter(Descripcion=nombre).exists()
    if existente:
        errorCol = 'error'
        FEstatus = tblEstatus.objects.all() 
        messages.error(request, f'El Operador {nombre} ya ha sido registrado antreriormente')
        columnas = {'clave':clave, 'FEstatus': FEstatus, 'errorCol':errorCol}
        return render(request, "Catalogos/Operador/form.html", columnas)
    else:
        tblOperadores.objects.create(
            Clave = formatoClave,  Descripcion=nombre, IDEstatus_id = estatus
        )
        agregarDatosTecnicos(request, Tecnico_v, NombreTabla_v, IDFilaTabla_v, AreaRegistro_v, IDFila_v)
        messages.success(request, f'El Operador {nombre} se ha registrado exitosamente')


    if request.method == 'POST':
        if 'salir' in request.POST:
            return redirect('T-Operador')
        elif 'agregar' in request.POST:
            return redirect('F-Operador')
    else:
        return redirect('T-Operador')   

# -----------------------------------------------------MATERIAS PRIMAS-----------------------------------------------------
def guardarMateriasPrimas(request):
    clave = request.POST['clave']
    descripcion = request.POST['descripcion'].upper()
    precio = request.POST['precio']
    merma = request.POST['merma']
    estatus = request.POST['estatus']
    unidad = request.POST['unidad']

    clave_int = int(clave)
    formatoClave = 'F-{:06d}'.format(clave_int)

    # tecnicos
    Tecnico_v = request.POST['tecnico'].upper()
    NombreTabla_v = 'Materia Prima'
    IDFilaTabla_v = formatoClave
    AreaRegistro_v = 'Catalogos'
    IDFila_v = clave

    existente = tblMateriaPrima.objects.filter(Descripcion=descripcion).exists()
    if existente:
        errorCol = 'error'
        FEstatus=tblEstatus.objects.all()
        FUnidadMedida=tblUnidades.objects.all()
        messages.error(request, f'La Materia Prima {descripcion} ya ha sido registrado antreriormente')
        columnas = {'clave':clave, 'FEstatus':FEstatus,'FUnidadMedida':FUnidadMedida,'errorCol':errorCol}
        return render(request, "Catalogos/Materia Prima/form.html", columnas)
    else:
        tblMateriaPrima.objects.create(
            Clave = formatoClave, Descripcion = descripcion, IDEstatus_id = estatus, 
            IDUnidadMedida_id = unidad, PrecioUnitario = precio, Merma = merma
        )
        agregarDatosTecnicos(request, Tecnico_v, NombreTabla_v, IDFilaTabla_v, AreaRegistro_v, IDFila_v)
        messages.success(request, f'La Materia Prima {descripcion} se ha registrado exitosamente')

        cambios = True
        eventos_tabla = tblEventosValmoSys.objects.get(ID = 1)
        eventos_tabla.MateriaPrima = cambios
        eventos_tabla.save()

    if request.method == 'POST':
        if 'salir' in request.POST:
            return redirect('T-MateriaPrima')
        elif 'agregar' in request.POST:
            return redirect('F-MateriaPrima')
    else:
        return redirect('T-MateriaPrima')   

# --------------------------------------------------------PRODUCTOS--------------------------------------------------------
def guardarProductos(request):
    clave = request.POST['clave']
    descripcion = request.POST['descripcion'].upper()
    precio = request.POST['precio']
    seSirve = request.POST['seSirve']
    estatus = request.POST['estatus']
    unidad = request.POST['unidad']

    clave_int = int(clave)
    formatoClave = 'F-{:06d}'.format(clave_int)

    # tecnicos
    Tecnico_v = request.POST['tecnico'].upper()
    NombreTabla_v = 'Producto'
    IDFilaTabla_v = formatoClave
    AreaRegistro_v = 'Catalogos'
    IDFila_v = clave

    existente = tblProductos.objects.filter(Descripcion=descripcion).exists()
    if existente:
        errorCol = 'error'
        FEstatus=tblEstatus.objects.all()
        FUnidadMedida=tblUnidades.objects.all()
        messages.error(request, f'El Producto {descripcion} ya ha sido registrado antreriormente')
        columnas = {'clave':clave, 'errorCol':errorCol, 'FEstatus':FEstatus,'FUnidadMedida':FUnidadMedida}
        return render(request, "Catalogos/Producto/form.html", columnas)
    else:
        tblProductos.objects.create(
            Clave = formatoClave, Descripcion = descripcion, IDEstatus_id = estatus, 
            IDUnidadMedida_id = unidad, PrecioUnitario = precio, SeSirve = seSirve
        )
        agregarDatosTecnicos(request, Tecnico_v, NombreTabla_v, IDFilaTabla_v, AreaRegistro_v, IDFila_v)
        messages.success(request, f'El Producto {descripcion} se ha registrado exitosamente')

        cambios = True
        eventos_tabla = tblEventosValmoSys.objects.get(ID = 1)
        eventos_tabla.Productos = cambios
        eventos_tabla.save()

    if request.method == 'POST':
        if 'salir' in request.POST:
            return redirect('T-Producto')
        elif 'agregar' in request.POST:
            return redirect('F-Producto')
    else:
        return redirect('T-Producto')

# -------------------------------------------------MOVIMIENTOS DE ANIMALES-------------------------------------------------
def guardarRecetas(request):
    clave = request.POST['clave']
    clave_int = int(clave)
    formatoClave = 'F-{:06d}'.format(clave_int)
 
    AgRecetas = tblProductos.objects.get(ID=clave)
    ClaveProducto = AgRecetas.Clave
    Estatus = AgRecetas.IDEstatus.ID
    Unidad = AgRecetas.IDUnidadMedida.ID
    FiltradoEstatus = tblEstatus.objects.get(ID=Estatus)
    FiltradoUnidad = tblUnidades.objects.get(ID=Unidad)
    FMateriaPrima = tblMateriaPrima.objects.all().order_by('Descripcion')
    Recetas = tblProductosMateriaPrima.objects.filter(Folio=ClaveProducto).values('ID', 'Folio',
    'IDMateriaPrima_id__Descripcion', 'Merma', 'Porcentaje')
    proporcion = request.POST['proporcion']
    merma = request.POST['merma']
    materia = request.POST['materia']

    ultimo_id = tblProductosMateriaPrima.objects.order_by('-ID').first()
    if ultimo_id:
        ultimo_folio = ultimo_id.ID + 1
    else:
        ultimo_folio = 1
    # tecnicos
    Tecnico_v = request.POST['tecnico'].upper()
    NombreTabla_v = 'Receta Producto'
    IDFilaTabla_v = ClaveProducto
    AreaRegistro_v = 'Catalogos'
    IDFila_v = ultimo_folio

    print(ClaveProducto)
    tblProductosMateriaPrima.objects.create(
        Folio = ClaveProducto, IDMateriaPrima_id = materia, Porcentaje = proporcion, Merma = merma, 
        IDProductos_id = clave
    )
    agregarDatosTecnicos(request, Tecnico_v, NombreTabla_v, IDFilaTabla_v, AreaRegistro_v, IDFila_v)
    messages.success(request, f'Se ha agregado exitosamente la receta')

    cambios = True
    eventos_tabla = tblEventosValmoSys.objects.get(ID = 1)
    eventos_tabla.Recetas = cambios
    eventos_tabla.save()
    
    # Filtra los registros basados en IDProductos y suma la columna 'Porcentaje'
    total_porcentaje = tblProductosMateriaPrima.objects.filter(IDProductos=clave_int).aggregate(Sum('Porcentaje'))


    # Verifica si el valor de la suma es None y maneja ese caso
    if total_porcentaje['Porcentaje__sum'] is None:
        total = 0
    else:
        total = total_porcentaje['Porcentaje__sum']

    print(total)
    if request.method == 'POST':
        if 'salir' in request.POST:
            return redirect('T-Producto')
        elif 'agregar' in request.POST:
            return render(request, "Catalogos/Producto/agregar.html", {'formatoClave':formatoClave, 'total':total,
            'Recetas':Recetas,'AgRecetas': AgRecetas,'FiltradoEstatus':FiltradoEstatus, 'FiltradoUnidad':FiltradoUnidad,
            'FMateriaPrima':FMateriaPrima })
    else:
        return redirect('T-Producto')
    
# --------------------------------------------------------CORRALES---------------------------------------------------------
def guardarCorrales(request):
    clave = request.POST['clave']
    descripcion = request.POST['descripcion'].upper()
    capacidad = request.POST['capacidad']
    cliente = request.POST['cliente']
    estatus = request.POST['estatus']
    fecha = request.POST['fecha']

    clave_int = int(clave)
    formatoClave = 'F-{:06d}'.format(clave_int)
    
    # tecnicos
    Tecnico_v = request.POST['tecnico'].upper()
    NombreTabla_v = 'Corral'
    IDFilaTabla_v = formatoClave
    AreaRegistro_v = 'Catalogos'
    IDFila_v = clave

    existente = tblCorrales.objects.filter(Descripcion=descripcion).exists()
    if existente:
        errorCol = 'error'
        FEstatus = tblEstatus.objects.all()
        FClientes = tblClientes.objects.exclude(Nombre__icontains =  'Liberado').all()
        FechaDeHoy = date.today().strftime('%Y-%m-%d') 
        messages.error(request, f'El Corral {descripcion} ya ha sido registrado antreriormente')
        columnas = {'clave':clave,'FEstatus':FEstatus,'FClientes':FClientes,'FechaDeHoy':FechaDeHoy,'errorCol':errorCol}
        return render(request, "Catalogos/Corral/form.html", columnas)
    else:
        tblCorrales.objects.create(
            Clave = formatoClave, Descripcion = descripcion, IDCliente_id = cliente, 
            IDEstatus_id = estatus, Capacidad = capacidad, FechaAsigna = fecha
        )
        agregarDatosTecnicos(request, Tecnico_v, NombreTabla_v, IDFilaTabla_v, AreaRegistro_v, IDFila_v)
        messages.success(request, f'El Corral {descripcion} se ha registrado exitosamente')

    if request.method == 'POST':
        if 'salir' in request.POST:
            return redirect('T-Corral')
        elif 'agregar' in request.POST:
            return redirect('F-Corral')
    else:
        return redirect('T-Corral')  

# ------------------------------------------------------TIPO ANIMALES------------------------------------------------------
def guardarTipoAnimales(request):
    clave = request.POST['clave']
    nombre = request.POST['descripcion'].upper()
    estatus = request.POST['estatus']

    clave_int = int(clave)
    formatoClave = 'F-{:06d}'.format(clave_int)

    # tecnicos
    Tecnico_v = request.POST['tecnico'].upper()
    NombreTabla_v = 'Tipo Animal'
    IDFilaTabla_v = formatoClave
    AreaRegistro_v = 'Catalogos'
    IDFila_v = clave
    
    existente = tblAnimalesTipo.objects.filter(Descripcion=nombre).exists()
    if existente:
        errorCol = 'error'
        FEstatus = tblEstatus.objects.all()
        messages.error(request, f'El Tipo Animal {nombre} ya ha sido registrado antreriormente')
        columnas = {'clave': clave, 'errorCol':errorCol, 'FEstatus':FEstatus}
        return render(request, "Catalogos/Tipo Animal/form.html", columnas)
    else:
        tblAnimalesTipo.objects.create(
            Clave = formatoClave, Descripcion=nombre, IDEstatus_id = estatus
        )
        agregarDatosTecnicos(request, Tecnico_v, NombreTabla_v, IDFilaTabla_v, AreaRegistro_v, IDFila_v)
        messages.success(request, f'El Tipo Animal {nombre} se ha registrado exitosamente')

    if request.method == 'POST':
        if 'salir' in request.POST:
            return redirect('T-TipoAnimal')
        elif 'agregar' in request.POST:
            return redirect('F-TipoAnimal')
    else:
        return redirect('T-TipoAnimal')

# ----------------------------------------------CONTENEDORES MATERIAS PRIMAS-----------------------------------------------
def guardarContenedoresMateriasPrimas(request):
    clave = request.POST['clave']
    cliente = request.POST['cliente']
    capacidad = request.POST['capacidad']
    estatus = request.POST['estatus']

    clave_int = int(clave)
    formatoClave = 'F-{:06d}'.format(clave_int)

    # tecnicos
    Tecnico_v = request.POST['tecnico'].upper()
    NombreTabla_v = 'Contenedor Materia Prima'
    IDFilaTabla_v = formatoClave
    AreaRegistro_v = 'Catalogos'
    IDFila_v = clave

    cliente_Existente = tblClientes.objects.get(ID=cliente)
    cliente_Nombre = cliente_Existente.Nombre 
    tblContenedoresMateriaPrima.objects.create(
        Clave = formatoClave,  IDEstatus_id = estatus, 
        Capacidad = capacidad, IDCliente_id = cliente, Cliente = cliente_Nombre
    )   
    agregarDatosTecnicos(request, Tecnico_v, NombreTabla_v, IDFilaTabla_v, AreaRegistro_v, IDFila_v)
    messages.success(request, f'El Contenedor Materia Prima  se ha registrado exitosamente')

    if request.method == 'POST':
        if 'salir' in request.POST:
            return redirect('T-ContenedorMP')
        elif 'agregar' in request.POST:
            return redirect('F-ContenedorMP')
    else:
        return redirect('T-ContenedorMP')

# -------------------------------------------------CONTENEDORES PRODUCTOS--------------------------------------------------
def guardarContenedoresProductos(request):
    clave = request.POST['clave']
    cliente = request.POST['cliente']
    capacidad = request.POST['capacidad']
    estatus = request.POST['estatus']

    clave_int = int(clave)
    formatoClave = 'F-{:06d}'.format(clave_int)
    
    # tecnicos
    Tecnico_v = request.POST['tecnico'].upper()
    NombreTabla_v = 'Contenedor Producto'
    IDFilaTabla_v = formatoClave
    AreaRegistro_v = 'Catalogos'
    IDFila_v = clave

    proveedor_Existente = tblProveedores.objects.get(ID=cliente)
    proveedor_Nombre = proveedor_Existente.Nombre 
    tblContenedoresProductos.objects.create(
        Clave = formatoClave,  IDCliente_id = cliente, IDEstatus_id = estatus, Capacidad = capacidad,
        Proveedor = proveedor_Nombre
    )
    agregarDatosTecnicos(request, Tecnico_v, NombreTabla_v, IDFilaTabla_v, AreaRegistro_v, IDFila_v)
    messages.success(request, f'El Contenedor Productos se ha registrado exitosamente')

    if request.method == 'POST':
        if 'salir' in request.POST:
            return redirect('T-ContenedorProducto')
        elif 'agregar' in request.POST:
            return redirect('F-ContenedorProducto')
    else:
        return redirect('T-ContenedorProducto')

# ------------------------------------------------------TIPO ANIMALES------------------------------------------------------
def guardarTolva(request):
    clave = request.POST['clave']
    alias = request.POST['alias'].upper()
    marca = request.POST['marca'].upper()
    modelo = request.POST['modelo'].upper()
    capacidad = request.POST['capacidad']
    estatus = request.POST['estatus']
    producto = request.POST['producto']
    unidad = request.POST['unidad']
    
    
    clave_int = int(clave)
    formatoClave = 'F-{:06d}'.format(clave_int)

    # tecnicos
    Tecnico_v = request.POST['tecnico'].upper()
    NombreTabla_v = 'Tolva'
    IDFilaTabla_v = formatoClave
    AreaRegistro_v = 'Catalogos'
    IDFila_v = clave
    
    existente = tblTolva.objects.filter(Alias=alias).exists()
    if existente:
        errorCol = 'error'
        FEstatus = tblEstatus.objects.all()
        FUnidadMedida=tblUnidades.objects.all()
        messages.error(request, f'La tolva {alias} ya ha sido registrado antreriormente')
        columnas = {'clave': clave, 'errorCol':errorCol, 'FUnidadMedida':FUnidadMedida}
        return render(request, "Catalogos/Tolva/form.html", columnas)
    else:
        tblTolva.objects.create(
            Clave = formatoClave, Marca=marca, Modelo = modelo,
            Capacidad = capacidad, Alias=alias, IDEstatus_id = estatus, 
            IDProducto_id = producto, UdeM_id = unidad
        )
        agregarDatosTecnicos(request, Tecnico_v, NombreTabla_v, IDFilaTabla_v, AreaRegistro_v, IDFila_v)
        messages.success(request, f'La tolva {alias} se ha registrado exitosamente')

    if request.method == 'POST':
        if 'salir' in request.POST:
            return redirect('T-Tolva')
        elif 'agregar' in request.POST:
            return redirect('F-Tolva')
    else:
        return redirect('T-Tolva')
