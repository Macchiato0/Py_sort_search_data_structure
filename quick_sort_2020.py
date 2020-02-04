def partition(sorted_list,low,high)
    i=low
    pivot=sorted_list[high]
    for j in range(low,high):
        if sorted_list[j]<=pivot:
            sorted_list[j],sorted_list[i]=sorted_list[i],sorted_list[j]
            i += 1
    sorted_list[high],sorted_list[i]=sorted_list[i],sorted_list[high]
    return i

def quick_sort(sorted_list,low,high):
    if low<high:
        pi=partition(sorted_list,low,high)
        quick_sort(sorted_list,pi+1,high)
        quick_sort(sorted_list,low,pi-1)

low=0
high=len(sorted_list)-1
