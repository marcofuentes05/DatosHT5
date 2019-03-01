#Simulacion de CPU de tiempo compartido usando SimPy
#Marco Fuentes - 18188
#Cristina Bautista - 161260

import simpy
import random
import math
import statistics as stats
random.seed(100)

maximo_memoria_proceso = 10
maximo_instrucciones = 10
instrucciones_por_unidad = 3
lst_tiempo = []
interval = 10

def programa(env, nombre, instrucciones, memoria, cpu, ram,intertval):
    contador = env.now
    num = int (instrucciones/instrucciones_por_unidad)+1
    
    yield ram.get(memoria)
    #Ya tiene memoria, el estado es READY
    if instrucciones <=2:
        env.timeout(1)
        contador += 1
    else:
        while instrucciones > 2:
            with cpu.request() as req:
                yield req
                #Si llega aqui, ya se esta procesando
                instrucciones -= instrucciones_por_unidad
                yield env.timeout(1)
                
                contador += 1
                
                aleatorio = random.randint(1,2)
                if aleatorio == 1:
                    env.timeout(1)
                    #print(nombre," está en waiting @",env.now)
                if instrucciones <= 0:
                    break
    yield ram.put(memoria)
    print(nombre," estuvo ", contador, " en el sistema")
    tiempo_total = env.now - contador
    print("El tiempo total es: %s" %(tiempo_total))
    lst_tiempo.append(tiempo_total)
    print("El promedio es: ",stats.mean(lst_tiempo))
    print("La desv estandar es: ",stats.pstdev(lst_tiempo))
    
#-----------------------------------------------------------------------------------------------------------------------

env = simpy.Environment()

ram = simpy.Container(env, capacity = 100, init = 100)

cpu = simpy.Resource(env, capacity = 1)
numero_procesos = 25


def gen(env, ram, cpu, numero_procesos,maximo_instrucciones, maximo_memoria_proceso, interval):
    
    res = numero_procesos

    while res >0:
        yield env.timeout(1)
        a = 1
        num = (int) (random.expovariate(1.0/interval))
        if res - num > 0:
            res -= num
            for i in range(num):
                env.process(programa(env, "Proceso %s" %a, random.randint(1,maximo_instrucciones),random.randint(1,maximo_memoria_proceso), cpu,ram, interval))
        else:
            for i in range(res):
                env.process(programa(env, "Proceso %s" %a, random.randint(1,maximo_instrucciones),random.randint(1,maximo_memoria_proceso), cpu,ram, interval))
            res = 0
        a += 1


env.process(gen(env, ram, cpu, numero_procesos,maximo_instrucciones, maximo_memoria_proceso, interval))
##tiempoPromedio = tiempo_total/numero_procesos
##print("\n\n\nTiempo promedio: ",tiempoPromedio," ciclos\n\n\n")
env.run()



