import logging
import asyncio
from aiogram import Router,F,Bot
from aiogram.types import Message,CallbackQuery,FSInputFile,ReplyKeyboardRemove
from aiogram.filters import Command
from baza import insert_user , insert_client,get_admin,get_user,get_all_clients
from keyboards.inline import start_kb,qayta_kb,lang_keyb,last,stop,are_you_sure
from states import Zaqaz,AdminState,Lang
from aiogram.fsm.context import FSMContext
from keyboards.reply import phone_kb
from config import TOKEN,INSTA,TG,SAYT
from datetime import datetime
from admin import IsBotAdminFilter
from languages import languages

ADMIN = [1212795522,-1002219577562]

bot = Bot(token=TOKEN)

router = Router()

now = datetime.now()

users_lang = {}

def user_lang_save(user_id,lang):
    users_lang[user_id] = lang



@router.message(Command('reklama'), IsBotAdminFilter(ADMIN))
async def ask_ad_content(message: Message, state: FSMContext):
    await message.answer("Reklama uchun post yuboring")
    await state.set_state(AdminState.ask_ad_content)


    

   
@router.message(Command('clients'),IsBotAdminFilter(ADMIN))
async def all_clients(message:Message):
    for client in get_all_clients():
        for i in ADMIN:
            
            await bot.send_message(i,f'Id : {client[0]}\nClient : {client[2]}\nLoyiha : {client[1]}\nTelefon raqam : {client[4]}\nUsername : {client[3]}\nYuborilgan vaqt : {str(client[5])[:19]}')
        

@router.message(AdminState.ask_ad_content, IsBotAdminFilter(ADMIN))
async def send_ad_to_users(message: Message, state: FSMContext):
    users = get_user()
    count = 0
    for user in users:
        user_id = user
        try:
            await message.send_copy(chat_id=user_id)
            count += 1
            await asyncio.sleep(0.05)
        except Exception as error:
            logging.info(f"Ad did not send to user: {user_id}. Error: {error}")
    await message.answer(text=f"Reklama {count} ta foydalauvchiga muvaffaqiyatli yuborildi.")
    await state.clear()


@router.message(Command('start'))
async def lang_to(msg:Message):
    full_name = msg.from_user.full_name
    tg_id = msg.from_user.id
    tg_user = msg.from_user.username
    insert_user(full_name,tg_id,tg_user,now)
    if tg_id in users_lang:
        txt = languages[users_lang[tg_id]]['start']
        
        await msg.answer( txt,reply_markup=start_kb(users_lang[tg_id],'start_kb_1','start_kb_2','start_kb_3','start_kb_4'))

    else:
        await msg.answer("🌐 Iltimos, tilni tanlang:\n\nTilni tanlash uchun pastdagi tugmalardan birini bosing.\n\n🌐 Пожалуйста, выберите язык:\n\nНажмите на одну из кнопок ниже, чтобы выбрать язык.\n\n🌐 Please select a language:\n\nClick one of the buttons below to choose a language.\n\n🇺🇿 O'zbekcha\n🇷🇺 Русский\n🇬🇧 English",reply_markup=lang_keyb)

@router.callback_query(F.data.startswith('lang'))
async def lang(data:CallbackQuery):
    action = data.data.split('_')
    lang = action[1]
    user_id = data.from_user.id
    user_lang_save(user_id,lang)
    
    txt = languages[users_lang[user_id]]['start']
    await data.message.delete()
    await data.message.answer( txt,reply_markup=start_kb(users_lang[user_id],'start_kb_1','start_kb_2','start_kb_3','start_kb_4'))

@router.callback_query(F.data=='return')
async def lang(data:CallbackQuery):
    user_id = data.from_user.id
    txt = languages[users_lang[user_id]]['start']
    await data.message.delete()
    await data.message.answer( txt,reply_markup=start_kb(users_lang[user_id],'start_kb_1','start_kb_2','start_kb_3','start_kb_4'))


