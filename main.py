import platform
from datetime import datetime
import logging

import aiohttp
import asyncio

import sys
from datetime import datetime, timedelta


async def request(url: str):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, ssl=False) as resp:
                if resp.status == 200:
                    r = await resp.json()
                    return r
                logging.error(f"Error status: {resp.status} for {url}")
                return None
        except aiohttp.ClientConnectorError as err:
            logging.error(f"Connection error: {str(err)}")
            return None


async def get_exchange(data: str):
    result = await request(f'https://api.privatbank.ua/p24api/exchange_rates?json&date={data}')
    # print(result)
    if result:
        rates = result.get("exchangeRate")

        exc_EUR, = list(
            filter(lambda element: element["currency"] == 'EUR', rates))

        exc_USD, = list(
            filter(lambda element: element["currency"] == 'USD', rates))

        course = f"EUR: buy: {exc_EUR['purchaseRateNB']}, sale: {exc_EUR['saleRateNB']}. Date: {data} \nUSD: buy: {exc_USD['purchaseRateNB']}, sale: {exc_USD['saleRateNB']}. Date: {data}"
        return course
        # return f"EUR: buy: {exc_EUR['purchaseRateNB']}, sale: {exc_EUR['saleRateNB']}. Date: {datetime.now().date()}"

    return "Failed to retrieve data"


def date_exc(data: int):
    datas = datetime.now() - timedelta(days=data)
    return datas.strftime("%d.%m.%Y")


if __name__ == '__main__':

    try:
        datat = date_exc(int(sys.argv[1]))
    except:
        datat = (datetime.now() - timedelta(days=1)).strftime("%d.%m.%Y")
        print(
            f"Так як не вказано кількість днів, курс буде виведен на дату {datat}")

    result = asyncio.run(get_exchange(str(datat)))
    print(result)
