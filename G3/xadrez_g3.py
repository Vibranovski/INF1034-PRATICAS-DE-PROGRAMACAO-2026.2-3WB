
import pygame
import sys
from pathlib import Path
from collections import deque

# ============================================================
# XADREZ ULTIMATE - INF1034 - PRÁTICAS DE PROGRAMAÇÃO
# ============================================================
#
# ETAPA 1: Criação do tabuleiro 8x8
# ETAPA 2: Posicionamento das 32 peças
# ETAPA 3: Movimentação e captura das peças
# ETAPA 4: Regras oficiais do xadrez
#
# Funcionalidades:
# - Movimentação das seis peças
# - Capturas
# - Alternância entre jogadores
# - Roque pequeno e grande
# - En passant
# - Promoção de peões
# - Proteção do rei contra xeque
# - Animação de deslocamento
# - Seleção com mouse ou teclado
#
# A detecção de xeque-mate e empates será implementada
# na Etapa 5.
# ============================================================


# ============================================================
# 1. INICIALIZAÇÃO DO PYGAME
# ============================================================

pygame.init()

# O tabuleiro possui oito linhas e oito colunas.
DIMENSAO = 8

# Cada casa possui 80 pixels de largura e altura.
TAMANHO_QUADRADO = 80

# A janela terá 640 x 640 pixels.
LARGURA = DIMENSAO * TAMANHO_QUADRADO
ALTURA = DIMENSAO * TAMANHO_QUADRADO

# Cores originais do tabuleiro.
COR_BRANCA = (240, 217, 181)
COR_PRETA = (181, 136, 99)

# As casas de destino legal recebem círculos verdes.
COR_VERDE = (105, 205, 110)

# Cor utilizada para destacar a peça selecionada.
COR_SELECAO = (255, 215, 60)

# Criamos a janela do jogo.
screen = pygame.display.set_mode((LARGURA, ALTURA))

pygame.display.set_caption(
    "Xadrez ULTIMATE - Regras Oficiais"
)

# O relógio controla a quantidade de quadros por segundo.
clock = pygame.time.Clock()

# Fonte utilizada para apresentar informações ao jogador.
fonte = pygame.font.SysFont("arial", 24, bold=True)


# ============================================================
# 2. MATRIZ 8x8 COM AS POSIÇÕES INICIAIS
# ============================================================

# Cada elemento da matriz representa uma casa.
#
# b = peça branca
# p = peça preta
#
# R = Rei
# D = Dama
# T = Torre
# B = Bispo
# C = Cavalo
# P = Peão
#
# "--" representa uma casa vazia.
#
# A primeira linha contém as peças pretas.
# A última linha contém as peças brancas.

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


# ============================================================
# 3. CONFIGURAÇÃO DAS IMAGENS
# ============================================================

# Dicionário com as imagens normais das peças.
imagens = {}

# Dicionário com as imagens ampliadas das peças.
imagens_selecionadas = {}

# Localização da pasta que contém a sprite sheet.
#
# IMPORTANTE:
# Caso o arquivo esteja em outra pasta, altere o caminho.

PASTA_IMAGENS = Path(
    r"C:\Users\g2620001\Downloads"
)

CAMINHO_SPRITE = PASTA_IMAGENS / "Chess_Pieces.png"


# ============================================================
# 4. VARIÁVEIS DE CONTROLE DO JOGO
# ============================================================

# As peças brancas começam a partida.
turno_atual = "b"

# Armazena o código da peça selecionada.
peca_selecionada = None

# Armazena a posição da peça selecionada.
origem_selecionada = None

# Lista das casas para as quais a peça pode se mover.
movimentos_disponiveis = []

# Controla a animação de movimentação.
animando = False

# Peça que está sendo animada.
peca_movendo = None

# Posições utilizadas na animação.
pos_atual_anim_x = 0.0
pos_atual_anim_y = 0.0

destino_anim_x = 0.0
destino_anim_y = 0.0

# Casa em que a peça será colocada após a animação.
destino_final = None

# Guarda as informações da jogada em andamento.
jogada_animacao = None

# Controla a possibilidade de realizar roque.
#
# Cada jogador possui três informações:
# - Se o rei já se movimentou
# - Se a torre da esquerda já se movimentou
# - Se a torre da direita já se movimentou

movimentou = {
    "b": {
        "rei": False,
        "torre_esquerda": False,
        "torre_direita": False
    },
    "p": {
        "rei": False,
        "torre_esquerda": False,
        "torre_direita": False
    }
}

# Armazena a casa vulnerável à captura en passant.
#
# Essa informação existe apenas durante a jogada
# imediatamente posterior ao avanço duplo de um peão.

en_passant = None

# Controla a promoção de peões.
promocao_pendente = None

# Cursor utilizado para selecionar casas pelo teclado.
cursor_linha = 7
cursor_coluna = 0


# ============================================================
# 5. FUNÇÕES AUXILIARES
# ============================================================

def dentro_tabuleiro(linha, coluna):
    """
    Verifica se uma posição pertence ao tabuleiro.

    As linhas e colunas devem estar entre 0 e 7.
    """

    return (
        0 <= linha < DIMENSAO
        and 0 <= coluna < DIMENSAO
    )


