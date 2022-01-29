import hashlib
from enum import Enum

class Salt:
    WHITESPACE = ' \t\n\r\v\f'
    ALPHA_LOWER = 'abcdefghijklmnopqrstuvwxyz'
    ALPHA_UPPER = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    ALPHA = ALPHA_LOWER + ALPHA_UPPER
    DIGITS = '0123456789'
    HEXADECIMAL = DIGITS + 'abcdef' + 'ABCDEF'
    OTCAL = '01234567'
    SYMBOLS = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
    ALPHANUMERIC = ALPHA + DIGITS
    PRINTABLE = ALPHANUMERIC + SYMBOLS + WHITESPACE

class SHA256:
    def Hash(self, password: str, salt: str = "") -> str:
        return hashlib.sha3_256( (salt + password).encode("utf-8") ).hexdigest()
class SHA384:
    def Hash(self, password: str, salt: str = "") -> str:
        return hashlib.sha3_384( (salt + password).encode("utf-8") ).hexdigest()
class SHA512():
    def Hash(self, password: str, salt: str = "") -> str:
        return hashlib.sha3_512( (salt + password).encode("utf-8") ).hexdigest()


class Algorithm:
    __instance = None

    @staticmethod
    def Get():
        if Algorithm.__instance is None:
            Algorithm()
        return Algorithm.__instance

    def __init__(self):
        if Algorithm.__instance is not None:
            raise Exception("LoginDB attempted re-init")
        else:
            Algorithm.__instance = self
            self.data = dict(
                SHA256 = SHA256(),
                SHA384 = SHA384(),
                SHA512 = SHA512()
            )

    def __getitem__(self, key: str):
        return self.data[key] # Intentionally throws errors for invalid keys

    def List(self) -> list[str]:
        return [key for key in self.data.keys()]