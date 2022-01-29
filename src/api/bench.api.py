import threading
import httpx
import asyncio

from faker import Faker
from random import choice


class User:
    url: str = "http://127.0.0.1:4352/"
    name: str = ""

    # async def __init__(self, requests: int):
    #     await asyncio.create_task(
    #         self.get_request()
    #     )
    def __init__(self, name: str):
        self.name = name

    async def get_request(self, requests: int):
        endpoints = ["monsters"]

        for _ in range(0, requests):
            async with httpx.AsyncClient() as client:
                r = await client.get(f"{self.url}{choice(endpoints)}?limit=5")
                # print("-------------------------------------------------")
                # print(
                #     f"[STATUS] -> {self.name} sending requests [{r.status_code}]")
                # print("-------------------------------------------------\n")


async def benchmark(users: int, requests: int):
    fake = Faker()

    users = [User(fake.name()) for _ in range(0, users)]

    await asyncio.gather(
        *[user.get_request(requests) for user in users]
    )


if __name__ == "__main__":
    asyncio.run(benchmark(10, 1000))
