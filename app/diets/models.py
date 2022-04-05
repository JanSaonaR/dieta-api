import pandas as pd
import json


def quantity_food_g(x):
    return round(100 * x['Multiplicador_Cantidad_Comer'])


def requierement_ok(x):
    if x['Multiplicador_Cantidad_Comer'] >= 1 and \
            x['Multiplicador_Cantidad_Comer'] <= 11:
        return True

    else:
        return False


class Child:
    def __init__(self, age, weight, height, activity, sex):
        self.age = age
        self.weight = weight
        self.height = height
        self.activity = activity
        self.sex = sex
        self.TMB = self.get_TMB()

    def get_TMB(self):
        if self.sex == 'F':
            if self.activity == 'sedentario':
                TMB = (655.0955 + (9.5634 * self.weight) +
                       (1.8449 * self.height) - (4.6756 * self.age)) * 1.20
                return TMB

            elif self.activity == 'baja_actividad':
                TMB = (655.0955 + (9.5634 * self.weight) +
                       (1.8449 * self.height) - (4.6756 * self.age)) * 1.375
                return TMB

            elif self.activity == 'activo':
                TMB = (655.0955 + (9.5634 * self.weight) +
                       (1.8449 * self.height) - (4.6756 * self.age)) * 1.725
                return TMB

            elif self.activity == 'muy_activo':
                TMB = (655.0955 + (9.5634 * self.weight) +
                       (1.8449 * self.height) - (4.6756 * self.age)) * 1.90
                return TMB

            else:
                return None

        elif self.sex == 'M':
            if self.activity == 'sedentario':
                TMB = (66.4730 + (13.7516 * self.weight) +
                       (5.0033 * self.height) - (6.7550 * self.age)) * 1.20
                return TMB

            elif self.activity == 'baja_actividad':
                TMB = (66.4730 + (13.7516 * self.weight) +
                       (5.0033 * self.height) - (6.7550 * self.age)) * 1.375
                return TMB

            elif self.activity == 'activo':
                TMB = (66.4730 + (13.7516 * self.weight) +
                       (5.0033 * self.height) - (6.7550 * self.age)) * 1.725
                return TMB

            elif self.activity == 'muy_activo':
                TMB = (66.4730 + (13.7516 * self.weight) +
                       (5.0033 * self.height) - (6.7550 * self.age)) * 1.90
                return TMB

            else:
                return None

    def get_cal_d(self):
        # Carbohidratos
        return ((self.TMB) * 0.6) * 0.3

    def get_cal_a(self):
        return ((self.TMB) * 0.6) * 0.4

    def get_g_d(self):
        # grasas
        return ((self.TMB)*0.3)*0.3

    def get_g_a(self):
        return ((self.TMB) * 0.3) * 0.4

    def get_p_d(self):
        # proteinas
        return ((self.TMB) * 0.10) * 0.3

    def get_p_a(self):
        return ((self.TMB) * 0.10) * 0.4


