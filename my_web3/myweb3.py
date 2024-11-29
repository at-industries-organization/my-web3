from . import utils
from .utils import afh
from .constants import *
from .models.token import *

from typing import Union, Optional, Tuple
from web3.eth import Contract, AsyncEth
from web3.types import HexBytes, ChecksumAddress

import random
import asyncio
import inspect

from web3 import Web3
from web3.middleware import geth_poa_middleware


class MyWeb3:
    timeout = TIMEOUT
    tx_type = EIP_1559
    amount_tokens_all = AMOUNT_TOKENS_ALL
    insufficient_fund_errors_list = [
        ERROR_INSUFFICIENT_FUNDS,
        ERROR_GAS_REQUIRED_EXCEEDS_ALLOWANCE,
    ]
    abi_ERC20 = utils.read_json_from_file(FILENAME_ABI_ERC20)
    address_zero = ADDRESS_ZERO

    def __init__(
            self,
            network: Network,
            private_key: Optional[str] = None,
            async_provider: Optional[bool] = False,
            proxy: Optional[str] = None,
            gas_eth_max: Optional[int] = None,
            gas_increase_gas: Optional[float] = None,
            gas_increase_base: Optional[float] = None,
    ):
        """
        my_web3 is a convenient library for interacting with blockchain.

        Almost all class methods (except utility functions) return tuples, with an integer status as the first element:
        - `0`: Success status (indicates the method completed successfully; the second element in the tuple contains the result)
        - `-1`: Error status (indicates the method failed; the second element in the tuple contains an error message)

        For more details, refer to the Documentation: https://github.com/at-industries-organization/my-web3

        :param network: The network to connect to (e.g., Ethereum, BSC, Base)
        :param private_key: The secret key of your wallet, used for signing transactions.
        :param async_provider: If True, enables asynchronous operation for functions.
        :param proxy: Proxy server address, used to change the API endpoint.
        :param gas_eth_max: Maximum amount of ETH that can be spent on gas for transactions.
        :param gas_increase_gas: A multiplier to increase the estimated gas for transactions.
        :param gas_increase_base: A base value for gas increase calculations.
        """
        self.private_key = private_key
        self.network = network
        self.async_provider = async_provider
        self.proxy = proxy
        self.max_eth_gwei = gas_eth_max
        self.gas_increase_gas = gas_increase_gas
        self.gas_increase_base = gas_increase_base
        self.w3 = self._get_w3(network=self.network, proxy=self.proxy, async_provider=self.async_provider)
        if self.private_key is not None:
            self.address = Web3.to_checksum_address(self.w3.eth.account.from_key(private_key=private_key).address)
        else:
            self.address: str = self.address_zero

    async def is_connected(self, ) -> Tuple[int, Union[bool, Exception]]:
        """Checks the connection status of the Ethereum client."""
        log_process = f'{inspect.currentframe().f_code.co_name}'
        try:
            connection = await afh(self.w3.is_connected, self.async_provider)
            if connection:
                return 0, True
            else:
                return 0, False
        except Exception as e:
            return -1, Exception(f'{log_process} | {e}')

    async def get_balance(self, address_wallet: Optional[str] = None) -> Tuple[int, Union[int, Exception]]:
        """Retrieves the balance of a specified Ethereum wallet address."""
        log_process = f'{inspect.currentframe().f_code.co_name}'
        try:
            address_wallet = self._get_address_wallet(address_wallet=address_wallet)
            return 0, int(await afh(self.w3.eth.get_balance, self.async_provider, address_wallet))

        except Exception as e:
            return -1, Exception(f'{log_process} | {e}')

    async def send_transaction(
            self,
            address_to: str,
            address_from: Optional[str] = None,
            data=None, value=None, gas_price=None, gas=None,
    ) -> Tuple[int, Union[HexBytes, Exception]]:
        """Facilitates sending a transaction on the Ethereum blockchain"""
        log_process = f'{inspect.currentframe().f_code.co_name}'
        try:
            if (self.network.coin == ETH) and (self.max_eth_gwei is not None):
                while True:
                    status, result = await self._get_eth_gas_price_gwei(self.proxy)
                    if status == 0:
                        if result > self.max_eth_gwei:
                            await asyncio.sleep(random.randint(10, 20))
                        else:
                            break
                    else:
                        return -1, Exception(f'{log_process} | eth |{result}')
            nonce = await afh(self.w3.eth.get_transaction_count, self.async_provider, self.address)
            chain_id = self.w3.eth.chain_id

            tx = {
                'from': self._get_address_wallet(address_wallet=address_from),
                'nonce': nonce,
                'to': Web3.to_checksum_address(address_to),
                'chainId': chain_id,
            }
            if data:
                tx['data'] = data
            if value:
                tx['value'] = value
            if gas_price:
                tx['gasPrice'] = gas_price
            else:
                if (self.tx_type == LEGACY) or (self.network.tx_type == LEGACY):
                    tx['gasPrice'] = self.w3.eth.gas_price

                else:
                    maxPriorityFeePerGas, maxFeePerGas = await self._get_EIP_1559_gas_price_parameters(
                        self.gas_increase_base)
                    tx['maxPriorityFeePerGas'] = maxPriorityFeePerGas
                    tx['maxFeePerGas'] = maxFeePerGas
            try:
                if gas:
                    gas_estimated = gas
                else:
                    gas_estimated = self.w3.eth.estimate_gas(tx)

                    if self.gas_increase_gas:
                        gas_estimated *= self.gas_increase_gas
                tx['gas'] = int(gas_estimated)
            except Exception as e:
                return -1, Exception(f'{log_process} | gas | {e}')
            sign = await afh(self.w3.eth.account.sign_transaction, self.async_provider, tx, self.private_key)
            transaction_hash = await afh(self.w3.eth.send_raw_transaction, self.async_provider, sign.rawTransaction)

            return 0, transaction_hash
        except Exception as e:
            return -1, Exception(f'{log_process} | {e}')

    async def verify_transaction(self, transaction_hash: HexBytes) -> Tuple[int, Union[bool, Exception]]:
        """Checks the status of a blockchain transaction using its hash."""
        log_process = f'{inspect.currentframe().f_code.co_name}'
        try:
            data = await afh(self.w3.eth.wait_for_transaction_receipt, self.async_provider, transaction_hash=transaction_hash, timeout=self.timeout)

            if ('status' in data) and (data['status'] == 1):
                return 0, True
            else:
                return 0, False
        except Exception as e:
            return -1, Exception(f'{log_process} | {e}')

    async def transfer_amount(self, address_recipient: str, amount: int) -> Tuple[int, Union[HexBytes, Exception]]:
        """Transfers a specified amount of the caller's balance to a designated recipient address."""
        log_process = f'{inspect.currentframe().f_code.co_name}'
        try:
            status, result = await self.send_transaction(address_to=address_recipient, value=amount)
            if status == 0:
                return 0, result
            else:
                return -1, Exception(f'{log_process} | {result}')
        except Exception as e:
            return -1, Exception(f'{log_process} | {e}')

    async def transfer_percent(self, address_recipient: str, percent: float) -> Tuple[int, Union[HexBytes, Exception]]:
        """Transfers a specified percentage of the caller's balance to a designated recipient address."""
        log_process = f'{inspect.currentframe().f_code.co_name}'
        try:
            status, result = await self.get_balance()
            if status == 0:
                balance: int = result
                if percent < 100:
                    amount = int(balance * (percent / 100))
                    status, result = await self.transfer_amount(address_recipient=address_recipient, amount=amount)
                    if status == 0:
                        return 0, result
                    else:
                        return -1, Exception(f'{log_process} | {result}')
                elif percent == 100:
                    amount = balance
                    while True:
                        if amount > 0:
                            status, result = await self.transfer_amount(address_recipient=address_recipient,
                                                                        amount=amount)
                            if status == 0:
                                return 0, result
                            else:
                                if any(error in str(result) for error in self.insufficient_fund_errors_list):
                                    amount -= self.network.get_step_withdraw()
                                    await asyncio.sleep(1)
                                else:
                                    return -1, Exception(f'{log_process} | {result}')
                        else:
                            return -1, Exception(f'{log_process} | amount <= 0')
                else:
                    return -1, Exception(f'{log_process} | percent > 100')
            else:
                return -1, Exception(f'{log_process} | {result}')
        except Exception as e:
            return -1, Exception(f'{log_process} | {e}')

    async def ERC20_get_decimals(
            self,
            address_token: str,
    ) -> Tuple[int, Union[int, Exception]]:
        """Retrieves decimals of an ERC20 token from blockchain based on its address."""
        log_process = f'{inspect.currentframe().f_code.co_name}'
        try:
            token_contract = self._get_contract_ERC20(address_token)
            return 0, await afh(token_contract.functions.decimals().call, self.async_provider)
        except Exception as e:
            return -1, Exception(f'{log_process} | {e}')

    async def ERC20_get_decimals_smart(
            self,
            address_token: str,
    ) -> Tuple[int, Union[int, Exception]]:
        """Retrieves decimals of an ERC20 token from internal token dict and blockchain based on its address."""
        log_process = f'{inspect.currentframe().f_code.co_name}'
        for token in TOKENS_LIST:
            if address_token == token.addresses[self.network]:
                return 0, token.decimals
        status, result = await self.ERC20_get_decimals(address_token)
        if status == -1:
            return -1, Exception(f'{log_process} | {result}')
        else:
            return 0, result

    async def ERC20_get_symbol(self, address_token: str) -> Tuple[int, Union[str, Exception]]:
        """Retrieves the symbol of an ERC20 token from blockchain based on its address."""
        log_process = f'{inspect.currentframe().f_code.co_name}'
        try:
            token_contract = self._get_contract_ERC20(address_token)
            return 0, await afh(token_contract.functions.name().call, self.async_provider)

        except Exception as e:
            return -1, Exception(f'{log_process} | {e}')

    async def ERC20_get_symbol_smart(self, address_token: str) -> Tuple[int, Union[str, Exception]]:
        """Retrieves the symbol of an ERC20 token from internal token dict and blockchain based on its address."""
        log_process = f'{inspect.currentframe().f_code.co_name}'
        for token in TOKENS_LIST:
            if address_token == token.addresses[self.network]:
                return 0, token.name
        status, result = await self.ERC20_get_symbol(address_token=address_token)
        if status == -1:
            return -1, Exception(f'{log_process} | {result}')
        else:
            return 0, result

    async def ERC20_get_balance(
            self,
            address_token: str,
            address_wallet: Optional[str] = None,
    ) -> Tuple[int, Union[int, Exception]]:
        """Retrieves the balance of a specified ERC20 token for a given wallet address."""
        log_process = f'{inspect.currentframe().f_code.co_name}'
        try:
            contract = self._get_contract_ERC20(address_token)
            address_wallet = self._get_address_wallet(address_wallet)
            return 0, await afh(contract.functions.balanceOf(address_wallet).call, self.async_provider)

        except Exception as e:
            return -1, Exception(f'{log_process} | {e}')

    async def ERC20_get_allowance(
            self,
            address_token: str,
            address_spender: str,
            address_wallet: Optional[str] = None,
    ) -> Tuple[int, Union[int, Exception]]:
        """Retrieves the allowance amount that a specified spender is allowed to withdraw from a given wallet for a specific ERC20 token."""
        log_process = f'{inspect.currentframe().f_code.co_name}'
        try:
            contract = self._get_contract_ERC20(address_token=address_token)
            address_wallet = self._get_address_wallet(address_wallet=address_wallet)
            address_spender = Web3.to_checksum_address(address_spender)
            return 0, await afh(contract.functions.allowance(address_wallet, address_spender).call, self.async_provider)

        except Exception as e:
            return -1, Exception(f'{log_process} | {e}')

    async def ERC20_approve(
            self,
            amount: int,
            address_token: str,
            address_spender: str,
    ) -> Tuple[int, Union[HexBytes, Exception]]:
        """Approves a specified amount of an ERC20 token for a spender address."""
        log_process = f'{inspect.currentframe().f_code.co_name}'
        try:
            contract = self._get_contract_ERC20(address_token)
            data_transaction = afh(contract.encodeABI, self.async_provider,
                                   fn_name='approve', args=(Web3.to_checksum_address(address_spender), amount))

            status, result = afh(self.send_transaction, self.async_provider, address_to=address_token, data=data_transaction)

            if status == 0:
                return 0, result
            else:
                return -1, Exception(f'{log_process} | {result}')
        except Exception as e:
            return -1, Exception(f'{log_process} | {e}')

    async def ERC20_approve_smart(
            self,
            amount: int,
            address_token: str,
            address_spender: str,
    ) -> Tuple[int, Union[HexBytes, Exception]]:
        """Checks allowance and balance and approves a specified amount of an ERC20 token for a spender address."""
        log_process = f'{inspect.currentframe().f_code.co_name}'
        try:
            status, result = await self.ERC20_get_allowance(address_token=address_token,
                                                            address_spender=address_spender)
            if status == 0:
                allowance: int = result
                status, result = await self.ERC20_get_balance(address_token=address_token)
                if status == 0:
                    balance: int = result
                    if balance > 0:
                        if (amount > balance) and (amount != self.amount_tokens_all):
                            amount = balance
                        if allowance >= amount:
                            return 0, HexBytes(0)
                        status, result = await self.ERC20_approve(
                            address_token=address_token, address_spender=address_spender, amount=amount,
                        )
                        if status == 0:
                            return 0, result
                        else:
                            return -1, Exception(f'{log_process} | {result}')
                    else:
                        return -1, Exception(f'{log_process} | {result}')
                else:
                    return -1, Exception(f'{log_process} | {result}')
            else:
                return -1, Exception(f'{log_process} | {result}')
        except Exception as e:
            return -1, Exception(f'{log_process} | {e}')

    async def ERC20_transfer_amount(
            self,
            amount: int,
            address_token: str,
            address_recipient: str,
    ) -> Tuple[int, Union[HexBytes, Exception]]:
        """Transfers an amount of an ERC20 token balance from the caller's address to a specified recipient address."""
        log_process = f'{inspect.currentframe().f_code.co_name}'
        try:
            contract = self._get_contract_ERC20(address_token)
            data_transaction = await afh(
                contract.encodeABI,
                self.async_provider,
                fn_name='transfer',
                args=(
                    Web3.to_checksum_address(address_recipient),
                    amount,
                )
            )
            status, result = await self.send_transaction(
                address_to=address_token,
                data=data_transaction,
            )
            if status == 0:
                return 0, result
            else:
                return -1, Exception(f'{log_process} | {result}')
        except Exception as e:
            return -1, Exception(f'{log_process} | {e}')

    async def ERC20_transfer_percent(
            self,
            percent: float,
            address_token: str,
            address_recipient: str,
    ) -> Tuple[int, Union[HexBytes, Exception]]:
        """Transfers a percentage of an ERC20 token balance from the caller's address to a specified recipient address."""
        log_process = f'{inspect.currentframe().f_code.co_name}'
        try:
            status, result = await self.ERC20_get_balance(address_token=address_token)
            if status == 0:
                balance: int = result
                amount = int(balance * (percent / 100))
                status, result = await self.ERC20_transfer_amount(
                    address_token=address_token, address_recipient=address_recipient, amount=amount,
                )
                if status == 0:
                    return 0, result
                else:
                    return -1, Exception(f'{log_process} | {result}')
            else:
                return -1, Exception(f'{log_process} | {result}')
        except Exception as e:
            return -1, Exception(f'{log_process} | {e}')

    async def ERC20_create_token(self, address_token: str) -> Tuple[int, Union[Token, Exception]]:
        """Creates an object of the Token class based on the provided ERC20 token address."""
        log_process = inspect.currentframe().f_code.co_name
        try:
            address_token = Web3.to_checksum_address(address_token)
            contract = self._get_contract_ERC20(address_token=address_token)
            name = await afh(contract.functions.name().call, self.async_provider)
            decimals = await afh(contract.functions.decimals().call, self.async_provider)
            address_dict = {self.network: address_token}
            token = Token(name=name, decimals=decimals, addresses=address_dict)
            return 0, token
        except Exception as e:
            return -1, Exception(f'{log_process} | {e}')

    def _get_w3(self, network: Network, proxy: Optional[str] = None, async_provider: Optional[bool] = False,
                poa_middleware: Optional[bool] = None) -> Web3:
        if not async_provider:
            if proxy is not None:
                w3 = Web3(
                    provider=Web3.HTTPProvider(
                        endpoint_uri=network.rpc,
                        request_kwargs={
                            'proxies': {
                                'http': f'http://{proxy}',
                                'https': f'http://{proxy}'
                            }
                        },
                    ),
                )
            else:
                w3 = Web3(
                    provider=Web3.HTTPProvider(
                        endpoint_uri=network.rpc,
                    ),
                )
        else:
            w3 = Web3(
                provider=Web3.AsyncHTTPProvider(endpoint_uri=network.rpc),
                modules={"eth": (AsyncEth,)},
                middlewares=[]
            )
        if poa_middleware is not None:
            w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        return w3

    def _get_address_wallet(self, address_wallet: Optional[str] = None) -> ChecksumAddress:
        if address_wallet is not None:
            return Web3.to_checksum_address(address_wallet)
        else:
            return self.address

    def _get_contract_ERC20(self, address_token: str) -> Contract:
        return self.w3.eth.contract(address=Web3.to_checksum_address(address_token), abi=self.abi_ERC20)

    async def _get_eth_gas_price_gwei(self, proxy: Optional[str] = None) -> Tuple[int, Union[int, Exception]]:
        log_process = f'{inspect.currentframe().f_code.co_name}'
        try:
            w3 = self._get_w3(network=ETHEREUM, proxy=proxy)
            return 0, int(Web3.from_wei(int(w3.eth.gas_price), 'gwei'))  # всегда синхронная?
        except Exception as e:
            return -1, Exception(f'{log_process} | {e}')

    async def _get_EIP_1559_gas_price_parameters(self, gas_increase_base: Optional[float] = None) -> Tuple[int, int]:
        w3 = self._get_w3(network=self.network, proxy=self.proxy, poa_middleware=True,
                          async_provider=self.async_provider)
        base_fee_per_gas = (await afh(w3.eth.get_block, self.async_provider, 'latest'))['baseFeePerGas']
        max_priority_fee_per_gas = int(await afh(w3.eth.max_priority_fee, self.async_provider))
        if gas_increase_base is not None:
            max_fee_per_gas = max_priority_fee_per_gas + int(base_fee_per_gas * gas_increase_base)
        else:
            max_fee_per_gas = max_priority_fee_per_gas + int(base_fee_per_gas)
        return max_priority_fee_per_gas, max_fee_per_gas
