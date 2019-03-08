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
	# run the post processor
	truss.post_process()
	# print out all displacements in a pretty way
	print("All displacements in order:")
	node_num = 0
	for node in truss.nodes:
		node_num+=1
		dof_num=0
		for dof in node.dofs:
			dof_num+=1
			print("node:{:d}	dof:{:d}	disp:{:6.3f} PL/AE    force:{:6.3f}P".format(node_num,dof_num,dof.disp,dof.force))
	print ("Info for all elements:")
	ele_num = 0
	for ele in truss.eles:
		ele_num += 1
		print("ele:{:d}		strain:{:6.3f}	stress:{:6.3f}	force:{:6.3f}".format(ele_num,ele.strain,ele.stress,ele.force))
main()