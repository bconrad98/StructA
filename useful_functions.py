import data_structures as ds
# useful functions for reading files

def create_nodes(node_file_name,disp_file_name,
					force_file_name):
	nodes = []
	node_file = open(node_file_name,'r')
	node_file.readline()
	for line in node_file:
		vals = line.strip().split('\t')[1:]
		if len(vals)<2:
			continue
		nodes.append(ds.Node(float(vals[0]),float(vals[1])))
	node_file.close()
	# read displacements and add the knowns in
	disp_file = open(disp_file_name,'r')
	disp_file.readline()
	for line in disp_file:
		vals = line.strip().split('\t')
		if len(vals)<3:
			continue
		nodes[int(vals[0])-1].dofs[int(vals[1])-1].disp = float(vals[2])
	disp_file.close()
	# finally read forces and input into nodes
	force_file = open(force_file_name,'r')
	force_file.readline()
	for line in force_file:
		vals = line.strip().split('\t')
		if len(vals)<3:
			continue
		nodes[int(vals[0])-1].dofs[int(vals[1])-1].force = float(vals[2])
	force_file.close()
	return nodes

def create_eles(file_name,nodes):
	eles = []
	ele_file = open(file_name,'r')
	ele_file.readline()
	for line in ele_file:
		vals = line.strip().split('\t')[1:]
		if (len(vals)<4):
			continue
		eles.append(ds.Ele(nodes[int(vals[0])-1],
						nodes[int(vals[1])-1],
						float(vals[2]),float(vals[3])))
	ele_file.close()
	return eles