def coordenada_xadrez(linha, coluna):
    """Converte índices da matriz (0 a 7) em casas como a1, e4 e h8."""
    letra = "abcdefgh"[coluna]
    fileira = DIMENSAO - linha
    return f"{letra}{fileira}"


def exibir_movimentos_legais(movimentos):
    """Mostra os destinos legais com a notação tradicional do xadrez."""
    casas = [coordenada_xadrez(l, c) for l, c in movimentos]
    print("Movimentos legais:", casas)


def cor_adversaria(cor):
    """
    Retorna a cor adversária.

    Se receber branco, retorna preto.
    Se receber preto, retorna branco.
    """

    if cor == "b":
        return "p"

    return "b"


def copiar_tabuleiro(tabuleiro):
    """
    Cria uma cópia independente da matriz.

    Isso permite simular movimentos sem modificar
    o tabuleiro original.
    """

    copia = []

    for linha in tabuleiro:
        copia.append(linha.copy())

    return copia


def mostrar_mensagem(texto):
    """
    Exibe uma mensagem no terminal.

    Também altera o título da janela.
    """

    print(texto)

    pygame.display.set_caption(
        "Xadrez ULTIMATE - " + texto
    )


# ============================================================
# 6. REMOÇÃO DO FUNDO BRANCO DAS IMAGENS
# ============================================================

def remover_fundo(sprite):
    """
    Remove o fundo branco conectado às bordas da imagem.

    Utilizamos uma fila para percorrer os pixels
    brancos encontrados nas extremidades.

    Essa técnica evita remover automaticamente todos
    os pixels brancos existentes dentro das peças.
    """

    largura, altura = sprite.get_size()

    mascara = pygame.mask.from_threshold(
        sprite,
        (255, 255, 255, 255),
        (15, 15, 15, 255)
    )

    visitados = set()

    fila = deque()

    # Adicionamos os pixels das bordas horizontais.
    for x in range(largura):
        fila.append((x, 0))
        fila.append((x, altura - 1))

    # Adicionamos os pixels das bordas verticais.
    for y in range(altura):
        fila.append((0, y))
        fila.append((largura - 1, y))

    # Percorremos os pixels conectados ao fundo.
    while fila:

        x, y = fila.popleft()

        if (x, y) in visitados:
            continue

        if mascara.get_at((x, y)) == 0:
            continue

        visitados.add((x, y))

        # O último valor, zero, representa transparência.
        sprite.set_at(
            (x, y),
            (255, 255, 255, 0)
        )

        # Procuramos pixels vizinhos.
        for dx, dy in [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1)
        ]:

            nx = x + dx
            ny = y + dy

            if dentro_imagem(nx, ny, largura, altura):

                if (nx, ny) not in visitados:
                    fila.append((nx, ny))

    return sprite


def dentro_imagem(x, y, largura, altura):
    """Verifica se um pixel pertence à imagem."""

    return (
        0 <= x < largura
        and 0 <= y < altura
    )


# ============================================================
# 7. CARREGAMENTO DAS 12 IMAGENS
# ============================================================

def carregar_imagens():
    """
    Carrega a sprite sheet e recorta as 12 peças.

    As coordenadas abaixo foram definidas
    individualmente para a imagem Chess_Pieces.png.

    Cada tupla contém:
    (x, y, largura, altura)
    """

    sprite_sheet = pygame.image.load(
        str(CAMINHO_SPRITE)
    ).convert_alpha()

    largura_original, altura_original = (
        sprite_sheet.get_size()
    )

    # Coordenadas individuais das 12 peças.
    coordenadas = {

        # Peças brancas.
        "bP": (210, 80, 290, 520),
        "bT": (620, 80, 310, 520),
        "bB": (1050, 80, 310, 520),
        "bC": (1460, 80, 320, 520),
        "bD": (210, 1210, 290, 680),
        "bR": (620, 1210, 310, 680),

        # Peças pretas.
        "pP": (210, 660, 290, 520),
        "pT": (620, 660, 310, 520),
        "pB": (1050, 660, 310, 520),
        "pC": (1460, 660, 320, 520),
        "pD": (1050, 1210, 310, 680),
        "pR": (1460, 1210, 320, 680)
    }

    # Ajustamos as coordenadas proporcionalmente.
    escala_x = largura_original / 2048
    escala_y = altura_original / 2048

    for codigo, dados in coordenadas.items():

        x, y, largura, altura = dados

        x = round(x * escala_x)
        y = round(y * escala_y)

        largura = round(largura * escala_x)
        altura = round(altura * escala_y)

        # Recortamos a peça da imagem original.
        sprite = sprite_sheet.subsurface(
            pygame.Rect(x, y, largura, altura)
        ).copy()

        # Criamos a imagem normal.
        proporcao = min(
            65 / largura,
            65 / altura
        )

        nova_largura = max(
            1,
            round(largura * proporcao)
        )

        nova_altura = max(
            1,
            round(altura * proporcao)
        )

        sprite_normal = pygame.transform.smoothscale(
            sprite,
            (nova_largura, nova_altura)
        )

        imagens[codigo] = remover_fundo(
            sprite_normal
        )

        # Criamos uma imagem maior para a seleção.
        proporcao_zoom = min(
            78 / largura,
            78 / altura
        )

        largura_zoom = max(
            1,
            round(largura * proporcao_zoom)
        )

        altura_zoom = max(
            1,
            round(altura * proporcao_zoom)
        )

        sprite_zoom = pygame.transform.smoothscale(
            sprite,
            (largura_zoom, altura_zoom)
        )

        imagens_selecionadas[codigo] = remover_fundo(
            sprite_zoom
        )


