import math

class NUM:
	'Used for NUMS manipulation'
	def __init__(self):
		self.min = float('inf')
		self.max = -float('inf')
		self.arr = []
		self.mean = 0.0
		self.sd = 0.0
		
	def update(self,x):
		self.arr.append(x)
		self.max = max(self.max,x)
		self.min = min(self.min,x)
		
		n = len(self.arr)+1
		old_mean = self.mean
		
		self.mean = (old_mean*1.0) + ((x-old_mean)/n)
		
		variance = ( ((n-1)*self.sd*self.sd) + (x-old_mean)*(x-self.mean) )/n
		
		self.sd = math.sqrt(variance)*1.0
		
	def normalize(self,x):
		y = ((x-self.min)*1.0)/(self.max-self.min)
		return y
		
if __name__ == '__main__':
	num = NUM()
	
	arr = [1,2,3,444,56]
	
	for x in arr:
		num.update(x)
	print num.arr, num.min, num.max, num.mean, num.sd
	