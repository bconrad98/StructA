import FrameSolver as fs
import useful_functions as uf
import argparse
import math

def main():
	# Add argument parser for easy command line use
	parser = argparse.ArgumentParser(description="Main file for solving truss structure")
	parser.add_argument('folder_path',help='The path to the directory containing displacements,elements,forces,nodes files')
	args = parser.parse_args()
	# get list of all the nodes from input files, frames have 3 degrees of freedom 
	nodes = uf.create_nodes(args.folder_path+"/nodes.txt",
						 args.folder_path+"/displacements.txt",
						 args.folder_path+"/forces.txt",
						 three_dof=True)
	# get list of all elements from input files, frames have three degrees of freedom and need I input
	eles = uf.create_eles(args.folder_path+"/elements.txt",nodes,three_dof=True,frame=True)
	# get the truss object
	frame = fs.FrameSolver(eles,nodes,three_dim=False)
	# solve for unkown displacements
	u_sol = frame.solve()
	# run the post processor
	frame.post_process()
	# print out all displacements in a pretty way
	print("All displacements in order:")
	node_num = 0
	for node in truss.nodes:
		node_num+=1
		dof_num=0
		for dof in node.dofs:
			dof_num+=1
			print("node:{:d}	dof:{:d}	disp:{:6.3E} PL/AE    force:{:6.3E} P".format(node_num,dof_num,dof.disp,dof.force))
	# print out info on all the elements
	print ("\nInfo for all elements:")
	ele_num = 0
	for ele in truss.eles:
		ele_num += 1
		print("ele:{:d}		strain:{:6.3E} P/EA	stress:{:6.3f} P/A	force:{:6.3f} P".format(ele_num,ele.strain,ele.stress,ele.force))
main()