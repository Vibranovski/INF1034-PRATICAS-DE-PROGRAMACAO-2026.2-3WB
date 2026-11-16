# -*- coding: utf-8 -*-
"""
XADREZ ULTIMATE — G3 / INF1034 — versão com programação básica

COMO EXECUTAR
1. Instale o PyGame: python -m pip install pygame
2. Coloque Chess_Pieces.png na mesma pasta do programa.
3. Abra o terminal nessa pasta e execute este arquivo.
   Ou altere CAMINHO_SPRITE para o caminho completo da sua imagem.

CONTROLES
Mouse: clique na peça e depois em um destino com bola verde.
Teclado: setas para mover o cursor; Enter para selecionar/jogar.
Escape: cancelar seleção. Promoção: D, T, B ou C.

ESTRUTURAS
Matriz 8 x 8 para o tabuleiro; listas para imagens, destinos e jogadas;
matriz de booleanos para os direitos de roque; funções, if/elif/else,
for e while. As coordenadas de uma casa são pares (linha, coluna).
None significa que ainda não existe seleção, imagem ou jogada pendente.
global permite que uma função atualize as variáveis de controle do jogo.

ESCOPO DESTE ARQUIVO
Mantém as etapas 1 a 4 do código fornecido, a detecção de xeque e a
animação de deslocamento. Xeque-mate, empates, ranking/TXT, animações
por sprite sheets, saltos e giros ficam para as próximas etapas.
As cores bege/marrom e as bolas verdes são preservadas.
"""

# 01. BIBLIOTECAS
# PyGame cuida da interface; sys permite encerrar o programa.
import pygame
import sys

# 02. CONFIGURAÇÃO DA JANELA
# Inicializa os recursos do PyGame antes de criar a janela.
pygame.init()

# Cada casa mede 80 x 80 pixels; o tabuleiro possui 8 x 8 casas.
DIMENSAO = 8
TAMANHO_QUADRADO = 80
LARGURA = DIMENSAO * TAMANHO_QUADRADO
ALTURA = DIMENSAO * TAMANHO_QUADRADO

# 03. CORES
# Valores RGB: vermelho, verde e azul, de 0 a 255.
COR_BRANCA = (240, 217, 181)
COR_PRETA = (181, 136, 99)
COR_VERDE = (105, 205, 110)
COR_SELECAO = (255, 215, 60)

# Cria a janela, o relógio e a fonte utilizados pela interface.
screen = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Xadrez ULTIMATE - Regras Oficiais")
clock = pygame.time.Clock()
fonte = pygame.font.SysFont("arial", 24, bold=True)

# 04. MATRIZ DO TABULEIRO
# Cada linha da lista corresponde a uma fileira do tabuleiro.
# b = branca; p = preta; -- = casa vazia.
# P = peão; T = torre; B = bispo; C = cavalo; D = dama; R = rei.
# As pretas ficam no alto da tela; as brancas, na parte inferior.
# Matriz 8 × 8 com as posições iniciais das 32 peças.

tabuleiro_estado = [
    # Colunas: a     b     c     d     e     f     g     h
    ["pT", "pC", "pB", "pD", "pR", "pB", "pC", "pT"],  # 8
    ["pP", "pP", "pP", "pP", "pP", "pP", "pP", "pP"],  # 7
    ["--", "--", "--", "--", "--", "--", "--", "--"],  # 6
    ["--", "--", "--", "--", "--", "--", "--", "--"],  # 5
    ["--", "--", "--", "--", "--", "--", "--", "--"],  # 4
    ["--", "--", "--", "--", "--", "--", "--", "--"],  # 3
    ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],  # 2
    ["bT", "bC", "bB", "bD", "bR", "bB", "bC", "bT"],  # 1
]

# 05. IMAGENS DAS PEÇAS
# Listas paralelas: imagens normais e imagens ampliadas para seleção.
imagens = [None] * 12
imagens_selecionadas = [None] * 12

# Arquivo com as 12 peças. Altere somente este caminho se necessário.
CAMINHO_SPRITE = "Chess_Pieces.png"

# 06. CONTROLE DA PARTIDA
# As brancas começam. None representa a ausência de uma seleção.
turno_atual = "b"
peca_selecionada = None
origem_selecionada = None
movimentos_disponiveis = []

# Controle da animação: peça, posição atual e posição de chegada.
animando = False
peca_movendo = None
pos_atual_anim_x = 0.0
pos_atual_anim_y = 0.0
destino_anim_x = 0.0
destino_anim_y = 0.0
destino_final = None

# A jogada guarda [origem, destino, peça] enquanto a animação acontece.
jogada_animacao = None

