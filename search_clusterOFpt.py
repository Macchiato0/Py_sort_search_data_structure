#collect data of lines and pts
fid='092101'

where="feederid='{}'".format(fid)

cursor=arcpy.da.SearchCursor(r'E:\Data\yfan\Connection to dgsep011.sde\ELECDIST.ElectricDist\ELECDIST.ServicePoint',["OID@","SHAPE@"],where+" and DEVICELOCATION is Null")
sp=[[i[0],i[1]] for i  in cursor]

cursor=arcpy.da.SearchCursor(r'E:\Data\yfan\Connection to dgsep011.sde\ELECDIST.ElectricDist\ELECDIST.Transformer',["SHAPE@","TLM"],where)
trans=[i for i in cursor]

cursor=arcpy.da.SearchCursor(r'E:\Data\yfan\Connection to dgsep011.sde\ELECDIST.ElectricDist\ELECDIST.SecOHElectricLineSegment'
,["SHAPE@"],where)
SecOH=[i[0] for i in cursor]

cursor=arcpy.da.SearchCursor(r'E:\Data\yfan\Connection to dgsep011.sde\ELECDIST.ElectricDist\ELECDIST.SecUGElectricLineSegment',["SHAPE@"],where)
SecUG=[i[0] for i in cursor]

all_line=SecOH+SecUG

#all_l=[i for i in all_line]
#shapes=sp[0][1]

def dist(geo1,geo2):
  p1=[geo2.firstPoint,geo2.lastPoint]
  result=0
  for i in p1:
      if geo1.distanceTo(i)==0:
        result+=1
  return result
    
    
#find one and delet one
def find_near(geo,lines):#geo is a line or point
  result=[]
  for j in lines:
    if j.>0: 
      result.append(j)
      lines.remove(j)
  return result

#find_near(shapes,all_line)
'''
pseudo-code

network=[]
r=find_near(shp,lines)
network+=r  
for i in r:
  r=find_near(shp,lines)
  network+=r  
  for i in r:
    r=find_near(shp,lines)
    network+=r
    until r is empty
'''
    
network=[]          
def create_network(lines,*shps):# * make a single item iterable
    global network
    sub=[]
    for i in shps:
      r=find_near(i,lines)
      if r:
        sub+=r      
    if sub:  
      network+=sub  
    if not sub:
      return network
    create_network(lines,*sub)# * make sub (i.e. list) iterable 
    
#network=[]     
#create_network(all_line,shapes)
#all_line=[i for i in all_l]
'''
* make a single or multiple single item iterable
* make a list iterable 
* arg needs placed as the last argument in a function
'''
def search_tlm(line,tlm_list):
  for i in tlm_list:
    if line.distanceTo(i[0])==0:
      return i[1]

sp_tlm=[]
for i in sp:
  network=[] 
  create_network(all_line,i[1])
  for j in network:
    t=search_tlm(j,trans)
    if t:
      break
  s_t=[i[0],t] 
  sp_tlm.append(s_t)
  

      
  
