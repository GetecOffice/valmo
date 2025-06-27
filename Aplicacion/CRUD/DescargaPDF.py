from django.template.loader import render_to_string
from io import BytesIO
from django.db.models import Q
from xhtml2pdf import pisa
from django.templatetags.static import static
from datetime import datetime, timedelta, date
from Aplicacion.forms import *
from Aplicacion.models import *
from django.http import HttpResponse
from django.db import connection
from django.db.models import Sum
# IMPORT PARA CORREOS ELECTRONICOS
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
#!<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>!
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# -----------------------------------------------------------INCREMENTADOR DE FOLIOS POR PDF-----------------------------------------------------------
def sacarFormatoClave(formatoAnterior):
    clave_int = int(formatoAnterior[2:])
    clave_int += 1  
    return 'F-{:06d}'.format(clave_int)

# ---------------------------------------------------------------CARGAR DE FOLIOS POR PDF--------------------------------------------------------------
def cargar_folio(valor):
    Folio = tblConfiguracion.objects.get(ID=1)
    
    # Diccionario para mapear valor a los atributos de Folio
    folio_map = {
        1: 'FolioSalMaquila',
        2: 'FolioEntProducto',
        3: 'FolioSalProducto',
        4: 'FolioEntMatPrima',
        5: 'FolioSalMatPrima',
        6: 'FolioRepServMov',
        7: 'FolioRepServLiq',
        8: 'FolioRepMovEntM',
        9: 'FolioRepMovSalM',
        10: 'FolioRepMovAnim',
        11: 'FolioRepMovAnCo',
        12: 'FolioRepMovAnCl'
    }
    
    if valor in folio_map:
        nombre_atributo = folio_map[valor]
        GFolio = getattr(Folio, nombre_atributo)
        formatoClave = sacarFormatoClave(GFolio)
        setattr(Folio, nombre_atributo, formatoClave)
        Folio.save()
        return formatoClave
    else:
        raise ValueError("El valor no corresponde a un caso válido")
# -----------------------------------------------------------------------------------------------------------------------------------------------------

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#!<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>!

#!<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>!
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# -------------------------------------------------------------PDF PARA SERVIDOS DE TOLVA--------------------------------------------------------------
def cargamento_tolva(request):
    valor = 1
    formatoClave = cargar_folio(valor)
    fecha_actual = datetime.today()
    formatted_fecha_actual = fecha_actual.strftime("%Y-%m-%d %H-%M-%S")
    user = request.user
    logo_url = request.build_absolute_uri(static('assets/img/inicio/valmo.png'))
    
    dataInput = request.POST.get('tolva', '')
    if dataInput is not None and dataInput != '':
        TTolva = tblTolva.objects.get(ID=dataInput)
        alias = TTolva.Alias
        producto = TTolva.IDProducto.ID
        FiltradoProducto= tblProductos.objects.get(ID=producto)
        unidad_id = FiltradoProducto.IDUnidadMedida.ID
        Filtradounidad= tblUnidades.objects.get(ID=unidad_id)
        TContenido = tblServido.objects.filter(IDEstatus_id = 8, IDTolva_id = dataInput).order_by('ID').values('Folio',
        'IDCliente_id__Nombre', 'IDCorral_id__Descripcion','CantidadSolicitada', 'CantidadServida')

    html_string = render_to_string('Descargas/PDF/Salida Maquila/index.html', {'logo_url': logo_url, 'Filtradounidad':Filtradounidad, 'folio': formatoClave,
                'alias':alias, 'user': user,  'TContenido': TContenido, 'fecha_actual': fecha_actual, 'FiltradoProducto':FiltradoProducto})

    # Create a BytesIO buffer to receive the PDF
    pdf_buffer = BytesIO()

    # Generate the PDF using xhtml2pdf
    pisa.CreatePDF(html_string, dest=pdf_buffer)

    # Get the PDF content from the buffer
    pdf_file = pdf_buffer.getvalue()

    # Create an HTTP response with the attached PDF file
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Servidos {formatted_fecha_actual}.pdf"'
        # response['Content-Disposition'] = 'attachment; filename="Sálida-' + \
    #     Folio+" "+Nombre+'.pdf"'
    return response

# ------------------------------------------------------------PDF PARA ENTRADA DE PRODUCTOS------------------------------------------------------------
def entradaBasculas(request):
    # valor = 2
    # formatoClave = cargar_folio(valor)
    fecha_actual = datetime.today()
    formatted_fecha_actual = fecha_actual.strftime("%Y-%m-%d %H-%M-%S")
    user = request.user
    logo_url = request.build_absolute_uri(static('assets/img/inicio/valmo.png'))
    
    dataInput = request.POST.get('entradaBascula', '')
    if dataInput is not None and dataInput != '':
        chofer = tblOtrosDatosMovMP.objects.filter(IDMovMP = dataInput).values('ID', 'IDMovMP', 'Costo', 'Flete',
                                                'Maniobra', 'Camion', 'Chofer', 'Placas', 'IDOperador_id__first_name')

        entradaBascula = tblEntradaProductos.objects.filter(IDFolio = dataInput).values(
                    'ID', 'IDFolio', 'IDProveedor_id__Nombre', 'IDAlmacen_id__Proveedor', 'IDProductos_id__Descripcion', 
                    'IDPresentacion_id__Descripcion', 'IDPresentacion_id', 'cantidad', 'referencia', 'fecha', 'notas'
        )
    # Render the HTML template with the data
    html_string = render_to_string('Descargas/PDF/EntradaProductos/index.html', {'logo_url': logo_url, 'folio':dataInput,
    'fecha_actual': fecha_actual, 'entradaBascula':entradaBascula, 'chofer':chofer})

    # Create a BytesIO buffer to receive the PDF
    pdf_buffer = BytesIO()

    # Generate the PDF using xhtml2pdf
    pisa.CreatePDF(html_string, dest=pdf_buffer)

    # Get the PDF content from the buffer
    pdf_file = pdf_buffer.getvalue()

    # Create an HTTP response with the attached PDF file
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Servidos {formatted_fecha_actual}.pdf"'
    return response

# ------------------------------------------------------------PDF PARA SALIDAS DE PRODUCTOS------------------------------------------------------------
def salidaBasculas(request):
    # valor = 3
    # formatoClave = cargar_folio(valor)
    fecha_actual = datetime.today()
    formatted_fecha_actual = fecha_actual.strftime("%Y-%m-%d %H-%M-%S")
    user = request.user
    logo_url = request.build_absolute_uri(static('assets/img/inicio/valmo.png'))
    
    dataInput= request.POST.get('salidaBascula', '')
    if dataInput is not None and dataInput != '':
        chofer = tblOtrosDatosSalXBas.objects.filter(IDSalida = dataInput).values('ID', 'IDSalida', 'Camion', 'Chofer', 'Placas', 'IDOperador')

        clientes = tblSalidaProductos.objects.filter(IDFolio = dataInput).values_list('IDCliente__Nombre', flat=True).distinct()
        for cliente in clientes:
            procedencia = cliente
        
        salidaBascula = tblSalidaProductos.objects.filter(IDFolio = dataInput).values(
                    'ID', 'IDFolio', 'IDCliente__Nombre', 'IDAlmacen__Proveedor', 'IDProductos_id__Descripcion', 
                    'IDPresentacion_id__Descripcion', 'IDPresentacion_id', 'cantidad', 'referencia', 'fecha', 'notas'
        )

    # Render the HTML template with the data
    html_string = render_to_string('Descargas/PDF/SalidaProductos/index.html', {'logo_url': logo_url,
    'folio':dataInput, 'fecha_actual': fecha_actual, 'salidaBascula':salidaBascula, 'chofer':chofer,
    'procedencia': procedencia})

    # Create a BytesIO buffer to receive the PDF
    pdf_buffer = BytesIO()

    # Generate the PDF using xhtml2pdf
    pisa.CreatePDF(html_string, dest=pdf_buffer)

    # Get the PDF content from the buffer
    pdf_file = pdf_buffer.getvalue()

    # Create an HTTP response with the attached PDF file
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Servidos {formatted_fecha_actual}.pdf"'
    return response

