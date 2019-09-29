#match the sp and tlm to points on lines.
def binary_search(sorted_list, left_pointer, right_pointer, target,y):
  # this condition indicates we've reached an empty "sub-list"
  if left_pointer >= right_pointer:
    return "value not found"
	
  # We calculate the middle index from the pointers now
  mid_idx = (left_pointer + right_pointer) // 2
  mid_val = sorted_list[mid_idx][1][0]
  y_val = sorted_list[mid_idx][1][1]
	
  if mid_val == target and y==y_val:
    return mid_idx
  if mid_val > target:
    # we reduce the sub-list by passing in a new right_pointer
    return binary_search(sorted_list, left_pointer, mid_idx, target,y)
  if mid_val < target:
    # we reduce the sub-list by passing in a new left_pointer
    return binary_search(sorted_list, mid_idx + 1, right_pointer, target,y)

#######
#example
#values = [77, 80, 102, 123, 288, 300, 540]
#start_of_values = 0
#end_of_values = len(values)
#result = binary_search(values, start_of_values, end_of_values, 288)
###

for i in sp_shp:
  target=i[1][0]	
  lat=i[1][1]
  result=binary_search(pt_shp,0,len(pt_shp),target,lat)
  if type(result) is int:
    row=['sp',i[0]]	
    pt_shp[result].extend(row)
	
  
for i in tlm_shp:
  target=i[1][0]
  lat=i[1][1]
  result=binary_search(pt_shp,0,len(pt_shp),target,lat)
  if type(result) is int:
    row=['tlm',i[0]]	
    pt_shp[result].extend(row)
	
##########
'''test if rows in pt_shp have more than 4 items
for i in pt_shp:
  if len(i)>4:
    print i
