from django.shortcuts import render,redirect
from django.contrib import messages
from datetime import datetime, date
from django.contrib.auth.models import Group
# LLAMAR ARCHIVOS LOCALES
from Aplicacion.forms import *
from Aplicacion.models import *
from Aplicacion.views import servicioActivo, estadoPago, registrarPago
from django.db import connection
from django.db.models import Q
import mysql.connector
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< TABLAS DE REPORTES >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# ------------------------------------------------REPORTES DE MATERIAS PRIMAS---------------------------------------------------

def reporteMovEntradaMP(request):
    FechaDeHoy = datetime.now().strftime('%Y-%m-%d %H:%M')
    FContenedores = tblContenedoresMateriaPrima.objects.all()

    if request.method == 'POST':
        if 'reportes' in request.POST:
            Contenedor = request.POST.get('contenedor')
            Fecha = request.POST.get('fecha1')
            Fecha2 = request.POST.get('fecha2')
            if Contenedor == 'todos':
                consulta_sql ="""SELECT Aplicacion_tblentradamp.IDFolio, Aplicacion_tblentradamp.fecha, 
                Aplicacion_tblmateriaprima.Descripcion, Aplicacion_tblentradamp.cantidad, 
                Aplicacion_tblcontenedoresmateriaprima.Cliente, Aplicacion_tblentradamp.Notas
                FROM Aplicacion_tblentradamp
                INNER JOIN Aplicacion_tblmateriaprima ON Aplicacion_tblmateriaprima.ID = Aplicacion_tblentradamp.IDMateriaPrima_id
                INNER JOIN Aplicacion_tblcontenedoresmateriaprima ON Aplicacion_tblcontenedoresmateriaprima.ID = Aplicacion_tblentradamp.IDAlmacen_id
                WHERE Aplicacion_tblentradamp.Fecha BETWEEN %s AND %s ORDER BY Aplicacion_tblentradamp.Fecha"""
                with connection.cursor() as cursor:
                    cursor.execute(consulta_sql, [Fecha, Fecha2])
                    reprotes = cursor.fetchall()
                Nombre = 'Se trajeron todos los clientes'
                Contenedor = 'todos'
                return render(request, 'Reportes/MovimientosMP/EntradaMP.html', {'reprotes': reprotes, 
                'FContenedores':FContenedores, 'Nombre': Nombre, 'Contenedor': Contenedor, 'Fecha':Fecha, 'Fecha2':Fecha2})
            else:
                consulta_sql ="""SELECT Aplicacion_tblentradamp.IDFolio, Aplicacion_tblentradamp.fecha, Aplicacion_tblmateriaprima.Descripcion, 
                Aplicacion_tblentradamp.cantidad, Aplicacion_tblcontenedoresmateriaprima.Cliente, Aplicacion_tblentradamp.Notas
                FROM Aplicacion_tblentradamp
                INNER JOIN Aplicacion_tblmateriaprima ON Aplicacion_tblmateriaprima.ID = Aplicacion_tblentradamp.IDMateriaPrima_id
                INNER JOIN Aplicacion_tblcontenedoresmateriaprima ON Aplicacion_tblcontenedoresmateriaprima.ID = Aplicacion_tblentradamp.IDAlmacen_id
                WHERE Aplicacion_tblcontenedoresmateriaprima.IDCliente_id = %s AND (Aplicacion_tblentradamp.Fecha  BETWEEN  %s AND  %s ) ORDER BY Aplicacion_tblentradamp.Fecha"""
                with connection.cursor() as cursor:
                    cursor.execute(consulta_sql, [Contenedor, Fecha, Fecha2])
                    reportes = cursor.fetchall()
                TEContenedores = tblContenedoresMateriaPrima.objects.get(IDCliente_id=Contenedor)
                Nombre = TEContenedores.Cliente
                return render(request, 'Reportes/MovimientosMP/EntradaMP.html', {'reportes': reportes, 
                'FContenedores':FContenedores, 'Nombre': Nombre, 'Contenedor': Contenedor, 'Fecha':Fecha, 'Fecha2':Fecha2})
    else:
        consulta_sql ="""SELECT Aplicacion_tblentradamp.IDFolio, Aplicacion_tblentradamp.fecha, 
        Aplicacion_tblmateriaprima.Descripcion, Aplicacion_tblentradamp.cantidad, 
        Aplicacion_tblcontenedoresmateriaprima.Cliente, Aplicacion_tblentradamp.Notas
        FROM Aplicacion_tblentradamp
        INNER JOIN Aplicacion_tblmateriaprima ON Aplicacion_tblmateriaprima.ID = Aplicacion_tblentradamp.IDMateriaPrima_id
        INNER JOIN Aplicacion_tblcontenedoresmateriaprima ON Aplicacion_tblcontenedoresmateriaprima.ID = Aplicacion_tblentradamp.IDAlmacen_id
        WHERE (Aplicacion_tblentradamp.Fecha BETWEEN %s AND %s) ORDER BY Aplicacion_tblentradamp.Fecha"""
        with connection.cursor() as cursor:
            cursor.execute(consulta_sql, [FechaDeHoy, FechaDeHoy])
            reportes = cursor.fetchall()
        Nombre = 'Buscar cliente'
        Contenedor = ''
        return render(request, 'Reportes/MovimientosMP/EntradaMP.html', {'reportes': reportes,
        'FechaDeHoy':FechaDeHoy, 'FContenedores':FContenedores, 'Nombre':Nombre, 'Contenedor':Contenedor})
    