# ---------------------------------------------------------PDF PARA ENTRADA DE MATERIAS PRIMAS---------------------------------------------------------
def entradaMateriaPrima(request):
    # valor = 4
    # formatoClave = cargar_folio(valor)
    fecha_actual = datetime.today()
    formatted_fecha_actual = fecha_actual.strftime("%Y-%m-%d %H-%M-%S")
    user = request.user
    logo_url = request.build_absolute_uri(static('assets/img/inicio/valmo.png'))
    
    dataInput = request.POST.get('entradaMateriaPrima', '')
    if dataInput is not None and dataInput != '':
        chofer = tblOtrosDatosMovMP.objects.filter(IDMovMP = dataInput).values('ID', 'IDMovMP', 'Costo', 'Flete',
                                                'Maniobra', 'Camion', 'Chofer', 'Placas', 'IDOperador_id__first_name')
        proveedores = tblEntradaMP.objects.filter(IDFolio=dataInput).values_list('IDProveedor_id__Nombre', flat=True).distinct()
        for proveedor in proveedores:
            procedencia = proveedor

        entradaMatPrima = tblEntradaMP.objects.filter(IDFolio = dataInput).values(
            'ID', 'IDFolio', 'IDProveedor_id__Nombre', 'IDAlmacen_id__Cliente', 'IDMateriaPrima_id__Descripcion', 'IDPresentacion_id__Descripcion',
            'IDPresentacion_id', 'cantidad', 'referencia', 'fecha', 'notas')
        
    # Render the HTML template with the data
    html_string = render_to_string('Descargas/PDF/EntradaMateriaPrima/index.html', {'logo_url': logo_url, 'procedencia':procedencia, 
    'folio':dataInput, 'fecha_actual': fecha_actual, 'entradaMatPrima':entradaMatPrima, 'chofer':chofer})

    # Create a BytesIO buffer to receive the PDF
    pdf_buffer = BytesIO()

    # Generate the PDF using xhtml2pdf
    pisa.CreatePDF(html_string, dest=pdf_buffer)

    # Get the PDF content from the buffer
    pdf_file = pdf_buffer.getvalue()

    # Create an HTTP response with the attached PDF file
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Entrada Materia Prima {formatted_fecha_actual}.pdf"'
    return response

# ---------------------------------------------------------PDF PARA SALIDAS DE MATERIAS PRIMAS---------------------------------------------------------
def salidaMateriaPrima(request):
    # valor = 5
    # formatoClave = cargar_folio(valor)
    fecha_actual = datetime.today()
    formatted_fecha_actual = fecha_actual.strftime("%Y-%m-%d %H-%M-%S")
    user = request.user
    logo_url = request.build_absolute_uri(static('assets/img/inicio/valmo.png'))
    
    dataInput= request.POST.get('salidaBascula', '')
    if dataInput is not None and dataInput != '':
        chofer = tblOtrosDatosSalXBas.objects.filter(IDSalida = dataInput).values('ID', 'IDSalida', 'Camion', 'Chofer', 'Placas', 'IDOperador')

        clientes = tblSalidaMP.objects.filter(IDFolio = dataInput).values_list('IDCliente__Nombre', flat=True).distinct()
        for cliente in clientes:
            procedencia = cliente
        
        salidaBascula = tblSalidaMP.objects.filter(IDFolio = dataInput).values(
            'ID', 'IDFolio', 'IDCliente_id__Nombre', 'IDAlmacen_id__Cliente', 'IDMateriaPrima_id__Descripcion', 
            'IDPresentacion_id__Descripcion',   'IDPresentacion_id', 'cantidad', 'referencia', 'fecha', 'notas'
        )
    print(dataInput)

    # Render the HTML template with the data
    html_string = render_to_string('Descargas/PDF/SalidaMateriaPrima/index.html', {'logo_url': logo_url,
    'folio': dataInput, 'fecha_actual': fecha_actual, 'salidaBascula':salidaBascula, 'chofer':chofer,
    'procedencia': procedencia})

    # Create a BytesIO buffer to receive the PDF
    pdf_buffer = BytesIO()

    # Generate the PDF using xhtml2pdf
    pisa.CreatePDF(html_string, dest=pdf_buffer)

    # Get the PDF content from the buffer
    pdf_file = pdf_buffer.getvalue()

    # Create an HTTP response with the attached PDF file
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Servidos {formatted_fecha_actual}.pdf"'
    return response

# ---------------------------------------------------------PDF PARA SALIDAS DE MATERIAS PRIMAS---------------------------------------------------------
def movimientoAnimales(request):
    valor = 13
    formatoClave = "F-000000"
    fecha_actual = date.today()
    formatted_fecha_actual = fecha_actual.strftime("%Y-%m-%d")
    user = request.user
    logo_url = request.build_absolute_uri(static('assets/img/inicio/valmo.png'))
    
    dataInput= request.POST.get('movimientoAnimales', '')
    if dataInput is not None and dataInput != '':
        Detalle = tblDetalleMovAnimales.objects.filter(IDFolio = dataInput).values('ID', 'IDFolio', 
        'IDAnimales_id__Descripcion', 'Cantidad', 'PesoTotal', 'PesoPromedio', 'IDCorral_id__Descripcion', 'No_Guia', 'Notas')
        # Realizar las sumas de los campos deseados
        suma_detalles = Detalle.aggregate( suma_cantidad=Sum('Cantidad'), suma_peso_total=Sum('PesoTotal'), suma_peso_promedio=Sum('PesoPromedio'))

        suma_cantidad = suma_detalles['suma_cantidad']
        suma_peso_total = suma_detalles['suma_peso_total']
        suma_peso_promedio = suma_detalles['suma_peso_promedio']

        movimientoAnimales = tblMovimientoAnimales.objects.get(Folio = dataInput)
        Cliente = movimientoAnimales.IDCliente.ID
        movimiento = movimientoAnimales.IDMovimiento.ID
        if movimiento == 1 or movimiento == "1":
            mov = "Entrada"
        else:
            mov = "Sálida"
        # fecha = movimientoAnimales.Fecha
        FiltradoCliente = tblClientes.objects.get(ID=Cliente)
    # Render the HTML template with the data}
    imprimir = 3
    html_string = render_to_string('Descargas/PDF/MovimientoAnimales/index.html', {'logo_url': logo_url, 'Detalle':Detalle, 'imprimir': range(imprimir),
    'formatoClave':formatoClave, 'fecha_actual': fecha_actual, 'movimientoAnimales':movimientoAnimales, 'procedencia': FiltradoCliente,
    'suma_cantidad':suma_cantidad, 'suma_peso_total':suma_peso_total, 'suma_peso_promedio':suma_peso_promedio})

    # Create a BytesIO buffer to receive the PDF
    pdf_buffer = BytesIO()

    # Generate the PDF using xhtml2pdf
    pisa.CreatePDF(html_string, dest=pdf_buffer)

    # Get the PDF content from the buffer
    pdf_file = pdf_buffer.getvalue()

    # Create an HTTP response with the attached PDF file
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{mov} Movimiento Animales {formatted_fecha_actual}.pdf"'
    return response
# -----------------------------------------------------------------------------------------------------------------------------------------------------

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#!<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>!

#!<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>!
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# ----------------------------------------------------------- PDF PARA MOVIMIENTOS SERVIDOS -----------------------------------------------------------

