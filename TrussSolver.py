import numpy as np 
import data_structures

#===============================================================================
# Class for solving truss structures
#===============================================================================
class TrussSolver:

	# ==========================================================================
	# eles - list of Element objects for the system
	# nodes - list of Node objects for the system
	# ==========================================================================
	def __init__(self,eles,nodes):
		self.eles = eles
		self.nodes = nodes
		self.dofs = []
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
		n = 2*len(self.nodes)-ndbcs
		K_red = np.zeros((n,n))
		F_red = np.zeros((n,1))
		# Fill F_red with the known forces
		for ele in self.eles:
			for dof in ele.dofs:
				if dof.force!=None:
					index = self.__get_gcon_dof(dof)
					F_red[index] = dof.force
		# assemble the reduced stiffness
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
		K_loc = np.zeros((m,m))
		c = ele.cos
		s = ele.sin
		# this angle matrix is different for 3D
		angle_mat = [[c**2,s*c,-c**2,-s*c],
					 [s*c,s**2,-s*c,-s**2],
					 [-c**2,-s*c,c**2,s*c],
					 [-s*c,-s**2,s*c,s**2]]
		for i in range(m):
			for j in range(m):
				K_loc[i][j] = ele.E*ele.A*angle_mat[i][j]/ele.length
		return K_loc

	#===========================================================================
	# Method returns number of boundary conditions(known displacements)
	# NOTE: this method cannnot be used correctly after using Truss.solve()
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