@router.callback_query(F.data=='change_lang')
async def change_lang(data:CallbackQuery):
    await data.message.delete()
    await data.message.answer("🌐 Iltimos, tilni tanlang:\n\nTilni tanlash uchun pastdagi tugmalardan birini bosing.\n\n🌐 Пожалуйста, выберите язык:\n\nНажмите на одну из кнопок ниже, чтобы выбрать язык.\n\n🌐 Please select a language:\n\nClick one of the buttons below to choose a language.\n\n🇺🇿 O'zbekcha\n🇷🇺 Русский\n🇬🇧 English",reply_markup=lang_keyb)

@router.callback_query(F.data=='zaqaz')
async def zaqaz(cb:CallbackQuery,state:FSMContext):
    await cb.message.delete()
    await state.set_state(Zaqaz.loyiha)
    tg_id = cb.from_user.id
    txt = languages[users_lang[tg_id]]['zaqaz']
    
    kb = stop(users_lang[tg_id])
    
    await cb.message.answer(txt,reply_markup=kb)

@router.callback_query(F.data=='break')
async def stop_state(data:CallbackQuery):
    tg_id = data.from_user.id
    txt = languages[users_lang[tg_id]]['start_2']
    await data.message.delete()
    await data.message.answer(txt,reply_markup=start_kb(users_lang[tg_id],'start_kb_1','start_kb_2','start_kb_3','start_kb_4'))

@router.message(Zaqaz.loyiha)
async def zaqaz_loyiha(msg:Message,state:FSMContext):
    await state.update_data(loyiha=msg.text)
    await state.set_state(Zaqaz.full_name)
    tg_id = msg.from_user.id
    txt = languages[users_lang[tg_id]]['loyiha']
    # try:
    
    await msg.answer(txt)
    # except:
    #     await msg.answer(txt)

@router.message(Zaqaz.full_name)
async def zaqaz_full_name(msg:Message,state:FSMContext):
    await state.update_data(full_name=msg.text)
    await state.set_state(Zaqaz.phone_number)
    tg_id = msg.from_user.id
    txt = languages[users_lang[tg_id]]['full_name']
    await msg.answer(txt,reply_markup=phone_kb(users_lang[tg_id],'phone_kb'))

@router.message(Zaqaz.phone_number)
async def zaqaz_phone_number(msg:Message,state:FSMContext):
    try:
       
        contact = msg.contact
        phone_number = contact.phone_number
        if phone_number.startswith('+'):
            await state.update_data(phone_number=f'{phone_number}')
        else:
            await state.update_data(phone_number=f'+{phone_number}')
        data = await state.get_data()
        await state.set_state(Zaqaz.sure)
        tg_id = msg.from_user.id
        # txt = languages[users_lang[tg_id]]['phone_number']
        if users_lang[tg_id]=='uz':
            txt = f"📋 Loyiha: {data['loyiha']}\n\n👤 Ism va familiya: {data['full_name']}\n\n📞 Telefon raqam: {data['phone_number']}\n\n✅ Hammasi to'g'ri bo'lsa, \"Ha\" tugmasini bosing.\n\n❌ Agar xato bo'lsa, \"Yo'q\" tugmasini bosing va qaytadan ma'lumotlarni kiritishga harakat qiling."
        elif users_lang[tg_id]=='ru':
            txt = f"📋 Проект: {data['loyiha']}\n\n👤 Имя и фамилия: {data['full_name']}\n\n📞 Номер телефона: {data['phone_number']}\n\n✅ Если все верно, нажмите \"Да\".\n\n❌ Если ошибка, нажмите \"Нет\" и попробуйте снова ввести данные."
        else:
           txt = f"📋 Project: {data['loyiha']}\n\n👤 Name and surname: {data['full_name']}\n\n📞 Phone number: {data['phone_number']}\n\n✅ If everything is correct, press \"Yes\".\n\n❌ If there is an error, press \"No\" and try to re-enter the information." 
        await msg.reply(txt,reply_markup=are_you_sure(users_lang[tg_id],'are_you_sure_kb_1','are_you_sure_kb_2'))
    except:
        tg_id = msg.from_user.id
        txt = languages[users_lang[tg_id]]['phone_number_err']
        await msg.reply(txt)
        await state.set_state(Zaqaz.phone_number)
        txt = languages[users_lang[tg_id]]['phone_number_err_2']
        
        await msg.answer(txt,reply_markup=phone_kb(users_lang[tg_id],'phone_kb'))