def reporteMovimientoServidos(request):
    valor = 6
    formatoClave = cargar_folio(valor)
    fecha_actual = datetime.today()
    formatted_fecha_actual = fecha_actual.strftime("%Y-%m-%d %H-%M-%S")
    user = request.user
    Cliente = request.POST['cliente']
    Fecha = request.POST['fechaInicial']
    Fecha2 = request.POST['fechaFinal']
    logo_url = request.build_absolute_uri(static('assets/img/inicio/valmo.png'))
    
    dataInput= request.POST.get('reporte-movimientos-servidos', '')
    if dataInput is not None and dataInput != '':
        if  Cliente == 'todos':
            consulta_sql = """SELECT DISTINCT Aplicacion_tblservido.ID, Aplicacion_tblclientes.Nombre, 
                Aplicacion_tblcorrales.Descripcion,  Aplicacion_tblproductos.Descripcion,
                Aplicacion_tblservido.CantidadSolicitada, Aplicacion_tblservido.CantidadServida,
                Aplicacion_tblservido.Fecha, Aplicacion_tblservido.FechaServida, Aplicacion_tblunidades.Abreviacion
                FROM Aplicacion_tblservido
                LEFT JOIN Aplicacion_tblproductos ON Aplicacion_tblservido.IDProducto_id = Aplicacion_tblproductos.ID
                LEFT JOIN Aplicacion_tblunidades ON Aplicacion_tblproductos.IDUnidadMedida_id = Aplicacion_tblunidades.ID
                LEFT JOIN Aplicacion_tblclientes ON Aplicacion_tblservido.IDCliente_id = Aplicacion_tblclientes.ID
                LEFT JOIN Aplicacion_tblcorrales ON Aplicacion_tblservido.IDCorral_id = Aplicacion_tblcorrales.ID
                WHERE Aplicacion_tblservido.Fecha BETWEEN  %s AND  %s and Aplicacion_tblservido.IDCliente_id != 1 and Aplicacion_tblservido.IDEstatus_id = 10 """
            with connection.cursor() as cursor:
                cursor.execute(consulta_sql, [Fecha, Fecha2])
                reportes = cursor.fetchall()
            Nombre = 'En general'
            Cliente = 'todos'
            correo = False
        else:
            consulta_sql = """SELECT DISTINCT Aplicacion_tblservido.ID, Aplicacion_tblclientes.Nombre, 
                Aplicacion_tblcorrales.Descripcion,  Aplicacion_tblproductos.Descripcion,
                Aplicacion_tblservido.CantidadSolicitada, Aplicacion_tblservido.CantidadServida,
                Aplicacion_tblservido.Fecha, Aplicacion_tblservido.FechaServida, Aplicacion_tblunidades.Abreviacion
                FROM Aplicacion_tblservido
                LEFT JOIN Aplicacion_tblproductos ON Aplicacion_tblservido.IDProducto_id = Aplicacion_tblproductos.ID
                LEFT JOIN Aplicacion_tblunidades ON Aplicacion_tblproductos.IDUnidadMedida_id = Aplicacion_tblunidades.ID
                LEFT JOIN Aplicacion_tblclientes ON Aplicacion_tblservido.IDCliente_id = Aplicacion_tblclientes.ID
                LEFT JOIN Aplicacion_tblcorrales ON Aplicacion_tblservido.IDCorral_id = Aplicacion_tblcorrales.ID
                WHERE  Aplicacion_tblclientes.ID = %s AND  (Aplicacion_tblservido.Fecha BETWEEN  %s AND  %s) and Aplicacion_tblservido.IDCliente_id != 1 and Aplicacion_tblservido.IDEstatus_id = 10 
                """
            with connection.cursor() as cursor:
                cursor.execute(consulta_sql, [Cliente, Fecha, Fecha2])
                reportes = cursor.fetchall()
            TECliente = tblClientes.objects.get(ID=Cliente)
            Nombre = TECliente.Nombre
            correo = TECliente.Email

    # Render the HTML template with the data
    html_string = render_to_string('Descargas/PDF/ReporteServidos/Movimientos.html', {'logo_url': logo_url, 'fecha_actual': fecha_actual,
                                        'formatoClave':formatoClave, 'reportes': reportes, 'Nombre': Nombre, 'Cliente': Cliente, 'Fecha1': Fecha, 'Fecha2': Fecha2})
    # Create a BytesIO buffer to receive the PDF
    pdf_buffer = BytesIO()

    # Generate the PDF using xhtml2pdf
    pisa.CreatePDF(html_string, dest=pdf_buffer)

    # Get the PDF content from the buffer
    pdf_file = pdf_buffer.getvalue()

    # Close the buffer
    pdf_buffer.close()
    
    # if correo:
    #     nombre_user = Nombre
    #     nombre_Reporte = "REPORTE MOVIMIENTO DE SERVIDOS"
    #     nombre_archivo = f"Servidos {formatted_fecha_actual}"
    #     Enviar_PDF_email(nombre_user, correo, nombre_Reporte, nombre_archivo, pdf_file, formatted_fecha_actual)

    # Create an HTTP response with the attached PDF file
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Servidos {formatted_fecha_actual}.pdf"'
    return response

