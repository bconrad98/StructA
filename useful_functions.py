import data_structures
# useful functions for reading files

def create_nodes(node_file_name,disp_file_name,
					force_file_name):
	nodes = []
	node_file = open(nod_file_name,'r')
	node_file.readline()
	for line in node_file:
		vals = line.strip().split(' ')[1:]
		nodes.append(Node(int(val[0]),int(val[1])))
	node_file.close()
	# read displacements and add the knowns in
	disp_file = open(disp_file_name,'r')
	disp_file.readline()
	for line in disp_file:
		vals = line.strip().split(' ')
		# this is questionable, may need if statement
		nodes[int(val[0])-1].dofs[int(val[1])-1].disp = float(val[2])
	disp_file.close()
	# finally read forces and input into nodes
	force_file = open(force_file_name,'r')
	force_file.readline()
	for line in force_file:
		vals = line.strip().split(' ')
		nodes[int(val[0])-1].dofs[int(val[1])-1].force = float(val[2])
	force_file.close()
	return nodes

def create_eles(file_name,nodes):
	eles = []
	ele_file = open(file_name,'r')
	ele_file.readline()
	for line in ele_file:
		vals = line.strip().split(' ')[1:]
		eles.append(Ele(nodes[int(val[0]-1)],
						nodes[int(val[1]-1)],
						val[2],val[3]))
	ele_file.close()
	return eles