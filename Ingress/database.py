from ._localdatabase import LocalDatabase

class UserDatabase:
    __instance = None

    @staticmethod
    def Get():
        if UserDatabase.__instance is None:
            UserDatabase()
        return UserDatabase.__instance

    def __init__(self):
        if UserDatabase.__instance is not None:
            raise Exception("LoginDB attempted re-init")
        else:
            UserDatabase.__instance = self
            self.CHARS = None
            self.Types = dict(
                local = LocalDatabase,
            )

    def SetSalt(self, saltChars: str) -> None:
        self.CHARS = saltChars

    def GetTypes(self) -> list:
        return [key for key in self.Types.keys()]

    def InitDB(self, dbType: str):
        db = dbType.lower()
        for key, value in self.Types.items():
            if db == key:
                if self.CHARS is None:
                    self.SetSalt()
                UserDatabase.__instance = value(self.CHARS)
                return UserDatabase.__instance
        raise Exception(f"Unknown database type specified: {db}")

