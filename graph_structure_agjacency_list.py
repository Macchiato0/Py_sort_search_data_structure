# load data from prod geodatabase
cursor=arcpy.da.SearchCursor(r"Primary Lines\Primary Overhead Conductor",["SHAPE@"],"FEEDERID='166303'")
line_oh=[i[0] for i in cursor]
#len(line_oh)
#631
cursor=arcpy.da.SearchCursor(r"Primary Lines\Primary Underground Conductor",["SHAPE@"],"FEEDERID='166303'")
line_ug=[i[0] for i in cursor]
#len(line_ug)
#2
cursor=arcpy.da.SearchCursor(r"Customers & Transformers\Transformer Connector Lines\OH Connector Line",["SHAPE@"],"FEEDERID='166303'")
line_oh_tlm=[i[0] for i in cursor]
#len(line_oh_tlm)
#349
cursor=arcpy.da.SearchCursor(r"Customers & Transformers\Transformer Connector Lines\UG Connector Line",["SHAPE@"],"FEEDERID='166303'")
line_ug_tlm=[i[0] for i in cursor]
#len(line_ug_tlm)
#1
# transform the lines into a list of edges composed by points index
# e.g. edges=[[0,2],[2,3],[3,5],[3,6],[6,7]]
# convert lines in to pts tuple
import copy
all_line= copy.deepcopy(line_oh + line_ug + line_oh_tlm + line_ug_tlm)

print len(all_line)

# make a list of edges

edges_0=[[i.firstPoint,i.lastPoint] for i in all_line]

edges_xy=[[[i[0].X,i[0].Y],[i[1].X,i[1].Y]] for i in edges_0]

edges_xy_tuple=[(tuple(i[0]),tuple(i[1])) for i in edges_xy]

#check duplicate:

len(set(edges_xy_tuple))==len(all_line)

pt_xy = []
for i in edges_xy:
    pt_xy.append(tuple(i[0]))
    pt_xy.append(tuple(i[1]))

len(set(pt_xy)) : 984

pt_id={}
for i,j in enumerate(list(set(pt_xy))):
    pt_id[i]=j

len(pt_id)

pt_id_key=list(pt_id.keys())
pt_id_value=list(pt_id.values())

edges_id=[]
for i in edges_xy_tuple:
    p0=i[0]
    ind0=pt_id_key[pt_id_value.index(p0)]
    p1=i[1]
    ind1=pt_id_key[pt_id_value.index(p1)]
    edges_id.append([ind0,ind1])

#check duplicate lines
#make sure q_id is empty
q_id=[]

for i in edges_id:
    for j in edges_id:
        if i==j:
            continue
        elif sum(i)==sum(j) and i[0]==j[1]:
            q_id.append(j)

print len(q_id)

# convert undirected to directed graph
# Python3 implementation of the approach 
# N verticies, M edges

M = copy.deepcopy(len(edges_id))
N = copy.deepcopy(len(pt_id))

print N,M
n, m = N,M

# start point is the substation recloser
cursor=arcpy.da.SearchCursor(r"Devices\Protective Devices & Switches\Dynamic Protective Device",["SHAPE@"],"FEEDERID='166303' and SUBSTATIONDEVICE='N'")
#find the p based on pt_id

start_p=966

# To store the graph 
# create an undirected graph

undirected_gr = [[] for i in range(N)] 

# To store edges 

edges = [] 

def add_edge(x, y):   
    undirected_gr[x].append(y) 
    undirected_gr[y].append(x) 
    edges.append([x, y])


for i in edges_id:
    add_edge(i[0],i[1])

print len(undirected_gr)

# To store colour of each vertex 
# To store the distance to the source

colour = ['black'] * N 
print len(colour)
distance =[9999] * N
print len(distance)

# Breath First Search Algorithm

distance[start_p]=0
colour[start_p]='red'

directed_gr=copy.deepcopy(undirected_gr)

