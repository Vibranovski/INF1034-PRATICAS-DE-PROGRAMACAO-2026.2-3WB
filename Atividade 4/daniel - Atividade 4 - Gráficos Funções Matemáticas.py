from turtle import *
from random import randint
from time import sleep

t = Turtle()
t.speed(0)

# --- Definição das funções matemáticas ---
def soma_10(x):
    return x + 10

def eleva_ao_quadrado(x):
    return x ** 2

def calcula_raiz(x):
    return x ** (1/2)

def calcula_divisao(x):
    return 1 / x

def calcula_dois_elevado_a_x(x):
    return 2 ** x

def calcula_funcao_quadratica(x):
    return x ** 2 - 5 * x + 6

def calcula_funcao_cubica(x):
    return x ** 3 - x ** 2 - x + 1

# Função mais simples e correta para o plano cartesiano
def desenha_eixo(x_inicial, y_inicial, angulo, tamanho):
    t.color("black")
    t.setheading(angulo)
    t.pu()
    t.goto(x_inicial, y_inicial)
    t.pd()
    t.fd(tamanho)
    t.stamp()
    t.pu() # Volta para o centro (0,0) para organizar
    t.goto(0, 0)

# Gráfico de f(x) = x + 10
desenha_eixo(0, -300, 90, 600)
desenha_eixo(-300, 0, 0, 600)

t.color("blue")
t.pu()
x = -250
y = soma_10(-250)
t.goto(x, y)
t.pd()
t.goto(250, soma_10(250))

# Permanece por 5 segundos
sleep(3)

# Limpa o turtle e o desenho
t.clear()

# --- Gráfico de f(x) = x**2 (Parábola) ---
desenha_eixo(0, -300, 90, 600)
desenha_eixo(-300, 0, 0, 600)

t.color("red")
t.pu()
t.goto(-200, eleva_ao_quadrado(-20))
t.pd()
for x in range(-20, 21):
    t.goto(10*x, eleva_ao_quadrado(x))

sleep(3)
t.clear()

# --- Gráfico de f(x) = x**(1/2) ---
desenha_eixo(0, -300, 90, 600)
desenha_eixo(-300, 0, 0, 600)

t.color("red")
t.pu()
t.goto(0, calcula_raiz(0))
t.pd()
for x in range(0, 300):
    t.goto(x, 10*calcula_raiz(x))

sleep(3)
t.clear()

# --- Gráfico de f(x) = 1 / x ---
desenha_eixo(0, -300, 90, 600)
desenha_eixo(-300, 0, 0, 600)

t.color("red")

# Desenha a parte negativa do gráfico
t.pu()
x = -20
t.goto(10 * x, 100 * calcula_divisao(x))
t.pd()

for x in range(-20, 0):
    y = calcula_divisao(x)
    t.goto(10 * x, 100 * y)

# Desenha a parte positiva do gráfico
t.pu()
x = 1
t.goto(10 * x, 100 * calcula_divisao(x))
t.pd()

for x in range(1, 21):
    y = calcula_divisao(x)
    t.goto(10 * x, 100 * y)

sleep(3)
t.clear()

# --- Gráfico de f(x) = 2 ** x ---
desenha_eixo(0, -300, 90, 600)
desenha_eixo(-300, 0, 0, 600)

t.color("red")
t.pu()

# Define o primeiro ponto do gráfico
x = -8
y = calcula_dois_elevado_a_x(x)
t.goto(25 * x, y)

t.pd()

# Desenha o restante do gráfico
for x in range(-8, 9):
    y = calcula_dois_elevado_a_x(x)
    t.goto(25 * x, y)

sleep(3)
t.clear()

# --- Gráfico de y = x² - 5x + 6 ---
desenha_eixo(0, -300, 90, 600)
desenha_eixo(-300, 0, 0, 600)

t.color("red")
t.pu()

# Define o primeiro ponto do gráfico
x = -3
y = calcula_funcao_quadratica(x)
t.goto(30 * x, 5 * y)

t.pd()

# Desenha os outros pontos da parábola
for x in range(-3, 9):
    y = calcula_funcao_quadratica(x)
    t.goto(30 * x, 5 * y)

sleep(3)
t.clear()

# --- Gráfico de y = x³ - x² - x + 1 ---
desenha_eixo(0, -300, 90, 600)
desenha_eixo(-300, 0, 0, 600)

t.color("red")
t.pu()

# Define o primeiro ponto do gráfico
x = -3
y = calcula_funcao_cubica(x)
t.goto(70 * x, 8 * y)

t.pd()

# Desenha os outros pontos do gráfico
for x in range(-3, 4):
    y = calcula_funcao_cubica(x)
    t.goto(70 * x, 8 * y)

sleep(3)
t.clear()

t.hideturtle()

# EXTRA
# Corrida de Tartarugas
def corrida_tartarugas(n):

    cores = ["red", "blue", "green", "orange", "purple", "pink"]
    tartarugas = []

    # Cria as tartarugas
    for numero in range(n):

        nova_tartaruga = Turtle()
        nova_tartaruga.shape("turtle")
        nova_tartaruga.speed(0)
        nova_tartaruga.pu()

        # Define a cor
        nova_tartaruga.color(cores[numero % len(cores)])

        # Define a posição inicial
        posicao_y = 150 - numero * 50
        nova_tartaruga.goto(-300, posicao_y)

        # Guarda a tartaruga na lista
        tartarugas.append(nova_tartaruga)

    sleep(1)

    # Realiza os movimentos da corrida
    for movimento in range(50):

        for tartaruga in tartarugas:
            distancia = randint(1, 20)
            tartaruga.fd(distancia)

# Pergunta a quantidade na própria janela do Turtle
quantidade = numinput(
    "Corrida de Tartarugas",
    "Digite a quantidade de tartarugas:",
    default=3,
    minval=1,
    maxval=6
)

if quantidade is not None:
    corrida_tartarugas(int(quantidade))

mainloop()