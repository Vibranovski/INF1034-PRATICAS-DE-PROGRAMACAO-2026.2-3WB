import pygame
import sys
from pathlib import Path
from collections import deque

pygame.init()

DIMENSAO = 8
TAMANHO_QUADRADO = 80
LARGURA = ALTURA = DIMENSAO * TAMANHO_QUADRADO

COR_BRANCA = (240, 217, 181)
COR_PRETA = (181, 136, 99)

screen = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Xadrez ULTIMATE - Animação e Efeito 3D")
clock = pygame.time.Clock()

tabuleiro_estado = [
    ["pT", "pC", "pB", "pD", "pR", "pB", "pC", "pT"],
    ["pP", "pP", "pP", "pP", "pP", "pP", "pP", "pP"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
    ["bT", "bC", "bB", "bD", "bR", "bB", "bC", "bT"]
]

imagens = {}
imagens_selecionadas = {}

PASTA_IMAGENS = Path(
    r"D:\PUC RIO\Práticas de PROG INF1034"
)
CAMINHO_SPRITE = PASTA_IMAGENS / "Chess_Pieces.png"

peca_selecionada = None
origem_selecionada = None

animando = False
peca_movendo = None
pos_atual_anim_x = 0.0
pos_atual_anim_y = 0.0
destino_anim_x = 0.0
destino_anim_y = 0.0


def remover_fundo(sprite):
    largura, altura = sprite.get_size()

    mascara = pygame.mask.from_threshold(
        sprite,
        (255, 255, 255, 255),
        (15, 15, 15, 255)
    )

    visitados = set()
    fila = deque()

    for x in range(largura):
        fila.append((x, 0))
        fila.append((x, altura - 1))

    for y in range(altura):
        fila.append((0, y))
        fila.append((largura - 1, y))

    while fila:
        x, y = fila.popleft()

        if (x, y) in visitados:
            continue

        if mascara.get_at((x, y)) == 0:
            continue

        visitados.add((x, y))
        sprite.set_at((x, y), (255, 255, 255, 0))

        for dx, dy in [(1, 0), (-1, 0),
                       (0, 1), (0, -1)]:
            nx = x + dx
            ny = y + dy

            if 0 <= nx < largura and 0 <= ny < altura:
                if (nx, ny) not in visitados:
                    fila.append((nx, ny))

    return sprite


def carregar_imagens():
    sprite_sheet = pygame.image.load(
        str(CAMINHO_SPRITE)
    ).convert_alpha()

    largura_original, altura_original = sprite_sheet.get_size()

    coordenadas = {
        "bP": (210, 80, 290, 520),
        "bT": (620, 80, 310, 520),
        "bB": (1050, 80, 310, 520),
        "bC": (1460, 80, 320, 520),
        "bD": (210, 1210, 290, 680),
        "bR": (620, 1210, 310, 680),

        "pP": (210, 660, 290, 520),
        "pT": (620, 660, 310, 520),
        "pB": (1050, 660, 310, 520),
        "pC": (1460, 660, 320, 520),
        "pD": (1050, 1210, 310, 680),
        "pR": (1460, 1210, 320, 680)
    }

    escala_x = largura_original / 2048
    escala_y = altura_original / 2048

    for codigo, (x, y, largura, altura) in coordenadas.items():
        x = round(x * escala_x)
        y = round(y * escala_y)
        largura = round(largura * escala_x)
        altura = round(altura * escala_y)

        sprite = sprite_sheet.subsurface(
            pygame.Rect(x, y, largura, altura)
        ).copy()

        proporcao = min(65 / largura, 65 / altura)
        nova_largura = max(1, round(largura * proporcao))
        nova_altura = max(1, round(altura * proporcao))
        sprite_normal = pygame.transform.smoothscale(sprite, (nova_largura, nova_altura))
        imagens[codigo] = remover_fundo(sprite_normal)

        proporcao_zoom = min(78 / largura, 78 / altura)
        largura_zoom = max(1, round(largura * proporcao_zoom))
        altura_zoom = max(1, round(altura * proporcao_zoom))
        sprite_zoom = pygame.transform.smoothscale(sprite, (largura_zoom, altura_zoom))
        imagens_selecionadas[codigo] = remover_fundo(sprite_zoom)


def desenhar_tabuleiro(screen):
    for linha in range(DIMENSAO):
        for coluna in range(DIMENSAO):
            if (linha + coluna) % 2 == 0:
                cor = COR_BRANCA
            else:
                cor = COR_PRETA

            pygame.draw.rect(
                screen,
                cor,
                (
                    coluna * TAMANHO_QUADRADO,
                    linha * TAMANHO_QUADRADO,
                    TAMANHO_QUADRADO,
                    TAMANHO_QUADRADO
                )
            )


def desenhar_pecas(screen):
    for linha in range(DIMENSAO):
        for coluna in range(DIMENSAO):
            peca = tabuleiro_estado[linha][coluna]

            if peca != "--":
                if animando and (linha, coluna) == origem_selecionada:
                    continue
                if not animando and peca_selecionada == peca and origem_selecionada == (linha, coluna):
                    imagem = imagens_selecionadas[peca]
                    largura = imagem.get_width()
                    altura = imagem.get_height()
                    x = (coluna * TAMANHO_QUADRADO) + (TAMANHO_QUADRADO - largura) // 2
                    y = (linha * TAMANHO_QUADRADO) + (TAMANHO_QUADRADO - altura) // 2
                    screen.blit(imagem, (x, y))
                    continue

                imagem = imagens[peca]
                largura = imagem.get_width()
                altura = imagem.get_height()

                x = coluna * TAMANHO_QUADRADO + (TAMANHO_QUADRADO - largura) // 2
                y = linha * TAMANHO_QUADRADO + (TAMANHO_QUADRADO - altura) // 2

                screen.blit(imagem, (x, y))


carregar_imagens()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN and not animando:
            pos_mouse = pygame.mouse.get_pos()

            coluna = pos_mouse[0] // TAMANHO_QUADRADO
            linha = pos_mouse[1] // TAMANHO_QUADRADO

            peca = tabuleiro_estado[linha][coluna]

            print(f"Clique na casa: Linha {linha+1}, Coluna {coluna+1}, Peça: {peca}")

            if peca_selecionada is None:
                if peca != "--":
                    peca_selecionada = peca
                    origem_selecionada = (linha, coluna)
                    print(f"Peça selecionada: {peca_selecionada} em ({linha+1}, {coluna+1})")
            
            else:
                origem_linha, origem_coluna = origem_selecionada

                if peca == "--":
                    tabuleiro_estado[origem_linha][origem_coluna] = "--"
                    
                    animando = True
                    peca_movendo = peca_selecionada
                    
                    img_temp = imagens[peca_movendo]
                    pos_atual_anim_x = origem_coluna * TAMANHO_QUADRADO + (TAMANHO_QUADRADO - img_temp.get_width()) // 2
                    pos_atual_anim_y = origem_linha * TAMANHO_QUADRADO + (TAMANHO_QUADRADO - img_temp.get_height()) // 2
                    
                    destino_anim_x = coluna * TAMANHO_QUADRADO + (TAMANHO_QUADRADO - img_temp.get_width()) // 2
                    destino_anim_y = linha * TAMANHO_QUADRADO + (TAMANHO_QUADRADO - img_temp.get_height()) // 2
                    
                    destino_final = (linha, coluna)
                
                peca_selecionada = None
                origem_selecionada = None

    clock.tick(60)
    dt = clock.get_time()

    if animando:
        velocidade_deslize = 0.015 
        
        pos_atual_anim_x += (destino_anim_x - pos_atual_anim_x) * velocidade_deslize * dt
        pos_atual_anim_y += (destino_anim_y - pos_atual_anim_y) * velocidade_deslize * dt

        if abs(destino_anim_x - pos_atual_anim_x) < 0.5 and abs(destino_anim_y - pos_atual_anim_y) < 0.5:
            pos_atual_anim_x = destino_anim_x
            pos_atual_anim_y = destino_anim_y
            animando = False
            tabuleiro_estado[destino_final[0]][destino_final[1]] = peca_movendo

    screen.fill((56, 203, 171))

    desenhar_tabuleiro(screen)

    desenhar_pecas(screen)

    if animando:
        img_mov = imagens[peca_movendo]
        screen.blit(img_mov, (pos_atual_anim_x, pos_atual_anim_y))

    pygame.display.update()
