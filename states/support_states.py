from aiogram.fsm.state import StatesGroup, State

class StatesSupport(StatesGroup):
    question = State()
    response = State()
