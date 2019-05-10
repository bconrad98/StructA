import TrussSolver as ts
import useful_functions as uf
import argparse
import math

def main():
	# Add argument parser for easy command line use
	parser = argparse.ArgumentParser(description="Main file for solving truss structure")
	parser.add_argument('folder_path',help='The path to the directory containing displacements,elements,forces,nodes files')
	args = parser.parse_args()
	# get list of all the nodes from input files
	extra = args.folder_path.strip().split('/')[2]
	nodes = uf.create_nodes(args.folder_path+"/nodes"+extra+".txt",
						 args.folder_path+"/displacements"+extra+".txt",
						 args.folder_path+"/forces"+extra+".txt")
	# get list of all elements from input files
	eles = uf.create_eles(args.folder_path+"/elements"+extra+".txt",nodes)
	# get the truss object
	truss = ts.TrussSolver(eles,nodes)
	# solve for unkown displacements
	u_sol = truss.solve()
	# run the post processor
	truss.post_process()
	# plot the elements
	#uf.plot_elements(truss,ext='_'+extra)
	# plot deformed elements
	#uf.plot_elements(truss,deformed=True,ext='_'+extra)
	# plot the stresses on x and y
	uf.plot_stresses(truss,ext='_'+extra)
	'''
	# print out all displacements in a pretty way
	print("All displacements in order:")
	node_num = 0
	for node in truss.nodes:
		node_num+=1
		dof_num=0
		for dof in node.dofs:
			dof_num+=1
			print("node:{:d}	dof:{:d}	disp:{:6.3E} PL/AE".format(node_num,dof_num,dof.disp))
	# print out info on all the elements
	print ("\nInfo for all elements:")
	ele_num = 0
	for ele in truss.eles:
		ele_num += 1
		#print("ele:{:d}		strain:{:6.3E} P/EA	stress:{:6.3f} P/A	force:{:6.3f} P".format(ele_num,ele.strain,ele.stress,ele.force))
		'''
main()