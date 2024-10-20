from aiogram.fsm.state import StatesGroup, State


class Register(StatesGroup):
    full_name = State()
    idora = State()
    contact = State()
    location = State()
    confirm = State()


class ChangeUserState(StatesGroup):
    type = State()
    confirm = State()


class GetOrder(StatesGroup):
    id = State()


class ConfirmBasket(StatesGroup):
    delivery = State()
    time = State()
    debt = State()
    confirm_time = State()


class ProductOrderState(StatesGroup):
    product_id = State()
    count = State()
    payment = State()
    confirm = State()


class ChangeTypeState(StatesGroup):
    permission = State()
    type = State()
