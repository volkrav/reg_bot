from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware


class DelMessage(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, data: dict):
        if update.message:
            await update.message.delete()


class CallbackAnswer(BaseMiddleware):
    async def on_pre_process_callback_query(self, cq: types.CallbackQuery, data: dict):
        await cq.answer()
