from django.shortcuts import redirect, render
from django.contrib import messages
# LLAMAR ARCHIVOS LOCALES
from django.db.models import Q
from Aplicacion.forms import *
from Aplicacion.models import *
from Aplicacion.views import editarDatosTecnicos
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< ACTUALIZAR DATOS CATALOGOS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# --------------------------------------------------------CLIENTES---------------------------------------------------------
def actualizarCliente(request):
    id = request.POST['id']
    clave = request.POST['clave']
    nombre = request.POST['nombre'].upper().strip()
    contacto = request.POST['contacto'].strip()
    direccion = request.POST['direccion'].strip()
    ciudad = request.POST['ciudad'].upper().strip()
    rfc = request.POST['rfc'].upper().strip()
    email = request.POST['email'].strip()
    telefono = request.POST['telefono'].strip()

    # tecnicos
    TecnicoEditor_v = request.POST['tecnico'].upper()
    NombreTabla_v = 'Cliente'
    IDFilaTabla_v = id


    nombre_existente = tblClientes.objects.filter(Nombre=nombre).exclude(ID=id).exists()
    if nombre_existente:
        messages.error(request, f'El Cliente "{nombre}" ya ha sido registrado anteriormente.')
        IDNumber = int(id)
        return redirect('E-Cliente', IDNumber)
    else:
        cliente = tblClientes.objects.get(ID=id)
        cliente.Nombre = nombre
        cliente.Contacto = contacto
        cliente.Direccion = direccion
        cliente.Ciudad = ciudad
        cliente.RFC = rfc
        cliente.Email = email
        cliente.TelefonoContacto = telefono
        cliente.save()
        try:
            editarDatosTecnicos(request, TecnicoEditor_v, NombreTabla_v, IDFilaTabla_v)
        except Exception as e:
            print(e)
        messages.success(request, f'El Cliente "{nombre}" se ha actualizado exitosamente.')

    return redirect('T-Cliente')

# -------------------------------------------------------PROVEEDORES-------------------------------------------------------
def actualizarProveedor(request):
    id = request.POST['id']
    clave = request.POST['clave']
    nombre = request.POST['nombre'].upper().strip()
    contacto = request.POST['contacto'].strip()
    direccion = request.POST['direccion'].strip()
    ciudad = request.POST['ciudad'].upper().strip()
    rfc = request.POST['rfc'].upper().strip()
    email = request.POST['email'].strip()
    telefono = request.POST['telefono'].strip()

    # tecnicos
    TecnicoEditor_v = request.POST['tecnico'].upper()
    NombreTabla_v = 'Proveedor'
    IDFilaTabla_v = id

    nombre_existente = tblProveedores.objects.filter(Nombre=nombre).exclude(ID=id).exists()
    if nombre_existente:
        messages.error(request, f'El Proveedor "{nombre}" ya ha sido registrado anteriormente.')
        IDNumber = int(id)
        return redirect('E-Proveedor', IDNumber)
    else:
        proveedor = tblProveedores.objects.get(ID=id)
        proveedor.Nombre = nombre
        proveedor.Contacto = contacto
        proveedor.Direccion = direccion
        proveedor.Ciudad = ciudad
        proveedor.RFC = rfc
        proveedor.Email = email
        proveedor.TelefonoContacto = telefono
        proveedor.save()
        try:
            editarDatosTecnicos(request, TecnicoEditor_v, NombreTabla_v, IDFilaTabla_v)
        except Exception as e:
            print(e)
        messages.success(request, f'El Proveedor "{nombre}" se ha actualizado exitosamente.')
    return redirect('T-Proveedor')

# -------------------------------------------------------OPERADORES--------------------------------------------------------
def actualizarOperador(request):
    id = request.POST['id']
    clave = request.POST['clave']
    descripcion = request.POST['operador'].upper().strip()
    estatus = request.POST['estatus']

    # tecnicos
    TecnicoEditor_v = request.POST['tecnico'].upper()
    NombreTabla_v = 'Operador'
    IDFilaTabla_v = id

    operador_existente = tblOperadores.objects.filter(Descripcion=descripcion).exclude(ID=id).exists()
    if operador_existente:
        messages.error(request, f'El Operador "{descripcion}" ya ha sido registrado anteriormente.')
        IDNumber = int(id)
        return redirect('E-Operador', IDNumber)
    else:
        operador = tblOperadores.objects.get(ID=id)
        Estatus_instancia = tblEstatus.objects.get(ID=estatus)

        operador.Descripcion = descripcion
        operador.IDEstatus = Estatus_instancia
        operador.save()
        try:
            editarDatosTecnicos(request, TecnicoEditor_v, NombreTabla_v, IDFilaTabla_v)
        except Exception as e:
            print(e)
        messages.success(request, f'El Operador "{descripcion}" se ha actualizado exitosamente.')
    return redirect('T-Operador')

