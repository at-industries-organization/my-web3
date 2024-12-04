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
        print(f'01 | Error while getting balance: {result}')

asyncio.run(example_01())


async def example_02():
    status, result = await my_web3.transfer_percent(
        address_recipient='0xB293cFf00bA3f110C839fBDB59186BD944B144D5',
        percent=10,
    )
    if status == 0:
        print(f'02 | Transaction hash: {result}')
    else:
        print(f'02 | Error while transferring coins: {result}')

asyncio.run(example_02())


async def example_03():
    status, result = await my_web3.ERC20_get_balance(
        address_token='0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913',
        address_wallet='0x2e988A386a799F506693793c6A5AF6B54dfAaBfB',
    )
    if status == 0:
        print(f'03 | Balance: {result}')
    else:
        print(f'03 | Error while getting balance: {result}')

asyncio.run(example_03())


async def example_04():
    status, result = await my_web3.ERC20_get_decimals(
        address_token='0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913',
    )
    if status == 0:
        print(f'04 | Decimals: {result}')
    else:
        print(f'04 | Error while getting decimals: {result}')

asyncio.run(example_04())


async def example_05():
    status, result = await my_web3.ERC20_approve(
        amount=1000000,
        address_token='0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913',
        address_spender='0x2626664c2603336E57B271c5C0b26F421741e481',
    )
    if status == 0:
        print(f'05 | Transaction hash: {result}')
    else:
        print(f'05 | Error while approving tokens: {result}')

asyncio.run(example_05())
