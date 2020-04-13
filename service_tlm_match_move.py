import sys
sys.path.append('E:\\Data\\yfan\\PyModules')
import removed_to_added_sp

# update added sp with tlm and swap added sp with removed/deleted sp


# -*- coding: utf-8 -*-

# ---------------------------------------------------------------------------

# removed_to_added_sp.py

# Created on: 2020-04-05 13:29

# (Author by Yi Fan)

# Description: 

# Move removed servive point to added service point with same tlm based on feederid

# ---------------------------------------------------------------------------



# Import arcpy module






def extract_data(fid):
    import arcpy
    where="feederid in {}".format(fid)
    cursor=arcpy.da.SearchCursor(r'E:\Data\yfan\Connection to dgsep011.sde\ELECDIST.ElectricDist\ELECDIST.ServicePoint',["OID@","SHAPE@"],where+" and     DEVICELOCATION is Null")
    sp_result=[[i[0],(i[1].firstPoint.X,i[1].firstPoint.Y)] for i  in cursor]
    cursor=arcpy.da.SearchCursor(r'E:\Data\yfan\Connection to dgsep011.sde\ELECDIST.ElectricDist\ELECDIST.Transformer',["SHAPE@","TLM"],where)
    trans_result=[[i[1],(i[0].firstPoint.X,i[0].firstPoint.Y)] for i in cursor]
    cursor=arcpy.da.SearchCursor(r'E:\Data\yfan\Connection to dgsep011.sde\ELECDIST.ElectricDist\ELECDIST.SecOHElectricLineSegment',["SHAPE@"],where)
    SecOH=[i[0] for i in cursor]
    cursor=arcpy.da.SearchCursor(r'E:\Data\yfan\Connection to dgsep011.sde\ELECDIST.ElectricDist\ELECDIST.SecUGElectricLineSegment',["SHAPE@"],where)
    SecUG=[i[0] for i in cursor]
    sec_lines=SecOH+SecUG
    sec_lines=[[(i.firstPoint.X,i.firstPoint.Y),(i.lastPoint.X,i.lastPoint.Y)] for i in sec_lines]
    return sp_result,trans_result,sec_lines

def get_pt(edges):
    import functools 
    lines=[]
    p_s=list(set([functools.reduce(lambda x,y:x+y,edges)][0]))
    print 'number of points: ',len(p_s)
    hash_pts=dict([[p_s[n],n] for n in range(len(p_s))])
    print 'number of hash dict: ',len(hash_pts)
    pts_dict={}
    for k in hash_pts:
        pts_dict[hash_pts[k]]=k
    print 'number of pts: ',len(pts_dict)
    for i in edges:
        pt1=hash_pts[i[0]]
        pt2=hash_pts[i[1]]   
        line=[pt1,pt2] 
        lines.append(line)
    print 'number of lines: ',len(lines)
    return pts_dict,lines
    
def compare(a,b):
    if abs(a[0]-b[0])<=0.1: 
        if abs(a[1]-b[1])<=0.1:
            return 0 # a==b
        else:
            return 3 #a[0]==b[0],a[1]!=b[1]
    elif a[0]-b[0]>0.1:
        return 1 # a>b
    else:# a[0]-b[0]<-0.1:
        return 2 # a<b 
        
def binary_search(arr,key):
    low=0
    high=len(arr)-1
    while (low<=high):
        mid=(low+high)//2
        a1=arr[mid][1]
        a2=key
        a3=compare(a1,a2)
        if a3==0:
            return mid
        elif a3==3:
            for u in range(len(arr)):
                c=compare(arr[u][1],a2)  
                if c==0:
                    return u
            return -1
        elif a3==2:
            low=mid+1
        elif a3==1:
            high=mid-1                     
    return -1        

def convert_tlm(tlms,plist):
    tlm_n={}
    for i in tlms:
        n=binary_search(plist,i[1])
        if n!=-1:
            #print n,i[0]
            tlm_n[plist[n][0]]=i[0]
        #else:
            #print n,i[0] 
    return tlm_n

def convert_sp(sps,pts_list):  
    sps_n={}
    for i in sps:
        n=binary_search(pts_list,i[1])
        if n!=-1:
            sps_n[pts_list[n][0]]=i[0]
            #print n,i[0]
        #else:
            #print -1,i[0]
    return sps_n
    
    