# -----------------------------------------------------MATERIAS PRIMAS-----------------------------------------------------
def actualizarMateriaPrima(request):
    id = request.POST['id']
    clave = request.POST['clave']
    materia_v = request.POST['materia'].upper().strip()
    precio_v = request.POST['precio']
    merma_v = request.POST['merma']
    estatus_v = request.POST['estatus']
    unidad_v = request.POST['unidad']

    # tecnicos
    TecnicoEditor_v = request.POST['tecnico'].upper()
    NombreTabla_v = 'Materia Prima'
    IDFilaTabla_v = id

    materia_existente = tblMateriaPrima.objects.filter(Descripcion=materia_v).exclude(ID=id).exists()
    if materia_existente:
        messages.error(request, f'La Materia Prima "{materia_v}" ya ha sido registrado anteriormente.')
        IDNumber = int(id)
        return redirect('E-Materia-Prima', IDNumber)
    else:
        mateira_prima = tblMateriaPrima.objects.get(ID=id)
        Estatus_instancia = tblEstatus.objects.get(ID=estatus_v)
        Unidad_instancia = tblUnidades.objects.get(ID=unidad_v)

        mateira_prima.Descripcion = materia_v
        mateira_prima.PrecioUnitario = precio_v
        mateira_prima.Merma = merma_v
        mateira_prima.IDEstatus = Estatus_instancia
        mateira_prima.IDUnidadMedida = Unidad_instancia
        mateira_prima.save()
        try:
            editarDatosTecnicos(request, TecnicoEditor_v, NombreTabla_v, IDFilaTabla_v)
        except Exception as e:
            print(e)
        messages.success(request, f'La Materia Prima "{materia_v}" se ha actualizado exitosamente.')
        cambios = True
        eventos_tabla = tblEventosValmoSys.objects.get(ID = 1)
        eventos_tabla.MateriaPrima = cambios
        eventos_tabla.save()        
    return redirect('T-MateriaPrima')

# --------------------------------------------------------PRODUCTOS--------------------------------------------------------
def actualizarProductos(request):
    id = request.POST['id']
    clave = request.POST['clave']
    producto_v = request.POST['producto'].upper().strip()
    precio_v = request.POST['precio']
    estatus_v = request.POST['estatus']
    unidad_v = request.POST['unidad']
    seSirve_v = request.POST['seSirve']

    # tecnicos
    TecnicoEditor_v = request.POST['tecnico'].upper()
    NombreTabla_v = 'Producto'
    IDFilaTabla_v = id

    producto_existente = tblProductos.objects.filter(Descripcion=producto_v).exclude(ID=id).exists()
    if producto_existente:
        messages.error(request, f'El Producto "{producto_v}" ya ha sido registrado anteriormente.')
        IDNumber = int(id)
        return redirect('E-Producto', IDNumber)
    else:
        producto_save = tblProductos.objects.get(ID=id)
        Estatus_instancia = tblEstatus.objects.get(ID=estatus_v)
        Unidad_instancia = tblUnidades.objects.get(ID=unidad_v)

        producto_save.Descripcion = producto_v
        producto_save.PrecioUnitario = precio_v
        producto_save.SeSirve = seSirve_v
        producto_save.IDEstatus = Estatus_instancia
        producto_save.IDUnidadMedida = Unidad_instancia
        producto_save.save()
        try:
            editarDatosTecnicos(request, TecnicoEditor_v, NombreTabla_v, IDFilaTabla_v)
        except Exception as e:
            print(e)
        messages.success(request, f'El Producto "{producto_v}" se ha actualizado exitosamente.')
        cambios = True
        eventos_tabla = tblEventosValmoSys.objects.get(ID = 1)
        eventos_tabla.Productos = cambios
        eventos_tabla.save()        
    return redirect('T-Producto')

