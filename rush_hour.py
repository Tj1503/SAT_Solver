from z3 import *
import sys
import math

l=[]
f = open(sys.argv[1],"r")
for e in f:
    l = l + e.split()

n = int(l[0].split(",")[0])
limit = int(l[0].split(",")[1])

red_loc = [int(l[1].split(",")[0]), int(l[1].split(",")[1])]

loc = []
for i in range(2,len(l)):
    vars = [int(e.strip()) for e in l[i].split(',')]
    loc.append(vars)

p = [[[[ Bool ("e_{}_{}_{}_{}".format(s,k,i,j)) for j in range(n)] for i in range(n)]for k in range(4)]for s in range(limit+1)]
#q=[[[Bool("e_{}_{}".format(s,i,j))for j in range(n)]for i in range(n)]for s in range(limit)]

for k in range(4):
    for i in range(n):
        for j in  range(n):
            p[0][k][i][j]=bool(0)

Q=Solver()
for i in loc:
    if i[0]==1:
        p[0][i[0]][i[1]][i[2]]=bool(1)
        Q.add(p[0][i[0]][i[1]][i[2]])
    elif i[0]==0:
        p[0][i[0]][i[1]][i[2]]=bool(1)
        Q.add(p[0][i[0]][i[1]][i[2]])
    else:
        p[0][i[0]][i[1]][i[2]]=bool(1)
        Q.add(p[0][i[0]][i[1]][i[2]])

p[0][3][red_loc[0]][red_loc[1]]=bool(1)
Q.add(p[0][3][red_loc[0]][red_loc[1]])

def prright(s,j):
    if j<n-2:
        move=And(p[s][3][red_loc[0]][j],p[s+1][3][red_loc[0]][j+1])
        New=Or(p[s][2][red_loc[0]][j+2],p[s][0][red_loc[0]][j+2],p[s][1][red_loc[0]][j+2])
        if red_loc[0]>=1:
            New=Or(New,p[s][0][red_loc[0]-1][j+2])
        New=Not(New)
        implication=Implies(move,New)
    else:
        implication=bool(1)
        move=bool(0)
    yield implication
    yield move

def prleft(s,j):
    if j>0:
        move=And(p[s][3][red_loc[0]][j],p[s+1][3][red_loc[0]][j-1])
        New=Or(p[s][2][red_loc[0]][j-1],p[s][0][red_loc[0]][j-1])
        if red_loc[0]>=1:
            New=Or(New,p[s][1][red_loc[0]-1][j-1])
        if j>1:
            New=Or(New,p[s][0][red_loc[0]][j-2])
        New=Not(New)
        implication=Implies(move,New)
    else:
        implication=bool(1)
        move=bool(0)
    yield implication
    yield move

def phleft(s,i,j):
    if j>0:
        move=And(p[s][1][i][j],p[s+1][1][i][j-1])
        New=Or(p[s][2][i][j-1],p[s][0][i][j-1])
        if i>=1:
            New=Or(New,p[s][1][i][j-1])
        if j>1:
            New=Or(New,p[s][0][i][j-2],p[s][3][i][j-2])
        New=Not(New)
        implication=Implies(move,New)
    else:
        implication=bool(1)
        move=bool(0)
    yield implication
    yield move


def phright(s,i,j):   
    if j<n-2:
        move=And(p[s][1][i][j],p[s+1][1][i][j+1])
        New=Or(p[s][2][i][j+2],p[s][0][i][j+2],p[s][1][i][j+2],p[s][3][i][j+2])
        if i>=1:
            New=Or(New,p[s][0][i-1][j+2])
        New=Not(New)
        implication=Implies(move,New)
    else:
        implication=bool(1)
        move=bool(0)
    yield implication
    yield move

def pvup(s,i,j):
    if i>0:
        move=And(p[s][0][i][j],p[s+1][0][i-1][j])
        New=Or(p[s][2][i-1][j],p[s][0][i-1][j],p[s][3][i-1][j])
        if i>1:
            New=Or(New,p[s][0][i-2][j])
        if j>0:
            New=Or(New,p[s][1][i-1][j-1],p[s][3][i-1][j-1])
        New=Not(New)
        implication=Implies(move,New)
    else:
        implication=bool(1)
        move=bool(0)
    yield implication
    yield move

def pvdown(s,i,j):
    if i<n-2:
        move=And(p[s][0][i][j],p[s+1][0][i+1][j])
        New=Or(p[s][2][i+2][j],p[s][0][i+2][j],p[s][3][i+2][j],p[s][1][i+2][j])
        if j>0:
            New=Or(New,p[s][1][i+2][j-1],p[s][3][i+2][j-1])
        New=Not(New)
        implication=Implies(move,New)
    else:
        implication=bool(1)
        move=bool(0)
    yield implication
    yield move

horizontal=set()
h=0
vertical=set()
v=0
mine=[]
lm=0
for e in loc:
    if e[0]==1:
        h+=1
        horizontal.add(e[1])
    if e[0]==0:
        v+=1
        vertical.add(e[2]) 
    if e[0]==2:
        l=[]
        l.append(e[1])
        l.append(e[2])
        mine.append(l)
        lm+=1


che=p[0][3][red_loc[0]][n-2]



