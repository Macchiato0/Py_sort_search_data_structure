#create a list of tlm as start point of a rout
#pt list structure:
pt_start=[i for i in pt_shp if 'tlm' in i]

#data structure of route
#rout [id,(line1,line2,line3),(point1,point2,point3)]

'''
#basic algorithm and data structure of function connect

lines=[(1,2),(2,3),(3,4),(2,12),(4,6),(6,7),(3,5),(7,8),(8,100),(100,101),(10,11)]
p=[1,10]

lines1=[i for i in lines]


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
    
connect(lines,1)
'''
#lines=[i for i in line_shp]
result=[]
def connect(*args):
  match=[]
  global lines
  global result
  for i in lines:
    if i[1][0] in args or i[1][1] in args:
      match.append(i)
  if len(match)>0: 
    result.append(match)
    for k in match:
      lines.remove(k)
    p1=[k[1][1] for k in match]
    p2=[k[1][0] for k in match]
    args=tuple(p1+p2)
    #print args
    return connect(*args)

      
#connect(194)
  
#sec_network is a list of lists of lines. Each item in sec_network contains lines linked directly or indirectly to a transformer 

#lines=[(i[1][0],i[1][1]) for i in line_shp]

sec_network=[] 
lines=[i for i in line_shp] 
for t in pt_start:
  p=t[0]
  connect(p)
  sec_network.append(result)
  result=[]

  
# result is a 2nd network of a transformer


#l is a line, lists is the line list

def neighbor(l,lists):
  near=[]
  for i in lists:
    if l[0] in i or l[1] in i:
      near.append(i)
  return near
    
  
#neighbor((1, 2),[(2, 3), (2, 12)])      

#result1=[i for i in result]

#grow the brachs(b) based on n of branchs,route the targe route the return is a list of new routes. 

def add_route(b,route):
  new_route=[]
  for i in b:
    r=[j for j in route]
    r.append(i)
    new_route.append(r)
  return new_route
  
  
#m is the number of branches of a tree shape 2nd network

nodes=[]
  
def next_node(tier,layers):
  global nodes
  if tier>=len(layers)-1:
    return nodes
  if tier==0:
    nodes.append(layers[0])
  for i in nodes:
    branch=neighbor(i[-1],layers[tier+1])
    if len(branch)==1:
      i.append(branch[0]) 
    if len(branch)>1:
      new=add_route(branch,i) 
      nodes.remove(i)
      nodes+=new
  return next_node(tier+1,layers)  


next_node(0,layers)

'''

layers=[[(1,2),(1,3),(1,4)],[(2,12),(6,4),(7,3),(3,5)],[(7, 8), (9, 7)],[(8,100),(9,11)],[(100,101)],[(102,101),(103,101)],[(103,14)],[(14,15),(16,14),(14,17)],[(16,21),(17,25)],[(25,33),(26,25)]]
