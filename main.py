import TrussSolver as ts
import useful_functions as uf
import argparse

def main():
	# Add argument parser for easy command line use
	parser = argparse.ArgumentParser(description="Main file for solving truss structure")
	parser.add_argument('folder_path',help='The path to the directory containing displacements,elements,forces,nodes files')
	args = parser.parse_args()
	# get list of all the nodes from input files
	nodes = uf.create_nodes(args.folder_path+"/nodes.txt",
						 args.folder_path+"/displacements.txt",
						 args.folder_path+"/forces.txt")
	# get list of all elements from input files
	eles = uf.create_eles(args.folder_path+"/elements.txt",nodes)
	# get the truss object
	truss = ts.TrussSolver(eles,nodes)
	# solve for unkown displacements
	u_sol = truss.solve()
	# print out all displacements in a pretty way
	print("All displacements in order:")
	node_num = 0
	for node in truss.nodes:
		node_num+=1
		dof_num=0
		for dof in node.dofs:
			dof_num+=1
			print("node:{:d}	dof:{:d}	disp:{:6.3f} PL/AE".format(node_num,dof_num,dof.disp))
main()