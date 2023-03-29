import  mySokobanSolver
import sokoban
import gui_sokoban

warehouse = sokoban.Warehouse()
warehouse.load_warehouse("warehouses\warehouse_5n.txt")

solver = mySokobanSolver.SokobanPuzzle(warehouse)
actions = solver.actions(warehouse.copy())
print(warehouse)
print(actions)