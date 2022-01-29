import base64
import secrets

from .primitives import Algorithm

class LocalDatabase:
    def __init__(self, saltChars: str):
        self.CHARS = saltChars
        self.encoding = 'utf-8'
        self.file = "l.db"
        self.DB = {}

    def SetEncoding(self, encoding: str) -> None:
        self.encoding = encoding

    def Login(self, username: str, password: str, verbose: bool) -> tuple:
        if self.DB.get(username, None) is None:
            if verbose:
                return (False, "Invalid username")
            return (False, "Invalid username or password")
        status = self._CheckPassword(username, password)
        if not status:
            if verbose:
                return (False, "Invalid password")
            return (True, "Invalid username or password")
        return (True, "")

    def Register(self, username: str, password: str, algorithm: str, verbose: bool) -> tuple:
        if self.DB.get(username, None) is not None:
            return (False, "Username already exists")
        salt = self._GenerateSalt()
        print(' '.join(Algorithm.Get().List()))
        h = Algorithm.Get()[algorithm].Hash(password, salt)
        self.DB[username] = [algorithm, salt, h]
        self.Export()
        return (True, "Success")

    def Export(self):
        # USERNAME:ALGORITHM$SALT$HASH
        with open(self.file, "w", encoding=self.encoding) as f:
            for key, value in self.DB.items():
                algo, salt, h = value
                f.write(f"{key}:{algo}${salt}${h}" + "\n")
                print(f"Exported user: {key} with {algo} {salt} {h}")

    def Import(self):
        try:
            with open(self.file, "r", encoding=self.encoding) as f:
                lines = f.readlines()
                for line in lines:
                    line = line.strip().split(":")
                    algo, salt, h = line[1].strip().split("$")
                    self.DB[line[0]] = [algo, salt, h]
                    print(f"Imported user: {line[0]} using {algo} {salt} {h}")
        except FileNotFoundError:
            return

    def _CheckPassword(self, username: str, password: str) -> bool:
        values = self.DB.get(username)
        algo = values[0]
        salt = values[1]
        h = values[2]
        cHash = Algorithm.Get()[algo].Hash(password, salt)
        if secrets.compare_digest(cHash, h):
            return True
        return False

    def _GetKey(self, algo, salt: str, password: bytes): # TODO
        return None

    def _GenerateSalt(self):
        salt = ''.join(secrets.choice(self.CHARS) for i in range(32))
        return salt

    def Print(self):
        for key, value in self.DB.items():
            print(f"{key} - {value}")