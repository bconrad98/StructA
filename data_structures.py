# Braeden Conrad

# Data structures to be used for solving trusses

# Class that represents a degree of freedom
class Dof:
	def __init__(self,val,disp=None):
		# value of location in space
		self.val = val
		# displacement after loads are applied
		self.disp = disp
		# global connectivity value to be assigned later
		self.gcon = None

# Class the represents a node
class Node:
	def __init__(self,val1,val2,num_dofs=2):
		if num_dofs == 2:
			self.dof1 = Dof(val1)
			self.dof2 = Dof(val2)
			self.dofs = [self.dof1,self.dof2]
		else
			pass
	def __str__(self):
		return "x: "+str(val1)+"y: "+str(val2)+"\n u: "+str(self.dof1.disp)+"v: "+str(self.dof2.disp)


# Class that represents an element
class Ele:
	def __init__(self,node1,node2,E,A):
		self.node1 = node1
		self.node2 = node2
		self.nodes = [node1,node2]
		# find the length
		self.length = ((self.node1.dof1.val-self.node2.dof1.val)**2 +
						(self.node1.dof2.val-self.node2.dof2.val)**2)**.5
		# Young's modulus and cross sectional area
		self.E = E
		self.A = A
		# Find the cos and sin for the element
		self.cos = (self.node2.dof1.val-self.node1.dof1.val)/self.length
		self.sin = (self.node2.dof2.val-self.node1.dof2.val)/self.length
		
	def __str__(self):
		string = ''
		i = 1
		for node in self.nodes:
			string += "Node "+str(i)+"\n"+str(node)
			i += 1
		# TODO: add more info? E,A,L,cos,sin,displacements?
		return string