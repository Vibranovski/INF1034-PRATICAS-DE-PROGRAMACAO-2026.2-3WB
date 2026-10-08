#bom dia

import pygame

## Definições de funções
# def valida_email(email):
#     sufixo = email[-8:]
#     if sufixo == "@puc.com":
#         return True
#     else:
#         return False

def valida_email(email):
    return email[-8:] == "@puc.com"

def possui_maiuscula(senha):
    for carac in senha:
        if 'A' <= carac <= 'Z':
            return True
    return False

def possui_minuscula(senha):
    for carac in senha:
        if 'a' <= carac <= 'z':
            return True
    return False

def possui_numero(senha):
    for carac in senha:
        if carac.isnumeric():
            return True
    return False

def valida_senha(senha):
    if len(senha) < 8:
        return False
    if not possui_maiuscula(senha):
        return False
    if not possui_minuscula(senha):
        return False
    if not possui_numero(senha):
        return False
    
    return True

def criptografa(senha):
    senha_cripto = ""
    for carac in senha:
        if carac.isalpha():
            pos_alpha = ord(carac) - ord('a')
            pos_alpha = (pos_alpha + 3) % 26
            pos_ascii = pos_alpha + ord('a')
            senha_cripto += chr(pos_ascii)
    return senha_cripto


# Configurar e utilizar o pygame
pygame.init()
screen = pygame.display.set_mode((1000, 520))
pygame.display.set_caption("Login e casinha")
running = True
relogio = pygame.time.Clock()

input_string = ""
input_senha = ""
campo = "email"
valid_email = False
valid_senha = False
pressed_enter = False
login = False
senha_cripto = ""
mensagem = ""
fonte = pygame.font.Font(None, 50)
fonte_validation = pygame.font.Font(None, 25)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not login:
            if pygame.Rect(100, 100, 500, 50).collidepoint(event.pos):
                campo = "email"
            elif pygame.Rect(100, 210, 500, 50).collidepoint(event.pos):
                campo = "senha"
            elif pygame.Rect(100, 300, 180, 50).collidepoint(event.pos):
                pressed_enter = True
        if event.type == pygame.KEYDOWN and not login:
            if event.key == pygame.K_BACKSPACE:
                if campo == "email":
                    input_string = input_string[:-1]
                else:
                    input_senha = input_senha[:-1]
                pressed_enter = False
            elif event.key == pygame.K_TAB:
                if campo == "email":
                    campo = "senha"
                else:
                    campo = "email"
            elif event.key == pygame.K_RETURN:
                if campo == "email":
                    campo = "senha"
                else:
                    pressed_enter = True
            elif event.unicode.isprintable() and event.unicode:
                if campo == "email":
                    input_string += event.unicode
                else:
                    input_senha += event.unicode
                pressed_enter = False

    if pressed_enter and not login:
        valid_email = valida_email(input_string)
        valid_senha = valida_senha(input_senha)
        valid_caracteres = True
        for carac in input_senha:
            if not '0' <= carac <= 'z':
                valid_caracteres = False

        if not valid_email:
            mensagem = "O seu e-mail não é válido. Digite novamente!"
        elif not valid_senha:
            mensagem = "A senha precisa de 8 caracteres, uma maiúscula, uma minúscula e um número."
        elif not valid_caracteres:
            mensagem = "Use na senha apenas caracteres ASCII entre '0' e 'z'."
        else:
            senha_cripto = criptografa(input_senha)
            login = True

    screen.fill("white")
    if not login:
        screen.blit(fonte_validation.render("E-mail", True, "black"), (100, 70))
        screen.blit(fonte_validation.render("Senha", True, "black"), (100, 180))
        pygame.draw.rect(screen, "black", (100, 100, 500, 50), 3)
        pygame.draw.rect(screen, "black", (100, 210, 500, 50), 3)
        if campo == "email":
            pygame.draw.rect(screen, "blue", (100, 100, 500, 50), 3)
        else:
            pygame.draw.rect(screen, "blue", (100, 210, 500, 50), 3)

        screen.set_clip((110, 103, 480, 44))
        input_text = fonte.render(input_string, True, "#000000")
        screen.blit(input_text, (120, 105))
        screen.set_clip((110, 213, 480, 44))
        input_text = fonte.render("*" * len(input_senha), True, "#000000")
        screen.blit(input_text, (120, 215))
        screen.set_clip(None)

        pygame.draw.rect(screen, "green", (100, 300, 180, 50))
        screen.blit(fonte.render("Entrar", True, "white"), (130, 307))
        if pressed_enter:
            valid_text = fonte_validation.render(mensagem, True, "red")
            screen.blit(valid_text, (100, 380))
    else:
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

    pygame.display.update()
    relogio.tick(60)

pygame.quit()