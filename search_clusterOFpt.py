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
#return 0 if not connected
#arcpy distancTo return distance between crossed lines as 0. 
#linked lines has 0 distance between line A and points on line B
    
#find one and delet one
def find_near(geo,lines):#geo is a line or point
  result=[]
  for j in lines:
    if dist(geo,j)>0: 
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
  s_t=[]
  del t

  
workspace = r'E:\Data\yfan\Connection to dgsep011.sde'
edit = arcpy.da.Editor(workspace)
edit.startEditing(False, True)
edit.startOperation() 
for i in sp_tlm:    
  where="OBJECTID={}".format(i[0])
  cursor=arcpy.da.UpdateCursor(r'E:\Data\yfan\Connection to dgsep011.sde\ELECDIST.ElectricDist\ELECDIST.ServicePoint',["TLM"],where)
  for row in cursor:
    row[0]=str(i[1])
    cursor.updateRow(row)
edit.stopOperation()


'''
[[2196087, u'1107364404'], [4156584, u'1106313209'], [4156590, u'1106313302'], [4156591, u'1106073203'], [4156597, u'1107131101'], [4156601, u'1106302201'], [4156606, u'1106282202'], [4156611, u'1107364403'], [4156612, u'1007021301'], [4156613, u'1107364414'], [4156623, u'1106313210'], [4156637, u'1107364342'], [4156638, u'1107364103'], [4156642, u'1106313301'], [4156583, u'1107363406'], [3388115, u'1107363406'], [4156346, u'1106303307'], [4156348, u'1106303307'], [4156349, u'1007011205'], [4156604, u'1107363404']]
'''
move_a2b(a,b)

#Function to move point A to point B based on oid, a an b are oid of points.
#point A is remove/delet
#point B is null Devicelocation

for i in sp_tlm:
  w="TLM ='{}' and CONSTRUCTIONSTATUS=55".format(i[1])
  cursor=arcpy.da.SearchCursor(r'E:\Data\yfan\Connection to dgsep011.sde\ELECDIST.ElectricDist\ELECDIST.ServicePoint',["OID@"],w)
    print [i[0] for i in cursor]
  

  
  
