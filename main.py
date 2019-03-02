import TrussSolver as ts
import useful_functions as uf
import argparse

def main():
	parser = argparse.ArgumentParser(description="Main file for solving truss structure")
	parser.add_argument('folder',help='The name of the folder containing displacements,elements,forces,nodes')
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
			print("node:",node_num,"dof:",dof_num,"disp:",dof.disp," PL/AE")
main()