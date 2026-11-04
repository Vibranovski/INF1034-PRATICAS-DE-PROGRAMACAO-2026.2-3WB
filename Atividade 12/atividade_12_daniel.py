import pygame
from pathlib import Path

#açdlsmasçvoimp - aqui é o Daniel comentando, e não a IA
# Inicializacao do Pygame e da janela
pygame.init()
LARGURA_TELA = 800
ALTURA_TELA = 600

tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Atividade 12 - Mapa com Tileset")
relogio = pygame.time.Clock()
PASTA_PROJETO = Path(__file__).resolve().parent


#lkruasklruu - aqui é o Daniel comentando, e não a IA
# Tileset: cada tile tem 16x16 pixels na imagem original e e desenhado 2x maior
TAMANHO_ORIGINAL = 16
ESCALA_TILE = 2
TAMANHO_TILE = TAMANHO_ORIGINAL * ESCALA_TILE

caminho_tileset = PASTA_PROJETO / "16x16 dungeon tiles.png"
tile_set = pygame.image.load(str(caminho_tileset)).convert_alpha()

# Dicionario de recortes: letra do mapa -> [coluna, linha] do tile no tileset
recortes = {
    "q": [1, 0],    # parede: canto de cima esquerdo
    "w": [2, 0],    # parede: teto
    "e": [3, 0],    # parede: canto de cima direito
    "a": [1, 1],    # parede: lado esquerdo
    "d": [3, 1],    # parede: lado direito
    "z": [1, 2],    # parede: canto de baixo esquerdo
    "x": [2, 2],    # parede: fundo
    "c": [3, 2],    # parede: canto de baixo direito
    "=": [6, 1],    # chao (parte de cima)
    "-": [6, 2],    # terra embaixo do chao
    "#": [7, 1],    # tijolos
    "_": [5, 0],    # plataforma flutuante
    "t": [13, 7],   # tocha
    "p": [13, 0],   # pocao
    "k": [15, 4],   # caveira
    "r": [13, 1],   # pedra
    "l": [13, 4],   # pilar
    "h": [13, 3],   # placa
}

# Letras que o personagem nao consegue atravessar
TILES_SOLIDOS = "qweadzxc=-#_"

# Recorta cada tile uma unica vez e guarda pronto para desenhar
tiles = {}

for letra, posicao in recortes.items():
    coluna, linha = posicao
    area = pygame.Rect(coluna * TAMANHO_ORIGINAL, linha * TAMANHO_ORIGINAL, TAMANHO_ORIGINAL, TAMANHO_ORIGINAL)
    recorte = tile_set.subsurface(area)
    tiles[letra] = pygame.transform.scale(recorte, (TAMANHO_TILE, TAMANHO_TILE))


# Carregamento do mapa a partir do txt
# Cada letra e um tile do dicionario, "." = vazio, "P" = onde o personagem comeca
caminho_mapa = PASTA_PROJETO / "mapa.txt"
with open(caminho_mapa) as arquivo:
    linhas_mapa = arquivo.read().splitlines()

LARGURA_MAPA = len(linhas_mapa[0]) * TAMANHO_TILE
ALTURA_MAPA = len(linhas_mapa) * TAMANHO_TILE

# Percorre o txt e monta as listas do mapa
tiles_do_mapa = []      # (imagem, x, y) de tudo que sera desenhado
blocos_solidos = []     # retangulos usados na colisao
inicio_x = TAMANHO_TILE
inicio_y = TAMANHO_TILE

for numero_linha, linha in enumerate(linhas_mapa):
    for numero_coluna, letra in enumerate(linha):
        x = numero_coluna * TAMANHO_TILE
        y = numero_linha * TAMANHO_TILE

        if letra in tiles:
            tiles_do_mapa.append((tiles[letra], x, y))

        if letra in TILES_SOLIDOS:
            bloco = pygame.Rect(x, y, TAMANHO_TILE, TAMANHO_TILE)
            if letra == "=":
                # o desenho do chao so comeca 6 pixels abaixo do topo do tile
                bloco.top = y + 6
            blocos_solidos.append(bloco)
        elif letra == "P":
            inicio_x = x
            inicio_y = y


#m,cxnbv.x,cdnfglskdfhr - aqui é o Daniel comentando, e não a IA
# Carregamento da spritesheet do Mega Man (5 colunas x 2 linhas, 60x64 cada)
caminho_spritesheet = PASTA_PROJETO / "megaman_spritesheet.png"
spritesheet = pygame.image.load(str(caminho_spritesheet)).convert_alpha()

# O fundo da spritesheet e cinza bem claro: deixa esses pixels transparentes
for px in range(spritesheet.get_width()):
    for py in range(spritesheet.get_height()):
        cor = spritesheet.get_at((px, py))
        if cor.r > 235 and cor.g > 235 and cor.b > 235:
            spritesheet.set_at((px, py), (0, 0, 0, 0))

LARGURA_FRAME = 60
ALTURA_FRAME = 64


def recortar_linha(spritesheet, linha):
    frames = []

    for coluna in range(5):
        x_recorte = coluna * LARGURA_FRAME
        y_recorte = linha * ALTURA_FRAME
        area = pygame.Rect(x_recorte, y_recorte, LARGURA_FRAME, ALTURA_FRAME)
        frames.append(spritesheet.subsurface(area).copy())

    return frames

#hfoegfoqufgfoegf - aqui é o Daniel comentando, e não a IA
frames_andar = recortar_linha(spritesheet, 0)
frames_pulo = recortar_linha(spritesheet, 1)
frame_parado = frames_andar[1]

# Altura do pe dentro de cada frame (para o desenho encostar no chao)
PE_FRAME_ANDAR = 60
PE_FRAME_PULO = 55

