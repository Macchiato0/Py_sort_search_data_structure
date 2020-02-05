def selection_sort(arr):
    for i in range(0,len(arr)-1):
        minIndex=i
        for j in range(i+1,,len(arr)):
            if a[j]<arr[minIndex]:
                minIndex=j
        if minIndex != i:
            arr[i],arr[minIndex]=arr[minIndex],arr[i]
