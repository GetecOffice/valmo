from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission, AbstractBaseUser, BaseUserManager
# -------------------------------------------------------SUBTABLAS-------------------------------------------------------
class tblConfiguracion(models.Model):
    ID = models.AutoField(primary_key=True)
    Usuario = models.CharField(max_length=150, null=True)
    BaseDeDatos = models.CharField(max_length=150,null=True)
    FechaDescarga = models.DateTimeField(null=True)
    FechaActualizacion = models.DateTimeField(max_length=150, null=True)
    FolioSalMaquila = models.CharField(max_length=10, null=True)
    FolioEntProducto = models.CharField(max_length=10, null=True)
    FolioSalProducto = models.CharField(max_length=10, null=True)
    FolioEntMatPrima = models.CharField(max_length=10, null=True)
    FolioSalMatPrima = models.CharField(max_length=10, null=True)
    FolioRepServMov = models.CharField(max_length=10, null=True)
    FolioRepServLiq = models.CharField(max_length=10, null=True)

    FolioRepMovEntM = models.CharField(max_length=10, null=True)
    FolioRepMovSalM = models.CharField(max_length=10, null=True)
    FolioRepMovAnim = models.CharField(max_length=10, null=True)
    FolioRepMovAnCo = models.CharField(max_length=10, null=True)
    FolioRepMovAnCl = models.CharField(max_length=10, null=True)

class tblEventosValmoSys(models.Model):
    ID = models.AutoField(primary_key=True)
    Productos = models.BooleanField(null=True)
    Recetas = models.BooleanField(null=True)
    MateriaPrima = models.BooleanField(null=True)

class tblEstatus(models.Model):
    ID = models.AutoField(primary_key=True)
    Clave = models.CharField(max_length=15, null=True)
    Descripcion = models.CharField(max_length=150,null=True)
    
class tblUnidades(models.Model):
    ID = models.AutoField(primary_key=True)
    Clave = models.CharField(max_length=15, null=True)
    Descripcion = models.CharField(max_length=150,null=True)
    Abreviacion = models.CharField(max_length=150,null=True)
    
class tblTipoMov(models.Model):
    ID = models.AutoField(primary_key=True)
    Clave = models.CharField(max_length=15, null=True)
    Descripcion = models.CharField(max_length=150,null=True)
    
class tblTipoMaterial(models.Model):
    ID = models.AutoField(primary_key=True)
    Clave = models.CharField(max_length=15, null=True)
    Descripcion = models.CharField(max_length=150,null=True)
    
class tblTipoPresentacion(models.Model):
    ID = models.AutoField(primary_key=True)
    Clave = models.CharField(max_length=15, null=True)
    Descripcion = models.CharField(max_length=150,null=True)
    UdeM = models.ForeignKey(tblUnidades, on_delete=models.DO_NOTHING, null=True)
    Cantidad = models.FloatField(null=True)
    Visible = models.CharField(max_length=15, null=True)
    
class tblTecnicos(models.Model):
    ID = models.AutoField(primary_key=True)
    Tecnico = models.CharField(max_length=150,null=True)
    TecnicoEditor = models.CharField(max_length=150,null=True)
    TecnicoElimino = models.CharField(max_length=150,null=True)
    AreaRegistro = models.CharField(max_length=150,null=True)
    NombreTabla = models.CharField(max_length=150,null=True)
    IDFilaTabla = models.CharField(max_length=150, null=True)
    IDFila = models.CharField(max_length=150, null=True)
    Acciones = models.CharField(max_length=50,null=True)
    AccionesEditado = models.CharField(max_length=50,null=True)
    AccionesEliminado = models.CharField(max_length=50,null=True)
    Fecha = models.DateTimeField(null=True)
    FechaActualizado = models.DateTimeField(null=True)
    FechaEliminado = models.DateTimeField(null=True)
    
