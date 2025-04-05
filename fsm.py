from aiogram.fsm.state import State, StatesGroup

class AddOperation(StatesGroup):
    choosing_type = State()
    entering_amount = State()
    entering_description = State()

class DateFiltering(StatesGroup):
    choosing_first_date = State()
    choosing_second_date = State()

class DeleteOperation(StatesGroup):
    geting_id = State()

class EditOperation(StatesGroup):
    geting_id = State()
    waiting_for_operation_id = State()
    choosing_field = State()
    entering_new_value = State()
    confirmation = State()

