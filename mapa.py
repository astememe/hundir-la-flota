from barco import Barco

class Mapa:
    agua = "~"
    hit = "x"
    miss = "o"
    barco = "H"

    def __init__(self):
        self.__tamano = 6
        self.__mapa_oculto = self.rellenarMapa()
        self.__mapa_visible = self.rellenarMapa()
        self.__barcos = []

    def rellenarMapa(self):
        forma = [[] for _ in range(self.__tamano)]
        for fila in forma:
            for i in range(self.__tamano):
                fila.append(self.agua)
        return forma

    def get_mapa_visible(self):
        return self.__mapa_visible

    def get_mapa_oculto(self):
        return self.__mapa_oculto

    def get_barcos(self):
        return self.__barcos

    def posicionar_barco(self, barco: Barco, orientacion: str, coord_x: int, coord_y: int):
        coords = []
        if coord_x > self.__tamano or coord_x - 1 < 0 or coord_y > self.__tamano or coord_y - 1 < 0:
            raise ValueError("El barco no se puede posicionar fuera del mapa")
        elif orientacion == "V" and coord_y - 1 + barco.get_longitud() > self.__tamano or orientacion == "H" and coord_x - 1 + barco.get_longitud() > self.__tamano:
            raise ValueError("El barco es demasiado largo para posicionarlo ahí")
        else:
            if orientacion.upper() == "H":
                for i in range(barco.get_longitud()):
                    if self.__mapa_oculto[coord_y - 1][coord_x - 1 + i] == self.barco:
                        raise ValueError("El barco se solapa con otro. Prueba otra posición")
                for i in range(barco.get_longitud()):
                    self.__mapa_oculto[coord_y - 1][coord_x - 1 + i] = self.barco
                    coords.append((coord_x + i, coord_y))
            elif orientacion.upper() == "V":
                for i in range(barco.get_longitud()):
                    if self.__mapa_oculto[coord_y - 1 + i][coord_x - 1] == self.barco:
                        raise ValueError("El barco se solapa con otro. Prueba otra posición")
                for i in range(barco.get_longitud()):
                    self.__mapa_oculto[coord_y - 1 + i][coord_x - 1] = self.barco
                    coords.append((coord_x, coord_y + i))
            else:
                raise ValueError("Orientación no válida")
            barco.set_coords(coords)
            self.__barcos.append(barco)

    def golpear(self, coord_x: int, coord_y: int):
        if self.__mapa_oculto[coord_y - 1][coord_x - 1] == "H":
            self.__mapa_oculto[coord_y - 1][coord_x - 1] = self.hit
            self.__mapa_visible[coord_y - 1][coord_x - 1] = self.hit
            barco = self.buscar_barco_por_coord(coord_x, coord_y)
            barco.recibir_golpe()
            if barco.is_hundido():
                return "HUNDIDO"
            return "TOCADO"
        elif self.__mapa_oculto[coord_y - 1][coord_x - 1] == "~":
            self.__mapa_oculto[coord_y - 1][coord_x - 1] = self.miss
            self.__mapa_visible[coord_y - 1][coord_x - 1] = self.miss
            return "AGUA"
        return "YA_DISPARADO"

    def buscar_barco_por_coord(self, x, y):
        for b in self.__barcos:
            if (x, y) in b.get_coords():
                return b

    def get_diseno(self):
        for fila in self.get_mapa_oculto():
            for columna in fila:
                print(columna, end="\t\t")
            print("\n")

    def get_diseno_string(self):
        salida = ""
        for fila in self.get_mapa_oculto():
            for col in fila:
                salida += str(col) + "\t\t"
            salida += "\n"
        return salida
