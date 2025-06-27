# LLAMAR ARCHIVOS LOCALES
from Aplicacion.forms import *
from Aplicacion.models import *
import mysql.connector

def RepsLiquidacion(NoRep, cliente, FechaInicial, FechaFinal):
    query = ""
    if NoRep == '1':
        query = """
        SELECT tblCorrales.Descripcion, tblProductos.Descripcion, tblUnidades.Abreviacion, SUM(tblServido.CantServida)
        FROM tblServido
        INNER JOIN tblClientes ON tblServido.IDCliente=tblClientes.ID 
        INNER JOIN tblProductos ON tblServido.IDProductos = tblProductos.ID
        INNER JOIN tblCorrales ON tblServido.IDCorral=tblCorrales.ID     
        INNER JOIN  tblUnidades ON tblProductos.UdeM = tblUnidades.ID  
        WHERE  tblClientes.ID like %s AND  (tblServido.Fecha BETWEEN %s AND %s )
        GROUP BY  tblProductos.Descripcion, tblServido.IDCorral 
        ORDER BY tblCorrales.Descripcion
        """
    elif NoRep == '3':
        query = """
        SELECT tblProductos.Descripcion,tblUnidades.Abreviacion, SUM(tblServido.CantServida)
        FROM tblServido
        INNER JOIN tblClientes ON tblServido.IDCliente=tblClientes.ID
        INNER JOIN tblProductos ON tblServido.IDProductos = tblProductos.ID
        INNER JOIN tblUnidades ON tblProductos.UdeM = tblUnidades.ID  
        WHERE  tblClientes.ID like %s AND (tblServido.Fecha BETWEEN %s AND %s )
        GROUP BY  tblProductos.ID
        ORDER BY  tblProductos.Descripcion desc
               """
    else:
        return -1
    # Datos = run_query2(query, (cliente, FechaInicial, FechaFinal))
    Datos = runMySqlQuery(query, (cliente, FechaInicial, FechaFinal))
    DatosToRep = []
    ListaTem = []
    for ren in range(0, len(Datos)):
        for col in range(0, len(Datos[0])):
            DaToTabla = str(Datos[ren][col])
            if col == 6 or col == 7:
                DaToTabla = '{:.2f}'.format(Datos[ren][col])
            ListaTem.append(DaToTabla)
        DatosToRep.append(ListaTem)
        ListaTem = []
    for i in DatosToRep:
        print(i)
    return DatosToRep


def Reporte2(cliente, FechaInicial, FechaFinal):
    query = """
                SELECT  tblCorrales.Descripcion, SUM(tblServido.CantServida),tblCorrales.ID
                FROM tblServido
                INNER JOIN 	tblCorrales ON  tblServido.IDCorral = tblCorrales.ID
                WHERE  tblServido.IDCliente = %s  AND  (tblServido.Fecha BETWEEN %s AND %s )
                GROUP BY  tblServido.IDCorral
                ORDER BY  tblCorrales.Descripcion
                """
    # Data=run_query2(query,(cliente,FechaInicial,FechaFinal))
    Data = runMySqlQuery(query, (cliente, FechaInicial, FechaFinal))
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


# Reporte diario argumentos,  IDCliente,FechaInicial,FechaFinal
def ReporteDiario(cliente, FechaInicial, FechaFinal):
    ListaForRep = []
    ListaTem = []
    query = 'SELECT tblCorrales.Descripcion,'
    IDListaProd = ProductosQueSeSirven(1)
    for k in range(len(IDListaProd)):
        query = query + \
            "SUM(CASE WHEN tblServido.IDProductos = %s THEN tblServido.CantServida ELSE 0 END),"
    query = query+"tblServido.IDCorral"
    query = query + """ FROM tblServido
                        INNER JOIN tblCorrales ON tblCorrales.ID =  tblServido.IDCorral
                WHERE  tblServido.IDCliente = %s AND tblServido.Fecha BETWEEN %s AND %s
                GROUP BY tblServido.IDCorral """
    param = IDListaProd
    param.append(cliente)
    param.append(FechaInicial)
    param.append(FechaFinal)
    Data = runMySqlQuery(query, param)
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
        query = """SELECT Descripcion FROM tblProductos WHERE IDTipoStatus = '1' and SeSirve = 'Si' ORDER BY Descripcion"""
    elif tipo == 1:
        query = """SELECT ID FROM tblProductos WHERE IDTipoStatus = '1' and SeSirve = 'Si' ORDER BY Descripcion"""
    ProdData = runMySqlQuery(query)
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
    query = """  SELECT FECHAS.FECHA_ASIGNA,(SELECT(CASE WHEN FECHAS.FECHA_LIBERA > FECHAS.FECHA_ASIGNA THEN FECHAS.FECHA_LIBERA ELSE 0 END)) AS FECHA_LIBERA
                FROM (
                        SELECT 
                        MAX(CASE WHEN tblAsignaCorrales.IDCorral = %s AND tblAsignaCorrales.IDCliente= %s  AND tblAsignaCorrales.TipoMov = 1  
                        THEN tblAsignaCorrales.Fecha ELSE 0 END) AS FECHA_ASIGNA,
	                    MAX(CASE WHEN tblAsignaCorrales.IDCorral = %s AND tblAsignaCorrales.IDCliente= %s  AND tblAsignaCorrales.TipoMov = 0  
                        THEN tblAsignaCorrales.Fecha ELSE 0 END) AS FECHA_LIBERA
                        FROM tblAsignaCorrales 
                     ) AS FECHAS
            """
    Datos = runMySqlQuery(query, (IDCorral, IDCliente, IDCorral, IDCliente))
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
    query = """ SELECT  SUM(case WHEN  tblMovimientoAnimales.IDMovimiento = 0  THEN  tblMovimientoAnimales.Cantidad ELSE 0 END) -
                       SUM(case WHEN  tblMovimientoAnimales.IDMovimiento = 1  THEN  tblMovimientoAnimales.Cantidad  ELSE 0 END) AS SUMA
                FROM tblMovimientoAnimales 
                WHERE tblMovimientoAnimales.IDCorral= %s  AND tblMovimientoAnimales.Fecha BETWEEN 
                (SELECT FechaAsigna FROM tblCorrales WHERE tblCorrales.ID= %s ) AND %s
            """
    Cantidad = runMySqlQuery(query, (IDCorral, IDCorral, fecha))
    if Cantidad[0][0] is None:
        return -1
    else:
        return Cantidad[0][0]

        
def runMySqlQuery(query, parameters=()):
    mydb = mysql.connector.connect(
        host="containers-us-west-155.railway.app",
        user="root",
        password="kSg6PWye2BgLpKRqOh6g",
        database="railway",
        port="7433")
    cursor = mydb.cursor()
    cursor.execute(query, parameters)
    result = cursor.fetchall()
    mydb.commit()
    return result