#coding:utf-8

import hashlib


def md5_16(s='cuijunling'):
    m=hashlib.md5()
    m.update(s.encode("utf-8"))
    return m.hexdigest()[8:-8]
import asyncio


async def hello():
    print("hello the world")
    r = await asyncio.sleep(1)
    print("hello again")

def main():
    loop = asyncio.get_event_loop()
    """
    tasks = [
        asyncio.ensure_future(hello()),
    ]
    loop.run_until_complete(asyncio.wait(tasks))
    """
    print("begin")
    loop.run_until_complete(hello())
    print("end")
    loop.close()

    print("program is finished.")


if __name__ == "__main__":
    print(md5_16())