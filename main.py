import asyncio
import random
from enum import Enum


class ForkSides(Enum):
    LEFT = "left"
    RIGHT = "right"


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
            left_fork_picked = await self.try_pick_up_fork(self.left_fork, ForkSides.LEFT)
            if left_fork_picked:
                right_fork_picked = await self.try_pick_up_fork(self.right_fork, ForkSides.RIGHT)
                if right_fork_picked:
                    break
                await self.put_down_fork_one_closed(self.left_fork, ForkSides.LEFT)
            return

        print(f"{self.name} starts eating.")
        await asyncio.sleep(random.uniform(1, 3))

        await self.put_down_fork(self.right_fork, ForkSides.RIGHT)
        await self.put_down_fork(self.left_fork, ForkSides.LEFT)

    async def try_pick_up_fork(self, fork, side):
        if not fork.lock.locked():
            await fork.lock.acquire()
            print(f"{self.name} picked up {side.value} fork.")
            return True
        return False

    async def put_down_fork(self, fork, side):
        fork.lock.release()
        print(f"{self.name} put down {side.value} fork.")

    async def put_down_fork_one_closed(self, fork, side):
        fork.lock.release()
        if side == ForkSides.LEFT:
            print(f"{self.name} put down {side.value} fork due to the reason the {ForkSides.RIGHT.value} fork"
                  f" was taken by another philosopher.")
        else:
            print(f"{self.name} put down {side.value} fork due to the reason the {ForkSides.LEFT.value} fork"
                  f" was taken by another philosopher.")


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
