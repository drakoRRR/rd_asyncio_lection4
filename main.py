import asyncio
import random


class Fork:
    def __init__(self):
        self.lock = asyncio.Lock()


class Philosopher:
    def __init__(self, name, left_fork, right_fork):
        self.name = name
        self.left_fork = left_fork
        self.right_fork = right_fork

    async def dine(self):
        while True:
            await asyncio.sleep(random.uniform(0, 2))
            await self.think()
            await self.eat()

    async def think(self):
        print(f"{self.name} is thinking.")
        await asyncio.sleep(random.uniform(1, 3))

    async def eat(self):
        print(f"{self.name} wants to eat.")
        while True:
            left_fork_picked = await self.try_pick_up_fork(self.left_fork, "left")
            if left_fork_picked:
                right_fork_picked = await self.try_pick_up_fork(self.right_fork, "right")
                if right_fork_picked:
                    break
                await self.put_down_fork(self.left_fork, "left")
            await asyncio.sleep(random.uniform(0.1, 0.5))

        print(f"{self.name} starts eating.")
        await asyncio.sleep(random.uniform(1, 3))

        await self.put_down_fork(self.right_fork, "right")
        await self.put_down_fork(self.left_fork, "left")

    async def try_pick_up_fork(self, fork, side):
        if await fork.lock.acquire():
            print(f"{self.name} picked up {side} fork.")
            return True
        return False

    async def put_down_fork(self, fork, side):
        fork.lock.release()
        print(f"{self.name} put down {side} fork.")


async def main():
    forks = [Fork() for _ in range(5)]
    philosophers = [
        Philosopher(f"Philosopher {i + 1}", forks[i], forks[(i + 1) % 5])
        for i in range(5)
    ]

    await asyncio.gather(*(philosopher.dine() for philosopher in philosophers))


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Dining philosophers simulation stopped.")