# ----------------------------------------------------------- PDF PARA LIQUIDACION SERVIDOS -----------------------------------------------------------
def reporteLiquidacionServidos(request):
    valor = 7
    formatoClave = cargar_folio(valor)
    fecha_actual = datetime.today()
    formatted_fecha_actual = fecha_actual.strftime("%Y-%m-%d %H-%M-%S")
    user = request.user
    Cliente = request.POST['Cliente']
    Fecha = request.POST['fechaInicial']
    Fecha2 = request.POST['fechaFinal']
    logo_url = request.build_absolute_uri(static('assets/img/inicio/valmo.png'))
    
    dataInput= request.POST.get('reporte-liquidacion-servidos', '')
    if dataInput is not None and dataInput != '':
        if Cliente == 'todos':
            consulta_sql = """SELECT Aplicacion_tblcorrales.Descripcion, Aplicacion_tblproductos.Descripcion, Aplicacion_tblunidades.Abreviacion, 
            SUM(Aplicacion_tblservido.CantidadServida)
            FROM Aplicacion_tblservido
            INNER JOIN Aplicacion_tblclientes ON Aplicacion_tblservido.IDCliente_id = Aplicacion_tblclientes.ID 
            INNER JOIN Aplicacion_tblproductos ON Aplicacion_tblservido.IDProducto_id = Aplicacion_tblproductos.ID
            INNER JOIN Aplicacion_tblcorrales ON Aplicacion_tblservido.IDCorral_id	= Aplicacion_tblcorrales.ID     
            INNER JOIN  Aplicacion_tblunidades ON Aplicacion_tblproductos.IDUnidadMedida_id = Aplicacion_tblunidades.ID  
            WHERE  Aplicacion_tblclientes.ID != 1 AND  (Aplicacion_tblservido.Fecha BETWEEN %s AND %s) and Aplicacion_tblservido.IDEstatus_id = 10 
            GROUP BY  Aplicacion_tblproductos.Descripcion, Aplicacion_tblservido.IDCorral_id, Aplicacion_tblunidades.Abreviacion
            ORDER BY Aplicacion_tblcorrales.Descripcion"""

            with connection.cursor() as cursor:
                cursor.execute(consulta_sql, [Fecha, Fecha2])
                reportes = cursor.fetchall()

            consulta2_sql = """
            SELECT Aplicacion_tblproductos.Descripcion, Aplicacion_tblunidades.Abreviacion, SUM(Aplicacion_tblservido.CantidadServida)
            FROM Aplicacion_tblservido
            INNER JOIN Aplicacion_tblclientes ON Aplicacion_tblservido.IDCliente_id = Aplicacion_tblclientes.ID
            INNER JOIN Aplicacion_tblproductos ON Aplicacion_tblservido.IDProducto_id = Aplicacion_tblproductos.ID
            INNER JOIN Aplicacion_tblunidades ON Aplicacion_tblproductos.IDUnidadMedida_id = Aplicacion_tblunidades.ID  
            WHERE  Aplicacion_tblclientes.ID != 1 AND (Aplicacion_tblservido.Fecha BETWEEN %s AND %s ) and Aplicacion_tblservido.IDEstatus_id = 10 
            GROUP BY  Aplicacion_tblproductos.ID, Aplicacion_tblunidades.Abreviacion
            ORDER BY  Aplicacion_tblproductos.Descripcion desc"""

            with connection.cursor() as cursor:
                cursor.execute(consulta2_sql, [Fecha, Fecha2])
                reportes2 = cursor.fetchall()

            query = """
                SELECT  Aplicacion_tblcorrales.Descripcion, SUM(Aplicacion_tblservido.CantidadServida),Aplicacion_tblcorrales.ID
                FROM Aplicacion_tblservido
                INNER JOIN 	Aplicacion_tblcorrales ON  Aplicacion_tblservido.IDCorral_id = Aplicacion_tblcorrales.ID
                WHERE  Aplicacion_tblservido.IDCliente_id != 1 AND  (Aplicacion_tblservido.Fecha BETWEEN %s AND %s ) and Aplicacion_tblservido.IDEstatus_id = 10 
                GROUP BY  Aplicacion_tblservido.IDCorral_id
                ORDER BY  Aplicacion_tblcorrales.Descripcion
                        """
            with connection.cursor() as cursor:
                cursor.execute(query, [Fecha, Fecha2])
                Data = cursor.fetchall()

            ListaTem = []
            Datos = []

            for i in range(0, len(Data)):
                ListaTem.append(Data[i][0])
                ListaTem.append(Data[i][1])
                DiasAnimal = CalculaDiasAnimal(
                    Cliente, Data[i][2], Fecha, Fecha2)
                DiasAnimFomated = "{:.0f}".format(DiasAnimal)
                if DiasAnimal < 1:
                    DiasAnimal = 1
                    ToTab = "ND"
                else:
                    ToTab = DiasAnimFomated

                ListaTem.append(ToTab)
                PromDia = int(Data[i][1])/int(DiasAnimal)
                PromDia = "{:.4f}".format(PromDia)
                ListaTem.append(PromDia)
                Datos.append(ListaTem)
                ListaTem = []

            ListaTem = []
            DataToRep = []
            for ren in range(0, len(Datos)):
                for col in range(0, len(Datos[0])):
                    DaToTabla = str(Datos[ren][col])
                    ListaTem.append(DaToTabla)
                DataToRep.append(ListaTem)
                ListaTem = []

            Nombre = 'En general'
            Cliente = 'todos'

        else:
            consulta_sql = """SELECT Aplicacion_tblcorrales.Descripcion, Aplicacion_tblproductos.Descripcion, Aplicacion_tblunidades.Abreviacion, 
            SUM(Aplicacion_tblservido.CantidadServida)
            FROM Aplicacion_tblservido
            INNER JOIN Aplicacion_tblclientes ON Aplicacion_tblservido.IDCliente_id = Aplicacion_tblclientes.ID 
            INNER JOIN Aplicacion_tblproductos ON Aplicacion_tblservido.IDProducto_id = Aplicacion_tblproductos.ID
            INNER JOIN Aplicacion_tblcorrales ON Aplicacion_tblservido.IDCorral_id	= Aplicacion_tblcorrales.ID     
            INNER JOIN  Aplicacion_tblunidades ON Aplicacion_tblproductos.IDUnidadMedida_id = Aplicacion_tblunidades.ID  
            WHERE  Aplicacion_tblclientes.ID = %s AND  (Aplicacion_tblservido.Fecha BETWEEN %s AND %s) and Aplicacion_tblservido.IDEstatus_id = 10 
            GROUP BY  Aplicacion_tblproductos.Descripcion, Aplicacion_tblservido.IDCorral_id, Aplicacion_tblunidades.Abreviacion
            ORDER BY Aplicacion_tblcorrales.Descripcion"""
            with connection.cursor() as cursor:
                cursor.execute(consulta_sql, [Cliente, Fecha, Fecha2])
                reportes = cursor.fetchall()
            consulta2_sql = """
            SELECT Aplicacion_tblproductos.Descripcion,Aplicacion_tblunidades.Abreviacion, SUM(Aplicacion_tblservido.CantidadServida)
            FROM Aplicacion_tblservido
            INNER JOIN Aplicacion_tblclientes ON Aplicacion_tblservido.IDCliente_id = Aplicacion_tblclientes.ID
            INNER JOIN Aplicacion_tblproductos ON Aplicacion_tblservido.IDProducto_id = Aplicacion_tblproductos.ID
            INNER JOIN Aplicacion_tblunidades ON Aplicacion_tblproductos.IDUnidadMedida_id = Aplicacion_tblunidades.ID  
            WHERE  Aplicacion_tblclientes.ID = %s AND (Aplicacion_tblservido.Fecha BETWEEN %s AND %s ) and Aplicacion_tblservido.IDEstatus_id = 10 
            GROUP BY  Aplicacion_tblproductos.ID, Aplicacion_tblunidades.Abreviacion
            ORDER BY  Aplicacion_tblproductos.Descripcion desc"""
            with connection.cursor() as cursor:
                cursor.execute(consulta2_sql, [Cliente, Fecha, Fecha2])
                reportes2 = cursor.fetchall()
            query = """
                SELECT  Aplicacion_tblcorrales.Descripcion, SUM(Aplicacion_tblservido.CantidadServida),Aplicacion_tblcorrales.ID
                FROM Aplicacion_tblservido
                INNER JOIN 	Aplicacion_tblcorrales ON  Aplicacion_tblservido.IDCorral_id = Aplicacion_tblcorrales.ID
                WHERE  Aplicacion_tblservido.IDCliente_id = %s AND  (Aplicacion_tblservido.Fecha BETWEEN %s AND %s ) and Aplicacion_tblservido.IDEstatus_id = 10 
                GROUP BY  Aplicacion_tblservido.IDCorral_id
                ORDER BY  Aplicacion_tblcorrales.Descripcion
                        """
            with connection.cursor() as cursor:
                cursor.execute(query, [Cliente, Fecha, Fecha2])
                Data = cursor.fetchall()
            ListaTem = []
            Datos = []
            for i in range(0, len(Data)):
                ListaTem.append(Data[i][0])
                ListaTem.append(Data[i][1])
                DiasAnimal = CalculaDiasAnimal(
                    Cliente, Data[i][2], Fecha, Fecha2)
                DiasAnimFomated = "{:.0f}".format(DiasAnimal)
                if DiasAnimal < 1:
                    DiasAnimal = 1
                    ToTab = "ND"
                else:
                    ToTab = DiasAnimFomated
                ListaTem.append(ToTab)
                PromDia = int(Data[i][1])/int(DiasAnimal)
                PromDia = "{:.4f}".format(PromDia)
                ListaTem.append(PromDia)
                Datos.append(ListaTem)
                ListaTem = []
            ListaTem = []
            DataToRep = []
            for ren in range(0, len(Datos)):
                for col in range(0, len(Datos[0])):
                    DaToTabla = str(Datos[ren][col])
                    ListaTem.append(DaToTabla)
                DataToRep.append(ListaTem)
                ListaTem = []
            TECliente = tblClientes.objects.get(ID=Cliente)
            Nombre = TECliente.Nombre

    # Render the HTML template with the data
    html_string = render_to_string('Descargas/PDF/ReporteServidos/Liquidacion.html', {'logo_url': logo_url, 'fecha_actual': fecha_actual,'reportes2': reportes2,
            'DataToRep':DataToRep, 'formatoClave':formatoClave, 'reportes': reportes, 'Nombre': Nombre, 'Cliente': Cliente, 'Fecha1': Fecha, 'Fecha2': Fecha2})
    # Create a BytesIO buffer to receive the PDF
    pdf_buffer = BytesIO()

    # Generate the PDF using xhtml2pdf
    pisa.CreatePDF(html_string, dest=pdf_buffer)

    # Get the PDF content from the buffer
    pdf_file = pdf_buffer.getvalue()

    # Create an HTTP response with the attached PDF file
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Servidos Liquidacion {formatted_fecha_actual}.pdf"'
    return response

