import pygame, sys
import random
from pygame.locals import QUIT, KEYDOWN, K_RETURN, K_BACKSPACE

LARGURA_JANELA = 1380
ALTURA_JANELA = 560
LARGURA_PAINEL = 460

# qpeomrcppmoui - aqui é o Daniel comentando.
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZA = (210, 210, 210)

# asçlkdehralksehyir - aqui é o Daniel comentando.
nums = [
    100, 120, 130, 120, 150, 100, 160, 200, 190, 110, 115, 125, 135, 170, 130
]


# Conta quantos numeros caem em cada faixa/categoria.
# tres histogramas (cada um com uma lista e uma quantidade de faixas diferente)
# nxzc,vn.xzc,vnb.,cn - aqui é o Daniel comentando.
def contabiliza_totais(nums, num_cat):
    num_min = min(nums)
    num_max = max(nums)
    tam_cat = (num_max - num_min) / num_cat
    lista_total = [0] * num_cat

    # Para cada número na minha lista
    for i in range(len(nums)):
        # O maior número não cabe em nenhuma faixa (o limite superior não
        # conta), então ele é colocado direto na última faixa
        if nums[i] == num_max:
            lista_total[-1] += 1
            continue

        # Para cada faixa/categoria
        for i_cat in range(num_cat):
            # Obtém os limites inferior e superior
            lim_inf = num_min + i_cat * tam_cat
            lim_sup = lim_inf + tam_cat

            # Checa em qual faixa/categoria o número está com base nesses limites
            if lim_inf <= nums[i] < lim_sup:
                lista_total[i_cat] += 1
                break
    return lista_total


# qwepiorquwoeiru - aqui é o Daniel comentando.
def cria_rotulos(nums, num_cat):
    num_min = min(nums)
    tam_cat = (max(nums) - num_min) / num_cat
    rotulos = []
    for i_cat in range(num_cat):
        lim_inf = num_min + i_cat * tam_cat
        lim_sup = lim_inf + tam_cat
        rotulos.append(str(round(lim_inf)) + "-" + str(round(lim_sup)))
    return rotulos


# ouciwerouinfvowierun - aqui é o Daniel comentando.
def cor_aleatoria():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return (r, g, b)

# nkjhfglkjfh - aqui é o Daniel comentando.
def cria_cores(num_cat):
    cores = []
    for i in range(num_cat):
        cores.append(cor_aleatoria())
    return cores

def sorteia_totais(nums, num_cat):
    restante = len(nums)
    lista_total = []
    for i in range(num_cat):
        sorteado = random.randint(0, restante)
        lista_total.append(sorteado)
        restante = restante - sorteado
    return lista_total


def converte_texto(texto):
    lista = []
    for pedaco in texto.split():
        if pedaco.isdigit() and int(pedaco) <= 1000:
            lista.append(int(pedaco))
        else:
            return [], "Valor invalido: " + pedaco + " (use numeros de 0 a 1000)"
    if len(lista) < 2:
        return [], "Digite pelo menos dois numeros"
    return lista, ""


def tela_de_entrada(screen, fonte):
    texto = ""
    erro = ""

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return None
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    lista, erro = converte_texto(texto)
                    if erro == "":
                        return lista
                elif event.key == K_BACKSPACE:
                    texto = texto[:-1]
                elif event.unicode.isdigit() or event.unicode == " ":
                    if len(texto) < 100:
                        texto = texto + event.unicode

        screen.fill(BRANCO)
        instrucao = fonte.render("Digite os valores para o histograma 3 (de 0 a 1000) separados por espaco e aperte Enter:", True, PRETO)
        screen.blit(instrucao, (60, 150))

        caixa = pygame.Rect(60, 190, LARGURA_JANELA - 120, 40)
        pygame.draw.rect(screen, PRETO, caixa, 2)
        texto_img = fonte.render(texto, True, PRETO)
        screen.blit(texto_img, (caixa.x + 10, caixa.y + 10))

        erro_img = fonte.render(erro, True, (200, 0, 0))
        screen.blit(erro_img, (60, 250))
        pygame.display.update()


