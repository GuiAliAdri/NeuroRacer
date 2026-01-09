import neat
import os
from src.game import Simulation


def main() -> None:
    local_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(local_dir, "config-neat.txt")

    if not os.path.exists(config_path):
        return

    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path,
    )

    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    sim = Simulation()
    p.run(sim.run_generation, 100)


if __name__ == "__main__":
    main()
