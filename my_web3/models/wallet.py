class Wallet:
    def __init__(self, seed_phrase: str, private_key: str, address: str):
        self.seed_phrase = seed_phrase
        self.private_key = private_key
        self.address = address
