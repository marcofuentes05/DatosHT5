#Simulacion de CPU de tiempo compartido usando SimPy
#Marco Fuentes - 18188
#Cristina Bautista -

import simpy
import random
random.seed(5)

maximo_memoria_proceso = 10
maximo_instrucciones = 10
instrucciones_por_unidad = 3
tiempo_total = 0
lst_tiempo = []

def programa(env, nombre, instrucciones, memoria, cpu, ram):
    num = int (instrucciones/instrucciones_por_unidad)+1
    
    contador = 0
    
    yield ram.get(memoria)
    #Ya tiene memoria, el estado es READY
    while instrucciones > 0:
        with cpu.request() as req:
            yield req
            #Si llega aqui, ya se esta procesando
            instrucciones -= instrucciones_por_unidad
            yield env.timeout(1)
            
            contador += 1
            
            aleatorio = random.randint(1,2)
            if aleatorio == 1:
                env.timeout(1)
                print(nombre," está en waiting @",env.now)
            if instrucciones <= 0:
                break
    yield ram.put(memoria)
    print(nombre," estuvo ", contador, " en el sistema")
    lst_tiempo.append(contador)
    
    
#-----------------------------------------------------------------------------------------------------------------------

env = simpy.Environment()

ram = simpy.Container(env, capacity = 100, init = 100)

cpu = simpy.Resource(env, capacity = 1)
numero_procesos = 10
for i in range (numero_procesos):
    env.process(programa(env, "Proceso %s" %i, random.randint(1,maximo_instrucciones),random.randint(1,maximo_memoria_proceso), cpu,ram))

print("Tiempo total: ",env.now)
tiempoPromedio = tiempo_total/numero_procesos
print("\n\n\nTiempo promedio: ",tiempoPromedio," ciclos\n\n\n")
env.run()



