import numpy as np 

#===============================================================================
# Class for solving frame structures
#===============================================================================
class FrameSolver:

	# ==========================================================================
	# eles - list of Element objects for the system
	# nodes - list of Node objects for the system
	# ==========================================================================
	def __init__(self,eles,nodes,three_dim=False):
		self.eles = eles
		self.nodes = nodes
		self.dofs = []
		# flag that indicates three dimensions
		self.three_dim = three_dim
		if self.three_dim:
			self.num_dof = 4
		else:
			self.num_dof = 3
		# assign values for id's to each unique dof
		i = 0
		for node in nodes:
			for dof in node.dofs:
				dof.id = i
				self.dofs.append(dof)
				i += 1

	# ==========================================================================
	# Method for solving for the unknown displacements in a system
	# return u_sol - nparray with the solutions
	# ==========================================================================
	def solve(self):
		# moves boundary condition dofs to end
		self.__reorder_dofs()
		# get number of boundary conditions
		ndbcs = self.__get_ndbcs()
		# this value changes based on number of dimensions
		n = self.num_dof*len(self.nodes)-ndbcs
		K_red = np.zeros((n,n))
		F_red = np.zeros((n,1))
		# fill f_red with the known forces
		for dof in self.dofs:
			if dof.force!=None:
				index = self.__get_gcon_dof(dof)
				F_red[index] = dof.force
		# assemble the reduced stiffness matrix
		[K_red,F_red] = self.__assemble_stiffness(K_red,F_red,n)
		u_sol = np.linalg.inv(K_red).dot(F_red)
		# fill the dofs with displacements in u_sol
		i = 0
		for dof in self.dofs:
			if dof.disp == None:
				dof.disp = float(u_sol[i])
				i+=1
		return u_sol

	# ==========================================================================
	# Method reorders the list of dofs so that the dof with known displacements
	# are at the end. (Identical to doing gcon)
	# ==========================================================================
	def __reorder_dofs(self):
		# get list of the boundary dofs
		bound_dofs = []
		for i in range(len(self.dofs)):
			# if a boundary condition
			if self.dofs[i].disp!=None:
				bound_dofs.append(self.dofs[i])
		# reorder for each boundary cond
		for dof in bound_dofs:
			# get index of boundary dof
			i = self.__get_gcon_dof(dof)
			# move this dof to end, ones before stay same, after get moved down 1
			self.dofs = self.dofs[0:i]+self.dofs[i+1:]+[self.dofs[i]]

	#===========================================================================
	# Method takes in empty K_red and F_red and returns them with correct vals
	#===========================================================================
	def __assemble_stiffness(self,K_red,F_red,n):
		# loop through each element
		for ele in self.eles:
			# call to internal method for creating local stiffness
			K_loc = self.__get_k_local(ele)
			# loop through each pair of dofs(dof_i,dof_j)
			for dof_i in ele.dofs:
				# uses 2 different methods to find the local and global index
				ldof_i = ele.get_index_dof(dof_i)
				gdof_i = self.__get_gcon_dof(dof_i)
				# this row is a known displacement, so skip it
				if gdof_i>=n:
					continue
				for dof_j in ele.dofs:
					ldof_j = ele.get_index_dof(dof_j)
					gdof_j = self.__get_gcon_dof(dof_j)
					# if outside K_red, it has to be a known displacement
					# consequence of reordering self.dofs
					if gdof_j>=n:
						# move the known displacement to the other side
						F_red[gdof_i] -= K_loc[ldof_i][ldof_j]*self.dofs[gdof_j].disp
					else:
						# inside K_red so add corresponding local element
						K_red[gdof_i][gdof_j] += K_loc[ldof_i][ldof_j]
		return K_red,F_red

	#===========================================================================
	# Method returns a local stiffness matrix for a given element
	# arg ele - Element object that find K_loc for
	#===========================================================================
	def __get_k_local(self,ele):
		# m is dimension of K_local (total degrees of freedom)
		m = len(ele.dofs)
		c = ele.cos
		s = ele.sin
		if self.three_dim:
			# 3D still needs to be updated
			R = np.zeros((m,m))
			angle_mat = R.transpose().dot(K).dot(R)
		else:
			R = np.zeros((m,m))
			# rotation matrix for 2D
			R[:3,:3] = [[c,s,0],[-s,c,0],[0,0,1]]
			R[3:,3:] = [[c,s,0],[-s,c,0],[0,0,1]]
			# derived K local for horizontal orientation
			a = ele.E*ele.A/ele.length	 # EA/L
			b = 2*ele.E*ele.I/ele.length # 2EI/L
			c = 2*b 					 # 4EI/L
			d = 3*b/ele.length			 # 6EI/L^2
			e = 2*d/ele.length			 # 12EI/L^3
			K = [[a,0,0,-a,0,0],
				 [0,e,d,0,-e,d],
				 [0,d,c,0,-d,b],
				 [-a,0,0,a,0,0],
				 [0,-e,-d,0,e,-d],
				 [0,d,b,0,-d,c]]
			K_loc = R.transpose().dot(K).dot(R)
		return K_loc

	#===========================================================================
	# Method returns number of boundary conditions(known displacements)
	# NOTE: this method cannnot be used correctly after using frame.solve()
	#===========================================================================
	def __get_ndbcs(self):
		num = 0
		# go through each node, if displacement already has a val, it is known
		for node in self.nodes:
			for dof in node.dofs:
				if (dof.disp != None):
					num+=1
		return num

	#===========================================================================
	# Method gets index of specific dof in self.dofs() (this is gcon)
	#===========================================================================
	def __get_gcon_dof(self,dof):
		for i in range(len(self.dofs)):
			if (dof == self.dofs[i]):
				return i

	#===========================================================================
	# Method does post processing to find strains, stresses, and forces
	#===========================================================================
	def post_process(self):
		# find the strain,stress,force in each bar
		for ele in self.eles:
			# this only works for 2D
			u1 = ele.node1.dof1.disp
			u2 = ele.node2.dof1.disp
			v1 = ele.node1.dof2.disp
			v2 = ele.node2.dof2.disp
			if self.three_dim:
				w1 = ele.node1.dof3.disp
				w2 = ele.node2.dof3.disp
				ele.strain = (u2-u1)*ele.cos/ele.length + \
							(v2-v1)*ele.sin/ele.length + \
							(w2-w1)*ele.caz/ele.length
			else:
				ele.strain = (u2-u1)*ele.cos/ele.length + \
							(v2-v1)*ele.sin/ele.length 
			ele.stress = ele.E*ele.strain
			ele.force = ele.A*ele.stress
			# set external forces that are still None to zero
			for dof in ele.dofs:
				if dof.force == None:
					dof.force = 0.0
			# find external forces on the nodes
			ele.node1.dof1.force -= ele.force*ele.cos
			ele.node1.dof2.force -= ele.force*ele.sin
			ele.node2.dof1.force += ele.force*ele.cos
			ele.node2.dof2.force += ele.force*ele.sin
			if self.three_dim:
				ele.node1.dof3.force -=ele.force*ele.caz
				ele.node2.dof3.force +=ele.force*ele.caz