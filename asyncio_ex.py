import asyncio
from asyncio import sleep
import asyncpg


QUERY = """INSERT INTO some_test_table VALUES ($1, $2, $3)"""


async def make_request(db_pool):
    # await - пока не выполнится sleep(.1) функция не пойдет дальше
    await db_pool.fetch(QUERY, 1, "some string", 3)
    await sleep(.1)


async def main():
    chunk = 200
    tasks = []
    pended = 0

    # Сама открывает и закрывает коннекты
    # 'postgresql://127.0.0.1:5432/postgres'
    db_pool = await asyncpg.create_pool(
        user='postgres',
        host='127.0.0.1',
        port='5432',
        password='asdaf231299'
    )

    for x in range(10_000):
        # Назначаем задачи
        # task_1 = asyncio.create_task(make_request())
        # task_2 = asyncio.create_task(make_request())
        tasks.append(asyncio.create_task(make_request(db_pool)))
        pended += 1
        if len(tasks) == chunk or pended == 10_000:
            # Передаем к исполнению
            await asyncio.gather(*tasks)
            tasks = []
            print(pended)


# Назначаем цикл переменной loop
loop = asyncio.get_event_loop()
# Работать до того момента, пока не выполнится функция main()
loop.run_until_complete(main())