# ============================================================
# 8. DESENHO DO TABULEIRO
# ============================================================

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

            # Alternamos as cores originais das casas.
            if (linha + coluna) % 2 == 0:
                cor = COR_BRANCA
            else:
                cor = COR_PRETA

            # Desenhamos a casa sem alterar sua cor de fundo.
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

            # Desenhamos um círculo verde somente nas casas legais.
            if (
                origem_selecionada is not None
                and (linha, coluna) in movimentos_disponiveis
            ):
                # Centro exato da casa de 80 x 80 pixels.
                centro_x = coluna * TAMANHO_QUADRADO + TAMANHO_QUADRADO // 2
                centro_y = linha * TAMANHO_QUADRADO + TAMANHO_QUADRADO // 2

                # Raio de 15 pixels = diâmetro de 30 pixels.
                pygame.draw.circle(
                    screen,
                    COR_VERDE,
                    (centro_x, centro_y),
                    15
                )

    # Mantemos o contorno amarelo da peça selecionada.
    if origem_selecionada is not None:
        linha, coluna = origem_selecionada
        pygame.draw.rect(
            screen,
            COR_SELECAO,
            (
                coluna * TAMANHO_QUADRADO,
                linha * TAMANHO_QUADRADO,
                TAMANHO_QUADRADO,
                TAMANHO_QUADRADO
            ),
            4
        )


def desenhar_coordenadas(screen):
    """Exibe a-h nas colunas e 1-8 nas fileiras, do lado das brancas.

    As coordenadas ficam nos cantos das casas, sem modificar
    o tamanho de 640 x 640 pixels nem os círculos verdes.
    """
    fonte_casas = pygame.font.SysFont("arial", 15, bold=True)

    # Fileiras: 8 na parte superior e 1 na parte inferior.
    for linha in range(DIMENSAO):
        numero = str(DIMENSAO - linha)
        cor_texto = COR_PRETA if linha % 2 == 0 else COR_BRANCA
        texto = fonte_casas.render(numero, True, cor_texto)
        screen.blit(texto, (4, linha * TAMANHO_QUADRADO + 3))

    # Colunas: a, b, c, d, e, f, g, h, da esquerda para a direita.
    for coluna, letra in enumerate("abcdefgh"):
        cor_texto = COR_BRANCA if coluna % 2 == 0 else COR_PRETA
        texto = fonte_casas.render(letra, True, cor_texto)
        x = (coluna + 1) * TAMANHO_QUADRADO - texto.get_width() - 5
        y = ALTURA - texto.get_height() - 3
        screen.blit(texto, (x, y))


# ============================================================
# 9. DESENHO DAS PEÇAS
# ============================================================

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

            # Durante a animação, a peça em movimento
            # é desenhada separadamente.
            if (
                animando
                and (linha, coluna) == origem_selecionada
            ):
                continue

            if (
                not animando
                and origem_selecionada == (linha, coluna)
            ):

                imagem = imagens_selecionadas[peca]

            else:
                imagem = imagens[peca]

            largura = imagem.get_width()
            altura = imagem.get_height()

            x = (
                coluna * TAMANHO_QUADRADO
                + (TAMANHO_QUADRADO - largura) // 2
            )

            y = (
                linha * TAMANHO_QUADRADO
                + (TAMANHO_QUADRADO - altura) // 2
            )

            screen.blit(imagem, (x, y))


# ============================================================
# 10. MOVIMENTOS BÁSICOS DAS PEÇAS
# ============================================================

