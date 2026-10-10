from secrets import choice
from random import choice
import pygame
from pygame import *


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
        if '0' <= carac <= '9':
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
        pos_alpha = ord(carac) - ord('0')
        pos_alpha = (pos_alpha + 3) % (ord('z') - ord('0') + 1)
        pos_ascii = pos_alpha + ord('0')
        senha_cripto += chr(pos_ascii)
    return senha_cripto

def descriptografa(senha_cripto):
    senha_original = ""
    for carac in senha_cripto:
        pos_alpha = ord(carac) - ord('0')
        pos_alpha = (pos_alpha - 3) % (ord('z') - ord('0') + 1)
        pos_ascii = pos_alpha + ord('0')
        senha_original += chr(pos_ascii)
    return senha_original


valid_email = False
valid_senha = False



# Configurar e utilizar o pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Login e casinha")
running = True
relogio = pygame.time.Clock()

michael_jackson_img = pygame.image.load("michael_jackson.png")
michael_jackson_img = pygame.transform.scale(michael_jackson_img, (200, 200))
michael_jackson_fonte = pygame.font.Font("Freedom-10eM.ttf", 50)

running = True
deslocamento = 0.10
nuvem_x = 500
nuvem_y = 100

sol_x, sol_y = pygame.mouse.get_pos()
mouse_anterior = (sol_x, sol_y)