# ---------------------------------------------------------PDF PARA ENTRADA DE MATERIAS PRIMAS---------------------------------------------------------
def reporteEntradaMateriaPrima(request):
    valor = 8
    formatoClave = cargar_folio(valor)
    fecha_actual = datetime.today()
    formatted_fecha_actual = fecha_actual.strftime("%Y-%m-%d %H-%M-%S")
    user = request.user
    logo_url = request.build_absolute_uri(static('assets/img/inicio/valmo.png'))
    Contenedor = request.POST['Contenedor']
    Fecha = request.POST['fechaInicial']
    Fecha2 = request.POST['fechaFinal']    
    dataInput = request.POST.get('reporte-entrada-mp', '')
    if dataInput is not None and dataInput != '':
        if Contenedor == 'todos':
            reportes = tblEntradaMP.objects.filter(fecha__range=[Fecha, Fecha2]).values('ID', 'notas',
                    'fecha', 'IDMateriaPrima_id__Descripcion', 'IDAlmacen_id__Cliente', 'cantidad').order_by('fecha')
            Nombre = 'En general'
        else:
            # Consulta los registros de tblEntradaMP para un contenedor específico en el rango de fechas
            reportes = tblEntradaMP.objects.filter(IDAlmacen__IDCliente=Contenedor, fecha__range=[Fecha, Fecha2]).values('ID','notas',
                'fecha', 'IDMateriaPrima_id__Descripcion', 'IDAlmacen_id__Cliente', 'cantidad').order_by('fecha')
            
            TEContenedores = tblContenedoresMateriaPrima.objects.get(IDCliente_id=Contenedor)
            Nombre = TEContenedores.Cliente

    # Render the HTML template with the data
    html_string = render_to_string('Descargas/PDF/ReporteMateriaPrima/Entrada.html', {'logo_url': logo_url,
    'formatoClave':formatoClave, 'fecha_actual': fecha_actual, 'reportes': reportes, 'Nombre': Nombre, 'Fecha1': Fecha, 'Fecha2': Fecha2})

    # Create a BytesIO buffer to receive the PDF
    pdf_buffer = BytesIO()

    # Generate the PDF using xhtml2pdf
    pisa.CreatePDF(html_string, dest=pdf_buffer)

    # Get the PDF content from the buffer
    pdf_file = pdf_buffer.getvalue()

    # Create an HTTP response with the attached PDF file
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Entrada Materia Prima {formatted_fecha_actual}.pdf"'
    return response

# ---------------------------------------------------------PDF PARA SALIDA DE MATERIAS PRIMAS----------------------------------------------------------
def reporteSalidaMateriaPrima(request):
    valor = 9
    formatoClave = cargar_folio(valor)
    fecha_actual = datetime.today()
    formatted_fecha_actual = fecha_actual.strftime("%Y-%m-%d %H-%M-%S")
    user = request.user
    logo_url = request.build_absolute_uri(static('assets/img/inicio/valmo.png'))
    Contenedor = request.POST['Contenedor']
    Fecha = request.POST['fechaInicial']
    Fecha2 = request.POST['fechaFinal']    
    dataInput = request.POST.get('reporte-entrada-mp', '')
    if dataInput is not None and dataInput != '':
        if Contenedor == 'todos':
            reportes = tblSalidaMP.objects.filter(fecha__range=[Fecha, Fecha2]) \
                .values('IDFolio', 'fecha', 'IDMateriaPrima_id__Descripcion', 'IDAlmacen_id__Cliente', 'cantidad', 'notas') \
                .order_by('fecha')
            Nombre = 'En general'
        else:
            reportes = tblSalidaMP.objects.filter(IDAlmacen__IDCliente=Contenedor, fecha__range=[Fecha, Fecha2]) \
                .values('IDFolio', 'fecha', 'IDMateriaPrima_id__Descripcion', 'IDAlmacen_id__Cliente', 'cantidad', 'notas') \
                .order_by('fecha')
            TEContenedores = tblContenedoresMateriaPrima.objects.get(IDCliente_id=Contenedor)
            Nombre = TEContenedores.Cliente
        
    # Render the HTML template with the data
    html_string = render_to_string('Descargas/PDF/ReporteMateriaPrima/Salida.html', {'logo_url': logo_url,
    'formatoClave':formatoClave, 'fecha_actual': fecha_actual, 'reportes': reportes, 'Nombre': Nombre, 'Fecha1': Fecha, 'Fecha2': Fecha2})

    # Create a BytesIO buffer to receive the PDF
    pdf_buffer = BytesIO()

    # Generate the PDF using xhtml2pdf
    pisa.CreatePDF(html_string, dest=pdf_buffer)

    # Get the PDF content from the buffer
    pdf_file = pdf_buffer.getvalue()

    # Create an HTTP response with the attached PDF file
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Salida Materia Prima {formatted_fecha_actual}.pdf"'
    return response

