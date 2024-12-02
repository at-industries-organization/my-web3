# MyWeb3
MyWeb3 - это утилитарная библиотека для работы с EVM сетями в Python.

## Особенность библиотеки
Почти все методы класса (кроме утилитарных функций) возвращают кортежи с целочисленным статусом в качестве первого элемента, где:
- `0`: статус успеха (указывает, что метод успешно завершен; второй элемент кортежа содержит результат).
- `-1`: статус ошибки (указывает на сбой метода; второй элемент в кортеже содержит сообщение об ошибке)

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
async def foo():
    status, result = await my_web3.is_connected()
    if status == 0:
        print(f'Connection: {result}')
    else:
        print(f'Error while checking connection: {result}')

asyncio.run(foo())
```
