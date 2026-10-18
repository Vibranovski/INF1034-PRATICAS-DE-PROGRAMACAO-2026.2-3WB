import tkinter
import turtle
from time import sleep

t = turtle.Turtle()
turtle.colormode(255)
t.speed(0)
t.pu()

# Criar um desenho recursivo fácil (até 5 ou 6 linhas, sem uso de função) (200XP)
# aqui é o Daniel comentando e não a IA
for i in range(20, 140, 20):
    t.goto(i, i)
    t.pd()
    for j in range(4):
        t.fd(i * 2)
        t.rt(90)
    t.pu()

sleep(3)
t.clear()

# Criar um desenho recursivo médio (entre 6 e 15 linhas, incluindo função) (300XP)
# asdlkfjaçsldfjaçsldfjdflk - a IA nunca faria um comentário desses 
# aqui é o Daniel comentando e não a IA
def arvore(tamanho, nivel, angulo, caneta):   
    if nivel == 0:
        return
    caneta.forward(tamanho)
    for giro in (-angulo, 0, angulo):
        caneta.left(giro)
        arvore(tamanho * 0.7, nivel - 1, angulo, caneta)
        caneta.right(giro)
    caneta.backward(tamanho)

t.pu()
t.goto(0, 0)
t.color("darkgreen")
t.setheading(90)
t.pd()
arvore(100, 5, 30, t)

sleep(3)
t.clear()

# Criar um desenho recursivo difícil (15+ linhas, incluindo função) (400XP)
# asdlkfjaçsldfjaçsldfjdflk - a IA nunca faria um comentário desses 
# aqui é o Daniel comentando e não a IA
def curva(tamanho, nivel, angulo, caneta):
    if nivel == 0:
        caneta.forward(tamanho)
    else:
        curva(tamanho / 3, nivel - 1, angulo, caneta)
        caneta.left(angulo)
        curva(tamanho / 3, nivel - 1, angulo, caneta)
        caneta.right(2 * angulo)
        curva(tamanho / 3, nivel - 1, angulo, caneta)
        caneta.left(angulo)
        curva(tamanho / 3, nivel - 1, angulo, caneta)

def floco(tamanho, nivel, angulo, caneta):
    for i in range(3):
        curva(tamanho, nivel, angulo, caneta)
        caneta.right(120)

t.pu()
t.goto(-150, 90)
t.color("darkgreen")
t.setheading(0)
t.pd()

floco(300, 2, 60, t)

sleep(3)
t.clear()







### EXTRA - aqui é o daniel comentando e não a IA - kqcowmedpvocqeikfr - a IA nunca faria um comentário desses
def quadrado(caneta, tamanho):   
    for i in range(20, 140, 20):
        caneta.goto(i - 300, i - 250)
        caneta.pd()
        for j in range(4):
            caneta.fd(tamanho)
            caneta.rt(90)
        caneta.pu()
        caneta.rt(90)
        caneta.pu()

def preparar(caneta, x, y, direcao):
    caneta.clear()
    caneta.pu()
    caneta.goto(x, y)
    caneta.setheading(direcao)
    caneta.pd()

caneta_quadrado = turtle.Turtle()
caneta_arvore = turtle.Turtle()
caneta_floco = turtle.Turtle()

caneta_quadrado.speed(0)
caneta_arvore.speed(0)
caneta_floco.speed(0)

caneta_quadrado.pu()
caneta_arvore.pu()
caneta_floco.pu()

def atualizar_espiral_quadrado(a):
    tamanho = int(a)
    caneta_quadrado.clear()
    caneta_quadrado.pu()
    caneta_quadrado.setheading(0)
    quadrado(caneta_quadrado, tamanho)
    tela.update()

def atualizar_arvore(b):
    tamanho_angulo = int(b)
    preparar(caneta_arvore, 0, -200, 90)
    color = "darkgreen"
    caneta_arvore.color(color)
    arvore(80, 5, tamanho_angulo, caneta_arvore)
    tela.update()

def atualizar_floco(c):
    tamanho_angulo = int(c)
    preparar(caneta_floco, 150, -50, 0)
    caneta_floco.color("darkgreen")
    floco(150, 2, tamanho_angulo, caneta_floco)
    tela.update()

tela = turtle.Screen()

janela = tela.getcanvas().winfo_toplevel()
tela.tracer(0)

slider_quadrado = tkinter.Scale(
    janela,
    from_=10,
    to=100,
    orient="horizontal",
    label="Tamanho do quadrado",
    command=atualizar_espiral_quadrado
)
slider_quadrado.set(40)
slider_quadrado.pack()

slider_arvore = tkinter.Scale(
    janela,
    from_=5,
    to=80,
    orient="horizontal",
    label="Abertura da árvore",
    command=atualizar_arvore
)
slider_arvore.set(30)
slider_arvore.pack()

slider_floco = tkinter.Scale(
    janela,
    from_=10,
    to=150,
    orient="horizontal",
    label="Ângulo do floco",
    command=atualizar_floco
)
slider_floco.set(60)
slider_floco.pack()
atualizar_espiral_quadrado(slider_quadrado.get())
atualizar_arvore(slider_arvore.get())
atualizar_floco(slider_floco.get())

turtle.done()