# Direitos de roque: cada booleano registra se a peça já se movimentou.
# Linhas: 0 = brancas, 1 = pretas.
# Colunas: 0 = rei, 1 = torre esquerda, 2 = torre direita.
movimentou = [[False, False, False], [False, False, False]]

# Casa disponível para en passant apenas na resposta ao avanço duplo.
en_passant = None

# Posição do peão que aguarda a escolha entre dama, torre, bispo e cavalo.
promocao_pendente = None

# Posição do cursor controlado pelas setas do teclado.
cursor_linha = 7
cursor_coluna = 0

# Listas paralelas: o código e a imagem usam o mesmo índice.
CODIGOS_PECAS = [
    "bP",
    "bT",
    "bB",
    "bC",
    "bD",
    "bR",
    "pP",
    "pT",
    "pB",
    "pC",
    "pD",
    "pR",
]


# ------------------------------------------------------------
# INDICE PECA
# ------------------------------------------------------------
def indice_peca(codigo):
    """Procura o código na lista das 12 peças."""
    for indice in range(len(CODIGOS_PECAS)):
        if CODIGOS_PECAS[indice] == codigo:
            return indice


# ------------------------------------------------------------
# INDICE COR
# ------------------------------------------------------------
def indice_cor(cor):
    if cor == "b":
        return 0
    else:
        return 1


# ------------------------------------------------------------
# NOME COR
# ------------------------------------------------------------
def nome_cor(cor):
    if cor == "b":
        return "brancas"
    else:
        return "pretas"


# ------------------------------------------------------------
# DENTRO TABULEIRO
# ------------------------------------------------------------
def dentro_tabuleiro(linha, coluna):
    """
    Verifica se uma posição pertence ao tabuleiro.
    As linhas e colunas devem estar entre 0 e 7.
    """
    return 0 <= linha < DIMENSAO and 0 <= coluna < DIMENSAO


# ------------------------------------------------------------
# COORDENADA XADREZ
# ------------------------------------------------------------
def coordenada_xadrez(linha, coluna):
    """Converte índices da matriz (0 a 7) em casas como a1, e4 e h8."""
    letra = "abcdefgh"[coluna]
    fileira = DIMENSAO - linha
    return f"{letra}{fileira}"


# ------------------------------------------------------------
# EXIBIR MOVIMENTOS LEGAIS
# ------------------------------------------------------------
def exibir_movimentos_legais(movimentos):
    """Mostra os destinos legais com a notação tradicional do xadrez."""
    casas = []
    for l, c in movimentos:
        casas.append(coordenada_xadrez(l, c))
    print("Movimentos legais:", casas)


# ------------------------------------------------------------
# COR ADVERSARIA
# ------------------------------------------------------------
def cor_adversaria(cor):
    """
    Retorna a cor adversária.
    Se receber branco, retorna preto.
    Se receber preto, retorna branco.
    """
    if cor == "b":
        return "p"
    return "b"


# ------------------------------------------------------------
# COPIAR TABULEIRO
# ------------------------------------------------------------
def copiar_tabuleiro(tabuleiro):
    """
    Cria uma cópia independente da matriz.
    Isso permite simular movimentos sem modificar
    o tabuleiro original.
    """
    copia = []
    for linha in tabuleiro:
        nova_linha = []
        for peca in linha:
            nova_linha.append(peca)
        copia.append(nova_linha)
    return copia


# ------------------------------------------------------------
# MOSTRAR MENSAGEM
# ------------------------------------------------------------
def mostrar_mensagem(texto):
    """
    Exibe uma mensagem no terminal.
    Também altera o título da janela.
    """
    print(texto)
    pygame.display.set_caption("Xadrez ULTIMATE - " + texto)


# ------------------------------------------------------------
# REMOVER FUNDO
# ------------------------------------------------------------
def remover_fundo(sprite):
    """Percorre o fundo branco pelas bordas, usando lista e matriz booleana.
    Os pixels brancos internos das peças são preservados.
    """
    largura, altura = sprite.get_size()

    # Matriz booleana: cada pixel será analisado no máximo uma vez.
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

    # O índice avança pela lista sem precisar remover o primeiro elemento.
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


# ------------------------------------------------------------
# DENTRO IMAGEM
# ------------------------------------------------------------
def dentro_imagem(x, y, largura, altura):
    """Verifica se um pixel pertence à imagem."""
    return 0 <= x < largura and 0 <= y < altura


