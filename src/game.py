import pygame
import sys
import neat
from typing import List, Any
from src.car import Car
from src.config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS
)
from src.track_generator import TrackGenerator

class Simulation:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 25)
        
        generator = TrackGenerator()
        # Guarda o número de waypoints para saber o que é "uma volta completa"
        self.total_waypoints = len(generator.points)
        self.visual_map, self.mask_map, self.start_pos, self.start_angle = generator.generate()
        self.generation = 0

    def run_generation(self, genomes: List[Any], config: neat.Config) -> None:
        self.generation += 1
        nets = []
        cars = []
        ge = []

        for _, genome in genomes:
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            nets.append(net)
            cars.append(Car('assets/car.png', self.start_pos, self.start_angle))
            genome.fitness = 0
            ge.append(genome)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            alive_cars = 0
            for i, car in enumerate(cars):
                if car.alive:
                    alive_cars += 1
                    output = nets[i].activate(car.get_data())
                    choice = output.index(max(output))
                    car.action(choice)
                    
                    car.update(self.mask_map)
                    
                    # Fitness: Recompensa checkpoints e pune a demora
                    ge[i].fitness = (car.checkpoints_passed * 500) + (car.time_since_last_checkpoint / 10)
                    
                    # Opcional: Se quiser parar quando alguém completar X voltas
                    if car.checkpoints_passed > self.total_waypoints * 3:
                        running = False

            if alive_cars == 0:
                running = False
                break

            self._draw_window(cars)

    def _draw_window(self, cars: List[Car]) -> None:
        self.screen.blit(self.visual_map, (0, 0))
        
        for car in cars:
            if car.alive:
                car.draw(self.screen)
        
        # Texto da Geração
        text_gen = self.font.render(f"Gen: {self.generation}", True, (255, 255, 255))
        self.screen.blit(text_gen, (10, 10))
        
        # --- ALTERAÇÃO AQUI: Contagem de Carros que Cruzaram a Linha ---
        if cars:
            # Conta quantos carros completaram pelo menos 1 volta (passaram por todos os waypoints)
            finished_count = 0
            for c in cars:
                if c.checkpoints_passed >= self.total_waypoints:
                    finished_count += 1
            
            # Exibe o contador
            text_finished = self.font.render(f"Finalistas: {finished_count}", True, (255, 255, 255))
            self.screen.blit(text_finished, (10, 40))
        
        pygame.display.flip()
        self.clock.tick(FPS)