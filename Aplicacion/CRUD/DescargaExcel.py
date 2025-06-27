import pandas as pd
from django.http import HttpResponse
from Aplicacion.models import tblServido
from datetime import datetime
from io import BytesIO

def xlsx(request):
    fecha_actual = datetime.today()
    formatted_fecha_actual = fecha_actual.strftime("%Y-%m-%d %H-%M-%S")

    # Obtener los datos que deseas incluir en el archivo XLSX
    TContenido = tblServido.objects.filter(IDEstatus_id=8).order_by('-ID')

    # Crear un DataFrame de pandas con los datos
    data = []
    for item in TContenido:
        data.append([
            item.ID,
            item.Folio,
            item.IDCliente.Nombre if item.IDCliente else '',
            item.IDCorral.Descripcion if item.IDCorral else '',
            item.IDProducto.Descripcion if item.IDProducto else '',
            item.IDEstatus.Descripcion if item.IDEstatus else '',
            item.CantidadSolicitada,
            item.CantidadServida,
            item.Prioridad,
            item.Fecha.strftime('%Y-%m-%d') if item.Fecha else '',  # Formatear la fecha
            item.FechaServida.strftime('%Y-%m-%d') if item.FechaServida else '',
        ])

    df = pd.DataFrame(data, columns=[
        'ID', 'Folio', 'Cliente', 'Corral', 'Producto', 'Estatus',
        'Cantidad Solicitada', 'Cantidad Servida', 'Prioridad', 'Fecha', 'Fecha Servida'
    ])

    # Crear un objeto BytesIO para almacenar el archivo XLSX
    xlsx_buffer = BytesIO()

    # Crear un escritor de Excel con XlsxWriter
    excel_writer = pd.ExcelWriter(xlsx_buffer, engine='xlsxwriter')
    df.to_excel(excel_writer, sheet_name='Servidos', index=False)

    # Obtener el objeto XlsxWriter y configurar el formato de fecha
    workbook = excel_writer.book
    date_format = workbook.add_format({'num_format': 'yyyy-mm-dd'})
    worksheet = excel_writer.sheets['Servidos']

    # Aplicar el formato de fecha a las columnas de fecha
    worksheet.set_column('J:K', None, date_format)

    # Cerrar el escritor de Excel para guardar el archivo
    excel_writer.close()

    # Configurar la respuesta HTTP para el archivo XLSX
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="Servidos_{formatted_fecha_actual}.xlsx"'
    xlsx_buffer.seek(0)
    response.write(xlsx_buffer.read())

    return response