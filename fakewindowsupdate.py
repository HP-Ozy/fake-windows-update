import pygame
import sys
import math
import time
import random

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Windows Update")
pygame.mouse.set_visible(False)

BG_COLOR = (0, 120, 215)
WHITE = (255, 255, 255)
LIGHT_BLUE = (100, 180, 255)


font_big = pygame.font.SysFont("Segoe UI", 42, bold=False)
font_medium = pygame.font.SysFont("Segoe UI", 28)
font_small = pygame.font.SysFont("Segoe UI", 20)

clock = pygame.time.Clock()
start_time = time.time()
percentage = 0
target_percentage = 0
phase = 0
last_phase_change = start_time

phases = [
    "Preparazione aggiornamento in corso...",
    "Download degli aggiornamenti...",
    "Installazione degli aggiornamenti...",
    "Configurazione di Windows...",
    "Applicazione delle impostazioni...",
    "Quasi fatto... Non spegnere il PC",
]

def draw_loading_circle(surface, center, radius, thickness, progress, color):
    start_angle = -math.pi / 2
    end_angle = start_angle + (2 * math.pi * progress)
    num_segments = max(int(100 * progress), 1)
    points = []
    for i in range(num_segments + 1):
        angle = start_angle + (end_angle - start_angle) * i / num_segments
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        points.append((x, y))
    if len(points) > 1:
        pygame.draw.lines(surface, color, False, points, thickness)

def draw_loading_dots(surface, center_x, center_y, t):
    num_dots = 5
    for i in range(num_dots):
        offset = (t * 2 + i * 0.35) % 3.0
        if offset < 1.5:
            x = center_x - 80 + (160 * (offset / 1.5))
            alpha = 255 if 0.2 < offset < 1.3 else 100
            size = 6
            dot_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(dot_surface, (*WHITE, alpha), (size, size), size)
            surface.blit(dot_surface, (x - size, center_y - size))

running = True
while running:
    dt = clock.tick(60) / 1000.0
    elapsed = time.time() - start_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            # ============================================
            #  PREMI  F4  PER CHIUDERE LA SCHERMATA
            # ============================================
            if event.key == pygame.K_F4:
                running = False
            
            if event.key == pygame.K_ESCAPE:
                pass  

    
    if elapsed - (last_phase_change - start_time) > random.uniform(6, 12):
        last_phase_change = time.time()
        phase = min(phase + 1, len(phases) - 1)

    if percentage < 99:
        speed = random.uniform(0.01, 0.15)
        
        if int(percentage) in [29, 30, 47, 48, 71, 72, 84, 85, 92, 93]:
            speed *= 0.02
        percentage = min(percentage + speed, 99.0)

    
    screen.fill(BG_COLOR)

    
    pct_text = f"{int(percentage)}%"
    pct_surface = font_big.render(pct_text, True, WHITE)
    pct_rect = pct_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60))
    screen.blit(pct_surface, pct_rect)

    
    draw_loading_circle(
        screen,
        (WIDTH // 2, HEIGHT // 2 - 60),
        radius=80,
        thickness=4,
        progress=percentage / 100.0,
        color=WHITE,
    )

    
    phase_text = phases[phase]
    phase_surface = font_medium.render(phase_text, True, WHITE)
    phase_rect = phase_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    screen.blit(phase_surface, phase_rect)

    
    draw_loading_dots(screen, WIDTH // 2, HEIGHT // 2 + 95, elapsed)

    
    warn_text = "Non spegnere il computer. L'operazione potrebbe richiedere alcuni minuti."
    warn_surface = font_small.render(warn_text, True, LIGHT_BLUE)
    warn_rect = warn_surface.get_rect(center=(WIDTH // 2, HEIGHT - 80))
    screen.blit(warn_surface, warn_rect)

    pygame.display.flip()

pygame.mouse.set_visible(True)
pygame.quit()
sys.exit()
