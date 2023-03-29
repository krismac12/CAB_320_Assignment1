import  mySokobanSolver;
import sokoban;

warehouse = sokoban.Warehouse()
warehouse.load_warehouse("warehouses\warehouse_5n.txt")

solver = mySokobanSolver.SokobanPuzzle(warehouse)
actions = solver.actions(warehouse.copy())

print(actions)