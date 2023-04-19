import  mySokobanSolver
import sokoban

warehouse = sokoban.Warehouse()
path = "warehouses\warehouse_8a.txt"
warehouse.load_warehouse(path)

solver = mySokobanSolver.solve_weighted_sokoban(warehouse)
print(solver.expanded_actionSequences[len(solver.expanded_actionSequences)-1])
print(solver.expanded_states[len(solver.expanded_states)-1])
#print(solver.unexpanded_actionSequences)
#print(solver.hueristic)


