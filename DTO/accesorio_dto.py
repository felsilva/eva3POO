class AccesorioDTO:
    def __init__(self, id_accesorio=None, nombre=None,          precio_dolar=None, especie=None, 
                 descripcion=None, stock=None, peso=None, edad_recomendada=None, tipo_id=None):
        self.id_accesorio = id_accesorio
        self.nombre = nombre
        self.precio_dolar = precio_dolar
        self.especie = especie
        self.descripcion = descripcion
        self.stock = stock
        self.peso = peso
        self.edad_recomendada = edad_recomendada
        self.tipo_id = tipo_id

    def __str__(self):
        return f"Accesorio: {self.nombre} - ${self.precio_dolar} USD - Stock: {self.stock}" 