import time
import random
import math

people=[('Seymour','BOS'),('Franny','DAL'),('Zooey','CAK'),('Walt','MIA'),
        ('Buddy','ORD'),('Les','OMA')]

destination='LGA'

flights={}

for line in file('schedule.txt'):
    origin,dest,depart,arrive,price=line.strip().split(',')
    flights.setdefault((origin,dest),[])

    #add details to the list of possible flights
    flights[(origin,dest)].append((depart,arrive,int(price)))

def getminutes(t):
    x=time.strptime(t,'%H:%M')
    return x[3]*60+x[4]

def printSchedule(r):
    for d in range(len(r)/2):
        name=people[d][0]
        origin=people[d][1]
        out=flights[(origin,destination)][r[d*2]] #Different from book
        ret=flights[(destination,origin)][r[d*2+1]]
        print '%10s%10s %5s-%5s $%3s %5s-%5s $%3s' % (name,origin,
                                                      out[0],out[1],out[2],
                                                      ret[0],ret[1],ret[2])

def schedulecost(sol):
    totalPrice=0
    latestarrival=0
    earliestdep=24*60

    for d in range(len(sol)/2):
        #Get the inbound and outbound flights
        origin=people[d][1]
        outbound=flights[(origin,destination)][int(sol[2*d])] #Seems need change
        returnf=flights[(destination,origin)][int(sol[2*d+1])]

        #Total price is the price of all outbound and return flights
        totalPrice+=outbound[2]
        totalPrice+=returnf[2]

        if latestarrival<getminutes(outbound[1]): latestarrival=getminutes(outbound[1])
        if earliestdep>getminutes(returnf[0]): earliestdep=getminutes(returnf[0])

    totalwait=0
    for d in range(len(sol)/2):
        origin=people[d][1]
        outbound=flights[(origin,destination)][int(sol[2*d])] #Seems need change
        returnf=flights[(destination,origin)][int(sol[2*d+1])]
        totalwait+=latestarrival-getminutes(outbound[1])
        totalwait+=getminutes(returnf[0])-earliestdep

    if latestarrival>earliestdep: totalPrice+=50

    return totalPrice+totalwait
    
    
def randomoptimize(domain,costf):
    best=99999999
    bestr=None
    for i in range(1000):
        #Create a random solution
        r=[random.randint(domain[i][0],domain[i][1])
           for i in range(len(domain))]
        cost=costf(r)

        if cost<best:
            best=cost
            bestr=r
    
    return r


def hillclimb(domain,costf):
    #Create a random solution
    sol=[random.randint(domain[i][0],domain[i][1])
         for i in range(len(domain))]

    while 1:
        #Create a list of neighbor solutions
        neighbors=[]
        for j in range(len(domain)):
            #One away in each direction
            if sol[j]>domain[j][0]:
                neighbors.append(sol[0:j]+[sol[j]-1]+sol[j+1:])
            if sol[j]<domain[j][1]:
                neighbors.append(sol[0:j]+[sol[j]+1]+sol[j+1:])

        current=costf(sol)
        best=current
        for j in range(len(neighbors)):
            cost=costf(neighbors[j])
            if cost<best:
                best=cost
                sol=neighbors[j]

            if best==current:
                break

        return sol

def annealingoptimize(domain,costf,T=10000.0,cool=0.95,step=1):
    vec=[float(random.randint(domain[i][0],domain[i][1])) for
         i in range(len(domain))]

    while T>0.1:
        i=random.randint(0,len(domain)-1)

        dire=random.randint(-step,step)

        vecb=vec[:]
        vecb[i]+=dire
        if vecb[i]<domain[i][0]:vecb[i]=domain[i][0]
        elif vecb[i]>domain[i][1]:vecb[i]=domain[i][1]

        ea=costf(vec)
        eb=costf(vecb)
        p=pow(math.e,0-abs(eb-ea)/T) #Or -abs(eb-ea)

        if (eb<ea or random.random()<p):
            vec=vecb

        T=T*cool
    return vec

def geneticoptimize(domain,costf,popsize=50,step=1,mutprod=0.2,
                        elite=0.2,maxiter=100):
    def mutate(vec):
        i=random.randint(0,len(domain)-1)
        if random.random()<0.5 and vec[i]>domain[i][0]:
            return vec[0:i]+[vec[i]-step]+vec[i+1:]
        elif vec[i]<domain[i][1]:
            return vec[0:i]+[vec[i]+step]+vec[i+1:]
        else:
            return vec[0:i]+[vec[i]-step]+vec[i+1:]

    def crossover(r1,r2):
        i=random.randint(1,len(domain)-2)
        return r1[0:i]+r2[i:]

    pop=[]
    for i in range(popsize):
        vec=[random.randint(domain[i][0],domain[i][1]) for i in
             range(len(domain))]
        pop.append(vec)

    topelite=int(elite*popsize)

    for i in range(maxiter):
        #print pop
        scores=[(costf(v),v) for v in pop]
        scores.sort()
        print scores
        ranked=[v for (s,v) in scores]

        pop=ranked[0:topelite]

        while len(pop)<popsize:
            if random.random()<mutprod:
                #Mutation
                c=random.randint(0,topelite)
                toadd=mutate(ranked[c])
                if toadd==None:
                    print "Mutation creates none",c,ranked[c]
                pop.append(toadd)
            else:
                c1=random.randint(0,topelite)
                c2=random.randint(0,topelite)
                toadd=crossover(ranked[c1],ranked[c2])
                if toadd==None:
                    print "Crossover creates none"
                pop.append(toadd)

        print scores[0][0]
        
    return scores[0][1]

        
    
    
