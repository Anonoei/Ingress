from .database import UserDatabase

from .primitives import Salt, Algorithm

class Login:
    def __init__(self):
        self.DB = None

    def SetDatabase(self, dbType: str = "local", saltChars: str = Salt.ALPHANUMERIC) -> None:
        self.DB = UserDatabase() # LoginDB should never be initialized again
        self.DB.SetSalt(saltChars)
        self.DB = self.DB.InitDB(dbType)
        self.DB.Import()

    def Register(self, username: str, password: str, algo: str = "SHA512", verbose: bool = False) -> tuple:
        """Creates a new user in the database

        Args:
            username (str): the username to register
            password (str): the password to register
            algo (str, optional): the hashing algorithm to use internally. Defaults to SHA512.
            verbose (bool, optional): if enabled returns what failed during register. Defaults to False.

        Returns:
            If successful:
                tuple: (True, key)
            If unsuccessful:
                tuple: (False, str)
        """
        self.__InitCheck()
        if not algo in Algorithm.Get().List():
            raise Exception("Invalid hashing algorithm")
        return self.DB.Register(username, password, algo, verbose)

    def Login(self, username: str, password: str, verbose: bool = False) -> tuple:
        """Attempts to login to the database

        Args:
            username (str): the username to login with
            password (str): the password to login with
            verbose (bool, optional): if enabled returns what failed during login. Defaults to False.

        Returns:
            If successful:
                tuple: (True, key)
            IF unsuccessful:
                tuple: (False, str)
        """
        self.__InitCheck()
        return self.DB.Login(username, password, verbose)

    def _ShowDatabase(self):
        self.__InitCheck()
        self.DB.Print()

    def __InitCheck(self):
        if self.DB is None:
            raise Exception("User database has not been initialized")