for s in range(limit): 
    z=0
    atleast=Bool("atleast")
    atleast=bool(0)

    nrs=[[ Int ("r_{}_{}".format(s,i,j)) for j in range(n)]for s in range(limit+1)]
    nhs=[[[ Int ("s_{}_{}_{}".format(s,i,j)) for j in range(n)] for i in range(n)]for s in range(limit+1)]
    nvs=[[[ Int ("h_{}_{}_{}".format(s,i,j)) for j in range(n)] for i in range(n)]for s in range(limit+1)]

    tr=Int("tr")
    th=Int("th")
    tv=Int("tv")
    tm=Int("tm")
    movessum=Int("movessum")

    tr=0
    tv=0
    th=0
    tm=0
    movessum=0

    
    for j in range(n):
        
        nrs[s+1][j]=IntSort().cast(p[s+1][3][red_loc[0]][j])
        tr+=nrs[s+1][j]
        
        lrleft=list(prleft(s,j))
        lrright=list(prright(s,j))
        Q.add(lrleft[0])
        Q.add(lrright[0])
        
        movessum+=IntSort().cast(lrleft[1])
        movessum+=IntSort().cast(lrright[1])
        
        samestate=Implies(p[s][3][red_loc[0]][j],p[s+1][3][red_loc[0]][j])
        poss=Or(And(samestate,Not(lrleft[1]),Not(lrright[1])),And(Not(samestate),(lrleft[1]),Not(lrright[1])),And(Not(samestate),Not(lrleft[1]),(lrright[1])))
        Q.add(poss)
        
        atleast=Or(atleast,lrleft[1],lrright[1])
        
        for i in horizontal:
            
            nhs[s+1][i][j]=IntSort().cast(p[s+1][1][i][j])
            th+=nhs[s+1][i][j]
            
            lrleft=list(phleft(s,i,j))
            lrright=list(phright(s,i,j))
            Q.add(lrleft[0])
            Q.add(lrright[0])

            movessum+=IntSort().cast(lrleft[1])
            movessum+=IntSort().cast(lrright[1])
            
            samestate=Implies(p[s][1][i][j],p[s+1][1][i][j])
            poss=Or(And(samestate,Not(lrleft[1]),Not(lrright[1])),And(Not(samestate),(lrleft[1]),Not(lrright[1])),And(Not(samestate),Not(lrleft[1]),(lrright[1])))
            Q.add(poss)
            
            atleast=Or(atleast,lrleft[1],lrright[1])

        for i in vertical:  

            nvs[s+1][j][i]=IntSort().cast(p[s+1][0][j][i])
            tv+=nvs[s+1][j][i]

            lrleft=list(pvup(s,j,i))
            lrright=list(pvdown(s,j,i))
            Q.add(lrleft[0])
            Q.add(lrright[0])
            
            movessum+=IntSort().cast(lrleft[1])
            movessum+=IntSort().cast(lrright[1])

            samestate=Implies(p[s][0][j][i],p[s+1][0][j][i])
            poss=Or(And(samestate,Not(lrleft[1]),Not(lrright[1])),And(Not(samestate),(lrleft[1]),Not(lrright[1])),And(Not(samestate),Not(lrleft[1]),(lrright[1])))
            Q.add(poss)
            
            atleast=Or(atleast,lrleft[1],lrright[1])
            
        for i in range(n):
            tm+=IntSort().cast(p[s+1][2][j][i])
            if [i,j] in mine:
                Q.add(p[s][2][i][j])

    che=Or(che,p[s+1][3][red_loc[0]][n-2])
    Q.add(atleast)
    Q.add(tr==1)
    Q.add(th==h)
    Q.add(tv==v)
    Q.add(tm==lm)
    Q.add(movessum==1)
Q.add(che)
Qsat=Q.check()


if Qsat==sat:
    m=Q.model()
    for j in range(n):
            if j>=1:
                if p[0][3][red_loc[0]][j] and  is_true(m[p[1][3][red_loc[0]][j-1]]):
                    print(red_loc[0],j,sep=",")
            if j<n-2:
                if  p[0][3][red_loc[0]][j] and  is_true(m[p[1][3][red_loc[0]][j+1]]):   
                    print(red_loc[0],j+1,sep=",") 
            for i in horizontal:
                if j>=1:
                    if p[0][1][i][j] and  is_true(m[p[1][1][i][j-1]]):
                        print(i,j,sep=",")
                if j<n-2:
                    if  p[0][1][i][j] and  is_true(m[p[1][1][i][j+1]]):   
                        print(i,j+1,sep=",") 
            for i in vertical:
                if j>=1:
                    if p[0][0][j][i] and  is_true(m[p[1][0][j-1][i]]):
                        print(j,i,sep=",")
                if j<n-2:
                    if p[0][0][j][i] and  is_true(m[p[1][0][j+1][i]]) :   
                        print(j+1,i,sep=",") 
    for s in range(limit):
        if is_true(m[p[s][3][red_loc[0]][n-2]]):
            break
        for j in range(n):
            if j>=1:
                if is_true(m[p[s][3][red_loc[0]][j]]) and  is_true(m[p[s+1][3][red_loc[0]][j-1]]):
                    print(red_loc[0],j,sep=",")
            if j<n-2:
                if  is_true(m[p[s][3][red_loc[0]][j]]) and  is_true(m[p[s+1][3][red_loc[0]][j+1]]):   
                    print(red_loc[0],j+1,sep=",") 
            for i in horizontal:
                if j>=1:
                    if is_true(m[p[s][1][i][j]]) and  is_true(m[p[s+1][1][i][j-1]]):
                        print(i,j,sep=",")
                if j<n-2:
                    if  is_true(m[p[s][1][i][j]]) and  is_true(m[p[s+1][1][i][j+1]]):   
                        print(i,j+1,sep=",") 
            for i in vertical:
                if j>=1:
                    if is_true(m[p[s][0][j][i]]) and  is_true(m[p[s+1][0][j-1][i]]):
                        print(j,i,sep=",")
                if j<n-2:
                    if is_true(m[p[s][0][j][i]]) and  is_true(m[p[s+1][0][j+1][i]]) :   
                        print(j+1,i,sep=",")
        
else:
    print("unsat")
          
        





    

    

        










