from django.shortcuts import render
from datetime import datetime, timedelta
# LLAMAR ARCHIVOS LOCALES
from django.db.models import Q
from Aplicacion.forms import *
from Aplicacion.models import *
from django.db import connection
import mysql.connector
import sqlite3
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< TABLAS DE REPORTES >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# ------------------------------------------------REPORTES DE MATERIAS PRIMAS---------------------------------------------------


def reporteMovEntradaMP(request):
    FContenedores = tblContenedoresMateriaPrima.objects.all().order_by('Cliente')
    FechaDia = datetime.now().strftime('%Y-%m-%d')
    FechaDeHoy = datetime.now().strftime('%Y-%m-%d')

    if request.method == 'POST':
        Contenedor = request.POST.get('contenedor')
        Fecha = request.POST.get('fecha1')
        Fecha2 = request.POST.get('fecha2')
        print(Contenedor)
        if Contenedor == 'todos':

            reportes = tblEntradaMP.objects.filter(fecha__range=[Fecha, Fecha2]).values('ID', 'notas',
                    'fecha', 'IDMateriaPrima_id__Descripcion', 'IDAlmacen_id__Cliente', 'cantidad').order_by('fecha')
            Nombre = 'Se trajeron todos los clientes'
        else:
            # Consulta los registros de tblEntradaMP para un contenedor específico en el rango de fechas
            reportes = tblEntradaMP.objects.filter(IDAlmacen__IDCliente=Contenedor, fecha__range=[Fecha, Fecha2]).values('ID','notas',
                'fecha', 'IDMateriaPrima_id__Descripcion', 'IDAlmacen_id__Cliente', 'cantidad').order_by('fecha')
            TEContenedores = tblContenedoresMateriaPrima.objects.get(IDCliente_id=Contenedor)
            Nombre = TEContenedores.Cliente
        return render(request, 'Reportes/MovimientosMP/EntradaMP.html', {
            'FContenedores': FContenedores, 'reportes': reportes, 'Nombre': Nombre, 'Contenedor': Contenedor, 'Fecha': Fecha, 'Fecha2': Fecha2,
        })
    else:
        reportes = tblEntradaMP.objects.filter(fecha__date=FechaDia).values('ID', 'notas',
                                                                            'fecha', 'IDMateriaPrima_id__Descripcion', 'IDAlmacen_id__Cliente', 'cantidad').order_by('fecha')
        Nombre = 'Buscar cliente'
        Contenedor = ''
    print("Hola mundo")
    return render(request, 'Reportes/MovimientosMP/EntradaMP.html', {'FContenedores': FContenedores, 'reportes': reportes, 'FechaDeHoy': FechaDeHoy, 
                                                                         'Nombre': Nombre, 'Contenedor': Contenedor})


def reporteMovSalidaMP(request):
    FContenedores = tblContenedoresMateriaPrima.objects.all().order_by('Cliente')
    FechaDia = datetime.now().strftime('%Y-%m-%d')
    FechaDeHoy = datetime.now().strftime('%Y-%m-%d')

    if request.method == 'POST':
        Contenedor = request.POST.get('contenedor')
        Fecha = request.POST.get('fecha1')
        Fecha2 = request.POST.get('fecha2')
        print(Contenedor)
        if Contenedor == 'todos':
            reportes = tblSalidaMP.objects.filter(fecha__range=[Fecha, Fecha2]) \
                .values('IDFolio', 'fecha', 'IDMateriaPrima__Descripcion', 'IDAlmacen__Cliente', 'cantidad', 'notas') \
                .order_by('fecha')
            Nombre = 'Se trajeron todos los clientes'
        else:
            reportes = tblSalidaMP.objects.filter(IDAlmacen__IDCliente=Contenedor, fecha__range=[Fecha, Fecha2]) \
                .values('IDFolio', 'fecha', 'IDMateriaPrima__Descripcion', 'IDAlmacen__Cliente', 'cantidad', 'notas') \
                .order_by('fecha')
            TEContenedores = tblContenedoresMateriaPrima.objects.get(IDCliente_id=Contenedor)
            Nombre = TEContenedores.Cliente

        return render(request, 'Reportes/MovimientosMP/SalidaMP.html', {
            'FContenedores': FContenedores, 'Contenedor': Contenedor, 'reportes': reportes, 'Nombre': Nombre, 'Fecha': Fecha, 'Fecha2': Fecha2,
        })
    else:
        # Consulta todos los registros de tblSalidaMP para la fecha actual
        reportes = tblSalidaMP.objects.filter(fecha__date=FechaDia) \
            .values('IDFolio', 'fecha', 'IDMateriaPrima__Descripcion', 'IDAlmacen__Cliente', 'cantidad', 'notas') \
            .order_by('fecha')
        Nombre = 'Buscar cliente'   
        Contenedor = ''

        return render(request, 'Reportes/MovimientosMP/SalidaMP.html', {
            'FContenedores': FContenedores, 'reportes': reportes, 'FechaDeHoy': FechaDeHoy, 'Nombre': Nombre, 'Contenedor': Contenedor,
        })

