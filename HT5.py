import random
import simpy
import math

# Brandon Hernández 1376
# Fecha: 4 de marzo de 2020
# HT5.py

# Para modificar las caracteristicas del simulador
unitTime = 1
capacityRam = 100
capacityCpu = 1
capacityInstr = 3
interval = 10.0
randomRoot = 10
iOperation = 1

# Para calcular el promedio y desviación estandar
allTimes = []
elementNumber = 25.0
totalTime = 0.0

# Valores Estadisticos
timeStandar = 0.0

def CPU(env, cpu, ram, ramNeed, totInstr, unitTime, capacityInstr, processName, creatingTime):
    global totalTime
    random.seed(10)
    yield env.timeout(creatingTime) # Simulando que esta en espera
    
    startTime = float(env.now)    
    
    print("El %s ha ingresado a ingresado al computador" % processName)
    # Entrando y solicitando memoria Ram (NEW)
    with ram.get(ramNeed) as getRam:  
        yield getRam
        print("El %s ha conseguido %d de RAM para ejecutar %i instrucciones" % (processName, ramNeed, totInstr))
        # Esperando a que el  (READY)
        ready(cpu)

        while totInstr > 0:
            
            print("Al %s lo atendera el CPU" % processName)
            # Quitandole instrucciones al proceso (RUNNING)
            for i in range(capacityInstr):
                totInstr = totInstr - 1
                if (totInstr == 0):
                    break
            yield env.timeout(unitTime)
            
            # Verificando que aun hay instrucciones que realizar
            if (totInstr != 0):
                # Generando número para ver a que lugar se va a ir
                option = random.randint(1,2)
                
                # Simulando que espera el proceso (WAITING)
                if (option == 1):
                    print("El %s esta en espera" % processName)
                    yield env.timeout(iOperation)
                    
                    ready(cpu)
                    print("El %s vuelve a estar listo" % processName)
                    
                # (READY)
                else:
                    print("El %s vuelve a estar listo" % processName)
                    ready(cpu)

    # (EXIT)
    ram.put(ramNeed)
    print("El %s ha terminado su proceso" % processName)
    
    # Consiguiendo los tiempos
    finalTime = float(env.now - startTime)
    totalTime += float(finalTime)
    allTimes.append(float(finalTime))

# Cuando este listo
def ready(cpu):
    with cpu.request():  
        yield cpu

# Función para la desviación
def statistics(totalTime, elementNumber):
    media = totalTime/elementNumber
    summation = 0.0
    for i in range(len(allTimes)):
        summation += (allTimes[i] - media)**2
    
    # Dividiendo
    summation = summation/elementNumber
    return math.sqrt(summation)
    
# El entorno y los recursos a utilizar
env = simpy.Environment()
cpu = simpy.Resource(env, capacity = capacityCpu)
ram = simpy.Container(env, init = capacityRam, capacity = capacityRam)

random.seed(randomRoot)
# Empezando la simulación
for i in range(int(elementNumber)):
    creatingTime = random.expovariate(1.0/interval)
    ramNeed = random.randint(1,10)
    totInstr = random.randint(1,10)
    env.process(CPU(env, cpu, ram, ramNeed, totInstr, unitTime, capacityInstr, "proceso: %s" % (i + 1), creatingTime))
      
# Corriendo la simulación
env.run()

timeStandar = statistics(totalTime, elementNumber)
# Mostrando resultados
print("\n|-------------------------------------------------------------------|")
print("En esta simulación se obtuvo una media de %f unidades de tiempo" % (totalTime/elementNumber))
print("y una desviación estandadr de %f unidades de tiempo" % timeStandar)