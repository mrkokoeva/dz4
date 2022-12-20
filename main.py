import telebot
import asyncio
from telebot.async_telebot import AsyncTeleBot
import aioschedule

import functions

TOKEN = "5888526093:AAE9GRembDaivHl07K4E-xZmnxJTi48gEFU"

bot = AsyncTeleBot(TOKEN)


@bot.message_handler(commands=['start'])
async def start(message):
    text = "Добро пожаловать в нашу увлекательную игру, где придется бороться с монстрами. Для того, чтобы" \
           "зарегистрироваться вбейте /start_game <ник персонажа>. Чтобы закончить игру напишите /finish_game"
    await bot.send_message(message.chat.id, text=text)


@bot.message_handler(commands=['start_game'])
async def start_game(message):
    mes = message.text.split()
    if len(mes) == 1:
        await bot.send_message(message.chat.id, "Неправильный ввод! Напигите ваш ник, иначе регистрация не пройдет(")
    elif not functions.check_user(message.chat.id):
        us_id = message.chat.id
        nickname = " ".join(mes[1:])
        functions.new_user(us_id, nickname)
        await bot.send_message(message.chat.id, "Вы успешно зарегистрировались! Начнем с того, что вы находитесь изначально в городе. Вы можете перемещаться в доступные другие города или подземелья для сражения с монстрами. Напиши /locations для того, чтобы узнать в какие другие локации вы можете пойти. Чтобы пойти в доступную напишите /go_to_location <название локации>")
    else:
        await bot.send_message(message.chat.id, "Вы уже зарегистрированы были ранее")


@bot.message_handler(commands=['locations'])
async def locations(message):
    user_id = message.chat.id
    if not functions.check_user(user_id):
        await bot.send_message(message.chat.id, "Зарегистрируйтесь для начала")
        return
    ans = functions.loc(message.chat.id)
    await bot.send_message(message.chat.id, "Вот список доступных локаций: " + ', '.join(ans))


@bot.message_handler(commands=["travel"])
async def go_to_location(message):
    user_id = message.chat.id
    if not functions.check_user(user_id):
        await bot.send_message(message.chat.id, "Зарегистрируйтесь для начала")
        return
    if functions.go_to_location(message.chat.id, " ".join(message.text.split()[1:])) == 0:
        await bot.send_message(message.chat.id, "Вы не можете перейти в эту локацию. Посмотрите с помощью /locations "
                                                "список доступных")
    else:
        await bot.send_message(message.chat.id, "Вы перешли в локацию " + functions.cur_loc(message.chat.id))


@bot.message_handler(commands=["cur_loc"])
async def cur_loc(message):
    user_id = message.chat.id
    if not functions.check_user(user_id):
        await bot.send_message(message.chat.id, "Зарегистрируйтесь для начала")
        return
    await bot.send_message(message.chat.id, "Вы находитесь в локации " + functions.cur_loc(message.chat.id))


@bot.message_handler(commands=["buy"])
async def buy(message):
    user_id = message.chat.id
    if not functions.check_user(user_id):
        await bot.send_message(message.chat.id, "Зарегистрируйтесь для начала")
        return
    item_name = " ".join(message.text.split()[1:])
    response = functions.buy_item(user_id, item_name)
    if response == 0:
        await bot.send_message(message.chat.id, "Вы успешно купили " + item_name)
    elif response == 1:
        await bot.send_message(message.chat.id, "Недостаточно денег на покупку " + item_name)
    elif response == 2:
        await bot.send_message(message.chat.id, "Нет такого предмета:  " + item_name)
    elif response == 3:
        await bot.send_message(message.chat.id, "Вы не в городе")


@bot.message_handler(commands=["sell"])
async def sell(message):
    user_id = message.chat.id
    if not functions.check_user(user_id):
        await bot.send_message(message.chat.id, "Зарегистрируйтесь для начала")
        return
    item_name = " ".join(message.text.split()[1:])
    response = functions.sell_item(user_id, item_name)
    if response == 0:
        await bot.send_message(message.chat.id, "Вы успешно продали " + item_name)
    elif response == 1:
        await bot.send_message(message.chat.id, "У вас нет такого предмета в инвентаре: " + item_name)
    elif response == 2:
        await bot.send_message(message.chat.id, "Нет такого предмета:  " + item_name)
    elif response == 3:
        await bot.send_message(message.chat.id, "Вы не в городе")


@bot.message_handler(commands=["equip"])
async def equip(message):
    user_id = message.chat.id
    if not functions.check_user(user_id):
        await bot.send_message(message.chat.id, "Зарегистрируйтесь для начала")
        return
    item_name = " ".join(message.text.split()[1:])
    response = functions.equip(user_id, item_name)
    if response == 1:
        await bot.send_message(message.chat.id, "У вас нет предмета в инвентаре")
        return
    await bot.send_message(message.chat.id, "Вы успешно надели предмет")


@bot.message_handler(commands=["unequip"])
async def unequip(message):
    user_id = message.chat.id
    if not functions.check_user(user_id):
        await bot.send_message(message.chat.id, "Зарегистрируйтесь для начала")
        return
    item_type = " ".join(message.text.split()[1:])
    response = functions.unequip(user_id, item_type)
    if response == 1:
        await bot.send_message(message.chat.id, "Нет такого предмета у вас")
        return
    else:
        await bot.send_message(message.chat.id, "Вы успешно сняли предмет")
        return


@bot.message_handler(commands=["stats"])
async def unequip(message):
    user_id = message.chat.id
    if not functions.check_user(user_id):
        await bot.send_message(message.chat.id, "Зарегистрируйтесь для начала")
        return
    lst = functions.stats(user_id)
    txt = "Level: " + str(lst[0]) + '\n' + "HP: " + str(lst[1]) + '\n' + "XP: " + str(lst[2]) + '\n' + "Money: " + str(lst[3]) + '\n' + "Location: " + str(lst[4]) + "\nAttack: " + str(lst[5]) + '\n' + "Armour: " + str(lst[6])
    await bot.send_message(message.chat.id, txt)


async def scheduler():
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def main():
    await asyncio.gather(bot.infinity_polling(), scheduler())

if __name__ == '__main__':
    asyncio.run(main())