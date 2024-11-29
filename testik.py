from my_web3 import MyWeb3, NETWORKS_DICT
import asyncio

w3 = MyWeb3(network=NETWORKS_DICT['Base'])


async def foo1():
    status, result = await w3.is_connected()
    print(result)


async def foo2():
    status, result = await w3.get_balance('0xB3A1D905C52b8002F877b335169904554F9b5e5c')
    print(result)


@property
async def foo3():
    result = w3._get_contract_ERC20('0xB3A1D905C52b8002F877b335169904554F9b5e5c')
    print(result)


async def foo4():
    status, result = await w3._get_eth_gas_price_gwei()
    print(result)


async def foo5():
    status, result = await w3.ERC20_create_token('0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913')
    print(result.name)

asyncio.run(foo5())

