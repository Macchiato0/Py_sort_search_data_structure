def partition(sorted_list,low,high)
    i=low
    pivot=sorted_list[high]
    for j in range(low,high):
        if sorted_list[j]<=pivot:
            sorted_list[j],sorted_list[i]=sorted_list[i],sorted_list[j]
            i += 1
    sorted_list[high],sorted_list[low]=sorted_list[low],sorted_list[high]
    
    
