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
        returnf=flights[(origin,destination)][int(sol[2*d+1])]

        #Total price is the price of all outbound and return flights
        totalPrice+=outbound[2]
        totalPrice+=returnf[2]

        if latestarrival<getminutes(outbound[1]): latestarrival=getminutes(outbound[1])
        if earliestdep>getminutes(returnf[0]): earliestdep=getminutes(returnf[0])

    totalwait=0
    for d in range(len(sol)/2):
        origin=people[d][1]
        outbound=flights[(origin,destination)][int(sol[2*d])] #Seems need change
        returnf=flights[(origin,destination)][int(sol[2*d+1])]
        totalwait+=latestarrival-getminutes(outbound[1])
        totalwait+=getminutes(returnf[0])-earliestdep

    if latestarrival>earliestdep: totalPrice+=50

    return totalPrice+totalwait
    
    
def randomoptimize(domain,costf):
    best=99999999
    bestr=None
    for i in range(10000):
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
