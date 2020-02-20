# A stack is a linear data structure that stores items in a Last-In/First-Out (LIFO) or First-In/Last-Out (FILO) manner. In stack, a new 
# element is added at one end and an element is removed from that end only. The insert and delete operations are often called push and 
# pop.

Python stack can be implemented using deque class from collections module. Deque is preferred over list in the cases where we need quicker append and pop operations from both the ends of the container, as deque provides an O(1) time complexity for append and pop operations as compared to list which provides O(n) time complexity.
Same methods on deque as seen in list are used, append() and pop().

# Python program to  
# demonstrate stack implementation 
# using collections.deque 
  
  
from collections import deque 
  
stack = deque() 
  
# append() function to push 
# element in the stack 
stack.append('a') 
stack.append('b') 
stack.append('c') 
  
print('Initial stack:') 
print(stack) 
  
# pop() fucntion to pop 
# element from stack in  
# LIFO order 
print('\nElements poped from stack:') 
print(stack.pop()) 
print(stack.pop()) 
print(stack.pop()) 
  
print('\nStack after elements are poped:') 
print(stack) 
  
# uncommenting print(stack.pop())   
# will cause an IndexError  
# as the stack is now empty 
