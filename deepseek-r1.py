import pygame
import math

pygame.init()

# Configurações da janela
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Bola Quicando em Hexágono Giratório")
relogio = pygame.time.Clock()

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)

# Parâmetros do hexágono
centro_x, centro_y = largura // 2, altura // 2
raio_hexagono = 200
angulo_rotacao = 0
velocidade_rotacao = 0.02  # radianos por quadro

# Parâmetros da bola
raio_bola = 15
cor_bola = VERMELHO
gravidade = 0.5
atrito_ar = 0.02
restituicao = 0.8
atrito_colisao = 0.2

# Estado inicial da bola
bola_x = centro_x
bola_y = centro_y - raio_hexagono + raio_bola + 5
velocidade_x = 2
velocidade_y = 0

def calcular_vertices_hexagono(raio, angulo):
    vertices = []
    for i in range(6):
        theta = angulo + math.radians(i * 60)
        x = centro_x + raio * math.cos(theta)
        y = centro_y + raio * math.sin(theta)
        vertices.append((x, y))
    return vertices

executando = True
while executando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False

    tela.fill(PRETO)

    # Atualizar rotação do hexágono
    angulo_rotacao += velocidade_rotacao
    vertices = calcular_vertices_hexagono(raio_hexagono, angulo_rotacao)

    # Desenhar hexágono
    pygame.draw.polygon(tela, BRANCO, vertices, 2)

    # Aplicar física na bola
    velocidade_x *= (1 - atrito_ar)
    velocidade_y *= (1 - atrito_ar)
    velocidade_y += gravidade

    # Atualizar posição da bola
    bola_x += velocidade_x
    bola_y += velocidade_y

    # Verificar colisões com as arestas
    colisao = False
    for i in range(6):
        A = vertices[i]
        B = vertices[(i + 1) % 6]
        
        # Calcular ponto médio e vetor normal
        meio_x = (A[0] + B[0]) / 2
        meio_y = (A[1] + B[1]) / 2
        normal_x = centro_x - meio_x
        normal_y = centro_y - meio_y
        comprimento = math.hypot(normal_x, normal_y)
        if comprimento == 0:
            continue
        normal_x /= comprimento
        normal_y /= comprimento

        # Calcular distância da bola à aresta
        distancia = (bola_x - meio_x) * normal_x + (bola_y - meio_y) * normal_y

        if distancia < raio_bola:
            # Encontrar ponto de colisão mais próximo
            vetor_AB = (B[0] - A[0], B[1] - A[1])
            vetor_AP = (bola_x - A[0], bola_y - A[1])
            produto_AB = vetor_AB[0]**2 + vetor_AB[1]**2
            if produto_AB == 0:
                continue
            t = (vetor_AP[0] * vetor_AB[0] + vetor_AP[1] * vetor_AB[1]) / produto_AB
            t = max(0, min(1, t))
            ponto_colisao_x = A[0] + t * vetor_AB[0]
            ponto_colisao_y = A[1] + t * vetor_AB[1]

            # Calcular velocidade da parede
            omega = velocidade_rotacao
            velocidade_parede_x = -omega * (ponto_colisao_y - centro_y)
            velocidade_parede_y = omega * (ponto_colisao_x - centro_x)

            # Calcular velocidade relativa
            velocidade_rel_x = velocidade_x - velocidade_parede_x
            velocidade_rel_y = velocidade_y - velocidade_parede_y

            # Componentes normal e tangencial
            produto_escalar = velocidade_rel_x * normal_x + velocidade_rel_y * normal_y
            normal_vx = produto_escalar * normal_x
            normal_vy = produto_escalar * normal_y
            tangente_vx = velocidade_rel_x - normal_vx
            tangente_vy = velocidade_rel_y - normal_vy

            # Aplicar restituição e atrito
            nova_normal_vx = -restituicao * normal_vx
            nova_normal_vy = -restituicao * normal_vy
            nova_tangente_vx = tangente_vx * (1 - atrito_colisao)
            nova_tangente_vy = tangente_vy * (1 - atrito_colisao)

            # Atualizar velocidade
            velocidade_x = velocidade_parede_x + nova_normal_vx + nova_tangente_vx
            velocidade_y = velocidade_parede_y + nova_normal_vy + nova_tangente_vy

            # Corrigir posição
            penetracao = raio_bola - distancia
            bola_x += normal_x * penetracao
            bola_y += normal_y * penetracao

            colisao = True
            break

    # Desenhar bola
    pygame.draw.circle(tela, cor_bola, (int(bola_x), int(bola_y)), raio_bola)

    pygame.display.flip()
    relogio.tick(60)

pygame.quit()