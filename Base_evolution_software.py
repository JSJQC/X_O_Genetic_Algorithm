# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 18:21:56 2017

@author: jakes

"""

## Add back basic AI training, with averagefitness at changeover point saved

## line 102 subject to experimentation
## Line 147 subject to experimentation
## Line 253 subject to experimentation
## Line 266 subject to experimentation

## NEED TO ASSIGN VALUES FOR FITNESS AND AGE REPLACEMENT
## Higher replacement factor means lower numbers replaced


import time
import numpy
import random
import cProfile

import Game_structural_software as mainGame
import Network_base_class as networkClass


def averageFitness(population):
    
    popSize = len(population)
    totalFitness = 0

    for item in population:
        fit = item.fitness
        totalFitness += fit

    average = totalFitness / popSize

    return average


def calcFitness(network, opponent, repeats):
    ## startTime = time.time()
    performance = 0
    winRecord = mainGame.autoplay(opponent, repeats, network)
    for item in winRecord:
        if item == 0:
            performance += 3
        elif item == '-':
            performance += 1
    ## print (performance)
    normPerf = performance / (3 * len(winRecord)) ## Could be subject to change
    if normPerf == 0:
        normPerf = 0.1
    ## print (normPerf)
    ## endTime = time.time()
    ## tTime = endTime - startTime
    #  print (tTime)
    return normPerf


def initialisePopulation(size):
    ## startTime = time.time()
    population = []
    counter = 0
    while counter < size:
        net = networkClass.Neural_Network()
        net.fitness = calcFitness(net, 'random', 40)
        net.birthGeneration = 0
        population.append(net)
        counter += 1
    ## endTime = time.time()
    ## tTime = endTime - startTime
    ## print(tTime)
    return population


def selectParents(population):
    sTime = time.time()
    lowest = 1.1
    tempPop = []
    parents = []
    
    for item in population:
        if item.fitness < lowest:
            lowest = item.fitness
    lowest = lowest / 10
    ## print (lowest)
    
    for item in population:
        times = int(item.fitness // lowest)
        ## print (item.fitness)
        ## print (times)
        for x in range(times + 1):
            tempPop.append(population.index(item))
    ## print (tempPop)
        
    num1 = mainGame.GenerateRandomNumber(0, len(tempPop)) - 1
    parentI1 = tempPop[num1]
    parent1 = population[parentI1]
    parents.append(parent1)
    done = False
    while done == False:
        num2 = mainGame.GenerateRandomNumber(0, len(tempPop)) - 1
        parentI2 = tempPop[num2]
        if parentI1 != parentI2:
            done = True
            parent2 = population[parentI2]
            parents.append(parent2)
    
    eTime = time.time()
    toTime = eTime - sTime
    return parents


def selectFitnessDeath(population, number): ## 'number' is number to be lost
    
    lowest = 0.10
    highest = 0
    best = None
    tempPop = []
    casualties = []
    
    fitnesses = []
    
    for item in population:
        '''if item.fitness < lowest:
            lowest = item.fitness'''
        
        if item.fitness > highest:
            best = item
            highest = item.fitness
    
    for item in population:
        if best != item:
            times = item.fitness / lowest
            iterations = round((1 / times ** (3/2)) * 100) ## SUBJECT TO CHANGE
            for x in range(iterations):
                tempPop.append(population.index(item))
    ##print (len(tempPop))
            
    for x in range (number):
        done = False
        while done == False:
            ## print(x)
            index = mainGame.GenerateRandomNumber(0,(len(tempPop)-1))
            check = tempPop[index] in casualties
            ## print (check)
            if check == True:
                ## print (tempPop[index])
                pass
            elif check == False:
                casualties.append(tempPop[index])
                done = True


    casualties = sorted(casualties, reverse = True)
            
    
    return casualties ## returns indices
            
        
            
    ## Temporary population has been set up, with the indices of individuals
    ## Now must choose individuals to be lost -- Done
    ## Will then return indices of lost individuals -- Done


def selectAgeDeath(population, number, generationNumber):

    highest = 0

    for item in population:
        
        if item.fitness > highest:
            best = item
            highest = item.fitness
    
    oldNetworks = []
    ageCasualties = []
    
    for network in population:
        age = generationNumber - network.birthGeneration
        if age >= 5:
            if network != best:
                oldNetworks.append(network)

    if len(oldNetworks) > 1:
        for x in range (number):
            done = False
            while done == False:
                index = mainGame.GenerateRandomNumber(0,(len(oldNetworks)-1))
                check = oldNetworks[index] in ageCasualties
                ## print (check)
                if check == True:
                    ## print (tempPop[index])
                    pass
                elif check == False:
                    ageCasualties.append(oldNetworks[index])
                    done = True
    elif len(oldNetworks) == 1:
        ageCasualties.append(oldNetworks[0])

    return ageCasualties ## Returns networks


def removeDead(population, generationNumber, replacementFactor): ## replacementFactor will likely be 5

    ## Age-related removal -------------------------------------------------
    
    oldNetworks = []

    highest = 0

    for item in population:
        
        if item.fitness > highest:
            best = item
            highest = item.fitness

    totalReplace = round(len (population) / replacementFactor)
    
    for network in population:
        age = generationNumber - network.birthGeneration
        if age >= 5:
            if network != best:
                oldNetworks.append(network)
            
    if len (oldNetworks) >= (totalReplace / 2):
        ageReplace = round(totalReplace / 2)
    else:
        ageReplace = len(oldNetworks)
        
    ageDead = selectAgeDeath(population, ageReplace, generationNumber) ## ageDead is a list of networks
    
    for network in oldNetworks:
        check = network in ageDead
        if check == True:
            population.remove(network)

    ## ------------------------------------------------------------------------
    ## Fitness-related removal ------------------------------------------------

    fitnessReplace = totalReplace - ageReplace
                     
    fitDead = selectFitnessDeath(population, fitnessReplace) ## fitDead is a list of indices

    for index in fitDead:
        population.remove(population[index]) ## issue here with index out of range
        
    ## -------------------------------------------------------------------------

    return population


def convertToChromosome(array, rows, columns):
    ## print (array)
    chromosome = []
    splitArray = numpy.split(array, rows)
    for x in range(rows):
        chromosome = numpy.concatenate((chromosome, splitArray[x][0])) ## issue here with different list sizes -- sorted
    ## print (chromosome)
    return chromosome
    

def chooseChiasmata(parents):

    chromosome1_1 = convertToChromosome(parents[0].inputToHidden, 18, 9)
    chromosome2_1 = convertToChromosome(parents[1].inputToHidden, 18, 9)
    chromosome1_2 = convertToChromosome(parents[0].hiddenToOutput, 9, 18)
    chromosome2_2 = convertToChromosome(parents[1].hiddenToOutput, 9, 18)
    ## print (chromosome1_1)
    ## print (chromosome1_2)
                  
    chiasmaNum1 = mainGame.GenerateRandomNumber(2, 5)
    swapPointsIn = []
    swapPointsOut = []
    
    for x in range(chiasmaNum1):
        point = mainGame.GenerateRandomNumber(1, len(chromosome1_1))
        if point in swapPointsIn: ## Helps to prevent two chiasmata of same position -- not vital or complete, but simulates biology closer
            point = mainGame.GenerateRandomNumber(1, len(chromosome1_1))
        swapPointsIn.append(point)
        
    for x in range(chiasmaNum1):
        point = mainGame.GenerateRandomNumber(1, len(chromosome1_2))
        if point in swapPointsOut: ## Helps to prevent two chiasmata of same position -- not vital or complete, but simulates biology closer
            point = mainGame.GenerateRandomNumber(1, len(chromosome1_2))
        swapPointsOut.append(point)
            
    swapPointsIn = sorted(swapPointsIn)
    swapPointsOut = sorted(swapPointsOut)
    
    return swapPointsIn, swapPointsOut


def applyChiasmata(swapPoints, parents): ## swapPoints = [swapPointsIn, swapPointsOut]

    chromosome1_1 = convertToChromosome(parents[0].inputToHidden, 18, 9)
    chromosome2_1 = convertToChromosome(parents[1].inputToHidden, 18, 9)
    chromosome1_2 = convertToChromosome(parents[0].hiddenToOutput, 9, 18)
    chromosome2_2 = convertToChromosome(parents[1].hiddenToOutput, 9, 18)

    ## NEED TO FIND EFFECTIVE IMPLEMENTATION OF 'BRAID' SYSTEM
    
    ## ----------- Layer 1 --------------------------------------------------------
    
    ## Initial conditions of chromosomes
    
    strand1 = chromosome1_1
    strand2 = chromosome2_1
    
    swapPointsIn = swapPoints[0]
    
    for x in range(len(swapPoints)):
        chiasma = swapPointsIn[x]
        
        perm1 = strand1[:(chiasma - 1)]
        perm2 = strand2[:(chiasma - 1)]
        # print (perm1)
        
        temp1 = strand2[(chiasma - 1):]
        temp2 = strand1[(chiasma - 1):]
        # print (temp1)
        
        strand1 = numpy.concatenate((perm1, temp1))
        strand2 = numpy.concatenate((perm2, temp2))
        
    choice1 = mainGame.GenerateRandomNumber(0,1)
    
    if choice1 == 0:
        mainStrand1 = strand1
    elif choice1 == 1:
        mainStrand1 = strand2
    
        
    ## ----------------------------------------------------------------------------
    ## ----------- Layer 2 --------------------------------------------------------
    
    strand3 = chromosome1_2
    strand4 = chromosome2_2
    
    swapPointsOut = swapPoints[1]
    
    for x in range(len(swapPoints)):
        chiasma = swapPointsOut[x]
        
        perm3 = strand3[:(chiasma - 1)]
        perm4 = strand4[:(chiasma - 1)]
        
        temp3 = strand4[(chiasma - 1):]
        temp4 = strand3[(chiasma - 1):]
        
        strand3 = numpy.concatenate((perm3, temp3))
        strand4 = numpy.concatenate((perm4, temp4))
        
    choice2 = mainGame.GenerateRandomNumber(0,1)
    
    if choice2 == 0:
        mainStrand2 = strand3
    elif choice2 == 1:
        mainStrand2 = strand4
    
    ## print (numpy.shape(strand1))
    ## print (numpy.shape(strand2))
    ## print (numpy.shape(strand3))
    ## print (numpy.shape(strand4))
    ## print (numpy.shape(layer1))
    ## print (numpy.shape(layer2))
    
    ## ----------------------------------------------------------------------------
    
    return mainStrand1, mainStrand2
    

def mutation(childWeights, rate):
    ## Mutates one whole layer from a given child
    
    mutation = None
    
    ## Taking any number below 10 to be a positive mutation occurence:
    upperbound = round(1000 / rate)
    for index in range(len(childWeights)):
        mutationChance = mainGame.GenerateRandomNumber(0, upperbound)
        if mutationChance <= 10:
            mutation = True
        else:
            mutation = False

        if mutation == True:
            childWeights[index] = numpy.random.uniform(-3, -3)
            
    return childWeights


def convertBackToLayer(strand, dimensions):
    
    layer = numpy.mat(strand)
    layer = layer.reshape(dimensions[0], dimensions[1])
    layer = numpy.array(layer)
    
    return layer

def createOffspring(parents, mutationRate, generationNumber):
    ## chiasmata will be formed, and the offspring's genotype selected
    ## Mutations will then be applied to the offspring
    ## The offspring will be converted back to the correct array dimensions
    ## Offspring will then be returned
    
    newStrands = []
    
    chiasmata = chooseChiasmata(parents)
    strands = applyChiasmata(chiasmata, parents)
    newStrands.append(mutation(strands[0], mutationRate))
    newStrands.append(mutation(strands[1], mutationRate))
    layer1 = convertBackToLayer(newStrands[0], numpy.shape(parents[0].inputToHidden))
    layer2 = convertBackToLayer(newStrands[1], numpy.shape(parents[0].hiddenToOutput))

    ## print (layer1)
    ## print (layer2)
    
    childNetwork = networkClass.Neural_Network()
    childNetwork.birthGeneration = generationNumber
    childNetwork.inputToHidden = layer1
    childNetwork.hiddenToOutput = layer2
    
    return childNetwork
        

def holdingPen(population, generationNumber, replacementFactor, mutationRate): ## In future, 'generation' can be used to determine which opponent to use
    counter = 0
    enclosure = []
    
    popSize = len(population) ## popSize should be divisible by replacementFactor to avoid population size fluctuations
    replaceNumber = round(popSize / replacementFactor)
    
    for x in range(replaceNumber):
        child = createOffspring(selectParents(population), mutationRate, generationNumber)
        enclosure.append(child)
        
    ## print (enclosure)
    ## print (enclosure[1].inputToHidden)
    
    for child in enclosure:
        fitness = calcFitness(child, 'random', 40) ## Third parameter will be an area of investigation
        child.fitness = fitness
        
    return enclosure


def saveBest(population):
    
    best = None
    highestFitness = 0
    
    for item in population:
        if item.fitness > highestFitness:
            highestFitness = item.fitness
            best = item
            
    return best


def generationCycle(population, generationNumber, replacementFactor, mutationRate):
    
    bestSpecimen = saveBest(population)
    enclosure = holdingPen(population, generationNumber, replacementFactor, mutationRate)
    removeDead(population, generationNumber, replacementFactor)
    for network in enclosure:
        population.append(network)
        
    ##print (population)
    
    averagefitness = averageFitness(population)
    
    return population, bestSpecimen, averagefitness
    
    
def speciesTimeline(startingSize, replacementFactor, cycleNumber, mutationRate):
    
    print ("Initialising...")
    
    s1 = round((cycleNumber / 10))
    s2 = round((cycleNumber / 10) * 2)
    s3 = round((cycleNumber / 10) * 3)
    s4 = round((cycleNumber / 10) * 4)
    s5 = round((cycleNumber / 10) * 5)
    s6 = round((cycleNumber / 10) * 6)
    s7 = round((cycleNumber / 10) * 7)
    s8 = round((cycleNumber / 10) * 8)
    s9 = round((cycleNumber / 10) * 9)
    s10 = round((cycleNumber / 10) * 10)
    
    startTime = time.time()
    
    generationCounter = 1
    population = initialisePopulation(startingSize)
    firstBest = saveBest(population)

    print ("Evolution starting")
    
    for x in range(cycleNumber + 1):
        
        if x == s1:
            print ("Evolution 10% complete")
        elif x == s2:
            print ("Evolution 20% complete")
        elif x == s3:
            print ("Evolution 30% complete")
        elif x == s4:
            print ("Evolution 40% complete")
        elif x == s5:
            print ("Evolution 50% complete")
        elif x == s6:
            print ("Evolution 60% complete")
        elif x == s7:
            print ("Evolution 70% complete")
        elif x == s8:
            print ("Evolution 80% complete")
        elif x == s9:
            print ("Evolution 90% complete")
        elif x == s10:
            print ("Evolution complete")

        generation = generationCycle(population, generationCounter, replacementFactor, mutationRate)
        population = generation[0]
        best = generation[1]
        ## averagefitness = generation[2]
        
        generationCounter += 1

    print ("")
    print ("Start:")
    print (firstBest.fitness)
    print ("")
    print ("Final:")
    print (best.fitness)
        
    endTime = time.time()
    dTime = endTime - startTime
    
    return firstBest, best
