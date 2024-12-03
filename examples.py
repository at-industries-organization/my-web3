import asyncio
from my_web3 import MyWeb3, BASE


my_web3 = MyWeb3(
    network=BASE,
    private_key='1234567890123456789012345678901234567890123456789012345678901234',
    async_provider=True,
)


async def example_00():
    status, result = await my_web3.is_connected()
    if status == 0:
        print(f'00 | Connection: {result}')
    else:
        print(f'00 | Error while checking connection: {result}')

asyncio.run(example_00())


async def example_01():
    status, result = await my_web3.get_balance(
        address_wallet='0x2e988A386a799F506693793c6A5AF6B54dfAaBfB',
    )
    if status == 0:
        print(f'01 | Balance: {result}')
    else:
        print(f'02 | Error while getting balance: {result}')

asyncio.run(example_01())


async def example_02():
    status, result = await my_web3.transfer_percent(
        address_recipient='0xB293cFf00bA3f110C839fBDB59186BD944B144D5',
        percent=10,
    )
    if status == 0:
        print(f'02 | Balance: {result}')
    else:
        print(f'02 | Error while getting balance: {result}')

asyncio.run(example_02())
