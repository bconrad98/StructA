import TrussSolver as ts
import useful_functions as uf
import argparse

def main():
	parser = argparse.ArgumentParser(description="Main file for solving truss structure")
	parser.add_argument('folder',help='The path to the directory containing displacements,elements,forces,nodes files')
	args = parser.parse_args()
	nodes = uf.create_nodes(args.folder+"/nodes.txt",
						 args.folder+"/displacements.txt",
						 args.folder+"/forces.txt")
	eles = uf.create_eles(args.folder+"/elements.txt",nodes)
	truss = ts.TrussSolver(eles,nodes)
	u_sol = truss.solve()
	print("All displacements in order:")
	node_num = 0
	for node in truss.nodes:
		node_num+=1
		dof_num=0
		for dof in node.dofs:
			dof_num+=1
			print("node:{:d}	dof:{:d}	disp:{:6.3f} PL/AE".format(node_num,dof_num,dof.disp))
main()