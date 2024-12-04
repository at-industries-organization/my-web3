# MyWeb3
MyWeb3 - это утилитарная библиотека для работы с EVM блокчейнами в Python.

## Общая информация
### Возможности
1. Асинхронное взаимодействие с блокчейном.
2. Подключение прокси к блокчейну.
3. Ожидание снижения цены газа в сети Ethereum.
4. Создание транзакций типа Legacy и EIP-1559.

### Методы
1.  `is_connected` - проверка подключения к блокчейну.
2. `get_balance` - получение баланса нативной монеты.
3. `send_transaction` - отправка транзакции на блокчейн.
4. `verify_transaction` - проверка транзакции.
5. `transfer_amount` - перевод нативной монеты (абсолютное значение).
6. `transfer_percent` - перевод нативной монеты (относительное значение).
7. `ERC20_get_balance` - получение баланса ERC20 токена.
8. `ERC20_get_allowance` - получение allowance ERC20 токена.
9. `ERC20_get_decimals` - получение decimals ERC20 токена.
10. `ERC20_get_decimals_smart` - получение decimals ERC20 токена (быстрое).
11. `ERC20_get_symbol` - получение symbol ERC20 токена.
12. `ERC20_get_symbol_smart` - получение symbol ERC20 токена (быстрое).
13. `ERC20_approve` - создание approve ERC20 токена.
14. `ERC20_approve_smart` - создание approve ERC20 токена (с проверками).
15. `ERC20_transfer_amount` - перевод ERC20 токенов (абсолютное значение).
16. `ERC20_transfer_percent` - перевод ERC20 токенов (относительное значение).

### Особенности
1. Методы библиотеки разделены на 3 основных типа:
- Методы работы с нативной монетой - это методы, которые работают только с нативной монетой блокчейна. Данные методы располагаются в начале класса.
- Метода работы с ERC20 токенами - это методы, которые работают с токенами стандарта ERC20. Данные методы имеют названия начиная на `ERC20_`.
- Утилитарные методы - это методы, которые выполняют утилитарные функции. Данные методы располагаются в самом конце класса.
2. Почти все методы класса возвращают кортежи с целым числом в качестве первого элемента, где:
- `0`: статус успеха (успешное завершение метода; второй элемент кортежа содержит результат)
- `-1`: статус ошибки (неуспешное завершение метода; второй элемент кортежа содержит ошибку)

## Примеры
### Импорт библиотек
Перед началом импортируем библиотеку `asyncio` для запуска асинхронных функций, класс `MyWeb3` и сеть `BASE`, с которой мы будем работать. Список всех сетей можно найти в файле: `my_web3/models/network.py`.
```python
import asyncio
from my_web3 import MyWeb3, BASE
```

### Создание экземпляра класса `MyWeb3`
Создаем экземпляр класса `MyWeb3` с обязательным параметром `network` и опциональными параметрами `private_key` и `async_provider`. При отсутствии `private_key` методы, требующие подписи транзакций, будут возвращать ошибку. Подробнее о параметрах — в комментариях конструктора класса `MyWeb3`. 
```python
my_web3 = MyWeb3(
    network=BASE,
    private_key='1234567890123456789012345678901234567890123456789012345678901234',
    async_provider=True,
)
```

### Пример использования функции `is_connected`
Метод `is_connected` проверяет статус подключения к RPC блокчейна и возвращает кортеж, содержащий код статуса и результат проверки подключения.
```python
async def example_00():
    status, result = await my_web3.is_connected()
    if status == 0:
        print(f'00 | Connection: {result}')
    else:
        print(f'00 | Error while checking connection: {result}')

asyncio.run(example_00())
```

### Пример использования функции `get_balance`
Метод `get_balance` возвращает баланс кошелька (в нативной монете сети). Если в функцию передан `address_wallet`, метод вернет баланс этого адреса. Если аргумент не указан, будет возвращен баланс кошелька экземпляра класса `MyWeb3`.
```python
async def example_01():
    status, result = await my_web3.get_balance(
        address_wallet='0x2e988A386a799F506693793c6A5AF6B54dfAaBfB',
    )
    if status == 0:
        print(f'01 | Balance: {result}')
    else:
        print(f'01 | Error while getting balance: {result}')

asyncio.run(example_01())
```

### Пример использования функции `transfer_percent`
Метод `transfer_percent` переводит указанный процент баланса на адрес `address_recipient`. Например, в нашем примере `10%` баланса будут отправлены на адрес `0xB293cFf00bA3f110C839fBDB59186BD944B144D5`.
```python
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
```

### Пример использования функции `ERC20_get_balance`
Метод `ERC20_get_balance` получает баланс ERC20 токенов на кошельке. В нашем примере мы получаем баланс токена `USDC` на кошельке `0x2e988A386a799F506693793c6A5AF6B54dfAaBfB`.
```python
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
```

### Пример использования функции `ERC20_get_decimals`
Метод `ERC20_get_decimals` получает `decimals` введенного ERC20 токена. В нашем случае мы получаем `decimals` токена `USDC` в сети `BASE`.
```python
async def example_04():
    status, result = await my_web3.ERC20_get_decimals(
        address_token='0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913',
    )
    if status == 0:
        print(f'04 | Decimals: {result}')
    else:
        print(f'04 | Error while getting decimals: {result}')

asyncio.run(example_04())
```

### Пример использования функции `ERC20_approve`
Метод `ERC20_approve` делает `approve` ERC20 токенов. В нашем примере, мы делаем `approve` одного токена `USDC`, разрешая адресу `0x2626664c2603336E57B271c5C0b26F421741e481` списывать наши токены.
```python
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
```
