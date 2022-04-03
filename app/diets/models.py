import pandas as pd


class Child:
    def __init__(self, age, weight, height, activity):
        self.age = age
        self.weight = weight
        self.height = height
        self.activity = activity

    # Función que calcula las macros del niño
    def calculate_macro(self):
        pass

    def serialize(self):
        return {
                'age': self.age,
                'weight': self.weight,
                'height': self.height,
                'activity': self.activity
                }


class Diet:
    def __init__(self, child):
        self.child = child

    # Agregar aquí las funciones para filtrar la dieta y devolver
    # La lista filtrada en formato Json
    def getDiets(self):
        pass