def movimentos_basicos(tabuleiro, linha, coluna,
                       considerar_en_passant=True):
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

    # --------------------------------------------------------
    # PEÃO
    # --------------------------------------------------------

    if tipo == "P":

        # Peões brancos sobem no tabuleiro.
        # Peões pretos descem no tabuleiro.

        if cor == "b":
            direcao = -1
            linha_inicial = 6
        else:
            direcao = 1
            linha_inicial = 1

        proxima_linha = linha + direcao

        # Movimento de uma casa para frente.
        if dentro_tabuleiro(proxima_linha, coluna):

            if tabuleiro[proxima_linha][coluna] == "--":

                movimentos.append(
                    (proxima_linha, coluna)
                )

                # Primeiro movimento: até duas casas.
                duas_linhas = linha + 2 * direcao

                if linha == linha_inicial:

                    if tabuleiro[duas_linhas][coluna] == "--":

                        movimentos.append(
                            (duas_linhas, coluna)
                        )

        # Captura diagonal.
        for deslocamento in [-1, 1]:

            nova_coluna = coluna + deslocamento

            if dentro_tabuleiro(
                proxima_linha,
                nova_coluna
            ):

                alvo = tabuleiro[proxima_linha][nova_coluna]

                # O peão captura apenas peças adversárias.
                # O rei adversário não pode ser capturado.
                if (
                    alvo != "--"
                    and alvo[0] != cor
                    and alvo[1] != "R"
                ):

                    movimentos.append(
                        (proxima_linha, nova_coluna)
                    )

                # Captura especial en passant.
                if considerar_en_passant:

                    if en_passant == (
                        proxima_linha,
                        nova_coluna
                    ):

                        # Verificamos o peão adversário
                        # que está ao lado do nosso peão.
                        peca_lateral = tabuleiro[
                            linha
                        ][
                            nova_coluna
                        ]

                        if peca_lateral == (
                            cor_adversaria(cor) + "P"
                        ):

                            movimentos.append(
                                (proxima_linha, nova_coluna)
                            )

    # --------------------------------------------------------
    # CAVALO
    # --------------------------------------------------------

    elif tipo == "C":

        # O cavalo se movimenta em formato de L.
        #
        # Ele pode saltar sobre outras peças.

        deslocamentos = [
            (-2, -1),
            (-2, 1),
            (-1, -2),
            (-1, 2),
            (1, -2),
            (1, 2),
            (2, -1),
            (2, 1)
        ]

        for dl, dc in deslocamentos:

            nova_linha = linha + dl
            nova_coluna = coluna + dc

            if dentro_tabuleiro(
                nova_linha,
                nova_coluna
            ):

                alvo = tabuleiro[nova_linha][nova_coluna]

                if (
                    alvo == "--"
                    or (
                        alvo[0] != cor
                        and alvo[1] != "R"
                    )
                ):

                    movimentos.append(
                        (nova_linha, nova_coluna)
                    )

    # --------------------------------------------------------
    # TORRE, BISPO E DAMA
    # --------------------------------------------------------

    elif tipo in ["T", "B", "D"]:

        direcoes = []

        # Torre: movimentos horizontais e verticais.
        if tipo in ["T", "D"]:

            direcoes += [
                (-1, 0),
                (1, 0),
                (0, -1),
                (0, 1)
            ]

        # Bispo: movimentos diagonais.
        if tipo in ["B", "D"]:

            direcoes += [
                (-1, -1),
                (-1, 1),
                (1, -1),
                (1, 1)
            ]

        # A dama combina torre e bispo.
        for dl, dc in direcoes:

            nova_linha = linha + dl
            nova_coluna = coluna + dc

            # Continuamos na direção até encontrar
            # uma peça ou alcançar a borda.
            while dentro_tabuleiro(
                nova_linha,
                nova_coluna
            ):

                alvo = tabuleiro[nova_linha][nova_coluna]

                if alvo == "--":

                    movimentos.append(
                        (nova_linha, nova_coluna)
                    )

                else:

                    # Capturamos uma peça adversária,
                    # exceto o rei.
                    if (
                        alvo[0] != cor
                        and alvo[1] != "R"
                    ):

                        movimentos.append(
                            (nova_linha, nova_coluna)
                        )

                    # Nenhuma peça deslizante pode
                    # atravessar outra peça.
                    break

                nova_linha += dl
                nova_coluna += dc

    # --------------------------------------------------------
    # REI
    # --------------------------------------------------------

    elif tipo == "R":

        # O rei movimenta-se uma casa em qualquer direção.
        #
        # O roque será acrescentado separadamente.

        for dl in [-1, 0, 1]:

            for dc in [-1, 0, 1]:

                if dl == 0 and dc == 0:
                    continue

                nova_linha = linha + dl
                nova_coluna = coluna + dc

                if dentro_tabuleiro(
                    nova_linha,
                    nova_coluna
                ):

                    alvo = tabuleiro[
                        nova_linha
                    ][
                        nova_coluna
                    ]

                    if (
                        alvo == "--"
                        or (
                            alvo[0] != cor
                            and alvo[1] != "R"
                        )
                    ):

                        movimentos.append(
                            (nova_linha, nova_coluna)
                        )

    return movimentos


