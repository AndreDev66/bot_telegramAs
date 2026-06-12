from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
import os

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def say_hello(update: Update, context):
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

async def mostrar_proyectos(update: Update, context):
    # Usar triple comillas para texto multilínea correctamente
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

async def mostrar_contacto(update: Update, context):
    teclado = InlineKeyboardMarkup([
        [InlineKeyboardButton("📧 Mostrar correo", callback_data="mostrar_correo")],
        [InlineKeyboardButton("📞 Mostrar teléfono", callback_data="mostrar_telefono")],
    ])
    await update.message.reply_text("Selecciona qué dato quieres ver:", reply_markup=teclado)

async def botones_contacto(update: Update, context):
    query = update.callback_query
    await query.answer()  # siempre responde para quitar la "carga"
    
    if query.data == "mostrar_correo":
        await query.edit_message_text("📧 Correo: `unisocorroandres@gmail.com`", parse_mode='Markdown')
    elif query.data == "mostrar_telefono":
        await query.edit_message_text("📞 Teléfono: `+58 412 5142837`", parse_mode='Markdown')

async def mostrar_stack(update: Update, context):
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


def main():
    if not TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN no está configurado en las variables de entorno.")

    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", say_hello))
    application.add_handler(CommandHandler("proyectos", mostrar_proyectos))
    application.add_handler(CommandHandler("contacto", mostrar_contacto))
    application.add_handler(CommandHandler("stack", mostrar_stack))
    application.add_handler(CallbackQueryHandler(botones_contacto))

    # Ejecutar sin argumentos (recibe todos los tipos por defecto)
    application.run_polling()


if __name__ == "__main__":
    main()