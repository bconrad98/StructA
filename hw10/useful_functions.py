import data_structures as ds
# useful functions for reading files

# function reads three input files to completely fill info for all dofs
def create_nodes(node_file_name,disp_file_name,
					force_file_name):
	nodes = []
	node_file = open(node_file_name,'r')
	# read the total num nodes
	node_file.readline()
	for line in node_file:
		# input files have tabs
		vals = line.strip().split(' ')[1:]
		# append node to list of nodes
		nodes.append(ds.Node(float(vals[0]),float(vals[1])))
	node_file.close()
	# read displacements and add the knowns in
	disp_file = open(disp_file_name,'r')
	disp_file.readline()
	for line in disp_file:
		vals = line.strip().split(' ')
		if len(vals)<3:
			continue
		# input the displacement into the corresponding dof
		nodes[int(vals[0])-1].dofs[int(vals[1])-1].disp = float(vals[2])
	disp_file.close()
	# finally read forces and input into nodes
	force_file = open(force_file_name,'r')
	force_file.readline()
	for line in force_file:
		vals = line.strip().split(' ')
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
	E,Nu = first_line.strip().split(' ')[1:]
	for line in ele_file:
		vals = line.strip().split(' ')[1:]
		if (len(vals)<3):
			continue
		eles.append(ds.Ele(nodes[int(vals[0])-1], nodes[int(vals[1])-1], nodes[int(vals[2])-1], E, Nu))
	ele_file.close()
	return eles