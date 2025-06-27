from django.shortcuts import render, redirect
# LLAMAR ARCHIVOS LOCALES
from Aplicacion.forms import *
from Aplicacion.models import *
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, date
from django.utils import timezone
from datetime import timedelta
from django.db import connection
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< TABLAS DE CATALOGOS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# --------------------------------------------------------CLIENTES---------------------------------------------------------

def formulario(request):
    corrales = []
    Nombre = []
    email_v = ''
    ultimo_contacto = tblServido.objects.order_by('-ID').first()
    FechaDeHoy = timezone.localtime(timezone.now()).strftime('%Y-%m-%d %H:%M')
    FEProductos = tblProductos.objects.all().exclude(ID=1).order_by('Descripcion')

    ultimo_folio = 0
    idCliente = 0

    email_v = request.session.get('email', None)
    if email_v is not None:
        del request.session['email']
        email = True
    elif request.method == 'POST' and 'email' in request.POST:
        email_v = request.POST.get('email')
        email = True
    else:
        email = False

    if email == True:
        try:
            ultimo_contacto = tblServido.objects.order_by('-ID').first()
            if ultimo_contacto:
                ultimo_folio = ultimo_contacto.ID + 1
            else:
                ultimo_folio = 1

            cliente = tblClientes.objects.get(Email=email_v)
            idCliente = cliente.ID
            Nombre = cliente.Nombre
            corrales = tblCorrales.objects.filter(
                IDCliente_id=idCliente).order_by('Descripcion')

        except ObjectDoesNotExist:
            print("Error")

        # Renderiza la vista con el contexto
    return render(request, 'Publico/form.html', {'corrales': corrales, 'Nombre': Nombre, 'email': email_v,
                                                 'FEProductos': FEProductos, 'ultimo_folio': ultimo_folio, 'FechaDeHoy': FechaDeHoy, 'idCliente': idCliente})

def servidos(request):
    servidos = []
    Nombre = []
    email_v = ''
    idCliente = 0

    email_v = request.session.get('email', None)
    if email_v is not None:
        del request.session['email']
        email = True
    elif request.method == 'POST' and 'email' in request.POST:
        email_v = request.POST.get('email')
        email = True
    else:
        email = False

    if email == True:
        try:
            cliente = tblClientes.objects.get(Email=email_v)
            idCliente = cliente.ID
            Nombre = cliente.Nombre
            servidos = tblServido.objects.filter(IDCliente_id=idCliente).values('Folio', 'IDCliente_id__Nombre', 'IDCorral_id__Descripcion', 'IDProducto_id', 'FechaAServir', 'FechaServida',
                                                                                'IDProducto_id__Descripcion', 'IDEstatus_id__Descripcion', 'CantidadSolicitada', 'CantidadServida', 'Fecha')
        except ObjectDoesNotExist:
            print("Error")
    return render(request, 'Publico/data.html', {'corrales': servidos, 'Nombre': Nombre, 'email': email_v,
                                                 'idCliente': idCliente})

def cliente(request):
    corrales = []
    Nombre = []
    corrales_filtro = []

    email_v = ''
    idCliente = 0
    if request.method == 'POST' and 'email' in request.POST:
        email_v = request.POST.get('email')
        try:
            cliente = tblClientes.objects.get(Email=email_v)
            idCliente = cliente.ID
            Nombre = cliente.Nombre
            # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
            # corrales = tblCorrales.objects.filter(IDCliente_id=idCliente).values('').order_by('Descripcion')
            consulta_sql = """SELECT c.ID, c.Descripcion AS CorralDescripcion, e.Descripcion AS EstatusDescripcion, p.Descripcion AS ProductoDescripcion,s.CantidadSolicitada, s.CantidadServida, s.Fecha, s.ID AS ServidoID, s.Folio
                                FROM aplicacion_tblcorrales c
                            LEFT JOIN (SELECT IDCorral_id, MAX(ID) AS MaxServidoID FROM aplicacion_tblservido where IDCliente_id = %s GROUP BY IDCorral_id) ms ON c.ID = ms.IDCorral_id
                            LEFT JOIN aplicacion_tblservido s ON ms.MaxServidoID = s.ID
                            LEFT JOIN aplicacion_tblestatus e ON s.IDEstatus_id = e.ID
                            LEFT JOIN aplicacion_tblproductos p ON s.IDProducto_id = p.ID
                            WHERE c.IDCliente_id = %s ORDER BY c.Descripcion;"""
            with connection.cursor() as cursor:
                cursor.execute(consulta_sql, [idCliente, idCliente])
                corrales = cursor.fetchall()
            corrales_filtro = tblServido.objects.filter(IDCliente_id  = idCliente).values('ID', 'Folio','IDCorral_id',
                            'IDCliente_id__Nombre', 'IDCorral_id__Descripcion', 'IDProducto_id__Descripcion', 'IDEstatus_id__Descripcion',
                            'CantidadSolicitada', 'CantidadServida', 'Prioridad', 'Fecha', 'FechaServida', 'FechaAServir')
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            # messages.success(
            #     request, f'El email "{email_v}" se ha encontrado exitosamente')

        except ObjectDoesNotExist:
            messages.error(
                request, f'El email "{email_v}" no se encuentra registrado en Ganadera Valmo, lo sentimos')

        # Renderiza la vista con el contexto
    return render(request, 'Publico/cliente.html', {'corrales': corrales, 'Nombre': Nombre, 'email': email_v,
                                                        'idCliente': idCliente, 'corrales_filtro':corrales_filtro})