@router.callback_query(F.data.startswith('sure_'))
async def zaqaz_sure(cb:CallbackQuery,state:FSMContext):
    action = cb.data.split('_')[1]
    if action=='yes':
        
        data = await state.get_data()
        if cb.from_user.username:
            insert_client(data['loyiha'],data['full_name'],f'@{cb.from_user.username}',data['phone_number'],now)
        else:
            insert_client(data['loyiha'],data['full_name'],'username yoq',data['phone_number'],now)
        for i in ADMIN:
            text=(
                        f"👤 Client: @{cb.from_user.username}\n\n"
                        f"👤 Ism va familiya: {data['full_name']}\n\n"
                        f"📋 Loyiha: {data['loyiha']}\n\n"
                        f"📞 Telefon raqam: {data['phone_number']}"
                )
            await bot.send_message(i,text)
        tg_id = cb.from_user.id
        
        txt = languages[users_lang[tg_id]]['sure']
        txt1 = languages[users_lang[tg_id]]['sure_2']
        
        await cb.message.delete()
        await cb.message.answer(txt, reply_markup=(ReplyKeyboardRemove()))
        await cb.message.answer(txt1, reply_markup=start_kb(users_lang[tg_id],'start_kb_1','start_kb_2','start_kb_3','start_kb_4'))
        await state.clear()
    if action=='no':
        tg_id = cb.from_user.id
        txt = languages[users_lang[tg_id]]['sure_no']
        await cb.message.delete()
        
        await cb.message.answer(txt,reply_markup=qayta_kb(users_lang[tg_id],'qayta_kb_1','qayta_kb_2'))
        

@router.callback_query(F.data.startswith('qayta'))
async def qayta(data:CallbackQuery,state:FSMContext):
    action = data.data.split('_')
    if action[1]=='rest':
        await state.set_state(Zaqaz.loyiha)
        tg_id = data.from_user.id
        txt = languages[users_lang[tg_id]]['zaqaz']
        await data.message.answer(txt)
    elif action[1]=='break':
        await state.clear()
        tg_id = data.from_user.id
        txt = languages[users_lang[tg_id]]['break']
        txt1 = languages[users_lang[tg_id]]['start_2']
        await data.message.answer(txt)
        await data.message.answer(txt1, reply_markup=start_kb(users_lang[tg_id],'start_kb_1','start_kb_2','start_kb_3','start_kb_4'))
        await data.message.delete()
        
        
@router.callback_query(F.data=='works')
async def works(data:CallbackQuery):
    ...
    

@router.callback_query(F.data=='sahifa')
async def sahifa(data:CallbackQuery):
    await data.message.delete()
    user_id = data.from_user.id
    txt = f"🌐 Instagram: <a href='{INSTA}'>Team of Infinity</a>\n\n📱 Telegram: <a href='{TG}'>Team of Infinity</a>\n\n🌍 Sayt: <a href='{SAYT}'>Team of Infinity</a>"
    await data.message.answer(txt,reply_markup=last(users_lang[user_id],'last_kb_1','last_kb_2'))
    
    
    
# @router.message(Command('get_chat_id'))
# async def get_chat_id(message: Message):
#     # Chat ID ni olamiz
#     chat_id = message.chat.id
#     # Chat ID ni foydalanuvchiga yuboramiz
#     await message.answer(f"Chat ID: {chat_id}")