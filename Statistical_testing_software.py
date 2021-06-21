import Base_evolution_software as evo
import matplotlib.pyplot as plt


def iterations(maximum): ## Maximum must be divisible by 25

    xvalues = []
    yvalues = []
    
    for x in range(25, maximum + 1, 25):
        print ("")
        print ("")
        print ("Starting {0} iteration testing".format(x))
        print ("")
        print ("")

        raw = 0
        xvalues.append(x)
        
        for y in range(0, 11):
            print("{0}.{1}".format(x, y))
            print ("")
            output = evo.speciesTimeline(100, 10, x, 0.5)
            difference = output[1].fitness - output[0].fitness
            percentage = (difference / output[0].fitness) * 100
            raw += percentage
        avg = raw / 10
        yvalues.append(avg)

        ## NEED TO ADD ANOMALY DETECTION


    plt.plot(xvalues, yvalues)
    plt.axis([0,maximum + 25, 0, 30])
    plt.show()


def mutations(maximum): ## Maximum must be divisble by 0.2

    xvalues = []
    yvalues = []
    x = 0.2 ## bounds for mutation are now rounded due to finite floating point precision - this may cause minor errors later on
    
    while x <= maximum:
        print ("")
        print ("")
        print ("Starting {0} mutation tesing testing".format(x))
        print ("")
        print ("")

        raw = 0
        xvalues.append(x)
        
        for y in range(0, 11):
            print("{0}.{1}".format(x, y))
            print ("")
            output = evo.speciesTimeline(100, 10, 100, x)
            difference = output[1].fitness - output[0].fitness
            percentage = (difference / output[0].fitness) * 100
            raw += percentage
        avg = raw / 10
        yvalues.append(avg)

        x += 0.2

        ## NEED TO ADD ANOMALY DETECTION


    plt.plot(xvalues, yvalues)
    plt.axis([0,maximum + 0.2, 0, 30])
    plt.show()


def populationSize(maximum):
    pass
    ## def populationSize will attempt to test how starting size affects convergence
    ## The proportion replaced each cyle will be kept the same -- this is instead of keeping the actual number replaced the same
