from fastapi import FastAPI, Request, Form, HTTPException, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from app.database import get_db_connection

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configuración de plantillas
templates = Jinja2Templates(directory="app/templates")

# Página principal en /index.html
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Nuevos destacados en /index.html/nuevos_destacados.html
@app.get("/nuevos_destacados.html", response_class=HTMLResponse)
async def nuevos_destacados(request: Request):
    juegos = [{"nombre": "Aloft", "descripcion": "Aloft es un juego de supervivencia acogedor y apacible ambientado entre nubes, donde puedes transformar cualquier isla en una nave voladora con la que explorar los cielos."},
              {"nombre": "Path Of Exile 2", "descripcion": "Path of Exile 2 es un RPG de acción gratuito de nueva generación creado por Grinding Gear Games, con un modo cooperativo de hasta seis jugadores."},
              {"nombre": "Farming Simulator 25", "descripcion": "¡Disfruta de la vida en la granja con Farming Simulator 25! Construye tu legado en solitario o de forma cooperativa en modo multijugador."},
              {"nombre": "Dynasty Warriors Origins", "descripcion": "Vive emocionantes batallas como un héroe sin nombre en los Tres Reinos. La acción más emocionante en la historia de la serieCampos de batalla llenos de tensión en los que te enfrentas a ejércitos inmensos que parecen no tener fin."},
              {"nombre": "Assetto Corsa Evo", "descripcion": "Assetto Corsa EVO eleva aún más el listón de realismo que ha hecho de la franquicia uno de los simuladores de conducción más populares de la última década."}]

    return templates.TemplateResponse("nuevos_destacados.html", {"request": request, "juegos": juegos})

# Top clásicos en /index.html/top_clasicos.html
@app.get("/top_clasicos.html", response_class=HTMLResponse)
async def top_clasicos(request: Request):
    clasicos = [{"nombre": "Super Mario 64", "año": 1996},
                {"nombre": "The Legend of Zelda Ocarina of Time", "año": 1998},
                {"nombre": "Final Fantasy VII", "año": 1997}]
    return templates.TemplateResponse("top_clasicos.html", {"request": request, "clasicos": clasicos})

# Por género en /index.html/por_genero.html
@app.get("/por_genero.html", response_class=HTMLResponse)
async def por_genero(request: Request):
    generos = [
        {"nombre": "Acción", "juegos": ["God of War", "Call of Duty", "Apex Legends"]},
        {"nombre": "Aventura", "juegos": ["The Legend of Zelda", "Tomb Raider", "Uncharted"]},
        {"nombre": "Deporte", "juegos": ["FIFA 21", "NBA 2K21", "Pro Evolution Soccer"]},
        {"nombre": "RPG", "juegos": ["The Witcher 3", "Skyrim", "Dark Souls"]},
        {"nombre": "Estrategia", "juegos": ["StarCraft", "Age of Empires", "Civilization VI"]},
    ]
    return templates.TemplateResponse("por_genero.html", {"request": request, "generos": generos}) 

# Endpoint para obtener la lista de juegos guardados
@app.get("/mi_lista.html", response_class=HTMLResponse)
async def mi_lista(request: Request):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT nombre FROM juegos")  # Obtener la lista de juegos de la BD
    juegos = [fila[0] for fila in cursor.fetchall()]
    cursor.close()
    db.close()
    
    return templates.TemplateResponse("mi_lista.html", {"request": request, "juegos": juegos})

# Endpoint para añadir un juego
@app.post("/mi_lista.html/agregar")
async def agregar_juego(nombre: str = Form(...)):
    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO juegos (nombre) VALUES (%s)", (nombre,))
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        db.close()
    return RedirectResponse(url="/mi_lista.html", status_code=303)

# Endpoint para actualizar un juego
@app.post("/mi_lista.html/actualizar")
async def actualizar_juego(nombre_actual: str = Form(...), nombre_nuevo: str = Form(...)):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("UPDATE juegos SET nombre = %s WHERE nombre = %s", (nombre_nuevo, nombre_actual))
    db.commit()
    cursor.close()
    db.close()
    return RedirectResponse(url="/mi_lista.html", status_code=303)

# Endpoint para eliminar un juego
@app.post("/mi_lista.html/eliminar")
async def eliminar_juego(nombre: str = Form(...)):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM juegos WHERE nombre = %s", (nombre,))
    db.commit()
    cursor.close()
    db.close()
    return RedirectResponse(url="/mi_lista.html", status_code=303)