def draw(screen, fonte, x_painel, titulo, rotulos, lista_total, cores):
    # Margens para sobrar espaco para os numeros e nomes dos eixos
    esquerda = x_painel + 60
    direita = x_painel + LARGURA_PAINEL - 20
    topo = 80
    base = ALTURA_JANELA - 90
    altura_grafico = base - topo
    largura_grafico = direita - esquerda

    # Escolhe o passo das marcacoes do eixo y e o valor maximo do eixo
    maior = max(lista_total)
    if maior <= 10:
        passo = 1
    elif maior <= 20:
        passo = 2
    else:
        passo = 5
    valor_max = ((maior + passo - 1) // passo) * passo
    if valor_max == 0:
        valor_max = passo

    titulo_img = fonte.render(titulo, True, PRETO)
    screen.blit(titulo_img, (esquerda, 30))

    # Linhas horizontais de fundo e os numeros do eixo y
    valor = 0
    while valor <= valor_max:
        y = base - (valor / valor_max) * altura_grafico
        pygame.draw.line(screen, CINZA, (esquerda, y), (direita, y), 1)
        pygame.draw.line(screen, PRETO, (esquerda - 5, y), (esquerda, y), 2)
        numero_img = fonte.render(str(valor), True, PRETO)
        screen.blit(numero_img, (esquerda - 12 - numero_img.get_width(), y - 8))
        valor += passo

    # Barras: cada faixa ocupa uma fatia igual da largura do grafico
    num_cat = len(lista_total)
    largura_fatia = largura_grafico / num_cat
    for i in range(num_cat):
        h = (lista_total[i] / valor_max) * altura_grafico
        x = esquerda + i * largura_fatia
        retangulo = pygame.Rect(x + 2, base - h, largura_fatia - 4, h)
        pygame.draw.rect(screen, cores[i], retangulo)
        pygame.draw.rect(screen, PRETO, retangulo, 1)

        # Total escrito em cima da barra
        total_img = fonte.render(str(lista_total[i]), True, PRETO)
        x_texto = x + (largura_fatia - total_img.get_width()) / 2
        screen.blit(total_img, (x_texto, base - h - 18))

        # Nome da faixa escrito abaixo do eixo x, na vertical para caber
        nome_img = fonte.render(rotulos[i], True, PRETO)
        nome_img = pygame.transform.rotate(nome_img, 90)
        x_nome = x + (largura_fatia - nome_img.get_width()) / 2
        screen.blit(nome_img, (x_nome, base + 8))

    # Eixos x e y desenhados por cima de tudo
    pygame.draw.line(screen, PRETO, (esquerda, topo), (esquerda, base), 2)
    pygame.draw.line(screen, PRETO, (esquerda, base), (direita, base), 2)

    # Nome de cada eixo
    nome_y = fonte.render("Quantidade", True, PRETO)
    screen.blit(nome_y, (x_painel + 5, topo - 25))
    nome_x = fonte.render("Faixas", True, PRETO)
    screen.blit(nome_x, (esquerda + largura_grafico / 2 - 20, ALTURA_JANELA - 25))



def main():
    pygame.init()
    screen = pygame.display.set_mode((LARGURA_JANELA, ALTURA_JANELA))
    pygame.display.set_caption('Histogramas')
    fonte = pygame.font.SysFont("arial", 16)

    # input do usuario para o histograma 3
    lista_usuario = tela_de_entrada(screen, fonte)
    if lista_usuario is None:
        pygame.quit()
        sys.exit()

    # 1 - lista aleatoria com 60 numeros e 5 faixas
    lista_aleatoria = []
    for i in range(60):
        lista_aleatoria.append(random.randint(0, 100))
    cat1 = 5
    totais1 = contabiliza_totais(lista_aleatoria, cat1)
    rotulos1 = cria_rotulos(lista_aleatoria, cat1)
    cores1 = cria_cores(cat1)

    # 2 - lista estatica do professor com 4 faixas e totais sorteados
    cat2 = 4
    totais2 = sorteia_totais(nums, cat2)
    rotulos2 = cria_rotulos(nums, cat2)
    cores2 = cria_cores(cat2)

    # 3 - lista do usuario com 6 faixas
    cat3 = 6
    totais3 = contabiliza_totais(lista_usuario, cat3)
    rotulos3 = cria_rotulos(lista_usuario, cat3)
    cores3 = cria_cores(cat3)

    # Comeca mostrando o primeiro histograma
    histograma = 1

    # Botoes para trocar o histograma
    botao_anterior = pygame.Rect(20, 520, 120, 30)
    botao_proximo = pygame.Rect(LARGURA_JANELA - 140, 520, 120, 30)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if botao_proximo.collidepoint(event.pos):
                        histograma += 1

                        # Depois do terceiro, volta para o primeiro
                        if histograma > 3:
                            histograma = 1

                    elif botao_anterior.collidepoint(event.pos):
                        histograma -= 1

                        # Antes do primeiro, volta para o terceiro
                        if histograma < 1:
                            histograma = 3

        screen.fill(BRANCO)

        if histograma == 1:
            draw(screen, fonte, 0, "1) Lista aleatoria (60 numeros)",
                 rotulos1, totais1, cores1)

        elif histograma == 2:
            draw(screen, fonte, 0, "2) Lista estatica (15 numeros)",
                 rotulos2, totais2, cores2)

        elif histograma == 3:
            draw(screen, fonte, 0, "3) Lista do usuario",
                 rotulos3, totais3, cores3)

        # Desenha os botoes
        pygame.draw.rect(screen, CINZA, botao_anterior)
        pygame.draw.rect(screen, PRETO, botao_anterior, 2)

        pygame.draw.rect(screen, CINZA, botao_proximo)
        pygame.draw.rect(screen, PRETO, botao_proximo, 2)

        texto_anterior = fonte.render("< Anterior", True, PRETO)
        texto_proximo = fonte.render("Proximo >", True, PRETO)

        screen.blit(texto_anterior,
                    (botao_anterior.x + 20, botao_anterior.y + 5))
        screen.blit(texto_proximo,
                    (botao_proximo.x + 20, botao_proximo.y + 5))

        pygame.display.update()


main()