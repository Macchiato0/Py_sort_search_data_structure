#create a list of tlm as start point of a rout
#pt list structure:
pt_start=[i for i in pt_shp if 'tlm' in i]

#data structure of route
#rout [id,(line1,line2,line3),(point1,point2,point3)]


#grow function to identify the linked lines
def grow_nodes(n,layers):
  l1=layers[n]
  l2=layers[n+1]
  nodes=[]
  for i in l1:
    for j in l2:
      if i[0] in j or i[1] in j:
        branch=[i,j]
        nodes.append(branch)
  return nodes 



#l=grow_nodes(0,layers)
#ll=grow_nodes(1,layers)

#n1,n2 should not empty
#n1 is the upper layer


#merge the nodes and create all feasible routes
def merge_branch(n1,n2):    
  if len(n2):
    nodes=[]
    for i in n1:
      b=[]
      for j in n2:
        if i[-1] in j:
          b=i+[j[-1]]
          nodes.append(b) 
      if not b:
        nodes.append(i)      
    return nodes

'''
l=grow_nodes(0,layers)
ll=grow_nodes(1,layers) 
lll=merge_branch(l,ll)
llll=[[i] for i in layers[3]] 
f=merge_branch(lll,llll)
''''

#execution of the code to get routes file
tier_l=range(len(layers))
for i in tier_l:
  if i==0:
    l=grow_nodes(0,layers)
    ll=grow_nodes(1,layers)
    lll=merge_branch(l,ll)
  elif i <len(layers)-2:#1,2,3,4,5,6,7
    llll=grow_nodes(i+1,layers)
    lll=merge_branch(lll,llll)
  else:
    nodes=[]
    for m in lll:
      b=[]
      for j in layers[i]:
        if [k for k in m[-1] if k in m]:
          b=m+[j]
          nodes.append(b)
      if not b:
        nodes.append(m)
 
'''
example data structure
layers=[[(1,2),(1,3),(1,4)],[(2,12),(6,4),(7,3),(3,5)],[(7, 8), (9, 7)],[(8,100),(9,11)],[(100,101)],[(102,101),(103,101)],[(103,14)],[(14,15),(16,14),(14,17)],[(16,21),(17,25)],[(25,33),(26,25)]]
layers=[[[553, 868], [553, 422], [553, 375], [553, 609], [553, 12], [553, 843]],[[375, 623], [375, 764], [868, 542], [609, 814], [868, 399], 
[609, 888], [12, 101], [868, 879], [12, 475], [12, 323], [843, 322], [843, 709]],
[[764, 747], [709, 134], [709, 298], [764, 167], [879, 862], [709, 104], [879, 518], [764, 860], [709, 216], [888, 353]],
[[747, 11], [747, 247]]]
