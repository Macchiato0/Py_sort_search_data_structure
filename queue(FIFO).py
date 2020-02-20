# Queue is a linear data structure that stores items in First In First Out (FIFO) manner.
# With a queue the least recently added item is removed first.

# Operations associated with queue are:
# Enqueue: Adds an item to the queue. If the queue is full, then it is said to be an Overflow condition 
# Dequeue: Removes an item from the queue.
# Front: Get the front item from queue 
# Rear: Get the last item from queue 

Implementation using collections.deque
Queue in Python can be implemented using deque class from the collections module. Deque is preferred over list in the cases where we need quicker append and pop operations from both the ends of container, as deque provides an O(1) time complexity for append and pop operations as compared to list which provides O(n) time complexity. Instead of enqueue and deque, append() and popleft() functions are used.

# Python program to 
# demonstrate queue implementation 
# using collections.dequeue 
  
  
from collections import deque 
  
# Initializing a queue 
q = deque() 
  
# Adding elements to a queue 
q.append('a') 
q.append('b') 
q.append('c') 
  
print("Initial queue") 
print(q) 
  
# Removing elements from a queue 
print("\nElements dequeued from the queue") 
print(q.popleft()) 
print(q.popleft()) 
print(q.popleft()) 
  
print("\nQueue after removing elements") 
print(q) 
  
# Uncommenting q.popleft() 
# will raise an IndexError 
# as queue is now empty 
