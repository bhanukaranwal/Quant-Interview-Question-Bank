from collections import deque

class StackUsingQueue:
    def __init__(self):
        # We will use just one queue
        self.q = deque()

    def push(self, x):
        """
        Push element x onto stack.
        Insert x at the end of the queue, then rotate all previous elements behind it
        so that x comes to the front (simulating the top of the stack).
        """
        self.q.append(x)
        # Rotate the queue to bring the new element to the front
        for _ in range(len(self.q) - 1):
            # Remove from front and append to back
            self.q.append(self.q.popleft())
        # Now, the last pushed element is at the front

    def pop(self):
        """
        Removes the element on top of the stack and returns it.
        It's simply the front of the queue (because we've rotated the newly-pushed element to the front).
        """
        if not self.q:
            raise IndexError("pop from empty stack")
        return self.q.popleft()

    def top(self):
        """
        Get the top element (front of the queue).
        """
        if not self.q:
            raise IndexError("top from empty stack")
        return self.q[0]

    def empty(self):
        """
        Returns whether the stack is empty.
        """
        return len(self.q) == 0

# Example usage
stack = StackUsingQueue()
stack.push(1)
stack.push(2)
print(f"Top: {stack.top()}")   # Should print 2
print(f"Pop: {stack.pop()}")   # Should print 2
print(f"Empty: {stack.empty()}")  # Should print False
print(f"Pop: {stack.pop()}")   # Should print 1
print(f"Empty: {stack.empty()}")  # Should print True
