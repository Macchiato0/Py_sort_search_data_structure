#create a list of tlm as start point of a rout
pt_start=[i for i in pt_shp if 'tlm' in i]

#data structure of route
#rout [id,(line1,line2,line3),(point1,point2,point3)]

'''
lines=[(1,2),(2,3),(3,4),(3,5),(2,12),(4,6),(6,7),(7,8),(8,100),(100,101),(10,11)]
p=[1,10]

lines1=[i for i in lines]
'''

result=[]
def connect(lines,p):
  global result
  match=[]
  for i in lines:
    if i[0]==p:
      match.append(i)
  if len(match)>0:    
    result.append(match)
  #print match
  for k in match:
    lines.remove(k)
  for j in match: 
    return connect(lines,j[1])

 
# connect(lines,1)
# result is a 2nd network
'''
def grow(p,l):
  branch=[]
  for i in l:
    if p[1]==i[0]:
      row=[p,i]
      branch.append(row)
  return branch


def route(lists):
  iter=range(len(lists)-1)
  for i in iter:
    for j in lists[i]:
      branch=grow (j,lists[i+1])
      print branch
'''

#tier start at 0, tier = idx of t, t is tuple representing a line

def neighbor(t,lists):
  nei=[]
  for i in lists:
    if i[0]==t[1]:
      nei.append(i)
  return nei
    
  
#neighbor((1, 2),[(2, 3), (2, 12)])      

tier=range(len(result)-1)

result1=[i for i in result]

tree=[]

for i in tier:
  tree.append(result[i])
  for t in result[i]:
    l=result[i+1]
    branch=neighbor(t,l)
    bb=[]
    for b in branch:
      bb.append([t,b])
    tree[i].append(bb)
    for d in tree[i]
      branch1=neighbor(d[1],result[i+1])
      for e in branch: 
        tree[i][
      
        
      
  
