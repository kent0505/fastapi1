from aiogram         import Router, F
from aiogram.filters import Command
from aiogram.types   import Message
from src.bot.utils   import *

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(f"Hello {message.from_user.username}")


@router.message(Command("balance"))
async def cmd_balance(message: Message):
    amount = format_number(get_amount())
    await message.answer(f"Баланс: {amount} сум")


@router.message()
async def all_messages(message: Message):
    if (check_text(message.text)):
        if (message.text[0] == "-"):
            amount = get_amount()
            amount = amount - int(message.text[1:])
            save_amount(str(amount))
            # await message.answer(f"Баланс: {format_number(amount)} сум")
        else:
            amount = get_amount()
            amount = amount + int(message.text[1:])
            save_amount(str(amount))
            # await message.answer(f"Баланс: {format_number(amount)} сум")
    else:
        await message.delete()


# @router.message(F.text == "-")
# async def filter_minus(message: Message):
#     await message.answer(f"Вы ввели {message.text}")