# -------------------------------------------------------CATALOGOS-------------------------------------------------------
class tblClientes(models.Model):
    ID = models.AutoField(primary_key=True)
    Clave = models.CharField(max_length=15, null=True)
    Nombre = models.CharField(max_length=150, unique=True, null=True)
    Direccion = models.CharField(max_length=150, null=True)
    Ciudad = models.CharField(max_length=150, null=True)
    RFC = models.CharField(max_length=50, null=True)
    Email = models.EmailField(null=True)
    Contacto = models.CharField(max_length=150,null=True)
    TelefonoContacto = models.CharField(max_length=150,null=True)
    
class tblProveedores(models.Model):
    ID = models.AutoField(primary_key=True)
    Clave = models.CharField(max_length=15, null=True)
    Nombre = models.CharField(max_length=150, unique=True, null=True)
    Direccion = models.CharField(max_length=150, null=True)
    Ciudad = models.CharField(max_length=150, null=True)
    RFC = models.CharField(max_length=50, null=True)
    Email = models.EmailField(null=True)
    Contacto = models.CharField(max_length=150,null=True)
    TelefonoContacto = models.CharField(max_length=150,null=True)
    
class tblOperadores(models.Model):
    ID = models.AutoField(primary_key=True)
    Clave = models.CharField(max_length=15, null=True)
    Descripcion = models.CharField(max_length=150, null=True)
    IDEstatus = models.ForeignKey(tblEstatus, on_delete=models.DO_NOTHING, null=True)

class tblMateriaPrima(models.Model):
    ID = models.AutoField(primary_key=True)
    Clave = models.CharField(max_length=15, null=True)
    Descripcion = models.CharField(max_length=150,null=True)
    IDEstatus = models.ForeignKey(tblEstatus, on_delete=models.DO_NOTHING, null=True)
    IDUnidadMedida = models.ForeignKey(tblUnidades, on_delete=models.DO_NOTHING, null=True)
    PrecioUnitario = models.FloatField(null=True)
    Merma = models.FloatField(null=True)
    
class tblProductos(models.Model):
    ID = models.AutoField(primary_key=True)
    Clave = models.CharField(max_length=15, null=True)
    Descripcion = models.CharField(max_length=150,null=True)
    IDEstatus = models.ForeignKey(tblEstatus, on_delete=models.DO_NOTHING, null=True)
    IDUnidadMedida = models.ForeignKey(tblUnidades, on_delete=models.DO_NOTHING, null=True)
    PrecioUnitario = models.FloatField(null=True)
    SeSirve = models.CharField(max_length=15, null=True)
    
class tblCorrales(models.Model):
    ID = models.AutoField(primary_key=True)
    Clave = models.CharField(max_length=150, null=True)
    Descripcion = models.CharField(max_length=150,null=True)
    IDCliente = models.ForeignKey(tblClientes, on_delete=models.DO_NOTHING, null=True)
    IDEstatus = models.ForeignKey(tblEstatus, on_delete=models.DO_NOTHING, null=True)
    Capacidad = models.FloatField(null=True)
    FechaAsigna = models.DateTimeField(max_length=150, null=True)
       
class tblAnimalesTipo(models.Model):
    ID = models.AutoField(primary_key=True)
    Clave = models.CharField(max_length=15, null=True)
    Descripcion = models.CharField(max_length=150,null=True)
    IDEstatus = models.ForeignKey(tblEstatus, on_delete=models.DO_NOTHING, null=True)
    
class tblContenedoresMateriaPrima(models.Model):
    ID = models.AutoField(primary_key=True)
    Clave = models.CharField(max_length=15, null=True)
    Cliente = models.CharField(max_length=150,null=True)
    IDEstatus = models.ForeignKey(tblEstatus, on_delete=models.DO_NOTHING, null=True)
    Capacidad = models.FloatField(max_length=150,null=True)
    IDCliente = models.ForeignKey(tblClientes, on_delete=models.DO_NOTHING, null=True)
    
class tblContenedoresProductos(models.Model):
    ID = models.AutoField(primary_key=True)
    Clave = models.CharField(max_length=15, null=True)
    Proveedor = models.CharField(max_length=150,null=True)
    IDEstatus = models.ForeignKey(tblEstatus, on_delete=models.DO_NOTHING, null=True)
    Capacidad = models.FloatField(max_length=150,null=True)
    IDCliente = models.ForeignKey(tblProveedores, on_delete=models.DO_NOTHING, null=True)
    
