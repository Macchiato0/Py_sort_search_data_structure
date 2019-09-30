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
    result
  for k in match:
    lines.remove(k)
  for j in match: 
    return connect(lines,j[1])

  
def route(result,p):
  for i in result):
    
     