# -------------------------------------------RECETAS DE PRODUCTOS----------------------------------------------------
def actualizarRecetasProductos(request):
    id = request.POST['id']
    folio_v = request.POST['folio']
    materia_v = request.POST['materia']
    proporcion_v = request.POST['proporcion']
    merma_v = request.POST['merma']
    producto_v = request.POST['producto']

    # tecnicos
    TecnicoEditor_v = request.POST['tecnico'].upper()
    NombreTabla_v = 'Receta Producto'
    IDFilaTabla_v = id
    
    recetas = tblProductosMateriaPrima.objects.get(ID=id)
    materia_instancia = tblMateriaPrima.objects.get(ID=materia_v)
   
    recetas.IDMateriaPrima = materia_instancia
    recetas.Porcentaje = proporcion_v
    recetas.Merma = merma_v
    recetas.save()
    try:
        editarDatosTecnicos(request, TecnicoEditor_v, NombreTabla_v, IDFilaTabla_v)
    except Exception as e:
        print(e)
    messages.success(request, f'La receta "{folio_v}" se ha actualizado exitosamente.')
    cambios = True
    eventos_tabla = tblEventosValmoSys.objects.get(ID = 1)
    eventos_tabla.Recetas = cambios
    eventos_tabla.save()
    return redirect('D-Producto', ID=producto_v)
# --------------------------------------------------------CORRALES---------------------------------------------------------
def actualizarCorral(request):
    id = request.POST['id']
    clave = request.POST['clave']
    corral_v = request.POST['corral'].upper().strip()
    capacidad_v = request.POST['capacidad']
    cliente_v = request.POST['cliente']
    estatus_v = request.POST['estatus']
    fecha_v = request.POST['fecha']

    # tecnicos
    TecnicoEditor_v = request.POST['tecnico'].upper()
    NombreTabla_v = 'Corral'
    IDFilaTabla_v = id
    
    corral_existente = tblCorrales.objects.filter(Descripcion=corral_v).exclude(ID=id).exists()
    if corral_existente:
        messages.error(request, f'El Corral "{corral_v}" ya ha sido registrado anteriormente.')
        IDNumber = int(id)
        return redirect('E-Corral', IDNumber)
    else:
        corral_save = tblCorrales.objects.get(ID=id)
        Estatus_instancia = tblEstatus.objects.get(ID=estatus_v)
        Cliente_instancia = tblClientes.objects.get(ID=cliente_v)

        corral_save.Clave = clave
        corral_save.Descripcion = corral_v
        corral_save.Capacidad = capacidad_v
        corral_save.FechaAsigna = fecha_v
        corral_save.IDEstatus = Estatus_instancia
        corral_save.IDCliente = Cliente_instancia
        corral_save.save()
        
        # Servidos_instancias = tblServido.objects.filter(Q(IDCorral_id=id) & (Q(IDEstatus_id=3) | Q(IDEstatus_id=8)))
        # for servido_instancia in Servidos_instancias:
        #     servido_instancia.IDCliente = Cliente_instancia
        #     servido_instancia.save()
        try:
            editarDatosTecnicos(request, TecnicoEditor_v, NombreTabla_v, IDFilaTabla_v)
        except Exception as e:
            print(e)

        messages.success(request, f'El Corral "{corral_v}" se ha actualizado exitosamente.')
    return redirect('T-Corral')

# ------------------------------------------------------TIPO ANIMALES------------------------------------------------------
def actualizarTipoAnimales(request):
    id = request.POST['id']
    clave = request.POST['clave']
    descripcion_v = request.POST['descripcion'].upper().strip()
    estatus_v = request.POST['estatus']

    # tecnicos
    TecnicoEditor_v = request.POST['tecnico'].upper()
    NombreTabla_v = 'Tipo Animal'
    IDFilaTabla_v = id
    
    animales_existente = tblAnimalesTipo.objects.filter(Descripcion=descripcion_v).exclude(ID=id).exists()
    if animales_existente:
        messages.error(request, f'El Animal "{descripcion_v}" ya ha sido registrado anteriormente.')
        IDNumber = int(id)
        return redirect('E-Tipo-Animal', IDNumber)
    else:
        animales_save = tblAnimalesTipo.objects.get(ID=id)
        Estatus_instancia = tblEstatus.objects.get(ID=estatus_v)

        animales_save.Descripcion = descripcion_v
        animales_save.IDEstatus = Estatus_instancia
        animales_save.save()
        try:
            editarDatosTecnicos(request, TecnicoEditor_v, NombreTabla_v, IDFilaTabla_v)
        except Exception as e:
            print(e)
        messages.success(request, f'El Animal "{descripcion_v}" se ha actualizado exitosamente.')
    return redirect('T-TipoAnimal')

