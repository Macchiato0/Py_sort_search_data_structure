def insertion_sort(A):
#sort from right to left
    for i in range(1,len(A)):
        j=i-1
        while A[j]>A[j+1] and j>0:
            A[j],A[j+1]=A[j+1],A[j]
            j=j-1
            