def reporteMovSalidaMP(request):
    FechaDeHoy = datetime.now().strftime('%Y-%m-%d %H:%M')
    FContenedores = tblContenedoresMateriaPrima.objects.all()

    if request.method == 'POST':
        if 'reportes' in request.POST:
            Contenedor = request.POST.get('contenedor')
            Fecha = request.POST.get('fecha1')
            Fecha2 = request.POST.get('fecha2')
            if Contenedor == 'todos':
                consulta_sql ="""SELECT Aplicacion_tblsalidamp.IDFolio, Aplicacion_tblsalidamp.fecha, 
                Aplicacion_tblmateriaprima.Descripcion, Aplicacion_tblsalidamp.cantidad, 
                Aplicacion_tblcontenedoresmateriaprima.Cliente, Aplicacion_tblsalidamp.Notas
                FROM Aplicacion_tblsalidamp
                INNER JOIN Aplicacion_tblmateriaprima ON Aplicacion_tblmateriaprima.ID = Aplicacion_tblsalidamp.IDMateriaPrima_id
                INNER JOIN Aplicacion_tblcontenedoresmateriaprima ON Aplicacion_tblcontenedoresmateriaprima.ID = Aplicacion_tblsalidamp.IDAlmacen_id
                WHERE Aplicacion_tblsalidamp.Fecha BETWEEN %s AND %s ORDER BY Aplicacion_tblsalidamp.Fecha"""
                with connection.cursor() as cursor:
                    cursor.execute(consulta_sql, [Fecha, Fecha2])
                    reprotes = cursor.fetchall()
                Nombre = 'Se trajeron todos los clientes'
                Contenedor = 'todos'
                return render(request, 'Reportes/MovimientosMP/SalidaMP.html', {'reprotes': reprotes, 
                'FContenedores':FContenedores, 'Nombre': Nombre, 'Contenedor': Contenedor, 'Fecha':Fecha, 'Fecha2':Fecha2})
            else:
                consulta_sql ="""SELECT Aplicacion_tblsalidamp.IDFolio, Aplicacion_tblsalidamp.fecha, Aplicacion_tblmateriaprima.Descripcion, 
                Aplicacion_tblsalidamp.cantidad, Aplicacion_tblcontenedoresmateriaprima.Cliente, Aplicacion_tblsalidamp.Notas
                FROM Aplicacion_tblsalidamp
                INNER JOIN Aplicacion_tblmateriaprima ON Aplicacion_tblmateriaprima.ID = Aplicacion_tblsalidamp.IDMateriaPrima_id
                INNER JOIN Aplicacion_tblcontenedoresmateriaprima ON Aplicacion_tblcontenedoresmateriaprima.ID = Aplicacion_tblsalidamp.IDAlmacen_id
                WHERE Aplicacion_tblcontenedoresmateriaprima.IDCliente_id = %s AND (Aplicacion_tblsalidamp.Fecha  BETWEEN  %s AND  %s ) ORDER BY Aplicacion_tblsalidamp.Fecha"""
                with connection.cursor() as cursor:
                    cursor.execute(consulta_sql, [Contenedor, Fecha, Fecha2])
                    reportes = cursor.fetchall()
                TEContenedores = tblContenedoresMateriaPrima.objects.get(IDCliente_id=Contenedor)
                Nombre = TEContenedores.Cliente
                return render(request, 'Reportes/MovimientosMP/SalidaMP.html', {'reportes': reportes, 
                'FContenedores':FContenedores, 'Nombre': Nombre, 'Contenedor': Contenedor, 'Fecha':Fecha, 'Fecha2':Fecha2})
    else:
        consulta_sql ="""SELECT Aplicacion_tblsalidamp.IDFolio, Aplicacion_tblsalidamp.fecha, 
        Aplicacion_tblmateriaprima.Descripcion, Aplicacion_tblsalidamp.cantidad, 
        Aplicacion_tblcontenedoresmateriaprima.Cliente, Aplicacion_tblsalidamp.Notas
        FROM Aplicacion_tblsalidamp
        INNER JOIN Aplicacion_tblmateriaprima ON Aplicacion_tblmateriaprima.ID = Aplicacion_tblsalidamp.IDMateriaPrima_id
        INNER JOIN Aplicacion_tblcontenedoresmateriaprima ON Aplicacion_tblcontenedoresmateriaprima.ID = Aplicacion_tblsalidamp.IDAlmacen_id
        WHERE (Aplicacion_tblsalidamp.Fecha BETWEEN %s AND %s) ORDER BY Aplicacion_tblsalidamp.Fecha"""
        with connection.cursor() as cursor:
            cursor.execute(consulta_sql, [FechaDeHoy, FechaDeHoy])
            reportes = cursor.fetchall()
        Nombre = 'Buscar cliente'
        Contenedor = ''
        return render(request, 'Reportes/MovimientosMP/SalidaMP.html', {'reportes': reportes,
        'FechaDeHoy':FechaDeHoy, 'FContenedores':FContenedores, 'Nombre':Nombre, 'Contenedor':Contenedor})
    
