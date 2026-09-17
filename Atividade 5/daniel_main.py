import pygame
from pygame import *

init()
screen = display.set_mode((800, 600))

# Recursos
michael_jackson_img = image.load("michael_jackson.png")
michael_jackson_img = transform.scale(michael_jackson_img, (200, 200))
michael_jackson_fonte = font.Font("Freedom-10eM.ttf", 50)

mixer.music.load("Diego_Acende_Ipanema.mp3")
mixer.music.play(-1)


running = True
deslocamento = 0.10
nuvem_x = 500
nuvem_y = 100

while running: # running == True

    nuvem_x = nuvem_x + deslocamento

    if nuvem_x > 800:
        nuvem_x = -150

    for ev in event.get():
        if ev.type == QUIT:
            running = False

    ## Desenhar os elementos na tela
    screen.fill("#97D1FA") # cor do céu

    # Primitivas geométricas

    # desenhando quadrados
    draw.rect(screen, "#FF0015", (0, 500, 800, 100)) # piso verde
    draw.rect(screen, "#646464", (200, 300, 200, 200)) # estrutura da casa
    draw.rect(screen, "#0D1664", (220, 350, 40, 60)) # janela da casa
    draw.rect(screen, "#0D1664", (300, 350, 60, 150)) # porta da casa
    draw.rect(screen, "#0D1664", (600, 350, 40, 150)) # tronco da árvore

    # desenhando o sol - círculo
    draw.circle(screen, "#FFF251", (100, 100), 40)
    draw.circle(screen, "#FFF251", (625, 275), 80)

    # desenha maçaneta da porta
    draw.circle(screen, "#FFFFFF", (310, 450), 5)

    # desenhando as linhas do sol
    draw.line(screen, "#FFF251", (50, 50), (150, 150), 5)
    draw.line(screen, "#FFF251", (50, 150), (150, 50), 5)
    draw.line(screen, "#FFF251", (100, 50), (100, 150), 5)
    draw.line(screen, "#FFF251", (50, 100), (150, 100), 5)
    
    # desenhando nuvem - círculo - aqui é o Daniel comentando, não sou IA
    draw.circle(screen, "#FFFFFF", (nuvem_x, nuvem_y), 40)
    draw.circle(screen, "#FFFFFF", (nuvem_x + 50, nuvem_y), 40)
    draw.circle(screen, "#FFFFFF", (nuvem_x + 100, nuvem_y), 40)
    draw.circle(screen, "#FFFFFF", (nuvem_x + 150, nuvem_y), 40)


    screen.blit(michael_jackson_img, (10, 200))
    texto = michael_jackson_fonte.render("Michael Jackson", True, "#000000")
    screen.blit(texto, (200, 500))




    # desenhando imagens
    screen.blit(michael_jackson_img, (10, 200))
    
    # desenhando o polígono
    draw.polygon(screen, "#000000", ((200, 300), (300, 150), (400, 300)))
    display.update()

