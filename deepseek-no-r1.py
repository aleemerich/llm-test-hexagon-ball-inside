import pygame
import math
import sys

# Inicializa o Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bola Quicando em Hexágono Giratório")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Configurações da bola
ball_radius = 20
ball_pos = [WIDTH // 2, HEIGHT // 4]
ball_vel = [0, 0]  # Velocidade inicial
gravity = 0.5
friction = 0.99

# Configurações do hexágono
num_sides = 6
side_length = 200
rotation_speed = 0.02
angle = 0

def rotate_point(point, center, angle):
    """Rotaciona um ponto em torno de um centro por um ângulo."""
    x, y = point
    cx, cy = center
    dx = x - cx
    dy = y - cy
    cos_angle = math.cos(angle)
    sin_angle = math.sin(angle)
    new_x = cx + dx * cos_angle - dy * sin_angle
    new_y = cy + dx * sin_angle + dy * cos_angle
    return (new_x, new_y)

def get_hexagon_points(center, side_length, angle):
    """Retorna os pontos do hexágono rotacionado."""
    points = []
    for i in range(num_sides):
        theta = 2 * math.pi / num_sides * i + angle
        x = center[0] + side_length * math.cos(theta)
        y = center[1] + side_length * math.sin(theta)
        points.append((x, y))
    return points

def check_collision(ball_pos, ball_radius, hexagon_points):
    """Verifica se a bola colidiu com alguma parede do hexágono."""
    for i in range(len(hexagon_points)):
        p1 = hexagon_points[i]
        p2 = hexagon_points[(i + 1) % len(hexagon_points)]
        
        # Calcula a distância da bola até a linha do hexágono
        line_vec = (p2[0] - p1[0], p2[1] - p1[1])
        ball_vec = (ball_pos[0] - p1[0], ball_pos[1] - p1[1])
        line_len_sq = line_vec[0]**2 + line_vec[1]**2
        t = max(0, min(1, (ball_vec[0] * line_vec[0] + ball_vec[1] * line_vec[1]) / line_len_sq))
        closest_point = (p1[0] + t * line_vec[0], p1[1] + t * line_vec[1])
        dist_sq = (ball_pos[0] - closest_point[0])**2 + (ball_pos[1] - closest_point[1])**2
        
        if dist_sq <= ball_radius**2:
            return True, (p1, p2), closest_point
    return False, None, None

def reflect_velocity(ball_vel, wall):
    """Reflete a velocidade da bola ao colidir com a parede."""
    p1, p2 = wall
    wall_vec = (p2[0] - p1[0], p2[1] - p1[1])
    normal = (-wall_vec[1], wall_vec[0])
    normal_len = math.sqrt(normal[0]**2 + normal[1]**2)
    normal = (normal[0] / normal_len, normal[1] / normal_len)
    
    dot = ball_vel[0] * normal[0] + ball_vel[1] * normal[1]
    ball_vel[0] -= 2 * dot * normal[0]
    ball_vel[1] -= 2 * dot * normal[1]
    
    return ball_vel

# Loop principal
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Atualiza a posição da bola
    ball_vel[1] += gravity
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # Aplica atrito
    ball_vel[0] *= friction
    ball_vel[1] *= friction

    # Rotaciona o hexágono
    angle += rotation_speed
    hexagon_points = get_hexagon_points((WIDTH // 2, HEIGHT // 2), side_length, angle)

    # Verifica colisão com as paredes do hexágono
    collision, wall, closest_point = check_collision(ball_pos, ball_radius, hexagon_points)
    if collision:
        ball_vel = reflect_velocity(ball_vel, wall)

        # Ajusta a posição da bola para evitar que ela fique presa dentro da parede
        p1, p2 = wall
        wall_vec = (p2[0] - p1[0], p2[1] - p1[1])
        normal = (-wall_vec[1], wall_vec[0])
        normal_len = math.sqrt(normal[0]**2 + normal[1]**2)
        normal = (normal[0] / normal_len, normal[1] / normal_len)
        
        # Move a bola para fora da parede
        overlap = ball_radius - math.sqrt((ball_pos[0] - closest_point[0])**2 + (ball_pos[1] - closest_point[1])**2)
        ball_pos[0] += normal[0] * overlap
        ball_pos[1] += normal[1] * overlap

    # Desenha o fundo
    screen.fill(WHITE)

    # Desenha o hexágono
    pygame.draw.polygon(screen, BLACK, hexagon_points, 2)

    # Desenha a bola
    pygame.draw.circle(screen, RED, (int(ball_pos[0]), int(ball_pos[1])), ball_radius)

    # Atualiza a tela
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()