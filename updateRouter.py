from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import types, Router, F
from keyboard import main_menu
from fsm import EditOperation
from keyboard import edit_keyboard, confirm_keyboard
from api import get_operation_by_id, update_operation, get_all_operations

up_router = Router()

@up_router.message(F.text == "✏️ Редагувати запис")
async def start_edit_operation(message: types.Message, state: FSMContext):
    operations, js_ob = await get_all_operations(message.from_user.id, True)
    if not operations:
        await message.answer("У вас поки що немає операцій.")
        return

    await message.answer(f"Ваші операції:\n\n{operations}")
    await state.set_state(EditOperation.geting_id)

@up_router.message(EditOperation.geting_id)
async def ask_id_to_change(message: types.Message, state: FSMContext):
    try:
        operation_id = int(message.text)
        operation = await get_operation_by_id(operation_id, message.from_user.id)
        if not operation:
            await message.answer("Операцію з таким ID не знайдено. Спробуйте ще раз.")
            return
            
        await state.update_data(operation_id=operation_id, current_operation=operation)
        await message.answer(
            f"Вибрана операція:\n"
            f"Тип: {operation['type']}\n"
            f"Сума: {operation['amount']}\n"
            f"Опис: {operation['description']}\n\n"
            f"Яке поле ви хочете змінити?",
            reply_markup=edit_keyboard
        )
        await state.set_state(EditOperation.choosing_field)
    except ValueError:
        await message.answer("ID операції має бути числом. Спробуйте ще раз.")

@up_router.message(EditOperation.choosing_field)
async def process_field_selection(message: types.Message, state: FSMContext):
    valid_fields = ['type', 'amount', 'description']
    if message.text not in valid_fields:
        await message.answer("Будь ласка, оберіть поле з запропонованих варіантів.")
        return
    
    await state.update_data(selected_field=message.text)
    
    if message.text == 'type':
        await message.answer(
            "Введіть новий тип операції (income/expence):",
            reply_markup=types.ReplyKeyboardRemove()
        )
    elif message.text == 'amount':
        await message.answer(
            "Введіть нову суму:",
            reply_markup=types.ReplyKeyboardRemove()
        )
    else:
        await message.answer(
            "Введіть новий опис:",
            reply_markup=types.ReplyKeyboardRemove()
        )
    
    await state.set_state(EditOperation.entering_new_value)

@up_router.message(EditOperation.entering_new_value)
async def process_new_value(message: types.Message, state: FSMContext):
    data = await state.get_data()
    selected_field = data['selected_field']
    new_value = message.text
    
    if selected_field == 'type' and new_value not in ['income', 'expence']:
        await message.answer("Тип операції має бути 'income' або 'expence'. Спробуйте ще раз.")
        return
    elif selected_field == 'amount':
        try:
            new_value = float(new_value)
            if new_value <= 0:
                await message.answer("Сума має бути додатнім числом. Спробуйте ще раз.")
                return
        except ValueError:
            await message.answer("Сума має бути числом. Спробуйте ще раз.")
            return
    
    await state.update_data(new_value=new_value)
    
    current_operation = data['current_operation']
    changes_message = (
        f"Поточні дані операції:\n"
        f"Тип: {current_operation['type']}\n"
        f"Сума: {current_operation['amount']}\n"
        f"Опис: {current_operation['description']}\n\n"
        f"Після змін:\n"
    )
    
    updated_operation = current_operation.copy()
    updated_operation[selected_field] = new_value
    
    changes_message += (
        f"Тип: {updated_operation['type']}\n"
        f"Сума: {updated_operation['amount']}\n"
        f"Опис: {updated_operation['description']}\n\n"
        f"Підтверджуєте зміни?"
    )
    
    await message.answer(changes_message, reply_markup=confirm_keyboard)
    await state.set_state(EditOperation.confirmation)

@up_router.message(EditOperation.confirmation)
async def process_confirmation(message: types.Message, state: FSMContext):
    if message.text.lower() != 'так':
        await message.answer("Зміни скасовано.", reply_markup=main_menu)
        await state.clear()
        return
    
    data = await state.get_data()
    operation_id = data['operation_id']
    selected_field = data['selected_field']
    new_value = data['new_value']
    
    obj = {
        "type": data["current_operation"]['type'],
        "amount": data["current_operation"]['amount'],
        "description": data["current_operation"]['description']
    }
    obj[selected_field] = new_value
    
    success = await update_operation(operation_id, obj)

    if success:
        await message.answer("✅ Операцію успішно оновлено!", reply_markup=main_menu)
    else:
        await message.answer("❌ Помилка при оновленні операції.", reply_markup=main_menu)
    
    await state.clear()