class tblTolva(models.Model):
    ID = models.AutoField(primary_key=True)
    Clave = models.CharField(max_length=15, null=True)
    Marca = models.CharField(max_length=15, null=True)
    Modelo = models.CharField(max_length=150, null=True)
    IDEstatus = models.ForeignKey(tblEstatus, on_delete=models.DO_NOTHING, null=True)
    IDProducto = models.ForeignKey(tblProductos, on_delete=models.DO_NOTHING, null=True)
    Capacidad = models.IntegerField(null=True)
    UdeM = models.ForeignKey(tblUnidades, on_delete=models.DO_NOTHING, null=True)
    Alias = models.CharField(max_length=100, null=True)

# -------------------------------------------------------SUBTABLAS------------------------------------------------------
class tblAsignaCorrales(models.Model):
    ID = models.AutoField(primary_key=True)
    Clave = models.CharField(max_length=15, null=True)
    IDCorral = models.ForeignKey(tblCorrales, on_delete=models.DO_NOTHING, null=True)
    IDCliente = models.ForeignKey(tblClientes, on_delete=models.DO_NOTHING, null=True)
    Fecha = models.DateTimeField(max_length=150, null=True)
    TipoMov = models.ForeignKey(tblTipoMov, on_delete=models.DO_NOTHING, null=True)

# -------------------------------------------------------PROCESOS-------------------------------------------------------
class tblEntradaMP(models.Model):
    ID = models.AutoField(primary_key=True)
    IDFolio = models.CharField(max_length=15, null=True)
    IDProveedor =  models.ForeignKey(tblProveedores, on_delete=models.DO_NOTHING, null=True)
    IDAlmacen = models.ForeignKey(tblContenedoresMateriaPrima, on_delete=models.DO_NOTHING, null=True)
    IDMateriaPrima = models.ForeignKey(tblMateriaPrima, on_delete=models.DO_NOTHING, null=True)
    IDPresentacion = models.ForeignKey(tblTipoPresentacion, on_delete=models.DO_NOTHING, null=True)
    cantidad = models.FloatField(null=True)
    referencia = models.IntegerField(null=True)
    fecha = models.DateTimeField(max_length=150, null=True)
    notas = models.CharField(max_length=120,  null=True)
    
class tblSalidaMP(models.Model):
    ID = models.AutoField(primary_key=True)
    IDFolio = models.CharField(max_length=15, null=True)
    IDCliente =  models.ForeignKey(tblClientes, on_delete=models.DO_NOTHING, null=True)
    IDAlmacen = models.ForeignKey(tblContenedoresMateriaPrima, on_delete=models.DO_NOTHING, null=True)
    IDMateriaPrima = models.ForeignKey(tblMateriaPrima, on_delete=models.DO_NOTHING, null=True)
    IDPresentacion = models.ForeignKey(tblTipoPresentacion, on_delete=models.DO_NOTHING, null=True)
    cantidad = models.FloatField(null=True)
    referencia = models.IntegerField(null=True)
    fecha = models.DateTimeField(max_length=150, null=True)
    notas = models.CharField(max_length=120,  null=True)
    
class tblServido(models.Model):
    ID = models.AutoField(primary_key=True)
    Folio = models.CharField(max_length=15, null=True)
    IDCliente = models.ForeignKey(tblClientes, on_delete=models.DO_NOTHING, null=True)
    IDCorral = models.ForeignKey(tblCorrales, on_delete=models.DO_NOTHING, null=True)
    IDProducto = models.ForeignKey(tblProductos, on_delete=models.DO_NOTHING, null=True)
    IDEstatus = models.ForeignKey(tblEstatus, on_delete=models.DO_NOTHING, null=True)
    IDTolva = models.ForeignKey(tblTolva, on_delete=models.DO_NOTHING, null=True)
    CantidadSolicitada = models.IntegerField(null=True)
    CantidadServida = models.IntegerField(null=True)
    Prioridad = models.CharField(max_length=100, null=True)
    Fecha = models.DateTimeField(max_length=150, null=True)
    FechaAServir = models.DateField(max_length=150, null=True)
    FechaServida = models.DateTimeField(max_length=150, null=True)

