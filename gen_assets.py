import pygame
import os

def create_assets():
    # Cria a pasta assets se não existir
    if not os.path.exists("assets"):
        os.makedirs("assets")
        print("Pasta 'assets' criada.")

    # --- CRIA O CARRO (car.png) ---
    # Tamanho 30x30
    surf = pygame.Surface((30, 30), pygame.SRCALPHA)
    
    # Corpo do carro (Vermelho)
    pygame.draw.rect(surf, (255, 0, 0), (0, 5, 30, 20), border_radius=4)
    # Teto (Vermelho escuro)
    pygame.draw.rect(surf, (200, 0, 0), (5, 10, 20, 10))
    # Para-brisa (Azul claro)
    pygame.draw.rect(surf, (100, 200, 255), (20, 6, 5, 18))
    # Rodas (Pretas)
    pygame.draw.rect(surf, (0, 0, 0), (2, 0, 6, 6))   # TR
    pygame.draw.rect(surf, (0, 0, 0), (2, 24, 6, 6))  # BR
    pygame.draw.rect(surf, (0, 0, 0), (22, 0, 6, 6))  # TL
    pygame.draw.rect(surf, (0, 0, 0), (22, 24, 6, 6)) # BL
    
    # Salva
    pygame.image.save(surf, "assets/car.png")
    print("Arquivo 'assets/car.png' gerado com sucesso!")

if __name__ == "__main__":
    pygame.init()
    create_assets()
    pygame.quit()