#Simulacion de CPU de tiempo compartido usando SimPy
#Marco Fuentes - 18188
#Cristina Bautista -

import simpy
import random
random.seed(30)

maximo_memoria_proceso = 10
maximo_instrucciones = 10
instrucciones_por_unidad = 3

def programa(env, nombre, instrucciones, memoria, cpu, ram):
    print(instrucciones," para ", nombre)
    num = int (instrucciones/instrucciones_por_unidad)+1
    
    contador = 0
    
    yield ram.get(memoria)
    #Ya tiene memoria, el estado es READY
    print(nombre," ya tiene RAM asignada")
    while instrucciones > 0:
        
        with cpu.request() as req:
            yield req
            #Si llega aqui, ya se esta procesando
            instrucciones -= instrucciones_por_unidad
            print("Las instrucciones restantes del ",nombre," son: ",instrucciones)
            yield env.timeout(1)
            print(nombre, " acaba de ejecutarse una vez @", env.now)
            contador += 1
            print("El contador es ",contador)

            if instrucciones <= 0:
                break
                yield ram.put(memoria)
                print(nombre," estuvo ", contador, " en el sistema")

    print("El nivel de la ram es: ",ram.level)
#---------------------------------

env = simpy.Environment()

ram = simpy.Container(env, capacity = 100, init = 100)

cpu = simpy.Resource(env, capacity = 1)
print("El nivel de la ram es: ", ram.level)
for i in range (2):
    env.process(programa(env, "Proceso %s" %i, random.randint(1,maximo_instrucciones),random.randint(1,maximo_memoria_proceso), cpu,ram))

env.run()