# ---------------------------------------------------------- PDF PARA MOVIMIENTO DE ANIMALES ---------------------------------------------------------- 
def reporteMovimientoAnimales(request):
    valor = 10
    formatoClave = cargar_folio(valor)
    fecha_actual = date.today()
    formatted_fecha_actual = fecha_actual.strftime("%Y-%m-%d")
    user = request.user
    logo_url = request.build_absolute_uri(static('assets/img/inicio/valmo.png'))

    Cliente = request.POST['cliente']
    Movimiento_v = request.POST['mov']
    Fecha = request.POST['fechaInicial']
    Fecha2 = request.POST['fechaFinal']    
    
    TEMov = tblTipoMov.objects.get(ID=Movimiento_v)
    Movimiento = TEMov.Descripcion  
    dataInput = request.POST.get('reporte-movimiento-animales', '')
    if dataInput is not None and dataInput != '':
        if Cliente == 'todos':
            consulta_sql = """SELECT Aplicacion_tbldetallemovanimales.IDFolio, Aplicacion_tblclientes.Nombre, Aplicacion_tbldetallemovanimales.Cantidad,
            Aplicacion_tblAnimalesTipo.Descripcion,Aplicacion_tbldetallemovanimales.PesoTotal, Aplicacion_tblcorrales.Descripcion
            FROM  Aplicacion_tblmovimientoanimales
            INNER JOIN Aplicacion_tblclientes ON Aplicacion_tblclientes.ID = Aplicacion_tblmovimientoanimales.IDCliente_id 
            INNER JOIN Aplicacion_tbldetallemovanimales ON  Aplicacion_tblmovimientoanimales.Folio = Aplicacion_tbldetallemovanimales.IDFolio
            INNER JOIN Aplicacion_tblcorrales ON Aplicacion_tblcorrales.ID = Aplicacion_tbldetallemovanimales.IDCorral_id
            INNER JOIN Aplicacion_tblAnimalesTipo ON Aplicacion_tblAnimalesTipo.ID = Aplicacion_tbldetallemovanimales.IDAnimales_id 
            WHERE DATE(Aplicacion_tblmovimientoanimales.Fecha) BETWEEN %s AND %s AND Aplicacion_tblmovimientoanimales.IDMovimiento_id = %s
            ORDER by Aplicacion_tbldetallemovanimales.IDFolio DESC"""
            with connection.cursor() as cursor:
                cursor.execute(
                    consulta_sql, [Fecha, Fecha2, Movimiento_v])
                reportes = cursor.fetchall()
            Nombre = 'En general'
            Cliente = 'todos'
        else:
            consulta_sql = """SELECT Aplicacion_tbldetallemovanimales.IDFolio, Aplicacion_tblclientes.Nombre, Aplicacion_tbldetallemovanimales.Cantidad,
            Aplicacion_tblAnimalesTipo.Descripcion,Aplicacion_tbldetallemovanimales.PesoTotal, Aplicacion_tblcorrales.Descripcion
            FROM  Aplicacion_tblmovimientoanimales
            INNER JOIN Aplicacion_tblclientes ON Aplicacion_tblclientes.ID = Aplicacion_tblmovimientoanimales.IDCliente_id 
            INNER JOIN Aplicacion_tbldetallemovanimales ON  Aplicacion_tblmovimientoanimales.Folio = Aplicacion_tbldetallemovanimales.IDFolio
            INNER JOIN Aplicacion_tblcorrales ON Aplicacion_tblcorrales.ID = Aplicacion_tbldetallemovanimales.IDCorral_id
            INNER JOIN Aplicacion_tblAnimalesTipo ON Aplicacion_tblAnimalesTipo.ID = Aplicacion_tbldetallemovanimales.IDAnimales_id 
            WHERE Aplicacion_tblmovimientoanimales.IDCliente_id = %s AND  DATE(Aplicacion_tblmovimientoanimales.Fecha) BETWEEN %s AND %s 
            AND Aplicacion_tblmovimientoanimales.IDMovimiento_id = %s
            ORDER by Aplicacion_tbldetallemovanimales.IDFolio DESC"""
            with connection.cursor() as cursor:
                cursor.execute(
                    consulta_sql, [Cliente, Fecha, Fecha2, Movimiento_v])
                reportes = cursor.fetchall()
            TECliente = tblClientes.objects.get(ID=Cliente)
            Nombre = TECliente.Nombre
        
        
    # Render the HTML template with the data
    html_string = render_to_string('Descargas/PDF/ReporteAnimales/Movimientos2.html', {'logo_url': logo_url, 'Movimiento':Movimiento,
    'formatoClave':formatoClave, 'fecha_actual': fecha_actual, 'reportes': reportes, 'Nombre': Nombre, 'Fecha1': Fecha, 'Fecha2': Fecha2})

    # Create a BytesIO buffer to receive the PDF
    pdf_buffer = BytesIO()

    # Generate the PDF using xhtml2pdf
    pisa.CreatePDF(html_string, dest=pdf_buffer)

    # Get the PDF content from the buffer
    pdf_file = pdf_buffer.getvalue()

    # Create an HTTP response with the attached PDF file
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Movimientos Animales {formatted_fecha_actual}.pdf"'
    return response

def reporteMovimientoAnimales2(request):
    valor = 10
    formatoClave = cargar_folio(valor)
    fecha_actual = datetime.today()
    formatted_fecha_actual = fecha_actual.strftime("%Y-%m-%d %H-%M-%S")
    user = request.user
    logo_url = request.build_absolute_uri(static('assets/img/inicio/valmo.png'))

    Cliente = request.POST['cliente']
    Fecha = request.POST['fechaInicial']
    Fecha2 = request.POST['fechaFinal']    

    dataInput = request.POST.get('reporte-movimiento-animales', '')
    if dataInput is not None and dataInput != '':
        if Cliente == 'todos':
            reportes = tblMovimientoAnimales.objects.filter(Fecha__range=[Fecha, Fecha2]) \
                .exclude(IDCliente=1) \
                .values('Folio', 'Fecha', 'IDCliente__Nombre', 'IDCorral__Descripcion', 'IDMovimiento__Descripcion') \
                .order_by('Folio')
            Nombre = 'En general'
            Cliente = 'todos'
        else:
            reportes = tblMovimientoAnimales.objects.filter(
                Q(IDCliente=Cliente) & Q(Fecha__range=[
                    Fecha, Fecha2]) & ~Q(IDCliente=1)
            ).values('Folio', 'Fecha', 'IDCliente__Nombre', 'IDCorral__Descripcion', 'IDMovimiento__Descripcion') \
                .order_by('Folio')
            TECliente = tblClientes.objects.get(ID=Cliente)
            Nombre = TECliente.Nombre
        
    # Render the HTML template with the data
    html_string = render_to_string('Descargas/PDF/ReporteAnimales/Movimientos.html', {'logo_url': logo_url,
    'formatoClave':formatoClave, 'fecha_actual': fecha_actual, 'reportes': reportes, 'Nombre': Nombre, 'Fecha1': Fecha, 'Fecha2': Fecha2})

    # Create a BytesIO buffer to receive the PDF
    pdf_buffer = BytesIO()

    # Generate the PDF using xhtml2pdf
    pisa.CreatePDF(html_string, dest=pdf_buffer)

    # Get the PDF content from the buffer
    pdf_file = pdf_buffer.getvalue()

    # Create an HTTP response with the attached PDF file
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Movimientos Animales {formatted_fecha_actual}.pdf"'
    return response
    
