import sys
import re
import sqlite3
import mysql.connector

# Reporte diario argumentos,  IDCliente,FechaInicial,FechaFinal

cliente = 2
FechaInicial = '2023-09-01'
FechaFinal   = '2023-11-01'
tipo = 2
def ReporteDiario(cliente, FechaInicial, FechaFinal):
    ListaForRep = []
    ListaTem = []
    query = 'SELECT Aplicacion_tblcorrales.Descripcion,'
    IDListaProd = ProductosQueSeSirven(1)
    for k in range(len(IDListaProd)):
        query = query + \
            "SUM(CASE WHEN Aplicacion_tblservido.IDProducto_id = %s THEN Aplicacion_tblservido.CantidadServida ELSE 0 END),"
    query = query+"Aplicacion_tblservido.IDCorral_id"
    query = query + """ FROM Aplicacion_tblservido
                        INNER JOIN Aplicacion_tblcorrales ON Aplicacion_tblcorrales.ID =  Aplicacion_tblservido.IDCorral_id
                WHERE  Aplicacion_tblservido.IDCliente_id = %s AND Aplicacion_tblservido.Fecha BETWEEN %s AND %s
                GROUP BY Aplicacion_tblservido.IDCorral_id """
    param = IDListaProd
    param.append(cliente)
    param.append(FechaInicial)
    param.append(FechaFinal)
    Data = run_query2(query, param)
    TotServido = 0
    Promedio = 0
    for ren, item in enumerate(Data):
        for col in range(len(item)-1):
            if col > 0:
                # data="{:,.2f}".format(item[col])
                data = item[col]
                TotServido = TotServido+item[col]
            else:
                data = item[col]
            ListaTem.append(data)
        # ListaTem.append("{:,.2f}".format(TotServido)  )
        ListaTem.append(TotServido)
        NoAnimalesActual = CantidadActualAnimales(Data[ren][5], FechaFinal)
        ListaTem.append(NoAnimalesActual)
        DiasAnimal = CalculaDiasAnimal(
            cliente, item[-1], FechaInicial, FechaFinal)
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
    for it in ListaForRep:
        print(it)
    return ListaForRep


def ProductosQueSeSirven(tipo):
    Lista = []
    if tipo == 2:
        query = """SELECT Descripcion FROM Aplicacion_tblproductos WHERE IDEstatus_id = '1' and SeSirve = 'Si' ORDER BY Descripcion"""
    elif tipo == 1:
        query = """SELECT ID FROM Aplicacion_tblproductos WHERE IDEstatus_id = '1' and SeSirve = 'Si' ORDER BY Descripcion"""
    ProdData = run_query2(query)
    for ren, item in enumerate(ProdData):
        Lista.append(item[0])
        print(Lista)
    return Lista

#  Calcula los dias animal en rango de fecha de un solo corral


def CalculaDiasAnimal(IDCliente, IDCorral, FechaInicial, FechaFinal):
    ListaTem = []
    ListaForRet = []
    FechasOcupa = RangoFechasOcupaCorral(IDCorral, IDCliente)
    if FechasOcupa[0][1] == 0:
        pass
    elif FechasOcupa[0][1] < FechaFinal:
        # FechaFinal = FechasOcupa[0][1]
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
    Datos = run_query2(query, (IDCorral, IDCliente, IDCorral, IDCliente))
    return Datos

#  Genera una lista de fechas a partir de una inicial y final


def GeneraListaFechas(fi, ff):
    from datetime import datetime
    from datetime import timedelta
    import sys
    FechaInicial = datetime.strptime(fi, '%Y-%m-%d')
    FechaFinal = datetime.strptime(ff, '%Y-%m-%d')
    Fecha = FechaInicial
    ListaFechas = [datetime.strftime(Fecha, '%Y-%m-%d'), ]
    cnt = 0
    while Fecha != FechaFinal:
        cnt += 1
        if cnt > 30:
            break
        Fecha = Fecha + timedelta(days=1)
        ListaFechas.append(datetime.strftime(Fecha, '%Y-%m-%d'))
    return ListaFechas

#   Obtiene  la cantidad de animales en el corral desde la fecha de asignacion hasta la fecha proporcionada


def CantidadActualAnimales(IDCorral, fecha):
    query = """SELECT  SUM(case WHEN  Aplicacion_tblmovimientoanimales.IDMovimiento_id = 0  THEN  Aplicacion_tbldetallemovanimales.Cantidad ELSE 0 END) -
    SUM(case WHEN  Aplicacion_tblmovimientoanimales.IDMovimiento_id = 1  THEN  Aplicacion_tbldetallemovanimales.Cantidad  ELSE 0 END) AS SUMA
    FROM Aplicacion_tblmovimientoanimales 
    INNER JOIN Aplicacion_tbldetallemovanimales ON Aplicacion_tblmovimientoanimales.Folio = Aplicacion_tbldetallemovanimales.IDFolio
    WHERE Aplicacion_tblmovimientoanimales.IDCorral_id= %s  AND Aplicacion_tblmovimientoanimales.Fecha BETWEEN 
    (SELECT FechaAsigna FROM Aplicacion_tblcorrales WHERE Aplicacion_tblcorrales.ID= %s ) AND %s"""
    Cantidad = run_query2(query, (IDCorral, IDCorral, fecha))
    if Cantidad[0][0] is None:
        return -1
    else:
        return Cantidad[0][0]



# def run_query2(query, parameters=()):
#     conn = sqlite3.connect("respaldo.sqlite3")
#     cursor = conn.cursor()
#     cursor.execute(query, parameters)
#     result = cursor.fetchall()
#     conn.commit()
#     return result


def run_query2(query, parameters=()):
    mydb = mysql.connector.connect(
        host="containers-us-west-200.railway.app",
        user="root",
        password="KeRCIq2V93Z89OiWzpy2",
        database="railway",
        port="5663")
    cursor = mydb.cursor()
    cursor.execute(query, parameters)
    result = cursor.fetchall()
    mydb.commit()
    return result

if __name__ == "__main__":
    print("Resultados de la función ProductosQueSeSirven:")
    resultado_productos = ProductosQueSeSirven(tipo)
    print(resultado_productos)
    
    print("\nResultados de la función ReporteDiario:")
    resultado_reporte = ReporteDiario(cliente, FechaInicial, FechaFinal)
    for item in resultado_reporte:
        print(item)
