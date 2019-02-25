import numpy as np 
import data_structures

class TrussSolver:
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


	def solve(self):
		# moves boundary condition dofs to end
		self.__reorder_dofs()
		# get number of boundary conditions
		ndbcs = self.__get_ndbcs()
		n = 2*len(self.nodes)-ndbcs
		K_red = np.zeros((n,n))
		F_red = np.zeros((n,1))
		# Fill F_red with the known forces
		i = 0
		for node in self.nodes:
			for dof in node.dofs:
				if dof.force!=None:
					F_red[i] = dof.force
					i+=1
		# assemble the reduced stiffness
		[K_red,F_red] = self.__assemble_stiffness(K_red,F_red,n)
		u_sol = np.linalg.inv(K_red).dot(F_red)
		return u_sol

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


	def __assemble_stiffness(self,K_red,F_red,n):
		# loop through each element
		i = 0
		for ele in self.eles:
			K_loc = self.__get_k_local(ele)
			for node_i in ele.nodes:
				for dof_i in node_i.dofs:
					ldof_i = ele.get_index_dof(dof_i)
					gdof_i = self.__get_gcon_dof(dof_i)
					#print (gdof_i)
					if gdof_i>=n:
						continue
					for node_j in ele.nodes:
						for dof_j in node_j.dofs:
							ldof_j = ele.get_index_dof(dof_j)
							gdof_j = self.__get_gcon_dof(dof_j)
							#print(gdof_j)
							# if outside K_red, it has to be a known displacement
							# consequence of reordering self.dofs
							if gdof_j>=n:
								F_red[gdof_i] -= K_loc[ldof_i][ldof_j]*self.dofs[gdof_j].disp
							else:
								K_red[gdof_i][gdof_j] += K_loc[ldof_i][ldof_j]
		return K_red,F_red

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

	# return number of boundary conditions(knowns)
	def __get_ndbcs(self):
		num = 0
		for node in self.nodes:
			for dof in node.dofs:
				if (dof.disp != None):
					num+=1
		return num

	# get index of specific dof in self.dofs()
	def __get_gcon_dof(self,dof):
		for i in range(len(self.dofs)):
			if (dof == self.dofs[i]):
				return i

