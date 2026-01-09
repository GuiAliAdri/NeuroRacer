import pygame
import math
from typing import List, Tuple
# ADICIONE O IMPORT DA NOVA COR AQUI
from src.config import (
    CAR_SIZE_X, CAR_SIZE_Y, SPEED, ROTATION_SPEED,
    SCREEN_WIDTH, SCREEN_HEIGHT, SENSOR_MAX_LENGTH, SENSOR_ANGLES,
    COLOR_GRASS_MASK, WAYPOINT_COLORS, COLOR_RAY_SENSOR, FPS
)

class Car:
    def __init__(self, sprite_path: str, start_pos: Tuple[int, int], start_angle: float):
        self.original_image = pygame.image.load(sprite_path).convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (CAR_SIZE_X, CAR_SIZE_Y))
        self.image = self.original_image
        self.rect = self.image.get_rect(center=start_pos)

        self.position = pygame.math.Vector2(start_pos[0], start_pos[1])
        self.angle = start_angle
        self.speed = SPEED
        
        self.alive = True
        self.radars = []
        
        self.current_checkpoint = 0
        self.checkpoints_passed = 0
        self.time_since_last_checkpoint = 0

    def update(self, game_map_mask: pygame.Surface) -> None:
        if not self.alive:
            return

        self._move()
        self._rotate()
        self._check_collision_and_waypoints(game_map_mask)
        self._update_radars(game_map_mask)
        
        self.time_since_last_checkpoint += 1
        if self.time_since_last_checkpoint > FPS * 6:
            self.alive = False

    def action(self, choice: int) -> None:
        if choice == 0:
            self.angle += ROTATION_SPEED
        elif choice == 1:
            self.angle -= ROTATION_SPEED

    def get_data(self) -> List[float]:
        return_values = [0.0] * 5
        for i, radar in enumerate(self.radars):
            return_values[i] = int(radar[1] / 30)
        return return_values

    # --- MÉTODO DRAW ATUALIZADO ---
    def draw(self, screen: pygame.Surface) -> None:
        # 1. Desenha o carro
        screen.blit(self.image, self.rect.topleft)
        
        # 2. Desenha os sensores (Raios)
        # Se o carro estiver vivo, mostramos o que ele está vendo
        if self.alive:
            for radar in self.radars:
                collision_point = radar[0]
                # Linha do centro até o ponto de colisão
                pygame.draw.line(screen, COLOR_RAY_SENSOR, self.rect.center, collision_point, 1)
                # Pequeno círculo na ponta para mostrar onde bateu
                pygame.draw.circle(screen, COLOR_RAY_SENSOR, collision_point, 3)
    # ------------------------------

    def _move(self) -> None:
        rad = math.radians(360 - self.angle)
        self.position.x += math.cos(rad) * self.speed
        self.position.y += math.sin(rad) * self.speed
        self.rect.center = (int(self.position.x), int(self.position.y))

    def _rotate(self) -> None:
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def _check_collision_and_waypoints(self, game_map_mask: pygame.Surface) -> None:
        rad = math.radians(360 - self.angle)
        offset = CAR_SIZE_X // 2
        check_x = int(self.position.x + math.cos(rad) * offset)
        check_y = int(self.position.y + math.sin(rad) * offset)

        if not (0 <= check_x < SCREEN_WIDTH and 0 <= check_y < SCREEN_HEIGHT):
            self.alive = False
            return

        try:
            pixel_color = game_map_mask.get_at((check_x, check_y))[:3]
            
            if pixel_color == COLOR_GRASS_MASK:
                self.alive = False
                return

            target_color = WAYPOINT_COLORS[self.current_checkpoint]
            
            if pixel_color == target_color:
                self.checkpoints_passed += 1
                self.time_since_last_checkpoint = 0
                self.current_checkpoint += 1
                if self.current_checkpoint >= len(WAYPOINT_COLORS):
                    self.current_checkpoint = 0
                
        except IndexError:
            self.alive = False

    def _update_radars(self, game_map_mask: pygame.Surface) -> None:
        self.radars.clear()
        for angle in SENSOR_ANGLES:
            length = 0
            x = 0
            y = 0
            while length < SENSOR_MAX_LENGTH:
                length += 10
                x = int(self.rect.center[0] + math.cos(math.radians(360 - (self.angle + angle))) * length)
                y = int(self.rect.center[1] + math.sin(math.radians(360 - (self.angle + angle))) * length)
                
                if not (0 <= x < SCREEN_WIDTH and 0 <= y < SCREEN_HEIGHT):
                    break
                try:
                    if game_map_mask.get_at((x, y))[:3] == COLOR_GRASS_MASK:
                        break
                except IndexError:
                    break
            
            dist = int(math.sqrt(math.pow(x - self.rect.center[0], 2) + math.pow(y - self.rect.center[1], 2)))
            self.radars.append(((x, y), dist))