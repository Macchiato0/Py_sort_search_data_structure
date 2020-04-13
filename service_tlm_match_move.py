def extract_data(fid):
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
    
