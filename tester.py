import  mySokobanSolver
import sokoban

warehouse = sokoban.Warehouse()
path = "warehouses\warehouse_15.txt"
warehouse.load_warehouse(path)

solver = mySokobanSolver.solve_weighted_sokoban(warehouse)

#solver = mySokobanSolver
#solver.taboo_cells(warehouse)
#print(mySokobanSolver.remove_taboo_state(warehouse))

#mySokobanSolver.taboo_cells(warehouse)
#print(mySokobanSolver.remove_taboo_state(warehouse))
#print(solver.unexpanded_actionSequences)
#print(solver.hueristic)
#print(mySokobanSolver.taboo_cells(warehouse))
#print(solver.initial)
#print(solver.initial)


print(solver)



