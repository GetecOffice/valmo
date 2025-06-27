from django.shortcuts import render
from datetime import datetime, timedelta
# LLAMAR ARCHIVOS LOCALES
from django.db.models import Q
from django.db import connection
import mysql.connector
import sqlite3

# Reporte diario argumentos,  IDCliente,FechaInicial,FechaFinal

cliente = 2
FechaInicial = '2023-09-01'
FechaFinal = '2023-11-01'
tipo = 2


def Reporte2(cliente, FechaInicial, FechaFinal):
    query = """
        SELECT  Aplicacion_tblcorrales.Descripcion, SUM(Aplicacion_tblservido.CantidadServida),Aplicacion_tblcorrales.ID
        FROM Aplicacion_tblservido
        INNER JOIN 	Aplicacion_tblcorrales ON  Aplicacion_tblservido.IDCorral_id = Aplicacion_tblcorrales.ID
        WHERE  Aplicacion_tblservido.IDCliente_id = 2 AND  (Aplicacion_tblservido.Fecha BETWEEN '2023-08-010' AND '2023-10-09' )
        GROUP BY  Aplicacion_tblservido.IDCorral_id
        ORDER BY  Aplicacion_tblcorrales.Descripcion
                """
    # Data=run_query2(query,(cliente,FechaInicial,FechaFinal))
    with connection.cursor() as cursor:
        cursor.execute(query, [cliente, FechaInicial, FechaFinal])
        Data = cursor.fetchall()

    ListaTem = []
    Datos = []

    for i in range(0, len(Data)):
        ListaTem.append(Data[i][0])
        ListaTem.append(Data[i][1])
        DiasAnimal = CalculaDiasAnimal(
            cliente, Data[i][2], FechaInicial, FechaFinal)
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
    for i in DataToRep:
        print(i)
    return DataToRep


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
    FechaInicial = datetime.strptime(ff, '%Y-%m-%dT%H:%M')
    FechaFinal = datetime.strptime(fi, '%Y-%m-%dT%H:%M')
    Fecha = FechaInicial
    ListaFechas = [Fecha.strftime('%Y-%m-%d %H:%M'), ]

    cnt = 0
    while Fecha != FechaFinal:
        cnt += 1
        if cnt > 30:
            break
        Fecha = Fecha + timedelta(days=1)
        ListaFechas.append(Fecha.strftime('%Y-%m-%d %H:%M'))
    return ListaFechas

#   Obtiene  la cantidad de animales en el corral desde la fecha de asignacion hasta la fecha proporcionada
def CantidadActualAnimales(IDCorral, fecha):
    query = """SELECT  SUM(case WHEN  Aplicacion_tblmovimientoanimales.IDMovimiento_id = 0  THEN  Aplicacion_tbldetallemovanimales.Cantidad ELSE 0 END) -
    SUM(case WHEN  Aplicacion_tblmovimientoanimales.IDMovimiento_id = 1  THEN  Aplicacion_tbldetallemovanimales.Cantidad  ELSE 0 END) AS SUMA
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

def run_query2(query, parameters=()):
    conn = sqlite3.connect("respaldo.sqlite3")
    cursor = conn.cursor()
    cursor.execute(query, parameters)
    result = cursor.fetchall()
    conn.commit()
    return result


# def run_query2(query, parameters=()):
#     mydb = mysql.connector.connect(
#         host="containers-us-west-200.railway.app",
#         user="root",
#         password="KeRCIq2V93Z89OiWzpy2",
#         database="railway",
#         port="5663")
#     cursor = mydb.cursor()
#     cursor.execute(query, parameters)
#     result = cursor.fetchall()
#     mydb.commit()
#     return result


if __name__ == "__main__":
    print("Resultados de la función ProductosQueSeSirven:")
    resultado_productos = ProductosQueSeSirven(tipo)
    print(resultado_productos)

    print("\nResultados de la función ReporteDiario:")
    resultado_reporte = Reporte2(cliente, FechaInicial, FechaFinal)
    for item in resultado_reporte:
        print(item)
