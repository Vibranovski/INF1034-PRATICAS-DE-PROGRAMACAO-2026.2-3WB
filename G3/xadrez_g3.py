# -*- coding: utf-8 -*-
"""
XADREZ ULTIMATE — G3 / INF1034 — versão com programação básica
(Atualizado com detecção de Xeque-Mate e Empate)
"""

import pygame
import sys

pygame.init()

DIMENSAO = 8
TAMANHO_QUADRADO = 80
LARGURA = DIMENSAO * TAMANHO_QUADRADO
ALTURA = DIMENSAO * TAMANHO_QUADRADO

COR_BRANCA = (240, 217, 181)
COR_PRETA = (181, 136, 99)
COR_VERDE = (105, 205, 110)
COR_SELECAO = (255, 215, 60)

screen = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Xadrez ULTIMATE - Regras Oficiais")
clock = pygame.time.Clock()
fonte = pygame.font.SysFont("arial", 24, bold=True)

tabuleiro_estado = [
    ["pT", "pC", "pB", "pD", "pR", "pB", "pC", "pT"],
    ["pP", "pP", "pP", "pP", "pP", "pP", "pP", "pP"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
    ["bT", "bC", "bB", "bD", "bR", "bB", "bC", "bT"],
]

imagens = [None] * 12
imagens_selecionadas = [None] * 12

# Caminho completo para a imagem conforme especificado
CAMINHO_SPRITE = r"D:\PUC RIO\Práticas de PROG INF1034\Chess_Pieces.png"

turno_atual = "b"
peca_selecionada = None
origem_selecionada = None
movimentos_disponiveis = []

animando = False
peca_movendo = None
pos_atual_anim_x = 0.0
pos_atual_anim_y = 0.0
destino_anim_x = 0.0
destino_anim_y = 0.0
destino_final = None
jogada_animacao = None

movimentou = [[False, False, False], [False, False, False]]
en_passant = None
promocao_pendente = None
cursor_linha = 7
cursor_coluna = 0

# Variável booleana para controlar se o jogo acabou
jogo_encerrado = False

CODIGOS_PECAS = [
    "bP", "bT", "bB", "bC", "bD", "bR",
    "pP", "pT", "pB", "pC", "pD", "pR"
]

def indice_peca(codigo):
    for indice in range(len(CODIGOS_PECAS)):
        if CODIGOS_PECAS[indice] == codigo:
            return indice

def indice_cor(cor):
    if cor == "b":
        return 0
    else:
        return 1

def nome_cor(cor):
    if cor == "b":
        return "brancas"
    else:
        return "pretas"

def dentro_tabuleiro(linha, coluna):
    return 0 <= linha < DIMENSAO and 0 <= coluna < DIMENSAO

def coordenada_xadrez(linha, coluna):
    letra = "abcdefgh"[coluna]
    fileira = DIMENSAO - linha
    return f"{letra}{fileira}"

def exibir_movimentos_legais(movimentos):
    casas = []
    for l, c in movimentos:
        casas.append(coordenada_xadrez(l, c))
    print("Movimentos legais:", casas)

def cor_adversaria(cor):
    if cor == "b":
        return "p"
    return "b"

def copiar_tabuleiro(tabuleiro):
    copia = []
    for linha in tabuleiro:
        nova_linha = []
        for peca in linha:
            nova_linha.append(peca)
        copia.append(nova_linha)
    return copia

def mostrar_mensagem(texto):
    print(texto)
    pygame.display.set_caption("Xadrez ULTIMATE - " + texto)

def remover_fundo(sprite):
    largura, altura = sprite.get_size()
    visitados = []
    for y in range(altura):
        linha = []
        for x in range(largura):
            linha.append(False)
        visitados.append(linha)
    fila = []
    for x in range(largura):
        fila.append((x, 0))
        fila.append((x, altura - 1))
    for y in range(altura):
        fila.append((0, y))
        fila.append((largura - 1, y))

    inicio = 0
    while inicio < len(fila):
        x, y = fila[inicio]
        inicio = inicio + 1
        if not visitados[y][x]:
            visitados[y][x] = True
            cor = sprite.get_at((x, y))
            if cor[0] >= 240 and cor[1] >= 240 and (cor[2] >= 240):
                sprite.set_at((x, y), (255, 255, 255, 0))
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    nx = x + dx
                    ny = y + dy
                    if dentro_imagem(nx, ny, largura, altura):
                        if not visitados[ny][nx]:
                            fila.append((nx, ny))
    return sprite

def dentro_imagem(x, y, largura, altura):
    return 0 <= x < largura and 0 <= y < altura

def carregar_imagens():
    sprite_sheet = pygame.image.load(str(CAMINHO_SPRITE)).convert_alpha()
    largura_original, altura_original = sprite_sheet.get_size()
    coordenadas = [
        (210, 80, 290, 520), (620, 80, 310, 520), (1050, 80, 310, 520), (1460, 80, 320, 520),
        (210, 1210, 290, 680), (620, 1210, 310, 680), (210, 660, 290, 520), (620, 660, 310, 520),
        (1050, 660, 310, 520), (1460, 660, 320, 520), (1050, 1210, 310, 680), (1460, 1210, 310, 680)
    ]
    escala_x = largura_original / 2048
    escala_y = altura_original / 2048
    for indice in range(len(CODIGOS_PECAS)):
        codigo = CODIGOS_PECAS[indice]
        dados = coordenadas[indice]
        x, y, largura, altura = dados
        x = round(x * escala_x)
        y = round(y * escala_y)
        largura = round(largura * escala_x)
        altura = round(altura * escala_y)
        sprite = sprite_sheet.subsurface(pygame.Rect(x, y, largura, altura)).copy()
        proporcao = min(65 / largura, 65 / altura)
        nova_largura = max(1, round(largura * proporcao))
        nova_altura = max(1, round(altura * proporcao))
        sprite_normal = pygame.transform.smoothscale(sprite, (nova_largura, nova_altura))
        imagens[indice_peca(codigo)] = remover_fundo(sprite_normal)
        proporcao_zoom = min(78 / largura, 78 / altura)
        largura_zoom = max(1, round(largura * proporcao_zoom))
        altura_zoom = max(1, round(altura * proporcao_zoom))
        sprite_zoom = pygame.transform.smoothscale(sprite, (largura_zoom, altura_zoom))
        imagens_selecionadas[indice_peca(codigo)] = remover_fundo(sprite_zoom)

def desenhar_tabuleiro(screen):
    for linha in range(DIMENSAO):
        for coluna in range(DIMENSAO):
            if (linha + coluna) % 2 == 0:
                cor = COR_BRANCA
            else:
                cor = COR_PRETA
            pygame.draw.rect(screen, cor, (coluna * TAMANHO_QUADRADO, linha * TAMANHO_QUADRADO, TAMANHO_QUADRADO, TAMANHO_QUADRADO))
            if origem_selecionada is not None and (linha, coluna) in movimentos_disponiveis:
                centro_x = coluna * TAMANHO_QUADRADO + TAMANHO_QUADRADO // 2
                centro_y = linha * TAMANHO_QUADRADO + TAMANHO_QUADRADO // 2
                pygame.draw.circle(screen, COR_VERDE, (centro_x, centro_y), 15)
    if origem_selecionada is not None:
        linha, coluna = origem_selecionada
        pygame.draw.rect(screen, COR_SELECAO, (coluna * TAMANHO_QUADRADO, linha * TAMANHO_QUADRADO, TAMANHO_QUADRADO, TAMANHO_QUADRADO), 4)

def desenhar_coordenadas(screen):
    fonte_casas = pygame.font.SysFont("arial", 15, bold=True)
    for linha in range(DIMENSAO):
        numero = str(DIMENSAO - linha)
        cor_texto = COR_PRETA if linha % 2 == 0 else COR_BRANCA
        texto = fonte_casas.render(numero, True, cor_texto)
        screen.blit(texto, (4, linha * TAMANHO_QUADRADO + 3))
    for coluna in range(8):
        letra = "abcdefgh"[coluna]
        cor_texto = COR_BRANCA if coluna % 2 == 0 else COR_PRETA
        texto = fonte_casas.render(letra, True, cor_texto)
        x = (coluna + 1) * TAMANHO_QUADRADO - texto.get_width() - 5
        y = ALTURA - texto.get_height() - 3
        screen.blit(texto, (x, y))

def desenhar_pecas(screen):
    for linha in range(DIMENSAO):
        for coluna in range(DIMENSAO):
            peca = tabuleiro_estado[linha][coluna]
            if peca == "--":
                continue
            if animando and (linha, coluna) == origem_selecionada:
                continue
            if not animando and origem_selecionada == (linha, coluna):
                imagem = imagens_selecionadas[indice_peca(peca)]
            else:
                imagem = imagens[indice_peca(peca)]
            largura = imagem.get_width()
            altura = imagem.get_height()
            x = coluna * TAMANHO_QUADRADO + (TAMANHO_QUADRADO - largura) // 2
            y = linha * TAMANHO_QUADRADO + (TAMANHO_QUADRADO - altura) // 2
            screen.blit(imagem, (x, y))

def movimentos_basicos(tabuleiro, linha, coluna, considerar_en_passant=True):
    peca = tabuleiro[linha][coluna]
    if peca == "--":
        return []
    cor = peca[0]
    tipo = peca[1]
    movimentos = []

    if tipo == "P":
        direcao = -1 if cor == "b" else 1
        linha_inicial = 6 if cor == "b" else 1
        proxima_linha = linha + direcao
        if dentro_tabuleiro(proxima_linha, coluna):
            if tabuleiro[proxima_linha][coluna] == "--":
                movimentos.append((proxima_linha, coluna))
                duas_linhas = linha + 2 * direcao
                if linha == linha_inicial and tabuleiro[duas_linhas][coluna] == "--":
                    movimentos.append((duas_linhas, coluna))
        for deslocamento in [-1, 1]:
            nova_coluna = coluna + deslocamento
            if dentro_tabuleiro(proxima_linha, nova_coluna):
                alvo = tabuleiro[proxima_linha][nova_coluna]
                if alvo != "--" and alvo[0] != cor and alvo[1] != "R":
                    movimentos.append((proxima_linha, nova_coluna))
                if considerar_en_passant and en_passant == (proxima_linha, nova_coluna):
                    if tabuleiro[linha][nova_coluna] == cor_adversaria(cor) + "P":
                        movimentos.append((proxima_linha, nova_coluna))

    elif tipo == "C":
        deslocamentos = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for dl, dc in deslocamentos:
            nl, nc = linha + dl, coluna + dc
            if dentro_tabuleiro(nl, nc):
                alvo = tabuleiro[nl][nc]
                if alvo == "--" or (alvo[0] != cor and alvo[1] != "R"):
                    movimentos.append((nl, nc))

    elif tipo in ["T", "B", "D"]:
        direcoes = []
        if tipo in ["T", "D"]:
            direcoes += [(-1, 0), (1, 0), (0, -1), (0, 1)]
        if tipo in ["B", "D"]:
            direcoes += [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dl, dc in direcoes:
            nl, nc = linha + dl, coluna + dc
            while dentro_tabuleiro(nl, nc):
                alvo = tabuleiro[nl][nc]
                if alvo == "--":
                    movimentos.append((nl, nc))
                else:
                    if alvo[0] != cor and alvo[1] != "R":
                        movimentos.append((nl, nc))
                    break
                nl += dl
                nc += dc

    elif tipo == "R":
        for dl in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dl == 0 and dc == 0:
                    continue
                nl, nc = linha + dl, coluna + dc
                if dentro_tabuleiro(nl, nc):
                    alvo = tabuleiro[nl][nc]
                    if alvo == "--" or (alvo[0] != cor and alvo[1] != "R"):
                        movimentos.append((nl, nc))
    return movimentos

def casa_atacada(tabuleiro, linha, coluna, atacante):
    for l in range(DIMENSAO):
        for c in range(DIMENSAO):
            peca = tabuleiro[l][c]
            if peca == "--" or peca[0] != atacante:
                continue
            tipo = peca[1]
            if tipo == "P":
                direcao = -1 if atacante == "b" else 1
                if linha == l + direcao and abs(coluna - c) == 1:
                    return True
            elif tipo == "C":
                dl, dc = abs(linha - l), abs(coluna - c)
                if (dl == 2 and dc == 1) or (dl == 1 and dc == 2):
                    return True
            elif tipo == "R":
                if max(abs(linha - l), abs(coluna - c)) == 1:
                    return True
            elif tipo in ["T", "B", "D"]:
                dl = linha - l
                dc = coluna - c
                movimento_reto = dl == 0 or dc == 0
                movimento_diagonal = abs(dl) == abs(dc)
                permitido = (tipo == "T" and movimento_reto) or (tipo == "B" and movimento_diagonal) or (tipo == "D" and (movimento_reto or movimento_diagonal))
                if not permitido:
                    continue
                direcao_linha = 1 if dl > 0 else (-1 if dl < 0 else 0)
                direcao_coluna = 1 if dc > 0 else (-1 if dc < 0 else 0)
                atual_linha, atual_coluna = l + direcao_linha, c + direcao_coluna
                caminho_livre = True
                while (atual_linha, atual_coluna) != (linha, coluna):
                    if tabuleiro[atual_linha][atual_coluna] != "--":
                        caminho_livre = False
                        break
                    atual_linha += direcao_linha
                    atual_coluna += direcao_coluna
                if caminho_livre:
                    return True
    return False

def localizar_rei(tabuleiro, cor):
    codigo_rei = cor + "R"
    for linha in range(DIMENSAO):
        for coluna in range(DIMENSAO):
            if tabuleiro[linha][coluna] == codigo_rei:
                return (linha, coluna)
    return None

def rei_em_xeque(tabuleiro, cor):
    posicao_rei = localizar_rei(tabuleiro, cor)
    if posicao_rei is None:
        return True
    linha, coluna = posicao_rei
    return casa_atacada(tabuleiro, linha, coluna, cor_adversaria(cor))

def movimentos_roque(tabuleiro, cor):
    movimentos = []
    linha = 7 if cor == "b" else 0
    if tabuleiro[linha][4] != cor + "R" or movimentou[indice_cor(cor)][0] or rei_em_xeque(tabuleiro, cor):
        return movimentos
    adversario = cor_adversaria(cor)
    if not movimentou[indice_cor(cor)][2] and tabuleiro[linha][7] == cor + "T":
        if tabuleiro[linha][5] == "--" and tabuleiro[linha][6] == "--":
            if not casa_atacada(tabuleiro, linha, 5, adversario) and not casa_atacada(tabuleiro, linha, 6, adversario):
                movimentos.append((linha, 6))
    if not movimentou[indice_cor(cor)][1] and tabuleiro[linha][0] == cor + "T":
        if tabuleiro[linha][1] == "--" and tabuleiro[linha][2] == "--" and tabuleiro[linha][3] == "--":
            if not casa_atacada(tabuleiro, linha, 3, adversario) and not casa_atacada(tabuleiro, linha, 2, adversario):
                movimentos.append((linha, 2))
    return movimentos

def simular_movimento(tabuleiro, origem, destino):
    copia = copiar_tabuleiro(tabuleiro)
    lo, co = origem
    ld, cd = destino
    peca = copia[lo][co]
    copia[lo][co] = "--"
    if peca[1] == "P" and co != cd and copia[ld][cd] == "--":
        copia[lo][cd] = "--"
    if peca[1] == "R" and abs(cd - co) == 2:
        if cd == 6:
            copia[lo][5] = copia[lo][7]
            copia[lo][7] = "--"
        elif cd == 2:
            copia[lo][3] = copia[lo][0]
            copia[lo][0] = "--"
    copia[ld][cd] = peca
    return copia

def movimentos_legais(tabuleiro, linha, coluna):
    peca = tabuleiro[linha][coluna]
    if peca == "--":
        return []
    cor = peca[0]
    movimentos = movimentos_basicos(tabuleiro, linha, coluna)
    if peca[1] == "R":
        movimentos += movimentos_roque(tabuleiro, cor)
    movimentos_validos = []
    for destino in movimentos:
        copia = simular_movimento(tabuleiro, (linha, coluna), destino)
        if not rei_em_xeque(copia, cor):
            movimentos_validos.append(destino)
    return movimentos_validos

def tem_movimentos_legais(tabuleiro, cor):
    for linha in range(DIMENSAO):
        for coluna in range(DIMENSAO):
            peca = tabuleiro[linha][coluna]
            if peca != "--" and peca[0] == cor:
                if len(movimentos_legais(tabuleiro, linha, coluna)) > 0:
                    return True
    return False

def atualizar_direitos_roque(peca, origem, capturada, destino):
    linha, coluna = origem
    cor = peca[0]
    if peca[1] == "R":
        movimentou[indice_cor(cor)][0] = True
    elif peca[1] == "T":
        linha_inicial = 7 if cor == "b" else 0
        if linha == linha_inicial:
            if coluna == 0:
                movimentou[indice_cor(cor)][1] = True
            elif coluna == 7:
                movimentou[indice_cor(cor)][2] = True
    if capturada != "--" and capturada[1] == "T":
        cor_capturada = capturada[0]
        linha_inicial = 7 if cor_capturada == "b" else 0
        ld, cd = destino
        if ld == linha_inicial:
            if cd == 0:
                movimentou[indice_cor(cor_capturada)][1] = True
            elif cd == 7:
                movimentou[indice_cor(cor_capturada)][2] = True

def iniciar_animacao(origem, destino):
    global animando, peca_movendo, pos_atual_anim_x, pos_atual_anim_y, destino_anim_x, destino_anim_y, destino_final, jogada_animacao
    lo, co = origem
    ld, cd = destino
    peca_movendo = tabuleiro_estado[lo][co]
    imagem = imagens[indice_peca(peca_movendo)]
    largura, altura = imagem.get_width(), imagem.get_height()
    pos_atual_anim_x = co * TAMANHO_QUADRADO + (TAMANHO_QUADRADO - largura) // 2
    pos_atual_anim_y = lo * TAMANHO_QUADRADO + (TAMANHO_QUADRADO - altura) // 2
    destino_anim_x = cd * TAMANHO_QUADRADO + (TAMANHO_QUADRADO - largura) // 2
    destino_anim_y = ld * TAMANHO_QUADRADO + (TAMANHO_QUADRADO - altura) // 2
    destino_final = destino
    jogada_animacao = [origem, destino, peca_movendo]
    animando = True

def finalizar_jogada():
    global en_passant, turno_atual, promocao_pendente, jogada_animacao, peca_selecionada, origem_selecionada, movimentos_disponiveis, jogo_encerrado

    origem = jogada_animacao[0]
    destino = jogada_animacao[1]
    peca = jogada_animacao[2]
    lo, co = origem
    ld, cd = destino
    capturada = tabuleiro_estado[ld][cd]

    if peca[1] == "P" and co != cd and capturada == "--":
        tabuleiro_estado[lo][cd] = "--"
        mostrar_mensagem("Captura en passant!")

    atualizar_direitos_roque(peca, origem, capturada, destino)
    tabuleiro_estado[lo][co] = "--"
    tabuleiro_estado[ld][cd] = peca

    if peca[1] == "R" and abs(cd - co) == 2:
        if cd == 6:
            tabuleiro_estado[ld][5] = tabuleiro_estado[ld][7]
            tabuleiro_estado[ld][7] = "--"
        elif cd == 2:
            tabuleiro_estado[ld][3] = tabuleiro_estado[ld][0]
            tabuleiro_estado[ld][0] = "--"

    en_passant = None
    if peca[1] == "P" and abs(ld - lo) == 2:
        en_passant = ((lo + ld) // 2, co)

    if peca[1] == "P":
        ultima_linha = 0 if peca[0] == "b" else 7
        if ld == ultima_linha:
            promocao_pendente = (ld, cd)
            mostrar_mensagem("PROMOÇÃO: pressione D, T, B ou C")
            jogada_animacao = None
            return

    turno_atual = cor_adversaria(turno_atual)
    peca_selecionada = None
    origem_selecionada = None
    movimentos_disponiveis = []
    jogada_animacao = None

    if not tem_movimentos_legais(tabuleiro_estado, turno_atual):
        jogo_encerrado = True
        vencedor = nome_cor(cor_adversaria(turno_atual))
        if rei_em_xeque(tabuleiro_estado, turno_atual):
            mostrar_mensagem(f"XEQUE-MATE! Vitória das {vencedor}!")
        else:
            mostrar_mensagem("EMPATE por Afogamento (Stalemate)!")
    else:
        if rei_em_xeque(tabuleiro_estado, turno_atual):
            mostrar_mensagem("XEQUE! Vez das " + nome_cor(turno_atual))
        else:
            mostrar_mensagem("Vez das " + nome_cor(turno_atual))

def promover_peao(tipo):
    global promocao_pendente, turno_atual, peca_selecionada, origem_selecionada, movimentos_disponiveis, jogo_encerrado
    if promocao_pendente is None or tipo not in ["D", "T", "B", "C"]:
        return
    linha, coluna = promocao_pendente
    peca = tabuleiro_estado[linha][coluna]
    cor = peca[0]
    tabuleiro_estado[linha][coluna] = cor + tipo
    promocao_pendente = None
    
    turno_atual = cor_adversaria(turno_atual)
    peca_selecionada = None
    origem_selecionada = None
    movimentos_disponiveis = []

    if not tem_movimentos_legais(tabuleiro_estado, turno_atual):
        jogo_encerrado = True
        vencedor = nome_cor(cor_adversaria(turno_atual))
        if rei_em_xeque(tabuleiro_estado, turno_atual):
            mostrar_mensagem(f"Promoção realizada! XEQUE-MATE! Vitória das {vencedor}!")
        else:
            mostrar_mensagem("Promoção realizada! EMPATE por Afogamento!")
    else:
        if rei_em_xeque(tabuleiro_estado, turno_atual):
            mostrar_mensagem("Promoção realizada! XEQUE!")
        else:
            mostrar_mensagem("Promoção realizada!")

def selecionar_casa(linha, coluna):
    global peca_selecionada, origem_selecionada, movimentos_disponiveis
    
    if jogo_encerrado:
        return
        
    if not dentro_tabuleiro(linha, coluna) or animando or promocao_pendente is not None:
        return
        
    peca = tabuleiro_estado[linha][coluna]
    if origem_selecionada is None:
        if peca != "--" and peca[0] == turno_atual:
            peca_selecionada = peca
            origem_selecionada = (linha, coluna)
            movimentos_disponiveis = movimentos_legais(tabuleiro_estado, linha, coluna)
        return
    if origem_selecionada == (linha, coluna):
        peca_selecionada = None
        origem_selecionada = None
        movimentos_disponiveis = []
        return
    if peca != "--" and peca[0] == turno_atual:
        peca_selecionada = peca
        origem_selecionada = (linha, coluna)
        movimentos_disponiveis = movimentos_legais(tabuleiro_estado, linha, coluna)
        return
    destino = (linha, coluna)
    if destino in movimentos_disponiveis:
        iniciar_animacao(origem_selecionada, destino)
    else:
        mostrar_mensagem("Movimento inválido!")

def atualizar_animacao(dt):
    global animando, pos_atual_anim_x, pos_atual_anim_y
    if not animando:
        return
    velocidade_deslize = 0.015
    fator = min(velocidade_deslize * dt, 1.0)
    pos_atual_anim_x += (destino_anim_x - pos_atual_anim_x) * fator
    pos_atual_anim_y += (destino_anim_y - pos_atual_anim_y) * fator
    if abs(destino_anim_x - pos_atual_anim_x) < 0.5 and abs(destino_anim_y - pos_atual_anim_y) < 0.5:
        pos_atual_anim_x = destino_anim_x
        pos_atual_anim_y = destino_anim_y
        animando = False
        finalizar_jogada()

def desenhar_animacao(screen):
    if not animando:
        return
    imagem = imagens[indice_peca(peca_movendo)]
    screen.blit(imagem, (pos_atual_anim_x, pos_atual_anim_y))

def desenhar_promocao(screen):
    if promocao_pendente is None:
        return
    camada = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
    camada.fill((0, 0, 0, 170))
    screen.blit(camada, (0, 0))
    caixa = pygame.Rect(60, 250, 520, 140)
    pygame.draw.rect(screen, (245, 235, 215), caixa, border_radius=12)
    pygame.draw.rect(screen, (90, 60, 40), caixa, 3, border_radius=12)
    screen.blit(fonte.render("PROMOÇÃO DO PEÃO", True, (40, 40, 40)), (185, 265))
    screen.blit(fonte.render("D = Dama   T = Torre", True, (40, 40, 40)), (175, 310))
    screen.blit(fonte.render("B = Bispo   C = Cavalo", True, (40, 40, 40)), (165, 345))

carregar_imagens()
mostrar_mensagem("Vez das brancas")

while True:
    clock.tick(60)
    dt = clock.get_time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if jogo_encerrado:
                continue
            if promocao_pendente is not None:
                if event.key == pygame.K_d: promover_peao("D")
                elif event.key == pygame.K_t: promover_peao("T")
                elif event.key == pygame.K_b: promover_peao("B")
                elif event.key == pygame.K_c: promover_peao("C")
                continue
            if animando:
                continue
            if event.key == pygame.K_UP: cursor_linha = max(0, cursor_linha - 1)
            elif event.key == pygame.K_DOWN: cursor_linha = min(7, cursor_linha + 1)
            elif event.key == pygame.K_LEFT: cursor_coluna = max(0, cursor_coluna - 1)
            elif event.key == pygame.K_RIGHT: cursor_coluna = min(7, cursor_coluna + 1)
            elif event.key == pygame.K_RETURN: selecionar_casa(cursor_linha, cursor_coluna)
            elif event.key == pygame.K_ESCAPE:
                peca_selecionada, origem_selecionada, movimentos_disponiveis = None, None, []

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if not animando and promocao_pendente is None:
                    x, y = event.pos
                    cursor_linha, cursor_coluna = y // TAMANHO_QUADRADO, x // TAMANHO_QUADRADO
                    selecionar_casa(cursor_linha, cursor_coluna)

    atualizar_animacao(dt)

    screen.fill((56, 203, 171))
    desenhar_tabuleiro(screen)
    desenhar_pecas(screen)
    desenhar_animacao(screen)
    pygame.draw.rect(screen, (50, 100, 230), (cursor_coluna * TAMANHO_QUADRADO, cursor_linha * TAMANHO_QUADRADO, TAMANHO_QUADRADO, TAMANHO_QUADRADO), 2)
    desenhar_coordenadas(screen)
    desenhar_promocao(screen)

    pygame.display.update()
