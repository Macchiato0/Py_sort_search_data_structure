def linear_search(search_list, target_value):
  matches =[]
  for idx in range(len(search_list)):
    if search_list[idx][1] == target_value:
      matches.append(idx)
  if matches:
    return matches

#tlm_shp
n=0
for i in tlm_shp:
  target=i[1]
  result=linear_search(pt_shp,target)
  if not result:
    n+=1
  else:
    row=['tlm',i[0]]	
    pt_shp[result].extend(row)