# ============================================================
# 11. VERIFICAÇÃO DAS CASAS ATACADAS
# ============================================================

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

            # ------------------------------------------------
            # Ataques do peão
            # ------------------------------------------------

            if tipo == "P":

                direcao = -1 if atacante == "b" else 1

                if linha == l + direcao:

                    if abs(coluna - c) == 1:
                        return True

            # ------------------------------------------------
            # Ataques do cavalo
            # ------------------------------------------------

            elif tipo == "C":

                diferenca_linha = abs(linha - l)
                diferenca_coluna = abs(coluna - c)

                if (
                    (diferenca_linha == 2
                     and diferenca_coluna == 1)
                    or
                    (diferenca_linha == 1
                     and diferenca_coluna == 2)
                ):
                    return True

            # ------------------------------------------------
            # Ataques do rei
            # ------------------------------------------------

            elif tipo == "R":

                if (
                    max(
                        abs(linha - l),
                        abs(coluna - c)
                    ) == 1
                ):
                    return True

            # ------------------------------------------------
            # Ataques de torre, bispo e dama
            # ------------------------------------------------

            elif tipo in ["T", "B", "D"]:

                dl = linha - l
                dc = coluna - c

                direcao_linha = 0
                direcao_coluna = 0

                # Movimento horizontal ou vertical.
                movimento_reto = (
                    dl == 0 or dc == 0
                )

                # Movimento diagonal.
                movimento_diagonal = (
                    abs(dl) == abs(dc)
                )

                permitido = False

                if tipo == "T" and movimento_reto:
                    permitido = True

                elif tipo == "B" and movimento_diagonal:
                    permitido = True

                elif tipo == "D":
                    permitido = (
                        movimento_reto
                        or movimento_diagonal
                    )

                if not permitido:
                    continue

                # Descobrimos a direção do ataque.
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

                # Verificamos se existem peças entre
                # o atacante e a casa analisada.
                while (
                    atual_linha,
                    atual_coluna
                ) != (linha, coluna):

                    if tabuleiro[
                        atual_linha
                    ][
                        atual_coluna
                    ] != "--":

                        caminho_livre = False
                        break

                    atual_linha += direcao_linha
                    atual_coluna += direcao_coluna

                if caminho_livre:
                    return True

    return False


# ============================================================
# 12. LOCALIZAÇÃO DO REI
# ============================================================

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


def rei_em_xeque(tabuleiro, cor):
    """
    Verifica se o rei está sob ataque.
    """

    posicao_rei = localizar_rei(tabuleiro, cor)

    if posicao_rei is None:
        return True

    linha, coluna = posicao_rei

    return casa_atacada(
        tabuleiro,
        linha,
        coluna,
        cor_adversaria(cor)
    )


# ============================================================
# 13. IMPLEMENTAÇÃO DO ROQUE
# ============================================================

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

    linha = 7 if cor == "b" else 0

    # O rei deve estar na posição inicial.
    if tabuleiro[linha][4] != cor + "R":
        return movimentos

    if movimentou[cor]["rei"]:
        return movimentos

    # Não podemos realizar roque enquanto estamos em xeque.
    if rei_em_xeque(tabuleiro, cor):
        return movimentos

    adversario = cor_adversaria(cor)

    # --------------------------------------------------------
    # ROQUE PEQUENO
    # --------------------------------------------------------

    if not movimentou[cor]["torre_direita"]:

        if tabuleiro[linha][7] == cor + "T":

            if (
                tabuleiro[linha][5] == "--"
                and tabuleiro[linha][6] == "--"
            ):

                if (
                    not casa_atacada(
                        tabuleiro, linha, 5, adversario
                    )
                    and not casa_atacada(
                        tabuleiro, linha, 6, adversario
                    )
                ):

                    movimentos.append((linha, 6))

    # --------------------------------------------------------
    # ROQUE GRANDE
    # --------------------------------------------------------

    if not movimentou[cor]["torre_esquerda"]:

        if tabuleiro[linha][0] == cor + "T":

            if (
                tabuleiro[linha][1] == "--"
                and tabuleiro[linha][2] == "--"
                and tabuleiro[linha][3] == "--"
            ):

                if (
                    not casa_atacada(
                        tabuleiro, linha, 3, adversario
                    )
                    and not casa_atacada(
                        tabuleiro, linha, 2, adversario
                    )
                ):

                    movimentos.append((linha, 2))

    return movimentos


# ============================================================
# 14. SIMULAÇÃO DE MOVIMENTOS
# ============================================================

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

    # Removemos a peça da casa original.
    copia[linha_origem][coluna_origem] = "--"

    # --------------------------------------------------------
    # Simulação do en passant
    # --------------------------------------------------------

    if (
        peca[1] == "P"
        and coluna_origem != coluna_destino
        and copia[linha_destino][coluna_destino] == "--"
    ):

        # O peão capturado está na linha de origem.
        copia[linha_origem][coluna_destino] = "--"

    # --------------------------------------------------------
    # Simulação do roque
    # --------------------------------------------------------

    if (
        peca[1] == "R"
        and abs(coluna_destino - coluna_origem) == 2
    ):

        if coluna_destino == 6:

            # Torre da direita vai para a coluna 5.
            copia[linha_origem][5] = copia[
                linha_origem
            ][7]

            copia[linha_origem][7] = "--"

        elif coluna_destino == 2:

            # Torre da esquerda vai para a coluna 3.
            copia[linha_origem][3] = copia[
                linha_origem
            ][0]

            copia[linha_origem][0] = "--"

    # Colocamos a peça na posição de destino.
    copia[linha_destino][coluna_destino] = peca

    return copia


# ============================================================
# 15. VALIDAÇÃO DOS MOVIMENTOS LEGAIS
# ============================================================

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

    movimentos = movimentos_basicos(
        tabuleiro,
        linha,
        coluna
    )

    # Acrescentamos as possibilidades de roque.
    if peca[1] == "R":

        movimentos += movimentos_roque(
            tabuleiro,
            cor
        )

    movimentos_validos = []

    for destino in movimentos:

        copia = simular_movimento(
            tabuleiro,
            (linha, coluna),
            destino
        )

        # A jogada só será permitida se o próprio
        # rei permanecer protegido.
        if not rei_em_xeque(copia, cor):

            movimentos_validos.append(destino)

    return movimentos_validos