# ------------------------------------------------REPORTES ANIMALES--------------------------------------------------------------------------
def reporteAnimalesMovimientos(request):
    FechaDeHoy = datetime.now().strftime('%Y-%m-%d %H:%M')
    FClientes = tblClientes.objects.exclude(ID=1)

    if request.method == 'POST':
        if 'reportes' in request.POST:
            Cliente = request.POST.get('cliente')
            Fecha = request.POST.get('fecha1')
            Fecha2 = request.POST.get('fecha2')
            if Cliente == 'todos':
                consulta_sql = """SELECT Aplicacion_tblmovimientoanimales.Folio, Aplicacion_tblmovimientoanimales.Fecha, 
                Aplicacion_tblclientes.Nombre, Aplicacion_tblcorrales.Descripcion, Aplicacion_tbltipomov.Descripcion AS TipoMov
                FROM Aplicacion_tblmovimientoanimales
                INNER JOIN Aplicacion_tblclientes ON Aplicacion_tblmovimientoanimales.IDCliente_id = Aplicacion_tblclientes.ID
                INNER JOIN Aplicacion_tbltipomov ON Aplicacion_tblmovimientoanimales.IDMovimiento_id = Aplicacion_tbltipomov.ID 
                INNER JOIN Aplicacion_tblcorrales ON  Aplicacion_tblmovimientoanimales.IDCorral_id =Aplicacion_tblcorrales.ID
                WHERE Aplicacion_tblmovimientoanimales.Fecha BETWEEN %s AND %s and Aplicacion_tblclientes.ID != 1
                ORDER BY Aplicacion_tblmovimientoanimales.Folio"""

                with connection.cursor() as cursor:
                    cursor.execute(consulta_sql, [Fecha, Fecha2])
                    reportes = cursor.fetchall()
                Nombre = 'Se trajeron todos los clientes'
                Cliente = 'todos'
                return render(request, 'Reportes/Animales/MovimientoAnimales.html', {'reportes': reportes, 
                'FClientes':FClientes, 'Nombre': Nombre, 'Cliente': Cliente, 'Fecha':Fecha, 'Fecha2':Fecha2})
            else:
                consulta_sql = """SELECT Aplicacion_tblmovimientoanimales.Folio, Aplicacion_tblmovimientoanimales.Fecha, 
                Aplicacion_tblclientes.Nombre, Aplicacion_tblcorrales.Descripcion, Aplicacion_tbltipomov.Descripcion AS TipoMov
                FROM Aplicacion_tblmovimientoanimales
                INNER JOIN Aplicacion_tblclientes ON Aplicacion_tblmovimientoanimales.IDCliente_id = Aplicacion_tblclientes.ID
                INNER JOIN Aplicacion_tbltipomov ON Aplicacion_tblmovimientoanimales.IDMovimiento_id = Aplicacion_tbltipomov.ID 
                INNER JOIN Aplicacion_tblcorrales ON  Aplicacion_tblmovimientoanimales.IDCorral_id =Aplicacion_tblcorrales.ID
                WHERE Aplicacion_tblclientes.ID = %s AND  (Aplicacion_tblmovimientoanimales.Fecha BETWEEN %s AND %s) and Aplicacion_tblclientes.ID != 1
                ORDER BY Aplicacion_tblmovimientoanimales.Folio"""

                with connection.cursor() as cursor:
                    cursor.execute(consulta_sql, [Cliente, Fecha, Fecha2])
                    reportes = cursor.fetchall()
                TECliente = tblClientes.objects.get(ID=Cliente)
                Nombre = TECliente.Nombre
                return render(request, 'Reportes/Animales/MovimientoAnimales.html', {'reportes': reportes, 
                'FClientes':FClientes, 'Nombre': Nombre, 'Cliente': Cliente, 'Fecha':Fecha, 'Fecha2':Fecha2})
    else:
        consulta_sql ="""SELECT Aplicacion_tblmovimientoanimales.Folio, Aplicacion_tblmovimientoanimales.Fecha, 
        Aplicacion_tblclientes.Nombre, Aplicacion_tblcorrales.Descripcion, Aplicacion_tbltipomov.Descripcion AS TipoMov
        FROM Aplicacion_tblmovimientoanimales
        INNER JOIN Aplicacion_tblclientes ON Aplicacion_tblmovimientoanimales.IDCliente_id = Aplicacion_tblclientes.ID
        INNER JOIN Aplicacion_tbltipomov ON Aplicacion_tblmovimientoanimales.IDMovimiento_id = Aplicacion_tbltipomov.ID 
        INNER JOIN Aplicacion_tblcorrales ON  Aplicacion_tblmovimientoanimales.IDCorral_id =Aplicacion_tblcorrales.ID
        WHERE  (Aplicacion_tblmovimientoanimales.Fecha BETWEEN %s AND %s) and Aplicacion_tblclientes.ID != 1
        ORDER BY Aplicacion_tblmovimientoanimales.Folio"""
        with connection.cursor() as cursor:
            cursor.execute(consulta_sql, [FechaDeHoy, FechaDeHoy])
            reportes = cursor.fetchall()
        Nombre = 'Buscar cliente'
        Cliente = ''
        return render(request, 'Reportes/Animales/MovimientoAnimales.html', {'reportes': reportes,
        'FechaDeHoy':FechaDeHoy, 'FClientes':FClientes, 'Nombre':Nombre, 'Cliente':Cliente})

