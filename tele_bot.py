import telegram.bot
from telegram import (
    ReplyMarkup,
    Message,
    InlineKeyboardMarkup,
    Poll,
    MessageId,
    Update,
    Chat,
    CallbackQuery,
)

from telegram.ext.callbackdatacache import CallbackDataCache
from telegram.utils.types import JSONDict, ODVInput, DVInput
from ..utils.helpers import DEFAULT_NONE
import telegram
import telegramApi
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, CallbackQueryHandler

# Включить логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Обработчики команд ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Опция 1", callback_data='option_1')],
        [InlineKeyboardButton("Опция 2", callback_data='option_2')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Пожалуйста, выберите опцию:", reply_markup=reply_markup)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Я эхо-бот с inline-кнопками. Используйте /start для начала.")


# --- Обработчики сообщений ---

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


# --- Обработчики callback-запросов ---

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer() # Ответить на callback-запрос, чтобы убрать "часики"

    if query.data == 'option_1':
        text = "Вы выбрали опцию 1!"
    elif query.data == 'option_2':
        text = "Вы выбрали опцию 2!"
    else:
        text = "Неизвестная опция."

    await query.edit_message_text(text=text) # Редактировать сообщение с кнопками

# --- Обработчик неизвестных команд ---

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Извините, я не знаю такой команды.")


# --- Обработчик ошибок ---
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before sending the message, so you can see what happened
    logger.error(f"Update {update} caused error {context.error}")

    # Optionally, send the error to the developer.
    await update.message.reply_text(f"Произошла ошибка: {context.error}")


if __name__ == '__main__':
    # Замените 'YOUR_TELEGRAM_BOT_TOKEN' на ваш токен бота
    application = ApplicationBuilder().token('.......').build()

    # --- Добавление обработчиков ---
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo)) # Обработчик эхо
    application.add_handler(CallbackQueryHandler(button)) # Обработчик callback-запросов от inline-кнопок
    application.add_handler(MessageHandler(filters.COMMAND, unknown)) # Обработчик неизвестных команд
    application.add_error_handler(error_handler)

    # --- Запуск бота ---
    application.run_polling()

