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
	for u in u_sol:
		print(str(u)+"PL/AE")
main()