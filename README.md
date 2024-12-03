# MyWeb3
MyWeb3 - это утилитарная библиотека для работы с EVM блокчейнами в Python.

## Особенность библиотеки
Почти все методы класса (кроме утилитарных функций) возвращают кортежи с целым числом в качестве первого элемента, где:
- `0`: статус успеха (указывает на успешное завершение; второй элемент кортежа содержит результат)
- `-1`: статус ошибки (указывает неуспешное завершение; второй элемент кортежа содержит ошибку)

## Пример кода
### Импорт библиотек
Перед началом импортируем библиотеку `asyncio` для запуска асинхронных функций, класс `MyWeb3` и сеть `BASE`, с которой мы будем работать.
```python
import asyncio
from my_web3 import MyWeb3, BASE
```

### Создание объекта класса `MyWeb3`
Создаем объект нашего класса MyWeb3, у которого мы будем вызывать необходимые нам методы.
```python
my_web3 = MyWeb3(
    network=BASE,
    private_key='1234567890123456789012345678901234567890123456789012345678901234',
    async_provider=True,
)
```

### Пример использования функции `is_connected`
Метод `is_connected` проверяет статус подключения к Ethereum клиенту и возвращает кортеж, содержащий код статуса и результат проверки подключения.
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
        print(f'02 | Error while getting balance: {result}')

asyncio.run(example_01())
```

### Пример использования функции `transfer_percent`
Метод `transfer_percent` переводит указанный процент баланса на кошелек `address_recipient`. Например, в нашем примере `10%` баланса кошелька экземпляра класса `MyWeb3` будут отправлены на адрес `0xB293cFf00bA3f110C839fBDB59186BD944B144D5`.
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