# ------------------------------------------------------------
# CARREGAR IMAGENS
# ------------------------------------------------------------
def carregar_imagens():
    """
    Carrega a sprite sheet e recorta as 12 peças.
    As coordenadas abaixo foram definidas
    individualmente para a imagem Chess_Pieces.png.
    Cada tupla contém:
    (x, y, largura, altura)
    """
    sprite_sheet = pygame.image.load(str(CAMINHO_SPRITE)).convert_alpha()
    largura_original, altura_original = sprite_sheet.get_size()

    # Cada recorte contém (x, y, largura, altura), na ordem de CODIGOS_PECAS.
    coordenadas = [
        (210, 80, 290, 520),
        (620, 80, 310, 520),
        (1050, 80, 310, 520),
        (1460, 80, 320, 520),
        (210, 1210, 290, 680),
        (620, 1210, 310, 680),
        (210, 660, 290, 520),
        (620, 660, 310, 520),
        (1050, 660, 310, 520),
        (1460, 660, 320, 520),
        (1050, 1210, 310, 680),
        (1460, 1210, 320, 680),
    ]

    # Os recortes são proporcionais à imagem de referência de 2048 x 2048.
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
        sprite_normal = pygame.transform.smoothscale(
            sprite, (nova_largura, nova_altura)
        )
        imagens[indice_peca(codigo)] = remover_fundo(sprite_normal)
        proporcao_zoom = min(78 / largura, 78 / altura)
        largura_zoom = max(1, round(largura * proporcao_zoom))
        altura_zoom = max(1, round(altura * proporcao_zoom))
        sprite_zoom = pygame.transform.smoothscale(sprite, (largura_zoom, altura_zoom))
        imagens_selecionadas[indice_peca(codigo)] = remover_fundo(sprite_zoom)


# ------------------------------------------------------------
# DESENHAR TABULEIRO
# ------------------------------------------------------------
def desenhar_tabuleiro(screen):
    """
    Desenha as 64 casas com as cores originais (bege e marrom).
    Quando uma peça está selecionada:
    - Desenha círculos verdes nas casas de destino legal.
    - Mantém a cor original de cada casa.
    - Destaca a casa selecionada com um contorno amarelo.
    """
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
                    TAMANHO_QUADRADO,
                ),
            )
            if (
                origem_selecionada is not None
                and (linha, coluna) in movimentos_disponiveis
            ):
                centro_x = coluna * TAMANHO_QUADRADO + TAMANHO_QUADRADO // 2
                centro_y = linha * TAMANHO_QUADRADO + TAMANHO_QUADRADO // 2

                # Bola verde no centro da casa: raio de 15 pixels.
                pygame.draw.circle(screen, COR_VERDE, (centro_x, centro_y), 15)
    if origem_selecionada is not None:
        linha, coluna = origem_selecionada
        pygame.draw.rect(
            screen,
            COR_SELECAO,
            (
                coluna * TAMANHO_QUADRADO,
                linha * TAMANHO_QUADRADO,
                TAMANHO_QUADRADO,
                TAMANHO_QUADRADO,
            ),
            4,
        )


# ------------------------------------------------------------
# DESENHAR COORDENADAS
# ------------------------------------------------------------
def desenhar_coordenadas(screen):
    """Exibe a-h nas colunas e 1-8 nas fileiras, do lado das brancas.
    As coordenadas ficam nos cantos das casas, sem modificar
    o tamanho de 640 x 640 pixels nem os círculos verdes.
    """
    fonte_casas = pygame.font.SysFont("arial", 15, bold=True)
    for linha in range(DIMENSAO):
        numero = str(DIMENSAO - linha)
        if linha % 2 == 0:
            cor_texto = COR_PRETA
        else:
            cor_texto = COR_BRANCA
        texto = fonte_casas.render(numero, True, cor_texto)
        screen.blit(texto, (4, linha * TAMANHO_QUADRADO + 3))
    for coluna in range(8):
        letra = "abcdefgh"[coluna]
        if coluna % 2 == 0:
            cor_texto = COR_BRANCA
        else:
            cor_texto = COR_PRETA
        texto = fonte_casas.render(letra, True, cor_texto)
        x = (coluna + 1) * TAMANHO_QUADRADO - texto.get_width() - 5
        y = ALTURA - texto.get_height() - 3
        screen.blit(texto, (x, y))


# ------------------------------------------------------------
# DESENHAR PECAS
# ------------------------------------------------------------
def desenhar_pecas(screen):
    """
    Percorre a matriz e desenha todas as peças.
    A peça selecionada aparece ampliada.
    """
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


