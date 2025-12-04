class Barco:
    def __init__(self, tipo: str):
        self.__tipo = tipo.lower()
        self.__longitud = self.longitud(tipo)
        self.__vida = self.__longitud
        self.__coords = []
        # self.__coords = [[] for _ in range(self.longitud(tipo))]


    @staticmethod
    def longitud(tipo: str):
        if tipo.lower() == 'fragata':
            return 1
        elif tipo.lower() == 'destructor':
            return 2
        elif tipo.lower() == 'acorazado':
            return 3
        elif tipo.lower() == 'portaviones':
            return 4
        else:
            raise ValueError("Tipo de barco inválido")

    def get_vida(self):
        return self.__vida

    def recibir_golpe(self):
        self.__vida -= 1

    def get_longitud(self):
        return self.__longitud

    def is_hundido(self):
        return self.__vida <= 0

    def get_coords(self):
        return self.__coords

    def set_coords(self, coords):
        self.__coords = coords