# ---------------------------------------------------- PDF PARA MOVIMIENTO DE ANIMALES POR CORRAL -----------------------------------------------------
def reporteMovimientoAnimalesCorral(request):
    valor = 11
    formatoClave = cargar_folio(valor)
    fecha_actual = datetime.today()
    formatted_fecha_actual = fecha_actual.strftime("%Y-%m-%d %H-%M-%S")
    user = request.user
    logo_url = request.build_absolute_uri(static('assets/img/inicio/valmo.png'))
    Cliente = request.POST['cliente']
    Fecha = request.POST['fechaInicial']
    Fecha2 = request.POST['fechaFinal']    
    dataInput = request.POST.get('reporte-movimiento-animales-corral', '')
    if dataInput is not None and dataInput != '':
        if Cliente == 'todos':
            consulta_sql = """SELECT Aplicacion_tblclientes.Nombre, Aplicacion_tblcorrales.Descripcion,
            SUM(case WHEN  Aplicacion_tblmovimientoanimales.IDMovimiento_id = 1 AND DATE(Aplicacion_tblmovimientoanimales.Fecha) 
                BETWEEN DATE(Aplicacion_tblcorrales.FechaAsigna) AND %s THEN  Aplicacion_tbldetallemovanimales.Cantidad ELSE 0 END) - 
            SUM(case WHEN  Aplicacion_tblmovimientoanimales.IDMovimiento_id = 2 AND DATE(Aplicacion_tblmovimientoanimales.Fecha)  
                BETWEEN DATE(Aplicacion_tblcorrales.FechaAsigna) AND %s THEN  Aplicacion_tbldetallemovanimales.Cantidad   ELSE 0 END) AS INICIAL,
            SUM(case WHEN  Aplicacion_tblmovimientoanimales.IDMovimiento_id = 1 AND DATE(Aplicacion_tblmovimientoanimales.Fecha) 
                BETWEEN %s AND %s THEN  Aplicacion_tbldetallemovanimales.Cantidad ELSE 0 END) AS ENTRADA,
            SUM(case WHEN  Aplicacion_tblmovimientoanimales.IDMovimiento_id = 2 AND DATE(Aplicacion_tblmovimientoanimales.Fecha) 
                BETWEEN %s AND %s THEN  Aplicacion_tbldetallemovanimales.Cantidad  ELSE 0 END) AS SALIDA
            FROM  Aplicacion_tblmovimientoanimales
            INNER JOIN Aplicacion_tblclientes ON Aplicacion_tblclientes.ID = Aplicacion_tblmovimientoanimales.IDCliente_id 
            INNER JOIN Aplicacion_tblcorrales ON  Aplicacion_tblcorrales.ID = Aplicacion_tblmovimientoanimales.IDCorral_id
            INNER JOIN Aplicacion_tbldetallemovanimales ON  Aplicacion_tblmovimientoanimales.Folio = Aplicacion_tbldetallemovanimales.IDFolio
            WHERE  Aplicacion_tblmovimientoanimales.IDCorral_id IN (SELECT  Aplicacion_tblcorrales.ID FROM Aplicacion_tblcorrales)
            GROUP BY Aplicacion_tblmovimientoanimales.IDCorral_id, Aplicacion_tblclientes.Nombre """

            with connection.cursor() as cursor:
                cursor.execute(
                    consulta_sql, [Fecha2, Fecha2, Fecha, Fecha2, Fecha, Fecha2])
                reportes = cursor.fetchall()
            Nombre = 'En general'
            Cliente = 'todos'
           
        else:
            consulta_sql = """SELECT Aplicacion_tblclientes.Nombre, Aplicacion_tblcorrales.Descripcion,
            SUM(case WHEN  Aplicacion_tblmovimientoanimales.IDMovimiento_id = 1 AND DATE(Aplicacion_tblmovimientoanimales.Fecha) 
                BETWEEN DATE(Aplicacion_tblcorrales.FechaAsigna) AND %s THEN  Aplicacion_tbldetallemovanimales.Cantidad ELSE 0 END) - 
            SUM(case WHEN  Aplicacion_tblmovimientoanimales.IDMovimiento_id = 2 AND DATE(Aplicacion_tblmovimientoanimales.Fecha)  
                BETWEEN DATE(Aplicacion_tblcorrales.FechaAsigna) AND %s THEN  Aplicacion_tbldetallemovanimales.Cantidad   ELSE 0 END) AS INICIAL,
            SUM(case WHEN  Aplicacion_tblmovimientoanimales.IDMovimiento_id = 1 AND DATE(Aplicacion_tblmovimientoanimales.Fecha) 
                BETWEEN %s AND %s THEN  Aplicacion_tbldetallemovanimales.Cantidad ELSE 0 END) AS ENTRADA,
            SUM(case WHEN  Aplicacion_tblmovimientoanimales.IDMovimiento_id = 2 AND DATE(Aplicacion_tblmovimientoanimales.Fecha) 
                BETWEEN %s AND %s THEN  Aplicacion_tbldetallemovanimales.Cantidad  ELSE 0 END) AS SALIDA
            FROM  Aplicacion_tblmovimientoanimales
            INNER JOIN Aplicacion_tblclientes ON Aplicacion_tblclientes.ID = Aplicacion_tblmovimientoanimales.IDCliente_id 
            INNER JOIN Aplicacion_tblcorrales ON  Aplicacion_tblcorrales.ID = Aplicacion_tblmovimientoanimales.IDCorral_id
            INNER JOIN Aplicacion_tbldetallemovanimales ON  Aplicacion_tblmovimientoanimales.Folio = Aplicacion_tbldetallemovanimales.IDFolio
            WHERE  Aplicacion_tblmovimientoanimales.IDCorral_id IN 
                (SELECT  Aplicacion_tblcorrales.ID FROM Aplicacion_tblcorrales where  Aplicacion_tblcorrales.IDCliente_id = %s)
                            AND Aplicacion_tblmovimientoanimales.IDCliente_id = %s
            GROUP BY Aplicacion_tblmovimientoanimales.IDCorral_id, Aplicacion_tblclientes.Nombre """

            with connection.cursor() as cursor:
                cursor.execute(
                    consulta_sql, [Fecha2, Fecha2, Fecha, Fecha2, Fecha, Fecha2, Cliente, Cliente])
                reportes = cursor.fetchall()
            TECliente = tblClientes.objects.get(ID=Cliente)
            Nombre = TECliente.Nombre
    
    # Render the HTML template with the data
    html_string = render_to_string('Descargas/PDF/ReporteAnimales/Corral.html', {'logo_url': logo_url,
    'formatoClave':formatoClave, 'fecha_actual': fecha_actual, 'reportes': reportes, 'Nombre': Nombre, 'Fecha1': Fecha, 'Fecha2': Fecha2})

    # Create a BytesIO buffer to receive the PDF
    pdf_buffer = BytesIO()

    # Generate the PDF using xhtml2pdf
    pisa.CreatePDF(html_string, dest=pdf_buffer)

    # Get the PDF content from the buffer
    pdf_file = pdf_buffer.getvalue()

    # Create an HTTP response with the attached PDF file
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Movimientos Animales Por Corral {formatted_fecha_actual}.pdf"'
    return response

# ---------------------------------------------------- PDF PARA MOVIMIENTO DE ANIMALES POR CLIENTE ---------------------------------------------------- 
def reporteMovimientoAnimalesCliente(request):
    valor = 12
    formatoClave = cargar_folio(valor)
    fecha_actual = datetime.today()
    formatted_fecha_actual = fecha_actual.strftime("%Y-%m-%d %H-%M-%S")
    user = request.user
    logo_url = request.build_absolute_uri(static('assets/img/inicio/valmo.png'))

    Cliente = request.POST['cliente']
    Fecha = request.POST['fechaInicial']
    Fecha2 = request.POST['fechaFinal']    

    dataInput = request.POST.get('reporte-movimiento-animales-cliente', '')
    if dataInput is not None and dataInput != '':
        if Cliente == 'todos':
            consulta_sql = """SELECT TT.CLIENTE, TT.CORRALES, TT.ENTRADAS, TT.SALIDAS, TT.ENTRADAS-TT.SALIDAS AS TOTA
            FROM (SELECT  Aplicacion_tblclientes.Nombre AS CLIENTE, Aplicacion_tblcorrales.Descripcion AS CORRALES,
            SUM(case WHEN Aplicacion_tblmovimientoanimales.IDMovimiento_id = 1 AND DATE(Aplicacion_tblmovimientoanimales.Fecha) BETWEEN DATE(Aplicacion_tblcorrales.FechaAsigna) 
            AND %s THEN  Aplicacion_tbldetallemovanimales.Cantidad ELSE 0 END) AS ENTRADAS,
            SUM(case WHEN  Aplicacion_tblmovimientoanimales.IDMovimiento_id = 2 AND DATE(Aplicacion_tblmovimientoanimales.Fecha) BETWEEN DATE(Aplicacion_tblcorrales.FechaAsigna) 
            AND %s THEN  Aplicacion_tbldetallemovanimales.Cantidad ELSE 0 END) AS SALIDAS
            FROM  Aplicacion_tblmovimientoanimales
            INNER JOIN Aplicacion_tblclientes ON Aplicacion_tblclientes.ID = Aplicacion_tblmovimientoanimales. IDCliente_id 
            INNER JOIN Aplicacion_tblcorrales ON  Aplicacion_tblcorrales.ID = Aplicacion_tblmovimientoanimales.IDCorral_id 
            INNER JOIN Aplicacion_tbldetallemovanimales ON  Aplicacion_tblmovimientoanimales.Folio = Aplicacion_tbldetallemovanimales.IDFolio
            WHERE  Aplicacion_tblmovimientoanimales. IDCliente_id IN (SELECT Aplicacion_tblcorrales.IDCliente_id FROM Aplicacion_tblcorrales WHERE Aplicacion_tblcorrales.IDCliente_id  > 1 )
            GROUP BY Aplicacion_tblmovimientoanimales. IDCliente_id) AS  TT ORDER BY TT.CLIENTE"""
            with connection.cursor() as cursor:
                cursor.execute(consulta_sql, [Fecha, Fecha])
                reportes = cursor.fetchall()
            Nombre = 'En general'
            Cliente = 'todos'
        
        else:
            consulta_sql = """SELECT TT.CLIENTE, TT.CORRAL, TT.ENTRADAS, TT.SALIDAS, TT.ENTRADAS-TT.SALIDAS AS TOTA
            FROM (SELECT Aplicacion_tblclientes.Nombre AS CLIENTE, Aplicacion_tblcorrales.Descripcion AS CORRAL, DATE(Aplicacion_tblcorrales.FechaAsigna) AS FECHA,
            SUM(case WHEN   Aplicacion_tblmovimientoanimales.IDMovimiento_id = 1 AND  DATE(Aplicacion_tblmovimientoanimales.Fecha) BETWEEN DATE(Aplicacion_tblcorrales.FechaAsigna) 
                AND %s THEN   Aplicacion_tbldetallemovanimales.Cantidad ELSE 0 END) AS ENTRADAS,
            SUM(case WHEN   Aplicacion_tblmovimientoanimales.IDMovimiento_id = 2 AND  DATE(Aplicacion_tblmovimientoanimales.Fecha) BETWEEN DATE(Aplicacion_tblcorrales.FechaAsigna) 
                AND %s THEN   Aplicacion_tbldetallemovanimales.Cantidad   ELSE 0 END) AS SALIDAS
            FROM   Aplicacion_tblmovimientoanimales
            INNER JOIN Aplicacion_tblclientes ON Aplicacion_tblclientes.ID =  Aplicacion_tblmovimientoanimales.IDCliente_id 
            INNER JOIN Aplicacion_tblcorrales ON  Aplicacion_tblcorrales.ID =  Aplicacion_tblmovimientoanimales.IDCorral_id
            INNER JOIN Aplicacion_tbldetallemovanimales ON  Aplicacion_tblmovimientoanimales.Folio = Aplicacion_tbldetallemovanimales.IDFolio
            WHERE   Aplicacion_tblmovimientoanimales.IDCorral_id IN 
                (SELECT Aplicacion_tblcorrales.ID FROM Aplicacion_tblcorrales WHERE Aplicacion_tblcorrales.IDCliente_id = %s) 
                AND  Aplicacion_tblmovimientoanimales.IDCliente_id = %s
            GROUP BY  Aplicacion_tblmovimientoanimales.IDCorral_id) AS  TT
            ORDER BY TT.CORRAL"""
            with connection.cursor() as cursor:
                cursor.execute(
                    consulta_sql, [Fecha, Fecha, Cliente, Cliente])
                reportes = cursor.fetchall()
            TECliente = tblClientes.objects.get(ID=Cliente)
            Nombre = TECliente.Nombre
        
    # Render the HTML template with the data
    html_string = render_to_string('Descargas/PDF/ReporteAnimales/Cliente.html', {'logo_url': logo_url,
    'formatoClave':formatoClave, 'fecha_actual': fecha_actual, 'reportes': reportes, 'Nombre': Nombre})

    # Create a BytesIO buffer to receive the PDF
    pdf_buffer = BytesIO()

    # Generate the PDF using xhtml2pdf
    pisa.CreatePDF(html_string, dest=pdf_buffer)

    # Get the PDF content from the buffer
    pdf_file = pdf_buffer.getvalue()

    # Create an HTTP response with the attached PDF file
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Movimientos Animales Por Cliente {formatted_fecha_actual}.pdf"'
    return response
