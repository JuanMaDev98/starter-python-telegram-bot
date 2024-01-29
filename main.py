import os
from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException, Depends
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackContext, ConversationHandler
from pydantic import BaseModel

class TelegramUpdate(BaseModel):
    update_id: int
    message: dict

app = FastAPI()

# Load variables from .env file if present
load_dotenv()

# Read the variable from the environment (or .env file)
bot_token = os.getenv('BOT_TOKEN')
secret_token = os.getenv("SECRET_TOKEN")
# webhook_url = os.getenv('CYCLIC_URL', 'http://localhost:8181') + "/webhook/"

bot = Bot(token=bot_token)
# bot.set_webhook(url=webhook_url)
# webhook_info = bot.get_webhook_info()
# print(webhook_info)

def auth_telegram_token(x_telegram_bot_api_secret_token: str = Header(None)) -> str:
    return True # uncomment to disable authentication
    if x_telegram_bot_api_secret_token != secret_token:
        raise HTTPException(status_code=403, detail="Not authenticated")
    return x_telegram_bot_api_secret_token

@app.post("/webhook/")
async def handle_webhook(update: TelegramUpdate, token: str = Depends(auth_telegram_token)):
    chat_id = update.message["chat"]["id"]
    text = update.message["text"]
    # print("Received message:", update.message)

    if text == "/start":
        await bot.send_message(chat_id=chat_id, reply_to_message_id=update.message["message_id"], text=f"👋 Hola,\nEste bot te ayudará a aumentar tus horas de juego en Steam\\.\nEscribe *_/help_* para ver los comandos disponibles\\.\n\n[_Mi Youtube_](https://www.youtube.com/channel/UCElCoULDa68Yzqi1slcWvKA?sub_confirmation=1)", parse_mode='MarkdownV2')
    elif text == "/help":
        await bot.send_message(chat_id=chat_id, reply_to_message_id=update.message["message_id"], text=f"❓ Usando este bot es muy simple aumentar tus horas de juego en Steam\\.\n\nComandos disponibles:\n *_/account_* \- configura tus credenciales de Steam, va seguido de tu nombre de usuario de steam y contraseña, separados por espacios\\.\n *_/games_* \- va seguido del ID de los juegos de Steam que quieres jugar separados por espacios. Máximo 30 juegos\\.\n *_/farm_* \- comienza a farmear horas, va seguido de la cantidad de horas que quieres farmear\\.\n\n[_Mi Youtube_](https://www.youtube.com/channel/UCElCoULDa68Yzqi1slcWvKA?sub_confirmation=1)", parse_mode='MarkdownV2')
    elif text.startswith("/account"):
        try:
            user_input = update.message["text"].split()
            steam_user = user_input[1]
            steam_password = user_input[2]
        except IndexError:
            await bot.send_message(chat_id=chat_id, reply_to_message_id=update.message["message_id"], text=f"🚫 Mal uso del comando *_/account_*, el formato correcto sería: \\ \n\n*_/account username password_*", parse_mode='MarkdownV2')
            return
        await bot.send_message(chat_id=chat_id, reply_to_message_id=update.message["message_id"], text=f"*_Usuario de Steam_*:  {steam_user}\\\n*_Password de Steam_*: {steam_password}\\\n\n💾 Nueva configuración de la cuenta guardada", parse_mode='MarkdownV2')
    elif text.startswith("/games"):
        try:
            steam_games = update.message["text"].split()[1:]
            print(steam_games)
        except IndexError:
            await bot.send_message(chat_id=chat_id, reply_to_message_id=update.message["message_id"], text=f"🚫 Mal uso del comando *_/games_*, el formato correcto sería: \\ \n\n*_/games IDgame1 IDgame2 IDgame3 ... IDgame30_*\\ \n\nEl máximo de juegos a la vez es 30", parse_mode='MarkdownV2')
            return
        await bot.send_message(chat_id=chat_id, reply_to_message_id=update.message["message_id"], text=f"🎮 Lista de juegos actualizada a: \\ \n\n{steam_games}", parse_mode='MarkdownV2')
    elif text == "/farm":
        await bot.send_message(chat_id=chat_id, reply_to_message_id=update.message["message_id"], text=f"Usando este bot es muy simple aumentar tus horas de juego en Steam\\.\n\nComandos disponibles:\n *_/config_* \- configura tus credenciales de Steam\\.\n *_/farm_* \- comienza a farmear horas\\.\n\n[_Mi Youtube_](https://www.youtube.com/channel/UCElCoULDa68Yzqi1slcWvKA?sub_confirmation=1)", parse_mode='MarkdownV2')
    else:
        await bot.send_message(chat_id=chat_id, reply_to_message_id=update.message["message_id"], text=f"🚫 Ese no es un comando válido, para más información de como usar el bot usa el comando *_/help_* o mira el tutorial en mi [_canal de Youtube_](https://www.youtube.com/channel/UCElCoULDa68Yzqi1slcWvKA?sub_confirmation=1)", parse_mode='MarkdownV2')
        
    
    return {"ok": True}
