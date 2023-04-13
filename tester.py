import  mySokobanSolver
import sokoban

warehouse = sokoban.Warehouse()
warehouse.load_warehouse("warehouses\warehouse_01_a.txt")

solver = mySokobanSolver.solve_weighted_sokoban(warehouse)
print(solver.current)
index = solver.expanded_states.index(solver.current)
print(solver.expanded_actionSequences[index])

#print(solver.unexpanded_actionSequences)
#print(solver.hueristic)