# ============================================================
# 16. CONTROLE DOS DIREITOS DE ROQUE
# ============================================================

def atualizar_direitos_roque(peca, origem,
                            capturada, destino):
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
        movimentou[cor]["rei"] = True

    elif peca[1] == "T":

        linha_inicial = 7 if cor == "b" else 0

        if linha == linha_inicial:

            if coluna == 0:
                movimentou[cor]["torre_esquerda"] = True

            elif coluna == 7:
                movimentou[cor]["torre_direita"] = True

    # Verificamos se uma torre foi capturada.
    if capturada != "--" and capturada[1] == "T":

        cor_capturada = capturada[0]

        linha_inicial = (
            7 if cor_capturada == "b" else 0
        )

        linha_destino, coluna_destino = destino

        if linha_destino == linha_inicial:

            if coluna_destino == 0:
                movimentou[
                    cor_capturada
                ]["torre_esquerda"] = True

            elif coluna_destino == 7:
                movimentou[
                    cor_capturada
                ]["torre_direita"] = True


# ============================================================
# 17. INÍCIO DA ANIMAÇÃO
# ============================================================

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

    peca_movendo = tabuleiro_estado[
        linha_origem
    ][
        coluna_origem
    ]

    imagem = imagens[peca_movendo]

    largura = imagem.get_width()
    altura = imagem.get_height()

    # Posição inicial da imagem.
    pos_atual_anim_x = (
        coluna_origem * TAMANHO_QUADRADO
        + (TAMANHO_QUADRADO - largura) // 2
    )

    pos_atual_anim_y = (
        linha_origem * TAMANHO_QUADRADO
        + (TAMANHO_QUADRADO - altura) // 2
    )

    # Posição final da imagem.
    destino_anim_x = (
        coluna_destino * TAMANHO_QUADRADO
        + (TAMANHO_QUADRADO - largura) // 2
    )

    destino_anim_y = (
        linha_destino * TAMANHO_QUADRADO
        + (TAMANHO_QUADRADO - altura) // 2
    )

    destino_final = destino

    jogada_animacao = {
        "origem": origem,
        "destino": destino,
        "peca": peca_movendo
    }

    animando = True


# ============================================================
# 18. EXECUÇÃO DA JOGADA
# ============================================================

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

    origem = jogada_animacao["origem"]
    destino = jogada_animacao["destino"]
    peca = jogada_animacao["peca"]

    lo, co = origem
    ld, cd = destino

    capturada = tabuleiro_estado[ld][cd]

    # --------------------------------------------------------
    # Captura en passant
    # --------------------------------------------------------

    if (
        peca[1] == "P"
        and co != cd
        and capturada == "--"
    ):

        # A peça capturada está ao lado do peão.
        tabuleiro_estado[lo][cd] = "--"

        mostrar_mensagem("Captura en passant!")

    # --------------------------------------------------------
    # Atualização dos direitos de roque
    # --------------------------------------------------------

    atualizar_direitos_roque(
        peca,
        origem,
        capturada,
        destino
    )

    # --------------------------------------------------------
    # Movimento normal da peça
    # --------------------------------------------------------

    tabuleiro_estado[lo][co] = "--"
    tabuleiro_estado[ld][cd] = peca

    # --------------------------------------------------------
    # Movimentação da torre durante o roque
    # --------------------------------------------------------

    if (
        peca[1] == "R"
        and abs(cd - co) == 2
    ):

        if cd == 6:

            # Roque pequeno.
            tabuleiro_estado[ld][5] = tabuleiro_estado[
                ld
            ][7]

            tabuleiro_estado[ld][7] = "--"

            mostrar_mensagem("Roque pequeno!")

        elif cd == 2:

            # Roque grande.
            tabuleiro_estado[ld][3] = tabuleiro_estado[
                ld
            ][0]

            tabuleiro_estado[ld][0] = "--"

            mostrar_mensagem("Roque grande!")

    # --------------------------------------------------------
    # Atualização do en passant
    # --------------------------------------------------------

    # O direito anterior deixa de existir após esta jogada.
    en_passant = None

    # Se um peão avançou duas casas, registramos a casa
    # intermediária que poderá ser utilizada na captura.
    if (
        peca[1] == "P"
        and abs(ld - lo) == 2
    ):

        linha_intermediaria = (lo + ld) // 2

        en_passant = (
            linha_intermediaria,
            co
        )

    # --------------------------------------------------------
    # Promoção do peão
    # --------------------------------------------------------

    if peca[1] == "P":

        ultima_linha = 0 if peca[0] == "b" else 7

        if ld == ultima_linha:

            promocao_pendente = (ld, cd)

            mostrar_mensagem(
                "PROMOÇÃO: pressione D, T, B ou C"
            )

            jogada_animacao = None
            return

    # --------------------------------------------------------
    # Alternância entre jogadores
    # --------------------------------------------------------

    turno_atual = cor_adversaria(turno_atual)

    peca_selecionada = None
    origem_selecionada = None
    movimentos_disponiveis = []

    jogada_animacao = None

    # Informamos quando o adversário está em xeque.
    if rei_em_xeque(tabuleiro_estado, turno_atual):

        mostrar_mensagem(
            "XEQUE! Vez das "
            + (
                "brancas"
                if turno_atual == "b"
                else "pretas"
            )
        )

    else:

        mostrar_mensagem(
            "Vez das "
            + (
                "brancas"
                if turno_atual == "b"
                else "pretas"
            )
        )


