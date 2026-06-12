import os
import asyncio
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import JSONResponse
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    ContextTypes
)
from telegram.request import HTTPXRequest
import uvicorn

# ================= CONFIGURACIÓN =================
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN no está configurado en las variables de entorno.")

# Render asigna automáticamente RENDER_EXTERNAL_URL, si no está (ejecución local) usamos placeholder
BASE_URL = os.getenv("RENDER_EXTERNAL_URL", "http://localhost:8000")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"{BASE_URL}{WEBHOOK_PATH}"
# =================================================

# ================= TUS FUNCIONES ORIGINALES (adaptadas solo el parse_mode) =================

async def say_hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f" *👋 ¡Hola {user.first_name}! Te doy la bienvenida a este Bot de Demostración.\n Este espacio fue desarrollado  por mi creador como parte de su portafolio digital para mostrar la integración de servicios y automatización en Telegram.*\n\n"
        "🛠️ ¿Qué puedes hacer aquí?\n\n"
        "• Explorar una lista de proyectos variados.\n"
        "• Ver las tecnologías con las que trabaja mi creador.\n"
        "• Probar comandos interactivos en tiempo real.\n\n"
        "👨‍💻 *Creador:* Andrés Socorro\n\n"
        "📌 *Comandos disponibles:*\n"
        "• `/proyectos` - Ver proyectos\n"
        "• `/contacto` - Contactar\n"
        "• `/stack` - Tecnologías y herramientas que utilizo.\n\n"
        "⚡ ¡Usa el que necesites!",
        parse_mode='Markdown'
    )

async def mostrar_proyectos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = """
📁 *Proyectos*
━━━━━━━━━
• 🤖 Bot de Telegram
• 🌐🔗 [Sitio web](https://andrewdev2004.neocities.org/)
• 📁🔗 [Portafolio Digital](https://andrewdev2004.neocities.org/portafolio)
• 📊🔗 [Github Dashboard](https://github.com/AndreDev66)
"""
    await update.message.reply_text(
        texto,
        parse_mode='Markdown',
        disable_web_page_preview=True
    )

async def mostrar_contacto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    teclado = InlineKeyboardMarkup([
        [InlineKeyboardButton("📧 Mostrar correo", callback_data="mostrar_correo")],
        [InlineKeyboardButton("📞 Mostrar teléfono", callback_data="mostrar_telefono")],
    ])
    await update.message.reply_text("Selecciona qué dato quieres ver:", reply_markup=teclado)

async def botones_contacto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "mostrar_correo":
        await query.edit_message_text("📧 Correo: `unisocorroandres@gmail.com`", parse_mode='Markdown')
    elif query.data == "mostrar_telefono":
        await query.edit_message_text("📞 Teléfono: `+58 412 5142837`", parse_mode='Markdown')

async def mostrar_stack(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = """🛠️ *Tecnologías y Herramientas*
━━━━━━━━━━━━━━━━━━
💻 Stack Tecnológico

Estas son las principales herramientas, lenguajes y librerías que utilizamos para construir soluciones de software, desde aplicaciones de escritorio hasta aplicabilidades web y gráficos por computadora.:

🐍 Lenguajes & Backend
• Python (Desarrollo principal, automatización y lógica de negocio)

🎨 UI/UX & Interfaces
• CustomTkinter & Pillow (Interfaces de escritorio modernas y estilizadas)
• HTML5, CSS3 y JavaScript (Diseño web intuitivo y responsivo)

🎮 Gráficos por Computadora
• OpenGL & Raylib (Programación de gráficos 3D y renderizado)

🛠️ Herramientas & Despliegue
• Git & GitHub (Control de versiones y entornos colaborativos)
• Netlify, Neocities e InfinityFree (Despliegue y hosting web)
• Telegram Bot API (Integración de bots y automatización en Telegram)"""
    await update.message.reply_text(
        texto,
        parse_mode='Markdown',
        disable_web_page_preview=True
    )

# ================= CONFIGURACIÓN DE WEBHOOK CON STARLETTE =================

async def healthcheck(request):
    """Endpoint para que Render verifique que la app está viva."""
    return JSONResponse({"status": "ok"})

async def handle_telegram(request):
    """Maneja las solicitudes entrantes de Telegram."""
    request_data = await request.json()
    # Construimos la aplicación de telegram-bot con todos los handlers
    ptb_app = Application.builder().token(TOKEN).build()
    ptb_app.add_handler(CommandHandler("start", say_hello))
    ptb_app.add_handler(CommandHandler("proyectos", mostrar_proyectos))
    ptb_app.add_handler(CommandHandler("contacto", mostrar_contacto))
    ptb_app.add_handler(CommandHandler("stack", mostrar_stack))
    ptb_app.add_handler(CallbackQueryHandler(botones_contacto))

    # Creamos el objeto Update desde los datos JSON
    update = Update.de_json(request_data, ptb_app.bot)
    # Procesamos la actualización
    await ptb_app.process_update(update)
    return JSONResponse({"ok": True})

# Aplicación Starlette con las rutas
app = Starlette(routes=[
    Route("/healthcheck", healthcheck, methods=["GET"]),
    Route(WEBHOOK_PATH, handle_telegram, methods=["POST"]),
])

async def set_webhook():
    """Configura el webhook en Telegram al iniciar el servidor."""
    bot = Bot(TOKEN, request=HTTPXRequest())
    # Desactivamos el webhook anterior por si acaso (opcional)
    await bot.delete_webhook()
    # Establecemos el nuevo webhook
    await bot.set_webhook(WEBHOOK_URL, allowed_updates=Update.ALL_TYPES)
    print(f"✅ Webhook establecido correctamente en {WEBHOOK_URL}")

def start_webhook():
    """Función principal que inicia el servidor Starlette/Uvicorn."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(set_webhook())
    # Iniciamos el servidor
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))

if __name__ == "__main__":
    start_webhook()
