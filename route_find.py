#create a list of tlm as start point of a rout
#pt list structure:
pt_start=[i for i in pt_shp if 'tlm' in i]

#data structure of route
#rout [id,(line1,line2,line3),(point1,point2,point3)]

'''
#basic algorithm and data structure of function connect

lines=[(1,2),(2,3),(3,4),(3,5),(2,12),(4,6),(6,7),(7,8),(8,100),(100,101),(10,11)]
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
'''
result=[]
def connect(lines,p):
  global result
  match=[]
  for i in lines:
    if i[1][0]==p:
      match.append(i)
  if len(match)>0:    
    result.append(match)
  #print match
  for k in match:
    lines.remove(k)
  for j in match: 
    return connect(lines,j[1])
  
#sec_network is a list of lists of lines. Each item in sec_network contains lines linked directly or indirectly to a transformer 
#line1=[i for i in line_shp]

sec_network=[] 
 
for i in pt_start:
  global result
  result=[]

connect(line1,680)
sec_network.append(result)
 
# connect(lines,1)
# result is a 2nd network of a transformer


#l is a line, lists is the line list

def neighbor(l,lists):
  nei=[]
  for i in lists:
    if i[0]==l[1]:
      nei.append(i)
  return nei
    
  
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