class tblEntradaProductos(models.Model):
    ID = models.AutoField(primary_key=True)
    IDFolio = models.CharField(max_length=15, null=True)
    IDProveedor = models.ForeignKey(tblProveedores, on_delete=models.DO_NOTHING, null=True)
    IDAlmacen = models.ForeignKey(tblContenedoresProductos, on_delete=models.DO_NOTHING, null=True)
    IDProductos = models.ForeignKey(tblProductos, on_delete=models.DO_NOTHING, null=True)
    IDPresentacion = models.ForeignKey(tblTipoPresentacion, on_delete=models.DO_NOTHING, null=True)
    IDTipoMov = models.ForeignKey(tblTipoMov, on_delete=models.DO_NOTHING, null=True)
    cantidad = models.FloatField(null=True) 
    referencia = models.IntegerField(null=True)
    fecha = models.DateTimeField(max_length=150, null=True)
    notas = models.CharField(max_length=120,  null=True)
    
class tblSalidaProductos(models.Model):
    ID = models.AutoField(primary_key=True)
    IDFolio = models.CharField(max_length=15, null=True)
    IDCliente = models.ForeignKey(tblClientes, on_delete=models.DO_NOTHING, null=True)
    IDAlmacen = models.ForeignKey(tblContenedoresProductos, on_delete=models.DO_NOTHING, null=True)
    IDProductos = models.ForeignKey(tblProductos, on_delete=models.DO_NOTHING, null=True)
    IDPresentacion = models.ForeignKey(tblTipoPresentacion, on_delete=models.DO_NOTHING, null=True)
    IDTipoMov = models.ForeignKey(tblTipoMov, on_delete=models.DO_NOTHING, null=True)
    cantidad = models.FloatField(null=True) 
    referencia = models.IntegerField(null=True)
    fecha = models.DateTimeField(max_length=150, null=True)
    notas = models.CharField(max_length=120,  null=True)
    
class tblDetalleAnimales(models.Model):
    ID = models.AutoField(primary_key=True)
    Folio = models.CharField(max_length=15, null=True)
    IDCliente = models.ForeignKey(tblClientes, on_delete=models.DO_NOTHING, null=True)
    IDCorral = models.ForeignKey(tblCorrales, on_delete=models.DO_NOTHING, null=True)
    IDAnimal = models.ForeignKey(tblAnimalesTipo, on_delete=models.DO_NOTHING, null=True)
    Fecha = models.DateTimeField(null=True)
    Peso = models.FloatField(null=True)
    NoPartida = models.IntegerField(null=True)
    No_Guia = models.CharField(max_length=30,null=True)
    

class tblMovimientoAnimales(models.Model):
    ID = models.AutoField(primary_key=True)
    Folio = models.CharField(max_length=15, null=True)
    IDCliente = models.ForeignKey(tblClientes, on_delete=models.DO_NOTHING, null=True)
    IDMovimiento = models.ForeignKey(tblTipoMov, on_delete=models.DO_NOTHING, null=True)
    Fecha = models.DateField(null=True)
    Peso = models.FloatField(null=True)
    NoPartida = models.CharField(max_length=30, null=True)

class tblDetalleMovAnimales(models.Model):
    ID = models.AutoField(primary_key=True)
    IDFolio = models.CharField(max_length=150,null=True)
    IDAnimales = models.ForeignKey(tblAnimalesTipo, on_delete=models.DO_NOTHING, null=True)
    Cantidad = models.IntegerField(null=True)
    PesoTotal = models.FloatField(null=True)
    PesoPromedio = models.FloatField(null=True)
    # modificaciones agregadas el 161124
    IDCorral = models.ForeignKey(tblCorrales, on_delete=models.DO_NOTHING, null=True)
    No_Guia = models.CharField(max_length=30, null=True)
    Notas = models.CharField(max_length=150, null=True) 

    
