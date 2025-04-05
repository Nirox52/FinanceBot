from aiogram import types, Router, F
from keyboard import main_menu, operation_type_kb
from api import delete_operation, register_user, get_all_operations, create_operation, get_all_operations_by_date
from aiogram.fsm.context import FSMContext
from fsm import AddOperation, DateFiltering, DeleteOperation
from exel_module import save_to_excel_and_send

router = Router()

async def start_handler(message: types.Message):
    await register_user(message.from_user.id)
    await message.answer("Ласкаво просимо! Оберіть дію:", reply_markup=main_menu)

async def show_all_operations(message: types.Message):
    operations, js_ob = await get_all_operations(message.from_user.id)
    if not operations:
        await message.answer("У вас поки що немає операцій.")
        return

    await message.answer(f"Ваші операції:\n\n{operations}")

@router.message(F.text == "📅 Фільтр по датам")
async def date_handler(message: types.Message, state: FSMContext):
    await message.answer("Напишіть початкову дату")
    await state.set_state(DateFiltering.choosing_first_date)

@router.message(DateFiltering.choosing_first_date)
async def ask_first_date(message: types.Message, state: FSMContext):
    try:
        first_date = message.text
    except ValueError:
        await message.answer("Введіть коректну дату.")
        return

    await state.update_data(first_date=first_date)
    await message.answer("Введіть кінцеву дату")
    await state.set_state(DateFiltering.choosing_second_date)

@router.message(DateFiltering.choosing_second_date)
async def ask_second_date(message: types.Message, state: FSMContext):
    try:
        second_date = message.text
    except ValueError:
        await message.answer("Введіть коректну дату.")
        return

    await state.update_data(second_date=second_date)

    data = await state.get_data()
    success, js_ob = await get_all_operations_by_date(message.from_user.id, data['first_date'], data['second_date'])
    await save_to_excel_and_send(js_ob, message)

    if success:
        await message.answer(success, reply_markup=main_menu)
    else:
        await message.answer("❌ Помилка операції.", reply_markup=main_menu)

    await state.clear()

@router.message(F.text == "➕ Додати операцію")
async def ask_type(message: types.Message, state: FSMContext):
    await message.answer("Оберіть тип операції:", reply_markup=operation_type_kb)
    await state.set_state(AddOperation.choosing_type)

@router.message(AddOperation.choosing_type, F.text.in_(["📈 Прибуток", "📉 Витрата"]))
async def ask_amount(message: types.Message, state: FSMContext):
    type_map = {"📈 Прибуток": "income", "📉 Витрата": "expence"}
    await state.update_data(type=type_map[message.text])
    await message.answer("Введіть суму операції:")
    await state.set_state(AddOperation.entering_amount)

@router.message(AddOperation.entering_amount)
async def ask_description(message: types.Message, state: FSMContext):
    try:
        amount = float(message.text)
    except ValueError:
        await message.answer("Введіть коректне число.")
        return

    await state.update_data(amount=amount)
    await message.answer("Введіть опис операції:")
    await state.set_state(AddOperation.entering_description)

@router.message(AddOperation.entering_description)
async def finish_add(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    data = await state.get_data()

    operation_data = {
        "telegram_id": message.from_user.id,
        "type": data["type"],
        "amount": data["amount"],
        "description": data["description"],
    }
    print(operation_data)

    success = await create_operation(operation_data)

    if success:
        await message.answer("✅ Операція успішно додана!", reply_markup=main_menu)
    else:
        await message.answer("❌ Помилка при додаванні операції.", reply_markup=main_menu)

    await state.clear()

@router.message(F.text == "Видалити операцію")
async def delete_handler(message: types.Message, state: FSMContext):
    operations, js_ob = await get_all_operations(message.from_user.id, True)
    if not operations:
        await message.answer("У вас немає операцій")
        return

    await message.answer(f"Ваші операції:\n\n{operations}")
    await state.set_state(DeleteOperation.geting_id)

@router.message(DeleteOperation.geting_id)
async def ask_id_to_del(message: types.Message, state: FSMContext):
    try:
        id_to_del = int(message.text)
        await state.update_data(id_to_del=id_to_del)
        res = await delete_operation(message.from_user.id, id_to_del)
        if res:
            await message.answer("✅ Операція успішно видалена!", reply_markup=main_menu)
        else:
            await message.answer("❌ Помилка при видаленні операції.", reply_markup=main_menu)
    except ValueError:
        await message.answer("Будь ласка, введіть числовий ID операції.")
    
    await state.clear()
