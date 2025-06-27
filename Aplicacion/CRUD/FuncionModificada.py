import sqlite3

# Función desactualizada:
# La siguiente consulta requiere de un campo "Cantidad" perteneciente a "tblMovimientoAnimales", pero 
# en modificaciones anteriores a las tablas, se elimino el campo "Cantidad" de  "tblMovimientoAnimales"
# y se exporto a otra tabla llamada "tblDetalleMovAnimales"
def CantidadActualAnimales(IDCorral, fecha):
    query = """ SELECT  SUM(case WHEN  tblMovimientoAnimales.IDMovimiento = 0  THEN  tblMovimientoAnimales.Cantidad ELSE 0 END) -
                       SUM(case WHEN  tblMovimientoAnimales.IDMovimiento = 1  THEN  tblMovimientoAnimales.Cantidad  ELSE 0 END) AS SUMA
                FROM tblMovimientoAnimales 
                WHERE tblMovimientoAnimales.IDCorral= %s  AND tblMovimientoAnimales.Fecha BETWEEN 
                (SELECT FechaAsigna FROM tblCorrales WHERE tblCorrales.ID= %s ) AND %s
            """
    Cantidad = run_query2(query, (IDCorral, IDCorral, fecha))
    if Cantidad[0][0] is None:
        return -1
    else:
        return Cantidad[0][0]
    
# Funcion actualizada
def CantidadActualAnimales(IDCorral, fecha):
    query = """ SELECT  SUM(case WHEN  Aplicacion_tblmovimientoanimales.IDMovimiento_id = 0  THEN  Aplicacion_tbldetallemovanimales.Cantidad ELSE 0 END) -
SUM(case WHEN  Aplicacion_tblmovimientoanimales.IDMovimiento_id = 1  THEN  Aplicacion_tbldetallemovanimales.Cantidad  ELSE 0 END) AS SUMA
FROM Aplicacion_tblmovimientoanimales 
INNER JOIN Aplicacion_tbldetallemovanimales ON Aplicacion_tblmovimientoanimales.Folio = Aplicacion_tbldetallemovanimales.IDFolio
WHERE Aplicacion_tblmovimientoanimales.IDCorral_id= %s  AND Aplicacion_tblmovimientoanimales.Fecha BETWEEN 
(SELECT FechaAsigna FROM Aplicacion_tblcorrales WHERE Aplicacion_tblcorrales.ID= %s ) AND %s
            """
    Cantidad = run_query2(query, (IDCorral, IDCorral, fecha))
    if Cantidad[0][0] is None:
        return -1
    else:
        return Cantidad[0][0]

def run_query2(query, parameters=()):
    conn = sqlite3.connect("respaldo")
    cursor = conn.cursor()
    cursor.execute(query, parameters)
    result = cursor.fetchall()
    conn.commit()
    return result
