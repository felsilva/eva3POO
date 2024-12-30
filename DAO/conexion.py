import pymysql

class Conexion:
    _instance = None
    _connection = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Conexion, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._connection:
            self._connection = pymysql.connect(
                host='127.0.0.1',
                user='root',
                password='Inacap@2024.',
                database='santa_clara_mantenedor_db',
                cursorclass=pymysql.cursors.DictCursor
            )

    def get_connection(self):
        if not self._connection or not self._connection.open:
            self.__init__()
        return self._connection

    def close_connection(self):
        if self._connection and self._connection.open:
            self._connection.close() 