# -----------------------------------------------------------------------------------------------------------------------------------------------------

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#!<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>!

#!<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>!
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# ----------------------------------------------- Funciones referenciadas para los reportes anteriores ------------------------------------------------
def CalculaDiasAnimal(IDCliente, IDCorral, FechaInicial, FechaFinal):
    ListaTem = []
    ListaForRet = []
    FechasOcupa = RangoFechasOcupaCorral(IDCorral, IDCliente)
    if FechasOcupa[0][1] == 0:
        pass
    elif FechasOcupa[0][1] < FechaFinal:
        FechaFinal = FechaFinal

    # -----------------------------------------------------------------------
    ListaFechas = GeneraListaFechas(FechaInicial, FechaFinal)
    AcuDiasAnimal = 0

    for i, fecha in enumerate(ListaFechas):
        ListaTem.append(fecha)
        ListaTem.append(CantidadActualAnimales(IDCorral, fecha))
        ListaForRet.append(ListaTem)
        ListaTem = []

    for d, item in enumerate(ListaForRet):
        if int(item[1]) > -1:
            AcuDiasAnimal = AcuDiasAnimal+int(item[1])

    return AcuDiasAnimal

# Saca el rango de fechas
def RangoFechasOcupaCorral(IDCorral, IDCliente):
    query = """SELECT FECHAS.FECHA_ASIGNA,(SELECT(CASE WHEN FECHAS.FECHA_LIBERA > FECHAS.FECHA_ASIGNA THEN FECHAS.FECHA_LIBERA ELSE 0 END)) AS FECHA_LIBERA
        FROM ( SELECT 
        MAX(CASE WHEN Aplicacion_tblasignacorrales.IDCorral_id = %s AND Aplicacion_tblasignacorrales.IDCliente_id= %s  AND Aplicacion_tblasignacorrales.TipoMov_id = 1  
        THEN Aplicacion_tblasignacorrales.Fecha ELSE 0 END) AS FECHA_ASIGNA,
        MAX(CASE WHEN Aplicacion_tblasignacorrales.IDCorral_id = %s AND Aplicacion_tblasignacorrales.IDCliente_id= %s  AND Aplicacion_tblasignacorrales.TipoMov_id = 0  
        THEN Aplicacion_tblasignacorrales.Fecha ELSE 0 END) AS FECHA_LIBERA
        FROM Aplicacion_tblasignacorrales ) AS FECHAS"""

    with connection.cursor() as cursor:
        cursor.execute(query, [IDCorral, IDCliente, IDCorral, IDCliente])
        Datos = cursor.fetchall()
    return Datos

# Genera una lista de fechas a partir de una inicial y final
def GeneraListaFechas(ff, fi):
    FechaInicial = datetime.strptime(ff, '%Y-%m-%d')
    FechaFinal = datetime.strptime(fi, '%Y-%m-%d')
    Fecha = FechaInicial
    ListaFechas = [Fecha.strftime('%Y-%m-%d'), ]

    cnt = 0
    while Fecha != FechaFinal:
        cnt += 1
        if cnt > 30:
            break
        Fecha = Fecha + timedelta(days=1)
        ListaFechas.append(Fecha.strftime('%Y-%m-%d'))
    return ListaFechas

# Obtiene  la cantidad de animales en el corral desde la fecha de asignacion hasta la fecha proporcionada
def CantidadActualAnimales(IDCorral, fecha):
    query = """SELECT  SUM(case WHEN  Aplicacion_tblmovimientoanimales.IDMovimiento_id = 1  THEN  Aplicacion_tbldetallemovanimales.Cantidad ELSE 0 END) -
    SUM(case WHEN  Aplicacion_tblmovimientoanimales.IDMovimiento_id = 2  THEN  Aplicacion_tbldetallemovanimales.Cantidad  ELSE 0 END) AS SUMA
    FROM Aplicacion_tblmovimientoanimales 
    INNER JOIN Aplicacion_tbldetallemovanimales ON Aplicacion_tblmovimientoanimales.Folio = Aplicacion_tbldetallemovanimales.IDFolio
    WHERE Aplicacion_tblmovimientoanimales.IDCorral_id= %s  AND Aplicacion_tblmovimientoanimales.Fecha BETWEEN 
    (SELECT FechaAsigna FROM Aplicacion_tblcorrales WHERE Aplicacion_tblcorrales.ID= %s ) AND %s"""

    with connection.cursor() as cursor:
        cursor.execute(query, [IDCorral, IDCorral, fecha])
        Cantidad = cursor.fetchall()

    if Cantidad[0][0] is None:
        return -1
    else:
        return Cantidad[0][0]
# -----------------------------------------------------------------------------------------------------------------------------------------------------