class tblInventarioInicialesMP(models.Model):
    ID = models.AutoField(primary_key=True)
    Folio = models.CharField(max_length=15, null=True)
    IDContenedor = models.ForeignKey(tblContenedoresMateriaPrima, on_delete=models.DO_NOTHING, null=True)
    IDMateriaPrima = models.ForeignKey(tblMateriaPrima, on_delete=models.DO_NOTHING, null=True)
    Cantidad = models.FloatField(null=True)
    Fecha = models.DateTimeField(max_length=150, null=True)
    Notas = models.CharField(max_length=150, null=True)
    
class tblInventarioInicialesProductos(models.Model):
    ID = models.AutoField(primary_key=True)
    Folio = models.CharField(max_length=15, null=True)
    IDContenedor = models.ForeignKey(tblContenedoresProductos, on_delete=models.DO_NOTHING, null=True)
    IDProducto = models.ForeignKey(tblProductos, on_delete=models.DO_NOTHING, null=True)
    Cantidad = models.FloatField(null=True)
    Fecha = models.DateTimeField(max_length=150, null=True)
    Notas = models.CharField(max_length=150, null=True)
     
# -------------------------------------------------------SUBTABLAS-------------------------------------------------------
class tblProductosMateriaPrima(models.Model):
    ID = models.AutoField(primary_key=True)
    Folio = models.CharField(max_length=15, null=True)
    IDMateriaPrima = models.ForeignKey(tblMateriaPrima, on_delete=models.DO_NOTHING, null=True)
    IDProductos = models.ForeignKey(tblProductos, on_delete=models.DO_NOTHING, null=True)
    Porcentaje = models.FloatField(null=True)
    Merma = models.FloatField(null=True)
    
class tblOtrosDatosMovMP(models.Model):
    ID = models.AutoField(primary_key=True)
    IDMovMP = models.CharField(max_length=15, null=True)
    IDOperador = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    Costo = models.FloatField(null=True)
    Flete = models.FloatField(null=True)
    Maniobra = models.FloatField(null=True)
    Camion = models.CharField(max_length=150, null=True)
    Chofer = models.CharField(max_length=150, null=True)
    Placas = models.CharField(max_length=150, null=True)
    
class tblOtrosDatosSalXBas(models.Model):
    ID = models.AutoField(primary_key=True)
    IDSalida = models.CharField(max_length=15, null=True)
    IDOperador = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    Camion = models.CharField(max_length=150, null=True)
    Chofer = models.CharField(max_length=150, null=True)
    Placas = models.CharField(max_length=150, null=True)
    
class tblServiciosWeb(models.Model):
    ID = models.AutoField(primary_key=True)
    Servicio = models.BooleanField(True, null=True)
    EstadoPago = models.BooleanField(True, null=True)
    FechaVencimiento = models.DateField(null=True)
    Notificacion = models.BooleanField(True, null=True)

# ------------------------------------------------------------------------------- TABLAS VALMOSYS -------------------------------------------------------------------------------
class tblMPMovimientos(models.Model):
    ID = models.AutoField(primary_key=True)
    Fecha = models.DateField(null=True)
    IDMateriaPrima = models.ForeignKey(tblMateriaPrima, on_delete=models.DO_NOTHING, null=True)
    cantidad = models.FloatField(null=True) 
    IDFolio = models.CharField(max_length=15, null=True)

class tblProductoMovimientos(models.Model):
    ID = models.AutoField(primary_key=True)
    IDFolio = models.CharField(max_length=15, null=True)
    Fecha = models.DateField(null=True)
    TipoMov = models.ForeignKey(tblTipoMov, on_delete=models.DO_NOTHING, null=True)
    IDProducto = models.ForeignKey(tblProductos, on_delete=models.DO_NOTHING, null=True)
    cantidad = models.FloatField(null=True) 
    notas = models.CharField(max_length=120,  null=True)