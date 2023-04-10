import  mySokobanSolver
import sokoban

warehouse = sokoban.Warehouse()
warehouse.load_warehouse("warehouses\warehouse_71.txt")

solver = mySokobanSolver.SokobanPuzzle(warehouse)


print(warehouse)
mySokobanSolver.move_worker(warehouse,"Left")
mySokobanSolver.move_worker(warehouse,"Up")


print("moved")




print(warehouse)