def guardarSolicitudServidoCliente(request):
    if request.method == 'POST':
        # Un solo producto seleccionado
        folios = request.POST.getlist('folio')
        productos = request.POST.get('producto')

        # Obtener listas de datos desde el formulario
        clientes = request.POST.getlist('cliente[]')
        corrales = request.POST.getlist('corral[]')
        estatuses = request.POST.getlist('estatus[]')
        prioridades = request.POST.getlist('prioridad[]')
        cantidadesSol = request.POST.getlist('cantidadSol[]')
        cantidadesSer = request.POST.getlist('cantidadSer[]')
        fechasSol = request.POST.getlist('fechaSol[]')
        fechasSer = request.POST.getlist('fechaSer[]')
        peticiones = request.POST.getlist('peticion[]')
        emails = request.POST.getlist('email[]')

        fechaCheck = request.POST.getlist('checkFecha[]')


        solicitudes = []

        for i in range(len(cantidadesSol)):
            if cantidadesSol[i] and float(cantidadesSol[i]) != 0:
                
                solicitud = {
                    'cliente': clientes[i],
                    'corral': corrales[i],
                    'producto': productos,
                    'estatus': estatuses[i],
                    'cantidadSol': cantidadesSol[i],
                    'cantidadSer': cantidadesSer[i],
                    'prioridad': prioridades[i],
                    'fechaSol': fechasSol[i],
                    'fechaSer': fechasSer[i],
                    'fechasPet': fechaCheck[i],
                    'peticion': peticiones[i],
                    'email': emails[i],
                }
                solicitudes.append(solicitud)

      # Obtener el último folio
        if tblServido.objects.exists():
            ultimo_folio_str = tblServido.objects.latest('ID').Folio
            ultimo_folio = int(ultimo_folio_str.split('-')[-1])
        else:
            ultimo_folio = 0

        # Aquí puedes guardar las solicitudes en la base de datos o procesarlas como sea necesario.
        for solicitud in solicitudes:
                # Incrementar el folio
                ultimo_folio += 1
                formatoClave = 'F-{:06d}'.format(ultimo_folio)

                if solicitud['fechasPet'] == 'hoy':
                    FechaDeHoy = timezone.localtime(timezone.now()).strftime('%Y-%m-%d')
                elif solicitud['fechasPet'] == 'mañana':
                    fechaMañana = timezone.localtime(timezone.now()) + timedelta(days=1)
                    FechaDeHoy = fechaMañana.strftime('%Y-%m-%d')       
                print(FechaDeHoy)                                 

                tblServido.objects.create(
                Folio=formatoClave,
                IDCliente_id=solicitud['cliente'],
                IDCorral_id=solicitud['corral'],
                IDProducto_id=solicitud['producto'],
                IDEstatus_id=solicitud['estatus'],
                CantidadSolicitada=solicitud['cantidadSol'],
                CantidadServida=solicitud['cantidadSer'],
                Prioridad=solicitud['prioridad'],
                FechaAServir = FechaDeHoy,
                Fecha=solicitud['fechaSol'],
                FechaServida=solicitud['fechaSer']
            )
    peticion = 2

    if request.method == 'POST':

        if peticion == 2:
            email = request.POST['email']
            request.session['email'] = email
            return redirect('FP-Cliente')
    else:
        return redirect('T-Solicitud-Servidos')
