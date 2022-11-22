import main
from main import run_simulation
from main import Car 

reload = main.Checkpointer()
population = reload.restore_checkpoint("./neat-checkpoint-15")
population.run(run_simulation, 1000)