print len(distance),len(colour),len(directed_gr)

qu=list() 
	
for v in directed_gr[start_p]:
    distance[v]=1
    qu.append(v)

while len(qu)>0:
    u=qu.pop(0)
    colour[u]='red'
    for v in undirected_gr[u]:
        if distance[v]<distance[u]:
            directed_gr[u].remove(v)
        elif colour[v]=='black':
            qu.append(v)
            if distance[v]>distance[u]+1:
                distance[v]=distance[u]+1
        
#find the point id (vertax) of transformer, fuse, dynamic protective device, and switch
FEEDERID='166303'

# find pt_id of transformers

cursor=arcpy.da.SearchCursor(r"Customers & Transformers\Secondary Transformers",["OID@","SHAPE@"],"FEEDERID='166303'")
tlm_oid=[]
tlm_shp=[]
for row in cursor:
    tlm_oid.append(row[0])
    shp_p=row[1].firstPoint
    tlm_shp.append((shp_p.X,shp_p.Y))

tlm=[0]*N

for i in tlm_shp:
    ind_1=pt_id_value.index(i)
    ind_2=pt_id_key[ind_1]
    tlm[ind_2]=tlm_oid[tlm_shp.index(i)] 

# find pt_id of fuses

cursor=arcpy.da.SearchCursor(r"Devices\Protective Devices & Switches\Fuse",["OID@","SHAPE@"],"FEEDERID='166303'")
fuse_oid=[]
fuse_shp=[]
for row in cursor:
    fuse_oid.append(row[0])
    shp_p=row[1].firstPoint
    fuse_shp.append((shp_p.X,shp_p.Y))

fuse=[0]*N
for i in fuse_shp:
    ind_1=pt_id_value.index(i)
    ind_2=pt_id_key[ind_1]
    fuse[ind_2]=fuse_oid[fuse_shp.index(i)] 

# find pt_id of dynamic prodective devices

cursor=arcpy.da.SearchCursor(r"Devices\Protective Devices & Switches\Dynamic Protective Device",["OID@","SHAPE@"],"FEEDERID='166303' and SUBSTATIONDEVICE='N'")

dpd_oid=[]
dpd_shp=[]
for row in cursor:
    dpd_oid.append(row[0])
    shp_p=row[1].firstPoint
    dpd_shp.append((shp_p.X,shp_p.Y))

dpd=[0]*N

for i in dpd_shp:
    ind_1=pt_id_value.index(i)
    ind_2=pt_id_key[ind_1]
    dpd[ind_2]=dpd_oid[dpd_shp.index(i)] 


# find the pt_id of switches

cursor=arcpy.da.SearchCursor(r"Devices\Protective Devices & Switches\Switch",["OID@","SHAPE@"],"FEEDERID='166303' and SWITCHSTATUS in (1,2)")
swc_oid=[]
swc_shp=[]
for row in cursor:
    swc_oid.append(row[0])
    shp_p=row[1].firstPoint
    swc_shp.append((shp_p.X,shp_p.Y))

swc=[0]*N

for i in swc_shp:
    ind_1=pt_id_value.index(i)
    ind_2=pt_id_key[ind_1]
    swc[ind_2]=swc_oid[swc_shp.index(i)] 

# generated all possibal route to an end
# if the end is a tlm, record every upstream devices

# make a dictionary of graph
gr_dict={}
for i in range(len(directed_gr)):
    gr_dict[i]=directed_gr[i]

ends=[k for k in gr_dict if gr_dict[k]==[]]


#s is start point

def pred(v):
    for k in gr_dict:
        if v in gr_dict[k]:
            return k
    if v==start_p:
        return -1

routes=[]
for i in ends:
    e=i
    r=[i]
    while e!=start_p:
        s=pred(e)
        r.append(s)
        e=s
    routes.append(r)

# match the tlm 
# if the routes has tl
