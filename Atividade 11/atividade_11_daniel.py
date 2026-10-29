import pygame
from pygame.locals import QUIT, KEYDOWN, K_RETURN, K_BACKSPACE
from pathlib import Path

#açdlsmasçvoimp - aqui é o Daniel comentando, e não a IA
# Inicializacao do Pygame e da janela
pygame.init()
LARGURA_TELA = 800
ALTURA_TELA = 700



tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Atividade 11 - Animacoes")
relogio = pygame.time.Clock()
PASTA_PROJETO = Path(__file__).resolve().parent

#lkruasklruu - aqui é o Daniel comentando, e não a IA
# Carregamento dos quatro frames da animacao constante
frames_constantes = []

for numero in range(1, 5):
    nome_arquivo = f"Hero_Walk_{numero:02d}.png"
    caminho = PASTA_PROJETO / "assets" / nome_arquivo
    imagem = pygame.image.load(str(caminho)).convert_alpha()
    frames_constantes.append(imagem)

#m,cxnbv.x,cdnfglskdfhr - aqui é o Daniel comentando, e não a IA
# Carregamento da spritesheet do Mega Man (5 colunas x 2 linhas, 60x64 cada)
caminho_spritesheet = PASTA_PROJETO / "megaman_spritesheet.png"
spritesheet = pygame.image.load(str(caminho_spritesheet)).convert_alpha()

LARGURA_FRAME = 60
ALTURA_FRAME = 64
ESCALA = 2



def recortar_linha(spritesheet, linha):
    frames = []

    for coluna in range(5):
        x_recorte = coluna * LARGURA_FRAME
        y_recorte = linha * ALTURA_FRAME
        area = pygame.Rect(x_recorte, y_recorte, LARGURA_FRAME, ALTURA_FRAME)
        recorte = spritesheet.subsurface(area).copy()
        tamanho = (LARGURA_FRAME * ESCALA, ALTURA_FRAME * ESCALA)
        frame_ampliado = pygame.transform.scale(recorte, tamanho)
        frames.append(frame_ampliado)

    return frames


frames_tecla = recortar_linha(spritesheet, 0)
frames_evento = recortar_linha(spritesheet, 1)
LARGURA_SPRITE = LARGURA_FRAME * ESCALA

#-109234u-jorqw´f - aqui é o Daniel comentando, e não a IA
# Configuracao do tempo das tres animacoes
INTERVALO_CONSTANTE = 0.10
INTERVALO_TECLA = 0.12
INTERVALO_EVENTO = 0.12
DURACAO_EVENTO = len(frames_evento) * INTERVALO_EVENTO



#askdlfjnaçlsdfjk - aqui é o Daniel comentando, e não a IA
# Variaveis que guardam o tempo, o frame atual e as posicoes
tempo_constante = 0.0
tempo_tecla = 0.0
tempo_evento = 0.0

indice_constante = 0
indice_tecla = 0
indice_evento = 0

#pwoievmtrpwoeti - aqui é o Daniel comentando, e não a IA
# Animacao 2: personagem que anda para a direita enquanto ESPACO esta pressionado
X_INICIAL_TECLA = 20.0
x_tecla = X_INICIAL_TECLA
VELOCIDADE_TECLA = 200.0


#plaksmdcpeoriuhtpweroiuy - aqui é o Daniel comentando, e não a IA
# Animacao 3: toca uma vez com um "pulo" (sobe e desce no lugar)
animando_evento = False
X_EVENTO = 420
Y_BASE_EVENTO = 70
ALTURA_PULO = 40
y_evento = Y_BASE_EVENTO

# personagem extra: anda com as setas e pula com a seta para cima
x_jogador = 340.0
Y_CHAO_JOGADOR = 540
y_jogador = Y_CHAO_JOGADOR
VELOCIDADE_JOGADOR = 250.0
FORCA_PULO = -700.0
GRAVIDADE = 1900.0
INTERVALO_PULO = 0.15

velocidade_y = 0.0
no_chao = True
olhando_direita = True
tempo_andar = 0.0
tempo_no_ar = 0.0

#kjdefpçgvjwnrtep - aqui é o Daniel comentando, e não a IA
# Textos que identificam cada animacao
fonte = pygame.font.Font(None, 26)
textos = [
    fonte.render("1. Animacao constante", True, (20, 20, 20)),
    fonte.render("2. Segure ESPACO para andar", True, (20, 20, 20)),
    fonte.render("3. Pressione E ou clique esquerdo", True, (20, 20, 20)),
    fonte.render("4. Setas esquerda/direita para andar, seta para cima para pular", True, (20, 20, 20)),
]




#qowpuieripofweqlckj - aqui é o Daniel comentando, e não a IA
# Game Loop: o jogo continua ate a janela ser fechada
rodando = True

