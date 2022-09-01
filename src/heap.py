from nodeClass import nodeClass

class heap:

	def __init__(self):
		self.empty = nodeClass(None, [0,0])
		self.size = 0
		self.Heap = [self.empty]
		

	def parent(self, pos):
		return pos//2

	def leftChild(self, pos):
		return 2 * pos

	def rightChild(self, pos):
		return (2 * pos) + 1
		
	
	def up(self, pos):		 
		while  self.parent(pos) > 0:
			if self.Heap[pos].f == self.Heap[self.parent(pos)].f:
				if self.Heap[pos].g > self.Heap[self.parent(pos)].g:
					self.Heap[pos], self.Heap[self.parent(pos)] = self.Heap[self.parent(pos)], self.Heap[pos]
			elif self.Heap[pos].f < self.Heap[self.parent(pos)].f:
				self.Heap[pos], self.Heap[self.parent(pos)] = self.Heap[self.parent(pos)], self.Heap[pos]
			pos = pos // 2


	def down(self, pos):
			while self.leftChild(pos) <= self.size:
				mc = self.min_node(pos)
				if self.Heap[pos].f == self.Heap[self.parent(pos)].f:
					if self.Heap[pos].g < self.Heap[self.parent(pos)].g:
						self.Heap[pos], self.Heap[mc] = self.Heap[mc], self.Heap[pos]
				elif self.Heap[pos].f > self.Heap[mc].f:
					self.Heap[pos], self.Heap[mc] = self.Heap[mc], self.Heap[pos]
				pos = mc


	def min_node(self, pos):
			if self.rightChild(pos) > self.size:
				return self.leftChild(pos)
			else:
				if self.Heap[self.leftChild(pos)].f == self.Heap[self.rightChild(pos)].f:
					if self.Heap[pos].g > self.Heap[self.parent(pos)].g:
						return self.leftChild(pos)
					else:
						return self.rightChild(pos)
				elif self.Heap[self.leftChild(pos)].f < self.Heap[self.rightChild(pos)].f:
					return self.leftChild(pos)
				else:
					return self.rightChild(pos)


	def search(self, node):
		if node in self.Heap:
			return True
		return False


	def rebuild(self, node):
		pos = self.Heap.index(node)
		self.Heap[pos] = node
		mc = self.min_node()

		if self.Heap[self.Heap.index(node)].f == self.Heap[mc].f:
			if self.Heap[self.Heap.index(node)].g > self.Heap[mc].g:
				self.up(pos)
			else:
				self.down(pos)
		if self.Heap[self.Heap.index(node)].f < self.Heap[mc].f:
			self.down(pos)
		else:
			self.up(pos)


	def insert(self, k):
		self.Heap.append(k)
		self.size += 1
		self.up(self.size)
	

	def pop(self):
		root = self.Heap[1]
		self.Heap[1] = self.Heap[self.size]
		*self.Heap, _ = self.Heap
		self.size -= 1
		self.down(1)
 
		return root



 
	

