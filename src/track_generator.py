import pygame
import math
from typing import Tuple
from src.config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    COLOR_GRASS,
    COLOR_ASPHALT,
    COLOR_BORDER,
    COLOR_OBSTACLE_VISUAL,
    COLOR_GRASS_MASK,
    WAYPOINT_COLORS,
    COLOR_ASPHALT_MASK
)

class TrackGenerator:
    def __init__(self):
        # Definição dos pontos que formam o traçado da pista
        self.points = [
            (100, 100),
            (600, 50),
            (1100, 100),
            (1200, 300),
            (1100, 600),
            (700, 500),
            (600, 650),
            (200, 600),
            (50, 350) 
        ]
        
        # Lista de obstáculos: (x, y, raio)
        self.obstacles = [
            (600, 50, 30),
            (1180, 250, 40),
            (900, 550, 25),
            (400, 620, 35),
            (150, 350, 20)
        ]
        
        self.track_width = 140

    def generate(self) -> Tuple[pygame.Surface, pygame.Surface, Tuple[int, int], float]:
        # 1. Cria as superfícies vazias
        visual_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        visual_surface.fill(COLOR_GRASS) # Fundo Verde

        mask_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        mask_surface.fill(COLOR_GRASS_MASK) # Máscara Verde (Morte)

        # 2. Desenha o Asfalto (Base)
        if len(self.points) > 2:
            # Borda Branca (Zebra)
            pygame.draw.lines(visual_surface, COLOR_BORDER, True, self.points, self.track_width + 20)
            # Asfalto Cinza
            pygame.draw.lines(visual_surface, COLOR_ASPHALT, True, self.points, self.track_width)
            
            # Desenha círculos nos vértices para suavizar as curvas
            for point in self.points:
                pygame.draw.circle(visual_surface, COLOR_BORDER, point, (self.track_width // 2) + 10)
                pygame.draw.circle(visual_surface, COLOR_ASPHALT, point, self.track_width // 2)

            # Desenha a Máscara Lógica (Onde o carro pode andar)
            pygame.draw.lines(mask_surface, COLOR_ASPHALT_MASK, True, self.points, self.track_width)
            for point in self.points:
                pygame.draw.circle(mask_surface, COLOR_ASPHALT_MASK, point, self.track_width // 2)

        # 3. Desenha Obstáculos
        for obs in self.obstacles:
            # Visual: Marrom com borda preta
            pygame.draw.circle(visual_surface, COLOR_OBSTACLE_VISUAL, (obs[0], obs[1]), obs[2])
            pygame.draw.circle(visual_surface, (0,0,0), (obs[0], obs[1]), obs[2], 3)
            
            # Máscara: Verde (Morte)
            pygame.draw.circle(mask_surface, COLOR_GRASS_MASK, (obs[0], obs[1]), obs[2])

        # 4. Desenha Linha de Chegada e Waypoints
        for i in range(len(self.points)):
            p1 = self.points[i]
            p2 = self.points[(i + 1) % len(self.points)]
            
            # Matemática para achar a perpendicular (largura da pista)
            dx = p2[0] - p1[0]
            dy = p2[1] - p1[1]
            angle = math.atan2(dy, dx)
            
            mid_x = (p1[0] + p2[0]) / 2
            mid_y = (p1[1] + p2[1]) / 2
            
            perp_angle = angle + math.pi / 2
            line_len = self.track_width
            
            start_line = (
                mid_x + math.cos(perp_angle) * (line_len / 2),
                mid_y + math.sin(perp_angle) * (line_len / 2)
            )
            end_line = (
                mid_x - math.cos(perp_angle) * (line_len / 2),
                mid_y - math.sin(perp_angle) * (line_len / 2)
            )

            # --- Desenha na MÁSCARA (Lógica Invisível) ---
            color_idx = i % len(WAYPOINT_COLORS)
            color = WAYPOINT_COLORS[color_idx]
            pygame.draw.line(mask_surface, color, start_line, end_line, 12) # Linha grossa para o sensor pegar bem
            
            # --- Desenha no VISUAL (O que a gente vê) ---
            if i == 0:
                # === LINHA DE CHEGADA QUADRICULADA ===
                # Divide a linha em vários segmentos para criar o xadrez
                checkers = 8 # Número de quadrados
                diff_x = (end_line[0] - start_line[0]) / checkers
                diff_y = (end_line[1] - start_line[1]) / checkers
                
                for j in range(checkers):
                    c_start = (start_line[0] + diff_x * j, start_line[1] + diff_y * j)
                    c_end = (start_line[0] + diff_x * (j+1), start_line[1] + diff_y * (j+1))
                    
                    # Alterna entre Preto e Branco
                    c_color = (255, 255, 255) if j % 2 == 0 else (0, 0, 0)
                    pygame.draw.line(visual_surface, c_color, c_start, c_end, 15)
            else:
                # Desenha uma linha cinza bem clarinha só para ver onde são os setores
                pygame.draw.line(visual_surface, (80, 80, 80), start_line, end_line, 2)

        # 5. Calcula posição inicial do carro
        start_p1 = self.points[0]
        start_p2 = self.points[1]
        dx = start_p2[0] - start_p1[0]
        dy = start_p2[1] - start_p1[1]
        angle_rad = math.atan2(dy, dx)
        start_angle = -math.degrees(angle_rad)
        
        # Posiciona um pouco antes da linha de chegada
        start_pos = (
            int(start_p1[0] + math.cos(angle_rad) * 50),
            int(start_p1[1] + math.sin(angle_rad) * 50)
        )

        return visual_surface, mask_surface, start_pos, start_angle