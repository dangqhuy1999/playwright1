import asyncio
import time

async def ham1(i):
    await asyncio.sleep(1)
    print(f'hettoo {i}')

def get_tasks():
    tasks = []
    for i in range(100000):
        tasks.append(ham1(i))
    return tasks

async def main():
    start = time.time()

    #processing async
    tasks = get_tasks()
    await asyncio.gather(*tasks) 

    stop = time.time()
    times = stop - start

    print(times)

asyncio.run(main())