input_string = ""
input_senha = ""
campo = "email"
valid_email = False
valid_senha = False
pressed_enter = False
login = False
tela = "login"
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
        if event.type == pygame.MOUSEBUTTONDOWN and tela == "menu":
            if pygame.Rect(250, 180, 300, 70).collidepoint(event.pos):
                tela = "jogo1"
            elif pygame.Rect(250, 280, 300, 70).collidepoint(event.pos):
                tela = "jogo2"
            elif pygame.Rect(250, 380, 300, 70).collidepoint(event.pos):
                tela = "jogo3"
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if tela in ("jogo1", "jogo2", "jogo3"):
                tela = "menu"
                pygame.mixer.music.stop()
        if event.type == pygame.MOUSEBUTTONDOWN and tela == "jogo1":
            if sol_x <= 250:
                pygame.mixer.music.load("1_manha_Bossa_de_Jose_Carlos.mp3")
            elif sol_x <= 500:
                pygame.mixer.music.load("2_tarde_Mapa_de_Ferro.mp3")
            else:
                pygame.mixer.music.load("3_noite_Diego_Acende_Ipanema.mp3")
            pygame.mixer.music.play(-1)
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
            tela = "menu"

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

        if input_senha:
            senha_cesar = criptografa(input_senha)
            senha_original = descriptografa(senha_cesar)
            texto_cripto = fonte_validation.render(
                "Senha criptografada: " + senha_cesar, True, "black"
            )
            screen.blit(texto_cripto, (100, 370))
            texto_descripto = fonte_validation.render(
                "Senha descriptografada: " + senha_original, True, "black"
            )
            screen.blit(texto_descripto, (100, 400))


        pygame.draw.rect(screen, "green", (100, 300, 180, 50))
        screen.blit(fonte.render("Entrar", True, "white"), (130, 307))



    elif tela == "menu":
        screen.fill("white")

        # Mostrar senha criptografada
        texto_cripto = fonte_validation.render(
            "Senha criptografada: " + senha_cripto, True, "black"
        )
        screen.blit(texto_cripto, (100, 490))

        # Descriptografar a senha usando a nova função
        senha_descripto = descriptografa(senha_cripto)

        # Mostrar senha descriptografada
        texto_descripto = fonte_validation.render(
            "Senha descriptografada: " + senha_descripto, True, "black"
        )
        screen.blit(texto_descripto, (100, 520))

        titulo = fonte.render("Escolha um jogo", True, "black")
        screen.blit(titulo, (250, 80))

        pygame.draw.rect(screen, "blue", (250, 180, 300, 70))
        pygame.draw.rect(screen, "blue", (250, 280, 300, 70))
        pygame.draw.rect(screen, "blue", (250, 380, 300, 70))

        screen.blit(fonte.render("Casinha", True, "white"), (330, 195))
        screen.blit(fonte.render("Forca", True, "white"), (330, 295))
        screen.blit(fonte.render("JokenPô", True, "white"), (330, 395))

    elif tela == "jogo1":
        # Recursos
        nuvem_x = nuvem_x + deslocamento

        if nuvem_x > 600:
            deslocamento = -0.1
        elif nuvem_x < 50:
            deslocamento = 0.1

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

    elif tela == "jogo2":
            
        fonte_titulo_forca = pygame.font.SysFont("arial", 38, bold=True)
        fonte_palavra_forca = pygame.font.SysFont("arial", 28)
        fonte_texto_forca = pygame.font.SysFont("arial", 22)

        lista = ["banana", "laranja", "maca", "abacaxi", "kiwi"]
        palavra_aleatoria = choice(lista)
        palavra_oculta = "_ " * len(palavra_aleatoria)
        vida = 6
        entrada = ""
        mensagem_forca = "Digite uma letra ou a palavra inteira."
        fim = False

        while running and tela == "jogo2":
            for evento_forca in pygame.event.get():
                if evento_forca.type == pygame.QUIT:
                    running = False
                    break

                elif evento_forca.type == pygame.KEYDOWN:
                    if evento_forca.key == pygame.K_ESCAPE:
                        tela = "menu"
                        pygame.mixer.music.stop()
                        break

                    elif fim:
                        if evento_forca.key == pygame.K_s:
                            palavra_aleatoria = choice(lista)
                            palavra_oculta = "_ " * len(palavra_aleatoria)
                            vida = 6
                            entrada = ""
                            mensagem_forca = "Digite uma letra ou a palavra inteira."
                            fim = False

                        elif evento_forca.key == pygame.K_n:
                            tela = "menu"
                            break

                    elif evento_forca.key == pygame.K_BACKSPACE:
                        entrada = entrada[:-1]

                    elif evento_forca.key == pygame.K_RETURN:
                        tentativa = entrada.strip().lower()
                        entrada = ""

                        if not tentativa:
                            mensagem_forca = "Digite algo antes de confirmar."
                            continue

                        if not tentativa.isalpha():
                            mensagem_forca = "Entrada invalida! Digite apenas letras."
                            continue

                        if len(tentativa) == 1:
                            if tentativa in palavra_aleatoria:
                                for i in range(len(palavra_aleatoria)):
                                    if tentativa == palavra_aleatoria[i]:
                                        palavra_oculta = (
                                            palavra_oculta[:2 * i]
                                            + tentativa
                                            + palavra_oculta[2 * i + 1:]
                                        )
                                mensagem_forca = "Acertou a letra!"
                            else:
                                vida -= 1
                                mensagem_forca = f"Errou! Voce tem {vida} vidas restantes."

                        else:
                            if tentativa == palavra_aleatoria:
                                palavra_oculta = palavra_aleatoria
                            else:
                                vida -= 1
                                mensagem_forca = f"Errou a palavra! Restam {vida} vidas."

                        if palavra_oculta.replace(" ", "") == palavra_aleatoria:
                            mensagem_forca = "Parabens! Voce acertou a palavra!"
                            fim = True
                        elif vida == 0:
                            mensagem_forca = f"Voce perdeu! A palavra era: {palavra_aleatoria}."
                            fim = True

                    elif evento_forca.unicode.isalpha():
                        entrada += evento_forca.unicode.lower()

            if not running or tela != "jogo2":
                break

            screen.fill((245, 248, 252))

            titulo_forca = fonte_titulo_forca.render(
                "Jogo da Forca", True, (52, 120, 246)
            )
            screen.blit(titulo_forca, (400 - titulo_forca.get_width() // 2, 55))

            texto_palavra = fonte_palavra_forca.render(
                palavra_oculta, True, (30, 37, 46)
            )
            screen.blit(texto_palavra, (400 - texto_palavra.get_width() // 2, 155))

            texto_vidas = fonte_palavra_forca.render(
                f"Vidas: {vida}", True, (30, 37, 46)
            )
            screen.blit(texto_vidas, (60, 220))

            instrucao = fonte_texto_forca.render(
                "Digite uma letra ou a palavra inteira:", True, (30, 37, 46)
            )
            screen.blit(instrucao, (60, 275))

            caixa_forca = pygame.Rect(60, 310, 680, 54)
            pygame.draw.rect(screen, (230, 236, 245), caixa_forca, border_radius=8)
            pygame.draw.rect(
                screen, (52, 120, 246), caixa_forca, width=2, border_radius=8
            )

            screen.set_clip((74, 315, 652, 44))
            texto_entrada = fonte_palavra_forca.render(
                entrada, True, (30, 37, 46)
            )
            screen.blit(texto_entrada, (74, 320))
            screen.set_clip(None)

            cor_mensagem = (30, 37, 46)
            if "Errou" in mensagem_forca or "perdeu" in mensagem_forca:
                cor_mensagem = (192, 57, 43)
            elif "Parabens" in mensagem_forca:
                cor_mensagem = (39, 174, 96)

            texto_mensagem = fonte_texto_forca.render(
                mensagem_forca, True, cor_mensagem
            )
            screen.blit(texto_mensagem, (60, 395))

            ajuda = fonte_texto_forca.render(
                "Enter = confirmar | Backspace = apagar", True, (30, 37, 46)
            )
            screen.blit(ajuda, (60, 460))

            ajuda_menu = fonte_texto_forca.render(
                "Esc = voltar ao menu", True, (30, 37, 46)
            )
            screen.blit(ajuda_menu, (60, 490))

            if fim:
                texto_reinicio = fonte_texto_forca.render(
                    "S = jogar novamente | N = voltar ao menu",
                    True,
                    (52, 120, 246)
                )
                screen.blit(texto_reinicio, (60, 530))

            pygame.display.update()
            relogio.tick(60)

    elif tela == "jogo3":

        def pedra_papel_tesoura(jogador1, jogador2):
            if jogador1 == jogador2:
                return "Empate!"

            if jogador1 == "pedra" and jogador2 == "tesoura":
                return "Voce ganhou!"
            elif jogador1 == "papel" and jogador2 == "pedra":
                return "Voce ganhou!"
            elif jogador1 == "tesoura" and jogador2 == "papel":
                return "Voce ganhou!"
            else:
                return "O computador ganhou!"

        fonte_titulo_jokenpo = pygame.font.SysFont("arial", 38, bold=True)
        fonte_jokenpo = pygame.font.SysFont("arial", 28)
        fonte_ajuda_jokenpo = pygame.font.SysFont("arial", 22)

        opcoes = ["pedra", "papel", "tesoura"]
        soma_pontos_jogador1 = 0
        soma_pontos_jogador2 = 0
        jogador1 = ""
        jogador2 = ""
        resultado = "Escolha uma opcao para jogar!"

        botao_pedra = pygame.Rect(70, 220, 200, 70)
        botao_papel = pygame.Rect(300, 220, 200, 70)
        botao_tesoura = pygame.Rect(530, 220, 200, 70)

        while running and tela == "jogo3":
            for evento_jokenpo in pygame.event.get():
                if evento_jokenpo.type == pygame.QUIT:
                    running = False
                    break

                elif evento_jokenpo.type == pygame.KEYDOWN:
                    if evento_jokenpo.key == pygame.K_ESCAPE:
                        tela = "menu"
                        pygame.mixer.music.stop()
                        break

                elif evento_jokenpo.type == pygame.MOUSEBUTTONDOWN:
                    if evento_jokenpo.button == 1:
                        escolha = ""

                        if botao_pedra.collidepoint(evento_jokenpo.pos):
                            escolha = "pedra"
                        elif botao_papel.collidepoint(evento_jokenpo.pos):
                            escolha = "papel"
                        elif botao_tesoura.collidepoint(evento_jokenpo.pos):
                            escolha = "tesoura"

                        if escolha != "":
                            jogador1 = escolha
                            jogador2 = choice(opcoes)
                            resultado = pedra_papel_tesoura(jogador1, jogador2)

                            if resultado == "Voce ganhou!":
                                soma_pontos_jogador1 += 1
                            elif resultado == "O computador ganhou!":
                                soma_pontos_jogador2 += 1

            if not running or tela != "jogo3":
                break

            screen.fill((245, 248, 252))

            titulo_jokenpo = fonte_titulo_jokenpo.render(
                "Pedra, Papel e Tesoura", True, (52, 120, 246)
            )
            screen.blit(
                titulo_jokenpo,
                (400 - titulo_jokenpo.get_width() // 2, 55)
            )

            texto_placar = fonte_jokenpo.render(
                f"Placar: Voce {soma_pontos_jogador1} x "
                f"{soma_pontos_jogador2} Computador",
                True,
                (30, 37, 46)
            )
            screen.blit(texto_placar, (400 - texto_placar.get_width() // 2, 135))

            pygame.draw.rect(
                screen, (52, 120, 246), botao_pedra, border_radius=8
            )
            pygame.draw.rect(
                screen, (52, 120, 246), botao_papel, border_radius=8
            )
            pygame.draw.rect(
                screen, (52, 120, 246), botao_tesoura, border_radius=8
            )

            texto_pedra = fonte_jokenpo.render("Pedra", True, "white")
            texto_papel = fonte_jokenpo.render("Papel", True, "white")
            texto_tesoura = fonte_jokenpo.render("Tesoura", True, "white")

            screen.blit(texto_pedra, texto_pedra.get_rect(center=botao_pedra.center))
            screen.blit(texto_papel, texto_papel.get_rect(center=botao_papel.center))
            screen.blit(
                texto_tesoura, texto_tesoura.get_rect(center=botao_tesoura.center)
            )

            if jogador1 != "":
                texto_jogador = fonte_jokenpo.render(
                    f"Voce escolheu: {jogador1}", True, (30, 37, 46)
                )
                texto_computador = fonte_jokenpo.render(
                    f"O computador escolheu: {jogador2}", True, (30, 37, 46)
                )
                screen.blit(texto_jogador, (70, 330))
                screen.blit(texto_computador, (70, 375))

            cor_resultado = (30, 37, 46)
            if resultado == "Voce ganhou!":
                cor_resultado = (39, 174, 96)
            elif resultado == "O computador ganhou!":
                cor_resultado = (192, 57, 43)

            texto_resultado = fonte_jokenpo.render(
                resultado, True, cor_resultado
            )
            screen.blit(
                texto_resultado,
                (400 - texto_resultado.get_width() // 2, 445)
            )

            texto_ajuda = fonte_ajuda_jokenpo.render(
                "Clique em uma opcao para jogar novamente.",
                True,
                (30, 37, 46)
            )
            screen.blit(texto_ajuda, (70, 515))

            texto_voltar = fonte_ajuda_jokenpo.render(
                "Esc = voltar ao menu", True, (30, 37, 46)
            )
            screen.blit(texto_voltar, (70, 550))

            pygame.display.update()
            relogio.tick(60)

    texto_esc = fonte_validation.render(
    "Pressione ESC para voltar ao menu", True, "black"
    )
    screen.blit(texto_esc, (10, 10))
    
    
    pygame.display.update()
    relogio.tick(60)

pygame.quit()