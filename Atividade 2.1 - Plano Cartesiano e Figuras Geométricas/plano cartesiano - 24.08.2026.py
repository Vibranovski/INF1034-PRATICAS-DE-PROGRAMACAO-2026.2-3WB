from turtle import *

t = Turtle()
# t.shape("turtle")

# Desenhar o plano cartesiano
t.pu()
t.goto(0,-300)
t.pd()
t.lt(90)
t.fd(600)
t.stamp()


t.pu()
t.goto(-300,0)
t.pd()
t.rt(90)
t.fd(600)
t.lt(90)
t.stamp()
t.rt(90)


# --- QUADRANTE 1: Retângulo ---
t.pu()
t.goto(200,200)
t.pd()

# Exemplo usando o textinput para a cor da borda
cor_borda = textinput("Cor do Retângulo", "Digite a cor da borda:")
if cor_borda:
    t.color(cor_borda)

t.fillcolor("purple")
t.begin_fill()
for cont in range(2): # Retângulo tem lados diferentes (2 repetições)
    t.fd(120)
    t.lt(90)
    t.fd(60)
    t.lt(90)
t.end_fill()


# --- QUADRANTE 2: Triângulo Equilátero ---
t.pu()
t.goto(-200,200)
t.pd()

t.color("black")
t.fillcolor("red")
t.begin_fill()
for cont in range(3): # Triângulo tem 3 lados
    t.fd(100)
    t.lt(120) # Ângulo interno de 60, giro externo de 120
t.end_fill()


# --- QUADRANTE 3: Octógono ---
t.pu()
t.goto(-300,-300)
t.pd()

t.color("blue")
t.fillcolor("blue")
t.begin_fill()
# Desenhando uma espiral simples
tamanho = 30
for cont in range(8):
    t.fd(tamanho)
    t.lt(45)
t.end_fill()


# --- QUADRANTE 4: Pentágono ---
t.pu()
t.goto(200,-200)
t.pd()

t.color("green")
t.fillcolor("black")
t.begin_fill()
for cont in range(5): # Pentágono tem 5 lados
    t.fd(80)
    t.lt(72) # 360 / 5 = 72 graus
t.end_fill()


# --- EXTRA: Espiral (Substituindo uma das formas) ---
t.pu()
t.goto(-100,-100)
t.pd()

t.color("blue")
# Desenhando uma espiral simples
tamanho = 2
for cont in range(30):
    t.fd(tamanho)
    t.lt(45)
    tamanho = tamanho + 2 # Aumenta o traço a cada volta


mainloop()