INTERVALO_ANDAR = 0.10
INTERVALO_PULO = 0.12


# Personagem: o retangulo e a "caixa de colisao", menor que o desenho
jogador = pygame.Rect(0, 0, 26, 44)
jogador.midbottom = (inicio_x + TAMANHO_TILE // 2, inicio_y + TAMANHO_TILE)
x_jogador = float(jogador.x)
y_jogador = float(jogador.y)

VELOCIDADE_JOGADOR = 250.0
FORCA_PULO = -760.0
GRAVIDADE = 1900.0
VELOCIDADE_MAXIMA_QUEDA = 900.0

velocidade_y = 0.0
no_chao = False
olhando_direita = True
tempo_andar = 0.0
tempo_no_ar = 0.0

camera_x = 0
camera_y = 0

# Textos fixos na tela
fonte = pygame.font.Font(None, 28)
texto_controles = fonte.render("Setas ou A/D: andar   Seta para cima, W ou Espaço: pular", True, (240, 220, 230))


#qowpuieripofweqlckj - aqui é o Daniel comentando, e não a IA
# Game Loop: o jogo continua ate a janela ser fechada
rodando = True

while rodando:
    dt = relogio.tick(60) / 1000.0

    # se a janela travar, o dt fica grande e o personagem atravessaria o chao
    if dt > 0.05:
        dt = 0.05

    # Processa eventos pontuais: fechar e pular
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        elif evento.type == pygame.KEYDOWN and evento.key in (pygame.K_UP, pygame.K_w, pygame.K_SPACE):
            # so pula se estiver no chao
            if no_chao:
                velocidade_y = FORCA_PULO
                no_chao = False
                tempo_no_ar = 0.0

    if not rodando:
        break

    # Consulta o estado atual do teclado (tecla sendo segurada)
    teclas = pygame.key.get_pressed()

    direcao = 0
    if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
        direcao = direcao - 1
    if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
        direcao = direcao + 1

    if direcao != 0:
        olhando_direita = direcao > 0
        tempo_andar = tempo_andar + dt
    else:
        tempo_andar = 0.0

    #sauhuahdwahdpqhfqpaf - aqui é o Daniel comentando, e não a IA
    # movimento horizontal + colisao com colliderect
    x_jogador = x_jogador + (direcao * VELOCIDADE_JOGADOR * dt)
    jogador.x = round(x_jogador)

    for bloco in blocos_solidos:
        if jogador.colliderect(bloco):
            if direcao > 0:
                jogador.right = bloco.left
            elif direcao < 0:
                jogador.left = bloco.right
            x_jogador = float(jogador.x)

    # Movimento vertical (gravidade) + colisao com colliderect
    velocidade_y = velocidade_y + (GRAVIDADE * dt)
    if velocidade_y > VELOCIDADE_MAXIMA_QUEDA:
        velocidade_y = VELOCIDADE_MAXIMA_QUEDA

    y_jogador = y_jogador + (velocidade_y * dt)
    jogador.y = round(y_jogador)

    for bloco in blocos_solidos:
        if jogador.colliderect(bloco):
            if velocidade_y > 0:
                jogador.bottom = bloco.top
            elif velocidade_y < 0:
                jogador.top = bloco.bottom
            velocidade_y = 0.0
            y_jogador = float(jogador.y)

    # confere se tem chao logo abaixo do pe (1 pixel para baixo)
    pe = pygame.Rect(jogador.x, jogador.bottom, jogador.width, 1)
    no_chao = False
    for bloco in blocos_solidos:
        if pe.colliderect(bloco):
            no_chao = True

    if not no_chao:
        tempo_no_ar = tempo_no_ar + dt

    # camera: segue o personagem, sem mostrar nada fora do mapa
    camera_x = jogador.centerx - LARGURA_TELA // 2
    camera_y = jogador.centery - ALTURA_TELA // 2

    if camera_x < 0:
        camera_x = 0
    if camera_x > LARGURA_MAPA - LARGURA_TELA:
        camera_x = LARGURA_MAPA - LARGURA_TELA
    if camera_y < 0:
        camera_y = 0
    if camera_y > ALTURA_MAPA - ALTURA_TELA:
        camera_y = ALTURA_MAPA - ALTURA_TELA

    # Escolhe o frame pulando, andando ou parado
    if not no_chao:
        indice_jogador = int(tempo_no_ar / INTERVALO_PULO)
        if indice_jogador >= len(frames_pulo):
            indice_jogador = len(frames_pulo) - 1
        frame_jogador = frames_pulo[indice_jogador]
        altura_pe = PE_FRAME_PULO
    elif direcao != 0:
        indice_jogador = int(tempo_andar / INTERVALO_ANDAR) % len(frames_andar)
        frame_jogador = frames_andar[indice_jogador]
        altura_pe = PE_FRAME_ANDAR
    else:
        frame_jogador = frame_parado
        altura_pe = PE_FRAME_ANDAR

    # vira o desenho quando estiver indo para a esquerda
    #m,cxnbv.x,cdnfglskdfhr - aqui é o Daniel comentando, e não a IA
    if not olhando_direita:
        frame_jogador = pygame.transform.flip(frame_jogador, True, False)

    # Desenhar o quadro atual (tudo do mapa e deslocado pela camera)
    tela.fill((0, 0, 0))

    for imagem, x, y in tiles_do_mapa:
        tela.blit(imagem, (x - camera_x, y - camera_y))

    x_desenho = jogador.centerx - LARGURA_FRAME // 2 - camera_x
    y_desenho = jogador.bottom - altura_pe - camera_y
    tela.blit(frame_jogador, (x_desenho, y_desenho))

    tela.blit(texto_controles, (12, 10))

    pygame.display.flip()

pygame.quit()
