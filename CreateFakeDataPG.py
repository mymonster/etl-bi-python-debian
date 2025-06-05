from createFakeData import CreateFakeData
from dotenv import load_dotenv
import os
from pathlib import Path
import psycopg2

class CreateFakeDataPG(CreateFakeData):
    def __init__(self):
        env_path = Path(__file__).resolve().parents[2] / 'configs' / '.env'
        load_dotenv(dotenv_path = env_path)

        self.db_config = {
            "host": os.getenv("PG_DB_HOST"),
            "port": os.getenv("PG_DB_PORT"),
            "dbname": os.getenv("PG_DB_NAME"),
            "user": os.getenv("PG_DB_USER"),
            "password": os.getenv("PG_DB_PASS")
        }

        self.validate_config()
        print("[+] Config is loaded correctly")
        
        self._conn = None
        self._cursor = None
 
    def validate_config(self):
        missing = [k for k, v in self.db_config.items() if not v]
        if missing:
            errorMessage = "[-] Error: missed connection value"
            for key in missing:
                print(f" - {key}")
            raise ValueError(errorMessage)

    def openConnectonDB(self):
        try:
            self._conn = psycopg2.connect(
            dbname = self.db_config["dbname"],
            user = self.db_config["user"],
            password = self.db_config["password"],
            host = self.db_config["host"],
            port = self.db_config["port"]
            )

            return self._conn
        except psycopg2.OperationalError as e:
            raise ConnectionError(f"Connection to PostgreSQL failed: {e}")

        

    def closeConnectionDB(self): 
        if  self._conn:
            try:
                self._conn.close()
            except psycopg2.OperationalError as e:
                raise ConnectionError(f"Closing connection to PostgreSQL failed: {e}")
        else:
            raise RuntimeError("Connection was not established")
        
    def openCursorDB(self):
        if  self._conn:
            try:
                self._cursor = self._conn.cursor()
            except psycopg2.OperationalError as e:
                raise ConnectionError(f"Open cursor failed: {e}")
        else:
            raise RuntimeError("Connection was not established")

    def closeCursorDB(self):
        if  self._cursor:
            try:
                self._cursor.close()
            except psycopg2.OperationalError as e:
                raise ConnectionError(f"Close cursor failed: {e}")
        else:
            raise RuntimeError("Cursor was not created")
    
    @property
    def cursor(self):
        if not self._cursor:
            raise RuntimeError("Cursor is not initialized. Call openCursorDB() first.")
        return self._cursor
    
    def __enter__(self):
        try:
            self.openConnectonDB()
            self.openCursorDB()
        except Exception as e:
            raise RuntimeError("Failed to initialize DB connection") from e

    def __exit__(self):
        try:
            self.closeCursorDB()
            self.closeConnectionDB()
        except Exception as e:
            raise RuntimeError("Failed to initialize DB cursor") from e