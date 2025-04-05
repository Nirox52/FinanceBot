from openpyxl import Workbook
from aiogram.types import FSInputFile
from aiogram import types
import datetime

async def save_to_excel_and_send(data: list, message: types.Message):
    wb = Workbook()
    ws = wb.active
    ws.title = "Фінансовий звіт"
    
    headers = ["Тип операціїї", "Сумма", "Сумма (USD)", "Опис"]
    ws.append(headers)
    
    print(data)
    for record in data:
        row = [
            "Витрата" if record['type'] == 'expence' else "Прибуток",
            record['amount'],
            record['usd_amount'],
            record['description']
        ]
        ws.append(row)
    
    for column in ws.columns:
        max_length = 0
        column_letter = column[0].column_letter
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = (max_length + 2) * 1.2
        ws.column_dimensions[column_letter].width = adjusted_width
    
    filename = f"financial_report_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')}.xlsx"
    wb.save(filename)
    
    document = FSInputFile(filename)
    await message.answer_document(document, caption="Ваш фінансовий звіт")
    
    import os
    os.remove(filename)
