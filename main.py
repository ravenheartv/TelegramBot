# Importar las clases necesarias para interactuar con la API de Telegram y manejar actualizaciones
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import random  # Importar la librería random para generar números aleatorios
import os  # Para manejar variables de entorno
from dotenv import load_dotenv  # Para cargar el archivo .env
import asyncio  # Para manejar corrutinas
import re  # Para validar las expresiones matemáticas
import datetime  # Para obtener la fecha y hora actual

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener la API Key desde las variables de entorno
api_key = os.getenv("TELEGRAM_API_KEY")

# Validar que la API Key está configurada
if not api_key:
    raise ValueError("No se encontró la API Key. Por favor, configúrala en el archivo .env.")

# Define el comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("¡Hola! Soy tu bot. Usa /hola para saludarme,/saludo [Nombre] para que te salude, /aleatorio para un número aleatorio, /gif para recibir un GIF, /name para saber tu nombre, /math para realizar operaciones matemáticas, /coinflip para lanzar una moneda, /time para obtener la hora actual.")

# Define el comando /hola
async def hola(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Bomboclat!!")

# Define el comando /aleatorio
async def aleatorio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    numero = random.randint(1, 100)
    await update.message.reply_text(f"Numeroclat bombo es: {numero}")

# Define el comando /gif
async def gif(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    gif_url = "https://media.giphy.com/media/5GoVLqeAOo6PK/giphy.gif"
    await update.message.reply_animation(gif_url)

# Define el comando /name
async def name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Obtiene el nombre del usuario desde el mensaje
    user_name = update.message.from_user.first_name  # Puedes acceder al nombre con `first_name`
    
    # Responde con un saludo y el nombre del usuario
    await update.message.reply_text(f"¡Hola {user_name}!")

# Comando /saludo
async def saludo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Obtiene el nombre proporcionado por el usuario (el primer argumento después del comando)
    if context.args:
        nombre = ' '.join(context.args)  # Junta los posibles múltiples argumentos en un solo nombre
        await update.message.reply_text(f"¡Hola, {nombre}!")
    else:
        await update.message.reply_text("Por favor, proporciona un nombre después del comando, por ejemplo: /saludo Juan.")


# Define el comando /math
async def math(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Recibe el mensaje del usuario, extrae el texto después de /math
    expression = ' '.join(context.args)

    if expression:
        # Usamos una expresión regular para validar que la operación es válida
        if re.match(r"^[0-9+\-*/().\s]*$", expression):  # Validar que solo contiene caracteres seguros para operaciones matemáticas
            try:
                # Evalúa la expresión matemática
                result = eval(expression)
                await update.message.reply_text(f"El resultado de {expression} es: {result}")
            except Exception as e:
                await update.message.reply_text(f"Hubo un error al procesar la operación: {e}")
        else:
            await update.message.reply_text("Por favor, ingresa una operación matemática válida.")
    else:
        await update.message.reply_text("Por favor, ingresa una operación después de /math, como '/math 2+2'.")

# Define el comando /coinflip
async def coinflip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Simula el lanzamiento de una moneda
    flip = random.choice(["Cara", "Cruz"])
    await update.message.reply_text(f"El lanzamiento de la moneda resultó en: {flip}")

# Define el comando /time
async def time(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Obtiene la hora actual
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await update.message.reply_text(f"La hora actual es: {current_time}")

# Configuración principal del bot
async def main():
    # Crear la aplicación del bot
    app = ApplicationBuilder().token(api_key).build()

    # Agregar manejadores para los comandos
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("hola", hola))
    app.add_handler(CommandHandler("aleatorio", aleatorio))
    app.add_handler(CommandHandler("gif", gif))  # Agregar el comando /gif
    app.add_handler(CommandHandler("name", name))  # Agregar el comando /name
    app.add_handler(CommandHandler("math", math))  # Agregar el comando /math
    app.add_handler(CommandHandler("coinflip", coinflip))  # Agregar el comando /coinflip
    app.add_handler(CommandHandler("time", time))  # Agregar el comando /time
    app.add_handler(CommandHandler("saludo", saludo))

    # Iniciar el bot
    print("El bot está corriendo...")
    await app.run_polling()

# Punto de entrada del script
if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()  # Permite reutilizar el bucle de eventos en entornos interactivos
    asyncio.run(main())  # Ejecuta la corrutina principal