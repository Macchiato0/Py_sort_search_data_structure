#Quick sort list of [id, (x,y)] tuple based on x


from random import randrange, shuffle 


def quicksort(list, start, end):
  # this portion of listay has been sorted
  if start >= end:
    return

  # select random element to be pivot
  pivot_idx = randrange(start, end + 1)
  pivot_element = list[pivot_idx][1][0]

  # swap random element with last element in sub-listay
  list[end], list[pivot_idx] = list[pivot_idx], list[end]

  # tracks all elements which should be to left (lesser than) pivot
  less_than_pointer = start
  
  for i in range(start, end):
    # we found an element out of place
    if list[i][1][0] < pivot_element:
      # swap element to the right-most portion of lesser elements
      list[i], list[less_than_pointer] = list[less_than_pointer], list[i]
      # tally that we have one more lesser element
      less_than_pointer += 1
  # move pivot element to the right-most portion of lesser elements
  list[end], list[less_than_pointer] = list[less_than_pointer], list[end]
  
  # Call quicksort on the "left" and "right" sub-lists
  quicksort(list, start, less_than_pointer - 1)
  quicksort(list, less_than_pointer + 1, end)

  
  
##################################
#example
#unsorted_list = [3,7,12,24,36,42]
#shuffle(unsorted_list)
#print(unsorted_list)

quicksort(sp_shp, 0, len(sp_shp) - 1)
quicksort(pt_shp, 0, len(pt_shp) - 1)
quicksort(tlm_shp, 0, len(tlm_shp) - 1)
