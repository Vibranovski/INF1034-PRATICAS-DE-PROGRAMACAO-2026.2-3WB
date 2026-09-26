import pygame
from pygame import *

init()
screen = display.set_mode((800, 600))

# Recursos
michael_jackson_img = image.load("michael_jackson.png")
michael_jackson_img = transform.scale(michael_jackson_img, (200, 200))
michael_jackson_fonte = font.Font("Freedom-10eM.ttf", 50)

running = True
deslocamento = 0.10
nuvem_x = 500
nuvem_y = 100

sol_x, sol_y = pygame.mouse.get_pos()
mouse_anterior = (sol_x, sol_y)

while running: # running == True - aqui é o Daniel comentando, não a IA

    nuvem_x = nuvem_x + deslocamento

    if nuvem_x > 600:
        deslocamento = -0.1
    elif nuvem_x < 50:
        deslocamento = 0.1

    for ev in event.get():
        if ev.type == QUIT:
            running = False
        elif ev.type == pygame.MOUSEBUTTONDOWN:
            if sol_x <= 250:
                pygame.mixer.music.load("1_manha_Bossa_de_Jose_Carlos.mp3")
            elif sol_x <= 500:
                pygame.mixer.music.load("2_tarde_Mapa_de_Ferro.mp3")
            else:
                pygame.mixer.music.load("3_noite_Diego_Acende_Ipanema.mp3")
            pygame.mixer.music.play(-1)

    ## TROCA DE HORAS DO DIA - aqui é o Daniel comentando, não a IA
    ## TROCA COM GRADIENTE - cor do céu/ cor do FUNDO - aqui é o Daniel comentando, não a IA
    cor = pygame.Color(151, 209, 250).lerp(pygame.Color(12, 63, 99), sol_x / 750)
    screen.fill(cor)

    # Primitivas geométricas - aqui é o Daniel comentando, não a IA
    # desenhando quadrados - aqui é o Daniel comentando, não a IA
    draw.rect(screen, "#FF0015", (0, 500, 800, 100)) # piso verde - aqui é o Daniel comentando, não a IA
    draw.rect(screen, "#646464", (200, 300, 200, 200)) # estrutura da casa - aqui é o Daniel comentando, não a IA
    draw.rect(screen, "#0D1664", (220, 350, 40, 60)) # janela da casa - aqui é o Daniel comentando, não a IA
    draw.rect(screen, "#0D1664", (300, 350, 60, 150)) # porta da casa - aqui é o Daniel comentando, não a IA
    draw.rect(screen, "#0D1664", (600, 350, 40, 150)) # tronco da árvore - aqui é o Daniel comentando, não a IA

    # desenha maçaneta da porta - aqui é o Daniel comentando, não a IA
    draw.circle(screen, "#FFFFFF", (310, 450), 5)

    # Se o mouse se mover, o sol acompanha - aqui é o Daniel comentando, não a IA
    mouse_atual = pygame.mouse.get_pos()

    if mouse_atual != mouse_anterior:
        sol_x, sol_y = mouse_atual

    mouse_anterior = mouse_atual

    # Movimentação pelas setas do teclado - aqui é o Daniel comentando, não a IA
    teclas = pygame.key.get_pressed()

    if teclas[pygame.K_LEFT]:
        sol_x = sol_x - 0.1
    elif teclas[pygame.K_RIGHT]:
        sol_x = sol_x + 0.1
    elif teclas[pygame.K_UP]:
        sol_y = sol_y - 0.1
    elif teclas[pygame.K_DOWN]:
        sol_y = sol_y + 0.1

    if sol_x >= 700:
        sol_x = 700
    elif sol_x <= 100:
        sol_x = 100

    if sol_y >= 450:
        sol_y = 450
    elif sol_y <= 100:
        sol_y = 100

    # Desenhando o círculo - aqui é o Daniel comentando, não a IA
    draw.circle(screen, "#FFF251", (sol_x, sol_y), 40)

    # Desenhando as linhas do sol - aqui é o Daniel comentando, não a IA
    draw.line(screen, "#FFF251", (sol_x - 50, sol_y - 50), (sol_x + 50, sol_y + 50), 5)
    draw.line(screen, "#FFF251", (sol_x - 50, sol_y + 50), (sol_x + 50, sol_y - 50), 5)
    draw.line(screen, "#FFF251", (sol_x, sol_y - 50), (sol_x, sol_y + 50), 5)
    draw.line(screen, "#FFF251", (sol_x - 50, sol_y), (sol_x + 50, sol_y), 5)
   
    # desenhando nuvem - círculo - aqui é o Daniel comentando, não a IA
    draw.circle(screen, "#FFFFFF", (nuvem_x, nuvem_y), 40)
    draw.circle(screen, "#FFFFFF", (nuvem_x + 50, nuvem_y), 40)
    draw.circle(screen, "#FFFFFF", (nuvem_x + 100, nuvem_y), 40)
    draw.circle(screen, "#FFFFFF", (nuvem_x + 150, nuvem_y), 40)

    # desenhando as "folhas" da árvore - será um círculo amarelo
    draw.circle(screen, "#FFF251", (625, 275), 80)

    screen.blit(michael_jackson_img, (10, 200))
    texto = michael_jackson_fonte.render("Michael Jackson", True, "#000000")
    screen.blit(texto, (200, 500))

    # desenhando imagens
    screen.blit(michael_jackson_img, (10, 200))
    
    # desenhando o polígono
    draw.polygon(screen, "#000000", ((200, 300), (300, 150), (400, 300)))
    display.update()