class Diet:
    def __init__(self, child, data):
        self.child = child
        self.data = data

    def get_desayuno(self):
        dt_desayuno = self.data[(self.data['Horario_1'] == 'Desayuno') |
                                (self.data['Horario_2'] == 'Desayuno')]

        dt_desayuno['Total_Calorias_Desayuno'] = (self.child.get_cal_d() +
                                                  self.child.get_g_d() +
                                                  self.child.get_p_d())

        dt_desayuno['Multiplicador_Cantidad_Comer'] = \
            (dt_desayuno['Total_Calorias_Desayuno'] /
             dt_desayuno['Calorias_Total_100g'])

        dt_desayuno['Cumple_Requisitos'] = \
            dt_desayuno.apply(requierement_ok, axis=1)

        dt_desayuno = dt_desayuno[(dt_desayuno['Cumple_Requisitos'] == True)]

        dt_desayuno['Cantidad_Gramos_Consumir'] = \
            dt_desayuno.apply(quantity_food_g, axis=1)
        dt_desayuno['Proteinas']=round(dt_desayuno['Proteinas']*\
            dt_desayuno['Multiplicador_Cantidad_Comer'])
        dt_desayuno['Grasas']=round(dt_desayuno['Grasas']*\
            dt_desayuno['Multiplicador_Cantidad_Comer'])
        dt_desayuno['Carbohidratos']=round(dt_desayuno['Carbohidratos']*\
            dt_desayuno['Multiplicador_Cantidad_Comer'])


        return dt_desayuno[['Alimento', 'Proteinas', 'Grasas',
                            'Carbohidratos', 'Cantidad_Gramos_Consumir']]

    def get_almuerzo(self):
        dt_almuerzo = self.data[(self.data['Horario_1'] == 'Almuerzo') |
                                (self.data['Horario_2'] == 'Almuerzo')]

        dt_almuerzo['Total_Calorias_Almuerzo'] = (self.child.get_cal_a() +
                                                  self.child.get_g_a() +
                                                  self.child.get_p_a())

        dt_almuerzo['Multiplicador_Cantidad_Comer'] = \
            (dt_almuerzo['Total_Calorias_Almuerzo'] /
             dt_almuerzo['Calorias_Total_100g'])

        dt_almuerzo['Cumple_Requisitos'] = \
            dt_almuerzo.apply(requierement_ok, axis=1)

        dt_almuerzo = dt_almuerzo[(dt_almuerzo['Cumple_Requisitos'] == True)]

        dt_almuerzo['Cantidad_Gramos_Consumir'] = \
            dt_almuerzo.apply(quantity_food_g, axis=1)
        dt_almuerzo['Proteinas']=round(dt_almuerzo['Proteinas']*\
            dt_almuerzo['Multiplicador_Cantidad_Comer'])
        dt_almuerzo['Grasas']=round(dt_almuerzo['Grasas']*\
            dt_almuerzo['Multiplicador_Cantidad_Comer'])
        dt_almuerzo['Carbohidratos']=round(dt_almuerzo['Carbohidratos']*\
            dt_almuerzo['Multiplicador_Cantidad_Comer'])

        return dt_almuerzo[['Alimento', 'Proteinas', 'Grasas',
                            'Carbohidratos', 'Cantidad_Gramos_Consumir']]

    def get_cena(self):
        dt_cena = self.data[(self.data['Horario_1'] == 'Almuerzo') |
                            (self.data['Horario_2'] == 'Almuerzo')]

        dt_cena['Total_Calorias_Cena'] = (self.child.get_cal_d() +
                                          self.child.get_g_d() +
                                          self.child.get_p_d())

        dt_cena['Multiplicador_Cantidad_Comer'] =\
            (dt_cena['Total_Calorias_Cena'] / dt_cena['Calorias_Total_100g'])

        dt_cena['Cumple_Requisitos'] = dt_cena.apply(requierement_ok, axis=1)

        dt_cena['Cantidad_Gramos_Consumir'] = dt_cena.apply(quantity_food_g,
                                                            axis=1)
        dt_cena['Proteinas']=round(dt_cena['Proteinas']*\
            dt_cena['Multiplicador_Cantidad_Comer'])
        dt_cena['Grasas']=round(dt_cena['Grasas']*\
            dt_cena['Multiplicador_Cantidad_Comer'])
        dt_cena['Carbohidratos']=round(dt_cena['Carbohidratos']*\
            dt_cena['Multiplicador_Cantidad_Comer'])

        return dt_cena[['Alimento', 'Proteinas', 'Grasas', 'Carbohidratos',
                        'Cantidad_Gramos_Consumir']]

    def getDiets(self, days):
        result_desayuno = self.get_desayuno()
        result_desayuno['Tipo'] = 'Desayuno'

        result_almuerzo = self.get_almuerzo()
        result_almuerzo['Tipo'] = 'Almuerzo'

        result_cena = self.get_cena()
        result_cena['Tipo'] = 'Cena'

        dieta = pd.concat([result_desayuno.sample(n=days),
                           result_almuerzo.sample(n=days),
                           result_cena.sample(n=days)], ignore_index=True)
        #orient='records'
        result = dieta.to_dict()

        return result