def bsf_sec_network(start_points,gr,sp_n,points):
    import copy
    directed_g=copy.deepcopy(gr)
    revers_g = dict([(key,0) for key in points])
    sp_tl={}
    colour=['black'] * len(gr)    
    sec_ne={}
    qu=list()
    for key in start_points:
        rout=[key]
        revers_g[key]=0
        qu.append(key)
        while len(qu)>0:
            u=qu.pop(0)
            colour[u]='red'
            for v in gr[u]:
                if colour[v]=='black':
                    revers_g[v]=u
                    qu.append(v)
                    rout.append(v)
                    if v in sp_n: #sp_n is the point id match
                        sp_tl[sp_n[v]]=start_points[key]                            
                else:
                    directed_g[u].remove(v)
        sec_ne[start_points[key]]=rout
    return sec_ne,directed_g,revers_g,sp_tl
    
def update_tlm(s_t):
    import arcpy
    workspace = r'E:\Data\yfan\Connection to dgsep011.sde'
    edit = arcpy.da.Editor(workspace)
    edit.startEditing(False, True)
    edit.startOperation() 
    for key in s_t:    
        where1="OBJECTID={}".format(key)
        cursor=arcpy.da.UpdateCursor(r'E:\Data\yfan\Connection to dgsep011.sde\ELECDIST.ElectricDist\ELECDIST.ServicePoint',["TLM"],where1)
        for row in cursor:
            row[0]=str(s_t[key])
            cursor.updateRow(row)
    edit.stopOperation()

def move_a2b(a,b):
    import arcpy
    workspace = r'E:\Data\yfan\Connection to dgsep011.sde'
    edit = arcpy.da.Editor(workspace)
    edit.startEditing(False, True)
    edit.startOperation()
    where="OBJECTID={}".format(b)
    cursor=arcpy.da.SearchCursor(r'E:\Data\yfan\Connection to dgsep011.sde\ELECDIST.ElectricDist\ELECDIST.ServicePoint',["SHAPE@"],where)
    for row in cursor:
        pt=row[0]
    where="OBJECTID={}".format(a)
    cursor=arcpy.da.UpdateCursor(r'E:\Data\yfan\Connection to dgsep011.sde\ELECDIST.ElectricDist\ELECDIST.ServicePoint',["SHAPE@"],where)
    for row in cursor:
        row[0]=pt
        cursor.updateRow(row)
    edit.stopOperation()

def move(s_t):
    import arcpy
    del_sp=[]
    moved_sp=[]
    tlm_sp=dict([[s_t[key],[]] for key in s_t])
    for key in s_t:
        tlm_sp[s_t[key]].append(key)
    for key in tlm_sp:
        where2="TLM ='{}'".format(key)
        cursor=arcpy.da.SearchCursor(r'E:\Data\yfan\Connection to dgsep011.sde\ELECDIST.ElectricDist\ELECDIST.ServicePoint',["OID@"],where2+"and CONSTRUCTIONSTATUS = 55")
        list_a=[p[0] for p in cursor]         
        while len(list_a)>0 and len(tlm_sp[key])>0:
            p1=list_a.pop()
            p2=tlm_sp[key].pop()
            #print p1,p2
            moved_sp.append(p1)
            del_sp.append(p2)
            move_a2b(p1,p2)          
    print "del_added: {}".format(del_sp)      
    print "moved_sp: {}".format(moved_sp)  
    print "delete null=", len(del_sp)  
    print "moved removed sp=", len(moved_sp)    
    
def main(fid):
    sp_null,trans,all_l=extract_data(fid)  
    pts,edges=get_pt(all_l)
    pts_list=pts.items()#1s
    pts_list.sort(key=lambda r:r[1][0])#sort based on x value,1s

    trans.sort(key=lambda r:r[1][0])

    trans_pts=convert_tlm(trans,pts_list) 
    print "transformers: ",len(trans_pts)
    sp_null_pts=convert_sp(sp_null,pts_list)
    print "null service points: ",len(sp_null_pts)

    undirected_graph={}
    for key in pts:
        undirected_graph[key]=[]
    for i in edges:
        if i[1] not in undirected_graph[i[0]]:
            undirected_graph[i[0]].append(i[1])
        if i[0] not in undirected_graph[i[1]]:
            undirected_graph[i[1]].append(i[0]) 
 
    print "undirected_graph: ",len(undirected_graph)   

    sec_net,directed_gr,revers_gr,sp_tlm=bsf_sec_network(trans_pts,undirected_graph,sp_null_pts,pts)
    print sp_tlm
    update_tlm(sp_tlm)
    move(sp_tlm)
    
if __name__ == "__main__":    
    print __name__ 