# ------------------------------------------------------------
# MOVIMENTOS BASICOS
# ------------------------------------------------------------
def movimentos_basicos(tabuleiro, linha, coluna, considerar_en_passant=True):
    """
    Calcula os movimentos possíveis de uma peça.
    Nesta função analisamos apenas a maneira
    como cada peça se movimenta.
    A proteção do rei será verificada posteriormente.
    Retorna uma lista de posições:
    [(linha, coluna), ...]
    """
    peca = tabuleiro[linha][coluna]
    if peca == "--":
        return []
    cor = peca[0]
    tipo = peca[1]
    movimentos = []

    # Peão: avança para a frente e captura nas diagonais.
    if tipo == "P":
        if cor == "b":
            direcao = -1
            linha_inicial = 6
        else:
            direcao = 1
            linha_inicial = 1
        proxima_linha = linha + direcao
        if dentro_tabuleiro(proxima_linha, coluna):
            if tabuleiro[proxima_linha][coluna] == "--":
                movimentos.append((proxima_linha, coluna))
                duas_linhas = linha + 2 * direcao
                if linha == linha_inicial:
                    if tabuleiro[duas_linhas][coluna] == "--":
                        movimentos.append((duas_linhas, coluna))
        for deslocamento in [-1, 1]:
            nova_coluna = coluna + deslocamento
            if dentro_tabuleiro(proxima_linha, nova_coluna):
                alvo = tabuleiro[proxima_linha][nova_coluna]
                if alvo != "--" and alvo[0] != cor and (alvo[1] != "R"):
                    movimentos.append((proxima_linha, nova_coluna))
                if considerar_en_passant:
                    if en_passant == (proxima_linha, nova_coluna):
                        peca_lateral = tabuleiro[linha][nova_coluna]
                        if peca_lateral == cor_adversaria(cor) + "P":
                            movimentos.append((proxima_linha, nova_coluna))

    # Cavalo: testa os oito deslocamentos em L.
    elif tipo == "C":
        deslocamentos = [
            (-2, -1),
            (-2, 1),
            (-1, -2),
            (-1, 2),
            (1, -2),
            (1, 2),
            (2, -1),
            (2, 1),
        ]
        for dl, dc in deslocamentos:
            nova_linha = linha + dl
            nova_coluna = coluna + dc
            if dentro_tabuleiro(nova_linha, nova_coluna):
                alvo = tabuleiro[nova_linha][nova_coluna]
                if alvo == "--" or (alvo[0] != cor and alvo[1] != "R"):
                    movimentos.append((nova_linha, nova_coluna))

    # Torre, bispo e dama percorrem direções até uma peça ou a borda.
    elif tipo in ["T", "B", "D"]:
        direcoes = []
        if tipo in ["T", "D"]:
            direcoes += [(-1, 0), (1, 0), (0, -1), (0, 1)]
        if tipo in ["B", "D"]:
            direcoes += [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dl, dc in direcoes:
            nova_linha = linha + dl
            nova_coluna = coluna + dc
            while dentro_tabuleiro(nova_linha, nova_coluna):
                alvo = tabuleiro[nova_linha][nova_coluna]
                if alvo == "--":
                    movimentos.append((nova_linha, nova_coluna))
                else:
                    if alvo[0] != cor and alvo[1] != "R":
                        movimentos.append((nova_linha, nova_coluna))
                    break
                nova_linha += dl
                nova_coluna += dc

    # Rei: uma casa por vez; o roque é tratado separadamente.
    elif tipo == "R":
        for dl in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dl == 0 and dc == 0:
                    continue
                nova_linha = linha + dl
                nova_coluna = coluna + dc
                if dentro_tabuleiro(nova_linha, nova_coluna):
                    alvo = tabuleiro[nova_linha][nova_coluna]
                    if alvo == "--" or (alvo[0] != cor and alvo[1] != "R"):
                        movimentos.append((nova_linha, nova_coluna))
    return movimentos


# ------------------------------------------------------------
# CASA ATACADA
# ------------------------------------------------------------
def casa_atacada(tabuleiro, linha, coluna, atacante):
    """
    Verifica se uma casa está sendo atacada.
    Essa função é importante para:
    - Impedir que o rei entre em xeque.
    - Validar o roque.
    - Impedir movimentos que exponham o rei.
    Não utilizamos movimentos_basicos diretamente
    porque os peões atacam diagonalmente, mesmo
    quando a casa diagonal está vazia.
    """
    for l in range(DIMENSAO):
        for c in range(DIMENSAO):
            peca = tabuleiro[l][c]
            if peca == "--":
                continue
            if peca[0] != atacante:
                continue
            tipo = peca[1]
            if tipo == "P":
                if atacante == "b":
                    direcao = -1
                else:
                    direcao = 1
                if linha == l + direcao:
                    if abs(coluna - c) == 1:
                        return True
            elif tipo == "C":
                diferenca_linha = abs(linha - l)
                diferenca_coluna = abs(coluna - c)
                if (
                    diferenca_linha == 2
                    and diferenca_coluna == 1
                    or (diferenca_linha == 1 and diferenca_coluna == 2)
                ):
                    return True
            elif tipo == "R":
                if max(abs(linha - l), abs(coluna - c)) == 1:
                    return True
            elif tipo in ["T", "B", "D"]:
                dl = linha - l
                dc = coluna - c
                direcao_linha = 0
                direcao_coluna = 0
                movimento_reto = dl == 0 or dc == 0
                movimento_diagonal = abs(dl) == abs(dc)
                permitido = False
                if tipo == "T" and movimento_reto:
                    permitido = True
                elif tipo == "B" and movimento_diagonal:
                    permitido = True
                elif tipo == "D":
                    permitido = movimento_reto or movimento_diagonal
                if not permitido:
                    continue
                if dl > 0:
                    direcao_linha = 1
                elif dl < 0:
                    direcao_linha = -1
                if dc > 0:
                    direcao_coluna = 1
                elif dc < 0:
                    direcao_coluna = -1
                atual_linha = l + direcao_linha
                atual_coluna = c + direcao_coluna
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


# ------------------------------------------------------------
# LOCALIZAR REI
# ------------------------------------------------------------
def localizar_rei(tabuleiro, cor):
    """
    Procura o rei de determinada cor na matriz.
    """
    codigo_rei = cor + "R"
    for linha in range(DIMENSAO):
        for coluna in range(DIMENSAO):
            if tabuleiro[linha][coluna] == codigo_rei:
                return (linha, coluna)
    return None


# ------------------------------------------------------------
# REI EM XEQUE
# ------------------------------------------------------------
def rei_em_xeque(tabuleiro, cor):
    """
    Verifica se o rei está sob ataque.
    """
    posicao_rei = localizar_rei(tabuleiro, cor)
    if posicao_rei is None:
        return True
    linha, coluna = posicao_rei
    return casa_atacada(tabuleiro, linha, coluna, cor_adversaria(cor))


# ------------------------------------------------------------
# MOVIMENTOS ROQUE
# ------------------------------------------------------------
def movimentos_roque(tabuleiro, cor):
    """
    Calcula os movimentos de roque disponíveis.
    Regras:
    1. O rei não pode ter se movimentado.
    2. A torre envolvida não pode ter se movimentado.
    3. As casas entre rei e torre devem estar vazias.
    4. O rei não pode estar em xeque.
    5. O rei não pode atravessar uma casa atacada.
    6. O rei não pode terminar em uma casa atacada.
    """
    movimentos = []
    if cor == "b":
        linha = 7
    else:
        linha = 0
    if tabuleiro[linha][4] != cor + "R":
        return movimentos
    if movimentou[indice_cor(cor)][0]:
        return movimentos
    if rei_em_xeque(tabuleiro, cor):
        return movimentos
    adversario = cor_adversaria(cor)
    if not movimentou[indice_cor(cor)][2]:
        if tabuleiro[linha][7] == cor + "T":
            if tabuleiro[linha][5] == "--" and tabuleiro[linha][6] == "--":
                if not casa_atacada(tabuleiro, linha, 5, adversario) and (
                    not casa_atacada(tabuleiro, linha, 6, adversario)
                ):
                    movimentos.append((linha, 6))
    if not movimentou[indice_cor(cor)][1]:
        if tabuleiro[linha][0] == cor + "T":
            if (
                tabuleiro[linha][1] == "--"
                and tabuleiro[linha][2] == "--"
                and (tabuleiro[linha][3] == "--")
            ):
                if not casa_atacada(tabuleiro, linha, 3, adversario) and (
                    not casa_atacada(tabuleiro, linha, 2, adversario)
                ):
                    movimentos.append((linha, 2))
    return movimentos


# ------------------------------------------------------------
# SIMULAR MOVIMENTO
# ------------------------------------------------------------
def simular_movimento(tabuleiro, origem, destino):
    """
    Simula uma jogada em uma cópia da matriz.
    Essa simulação é utilizada para descobrir
    se determinado movimento deixa o rei em xeque.
    Também considera:
    - Roque
    - En passant
    """
    copia = copiar_tabuleiro(tabuleiro)
    linha_origem, coluna_origem = origem
    linha_destino, coluna_destino = destino
    peca = copia[linha_origem][coluna_origem]
    copia[linha_origem][coluna_origem] = "--"
    if (
        peca[1] == "P"
        and coluna_origem != coluna_destino
        and (copia[linha_destino][coluna_destino] == "--")
    ):
        copia[linha_origem][coluna_destino] = "--"
    if peca[1] == "R" and abs(coluna_destino - coluna_origem) == 2:
        if coluna_destino == 6:
            copia[linha_origem][5] = copia[linha_origem][7]
            copia[linha_origem][7] = "--"
        elif coluna_destino == 2:
            copia[linha_origem][3] = copia[linha_origem][0]
            copia[linha_origem][0] = "--"
    copia[linha_destino][coluna_destino] = peca
    return copia


# ------------------------------------------------------------
# MOVIMENTOS LEGAIS
# ------------------------------------------------------------
def movimentos_legais(tabuleiro, linha, coluna):
    """
    Retorna apenas os movimentos permitidos.
    Primeiro calculamos os movimentos básicos.
    Depois simulamos cada movimento.
    Se a jogada deixar o próprio rei em xeque,
    ela será descartada.
    """
    peca = tabuleiro[linha][coluna]
    if peca == "--":
        return []
    cor = peca[0]
    movimentos = movimentos_basicos(tabuleiro, linha, coluna)
    if peca[1] == "R":
        movimentos += movimentos_roque(tabuleiro, cor)

    # Simula cada destino e rejeita os que deixam o próprio rei em xeque.
    movimentos_validos = []
    for destino in movimentos:
        copia = simular_movimento(tabuleiro, (linha, coluna), destino)
        if not rei_em_xeque(copia, cor):
            movimentos_validos.append(destino)
    return movimentos_validos


# ------------------------------------------------------------
# ATUALIZAR DIREITOS ROQUE
# ------------------------------------------------------------
def atualizar_direitos_roque(peca, origem, capturada, destino):
    """
    Atualiza as informações sobre rei e torres.
    Uma vez movimentado, o rei perde definitivamente
    o direito ao roque.
    Uma torre também perde esse direito quando
    sai de sua casa inicial.
    A captura de uma torre na casa inicial também
    elimina o direito ao roque daquele lado.
    """
    linha, coluna = origem
    cor = peca[0]
    if peca[1] == "R":
        movimentou[indice_cor(cor)][0] = True
    elif peca[1] == "T":
        if cor == "b":
            linha_inicial = 7
        else:
            linha_inicial = 0
        if linha == linha_inicial:
            if coluna == 0:
                movimentou[indice_cor(cor)][1] = True
            elif coluna == 7:
                movimentou[indice_cor(cor)][2] = True
    if capturada != "--" and capturada[1] == "T":
        cor_capturada = capturada[0]
        if cor_capturada == "b":
            linha_inicial = 7
        else:
            linha_inicial = 0
        linha_destino, coluna_destino = destino
        if linha_destino == linha_inicial:
            if coluna_destino == 0:
                movimentou[indice_cor(cor_capturada)][1] = True
            elif coluna_destino == 7:
                movimentou[indice_cor(cor_capturada)][2] = True


# ------------------------------------------------------------
# INICIAR ANIMACAO
# ------------------------------------------------------------
def iniciar_animacao(origem, destino):
    """
    Prepara o deslocamento visual de uma peça.
    A matriz só será atualizada quando a animação
    terminar.
    Assim, a jogada é validada antes de ser executada.
    """
    global animando
    global peca_movendo
    global pos_atual_anim_x
    global pos_atual_anim_y
    global destino_anim_x
    global destino_anim_y
    global destino_final
    global jogada_animacao
    linha_origem, coluna_origem = origem
    linha_destino, coluna_destino = destino
    peca_movendo = tabuleiro_estado[linha_origem][coluna_origem]
    imagem = imagens[indice_peca(peca_movendo)]
    largura = imagem.get_width()
    altura = imagem.get_height()
    pos_atual_anim_x = (
        coluna_origem * TAMANHO_QUADRADO + (TAMANHO_QUADRADO - largura) // 2
    )
    pos_atual_anim_y = (
        linha_origem * TAMANHO_QUADRADO + (TAMANHO_QUADRADO - altura) // 2
    )
    destino_anim_x = (
        coluna_destino * TAMANHO_QUADRADO + (TAMANHO_QUADRADO - largura) // 2
    )
    destino_anim_y = linha_destino * TAMANHO_QUADRADO + (TAMANHO_QUADRADO - altura) // 2
    destino_final = destino
    jogada_animacao = [origem, destino, peca_movendo]
    animando = True


# ------------------------------------------------------------
# FINALIZAR JOGADA
# ------------------------------------------------------------
def finalizar_jogada():
    """
    Atualiza a matriz após a animação.
    Esta função também executa:
    - Capturas normais
    - Captura en passant
    - Movimentação da torre durante o roque
    - Atualização dos direitos de roque
    - Promoção de peões
    - Alternância de turnos
    """
    global en_passant
    global turno_atual
    global promocao_pendente
    global jogada_animacao
    global peca_selecionada
    global origem_selecionada
    global movimentos_disponiveis

    # Recupera os três dados da jogada já validada.
    origem = jogada_animacao[0]
    destino = jogada_animacao[1]
    peca = jogada_animacao[2]
    lo, co = origem
    ld, cd = destino
    capturada = tabuleiro_estado[ld][cd]
    if peca[1] == "P" and co != cd and (capturada == "--"):
        tabuleiro_estado[lo][cd] = "--"
        mostrar_mensagem("Captura en passant!")
    atualizar_direitos_roque(peca, origem, capturada, destino)
    tabuleiro_estado[lo][co] = "--"
    tabuleiro_estado[ld][cd] = peca
    if peca[1] == "R" and abs(cd - co) == 2:
        if cd == 6:
            tabuleiro_estado[ld][5] = tabuleiro_estado[ld][7]
            tabuleiro_estado[ld][7] = "--"
            mostrar_mensagem("Roque pequeno!")
        elif cd == 2:
            tabuleiro_estado[ld][3] = tabuleiro_estado[ld][0]
            tabuleiro_estado[ld][0] = "--"
            mostrar_mensagem("Roque grande!")
    en_passant = None
    if peca[1] == "P" and abs(ld - lo) == 2:
        linha_intermediaria = (lo + ld) // 2
        en_passant = (linha_intermediaria, co)
    if peca[1] == "P":
        if peca[0] == "b":
            ultima_linha = 0
        else:
            ultima_linha = 7
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
    if rei_em_xeque(tabuleiro_estado, turno_atual):
        mostrar_mensagem("XEQUE! Vez das " + nome_cor(turno_atual))
    else:
        mostrar_mensagem("Vez das " + nome_cor(turno_atual))


# ------------------------------------------------------------
# PROMOVER PEAO
# ------------------------------------------------------------
def promover_peao(tipo):
    """
    Transforma um peão que alcançou a última fileira.
    Opções:
    D = Dama
    T = Torre
    B = Bispo
    C = Cavalo
    A promoção não depende da existência de uma peça
    capturada: podemos escolher qualquer uma das
    quatro opções permitidas.
    """
    global promocao_pendente
    global turno_atual
    global peca_selecionada
    global origem_selecionada
    global movimentos_disponiveis
    if promocao_pendente is None:
        return
    if tipo not in ["D", "T", "B", "C"]:
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
    if rei_em_xeque(tabuleiro_estado, turno_atual):
        mostrar_mensagem("Promoção realizada! XEQUE!")
    else:
        mostrar_mensagem("Promoção realizada!")


# ------------------------------------------------------------
# SELECIONAR CASA
# ------------------------------------------------------------
def selecionar_casa(linha, coluna):
    """
    Controla os cliques nas casas.
    Primeiro clique:
        Seleciona uma peça do jogador atual.
    Segundo clique:
        Executa a jogada, caso seja legal.
    Também permite trocar a seleção por outra
    peça do mesmo jogador.
    """
    global peca_selecionada
    global origem_selecionada
    global movimentos_disponiveis
    if not dentro_tabuleiro(linha, coluna):
        return
    if animando or promocao_pendente is not None:
        return
    peca = tabuleiro_estado[linha][coluna]
    print(f"Clique: casa {coordenada_xadrez(linha, coluna)}, peça {peca}")
    if origem_selecionada is None:
        if peca != "--" and peca[0] == turno_atual:
            peca_selecionada = peca
            origem_selecionada = (linha, coluna)
            movimentos_disponiveis = movimentos_legais(tabuleiro_estado, linha, coluna)
            exibir_movimentos_legais(movimentos_disponiveis)
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
        exibir_movimentos_legais(movimentos_disponiveis)
        return
    destino = (linha, coluna)
    if destino in movimentos_disponiveis:
        iniciar_animacao(origem_selecionada, destino)
    else:
        mostrar_mensagem("Movimento inválido!")


# ------------------------------------------------------------
# ATUALIZAR ANIMACAO
# ------------------------------------------------------------
def atualizar_animacao(dt):
    """
    Atualiza gradualmente a posição da peça.
    dt representa o tempo decorrido entre os quadros.
    O deslocamento utiliza interpolação simples:
    a peça se aproxima progressivamente do destino.
    A animação não interfere na legalidade da jogada.
    """
    global animando
    global pos_atual_anim_x
    global pos_atual_anim_y
    if not animando:
        return

    # dt é o tempo entre quadros; o fator controla o deslocamento gradual.
    velocidade_deslize = 0.015
    fator = velocidade_deslize * dt
    fator = min(fator, 1.0)
    pos_atual_anim_x += (destino_anim_x - pos_atual_anim_x) * fator
    pos_atual_anim_y += (destino_anim_y - pos_atual_anim_y) * fator
    if (
        abs(destino_anim_x - pos_atual_anim_x) < 0.5
        and abs(destino_anim_y - pos_atual_anim_y) < 0.5
    ):
        pos_atual_anim_x = destino_anim_x
        pos_atual_anim_y = destino_anim_y
        animando = False
        finalizar_jogada()


# ------------------------------------------------------------
# DESENHAR ANIMACAO
# ------------------------------------------------------------
def desenhar_animacao(screen):
    """
    Desenha a peça na posição intermediária
    calculada pela animação.
    """
    if not animando:
        return
    imagem = imagens[indice_peca(peca_movendo)]
    screen.blit(imagem, (pos_atual_anim_x, pos_atual_anim_y))


# ------------------------------------------------------------
# DESENHAR PROMOCAO
# ------------------------------------------------------------
def desenhar_promocao(screen):
    """
    Exibe uma mensagem quando o jogador precisa
    escolher a peça de promoção.
    """
    if promocao_pendente is None:
        return
    camada = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
    camada.fill((0, 0, 0, 170))
    screen.blit(camada, (0, 0))
    caixa = pygame.Rect(60, 250, 520, 140)
    pygame.draw.rect(screen, (245, 235, 215), caixa, border_radius=12)
    pygame.draw.rect(screen, (90, 60, 40), caixa, 3, border_radius=12)
    texto1 = fonte.render("PROMOÇÃO DO PEÃO", True, (40, 40, 40))
    texto2 = fonte.render("D = Dama   T = Torre", True, (40, 40, 40))
    texto3 = fonte.render("B = Bispo   C = Cavalo", True, (40, 40, 40))
    screen.blit(texto1, (185, 265))
    screen.blit(texto2, (175, 310))
    screen.blit(texto3, (165, 345))


# 07. PREPARAÇÃO DA PARTIDA
# Carrega as imagens uma única vez, antes do laço principal.
carregar_imagens()
mostrar_mensagem("Vez das brancas")

# 08. LAÇO PRINCIPAL
# Repete a leitura de eventos, a atualização e o desenho da tela.
while True:

    # Limita a atualização a 60 quadros por segundo.
    clock.tick(60)
    dt = clock.get_time()

    # Trata os comandos recebidos desde o quadro anterior.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Teclado: promoção, cursor, seleção e cancelamento.
        elif event.type == pygame.KEYDOWN:
            if promocao_pendente is not None:
                if event.key == pygame.K_d:
                    promover_peao("D")
                elif event.key == pygame.K_t:
                    promover_peao("T")
                elif event.key == pygame.K_b:
                    promover_peao("B")
                elif event.key == pygame.K_c:
                    promover_peao("C")
                continue
            if animando:
                continue
            if event.key == pygame.K_UP:
                cursor_linha = max(0, cursor_linha - 1)
            elif event.key == pygame.K_DOWN:
                cursor_linha = min(7, cursor_linha + 1)
            elif event.key == pygame.K_LEFT:
                cursor_coluna = max(0, cursor_coluna - 1)
            elif event.key == pygame.K_RIGHT:
                cursor_coluna = min(7, cursor_coluna + 1)
            elif event.key == pygame.K_RETURN:
                selecionar_casa(cursor_linha, cursor_coluna)
            elif event.key == pygame.K_ESCAPE:
                peca_selecionada = None
                origem_selecionada = None
                movimentos_disponiveis = []

        # Mouse: converte a posição em pixels para linha e coluna da matriz.
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if not animando and promocao_pendente is None:
                    x, y = event.pos
                    coluna = x // TAMANHO_QUADRADO
                    linha = y // TAMANHO_QUADRADO
                    cursor_linha = linha
                    cursor_coluna = coluna
                    selecionar_casa(linha, coluna)

    # Atualiza o movimento antes de desenhar o novo quadro.
    atualizar_animacao(dt)

    # Ordem de desenho: fundo, tabuleiro, peças, animação e informações.
    screen.fill((56, 203, 171))
    desenhar_tabuleiro(screen)
    desenhar_pecas(screen)
    desenhar_animacao(screen)
    pygame.draw.rect(
        screen,
        (50, 100, 230),
        (
            cursor_coluna * TAMANHO_QUADRADO,
            cursor_linha * TAMANHO_QUADRADO,
            TAMANHO_QUADRADO,
            TAMANHO_QUADRADO,
        ),
        2,
    )
    desenhar_coordenadas(screen)
    desenhar_promocao(screen)

    # Apresenta na janela tudo o que foi desenhado neste quadro.
    pygame.display.update()
