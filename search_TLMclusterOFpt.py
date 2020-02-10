'094602','156201','156202','114701','114702','151901','151902','151903','041501','041502','041503','041701','041702','067201','067602','010601','010602','010603'

#collect data of lines and pts



fid="('041502','041503')"

'''
'''

where="feederid in {}".format(fid)

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

all_l=[i for i in all_line]
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
def search_tlm(line_list,tlm_list):
  for i in tlm_list:
    for l in line_list:
      if i[0].distanceTo(l)==0:
        return i[1]


sp_tlm=[]
for i in sp:
  network=[] 
  all_line=[a_l for a_l in all_l]
  create_network(all_line,i[1])
  print len(network), i[0]
  t=search_tlm(network,trans)
  if not t:
      print i[0], "N"
      continue #continue can skip over the part of a loop where an external condition is triggered
  s_t=[i[0],t] 
  sp_tlm.append(s_t)
         
         
workspace = r'E:\Data\yfan\Connection to dgsep011.sde'
edit = arcpy.da.Editor(workspace)
edit.startEditing(False, True)
edit.startOperation() 
for i in sp_tlm:    
  where1="OBJECTID={}".format(i[0])
  cursor=arcpy.da.UpdateCursor(r'E:\Data\yfan\Connection to dgsep011.sde\ELECDIST.ElectricDist\ELECDIST.ServicePoint',["TLM"],where1)
  for row in cursor:
    row[0]=str(i[1])
    cursor.updateRow(row)
edit.stopOperation()

[i[0] for i in sp_tlm]

# import move_a2b(a,b)
# Function to move point A to point B based on oid, a an b are oid of points.
# Point A is remove/delet
# Point B is null Devicelocation
# If tlm of spA without devicelocation == tlm of spB remove/deleted ==> move(sp.A, sp.B)
# If len(spA) or len(spB) > 0 ==> create a for loop
'''
create spA, create spB
    
for i in len[spA]:
  if spB[i]:
    move(spA[i],spB[i])  
    
'''
cursor=arcpy.da.SearchCursor(r'E:\Data\yfan\Connection to dgsep011.sde\ELECDIST.ElectricDist\ELECDIST.ServicePoint',["OID@","TLM"],where+" and DEVICELOCATION is Null")

sp_tlm=[list(i) for i in cursor]

tlm_list= list(set([i[1] for i in sp_tlm]))
del_sp=[]
moved_sp=[]
for i in tlm_list:
  where2="TLM ='{}' and CONSTRUCTIONSTATUS=55".format(i)
  cursor=arcpy.da.SearchCursor(r'E:\Data\yfan\Connection to dgsep011.sde\ELECDIST.ElectricDist\ELECDIST.ServicePoint',["OID@"],where2+" and CONSTRUCTIONSTATUS = 55")
  list_a=[p[0] for p in cursor]
  list_b=[b[0] for b in sp_tlm if b[1]==i]       
  if list_a and list_b:
    for n in range(len(list_a)):
      if n<len(list_b):
        move_a2b(list_a[n],list_b[n])
        del_sp.append(list_b[n])
        moved_sp.append(list_a[n])        
print "del_added: {}".format(del_sp)      
print "moved_sp: {}".format(moved_sp)      
        
  
# Solve the sp on the inconsistant tlm  

  