# ----------------------------------------------CONTENEDORES MATERIAS PRIMAS-----------------------------------------------
def actualizarContenedoresMP(request):
    id = request.POST['id']
    clave = request.POST['clave']
    cliente_v = request.POST['cliente']
    estatus_v = request.POST['estatus']
    capacidad_v = request.POST['capacidad']
   
    # tecnicos
    TecnicoEditor_v = request.POST['tecnico'].upper()
    NombreTabla_v = 'Contenedor Materia Prima'
    IDFilaTabla_v = id

    contenedorMP_save = tblContenedoresMateriaPrima.objects.get(ID=id)
    Cliente_instancia = tblClientes.objects.get(ID=cliente_v)
    Cliente=Cliente_instancia.Nombre
    Estatus_instancia = tblEstatus.objects.get(ID=estatus_v)

    contenedorMP_save.IDCliente = Cliente_instancia
    contenedorMP_save.IDEstatus = Estatus_instancia
    contenedorMP_save.Capacidad = capacidad_v
    contenedorMP_save.Cliente = Cliente
    contenedorMP_save.save()
    try:
        editarDatosTecnicos(request, TecnicoEditor_v, NombreTabla_v, IDFilaTabla_v)
    except Exception as e:
        print(e)
    messages.success(request, f'El Contenedor de Materia Prima se ha actualizado exitosamente.')
    return redirect('T-ContenedorMP')

# -------------------------------------------------CONTENEDORES PRODUCTOS--------------------------------------------------
def actualizarContenedoresProductos(request):
    id = request.POST['id']
    clave = request.POST['clave']
    cliente_v = request.POST['cliente']
    estatus_v = request.POST['estatus']
    capacidad_v = request.POST['capacidad']
   
    # tecnicos
    TecnicoEditor_v = request.POST['tecnico'].upper()
    NombreTabla_v = 'Contenedor Producto'
    IDFilaTabla_v = id

    contenedorProductos_save = tblContenedoresProductos.objects.get(ID=id)
    Cliente_instancia = tblProveedores.objects.get(ID=cliente_v)
    Proveedor = Cliente_instancia.Nombre
    Estatus_instancia = tblEstatus.objects.get(ID=estatus_v)
    
    contenedorProductos_save.IDCliente = Cliente_instancia
    contenedorProductos_save.IDEstatus = Estatus_instancia
    contenedorProductos_save.Capacidad = capacidad_v
    contenedorProductos_save.Proveedor = Proveedor
    contenedorProductos_save.save()
    try:
        editarDatosTecnicos(request, TecnicoEditor_v, NombreTabla_v, IDFilaTabla_v)
    except Exception as e:
        print(e)
    messages.success(request, f'El Contenedor de Productos se ha actualizado exitosamente.')
    return redirect('T-ContenedorProducto')

# ------------------------------------------------------TIPO ANIMALES------------------------------------------------------
def actualizarTolva(request):
    id = request.POST['id']
    clave = request.POST['clave']
    alias = request.POST['alias'].upper()
    marca = request.POST['marca'].upper()
    modelo = request.POST['modelo'].upper()
    capacidad = request.POST['capacidad']
    estatus = request.POST['estatus']
    unidad = request.POST['unidad']

    # tecnicos
    TecnicoEditor_v = request.POST['tecnico'].upper()
    NombreTabla_v = 'Tolva'
    IDFilaTabla_v = id
    
    tolva_existente = tblTolva.objects.filter(Alias=alias).exclude(ID=id).exists()
    if tolva_existente:
        messages.error(request, f'La tolva "{alias}" ya ha sido registrado anteriormente.')
        IDNumber = int(id)
        return redirect('E-Tolva', IDNumber)
    else:
        tolva_save = tblTolva.objects.get(ID=id)
        Estatus_instancia = tblEstatus.objects.get(ID=estatus)
        Unidades_instancia = tblUnidades.objects.get(ID=unidad)

        tolva_save.Alias = alias
        tolva_save.Marca = marca
        tolva_save.Modelo = modelo
        tolva_save.Capacidad = capacidad
        tolva_save.IDEstatus = Estatus_instancia
        tolva_save.UdeM = Unidades_instancia
        
        tolva_save.save()
        try:
            editarDatosTecnicos(request, TecnicoEditor_v, NombreTabla_v, IDFilaTabla_v)
        except Exception as e:
            print(e)
        messages.success(request, f'La tolva "{alias}" se ha actualizado exitosamente.')
    return redirect('T-Tolva')