while rodando:
    dt = relogio.tick(60) / 1000.0

    # Processar eventos pontuais: fechar, pressionar E ou clicar
    for evento in pygame.event.get():
        iniciar_evento = False

        if evento.type == pygame.QUIT:
            rodando = False
        elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_e:
            iniciar_evento = True
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            iniciar_evento = True
        elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_UP:
            # so pula se estiver no chao
            if no_chao:
                velocidade_y = FORCA_PULO
                no_chao = False
                tempo_no_ar = 0.0

        if iniciar_evento and not animando_evento:
            animando_evento = True
            tempo_evento = 0.0
            indice_evento = 0

    if not rodando:
        break

    # Consultar o estado atual do teclado (tecla sendo segurada)
    teclas = pygame.key.get_pressed()

    # avanca continuamente, sem precisar de entrada
    tempo_constante = tempo_constante + dt
    indice_constante = int(tempo_constante / INTERVALO_CONSTANTE)
    indice_constante = indice_constante % len(frames_constantes)

    # anima e move para a direita somente enquanto espaço estiver pressionado. Ao soltar, para no lugar.
    if teclas[pygame.K_SPACE]:
        tempo_tecla = tempo_tecla + dt
        quadros_passados = int(tempo_tecla / INTERVALO_TECLA)
        indice_tecla = quadros_passados % len(frames_tecla)

        x_tecla = x_tecla + (VELOCIDADE_TECLA * dt)

        # Saiu pela direita: volta pela esquerda
        if x_tecla > LARGURA_TELA:
            x_tecla = -LARGURA_SPRITE
    else:
        tempo_tecla = 0.0
        indice_tecla = 0

    # toca uma vez a partir do evento (como um pulo)
    if animando_evento:
        tempo_evento = tempo_evento + dt

        if tempo_evento >= DURACAO_EVENTO:
            tempo_evento = DURACAO_EVENTO
            animando_evento = False

        indice_evento = int(tempo_evento / INTERVALO_EVENTO)
        if indice_evento >= len(frames_evento):
            indice_evento = len(frames_evento) - 1

        # pulo
        if tempo_evento < DURACAO_EVENTO / 2:
            y_evento = Y_BASE_EVENTO - ALTURA_PULO
        else:
            y_evento = Y_BASE_EVENTO

    if not animando_evento:
        indice_evento = 0
        y_evento = Y_BASE_EVENTO

    # personagem extra: ve para qual lado as setas mandam andar
    direcao = 0
    if teclas[pygame.K_LEFT]:
        direcao = direcao - 1
    if teclas[pygame.K_RIGHT]:
        direcao = direcao + 1

    if direcao != 0:
        x_jogador = x_jogador + (direcao * VELOCIDADE_JOGADOR * dt)
        olhando_direita = direcao > 0
        tempo_andar = tempo_andar + dt
    else:
        tempo_andar = 0.0

    # nao deixa sair da tela
    if x_jogador < 0:
        x_jogador = 0
    if x_jogador > LARGURA_TELA - LARGURA_SPRITE:
        x_jogador = LARGURA_TELA - LARGURA_SPRITE

    # gravidade puxando para baixo enquanto esta no ar
    if not no_chao:
        tempo_no_ar = tempo_no_ar + dt
        velocidade_y = velocidade_y + (GRAVIDADE * dt)
        y_jogador = y_jogador + (velocidade_y * dt)

        # chegou no chao
        if y_jogador >= Y_CHAO_JOGADOR:
            y_jogador = Y_CHAO_JOGADOR
            velocidade_y = 0.0
            no_chao = True

    # escolhe o frame: pulando, andando ou parado
    if not no_chao:
        indice_jogador = int(tempo_no_ar / INTERVALO_PULO)
        if indice_jogador >= len(frames_evento):
            indice_jogador = len(frames_evento) - 1
        frame_jogador = frames_evento[indice_jogador]
    elif direcao != 0:
        indice_jogador = int(tempo_andar / INTERVALO_TECLA) % len(frames_tecla)
        frame_jogador = frames_tecla[indice_jogador]
    else:
        frame_jogador = frames_tecla[0]

    # vira o desenho quando estiver indo para a esquerda
    if not olhando_direita:
        frame_jogador = pygame.transform.flip(frame_jogador, True, False)

    # Desenhar o quadro atual
    tela.fill((247, 247, 247))

    tela.blit(textos[0], (20, 10))
    tela.blit(frames_constantes[indice_constante], (20, 40))

    tela.blit(textos[1], (20, 205))
    tela.blit(frames_tecla[indice_tecla], (round(x_tecla), 235))

    tela.blit(textos[2], (X_EVENTO, 10))
    tela.blit(frames_evento[indice_evento], (X_EVENTO, round(y_evento)))

    tela.blit(textos[3], (20, 380))
    tela.blit(frame_jogador, (round(x_jogador), round(y_jogador)))

    pygame.display.flip()

pygame.quit()
