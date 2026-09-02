from turtle import *
from random import randint
t = Turtle() # t.shape("turtle")

# Definição da função
def f(x):
    return x + 2

# Chamada da função + print
print(f(2))

def desenha_retangulo(x, y, lado_um, lado_dois, cor):
    t.pu()
    t.goto(x, y)  
    t.pd()
    t.color("black")
    t.fillcolor(cor)
    t.begin_fill()

    for cont in range(2): # Retângulo tem lados diferentes (2 repetições)
        t.fd(lado_um)
        t.lt(90)
        t.fd(lado_dois)
        t.lt(90)
    t.end_fill()
    return

def desenha_triangulo(x, y, lado, cor):
    t.pu()
    t.goto(x, y)
    t.pd()
    t.color("black")
    t.fillcolor(cor)
    t.begin_fill()  

    for cont in range(3): # Triângulo tem 3 lados
        t.fd(lado)
        t.lt(120)
    t.end_fill()
    return

def desenha_octogono(x, y, lado, cor):
    t.pu()
    t.goto(x, y)
    t.pd()
    t.color("black")
    t.fillcolor(cor)
    t.begin_fill()  

    for cont in range(8): # Octógono tem 8 lados
        t.fd(lado)
        t.lt(45) # 360 / 8 = 45 graus
    t.end_fill()
    return

def desenha_pentagono(x, y, lado, cor):
    t.pu()
    t.goto(x, y)
    t.pd()
    t.color("black")
    t.fillcolor(cor)
    t.begin_fill()  

    for cont in range(5): # Pentágono tem 5 lados
        t.fd(lado)
        t.lt(72) # 360 / 5 = 72 graus
    t.end_fill()
    return

def desenha_plano_cartesiano(x, y, z, w):
    t.pu()
    t.goto(x, y)
    t.pd()
    t.lt(z)
    t.fd(w)
    t.stamp()
    return

def desenhar_funcao_generica(x, y, lado, cor, n):
    t.pu()
    t.goto(x, y)
    t.pd()
    t.color("black")
    t.fillcolor(cor)
    t.begin_fill()  

    angulo = 360 / n
    
    for cont in range(n): # Polígono tem n lados
        t.fd(lado)
        t.lt(angulo) # 360 / n = angulo
    t.end_fill()
    return

# Desenhar o plano cartesiano
desenha_plano_cartesiano(0, -350, 90, 700)
desenha_plano_cartesiano(-400, 0, 270, 800)

# --- QUADRANTE 1: Retângulo ---
x = randint(250,300)
y = randint(250,300)
desenha_retangulo(x, y, 90, 60, "yellow")

# --- QUADRANTE 2: Triângulo Equilátero ---
x = randint(-300, -250)
y = randint(250, 300)
desenha_triangulo(x, y, 100, "red")

# --- QUADRANTE 3: Octógono ---
x = randint(-350, -300)
y = randint(-300, -250)
desenha_octogono(x, y, 30, "blue")

# --- QUADRANTE 4: Pentágono ---
x = randint(200, 300)
y = randint(-200, -150)
desenha_pentagono(x, y, 50, "green")

# --- EXTRA: Espiral (Substituindo uma das formas) ---
t.pu()
t.goto(-100,-100)
t.pd()

t.color("black")
# Desenhando uma espiral simples
tamanho = 2
for cont in range(30):
    t.fd(tamanho)
    t.lt(60)
    tamanho = tamanho + 2 # Aumenta o traço a cada volta
    
# --- EXTRA 2 : Polígono genérico ---
n = randint(4, 12)
desenhar_funcao_generica(150, 100, 20, "black", n)
    
mainloop()