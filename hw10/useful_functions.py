import data_structures as ds
from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt
import numpy as np

# function reads three input files to completely fill info for all dofs
def create_nodes(node_file_name,disp_file_name,
					force_file_name):
	nodes = []
	node_file = open(node_file_name,'r')
	# read the total num nodes
	node_file.readline()
	for line in node_file:
		# input files have tabs
		vals = line.strip().split('  ')[1:]
		# append node to list of nodes
		nodes.append(ds.Node(float(vals[0]),float(vals[1])))
	node_file.close()
	# read displacements and add the knowns in
	disp_file = open(disp_file_name,'r')
	disp_file.readline()
	for line in disp_file:
		vals = line.strip().split('  ')
		if len(vals)<3:
			continue
		# input the displacement into the corresponding dof
		nodes[int(vals[0])-1].dofs[int(vals[1])-1].disp = float(vals[2])
	disp_file.close()
	# finally read forces and input into nodes
	force_file = open(force_file_name,'r')
	force_file.readline()
	for line in force_file:
		vals = line.strip().split('  ')
		if len(vals)<3:
			continue
		# known forces are input into the corresponding dof
		nodes[int(vals[0])-1].dofs[int(vals[1])-1].force = float(vals[2])
	force_file.close()
	return nodes

# function reads input file and returns a list of elements
def create_eles(file_name,nodes):
	eles = []
	ele_file = open(file_name,'r')
	first_line = ele_file.readline()
	E,Nu = first_line.strip().split('  ')[1:]
	for line in ele_file:
		vals = line.strip().split('  ')[1:]
		if (len(vals)<3):
			continue
		eles.append(ds.Ele(nodes[int(vals[0])-1], nodes[int(vals[1])-1], nodes[int(vals[2])-1], 
							float(E), float(Nu)))
	ele_file.close()
	return eles

# function plots the elements
def plot_elements(truss,deformed=False,ext=''):
	plt.figure()
	plt.axis('equal')
	plt.xlabel('x')
	plt.ylabel('y')
	if deformed:
		plt.title('Deformed Elements')
	else:
		plt.title('Undeformed Elements')
	# for each element, add the points of the each node
	for ele in truss.eles:
		points = []
		for node in ele.nodes:
			coord = []
			for dof in node.dofs:
				if deformed:
					coord.append(dof.val+dof.disp)
				else:
					coord.append(dof.val)
			points.append(coord)
		points = np.array(points)
		# now get the Convex Hull for the points
		hull = ConvexHull(points)
		# plot the simple triangle shape
		for simplex in hull.simplices:
			plt.plot(points[simplex, 0], points[simplex, 1], 'k-')
	if deformed:
		plt.savefig('elements_def'+ext+'.png')
	else:
		plt.savefig('elements'+ext+'.png')

# function for plotting stress
def plot_stresses(truss,ext=''):
	x_vals = []
	y_vals = []
	stress_vals_x = []
	stress_vals_y = []
	stress_valsx = []
	stress_valsy = []
	# go through each element
	for ele in truss.eles:
		count_x0 = 0
		count_y0 = 0
		flag_y0 = False
		flag_x0 = False
		# if there are 2 y values equal to zero, it's one we use for plotting
		for node in ele.nodes:
			if node.dof2.val+node.dof2.disp == 0:
				count_y0+=1
				if (count_y0 > 1):
					# first element is the x component of stress
					stress_vals_x.append(ele.stress[0])
					stress_valsy.append(ele.stress[1])
					flag_y0 = True
					break
			if node.dof1.val+node.dof1.disp == 0:
				count_x0+=1
				if (count_x0 > 1):
					# second element is the y component of stress
					stress_vals_y.append(ele.stress[1])
					stress_valsx.append(ele.stress[0])
					flag_x0 = True
					break
		# if element has two nodes at y=0
		if flag_y0:
			for node in ele.nodes:
				# find the node not at y=0 and use that x value at that node
				if node.dof2.val+node.dof2.disp != 0:
					x_vals.append(node.dof1.val+node.dof1.disp)
		# if element has two nodes at x=0
		if flag_x0:
			for node in ele.nodes:
				# find the node not a x=0 and use that y value at that node
				if node.dof1.val+node.dof1.disp != 0:
					y_vals.append(node.dof2.val+node.dof2.disp)
	x_vals = np.array(x_vals)
	y_vals = np.array(y_vals)
	stress_vals_y = np.array(stress_vals_y)
	stress_vals_x = np.array(stress_vals_x)
	stress_valsy = np.array(stress_valsy)
	stress_valsx = np.array(stress_valsx)
	# now plot the x values
	plt.figure()
	plt.xlabel('x')
	plt.ylabel('Sigma (stress)')
	plt.plot(x_vals, stress_vals_x,'-o',label='sigma(xx)')
	plt.plot(x_vals, stress_valsy,'-o',label='sigma(yy)')
	plt.legend()
	plt.savefig('stress_x'+ext+'.png')

	# and the y values
	plt.figure()
	plt.xlabel('y')
	plt.ylabel('Sigma (stress)')
	plt.plot(y_vals, stress_vals_y,'-o', label='sigma(xx)') 
	plt.plot(y_vals, stress_valsx,'-o', label='sigma(yy)')
	plt.legend()
	plt.savefig('stress_y'+ext+'.png')