def reportePorClientes(request):
    FechaDeHoy = datetime.now().strftime('%Y-%m-%d %H:%M')
    FClientes = tblClientes.objects.exclude(ID=1)

    if request.method == 'POST':
        if 'reportes' in request.POST:
            Cliente = request.POST.get('cliente')
            Fecha = request.POST.get('fecha1')

            if Cliente == 'todos':
                consulta_sql = """SELECT TT.CLIENTE, 0, TT.ENTRADAS, TT.SALIDAS, TT.ENTRADAS-TT.SALIDAS AS TOTA
                FROM (SELECT  Aplicacion_tblclientes.Nombre AS CLIENTE,
                SUM(case WHEN Aplicacion_tblmovimientoanimales.IDMovimiento_id = 0 AND Aplicacion_tblmovimientoanimales.Fecha BETWEEN Aplicacion_tblcorrales.FechaAsigna 
                AND %s THEN  Aplicacion_tbldetallemovanimales.Cantidad ELSE 0 END) AS ENTRADAS,
                SUM(case WHEN  Aplicacion_tblmovimientoanimales.IDMovimiento_id = 1 AND Aplicacion_tblmovimientoanimales.Fecha BETWEEN Aplicacion_tblcorrales.FechaAsigna 
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
                'FClientes':FClientes, 'Nombre': Nombre, 'Cliente': Cliente, 'Fecha':Fecha})
            else:
                consulta_sql = """SELECT TT.CORRAL, TT.FECHA, TT.ENTRADAS, TT.SALIDAS, TT.ENTRADAS-TT.SALIDAS AS TOTA
                FROM (SELECT Aplicacion_tblcorrales.Descripcion AS CORRAL , Aplicacion_tblcorrales.FechaAsigna AS FECHA,
                SUM(case WHEN   Aplicacion_tblmovimientoanimales.IDMovimiento_id = 0 AND  Aplicacion_tblmovimientoanimales.Fecha BETWEEN Aplicacion_tblcorrales.FechaAsigna 
                    AND %s THEN   Aplicacion_tbldetallemovanimales.Cantidad ELSE 0 END) AS ENTRADAS,
                SUM(case WHEN   Aplicacion_tblmovimientoanimales.IDMovimiento_id = 1 AND  Aplicacion_tblmovimientoanimales.Fecha BETWEEN Aplicacion_tblcorrales.FechaAsigna 
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
                    cursor.execute(consulta_sql, [Fecha, Fecha, Cliente, Cliente])
                    reportes = cursor.fetchall()
                TECliente = tblClientes.objects.get(ID=Cliente)
                Nombre = TECliente.Nombre
                return render(request, 'Reportes/Animales/MovimientosClientes.html', {'reportes': reportes, 
                'FClientes':FClientes, 'Nombre': Nombre, 'Cliente': Cliente, 'Fecha':Fecha})
    else:
        consulta_sql ="""SELECT TT.CLIENTE, 0, TT.ENTRADAS, TT.SALIDAS, TT.ENTRADAS-TT.SALIDAS AS TOTA
        FROM (SELECT  Aplicacion_tblclientes.Nombre AS CLIENTE,
        SUM(case WHEN Aplicacion_tblmovimientoanimales.IDMovimiento_id = 0 AND Aplicacion_tblmovimientoanimales.Fecha BETWEEN Aplicacion_tblcorrales.FechaAsigna 
        AND %s THEN  Aplicacion_tbldetallemovanimales.Cantidad ELSE 0 END) AS ENTRADAS,
        SUM(case WHEN  Aplicacion_tblmovimientoanimales.IDMovimiento_id = 1 AND Aplicacion_tblmovimientoanimales.Fecha BETWEEN Aplicacion_tblcorrales.FechaAsigna 
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
        'FechaDeHoy':FechaDeHoy, 'FClientes':FClientes, 'Nombre':Nombre, 'Cliente':Cliente})
    
def reportePorClientesCorrales(request):
    FechaDeHoy = datetime.now().strftime('%Y-%m-%d %H:%M')
    FClientes = tblClientes.objects.exclude(ID=1)
    print(type(FechaDeHoy))
    if request.method == 'POST':
        if 'reportes' in request.POST:
            Cliente = request.POST.get('cliente')
            Fecha = request.POST.get('fecha1')
            Fecha2 = request.POST.get('fecha2')
            print(type(Fecha))
            print(type(Fecha2))
            if Cliente == 'todos':
                consulta_sql = """SELECT Aplicacion_tblclientes.Nombre, Aplicacion_tblcorrales.Descripcion,
                SUM(case WHEN  Aplicacion_tblmovimientoanimales.IDMovimiento_id = 0 AND Aplicacion_tblmovimientoanimales.Fecha 
                    BETWEEN Aplicacion_tblcorrales.FechaAsigna AND %s THEN  Aplicacion_tbldetallemovanimales.Cantidad ELSE 0 END) - 
                SUM(case WHEN  Aplicacion_tblmovimientoanimales.IDMovimiento_id = 1 AND Aplicacion_tblmovimientoanimales.Fecha  
                    BETWEEN Aplicacion_tblcorrales.FechaAsigna AND %s THEN  Aplicacion_tbldetallemovanimales.Cantidad   ELSE 0 END) AS INICIAL,
                SUM(case WHEN  Aplicacion_tblmovimientoanimales.IDMovimiento_id = 0 AND Aplicacion_tblmovimientoanimales.Fecha 
                    BETWEEN %s AND %s THEN  Aplicacion_tbldetallemovanimales.Cantidad ELSE 0 END) AS ENTRADA,
                SUM(case WHEN  Aplicacion_tblmovimientoanimales.IDMovimiento_id = 1 AND Aplicacion_tblmovimientoanimales.Fecha 
                    BETWEEN %s AND %s THEN  Aplicacion_tbldetallemovanimales.Cantidad  ELSE 0 END) AS SALIDA
                FROM  Aplicacion_tblmovimientoanimales
                INNER JOIN Aplicacion_tblclientes ON Aplicacion_tblclientes.ID = Aplicacion_tblmovimientoanimales.IDCliente_id 
                INNER JOIN Aplicacion_tblcorrales ON  Aplicacion_tblcorrales.ID = Aplicacion_tblmovimientoanimales.IDCorral_id
                INNER JOIN Aplicacion_tbldetallemovanimales ON  Aplicacion_tblmovimientoanimales.Folio = Aplicacion_tbldetallemovanimales.IDFolio
                WHERE  Aplicacion_tblmovimientoanimales.IDCorral_id IN (SELECT  Aplicacion_tblcorrales.ID FROM Aplicacion_tblcorrales)
                GROUP BY Aplicacion_tblmovimientoanimales.IDCorral_id"""

                with connection.cursor() as cursor:
                    cursor.execute(consulta_sql, [Fecha, Fecha, Fecha, Fecha2, Fecha, Fecha2])
                    reportes = cursor.fetchall()
                Nombre = 'Se trajeron todos los clientes'
                Cliente = 'todos'
                return render(request, 'Reportes/Animales/PorClienteCorral.html', {'reportes': reportes, 
                'FClientes':FClientes, 'Nombre': Nombre, 'Cliente': Cliente, 'Fecha':Fecha, 'Fecha2':Fecha2})
            else:
                consulta_sql = """SELECT Aplicacion_tblclientes.Nombre, Aplicacion_tblcorrales.Descripcion,
                SUM(case WHEN  Aplicacion_tblmovimientoanimales.IDMovimiento_id = 0 AND Aplicacion_tblmovimientoanimales.Fecha 
                    BETWEEN Aplicacion_tblcorrales.FechaAsigna AND %s THEN  Aplicacion_tbldetallemovanimales.Cantidad ELSE 0 END) - 
                SUM(case WHEN  Aplicacion_tblmovimientoanimales.IDMovimiento_id = 1 AND Aplicacion_tblmovimientoanimales.Fecha  
                    BETWEEN Aplicacion_tblcorrales.FechaAsigna AND %s THEN  Aplicacion_tbldetallemovanimales.Cantidad   ELSE 0 END) AS INICIAL,
                SUM(case WHEN  Aplicacion_tblmovimientoanimales.IDMovimiento_id = 0 AND Aplicacion_tblmovimientoanimales.Fecha 
                    BETWEEN %s AND %s THEN  Aplicacion_tbldetallemovanimales.Cantidad ELSE 0 END) AS ENTRADA,
                SUM(case WHEN  Aplicacion_tblmovimientoanimales.IDMovimiento_id = 1 AND Aplicacion_tblmovimientoanimales.Fecha 
                    BETWEEN %s AND %s THEN  Aplicacion_tbldetallemovanimales.Cantidad  ELSE 0 END) AS SALIDA
                FROM  Aplicacion_tblmovimientoanimales
                INNER JOIN Aplicacion_tblclientes ON Aplicacion_tblclientes.ID = Aplicacion_tblmovimientoanimales.IDCliente_id 
                INNER JOIN Aplicacion_tblcorrales ON  Aplicacion_tblcorrales.ID = Aplicacion_tblmovimientoanimales.IDCorral_id
                INNER JOIN Aplicacion_tbldetallemovanimales ON  Aplicacion_tblmovimientoanimales.Folio = Aplicacion_tbldetallemovanimales.IDFolio
                WHERE  Aplicacion_tblmovimientoanimales.IDCorral_id IN 
                    (SELECT  Aplicacion_tblcorrales.ID FROM Aplicacion_tblcorrales where  Aplicacion_tblcorrales.IDCliente_id = %s)
                                AND Aplicacion_tblmovimientoanimales.IDCliente_id = %s
                GROUP BY Aplicacion_tblmovimientoanimales.IDCorral_id"""

                with connection.cursor() as cursor:
                    cursor.execute(consulta_sql, [Fecha, Fecha, Fecha, Fecha2, Fecha, Fecha2, Cliente, Cliente])
                    reportes = cursor.fetchall()
                TECliente = tblClientes.objects.get(ID=Cliente)
                Nombre = TECliente.Nombre
                return render(request, 'Reportes/Animales/PorClienteCorral.html', {'reportes': reportes, 
                'FClientes':FClientes, 'Nombre': Nombre, 'Cliente': Cliente, 'Fecha':Fecha, 'Fecha2':Fecha2})
    else:
        consulta_sql ="""SELECT Aplicacion_tblclientes.Nombre, Aplicacion_tblcorrales.Descripcion,
        SUM(case WHEN  Aplicacion_tblmovimientoanimales.IDMovimiento_id = 0 AND Aplicacion_tblmovimientoanimales.Fecha 
            BETWEEN Aplicacion_tblcorrales.FechaAsigna AND %s THEN  Aplicacion_tbldetallemovanimales.Cantidad ELSE 0 END) - 
        SUM(case WHEN  Aplicacion_tblmovimientoanimales.IDMovimiento_id = 1 AND Aplicacion_tblmovimientoanimales.Fecha  
            BETWEEN Aplicacion_tblcorrales.FechaAsigna AND %s THEN  Aplicacion_tbldetallemovanimales.Cantidad   ELSE 0 END) AS INICIAL,
        SUM(case WHEN  Aplicacion_tblmovimientoanimales.IDMovimiento_id = 0 AND Aplicacion_tblmovimientoanimales.Fecha 
            BETWEEN %s AND %s THEN  Aplicacion_tbldetallemovanimales.Cantidad ELSE 0 END) AS ENTRADA,
        SUM(case WHEN  Aplicacion_tblmovimientoanimales.IDMovimiento_id = 1 AND Aplicacion_tblmovimientoanimales.Fecha 
            BETWEEN %s AND %s THEN  Aplicacion_tbldetallemovanimales.Cantidad  ELSE 0 END) AS SALIDA
        FROM  Aplicacion_tblmovimientoanimales
        INNER JOIN Aplicacion_tblclientes ON Aplicacion_tblclientes.ID = Aplicacion_tblmovimientoanimales.IDCliente_id 
        INNER JOIN Aplicacion_tblcorrales ON  Aplicacion_tblcorrales.ID = Aplicacion_tblmovimientoanimales.IDCorral_id
        INNER JOIN Aplicacion_tbldetallemovanimales ON  Aplicacion_tblmovimientoanimales.Folio = Aplicacion_tbldetallemovanimales.IDFolio
        WHERE  Aplicacion_tblmovimientoanimales.IDCorral_id IN (SELECT  Aplicacion_tblcorrales.ID FROM Aplicacion_tblcorrales)
        GROUP BY Aplicacion_tblmovimientoanimales.IDCorral_id"""
        with connection.cursor() as cursor:
            cursor.execute(consulta_sql, [FechaDeHoy, FechaDeHoy, FechaDeHoy, FechaDeHoy, FechaDeHoy, FechaDeHoy])
            reportes = cursor.fetchall()
        Nombre = 'Buscar cliente'
        Cliente = ''
        return render(request, 'Reportes/Animales/PorClienteCorral.html', {'reportes': reportes,
        'FechaDeHoy':FechaDeHoy, 'FClientes':FClientes, 'Nombre':Nombre, 'Cliente':Cliente})
    
# ------------------------------------------------REPORTES SERVIDOS--------------------------------------------------------------------------
def reporteServidosMovimientos(request):
    FechaDeHoy = datetime.now().strftime('%Y-%m-%d %H:%M')
    FClientes = tblClientes.objects.exclude(ID=1)

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
                    LEFT JOIN Aplicacion_tblproductos ON Aplicacion_tblproductos.ID = Aplicacion_tblservido.IDProducto_id
                    LEFT JOIN Aplicacion_tblclientes ON Aplicacion_tblclientes.ID = Aplicacion_tblclientes.ID
                    LEFT JOIN Aplicacion_tblcorrales ON Aplicacion_tblservido.IDCorral_id = Aplicacion_tblcorrales.ID
                    WHERE Aplicacion_tblservido.Fecha BETWEEN  %s AND  %s and Aplicacion_tblclientes.ID != 1"""

                with connection.cursor() as cursor:
                    cursor.execute(consulta_sql, [Fecha, Fecha2])
                    reportes = cursor.fetchall()
                Nombre = 'Se trajeron todos los clientes'
                Cliente = 'todos'
                return render(request, 'Reportes/Servidos/ServidosMovimientos.html', {'reportes': reportes, 
                'FClientes':FClientes, 'Nombre': Nombre, 'Cliente': Cliente, 'Fecha':Fecha, 'Fecha2':Fecha2})
            else:
                consulta_sql = """SELECT DISTINCT Aplicacion_tblservido.ID, Aplicacion_tblclientes.Nombre, 
                    Aplicacion_tblcorrales.Descripcion,  Aplicacion_tblproductos.Descripcion,
                    Aplicacion_tblservido.CantidadSolicitada, Aplicacion_tblservido.CantidadServida,
                    Aplicacion_tblservido.Fecha, Aplicacion_tblservido.FechaServida
                    FROM Aplicacion_tblservido
                    LEFT JOIN Aplicacion_tblproductos ON Aplicacion_tblproductos.ID = Aplicacion_tblservido.IDProducto_id
                    LEFT JOIN Aplicacion_tblclientes ON Aplicacion_tblclientes.ID = Aplicacion_tblclientes.ID
                    LEFT JOIN Aplicacion_tblcorrales ON Aplicacion_tblservido.IDCorral_id = Aplicacion_tblcorrales.ID
                    WHERE  Aplicacion_tblclientes.ID = %s AND  (Aplicacion_tblservido.Fecha BETWEEN  %s AND  %s) and Aplicacion_tblclientes.ID != 1
                    """
                with connection.cursor() as cursor:
                    cursor.execute(consulta_sql, [Cliente, Fecha, Fecha2])
                    reportes = cursor.fetchall()
                TECliente = tblClientes.objects.get(ID=Cliente)
                Nombre = TECliente.Nombre
                return render(request, 'Reportes/Servidos/ServidosMovimientos.html', {'reportes': reportes, 
                'FClientes':FClientes, 'Nombre': Nombre, 'Cliente': Cliente, 'Fecha':Fecha, 'Fecha2':Fecha2})
    else:
        consulta_sql = """  
        SELECT DISTINCT Aplicacion_tblservido.ID, Aplicacion_tblclientes.Nombre, Aplicacion_tblcorrales.Descripcion,  
        Aplicacion_tblproductos.Descripcion, Aplicacion_tblservido.CantidadSolicitada, Aplicacion_tblservido.CantidadServida, 
        Aplicacion_tblservido.Fecha, Aplicacion_tblservido.FechaServida FROM Aplicacion_tblservido
        LEFT JOIN Aplicacion_tblproductos  ON Aplicacion_tblproductos.ID = Aplicacion_tblservido.IDProducto_id
        LEFT JOIN Aplicacion_tblclientes ON Aplicacion_tblclientes.ID = Aplicacion_tblclientes.ID
        LEFT JOIN Aplicacion_tblcorrales ON Aplicacion_tblservido.IDCorral_id = Aplicacion_tblcorrales.ID
        WHERE  Aplicacion_tblservido.Fecha BETWEEN  %s AND  %s and Aplicacion_tblclientes.ID != 1
        """
        
        with connection.cursor() as cursor:
            cursor.execute(consulta_sql, [FechaDeHoy, FechaDeHoy])
            reportes = cursor.fetchall()
        Nombre = 'Buscar cliente'
        Cliente = ''
        return render(request, 'Reportes/Servidos/ServidosMovimientos.html', {'reportes': reportes,
        'FechaDeHoy':FechaDeHoy, 'FClientes':FClientes, 'Nombre':Nombre, 'Cliente':Cliente})
