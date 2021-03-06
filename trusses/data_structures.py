# Braeden Conrad

# Data structures to be used for solving trusses

# Class that represents a degree of freedom
class Dof:
	def __init__(self,val,disp=None,force=None):
		# value of location in space
		self.val = val
		# displacement after loads are applied
		self.disp = disp
		# force in each degree of freedom on each node
		self.force = force
		# give unique id to dof
		self.id = None
	# determine that a dof is equal by checking that unique id is same
	def __eq__(self,dof):
		return self.id == dof.id
	# when converted to string, returns the unique id and the displacement
	def __str__(self):
		return "id = "+str(self.id)+"\tdisp = "+str(self.disp)+"\tval= "+str(self.val)

# Class the represents a node
class Node:
	def __init__(self,val1,val2,val3=None):
		if val3==None:
			self.dof1 = Dof(val1)
			self.dof2 = Dof(val2)
			self.dofs = [self.dof1,self.dof2]
		else:
			# 3 degrees of freedom option
			self.dof1 = Dof(val1)
			self.dof2 = Dof(val2)
			self.dof3 = Dof(val3)
			self.dofs = [self.dof1,self.dof2,self.dof3]
	def __str__(self):
		string = ''
		for dof in self.dofs:
			string+=str(dof)+'\n'
		return string

# Class that represents an element
class Ele:
	def __init__(self,node1,node2,E,A,I=None,three_dof=False):
		# local nodes
		self.node1 = node1
		self.node2 = node2
		self.nodes = [self.node1,self.node2]
		# find the length
		if three_dof:
			self.length = ((self.node1.dof1.val-self.node2.dof1.val)**2 +
						(self.node1.dof2.val-self.node2.dof2.val)**2 +
						(self.node1.dof3.val-self.node2.dof3.val)**2)**.5
		else:
			self.length = ((self.node1.dof1.val-self.node2.dof1.val)**2 +
						(self.node1.dof2.val-self.node2.dof2.val)**2)**.5
		print (self.length)
		# Young's modulus, cross sectional area, and I for the element
		self.E = E
		self.A = A
		# only applicable for frames
		self.I = I
		# Find the cos and sin for the element
		self.cos = (self.node2.dof1.val-self.node1.dof1.val)/self.length
		self.sin = (self.node2.dof2.val-self.node1.dof2.val)/self.length
		if three_dof:
			# have to find angle for the z dimension
			self.caz = (self.node2.dof3.val-self.node1.dof3.val)/self.length
		# local degrees of freedom
		self.dofs = []
		for node in self.nodes:
			for dof in node.dofs:
				self.dofs.append(dof)
		# strain in the element
		self.strain = None
		# stress in the element
		self.stress = None
		# force in the element
		self.force = None
	# method that returns ldof index of specific dof
	def get_index_dof(self,dof):
		for i in range(len(self.dofs)):
			if dof == self.dofs[i]:
				return i

	# when converted to a string this is what is returned
	def __str__(self):
		string = ''
		i = 1
		for node in self.nodes:
			string += "Node "+str(i)+"\n"+str(node)
			i += 1
		return string