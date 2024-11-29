# MyWeb3
*вводная инфа про библиотеку*
## Пример кода
### Импорт библиотек
Перед началом импортируем класс `MyWeb3`, словарь `NETWORKS_DICT` с объектами класса `Network` и библиотеку `asyncio` для запуска асинхронных функций.
```python
from my_web3 import MyWeb3, NETWORKS_DICT
import asyncio
```
### Пример использования функции `is_connected`
Метод `is_connected` проверяет статус подключения к Ethereum клиенту и возвращает кортеж, содержащий код статуса и результат проверки подключения.




```python
async def foo():
    # Creates an object of MyWeb3
    w3 = MyWeb3(network=NETWORKS_DICT['Base'])

    # Checks the connection status of the Ethereum client
    status, result = await w3.is_connected()

    if status == 0:
        print(f'Connection: {result}')
    else:
        print(f'Error while checking connection: {result}')

# run function
asyncio.run(foo())
```
