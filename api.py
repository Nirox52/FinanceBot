from datetime import date,datetime
from math import fabs
import httpx
from config import API_URL

async def register_user(telegram_id: int):
    async with httpx.AsyncClient() as client:
        return await client.post(f"{API_URL}/users/?telegram_id={telegram_id}")

async def get_all_operations(telegram_id: int,with_ids=False):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_URL}/operations/tg/{telegram_id}")
        print(response.json())
        message =''
        for operation in response.json():
            if operation['type']=="income":
                symb = '📈'
            else:
                symb = '📉'
            if with_ids:
                message+=f'{operation["operation_id"]}) {symb}{operation["amount"]} - {operation["description"]}\n\n'
            else:
                message+=f'{symb}{operation["amount"]} - {operation["description"]}\n\n'
        return message,response.json()

async def create_operation(data: dict):
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{API_URL}/operations/", json=data)
        return resp.status_code == 200

async def update_operation(operation_id:int,data:dict):
    async with httpx.AsyncClient() as client:
        resp = await client.put(f"{API_URL}/operations/{operation_id}", json=data)
        return resp.status_code == 200


async def delete_operation(telegram_id:int,operation_id:int):
    async with httpx.AsyncClient() as client:
        resp = await client.delete(f"{API_URL}/operations/{operation_id}" )
        return resp.status_code == 200

async def get_all_operations_by_date(telegram_id: int,start_date:str,end_date:str):
    async with httpx.AsyncClient() as client:
        if '-' in start_date:
            start_date_obj = datetime.strptime(start_date, "%d-%m-%Y")
            start_date_str = start_date_obj.strftime("%Y-%m-%d")
        elif '.' in start_date:
            start_date_obj = datetime.strptime(start_date, "%d.%m.%Y")
            start_date_str = start_date_obj.strftime("%Y-%m-%d")
        else:
            print('error')

        if '-' in end_date:
            end_date_obj = datetime.strptime(end_date, "%d-%m-%Y")
            end_date_str = end_date_obj.strftime("%Y-%m-%d")
        elif '.' in end_date:
            end_date_obj = datetime.strptime(end_date, "%d.%m.%Y")
            end_date_str = end_date_obj.strftime("%Y-%m-%d")
        else:
            print('error')

        response = await client.get(f"{API_URL}/operations/operations_date/{telegram_id}?start={start_date_str}&end={end_date_str}")
        message = ''
        print(response.json())
        for operation in response.json():
            if operation['type']=="income":
                symb = '📈'
            else:
                symb = '📉'
            message+=f'{symb}{operation["amount"]} - {operation["description"]}\n\n'
        return message,response.json()

async def get_operation_by_id(operation_id:int, telegram_id:int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_URL}/operations/id/{operation_id}")
        return response.json()[0]