# ============================================================
# 19. PROMOÇÃO DE PEÕES
# ============================================================

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

    # Substituímos o peão pela peça escolhida.
    tabuleiro_estado[linha][coluna] = cor + tipo

    promocao_pendente = None

    # Finalizamos o turno após a promoção.
    turno_atual = cor_adversaria(turno_atual)

    peca_selecionada = None
    origem_selecionada = None
    movimentos_disponiveis = []

    if rei_em_xeque(tabuleiro_estado, turno_atual):

        mostrar_mensagem(
            "Promoção realizada! XEQUE!"
        )

    else:

        mostrar_mensagem(
            "Promoção realizada!"
        )


# ============================================================
# 20. SELEÇÃO DE PEÇAS E MOVIMENTAÇÃO
# ============================================================

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

    # --------------------------------------------------------
    # Nenhuma peça está selecionada
    # --------------------------------------------------------

    if origem_selecionada is None:

        # Só podemos selecionar peças do jogador atual.
        if peca != "--" and peca[0] == turno_atual:

            peca_selecionada = peca

            origem_selecionada = (
                linha,
                coluna
            )

            movimentos_disponiveis = movimentos_legais(
                tabuleiro_estado,
                linha,
                coluna
            )

            exibir_movimentos_legais(movimentos_disponiveis)

        return

    # --------------------------------------------------------
    # Clicamos novamente na peça selecionada
    # --------------------------------------------------------

    if origem_selecionada == (linha, coluna):

        peca_selecionada = None
        origem_selecionada = None
        movimentos_disponiveis = []

        return

    # --------------------------------------------------------
    # Selecionamos outra peça da mesma cor
    # --------------------------------------------------------

    if peca != "--" and peca[0] == turno_atual:

        peca_selecionada = peca

        origem_selecionada = (
            linha,
            coluna
        )

        movimentos_disponiveis = movimentos_legais(
            tabuleiro_estado,
            linha,
            coluna
        )

        exibir_movimentos_legais(movimentos_disponiveis)
        return

    # --------------------------------------------------------
    # Tentativa de movimentação
    # --------------------------------------------------------

    destino = (linha, coluna)

    if destino in movimentos_disponiveis:

        iniciar_animacao(
            origem_selecionada,
            destino
        )

        # A seleção é limpa depois da animação.

    else:

        mostrar_mensagem(
            "Movimento inválido!"
        )


# ============================================================
# 21. ATUALIZAÇÃO DA ANIMAÇÃO
# ============================================================

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

    velocidade_deslize = 0.015

    fator = velocidade_deslize * dt

    # Limitamos o fator para evitar ultrapassar o destino.
    fator = min(fator, 1.0)

    pos_atual_anim_x += (
        destino_anim_x - pos_atual_anim_x
    ) * fator

    pos_atual_anim_y += (
        destino_anim_y - pos_atual_anim_y
    ) * fator

    # Quando a peça chega suficientemente perto,
    # encerramos a animação.
    if (
        abs(destino_anim_x - pos_atual_anim_x) < 0.5
        and
        abs(destino_anim_y - pos_atual_anim_y) < 0.5
    ):

        pos_atual_anim_x = destino_anim_x
        pos_atual_anim_y = destino_anim_y

        animando = False

        finalizar_jogada()


# ============================================================
# 22. DESENHO DA PEÇA EM MOVIMENTO
# ============================================================

def desenhar_animacao(screen):
    """
    Desenha a peça na posição intermediária
    calculada pela animação.
    """

    if not animando:
        return

    imagem = imagens[peca_movendo]

    screen.blit(
        imagem,
        (
            pos_atual_anim_x,
            pos_atual_anim_y
        )
    )


# ============================================================
# 23. INTERFACE DE PROMOÇÃO
# ============================================================

def desenhar_promocao(screen):
    """
    Exibe uma mensagem quando o jogador precisa
    escolher a peça de promoção.
    """

    if promocao_pendente is None:
        return

    # Criamos uma superfície semitransparente.
    camada = pygame.Surface(
        (LARGURA, ALTURA),
        pygame.SRCALPHA
    )

    camada.fill((0, 0, 0, 170))

    screen.blit(camada, (0, 0))

    # Caixa central.
    caixa = pygame.Rect(
        60,
        250,
        520,
        140
    )

    pygame.draw.rect(
        screen,
        (245, 235, 215),
        caixa,
        border_radius=12
    )

    pygame.draw.rect(
        screen,
        (90, 60, 40),
        caixa,
        3,
        border_radius=12
    )

    texto1 = fonte.render(
        "PROMOÇÃO DO PEÃO",
        True,
        (40, 40, 40)
    )

    texto2 = fonte.render(
        "D = Dama   T = Torre",
        True,
        (40, 40, 40)
    )

    texto3 = fonte.render(
        "B = Bispo   C = Cavalo",
        True,
        (40, 40, 40)
    )

    screen.blit(texto1, (185, 265))
    screen.blit(texto2, (175, 310))
    screen.blit(texto3, (165, 345))


