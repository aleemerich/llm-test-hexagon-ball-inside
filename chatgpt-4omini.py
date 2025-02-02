import pygame, math, sys

# Inicialização do pygame
pygame.init()

# Parâmetros da janela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bola quicando no Hexágono Giratório")
clock = pygame.time.Clock()

# Parâmetros do hexágono
hex_center = (WIDTH // 2, HEIGHT // 2)
hex_radius = 250         # Distância do centro a cada vértice
hex_angle = 0.0          # Ângulo atual de rotação (em radianos)
hex_angular_velocity = 0.5  # Velocidade angular (rad/s)

# Pré-calcula os vértices de um hexágono unitário centrado na origem
hex_base = []
for i in range(6):
    angle = 2 * math.pi * i / 6
    x = hex_radius * math.cos(angle)
    y = hex_radius * math.sin(angle)
    hex_base.append((x, y))

# Parâmetros da bola
ball_radius = 15
ball_pos = [hex_center[0], hex_center[1] - 100]  # Inicia acima do centro
ball_vel = [150, 0]     # Velocidade inicial (pixels/s)
gravity = 500           # Aceleração da gravidade (pixels/s²)
damping = 0.999         # Amortecimento leve a cada frame (simula atrito do ar)
restitution = 0.9       # Coeficiente de restituição (energia conservada na colisão)

def rotaciona_ponto(pt, angle):
    """Rotaciona um ponto (x,y) em torno da origem pelo ângulo dado (rad)."""
    x, y = pt
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    return (x * cos_a - y * sin_a, x * sin_a + y * cos_a)

def get_hex_vertices(center, base_vertices, angle):
    """Retorna os vértices do hexágono, rotacionados e transladados."""
    vertices = []
    for vx, vy in base_vertices:
        rx, ry = rotaciona_ponto((vx, vy), angle)
        vertices.append( (center[0] + rx, center[1] + ry) )
    return vertices

def colide_bola_com_aresta(ball_pos, ball_radius, A, B, wall_vel):
    """
    Verifica colisão entre a bola (círculo) e a aresta definida pelos pontos A e B.
    Se houver colisão, retorna (penetracao, normal) onde:
      - penetracao: profundidade de interpenetração (>= 0)
      - normal: vetor unitário com a direção "para fora" da parede (apontando para o interior do hexágono)
    Caso contrário, retorna (0, None).
    """
    Ax, Ay = A
    Bx, By = B
    # Vetor da aresta e seu comprimento ao quadrado
    edge_vec = (Bx - Ax, By - Ay)
    edge_length_sq = edge_vec[0]**2 + edge_vec[1]**2
    if edge_length_sq == 0:
        return (0, None)
    
    # Projeção do vetor (ball_pos - A) sobre a aresta
    t = ((ball_pos[0] - Ax) * edge_vec[0] + (ball_pos[1] - Ay) * edge_vec[1]) / edge_length_sq
    t = max(0, min(1, t))  # limitar para ficar no segmento
    # Ponto mais próximo na aresta
    closest = (A[0] + t * edge_vec[0], A[1] + t * edge_vec[1])
    
    # Vetor do ponto mais próximo até o centro da bola
    diff = (ball_pos[0] - closest[0], ball_pos[1] - closest[1])
    dist = math.hypot(diff[0], diff[1])
    
    if dist < ball_radius:
        # Vetor normal: normaliza diff; se for zero (colisão exata no vértice) usa um normal aproximado
        if dist != 0:
            normal = (diff[0] / dist, diff[1] / dist)
        else:
            normal = (0, -1)
        penetration = ball_radius - dist
        return (penetration, normal)
    return (0, None)

# Loop principal
running = True
while running:
    dt = clock.tick(60) / 1000.0  # Delta time em segundos (60 FPS)
    
    # Processa eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    # Atualiza a rotação do hexágono
    hex_angle += hex_angular_velocity * dt
    
    # Atualiza a física da bola
    # Aplica gravidade (para baixo)
    ball_vel[1] += gravity * dt
    # Atualiza posição
    ball_pos[0] += ball_vel[0] * dt
    ball_pos[1] += ball_vel[1] * dt
    # Aplica amortecimento (atrito do ar)
    ball_vel[0] *= damping
    ball_vel[1] *= damping

    # Obtém os vértices atuais do hexágono
    hex_vertices = get_hex_vertices(hex_center, hex_base, hex_angle)
    
    # Processa colisões da bola com cada aresta do hexágono
    for i in range(len(hex_vertices)):
        A = hex_vertices[i]
        B = hex_vertices[(i+1) % len(hex_vertices)]
        
        # Calcula o ponto de colisão (aproximadamente, usando a projeção da bola sobre a aresta)
        Ax, Ay = A
        Bx, By = B
        edge_vec = (Bx - Ax, By - Ay)
        edge_length_sq = edge_vec[0]**2 + edge_vec[1]**2
        if edge_length_sq == 0:
            continue
        
        t = ((ball_pos[0] - Ax) * edge_vec[0] + (ball_pos[1] - Ay) * edge_vec[1]) / edge_length_sq
        t = max(0, min(1, t))
        # Ponto mais próximo na aresta
        closest = (A[0] + t * edge_vec[0], A[1] + t * edge_vec[1])
        
        # Calcula a velocidade da parede no ponto de colisão devido à rotação
        # A rotação é em torno do centro do hexágono; para um ponto p, a velocidade é: ω x (p - center)
        rx = closest[0] - hex_center[0]
        ry = closest[1] - hex_center[1]
        # Em 2D, o produto vetorial resulta em uma velocidade perpendicular:
        wall_vel = (-hex_angular_velocity * ry, hex_angular_velocity * rx)
        
        # Verifica colisão: se a distância do centro da bola ao segmento for menor que o raio
        penetration, normal = colide_bola_com_aresta(ball_pos, ball_radius, A, B, wall_vel)
        if penetration > 0 and normal is not None:
            # Para garantir que a colisão seja processada apenas se a bola estiver se movendo em direção à parede,
            # calculamos a velocidade relativa (bola em relação à parede).
            rel_vel = (ball_vel[0] - wall_vel[0], ball_vel[1] - wall_vel[1])
            # Se a velocidade relativa na direção do normal for negativa, a bola se aproxima da parede
            if rel_vel[0] * normal[0] + rel_vel[1] * normal[1] < 0:
                # Corrige a posição da bola para fora da parede
                ball_pos[0] += normal[0] * penetration
                ball_pos[1] += normal[1] * penetration
                
                # Reflete a velocidade relativa (com restituição)
                dot = rel_vel[0] * normal[0] + rel_vel[1] * normal[1]
                v_reflected = (
                    rel_vel[0] - (1 + restitution) * dot * normal[0],
                    rel_vel[1] - (1 + restitution) * dot * normal[1]
                )
                # Volta para a velocidade no referencial global (soma a velocidade da parede)
                ball_vel = [v_reflected[0] + wall_vel[0], v_reflected[1] + wall_vel[1]]
    
    # Prepara a tela para desenhar
    screen.fill((30, 30, 30))  # Fundo escuro

    # Desenha o hexágono (linhas brancas)
    pygame.draw.polygon(screen, (255, 255, 255), hex_vertices, 3)

    # Desenha a bola (círculo vermelho)
    pygame.draw.circle(screen, (200, 50, 50), (int(ball_pos[0]), int(ball_pos[1])), ball_radius)

    # Atualiza a tela
    pygame.display.flip()

pygame.quit()
sys.exit()
