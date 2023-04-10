import  mySokobanSolver
import sokoban

warehouse = sokoban.Warehouse()
warehouse.load_warehouse("warehouses\warehouse_01.txt")

solver = mySokobanSolver.SokobanPuzzle(warehouse)


print("initial")
print(warehouse)
for warehouse in solver.unexpanded_states:
    print("new")
    print(warehouse)

print("sequences")
for sequence in solver.actionSequences:
    print("new")
    print(sequence)