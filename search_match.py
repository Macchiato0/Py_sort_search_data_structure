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

def find_OH(sp_shp):
  pt=sp_shp.firstPoint
  for j in SecOH:
    lp=j.lastPoint
    if lp.X==pt.X and lp.Y==pt.Y:
      SecOH.remove(j)
      i.append(j)

def find_UG(sp_shp):      
  pt=sp_shp.firstPoint
  for j in SecUG:
    lp=j.lastPoint
    if lp.X==pt.X and lp.Y==pt.Y:
      SecUG.remove(j)
      i.append(j)
      
for i in sp:
  

