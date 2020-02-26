import main
import solve
import genetic
import importlib
import sys

importlib.reload(main)
importlib.reload(solve)
importlib.reload(genetic)

main.main(sys.argv[1])