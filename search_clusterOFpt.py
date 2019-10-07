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

def find_near(shp,lines):
  result=[]
  for j in lines:
    if shp.distanceTo(j)==0: 
      result.append(j)
      lines.remove(j)
      return result
    
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
    
    
#create_network(all_line,shapes)
#all_line=[i for i in all_l]
'''
* make a single or multiple single item iterable
* make a list iterable 
* arg needs placed as the last argument in a function