# ============================================================
# 24. CARREGAMENTO INICIAL
# ============================================================

# As imagens são carregadas apenas uma vez.
#
# Isso evita carregar arquivos repetidamente durante
# a execução e melhora o desempenho do jogo.

carregar_imagens()

mostrar_mensagem("Vez das brancas")


# ============================================================
# 25. LOOP PRINCIPAL DO JOGO
# ============================================================

# O loop principal mantém o jogo funcionando.
#
# Em cada repetição:
# 1. Lemos os eventos do usuário.
# 2. Atualizamos as animações.
# 3. Desenhamos o tabuleiro.
# 4. Desenhamos as peças.
# 5. Atualizamos a janela.

while True:

    # --------------------------------------------------------
    # Controle do tempo
    # --------------------------------------------------------

    clock.tick(60)

    dt = clock.get_time()

    # --------------------------------------------------------
    # Leitura dos eventos
    # --------------------------------------------------------

    for event in pygame.event.get():

        # Fechar a janela.
        if event.type == pygame.QUIT:

            pygame.quit()
            sys.exit()

        # ----------------------------------------------------
        # Eventos do teclado
        # ----------------------------------------------------

        elif event.type == pygame.KEYDOWN:

            # Se existe uma promoção pendente,
            # o teclado escolhe a nova peça.
            if promocao_pendente is not None:

                teclas_promocao = {
                    pygame.K_d: "D",
                    pygame.K_t: "T",
                    pygame.K_b: "B",
                    pygame.K_c: "C"
                }

                if event.key in teclas_promocao:

                    promover_peao(
                        teclas_promocao[event.key]
                    )

                continue

            # Não permitimos movimentos durante a animação.
            if animando:
                continue

            # As setas movimentam o cursor do teclado.
            if event.key == pygame.K_UP:

                cursor_linha = max(
                    0,
                    cursor_linha - 1
                )

            elif event.key == pygame.K_DOWN:

                cursor_linha = min(
                    7,
                    cursor_linha + 1
                )

            elif event.key == pygame.K_LEFT:

                cursor_coluna = max(
                    0,
                    cursor_coluna - 1
                )

            elif event.key == pygame.K_RIGHT:

                cursor_coluna = min(
                    7,
                    cursor_coluna + 1
                )

            # Enter seleciona ou movimenta a peça.
            elif event.key == pygame.K_RETURN:

                selecionar_casa(
                    cursor_linha,
                    cursor_coluna
                )

            # Escape cancela a seleção.
            elif event.key == pygame.K_ESCAPE:

                peca_selecionada = None
                origem_selecionada = None
                movimentos_disponiveis = []

        # ----------------------------------------------------
        # Eventos do mouse
        # ----------------------------------------------------

        elif event.type == pygame.MOUSEBUTTONDOWN:

            # Utilizamos apenas o botão esquerdo.
            if event.button == 1:

                if (
                    not animando
                    and promocao_pendente is None
                ):

                    x, y = event.pos

                    coluna = x // TAMANHO_QUADRADO
                    linha = y // TAMANHO_QUADRADO

                    # Sincronizamos o cursor do teclado.
                    cursor_linha = linha
                    cursor_coluna = coluna

                    selecionar_casa(
                        linha,
                        coluna
                    )

    # --------------------------------------------------------
    # Atualização da animação
    # --------------------------------------------------------

    atualizar_animacao(dt)

    # --------------------------------------------------------
    # Limpeza da janela
    # --------------------------------------------------------

    screen.fill((56, 203, 171))

    # --------------------------------------------------------
    # Desenho do tabuleiro
    # --------------------------------------------------------

    desenhar_tabuleiro(screen)

    # --------------------------------------------------------
    # Desenho das peças
    # --------------------------------------------------------

    desenhar_pecas(screen)

    # --------------------------------------------------------
    # Desenho da animação
    # --------------------------------------------------------

    desenhar_animacao(screen)

    # --------------------------------------------------------
    # Destaque do cursor do teclado
    # --------------------------------------------------------

    # Desenhamos um contorno azul na casa selecionada
    # pelas setas do teclado.
    pygame.draw.rect(
        screen,
        (50, 100, 230),
        (
            cursor_coluna * TAMANHO_QUADRADO,
            cursor_linha * TAMANHO_QUADRADO,
            TAMANHO_QUADRADO,
            TAMANHO_QUADRADO
        ),
        2
    )

    # --------------------------------------------------------
    # Letras e números da notação oficial do xadrez
    # --------------------------------------------------------

    desenhar_coordenadas(screen)

    # --------------------------------------------------------
    # Interface de promoção
    # --------------------------------------------------------

    desenhar_promocao(screen)

    # --------------------------------------------------------
    # Atualização da janela
    # --------------------------------------------------------

    pygame.display.update()
