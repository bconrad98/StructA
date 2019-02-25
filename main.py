import TrussSolver as ts
import useful_functions as uf

def main():
	nodes = uf.create_nodes("test_input/nodes.txt",
						 "test_input/displacements.txt",
						 "test_input/forces.txt")
	eles = uf.create_eles("test_input/elements.txt",nodes)
	truss = ts.TrussSolver(eles,nodes)
	u_sol = truss.solve()
	print(u_sol)
main()