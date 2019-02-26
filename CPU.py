#Simulacion de CPU de tiempo compartido usando SimPy
#Marco Fuentes - 18188
#Cristina Bautista -

import simpy
import random
random.seed(30)

listaProcesosNew = []
listaProcesosReady = []
listaProcesosWaiting = []
listaProcesosTerminados = []
instrucciones_por_unidad = 3
numero_de_procesos = 10

class SistemaOperativo(object):
    def __init__(self, env):
        self.env = env
        self.ram = simpy.Container(env,init = 100, capacity = 100)
        self.cpu = simpy.Resource(env, capacity = 1)

             

class Proceso(object):
    def __init__(self, env, memoriaNecesaria, instrucciones, nombre):
        self.env = env
        self.memoriaNecesaria = memoriaNecesaria
        self.instrucciones = instrucciones
        self.nombre = nombre
        self.contador = 0
        
    def ejecutado(self, env, num, sistema):
        if self.instrucciones > 0:
            yield sistema.ram.get(self.memoriaNecesaria)
            yield env.timeout(1)
            listaProcesosReady.append(self)
            with sistema.cpu.request() as req:
                yield req
                yield env.timeout(1)
                self.instrucciones = self.instrucciones - num
                self.contador += 1
                print("Instrucciones restantes del proceso ",self.nombre,": ",self.instrucciones)
        elif self.instrucciones <= 0:
            listaProcesosTerminados.append(self)
        

def processGen(env, sistema, numero):
    for i in range(numero):        
        mem = random.randint(1,10)
        inst = random.randint(1,10)
        programa =Proceso(env, mem, inst, i)
        listaProcesosNew.append(programa)
        #cantidad = int ((programa.instrucciones/sistema.instrucciones_por_unidad)+1)
        #programa.ejecutado(instrucciones_por_unidad, sistema)

def imprimirResultados():
    for i in listaProcesosTerminados:
        print("Proceso ",i.nombre, " tardo ",i.contador)

env = simpy.Environment()

sistema = SistemaOperativo(env)

processGen(env, sistema, numero_de_procesos)

while len(listaProcesosTerminados) != numero_de_procesos:
    ##No funciona
    generador = env.process(programa.ejecutado(env, instrucciones_por_unidad,sistema))

env.run(30)

imprimirResultados()








    










