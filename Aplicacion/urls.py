from django.urls import path
from . import views
from Aplicacion.CRUD import actualizarCatalogos, actualizarProcesos, actualizarSubTabla
from Aplicacion.CRUD import formularioCatalogos, formularioProcesos, formularioSubTabla
from Aplicacion.CRUD import mostrarCatalogos, mostrarProcesos, mostrarSubTabla
from Aplicacion.CRUD import guardarCatalogos, guardarProcesos, guardarSubTabla
from Aplicacion.CRUD import editarCatalogos, editarProcesos, editarSubTabla
from Aplicacion.CRUD import reportes, DescargaPDF, DescargaExcel, CopiaDeSeguridad, CopiaAMysql, cliente
from Aplicacion.CRUD import presentacion, Correo

# from .views import PDFView formularioCatalogos
from django.contrib.auth.views import LoginView, LogoutView
from .views import CustomLoginView
# La F = Formulario
# La T =  Tabla
# La G = Guardar Formulario


urlpatterns = [
     #  Presentacion
    path('Servidos_presentacion/', presentacion.presentacionServidos, name='Servidos_Presentacion'),
    path('Bascula_presentacion/', presentacion.presentacionBascula, name='Bascula_Presentacion'),
    path('Invenario_presentacion/', presentacion.presentacionInventario, name='Inventario_Presentacion'),
     
    # Vistas para el cliente
    path('Agregar_Servidos_Cliente/', cliente.formulario, name='FP-Cliente'),
    path('Ver_Servidos_Cliente/', cliente.servidos, name='FP-Servidos-Cliente'),
    path('Guardar_Servidos_Cliente/', cliente.guardarSolicitudServidoCliente, name='GS-Cliente'),
    path('Resultados_Cliente/', cliente.cliente, name='Cliente'),

    # vistas de inicio
    path('', views.home, name='Inicio'),
    path('Inicio/', views.sistema, name='Sistema'),

    # Respaldo en base de datos
    path('Copia_de_seguridad/', CopiaDeSeguridad.copiaDeSeguridad, name='Copia'),
    path('Descargar_copia_de_seguridad/',
         CopiaDeSeguridad.descargar_backup, name='Descargar-SQLite3'),
    path('Importar_SQLite3_A_Mysql/',
         CopiaAMysql.import_data, name='SQLite3-A-Mysql'),

    # USUARIOS LOGIN, REGISTER O LOGOUT
    path('Logout/', LogoutView.as_view(template_name='Acceso/logout.html'), name='Logout'),
    path('Login/', CustomLoginView.as_view(), name='Login'),
    path('Register/', views.Register, name='Register'),

    # PAGOS
    path('Estado-Pago/', views.estadoPago, name='Pagos'),
    path('No-Hay-Servicio/', views.NoPago, name='NoPago'),
    path('SeAgregoElPago/', views.registrarPago),
    path('Notificaciones/', views.notificacion),

    # USUARIOS
    path('Perfil/', views.perfil, name='perfil'),
    path('Usuarios/', views.TablaUsuarios, name='TUsuarios'),
    path('Agregar-Tecnicos/', views.agregarTecnicos, name='Agregar-tecnicos'),
    path('Editar-Tecnicos/', views.editadoTecnicos, name='Editar-tecnicos'),
    path('Usuario-Bloqueado/', views.usuarioBloqueado, name='Bloqueado'),

    # GRUPOS
    path('Formulario-Grupos/', views.FormularioGrupos, name='F-Grupos'),
    path('Guardar-Grupos/', views.agregarGrupos),
    path('Datos-Grupos/', views.TablaGrupos, name='T-Grupos'),
    path('Datos-Grupos/Editar/<ID>', views.editarGrupos),
    path('ActualizarGrupo/', views.actualizarGrupo),
    path('Permisos/Editar/<ID>', views.editarPermisos),
    path('Movimiento-Permisos/', views.TablaPermisosAsignaElimina,
         name='T-PermisoAsignadosEliminados'),
    path('Permisos/', views.TablaPermisos, name='T-Permisos'),
    path('Tipos-De-Rol/', views.TablaTiposDeRol, name='T-Tipo-Rol'),
    path('ActualizarPermiso/', views.actualizarPermiso),

    # REPORTES
    path('Reportes/', views.reportes, name='Reportes'),

    # EDITAR USUARIOS
    path('Usuarios/EdicionUsuario/<id>', views.edicionUsuario),

    # ACTUALIZAR USUARIOS
    path('ActualizarUsuario/', views.actualizarUsuario),

    # FORMULARIO SUBTABLAS
    path('Formulario-Estatus/',
         formularioSubTabla.formularioEstatus, name='F-Estatus'),
    path('Formulario-Tipo-Material/',
         formularioSubTabla.formularioTipoMaterial, name='F-Tipo-Material'),
    path('Formulario-Tipo-Movimiento/',
         formularioSubTabla.formularioTipoMovimiento, name='F-Tipo-Movimiento'),
    path('Formulario-Tipo-Presentacion/',
         formularioSubTabla.formularioTipoPresentacion, name='F-Tipo-Presentacion'),
    path('Formulario-Unidad-Medida/',
         formularioSubTabla.formularioUnidadMedida, name='F-Unidad-Medida'),

    # FORMULARIO DE CATALOGOS
    path('Formulario-Cliente/',
         formularioCatalogos.FormualrioClientes, name='F-Cliente'),
    path('Formulario-Proveedor/',
         formularioCatalogos.FormualrioProveedores, name='F-Proveedor'),
    path('Formulario-Operador/',
         formularioCatalogos.FormualrioOperadores, name='F-Operador'),
    path('Formulario-Materia-Prima/',
         formularioCatalogos.FormualrioMateriasPrimas, name='F-MateriaPrima'),
    path('Formulario-Producto/',
         formularioCatalogos.FormualrioProductos, name='F-Producto'),
    path('Formulario-Corral/', formularioCatalogos.FormualrioCorrales, name='F-Corral'),
    path('Formulario-Tipo-Animal/',
         formularioCatalogos.FormualrioTipoAnimaless, name='F-TipoAnimal'),
    path('Formulario-Contenedor-Materia-Prima/',
         formularioCatalogos.FormualrioContnendoresMateriasPrimas, name='F-ContenedorMP'),
    path('Formulario-Contenedor-Producto/',
         formularioCatalogos.FormualrioContenedoresProductos, name='F-ContenedorProducto'),
    path('Formulario-Tolva/', formularioCatalogos.FormualrioTolva, name='F-Tolva'),

    # FORMULARIO DE PROCESOS
    path('Formulario-Entrada-Materia-Prima/',
         formularioProcesos.FormularioEntradaMateriasPrimas, name='F-Ent-Materia-Prima'),
    path('Formulario-Salida-Materia-Prima/',
         formularioProcesos.FormularioSalidaMateriasPrimas, name='F-Sal-Materia-Prima'),
    path('Formulario-Entrada-Producto/',
         formularioProcesos.FormularioEntradaProductos, name='F-Ent-Productos'),
    path('Formulario-Salida-Producto/',
         formularioProcesos.FormularioSalidaProductos, name='F-Sal-Productos'),
    path('Formulario-Movimientos-Animales/',
         formularioProcesos.FormularioMovimientoAnimales, name='F-MovAnimales'),
    path('Formulario-Detalles-Animales/',
         formularioProcesos.FormularioDetallesAnimales, name='F-DetallesAnimales'),
    path('Formulario-Solicitud-Servido/',
         formularioProcesos.FormularioSolicitudServido, name='F-Solicitud-Servidos'),
    path('Formulario-Servidos-Manuales/',
         formularioProcesos.FormularioServidoAnimales, name='F-Servidos'),
    path('Formulario-Inventario-Materia-Prima/',
         formularioProcesos.FormularioInventarioMateriaPrima, name="F-InventarioMP"),
    path('Formulario-Inventario-Productos/',
         formularioProcesos.FormularioInventarioProducto, name="F-InventarioProductos"),

    # FORMULARIO DE OPERADORES
    path('Dato-Operador-Entrada-Productos/Agregar/<str:ID>',
         formularioProcesos.FormularioOperadoresEntradaProductos, name="A-Operaror-Entrada-Producto"),
    path('Dato-Operador-Salida-Productos/Agregar/<str:ID>',
         formularioProcesos.FormularioOperadoresSalidaProductos, name="A-Operaror-Salida-Producto"),
    path('Dato-Operador-Entrada-Materias-Primas/Agregar/<str:ID>',
         formularioProcesos.FormularioOperadorEntradaMateriaPrima, name="A-Operaror-Entrada-Materia"),
    path('Dato-Operador-Salida-Materias-Primas/Agregar/<str:ID>',
         formularioProcesos.FormularioOperadorSalidaMateriaPrima, name="A-Operaror-Salida-Materia"),

    # SUBTABLA
    path('SubTabla-Estatus/', mostrarSubTabla.TablaEstatus, name='T-Estatus'),
    path('SubTabla-Tipo-Material/',
         mostrarSubTabla.TablaTipoMaterial, name='T-Tipo-Material'),
    path('SubTabla-Tipo-Movimiento/',
         mostrarSubTabla.TablaTipoMovimiento, name='T-Tipo-Movimiento'),
    path('SubTabla-Tipo-Presentacion/',
         mostrarSubTabla.TablaTipoPresentacion, name='T-Tipo-Presentacion'),
    path('SubTabla-Unidad-Medida/',
         mostrarSubTabla.TablaUnidadMedida, name='T-Unidad-Medida'),
    path('Base_de_datos/', mostrarSubTabla.TablaConfiguracion, name='Base-de-datos'),

    # TABLA DE CATALOGOS
    path('Dato-Cliente/', mostrarCatalogos.TablaClientes, name='T-Cliente'),
    path('Dato-Proveedor/', mostrarCatalogos.TablaProveedores, name='T-Proveedor'),
    path('Dato-Operador/', mostrarCatalogos.TablaOperadores, name='T-Operador'),
    path('Dato-Materia-Prima/', mostrarCatalogos.TablaMateriasPrimas,
         name='T-MateriaPrima'),
    path('Dato-Producto/', mostrarCatalogos.TablaProductos, name='T-Producto'),
    path('Dato-Producto/Agregar/<ID>',
         mostrarCatalogos.AgregarRecetas, name='A-Producto'),
    path('Dato-Producto/Detalle/<str:ID>',
         mostrarCatalogos.detalleRecetas, name='D-Producto'),
    path('Dato-Corral/', mostrarCatalogos.TablaCorrales, name='T-Corral'),
    path('Dato-Tipo-Animal/', mostrarCatalogos.TablaTipoAnimales, name='T-TipoAnimal'),
    path('Dato-Contenedor-Materia-Prima/',
         mostrarCatalogos.TablaContenedoresMateriasPrimas, name='T-ContenedorMP'),
    path('Dato-Contenedor-Producto/',
         mostrarCatalogos.TablaContenedoresProductos, name='T-ContenedorProducto'),
    path('Dato-Tolva/', mostrarCatalogos.TablaTolva, name='T-Tolva'),

    # TABLA DE PROCESOS
    path('Dato-Entrada-Materia-Prima/',
         mostrarProcesos.TablaEntradaMateriasPrimas, name='T-Ent-Materia-Prima'),
    path('Dato-Salida-Materia-Prima/',
         mostrarProcesos.TablaSalidaMateriasPrimas, name='T-Sal-Materia-Prima'),
    path('Dato-Entrada-Producto/',
         mostrarProcesos.TablaEntradaProductos, name='T-Ent-Productos'),
    path('Dato-Salida-Producto/',
         mostrarProcesos.TablaSalidaProductos, name='T-Sal-Productos'),
    path('Dato-Movimientos-Animales/',
         mostrarProcesos.TablaMovimientoAnimales, name='T-MovAnimales'),
    path('Dato-Movimientos-Animales/Agregar/<ID>',
         mostrarProcesos.AgregarMovimientoAnimales, name='A-MovAnimales'),
    path('Dato-Movimientos-Animales/Detalle/<str:ID>',
         mostrarProcesos.detalleAnimales, name='D-MovAnimales'),
    path('Dato-Detalles-Animales/', mostrarProcesos.TablaDetallesAnimales, name='T-DetallesAnimales'),
    path('Dato-Historial/',
         mostrarProcesos.TablaHistorialAsignacionCorral, name='T-Historial'),
    path('Dato-Inventario-Materia-Prima/',
         mostrarProcesos.TablaInventarioMateriaPrima, name="T-InventarioMP"),
    path('Dato-Inventario-Productos/',
         mostrarProcesos.TablaInventarioProducto, name="T-InventarioProductos"),

    # DATOS DEL AREA DE SERVIDOS
    path('Dato-Solicitud-Servidos/',
         mostrarProcesos.TablaSolicitudServido, name='T-Solicitud-Servidos'),
    path('Dato-Corrales-Servidos/', mostrarProcesos.TablaServidoCorral,
         name='T-Corrales-Servidos'),
    path('Dato-Consolidacion-Servido/',
         mostrarProcesos.TablaConsolidacionServido, name='T-Consolidacion'),
    path('Dato-Consolidacion-Servido/Filtro/Tolva/<str:ID>/<int:Estatus>/<int:Producto>/',
         mostrarProcesos.TablaTolvaServido),
    path('Dato-Consolidacion-Servido-Filtro/',
         mostrarProcesos.TablaFiltroServido, name='FT-Consolidacion'),
    path('Dato-Tolva-Servido/', mostrarProcesos.TablaTolva, name='T-Tolva-Servido'),
    path('Dato-Tolva-Servido-Se-Sirve/',
         mostrarProcesos.TablaTolvaServidoCorral, name='T-Se-Sirve'),
    path('Dato-Servidos-Manuales/',
         mostrarProcesos.TablaServidoAnimales, name='T-Servidos'),

    # DATOS DE LOS DATOS DE LA TOLVA
    path('Dato-Cargamento-Tolva/',
         mostrarProcesos.TablaCargamentoTolva, name='T-Cargamento-Tolva'),
    
    # DETALLES DE OPERADORES
    path('Dato-Operador-Entrada-Productos/',
         mostrarProcesos.TablaOperadoresEntradaProductos),
    path('Dato-Operador-Salida-Productos/',
         mostrarProcesos.TablaOperadoresSalidaProductos, name="E-Operador-Producto"),
    path('Dato-Operador-Entrada-Materias-Primas/',
         mostrarProcesos.TablaOperadoresEntradaMateriasPrimas),
    path('Dato-Operador-Salida-Materias-Primas/',
         mostrarProcesos.TablaOperadoresSalidasMateriasPrimas),

    # ASIGNACION CORRALES
    path('Asignacion-Corrales/',
         mostrarProcesos.asignacionCorral, name='T-Asignacion'),

    # TRAER CORRALES EN TIEMPO REAL
    path('obtener_corrales/<int:id>/', mostrarProcesos.obtener_corrales),
    path('obtener_clientes/<int:id>/', mostrarProcesos.obtener_clientes),
    path('obtener_corrales_clientes/<int:id>/', mostrarProcesos.obtener_corrales_animales_clientes),

    # FORMULARIO SUBTABLA
    path('Guardar-Estatus/', guardarSubTabla.guardarEstatus),
    path('Guardar-Tipo-Movimiento/', guardarSubTabla.guardarTipoMovimiento),
    path('Guardar-Tipo-Material/', guardarSubTabla.guardarTipoMaterial),
    path('Guardar-Tipo-Presentacion/', guardarSubTabla.guardarTipoPresentacion),
    path('Guardar-Unidades/', guardarSubTabla.guardarUnidadMedida),

    # FORMULARIO CATALOGOS
    path('Guardar-Cliente/', guardarCatalogos.guardarCliente),
    path('Guardar-Proveedor/', guardarCatalogos.guardarProveedor),
    path('Guardar-Operador/', guardarCatalogos.guardarOperador),
    path('Guardar-Materia-Prima/', guardarCatalogos.guardarMateriasPrimas),
    path('Guardar-Producto/', guardarCatalogos.guardarProductos),
    path('Guardar-Recetas/', guardarCatalogos.guardarRecetas),
    path('Guardar-Corral/', guardarCatalogos.guardarCorrales),
    path('Guardar-Tipo-Animal/', guardarCatalogos.guardarTipoAnimales),
    path('Guardar-Contenedor-Materia-Prima/',
         guardarCatalogos.guardarContenedoresMateriasPrimas),
    path('Guardar-Contenedor-Producto/',
         guardarCatalogos.guardarContenedoresProductos),
    path('Guardar-Tolva/', guardarCatalogos.guardarTolva),

    # FORMULARIO PROCESOS
    path('Guardar-Entrada-Materia-Prima/',
         guardarProcesos.guardarEntradaMateriaPrima),
    path('Guardar-Salidas-Materias-Primas/',
         guardarProcesos.guardarSalidasMateriaPrima),
    path('Guardar-Entradas-Productos/', guardarProcesos.guardarEntradaBasculas),
    path('Guardar-Salidas-Productos/', guardarProcesos.guardarSalidaBasculas),
    path('Guardar-Movimiento-De-Amimales/',
         guardarProcesos.guardarMovimientos),
    path('Guardar-Movimiento-Animales/',
         guardarProcesos.guardarMovimientoAniamles),
    path('Guardar-Solicitud-Servidos/', guardarProcesos.guardarSolicitudServido),
    path('Guardar-Servidos-Manual/', guardarProcesos.guardarServidosManuales),
    path('Guardar-Inventario-Materia-Prima/',
         guardarProcesos.guardarInventarioMateriaPrima),
    path('Guardar-Inventario-Productos/',
         guardarProcesos.guardarInventarioProductos),

    # SUBTABLA EDITAR
    path('SubTabla-Estatus/Editar/<ID>',
         editarSubTabla.editarEstatus, name="E-Estatus"),
    path('SubTabla-Tipo-Movimiento/Editar/<ID>',
         editarSubTabla.editarTipoMovimiento, name="E-Tipo-Movimiento"),
    path('SubTabla-Tipo-Material/Editar/<ID>',
         editarSubTabla.editarTipoMaterial, name="E-Tipo-Material"),
    path('SubTabla-Tipo-Presentacion/Editar/<ID>',
         editarSubTabla.editarTipoPresentacion, name="E-Tipo-Presentacion"),
    path('SubTabla-Unidad-Medida/Editar/<ID>',
         editarSubTabla.editarUnidadMedida, name="E-Unidad-Medida"),

    # EDITAR CATALOGOS
    path('Dato-Cliente/Editar/<ID>',
         editarCatalogos.editarCliente, name="E-Cliente"),
    path('Dato-Proveedor/Editar/<ID>',
         editarCatalogos.editarProveedor, name="E-Proveedor"),
    path('Dato-Operador/Editar/<ID>',
         editarCatalogos.editarOperador, name="E-Operador"),
    path('Dato-Materia-Prima/Editar/<ID>',
         editarCatalogos.editarMateriaPrima, name="E-Materia-Prima"),
    path('Dato-Producto/Editar/<ID>',
         editarCatalogos.editarProducto, name="E-Producto"),
    path('Dato-Producto/Detalle/Editar/<ID>',
         editarCatalogos.editarProductoReceta),
    path('Dato-Corral/Editar/<ID>', editarCatalogos.editarCorral, name="E-Corral"),
    path('Dato-Tipo-Animal/Editar/<ID>',
         editarCatalogos.editarTipoAnimal, name="E-Tipo-Animal"),
    path('Dato-Contenedor-Materia-Prima/Editar/<ID>',
         editarCatalogos.editarContenendorMP),
    path('Dato-Contenedor-Producto/Editar/<ID>',
         editarCatalogos.editarContnenedorProducto),
    path('Dato-Tolva/Editar/<ID>', editarCatalogos.editarTolva, name="E-Tolva"),

    # EDITAR PROCESOS
    path('Dato-Entrada-Materia-Prima/Editar/<ID>',
         editarProcesos.editarEntradaMateriaPrima),
    path('Dato-Salida-Materia-Prima/Editar/<ID>',
         editarProcesos.editarSalidaMateriaPrima),
    path('Dato-Entrada-Producto/Editar/<ID>',
         editarProcesos.editarEntradaProductos),
    path('Dato-Salida-Producto/Editar/<ID>',
         editarProcesos.editarSalidaProductos),
    path('Dato-Movimientos-Animales/Editar/<ID>',
         editarProcesos.editarMovimientosAnimales),
    path('Dato-Movimientos-Animales/Detalle/Editar/<ID>',
         editarProcesos.editarCantidadMovimientosAnimales),
    path('Dato-Solicitud-Servidos/Editar/<ID>',
         editarProcesos.editarSolicitudServidos),
    path('Dato-Servidos-Manuales/Editar/<ID>',
         editarProcesos.editarServidosManuales),
    path('Dato-Inventario-Materia-Prima/Editar/<ID>',
         editarProcesos.editarInventarioInicialMateriaPrima),
    path('Dato-Inventario-Productos/Editar/<ID>',
         editarProcesos.editarInventarioInicialProducto),

    # EDITAR  DE OPERADORES
    path('Dato-Operador-Entrada-Productos/Editar/<str:ID>',
         editarProcesos.editarOperadorEntradaProducto, name="E-Operaror-Entrada-Producto"),
    path('Dato-Operador-Salida-Productos/Editar/<str:ID>',
         editarProcesos.editarOperadoresSalidaProductos, name="E-Operaror-Salida-Producto"),
    path('Dato-Operador-Entrada-Materias-Primas/Editar/<str:ID>',
         editarProcesos.editarOperadorEntradaMateriaPrima, name="E-Operaror-Entrada-Materia"),
    path('Dato-Operador-Salida-Materias-Primas/Editar/<str:ID>',
         editarProcesos.editarOperadorSalidaMateriaPrima, name="E-Operaror-Salida-Materia"),

    # ACTUALIZAR SUBTABLA
    path('ActualizarEstatus/', actualizarSubTabla.actualizarEstatus),
    path('ActualizarTipoMovimiento/',
         actualizarSubTabla.actualizarTipoMovmimiento),
    path('ActualizarTipoMaterial/', actualizarSubTabla.actualizarTipoMaterial),
    path('ActualizarTipoPresentacion/',
         actualizarSubTabla.actualizarTipoPresentacion),
    path('ActualizarUnidad/', actualizarSubTabla.actualizarUnidadMedida),

    # ACTUALIZAR CATALOGOS EntradaSalidaProductos
    path('ActualizarCliente/', actualizarCatalogos.actualizarCliente),
    path('ActualizarProveedor/', actualizarCatalogos.actualizarProveedor),
    path('ActualizarOperador/', actualizarCatalogos.actualizarOperador),
    path('ActualizarMateriaPrima/', actualizarCatalogos.actualizarMateriaPrima),
    path('ActualizarProducto/', actualizarCatalogos.actualizarProductos),
    path('actualizarRecetasProductos/',
         actualizarCatalogos.actualizarRecetasProductos),
    path('ActualizarCorral/', actualizarCatalogos.actualizarCorral),
    path('ActualizarTipoAnimal/', actualizarCatalogos.actualizarTipoAnimales),
    path('ActualizarContenedorMP/', actualizarCatalogos.actualizarContenedoresMP),
    path('ActualizarContenedorProducto/',
         actualizarCatalogos.actualizarContenedoresProductos),
    path('ActualizarTolva/', actualizarCatalogos.actualizarTolva),

    # ACTUALIZAR PROCESOS
    path('ActualizarServidorManual/', actualizarProcesos.actualizarServidosManual),
    path('ActualizarServidorManualCantidad/', actualizarProcesos.actualizarCantidadServidosManual, name="Cantidad_servidos_manuales"),
    path('ActualizarEntradaMateriasPrimas/',
         actualizarProcesos.actualizarEntradaMateriaPrima),
    path('ActualizarSalidaMateriasPrimas/',
         actualizarProcesos.actualizarSalidaMateriaPrima),
    path('ActualizarEntradaProductos/',
         actualizarProcesos.actualizarEntradaProductos),
    path('ActualizarSalidaProductos/',
         actualizarProcesos.actualizarSalidaProductos),
    path('ActualizarCantidadMovimientosAnimales/',
         actualizarProcesos.actualizarCantidadAnimales),
    path('ActualizarMovimientosAnimales/',
         actualizarProcesos.actualizarMovimientosAniamales),
    path('ActualizarInventatioInicialMateriaPrima/',
         actualizarProcesos.actualizarInventatioInicialMateriaPrima),
    path('ActualizarInventatioInicialProducto/',
         actualizarProcesos.actualizarInventatioInicialProducto),
    path('ActualizarServidosATolva/', actualizarProcesos.actualizarServidosATolva),

    # ACTUALIZAR OPRADORES PROCESOS
    path('ActualizarOperadoresEntradaProducto/',
         actualizarProcesos.actualizarOperadoresEntradaProducto),
    path('ActualizarOperadoresSalidaProducto/',
         actualizarProcesos.actualizarOperadoresSalidaProducto),
    path('ActualizarOperadoresEntradaMateriaPrima/',
         actualizarProcesos.actualizarOperadoresEntradaMateriasPrimas),
    path('ActualizarOperadoresSalidaMateriaPrima/',
         actualizarProcesos.actualizarOperadoresSalidaMateriasPrimas),
    path('ActualizarCancelarServidosVehiculos/',
         actualizarProcesos.actualizarCancelarTolva),
    # REPORTES
    # bascula
    path('Reporte-Movimientos-Entrada-Materia-Prima/',
         reportes.reporteMovEntradaMP, name='Reportes-Entrada-Materia-Prima'),
    path('Reporte-Movimientos-Salida-Materia-Prima/',
         reportes.reporteMovSalidaMP, name='Reportes-Salida-Materia-Prima'),
    # animales nuevos
    path('Reporte-Movimientos-Animales/', reportes.reporteAnimalesMovimientos,
         name='Reportes-Movimientos-Animales'),
    # animales
#     path('Reporte-Movimientos-Animales/', reportes.reporteAnimalesMovimientos,
#          name='Reportes-Movimientos-Animales'),
    path('Reporte-Animales-Clientes/', reportes.reportePorClientes,
         name='Reportes-Animales-Clientes'),
    path('Reporte-Animales-Clientes-Corrales/', reportes.reportePorClientesCorrales,
         name='Reportes-Animales-Clientes-Corrales'),
    # servidos
    path('Reporte-Movimientos-Servidos/', reportes.reporteServidosMovimientos,
         name='Reportes-Movimientos-Servidos'),
    path('Reporte-Servidos-Liquidacion/', reportes.reporteServidosLiquidacion,
         name='Reportes-Servidos-Liquidacion'),
     path('Reporte-Servidos-Promedio-Diario/', reportes.reporteServidosPromedio,
         name='Reportes-Servidos-Promedio'),

    # PDF
    path('Cargamento_tolva/', DescargaPDF.cargamento_tolva, name="C-Tolva"), # PDF para tolvas
    path('Descarga_PDF_Entrada_Bascula/', DescargaPDF.entradaBasculas, name="PDF_Entrada_Bascula"), # PDF entrada productos
    path('Descarga_PDF_Salida_Bascula/', DescargaPDF.salidaBasculas, name="PDF_Salida_Bascula"), # PDF salida productos
    path('Descarga_PDF_Entrada_Materia_Prima/', DescargaPDF.entradaMateriaPrima, name="PDF_Entrada_Materia_Prima"), # PDF entrada materias primas
    path('Descarga_PDF_Salida_Materia_Prima/', DescargaPDF.salidaMateriaPrima, name="PDF_Salida_Materia_Prima"), # PDF salida materias primas
    path('Descarga_PDF_Movimiento_Animales/', DescargaPDF.movimientoAnimales, name="PDF_Movimientos_Animales"), # PDF salida materias primas

    # PDF Reportes
    path('Descarga_PDF_Reporte_Movimientos_Servidos/', DescargaPDF.reporteMovimientoServidos, name="PDF_Reportes_Mov_Servidos"), # PDF movimientos servidos
    path('Descarga_PDF_Reporte_Liquidacion_Servidos/', DescargaPDF.reporteLiquidacionServidos, name="PDF_Reportes_Liq_Servidos"), # PDF liquidacion servidos
    path('Descarga_PDF_Reporte_Entrada_Materia_Prima/', DescargaPDF.reporteEntradaMateriaPrima, name="PDF_Reportes_Entrada_Materia_Prima"), # PDF movimiento entrada materias primas
    path('Descarga_PDF_Reporte_Salida_Materia_Prima/', DescargaPDF.reporteSalidaMateriaPrima, name="PDF_Reportes_Salida_Materia_Prima"), # PDF movimiento salida materias primas
    path('Descarga_PDF_Reporte_Movimientos_Animales/', DescargaPDF.reporteMovimientoAnimales, name="PDF_Reportes_Movimiento_Animales"), # PDF movimiento animales
    path('Descarga_PDF_Reporte_Movimientos_Animales_Corral/', DescargaPDF.reporteMovimientoAnimalesCorral, name="PDF_Reportes_Movimiento_Animales_Corral"), # PDF movimiento aniamles corrales
    path('Descarga_PDF_Reporte_Movimientos_Animales_Cliente/', DescargaPDF.reporteMovimientoAnimalesCliente, name="PDF_Reportes_Movimiento_Animales_Cliente"), # PDF movimiento animales cliente

    # EXCEL
    path('EXCEL/', DescargaExcel.xlsx, name="Excel"),

     # Servidos Materia prima
     path('Salidas_De_Servidos/', guardarProcesos.salidaMPServidos, name="ServidosSalidas"),


     # Descarga pdf
     # path('DescargaPDF2/',DescargaPDF.descargarPDF, name="DescargaPDFJorge" )
     # path('mensajes/', views.webhook, name="webhook"),

     path('Correo/', Correo.index, name="correos"),
]
