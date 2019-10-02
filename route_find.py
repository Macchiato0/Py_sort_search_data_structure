#create a list of tlm as start point of a rout
#pt list structure:
pt_start=[i for i in pt_shp if 'tlm' in i]

#data structure of route
#rout [id,(line1,line2,line3),(point1,point2,point3)]

#connect function sort linked lines into tiers
lines=[i for i in line_shp]

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
  
sec_network=[] 
lines=[i for i in line_shp] 
for t in pt_start:
  p=t[0]
  connect(p)
  sec_network.append(result)
  result=[]  
  
#the leftover items in lines are isolated lines
#grow function to identify the linked lines


def grow_nodes(n,layers):
  l1=layers[n]
  l2=layers[n+1]
  nodes=[]
  for i in l1: #i[1] is [p1,p2]
    for j in l2: #j[1] is [p1,p2]
      if i[1][0] in j[1] or i[1][1] in j[1]:
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
      for j in n2:#i[1] is [p1,p2]
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
def route_find(layers):
  tier_l=range(len(layers))
  nodes=[]
  for i in tier_l:
    if i==0:
      if len(layers)>2:
        l=grow_nodes(0,layers)
        ll=grow_nodes(1,layers)
        lll=merge_branch(l,ll)
      elif len(layers)==1:
        nodes=layers
      else:
        nodes=grow_nodes(0,layers)
    elif i <len(layers)-2:#1,2,3,4,5,6,7
      llll=grow_nodes(i+1,layers)
      lll=merge_branch(lll,llll)
    elif len(layers)>2:
      nodes=[]
      for m in lll:
        b=[]
        for j in layers[i]:
          if [k for k in m[-1] if k in m]:
            b=m+[j]
            nodes.append(b)
        if not b:
          nodes.append(m)
  return nodes 
'''
#test
r_l=route_find(layers)
for i in r_l:
    print [j[1] for j in i]
'''
#execute
sec_rout=[]

for i in sec_network:
  r_l=route_find(i)
  sec_rout.append(r_l)


#create data for route file
#basic structure [route_id,lines,pts,length]
'''  
id_n=0
for i in sec_rout:#i is a secondary network fed by a transformer 
  for j in i: #j is a route from a transformer to the end of the network
    a=[k[0] for k in j]
    b=[k[1] for k in j]
    for p in range(len(b)-1):
      if b[p][1]!=b[p+1][0]:
        b[p+1][0],b[p+1][1]=b[p+1][1],b[p+1][0]
    c=[k[0] for k in b]+[b[-1][1]]
    feet=sum([k[-1] for k in j])
    id_n+=1
    print id_n,a,c,feet


#add tlm to every route 
for i in sec_rout:
    for j in i:
        t_p=j[0][1][0]
        for s in pt_start:
            if s[0]==t_p:
                j.append(s[3])
                
'''                
file_name='E:\\Data\\yfan\\tlm_sec\\101route_{}.csv'.format(fid)
id_n=0
import csv 
with open(file_name, 'wb') as csvfile:
    filewriter = csv.writer(csvfile,delimiter=',',quotechar='"',quoting=csv.QUOTE_MINIMAL)
    for i in sec_rout:#i is a secondary network fed by a transformer 
      for j in i: #j is a route from a transformer to the end of the network
        a=[k[0] for k in j]
        b=[k[1] for k in j]
        for p in range(len(b)-1):
          if b[p][1]!=b[p+1][0]:
            b[p+1][0],b[p+1][1]=b[p+1][1],b[p+1][0]
        c=[k[0] for k in b]+[b[-1][1]]
        feet=sum([k[-1] for k in j])
        tlm_p=j[0][1][0]
        for s_tlm in pt_start: 
          if s_tlm[0]==tlm_p:
            w_tlm=s_tlm[3]
        #tl="'{}'".format(w_tlm)
        #print w_tlm
        id_n+=1
        row=[id_n,str(a),str(c),feet,"'{}'".format(w_tlm)]
        filewriter.writerow(row)    



file_name='E:\\Data\\yfan\\tlm_sec\\101pt_{}.csv'.format(fid)
import csv 
with open(file_name, 'wb') as csvfile:
    filewriter = csv.writer(csvfile,delimiter=',',quotechar='"',quoting=csv.QUOTE_MINIMAL)
    for i in pt_shp:
        x=i[1][0]
        y=i[1][1]
        row=[i[0],x,y]
        if len(i)<=2:
          filewriter.writerow(row)
        else:
          row=[i[0],x,y,i[2],"'{}'".format(i[3])] 
          filewriter.writerow(row)

          
file_name='E:\\Data\\yfan\\tlm_sec\\101line_{}.csv'.format(fid)
import csv 
with open(file_name, 'wb') as csvfile:
    filewriter = csv.writer(csvfile,delimiter=',',quoting=csv.QUOTE_MINIMAL)
    for i in line_shp:
        row=i
        filewriter.writerow(row)    
      
  
'''
#example data structure
layers=[[(1,2),(1,3),(1,4)],[(2,12),(6,4),(7,3),(3,5)],[(7, 8), (9, 7)],[(8,100),(9,11)],[(100,101)],[(102,101),(103,101)],[(103,14)],[(14,15),(16,14),(14,17)],[(16,21),(17,25)],[(25,33),(26,25)]]
layers=[[[553, 868], [553, 422], [553, 375], [553, 609], [553, 12], [553, 843]],[[375, 623], [375, 764], [868, 542], [609, 814], [868, 399], 
[609, 888], [12, 101], [868, 879], [12, 475], [12, 323], [843, 322], [843, 709]],
[[764, 747], [709, 134], [709, 298], [764, 167], [879, 862], [709, 104], [879, 518], [764, 860], [709, 216], [888, 353]],
[[747, 11], [747, 247]]]
