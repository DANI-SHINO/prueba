from itsdangerous import URLSafeTimedSerializer
from flask import current_app
import requests
import random
from app.models import Usuario, Prestamo
from flask import make_response
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from app.extensions import mail
from flask_mail import Message
from datetime import date, timedelta
import os

def generar_reporte_con_plantilla(atrasados):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # 📌 Fondo base
    c.drawImage("static/imagenes/plantilla.png", 0, 0, width=width, height=height)

    # Título
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(colors.darkgreen)
    c.drawString(50, height - 100, "Reporte de Libros Atrasados")

    # Datos tabla
    data = [["#", "Libro", "Usuario", "Fecha Vencida"]]
    for idx, p in enumerate(atrasados, start=1):
        data.append([
            str(idx),
            p.libro.titulo,
            p.usuario.correo,
            p.fecha_devolucion_esperada.strftime('%Y-%m-%d')
        ])

    # Tabla estilizada
    table = Table(data, colWidths=[40, 200, 200, 100])
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ])
    table.setStyle(style)

    # Posición tabla
    table.wrapOn(c, width, height)
    table.drawOn(c, 50, height - 300)

    c.showPage()
    c.save()

    pdf = buffer.getvalue()
    buffer.close()
    return pdf

def generar_reporte_prestados(prestados):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # 📌 Fondo base
    ruta = os.path.join(os.getcwd(), 'static', 'imagenes', 'plantilla.png')
    c.drawImage(ruta, 0, 0, width=width, height=height)

    # 📌 Título
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(colors.darkblue)
    c.drawString(50, height - 100, "📑 Reporte de Libros Más Prestados")

    # 📌 Datos tabla
    data = [["#", "Título", "Autor", "Total Préstamos"]]
    for idx, libro in enumerate(prestados, start=1):
        data.append([
            str(idx),
            libro.titulo,
            libro.autor,
            str(libro.total)
        ])

    # 📌 Tabla estilizada
    table = Table(data, colWidths=[40, 220, 150, 100])
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ])
    table.setStyle(style)

    table.wrapOn(c, width, height)
    table.drawOn(c, 50, height - 300)

    c.showPage()
    c.save()
    pdf = buffer.getvalue()
    buffer.close()
    return pdf



def generar_reporte_populares(populares):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # 📌 Fondo base
    ruta = os.path.join(os.getcwd(), 'static', 'imagenes', 'plantilla.png')
    c.drawImage(ruta, 0, 0, width=width, height=height)

    # 📌 Título
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(colors.purple)
    c.drawString(50, height - 100, "🌟 Reporte de Libros Populares")

    # 📌 Datos tabla
    data = [["#", "Título", "Autor", "Préstamos", "Reservas", "Total"]]
    for idx, libro in enumerate(populares, start=1):
        data.append([
            str(idx),
            libro.titulo,
            libro.autor,
            str(libro.prestamos),
            str(libro.reservas),
            str(libro.total)
        ])

    # 📌 Tabla estilizada
    table = Table(data, colWidths=[40, 150, 130, 70, 70, 70])
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.purple),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ])
    table.setStyle(style)

    table.wrapOn(c, width, height)
    table.drawOn(c, 50, height - 300)

    c.showPage()
    c.save()
    pdf = buffer.getvalue()
    buffer.close()
    return pdf


def generar_token(email):
    serializer = URLSafeTimedSerializer(current_app.secret_key)
    return serializer.dumps(email, salt='recuperar-contrasena')

def verificar_token(token, max_age=3600):
    serializer = URLSafeTimedSerializer(current_app.secret_key)
    try:
        email = serializer.loads(token, salt='recuperar-contrasena', max_age=max_age)
    except:
        return None
    return email

def generar_llave_prestamo():
    while True:
        nueva_llave = f"{random.randint(100, 999)}-{random.randint(100, 999)}"
        if not Usuario.query.filter_by(llave_prestamo=nueva_llave).first():
            return nueva_llave

