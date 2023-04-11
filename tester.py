import  mySokobanSolver
import sokoban

warehouse = sokoban.Warehouse()
warehouse.load_warehouse("warehouses\warehouse_8b.txt")

mySokobanSolver.move_worker(warehouse,"Left")


solved_boxes = mySokobanSolver.assign_boxes_to_targets(warehouse.boxes,warehouse.targets,warehouse.weights)



print(warehouse)

solver = mySokobanSolver.SokobanPuzzle(warehouse)

mySokobanSolver.move_worker(warehouse,"Left")
mySokobanSolver.move_worker(warehouse,"Up")
mySokobanSolver.move_worker(warehouse,"Right")
mySokobanSolver.move_worker(warehouse,"Right")

print(warehouse)

print(warehouse.boxes)
print(solved_boxes)

if solved_boxes == warehouse.boxes:
    print("Solved")