# ------------------------------------------------REPORTES ANIMALES--------------------------------------------------------------------------
# NUEVO REPORTE DE ANIMALES
def reporteAnimalesMovimientos(request):
    FechaDeHoy = datetime.now().strftime('%Y-%m-%d')
    FClientes = tblClientes.objects.exclude(ID=1).order_by('Nombre')
    FMovimientos = tblTipoMov.objects.filter(ID__range=(1, 2))

    if request.method == 'POST':
        if 'reportes' in request.POST:
            Cliente = request.POST.get('cliente')
            Movimiento_v = request.POST.get('mov')
            Fecha = request.POST.get('fecha1')
            Fecha2 = request.POST.get('fecha2')
            TEMov = tblTipoMov.objects.get(ID=Movimiento_v)
            Movimiento = TEMov.Descripcion            
            if Cliente == 'todos':
                consulta_sql = """SELECT Aplicacion_tbldetallemovanimales.IDFolio, Aplicacion_tblclientes.Nombre, Aplicacion_tbldetallemovanimales.Cantidad,
                Aplicacion_tblAnimalesTipo.Descripcion,Aplicacion_tbldetallemovanimales.PesoTotal, Aplicacion_tblcorrales.Descripcion
                FROM  Aplicacion_tblmovimientoanimales
                INNER JOIN Aplicacion_tblclientes ON Aplicacion_tblclientes.ID = Aplicacion_tblmovimientoanimales.IDCliente_id 
                INNER JOIN Aplicacion_tbldetallemovanimales ON  Aplicacion_tblmovimientoanimales.Folio = Aplicacion_tbldetallemovanimales.IDFolio
                INNER JOIN Aplicacion_tblcorrales ON Aplicacion_tblcorrales.ID = Aplicacion_tbldetallemovanimales.IDCorral_id
                INNER JOIN Aplicacion_tblAnimalesTipo ON Aplicacion_tblAnimalesTipo.ID = Aplicacion_tbldetallemovanimales.IDAnimales_id 
                WHERE DATE(Aplicacion_tblmovimientoanimales.Fecha) BETWEEN %s AND %s AND Aplicacion_tblmovimientoanimales.IDMovimiento_id = %s
                ORDER by Aplicacion_tbldetallemovanimales.IDFolio ASC"""

                with connection.cursor() as cursor:
                    cursor.execute(
                        consulta_sql, [Fecha, Fecha2, Movimiento_v])
                    reportes = cursor.fetchall()
                Nombre = 'Se trajeron todos los clientes'
                Cliente = 'todos'
                return render(request, 'Reportes/NuevoAnimales/MovimientoAnimales.html', {'reportes': reportes, 'FMovimientos':FMovimientos,
                'FClientes': FClientes, 'Nombre': Nombre, 'Cliente': Cliente, 'Fecha': Fecha, 'Fecha2': Fecha2, 'Movimiento':Movimiento, 'Movimiento_v':Movimiento_v})
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
                ORDER by Aplicacion_tbldetallemovanimales.IDFolio ASC"""

                with connection.cursor() as cursor:
                    cursor.execute(
                        consulta_sql, [Cliente, Fecha, Fecha2, Movimiento_v])
                    reportes = cursor.fetchall()
                TECliente = tblClientes.objects.get(ID=Cliente)
                Nombre = TECliente.Nombre
                return render(request, 'Reportes/NuevoAnimales/MovimientoAnimales.html', {'reportes': reportes, 'FMovimientos':FMovimientos,
                'FClientes': FClientes, 'Nombre': Nombre, 'Cliente': Cliente, 'Fecha': Fecha, 'Fecha2': Fecha2, 'Movimiento':Movimiento, 'Movimiento_v':Movimiento_v})
    else:
        consulta_sql = """SELECT Aplicacion_tbldetallemovanimales.IDFolio, Aplicacion_tblclientes.Nombre, Aplicacion_tbldetallemovanimales.Cantidad,
        Aplicacion_tblAnimalesTipo.Descripcion,Aplicacion_tbldetallemovanimales.PesoTotal, Aplicacion_tblcorrales.Descripcion
        FROM  Aplicacion_tblmovimientoanimales
        INNER JOIN Aplicacion_tblclientes ON Aplicacion_tblclientes.ID = Aplicacion_tblmovimientoanimales.IDCliente_id 
        INNER JOIN Aplicacion_tbldetallemovanimales ON  Aplicacion_tblmovimientoanimales.Folio = Aplicacion_tbldetallemovanimales.IDFolio
        INNER JOIN Aplicacion_tblcorrales ON Aplicacion_tblcorrales.ID = Aplicacion_tbldetallemovanimales.IDCorral_id
        INNER JOIN Aplicacion_tblAnimalesTipo ON Aplicacion_tblAnimalesTipo.ID = Aplicacion_tbldetallemovanimales.IDAnimales_id 
        ORDER by Aplicacion_tbldetallemovanimales.IDFolio ASC"""
        with connection.cursor() as cursor:
            cursor.execute(consulta_sql)
            reportes = cursor.fetchall()
        Nombre = 'Buscar cliente'
        Cliente = ''
        return render(request, 'Reportes/NuevoAnimales/MovimientoAnimales.html', {'reportes': reportes, 'FMovimientos':FMovimientos,
                'FechaDeHoy': FechaDeHoy, 'FClientes': FClientes, 'Nombre': Nombre, 'Cliente': Cliente})
    

# NUEVO REPORTES ANIMALES
def reportePorClientes(request):
    FechaDeHoy = datetime.now().strftime('%Y-%m-%d')
    FClientes = tblClientes.objects.exclude(ID=1).order_by('Nombre')

    if request.method == 'POST':
        if 'reportes' in request.POST:
            Cliente = request.POST.get('cliente')
            Fecha = request.POST.get('fecha1')

            if Cliente == 'todos':
                consulta_sql = """SELECT TT.CLIENTE, TT.CORRALES, TT.ENTRADAS, TT.SALIDAS, TT.ENTRADAS-TT.SALIDAS AS TOTA
                FROM (SELECT  Aplicacion_tblclientes.Nombre AS CLIENTE, Aplicacion_tblcorrales.Descripcion AS CORRALES,
                SUM(case WHEN Aplicacion_tblmovimientoanimales.IDMovimiento_id = 1 AND DATE(Aplicacion_tblmovimientoanimales.Fecha) BETWEEN DATE(Aplicacion_tblcorrales.FechaAsigna) 
                AND %s THEN  Aplicacion_tbldetallemovanimales.Cantidad ELSE 0 END) AS ENTRADAS,
                SUM(case WHEN  Aplicacion_tblmovimientoanimales.IDMovimiento_id = 2 AND DATE(Aplicacion_tblmovimientoanimales.Fecha) BETWEEN DATE(Aplicacion_tblcorrales.FechaAsigna) 
                AND %s THEN  Aplicacion_tbldetallemovanimales.Cantidad ELSE 0 END) AS SALIDAS
                FROM  Aplicacion_tblmovimientoanimales
                INNER JOIN Aplicacion_tblclientes ON Aplicacion_tblclientes.ID = Aplicacion_tblmovimientoanimales. IDCliente_id 
                INNER JOIN Aplicacion_tbldetallemovanimales ON  Aplicacion_tblmovimientoanimales.Folio = Aplicacion_tbldetallemovanimales.IDFolio
                INNER JOIN Aplicacion_tblcorrales ON  Aplicacion_tblcorrales.ID = Aplicacion_tbldetallemovanimales.IDCorral_id 
                WHERE  Aplicacion_tblmovimientoanimales.IDCliente_id IN (SELECT Aplicacion_tblcorrales.IDCliente_id FROM Aplicacion_tblcorrales WHERE Aplicacion_tblcorrales.IDCliente_id  > 1 )
                GROUP BY Aplicacion_tblmovimientoanimales.IDCliente_id) AS  TT ORDER BY TT.CLIENTE"""

                with connection.cursor() as cursor:
                    cursor.execute(consulta_sql, [Fecha, Fecha])
                    reportes = cursor.fetchall()
                Nombre = 'Se trajeron todos los clientes'
                Cliente = 'todos'
                return render(request, 'Reportes/Animales/MovimientosClientes.html', {'reportes': reportes,
                                                                                      'FClientes': FClientes, 'Nombre': Nombre, 'Cliente': Cliente, 'Fecha': Fecha})
            else:
                consulta_sql = """SELECT TT.CLIENTE, TT.CORRAL, TT.ENTRADAS, TT.SALIDAS, TT.ENTRADAS-TT.SALIDAS AS TOTA
                FROM (SELECT Aplicacion_tblclientes.Nombre AS CLIENTE, Aplicacion_tblcorrales.Descripcion AS CORRAL , DATE(Aplicacion_tblcorrales.FechaAsigna) AS FECHA,
                SUM(case WHEN   Aplicacion_tblmovimientoanimales.IDMovimiento_id = 1 AND  DATE(Aplicacion_tblmovimientoanimales.Fecha) BETWEEN DATE(Aplicacion_tblcorrales.FechaAsigna) 
                    AND %s THEN   Aplicacion_tbldetallemovanimales.Cantidad ELSE 0 END) AS ENTRADAS,
                SUM(case WHEN   Aplicacion_tblmovimientoanimales.IDMovimiento_id = 2 AND  DATE(Aplicacion_tblmovimientoanimales.Fecha) BETWEEN DATE(Aplicacion_tblcorrales.FechaAsigna) 
                    AND %s THEN   Aplicacion_tbldetallemovanimales.Cantidad   ELSE 0 END) AS SALIDAS
                FROM   Aplicacion_tblmovimientoanimales
                INNER JOIN Aplicacion_tblclientes ON Aplicacion_tblclientes.ID =  Aplicacion_tblmovimientoanimales.IDCliente_id 
                INNER JOIN Aplicacion_tbldetallemovanimales ON  Aplicacion_tblmovimientoanimales.Folio = Aplicacion_tbldetallemovanimales.IDFolio
                INNER JOIN Aplicacion_tblcorrales ON  Aplicacion_tblcorrales.ID =  Aplicacion_tbldetallemovanimales.IDCorral_id
                WHERE   Aplicacion_tbldetallemovanimales.IDCorral_id IN 
                    (SELECT Aplicacion_tblcorrales.ID FROM Aplicacion_tblcorrales WHERE Aplicacion_tblcorrales.IDCliente_id = %s) 
                    AND  Aplicacion_tblmovimientoanimales.IDCliente_id = %s
                GROUP BY  Aplicacion_tblmovimientoanimales.IDCliente_id) AS  TT
                ORDER BY TT.CORRAL"""

                with connection.cursor() as cursor:
                    cursor.execute(
                        consulta_sql, [ Cliente, Cliente])
                    reportes = cursor.fetchall()
                TECliente = tblClientes.objects.get(ID=Cliente)
                Nombre = TECliente.Nombre
                return render(request, 'Reportes/Animales/MovimientosClientes.html', {'reportes': reportes,
                                                                                      'FClientes': FClientes, 'Nombre': Nombre, 'Cliente': Cliente, 'Fecha': Fecha})
    else:
        consulta_sql = """SELECT TT.CLIENTE, 0, TT.ENTRADAS, TT.SALIDAS, TT.ENTRADAS-TT.SALIDAS AS TOTA
        FROM (SELECT  Aplicacion_tblclientes.Nombre AS CLIENTE,
        SUM(case WHEN Aplicacion_tblmovimientoanimales.IDMovimiento_id = 1 AND DATE(Aplicacion_tblmovimientoanimales.Fecha) BETWEEN DATE(Aplicacion_tblcorrales.FechaAsigna) 
        AND %s THEN  Aplicacion_tbldetallemovanimales.Cantidad ELSE 0 END) AS ENTRADAS,
        SUM(case WHEN  Aplicacion_tblmovimientoanimales.IDMovimiento_id = 2 AND DATE(Aplicacion_tblmovimientoanimales.Fecha) BETWEEN DATE(Aplicacion_tblcorrales.FechaAsigna) 
        AND %s THEN  Aplicacion_tbldetallemovanimales.Cantidad ELSE 0 END) AS SALIDAS
        FROM  Aplicacion_tblmovimientoanimales
        INNER JOIN Aplicacion_tblclientes ON Aplicacion_tblclientes.ID = Aplicacion_tblmovimientoanimales.IDCliente_id 
		INNER JOIN Aplicacion_tbldetallemovanimales ON  Aplicacion_tblmovimientoanimales.Folio = Aplicacion_tbldetallemovanimales.IDFolio
        INNER JOIN Aplicacion_tblcorrales ON  Aplicacion_tblcorrales.ID = Aplicacion_tbldetallemovanimales.IDCorral_id 
        WHERE  Aplicacion_tblmovimientoanimales.IDCliente_id IN (SELECT Aplicacion_tblcorrales.IDCliente_id FROM Aplicacion_tblcorrales WHERE Aplicacion_tblcorrales.IDCliente_id  > 1 )
        GROUP BY Aplicacion_tblmovimientoanimales.IDCliente_id) AS  TT ORDER BY TT.CLIENTE"""
        with connection.cursor() as cursor:
            cursor.execute(consulta_sql, [FechaDeHoy, FechaDeHoy])
            reportes = cursor.fetchall()
        Nombre = 'Buscar cliente'
        Cliente = ''
        return render(request, 'Reportes/Animales/MovimientosClientes.html', {'reportes': reportes,
                                                                              'FechaDeHoy': FechaDeHoy, 'FClientes': FClientes, 'Nombre': Nombre, 'Cliente': Cliente})


# REPORTES DE ANIMALES
def reporteAnimalesMovimientos2(request):
    FechaDia = datetime.now().strftime('%Y-%m-%d')
    FechaDeHoy = datetime.now().strftime('%Y-%m-%d')
    FClientes = tblClientes.objects.exclude(ID=1).order_by('Nombre')

    if request.method == 'POST':
        if 'reportes' in request.POST:
            Cliente = request.POST.get('cliente')
            Fecha = request.POST.get('fecha1')
            Fecha2 = request.POST.get('fecha2')

            if Cliente == 'todos':
                reportes = tblMovimientoAnimales.objects.filter(Fecha__range=[Fecha, Fecha2]) \
                    .exclude(IDCliente=1) \
                    .values('Folio', 'Fecha', 'IDCliente__Nombre', 'IDCorral__Descripcion', 'IDMovimiento__Descripcion') \
                    .order_by('Folio')
                Nombre = 'Se trajeron todos los clientes'
                Cliente = 'todos'
            else:
                reportes = tblMovimientoAnimales.objects.filter(
                    Q(IDCliente=Cliente) & Q(Fecha__range=[
                        Fecha, Fecha2]) & ~Q(IDCliente=1)
                ).values('Folio', 'Fecha', 'IDCliente__Nombre', 'IDCorral__Descripcion', 'IDMovimiento__Descripcion') \
                    .order_by('Folio')
                TECliente = tblClientes.objects.get(ID=Cliente)
                Nombre = TECliente.Nombre

            return render(request, 'Reportes/Animales/MovimientoAnimales.html', {
                'reportes': reportes, 'FClientes': FClientes, 'Nombre': Nombre, 'Cliente': Cliente, 'Fecha': Fecha, 'Fecha2': Fecha2,
            })
    else:
        reportes = tblMovimientoAnimales.objects.filter(Fecha__date=FechaDia).exclude(IDCliente=1) \
            .values('Folio', 'Fecha', 'IDCliente__Nombre', 'IDCorral__Descripcion', 'IDMovimiento__Descripcion') \
            .order_by('Folio')
        Nombre = 'Buscar cliente'
        Cliente = ''

        return render(request, 'Reportes/Animales/MovimientoAnimales.html', {
            'reportes': reportes, 'FechaDeHoy': FechaDeHoy, 'FClientes': FClientes, 'Nombre': Nombre, 'Cliente': Cliente,
        })

# REPORTES ANIMALES
def reportePorClientes2(request):
    FechaDeHoy = datetime.now().strftime('%Y-%m-%d')
    FClientes = tblClientes.objects.exclude(ID=1).order_by('Nombre')

    if request.method == 'POST':
        if 'reportes' in request.POST:
            Cliente = request.POST.get('cliente')
            Fecha = request.POST.get('fecha1')

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
                Nombre = 'Se trajeron todos los clientes'
                Cliente = 'todos'
                return render(request, 'Reportes/Animales/MovimientosClientes.html', {'reportes': reportes,
                                                                                      'FClientes': FClientes, 'Nombre': Nombre, 'Cliente': Cliente, 'Fecha': Fecha})
            else:
                consulta_sql = """SELECT TT.CLIENTE, TT.CORRAL, TT.ENTRADAS, TT.SALIDAS, TT.ENTRADAS-TT.SALIDAS AS TOTA
                FROM (SELECT Aplicacion_tblclientes.Nombre AS CLIENTE, Aplicacion_tblcorrales.Descripcion AS CORRAL , DATE(Aplicacion_tblcorrales.FechaAsigna) AS FECHA,
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
                return render(request, 'Reportes/Animales/MovimientosClientes.html', {'reportes': reportes,
                                                                                      'FClientes': FClientes, 'Nombre': Nombre, 'Cliente': Cliente, 'Fecha': Fecha})
    else:
        consulta_sql = """SELECT TT.CLIENTE, 0, TT.ENTRADAS, TT.SALIDAS, TT.ENTRADAS-TT.SALIDAS AS TOTA
        FROM (SELECT  Aplicacion_tblclientes.Nombre AS CLIENTE,
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
            cursor.execute(consulta_sql, [FechaDeHoy, FechaDeHoy])
            reportes = cursor.fetchall()
        Nombre = 'Buscar cliente'
        Cliente = ''
        return render(request, 'Reportes/Animales/MovimientosClientes.html', {'reportes': reportes,
                                                                              'FechaDeHoy': FechaDeHoy, 'FClientes': FClientes, 'Nombre': Nombre, 'Cliente': Cliente})

# REPORTES DE ANIMALES
def reportePorClientesCorrales(request):
    FechaDeHoy = datetime.now().strftime('%Y-%m-%d')
    FClientes = tblClientes.objects.exclude(ID=1).order_by('Nombre')
    if request.method == 'POST':
        if 'reportes' in request.POST:
            Cliente = request.POST.get('cliente')
            Fecha = request.POST.get('fecha1')
            Fecha2 = request.POST.get('fecha2')
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
                GROUP BY Aplicacion_tblmovimientoanimales.IDCorral_id, Aplicacion_tblclientes.Nombre"""

                with connection.cursor() as cursor:
                    cursor.execute(
                        consulta_sql, [Fecha2, Fecha2, Fecha, Fecha2, Fecha, Fecha2])
                    reportes = cursor.fetchall()
                Nombre = 'Se trajeron todos los clientes'
                Cliente = 'todos'
                return render(request, 'Reportes/Animales/PorClienteCorral.html', {'reportes': reportes,
                                                                                   'FClientes': FClientes, 'Nombre': Nombre, 'Cliente': Cliente, 'Fecha': Fecha, 'Fecha2': Fecha2})
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
                return render(request, 'Reportes/Animales/PorClienteCorral.html', {'reportes': reportes,
                                                                                   'FClientes': FClientes, 'Nombre': Nombre, 'Cliente': Cliente, 'Fecha': Fecha, 'Fecha2': Fecha2})
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
        WHERE  Aplicacion_tblmovimientoanimales.IDCorral_id IN (SELECT  Aplicacion_tblcorrales.ID FROM Aplicacion_tblcorrales)
        GROUP BY Aplicacion_tblmovimientoanimales.IDCorral_id, Aplicacion_tblclientes.Nombre"""
        with connection.cursor() as cursor:
            cursor.execute(consulta_sql, [
                           FechaDeHoy, FechaDeHoy, FechaDeHoy, FechaDeHoy, FechaDeHoy, FechaDeHoy])
            reportes = cursor.fetchall()
        Nombre = 'Buscar cliente'
        Cliente = ''
        return render(request, 'Reportes/Animales/PorClienteCorral.html', {'reportes': reportes,
                                                                           'FechaDeHoy': FechaDeHoy, 'FClientes': FClientes, 'Nombre': Nombre, 'Cliente': Cliente})

# ------------------------------------------------REPORTES SERVIDOS--------------------------------------------------------------------------
# REPORTES DE SERVIDOS
def reporteServidosMovimientos(request):
    FechaDeHoy = datetime.now().strftime('%Y-%m-%d')
    FClientes = tblClientes.objects.exclude(ID=1).order_by('Nombre')

    if request.method == 'POST':
        if 'reportes' in request.POST:
            Cliente = request.POST.get('cliente')
            Fecha = request.POST.get('fecha1')
            Fecha2 = request.POST.get('fecha2')
            if Cliente == 'todos':
                consulta_sql = """SELECT DISTINCT Aplicacion_tblservido.ID, Aplicacion_tblclientes.Nombre, 
                    Aplicacion_tblcorrales.Descripcion,  Aplicacion_tblproductos.Descripcion,
                    Aplicacion_tblservido.CantidadSolicitada, Aplicacion_tblservido.CantidadServida,
                    Aplicacion_tblservido.Fecha, Aplicacion_tblservido.FechaServida
                    FROM Aplicacion_tblservido
                    LEFT JOIN Aplicacion_tblproductos ON Aplicacion_tblservido.IDProducto_id = Aplicacion_tblproductos.ID
                    LEFT JOIN Aplicacion_tblclientes ON Aplicacion_tblservido.IDCliente_id = Aplicacion_tblclientes.ID
                    LEFT JOIN Aplicacion_tblcorrales ON Aplicacion_tblservido.IDCorral_id = Aplicacion_tblcorrales.ID
                    WHERE Aplicacion_tblservido.Fecha BETWEEN  %s AND  %s and Aplicacion_tblservido.IDCliente_id != 1 and Aplicacion_tblservido.IDEstatus_id = 10 """

                with connection.cursor() as cursor:
                    cursor.execute(consulta_sql, [Fecha, Fecha2])
                    reportes = cursor.fetchall()
                Nombre = 'Se trajeron todos los clientes'
                print(Nombre)
                Cliente = 'todos'
                return render(request, 'Reportes/Servidos/ServidosMovimientos.html', {'reportes': reportes,
                                                                                      'FClientes': FClientes, 'Nombre': Nombre, 'Cliente': Cliente, 'Fecha': Fecha, 'Fecha2': Fecha2})
            else:
                print("Selecciono un cliente")
                consulta_sql = """SELECT DISTINCT Aplicacion_tblservido.ID, Aplicacion_tblclientes.Nombre, 
                    Aplicacion_tblcorrales.Descripcion,  Aplicacion_tblproductos.Descripcion,
                    Aplicacion_tblservido.CantidadSolicitada, Aplicacion_tblservido.CantidadServida,
                    Aplicacion_tblservido.Fecha, Aplicacion_tblservido.FechaServida
                    FROM Aplicacion_tblservido
                    LEFT JOIN Aplicacion_tblproductos ON Aplicacion_tblservido.IDProducto_id = Aplicacion_tblproductos.ID
                    LEFT JOIN Aplicacion_tblclientes ON Aplicacion_tblservido.IDCliente_id = Aplicacion_tblclientes.ID
                    LEFT JOIN Aplicacion_tblcorrales ON Aplicacion_tblservido.IDCorral_id = Aplicacion_tblcorrales.ID
                    WHERE  Aplicacion_tblclientes.ID = %s AND  (Aplicacion_tblservido.Fecha BETWEEN  %s AND  %s) and Aplicacion_tblservido.IDCliente_id != 1 and Aplicacion_tblservido.IDEstatus_id = 10 
                    """
                with connection.cursor() as cursor:
                    cursor.execute(consulta_sql, [Cliente, Fecha, Fecha2])
                    reportes = cursor.fetchall()
                TECliente = tblClientes.objects.get(ID=Cliente)
                Nombre = TECliente.Nombre
                return render(request, 'Reportes/Servidos/ServidosMovimientos.html', {'reportes': reportes,
                                                                                      'FClientes': FClientes, 'Nombre': Nombre, 'Cliente': Cliente, 'Fecha': Fecha, 'Fecha2': Fecha2})
    else:
        consulta_sql = """  
        SELECT DISTINCT Aplicacion_tblservido.ID, Aplicacion_tblclientes.Nombre, Aplicacion_tblcorrales.Descripcion,  
        Aplicacion_tblproductos.Descripcion, Aplicacion_tblservido.CantidadSolicitada, Aplicacion_tblservido.CantidadServida, 
        Aplicacion_tblservido.Fecha, Aplicacion_tblservido.FechaServida FROM Aplicacion_tblservido
        LEFT JOIN Aplicacion_tblproductos  ON Aplicacion_tblservido.ID = Aplicacion_tblproductos.ID
        LEFT JOIN Aplicacion_tblclientes ON Aplicacion_tblservido.ID = Aplicacion_tblclientes.ID
        LEFT JOIN Aplicacion_tblcorrales ON Aplicacion_tblservido.IDCorral_id = Aplicacion_tblcorrales.ID
        WHERE  Aplicacion_tblservido.Fecha BETWEEN  %s AND  %s and Aplicacion_tblservido.IDCliente_id != 1
        """

        with connection.cursor() as cursor:
            cursor.execute(consulta_sql, [FechaDeHoy, FechaDeHoy])
            reportes = cursor.fetchall()
        Nombre = 'Buscar cliente'
        Cliente = ''
        print(Nombre)
        return render(request, 'Reportes/Servidos/ServidosMovimientos.html', {'reportes': reportes,
                                                                              'FechaDeHoy': FechaDeHoy, 'FClientes': FClientes, 'Nombre': Nombre, 'Cliente': Cliente})

# REPORTES SERVIDOS LIQUIDACION
def reporteServidosLiquidacion(request):
    FechaDeHoy = datetime.now().strftime('%Y-%m-%d')
    FClientes = tblClientes.objects.exclude(ID=1).all().order_by('Nombre')

    if request.method == 'POST':
        if 'reportes' in request.POST:
            Cliente = request.POST.get('cliente')
            Fecha = request.POST.get('fecha1')
            Fecha2 = request.POST.get('fecha2')

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

                Nombre = 'Se trajeron todos los clientes'
                Cliente = 'todos'

                return render(request, 'Reportes/Servidos/ServidosLiquidacion.html', {'reportes': reportes, 'reportes2': reportes2,
                'FClientes': FClientes, 'Nombre': Nombre, 'Cliente': Cliente, 'Fecha': Fecha, 'Fecha2': Fecha2,
                'DataToRep':DataToRep})
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
                return render(request, 'Reportes/Servidos/ServidosLiquidacion.html', {'reportes': reportes, 'reportes2': reportes2,
                'FClientes': FClientes, 'Nombre': Nombre, 'Cliente': Cliente, 'Fecha': Fecha, 'Fecha2': Fecha2, 'DataToRep':DataToRep})
    else:
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
            cursor.execute(consulta_sql, [FechaDeHoy, FechaDeHoy])
            reportes = cursor.fetchall()

        Nombre = 'Buscar cliente'
        Cliente = ''
        return render(request, 'Reportes/Servidos/ServidosLiquidacion.html', {'reportes': reportes,
        'FechaDeHoy': FechaDeHoy, 'FClientes': FClientes, 'Nombre': Nombre, 'Cliente': Cliente})

def reporteServidosPromedio(request):
    FechaDeHoy = datetime.now().strftime('%Y-%m-%d %H:%M')
    FClientes = tblClientes.objects.exclude(ID=1).all().order_by('Nombre')
    ListaForRep = []
    ListaTem = []

    if request.method == 'POST':
        if 'reportes' in request.POST:
            Cliente = request.POST.get('cliente')
            Fecha = request.POST.get('fecha1')
            Fecha2 = request.POST.get('fecha2')
            if Cliente == 'todos':
                query = 'SELECT Aplicacion_tblcorrales.Descripcion,'
                IDListaProd = ProductosQueSeSirven(1)
                for k in range(len(IDListaProd)):
                    query = query + \
                        "SUM(CASE WHEN Aplicacion_tblservido.IDProducto_id = %s THEN Aplicacion_tblservido.CantidadServida ELSE 0 END),"
                query = query+"Aplicacion_tblservido.IDCorral_id"
                query = query + """ FROM Aplicacion_tblservido
                                    INNER JOIN Aplicacion_tblcorrales ON Aplicacion_tblcorrales.ID =  Aplicacion_tblservido.IDCorral_id
                            WHERE  Aplicacion_tblservido.IDCliente_id != 1 AND Aplicacion_tblservido.Fecha BETWEEN %s AND %s  and Aplicacion_tblservido.IDEstatus_id = 10 
                            GROUP BY Aplicacion_tblservido.IDCorral_id """
                param = IDListaProd
 
                param.append(Fecha)
                param.append(Fecha2)

                with connection.cursor() as cursor:
                    cursor.execute(query, param)
                    Data = cursor.fetchall()

                TotServido = 0
                Promedio = 0
                for ren, item in enumerate(Data):
                    for col in range(len(item)-1):
                        if col > 0:
                            data = item[col]
                            TotServido = TotServido+item[col]
                        else:
                            data = item[col]
                        ListaTem.append(data)
                    ListaTem.append(TotServido)
                    NoAnimalesActual = CantidadActualAnimales(
                        Data[ren][5], Fecha2)
                    ListaTem.append(NoAnimalesActual)
                    DiasAnimal = CalculaDiasAnimal(
                        Cliente, item[-1], Fecha, Fecha2)
                    ListaTem.append(DiasAnimal)
                    if DiasAnimal > 0:
                        Promedio = TotServido/DiasAnimal
                    else:
                        Promedio = 1
                    Promedio = "{:.3f}".format(Promedio)
                    ListaTem.append(Promedio)
                    ListaForRep.append(ListaTem)
                    ListaTem = []
                    TotServido = 0
                Prod1 = 0
                Prod2 = 0
                Prod3 = 0
                Prod4 = 0
                Prod5 = 0
                TotProd = 0
                TotalAnim = 0
                TotDiasAnima = 0
                FinalRen = []
                ListaTem = []
                for ren, Ren in enumerate(ListaForRep):
                    Prod1 += Ren[1]
                    Prod2 += Ren[2]
                    Prod3 += Ren[3]
                    Prod4 += Ren[4]
                    TotProd += Ren[5]
                    TotalAnim += Ren[6]
                    TotDiasAnima += Ren[7]
                ListaTem.append('Totales')
                ListaTem.append("{:,.2f}".format(Prod1))
                ListaTem.append("{:,.2f}".format(Prod2))
                ListaTem.append("{:,.2f}".format(Prod3))
                ListaTem.append("{:,.2f}".format(Prod4))
                ListaTem.append("{:,.2f}".format(TotProd))
                ListaTem.append("{:,}".format(TotalAnim))
                ListaTem.append("{:,}".format(TotDiasAnima))
                ListaTem.append('NA')
                ListaForRep.append(ListaTem)
                Nombre = 'Se trajeron todos los clientes'
                Cliente = 'todos'
                return render(request, 'Reportes/Servidos/ServidosPromedioDiario.html', {'ListaForRep':ListaForRep,
                'FClientes': FClientes, 'Nombre': Nombre, 'Cliente': Cliente, 'Fecha': Fecha, 'Fecha2': Fecha2})
            else:
                query = 'SELECT Aplicacion_tblcorrales.Descripcion,'
                IDListaProd = ProductosQueSeSirven(1)
                for k in range(len(IDListaProd)):
                    query = query + \
                        "SUM(CASE WHEN Aplicacion_tblservido.IDProducto_id = %s THEN Aplicacion_tblservido.CantidadServida ELSE 0 END),"
                query = query+"Aplicacion_tblservido.IDCorral_id"
                query = query + """ FROM Aplicacion_tblservido
                                    INNER JOIN Aplicacion_tblcorrales ON Aplicacion_tblcorrales.ID =  Aplicacion_tblservido.IDCorral_id
                            WHERE  Aplicacion_tblservido.IDCliente_id = %s AND Aplicacion_tblservido.Fecha BETWEEN %s AND %s  and Aplicacion_tblservido.IDEstatus_id = 10 
                            GROUP BY Aplicacion_tblservido.IDCorral_id """
                param = IDListaProd
                param.append(Cliente)
                param.append(Fecha)
                param.append(Fecha2)

                with connection.cursor() as cursor:
                    cursor.execute(query, param)
                    Data = cursor.fetchall()

                TotServido = 0
                Promedio = 0
                for ren, item in enumerate(Data):
                    for col in range(len(item)-1):
                        if col > 0:
                            data = item[col]
                            TotServido = TotServido+item[col]
                        else:
                            data = item[col]
                        ListaTem.append(data)
                    ListaTem.append(TotServido)
                    NoAnimalesActual = CantidadActualAnimales(
                        Data[ren][5], Fecha2)
                    ListaTem.append(NoAnimalesActual)
                    DiasAnimal = CalculaDiasAnimal(
                        Cliente, item[-1], Fecha, Fecha2)
                    ListaTem.append(DiasAnimal)
                    if DiasAnimal > 0:
                        Promedio = TotServido/DiasAnimal
                    else:
                        Promedio = 1
                    Promedio = "{:.3f}".format(Promedio)
                    ListaTem.append(Promedio)
                    ListaForRep.append(ListaTem)
                    ListaTem = []
                    TotServido = 0
                Prod1 = 0
                Prod2 = 0
                Prod3 = 0
                Prod4 = 0
                Prod5 = 0
                TotProd = 0
                TotalAnim = 0
                TotDiasAnima = 0
                FinalRen = []
                ListaTem = []
                for ren, Ren in enumerate(ListaForRep):
                    Prod1 += Ren[1]
                    Prod2 += Ren[2]
                    Prod3 += Ren[3]
                    Prod4 += Ren[4]
                    TotProd += Ren[5]
                    TotalAnim += Ren[6]
                    TotDiasAnima += Ren[7]
                ListaTem.append('Totales')
                ListaTem.append("{:,.2f}".format(Prod1))
                ListaTem.append("{:,.2f}".format(Prod2))
                ListaTem.append("{:,.2f}".format(Prod3))
                ListaTem.append("{:,.2f}".format(Prod4))
                ListaTem.append("{:,.2f}".format(TotProd))
                ListaTem.append("{:,}".format(TotalAnim))
                ListaTem.append("{:,}".format(TotDiasAnima))
                ListaTem.append('NA')
                ListaForRep.append(ListaTem)
                TECliente = tblClientes.objects.get(ID=Cliente)
                Nombre = TECliente.Nombre
                return render(request, 'Reportes/Servidos/ServidosPromedioDiario.html', {'ListaForRep':ListaForRep,
                'FClientes': FClientes, 'Nombre': Nombre, 'Cliente': Cliente, 'Fecha': Fecha, 'Fecha2': Fecha2})
    else:
        query = 'SELECT Aplicacion_tblcorrales.Descripcion,'
        IDListaProd = ProductosQueSeSirven(1)
        for k in range(len(IDListaProd)):
            query = query + \
                "SUM(CASE WHEN Aplicacion_tblservido.IDProducto_id = %s THEN Aplicacion_tblservido.CantidadServida ELSE 0 END),"
        query = query+"Aplicacion_tblservido.IDCorral_id"
        query = query + """ FROM Aplicacion_tblservido
                            INNER JOIN Aplicacion_tblcorrales ON Aplicacion_tblcorrales.ID =  Aplicacion_tblservido.IDCorral_id
                    WHERE Aplicacion_tblservido.Fecha BETWEEN %s AND %s  and Aplicacion_tblservido.IDEstatus_id = 10 
                    GROUP BY Aplicacion_tblservido.IDCorral_id """
        param = IDListaProd
        param.append(FechaDeHoy)
        param.append(FechaDeHoy)
        with connection.cursor() as cursor:
            cursor.execute(query, param)
            Data = cursor.fetchall()
        TotServido = 0
        Promedio = 0
        for ren, item in enumerate(Data):
            for col in range(len(item)-1):
                if col > 0:
                    data = item[col]
                    TotServido = TotServido+item[col]
                else:
                    data = item[col]
                ListaTem.append(data)
            ListaTem.append(TotServido)
            NoAnimalesActual = CantidadActualAnimales(
                Data[ren][5], Fecha2)
            ListaTem.append(NoAnimalesActual)
            DiasAnimal = CalculaDiasAnimal(
                Cliente, item[-1], Fecha, Fecha2)
            ListaTem.append(DiasAnimal)
            if DiasAnimal > 0:
                Promedio = TotServido/DiasAnimal
            else:
                Promedio = 1
            Promedio = "{:.3f}".format(Promedio)
            ListaTem.append(Promedio)
            ListaForRep.append(ListaTem)
            ListaTem = []
            TotServido = 0
        Prod1 = 0
        Prod2 = 0
        Prod3 = 0
        Prod4 = 0
        Prod5 = 0
        TotProd = 0
        TotalAnim = 0
        TotDiasAnima = 0
        FinalRen = []
        ListaTem = []
        for ren, Ren in enumerate(ListaForRep):
            Prod1 += Ren[1]
            Prod2 += Ren[2]
            Prod3 += Ren[3]
            Prod4 += Ren[4]
            TotProd += Ren[5]
            TotalAnim += Ren[6]
            TotDiasAnima += Ren[7]
        ListaTem.append('Totales')
        ListaTem.append("{:,.2f}".format(Prod1))
        ListaTem.append("{:,.2f}".format(Prod2))
        ListaTem.append("{:,.2f}".format(Prod3))
        ListaTem.append("{:,.2f}".format(Prod4))
        ListaTem.append("{:,.2f}".format(TotProd))
        ListaTem.append("{:,}".format(TotalAnim))
        ListaTem.append("{:,}".format(TotDiasAnima))
        ListaTem.append('NA')
        ListaForRep.append(ListaTem)
        Nombre = 'Buscar cliente'
        Cliente = ''
    return render(request, 'Reportes/Servidos/ServidosPromedioDiario.html', {'ListaForRep':ListaForRep,
        'FClientes': FClientes, 'Nombre': Nombre, 'Cliente': Cliente, 'FechaDeHoy':FechaDeHoy})

def ProductosQueSeSirven(tipo):
    Lista = []
    if tipo == 2:
        query = """SELECT Descripcion FROM Aplicacion_tblproductos WHERE IDEstatus_id = '1' and SeSirve = 'Si' ORDER BY Descripcion"""
    elif tipo == 1:
        query = """SELECT ID FROM Aplicacion_tblproductos WHERE IDEstatus_id = '1' and SeSirve = 'Si' ORDER BY Descripcion"""

    with connection.cursor() as cursor:
        cursor.execute(query)
        ProdData = cursor.fetchall()

    for ren, item in enumerate(ProdData):
        Lista.append(item[0])
    return Lista

#  Calcula los dias animal en rango de fecha de un solo corral
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

#  Saca el rango de fechas de cuando se asigno y libero un corral con un cliente, si el segundo dato es 0 significa que sigue asignado
#  al cliente. si es diferente de 0 es la ultima fecha cuando se libero a este cliente
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

#  Genera una lista de fechas a partir de una inicial y final
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

#   Obtiene  la cantidad de animales en el corral desde la fecha de asignacion hasta la fecha proporcionada
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