def obtener_datos_libro_openlibrary(isbn):
    ol_url_bibkeys = f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data"

    titulo = autores = editorial = fecha = portada_url = descripcion = ''
    categoria = None

    try:
        response_bibkeys = requests.get(ol_url_bibkeys, timeout=10)
        response_bibkeys.raise_for_status()
        data_bibkeys = response_bibkeys.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al consultar OpenLibrary (bibkeys): {e}")
        return {"success": False, "error": "Error al obtener datos de OpenLibrary"}

    if f"ISBN:{isbn}" in data_bibkeys:
        libro_data_ol = data_bibkeys[f"ISBN:{isbn}"]

        titulo = libro_data_ol.get('title', '')
        autores = ', '.join(a['name'] for a in libro_data_ol.get('authors', [])) if libro_data_ol.get('authors') else ''
        editorial = ', '.join(p['name'] for p in libro_data_ol.get('publishers', [])) if 'publishers' in libro_data_ol else ''
        fecha = libro_data_ol.get('publish_date', None)

        desc_raw = libro_data_ol.get('description')
        if isinstance(desc_raw, dict):
            descripcion = desc_raw.get('value', '')
        elif isinstance(desc_raw, str):
            descripcion = desc_raw

        if 'cover' in libro_data_ol:
            portada_url = libro_data_ol['cover'].get('large') or libro_data_ol['cover'].get('medium') or libro_data_ol['cover'].get('small')
        if not portada_url and isbn:
            portada_url = f"https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg?default=false"
            try:
                check_resp = requests.head(portada_url, timeout=5)
                if not check_resp.ok:
                    portada_url = None
            except requests.exceptions.RequestException:
                portada_url = None

        mapeo_categorias = {
            "fiction": "novela",
            "novel": "novela",
            "detective and mystery stories": "novela",
            "police procedural": "thriller",
            "science fiction": "ciencia_ficcion",
            "fantasy": "fantasía",
            "thrillers": "thriller",
            "horror": "terror",
            "romance": "romance",
            "historical fiction": "novela_historica",
            "history": "historia",
            "biography": "biografia",
            "short stories": "cuento",
            "poetry": "poesia",
            "drama": "teatro",
            "comedies": "comedia",
            "juvenile fiction": "juvenil",
            "young adult fiction": "juvenil",
            "graphic novels": "historieta",
            "comics": "historieta",
            "philosophy": "filosofia",
            "essays": "ensayo",
            "true crime": "ficcion_criminal",
            "crime fiction": "ficcion_criminal",
            "political satire": "sátira",
            "satire": "sátira",
            "classic fiction": "clasico",
            "classic literature": "clasico",
            "magical realism": "realismo_magico"
        }

        edition_key = libro_data_ol.get('key')
        subjects = []
        if edition_key and edition_key.startswith('/books/'):
            olid = edition_key.split('/')[-1]
            ol_url_edition = f"https://openlibrary.org/books/{olid}.json"

            try:
                response_edition = requests.get(ol_url_edition, timeout=10)
                response_edition.raise_for_status()
                edition_data_full = response_edition.json()

                if not descripcion:
                    desc_ed = edition_data_full.get('description')
                    if isinstance(desc_ed, dict):
                        descripcion = desc_ed.get('value', '')
                    elif isinstance(desc_ed, str):
                        descripcion = desc_ed

                subjects = edition_data_full.get('subjects', [])

                if not subjects and 'works' in edition_data_full:
                    work_key = edition_data_full['works'][0]['key']
                    ol_url_work = f"https://openlibrary.org{work_key}.json"
                    try:
                        response_work = requests.get(ol_url_work, timeout=10)
                        response_work.raise_for_status()
                        work_data = response_work.json()

                        subjects = work_data.get('subjects', [])
                        if not descripcion:
                            desc_work = work_data.get('description')
                            if isinstance(desc_work, dict):
                                descripcion = desc_work.get('value', '')
                            elif isinstance(desc_work, str):
                                descripcion = desc_work

                    except requests.exceptions.RequestException:
                        pass

            except requests.exceptions.RequestException:
                pass

        categoria_mapeada = None
        for s in subjects:
            s_lower = s.lower().strip()
            if s_lower in mapeo_categorias:
                categoria_mapeada = mapeo_categorias[s_lower]
                break

        if not categoria_mapeada:
            for s in subjects:
                s_lower = s.lower().strip()
                for key in mapeo_categorias:
                    if key in s_lower:
                        categoria_mapeada = mapeo_categorias[key]
                        break
                if categoria_mapeada:
                    break

        if not categoria_mapeada:
            for s in subjects:
                s_lower = s.lower().strip()
                if "fiction" in s_lower:
                    categoria_mapeada = "novela"
                    break
                elif "science" in s_lower:
                    categoria_mapeada = "ciencia_ficcion"
                    break
                elif "fantasy" in s_lower:
                    categoria_mapeada = "fantasía"
                    break
                elif "horror" in s_lower:
                    categoria_mapeada = "terror"
                    break
                elif "biography" in s_lower:
                    categoria_mapeada = "biografia"
                    break
                elif "history" in s_lower:
                    categoria_mapeada = "historia"
                    break
                elif "political" in s_lower:
                    categoria_mapeada = "sátira"
                    break

        if not categoria_mapeada:
            categoria_mapeada = "otros"

        categoria = categoria_mapeada

        return {
            "success": True,
            "titulo": titulo or '',
            "autor": autores or '',
            "editorial": editorial or '',
            "fecha_publicacion": fecha or '',
            "isbn": isbn,
            "portada_url": portada_url or '',
            "descripcion": descripcion or '',
            "categoria": categoria or ''
        }

    return {"success": False, "error": "Libro no encontrado en OpenLibrary"}

def enviar_recordatorios(app):
    with app.app_context():
        mañana = date.today() + timedelta(days=1)
        prestamos = Prestamo.query.filter(
            Prestamo.estado == 'activo',
            Prestamo.fecha_devolucion_esperada == mañana
        ).all()

        for prestamo in prestamos:
            usuario = prestamo.usuario
            libro = prestamo.libro

            msg = Message(
                '⏰ Recordatorio de Devolución',
                sender='noreply@biblioteca.com',
                recipients=[usuario.correo]
            )
            msg.body = f"""
Hola {usuario.nombre},

Te recordamos que debes devolver el libro "{libro.titulo}" mañana.

📅 Fecha de devolución esperada: {prestamo.fecha_devolucion_esperada}

¡Gracias por usar nuestra biblioteca!

Biblioteca Avocado
"""
            mail.send(msg)



