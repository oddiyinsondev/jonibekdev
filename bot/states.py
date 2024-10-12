from aiogram.fsm.state import State,StatesGroup

class Zaqaz(StatesGroup):
    loyiha = State()
    full_name = State()
    phone_number = State()
    sure = State()
    
class AdminState(StatesGroup):
    are_you_sure = State()
    ask_ad_content = State()
    
class Lang(StatesGroup):
    lang = State()
    
class Form(StatesGroup):
    sure = State()
