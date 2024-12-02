# MyWeb3
*MyWeb3 - это утилитарная библиотека для работы с EVM сетями в Python.*

## Пример кода
### Импорт библиотек
Перед началом импортируем библиотеку `asyncio` для запуска асинхронных функций, класс `MyWeb3` и сеть `BASE`, с которой мы будем работать.
```python
import asyncio
from my_web3 import MyWeb3, BASE
```

### Пример использования функции `is_connected`
Метод `is_connected` проверяет статус подключения к Ethereum клиенту и возвращает кортеж, содержащий код статуса и результат проверки подключения.
```python
async def foo():
    w3 = MyWeb3(network=BASE)
    status, result = await w3.is_connected()
    if status == 0:
        print(f'Connection: {result}')
    else:
        print(f'Error while checking connection: {result}')

asyncio.run(foo())
```
