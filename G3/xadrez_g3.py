
import pygame
import sys
from pathlib import Path
from collections import deque

pygame.init()

# DIMENSÕES DO TABULEIRO
DIMENSAO = 8
TAMANHO_QUADRADO = 80
LARGURA = ALTURA = DIMENSAO * TAMANHO_QUADRADO

# Definição das cores (RGB)
COR_BRANCA = (240, 217, 181)  # Bege claro
COR_PRETA = (181, 136, 99)    # Marrom amadeirado

screen = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Xadrez ULTIMATE")
clock = pygame.time.Clock()

# Matriz 8x8 com as 32 peças nas posições iniciais
# b = branco | p = preto
# R = Rei | D = Dama | B = Bispo
# C = Cavalo | T = Torre | P = Peão

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

# Dicionário para armazenar os sprites
imagens = {}

# Caminho da imagem PNG
PASTA_IMAGENS = Path(
    r"C:\Users\Daniel\OneDrive\Documentos\estudos\@Graduação Ciência da Computação - PUC\1° Período\INF1034 - PRÁTICAS DE PROGRAMAÇÃO\G3\imagem_xadrez"
)

CAMINHO_SPRITE = PASTA_IMAGENS / "Chess_Pieces.png"

def remover_fundo(sprite):
    """Remove o fundo branco conectado às bordas."""

    largura, altura = sprite.get_size()

    # Máscara para identificar as regiões brancas
    mascara = pygame.mask.from_threshold(
        sprite,
        (255, 255, 255, 255),
        (15, 15, 15, 255)
    )

    # Marca os pixels brancos conectados às bordas
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
    """Recorta individualmente as 12 peças da sprite sheet."""

    sprite_sheet = pygame.image.load(
        str(CAMINHO_SPRITE)
    ).convert_alpha()

    largura_original, altura_original = sprite_sheet.get_size()

    # Coordenadas para a imagem original de 2048x2048
    coordenadas = {
        # Peças brancas
        "bP": (210, 80, 290, 520),
        "bT": (620, 80, 310, 520),
        "bB": (1050, 80, 310, 520),
        "bC": (1460, 80, 320, 520),
        "bD": (210, 1210, 290, 680),
        "bR": (620, 1210, 310, 680),

        # Peças pretas
        "pP": (210, 660, 290, 520),
        "pT": (620, 660, 310, 520),
        "pB": (1050, 660, 310, 520),
        "pC": (1460, 660, 320, 520),
        "pD": (1050, 1210, 310, 680),
        "pR": (1460, 1210, 320, 680)
    }

    # Adapta as coordenadas caso a imagem tenha outro tamanho
    escala_x = largura_original / 2048
    escala_y = altura_original / 2048

    for codigo, (x, y, largura, altura) in coordenadas.items():

        x = round(x * escala_x)
        y = round(y * escala_y)
        largura = round(largura * escala_x)
        altura = round(altura * escala_y)

        # Recorta a peça
        sprite = sprite_sheet.subsurface(
            pygame.Rect(x, y, largura, altura)
        ).copy()

        # Redimensiona antes de remover o fundo
        proporcao = min(65 / largura, 65 / altura)

        nova_largura = max(1, round(largura * proporcao))
        nova_altura = max(1, round(altura * proporcao))

        sprite = pygame.transform.smoothscale(
            sprite, (nova_largura, nova_altura)
        )

        # Remove o fundo branco
        sprite = remover_fundo(sprite)

        # Armazena a imagem no dicionário
        imagens[codigo] = sprite


def desenhar_tabuleiro(screen):
    """Desenha a grade 8x8 alternando as cores."""

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
    """Desenha as peças centralizadas nas casas."""

    for linha in range(DIMENSAO):
        for coluna in range(DIMENSAO):

            peca = tabuleiro_estado[linha][coluna]

            if peca != "--":

                imagem = imagens[peca]

                largura = imagem.get_width()
                altura = imagem.get_height()

                # Centraliza a peça na casa
                x = coluna * TAMANHO_QUADRADO
                x += (TAMANHO_QUADRADO - largura) // 2

                y = linha * TAMANHO_QUADRADO
                y += (TAMANHO_QUADRADO - altura) // 2

                screen.blit(imagem, (x, y))


# Carrega as imagens antes do loop principal
carregar_imagens()

# LOOP PRINCIPAL DO JOGO
while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Interação com o mouse
        elif event.type == pygame.MOUSEBUTTONDOWN:

            pos_mouse = pygame.mouse.get_pos()

            coluna = pos_mouse[0] // TAMANHO_QUADRADO
            linha = pos_mouse[1] // TAMANHO_QUADRADO

            peca = tabuleiro_estado[linha][coluna]

            print(
                f"Clique na casa: Linha {linha+1}, "
                f"Coluna {coluna+1}, Peça: {peca}"
            )

    # Desenha o tabuleiro
    desenhar_tabuleiro(screen)

    # Desenha as 32 peças
    desenhar_pecas(screen)

    # Atualiza a tela a 60 FPS
    clock.tick(60)
    pygame.display.update()
