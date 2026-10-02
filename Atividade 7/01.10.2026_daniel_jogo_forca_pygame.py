import pygame
from random import choice

pygame.init()
screen = pygame.display.set_mode((900, 650))
pygame.display.set_caption("Jogo da Forca")
relogio = pygame.time.Clock()

# Cores e fontes (não precisa baixar nenhuma fonte).
FUNDO = "#111827"
CARTAO = "#1F2937"
BRANCO = "#F3F4F6"
CINZA = "#A8B3C7"
LILAS = "#C4B5FD"
VERDE = "#6EE7B7"
ROSA = "#FDA4AF"

fonte_titulo = pygame.font.Font(None, 62)
fonte_palavra = pygame.font.Font(None, 52)
fonte_normal = pygame.font.Font(None, 30)
fonte_pequena = pygame.font.Font(None, 24)


def escrever(texto, fonte, cor, x, y):
    imagem = fonte.render(texto, True, cor)
    screen.blit(imagem, (x, y))


def substitui_palavra_oculta(palavra, palavra_oculta, letra):
    for i in range(len(palavra)):
        if letra == palavra[i]:
            palavra_oculta = (
                palavra_oculta[:2*i] + letra + palavra_oculta[2*i+1:]
            )
    return palavra_oculta


def desenhar_forca(vida):
    pygame.draw.line(screen, CINZA, (95, 390), (275, 390), 6)
    pygame.draw.line(screen, CINZA, (135, 390), (135, 190), 6)
    pygame.draw.line(screen, CINZA, (135, 190), (235, 190), 6)
    pygame.draw.line(screen, CINZA, (235, 190), (235, 220), 6)

    erros = 6 - vida
    if erros >= 1:
        pygame.draw.circle(screen, LILAS, (235, 245), 25, 4)
    if erros >= 2:
        pygame.draw.line(screen, LILAS, (235, 270), (235, 325), 4)
    if erros >= 3:
        pygame.draw.line(screen, LILAS, (235, 280), (205, 305), 4)
    if erros >= 4:
        pygame.draw.line(screen, LILAS, (235, 280), (265, 305), 4)
    if erros >= 5:
        pygame.draw.line(screen, LILAS, (235, 325), (210, 365), 4)
    if erros >= 6:
        pygame.draw.line(screen, LILAS, (235, 325), (260, 365), 4)


lista = ["banana", "laranja", "maca", "abacaxi", "kiwi"]
rodando = True

while rodando:
    # Começa uma nova partida.
    palavra_aleatoria = choice(lista)
    palavra_oculta = "_ " * len(palavra_aleatoria)
    vida = 6
    entrada = ""
    tentativas = []
    mensagem = "Boa sorte! Vamos descobrir a fruta?"
    cor_mensagem = CINZA
    terminou = False
    reiniciar = False

    while rodando and not reiniciar:
        # Lê o teclado sem travar a janela com input().
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    rodando = False

                elif terminou:
                    if evento.key == pygame.K_RETURN:
                        reiniciar = True

                elif evento.key == pygame.K_BACKSPACE:
                    entrada = entrada[:-1]

                elif evento.key == pygame.K_RETURN:
                    if entrada == "":
                        mensagem = "Digite uma letra ou uma palavra primeiro."
                        cor_mensagem = ROSA
                        continue

                    if entrada in tentativas:
                        mensagem = "Você já tentou isso! Escolha outra opção."
                        cor_mensagem = ROSA
                    else:
                        tentativas.append(entrada)

                        if entrada == palavra_aleatoria:
                            palavra_oculta = palavra_aleatoria
                        elif len(entrada) == 1 and entrada in palavra_aleatoria:
                            palavra_oculta = substitui_palavra_oculta(
                                palavra_aleatoria, palavra_oculta, entrada
                            )
                            mensagem = "Boa! Essa letra aparece na palavra."
                            cor_mensagem = VERDE
                        else:
                            vida -= 1
                            mensagem = "Não foi dessa vez. Tente novamente!"
                            cor_mensagem = ROSA

                    entrada = ""

                    if palavra_oculta.replace(" ", "") == palavra_aleatoria:
                        terminou = True
                        mensagem = "Parabéns! Você acertou a palavra!"
                        cor_mensagem = VERDE
                    elif vida == 0:
                        terminou = True
                        mensagem = "Fim de jogo! A palavra era: " + palavra_aleatoria
                        cor_mensagem = ROSA

                elif evento.unicode.isalpha() and len(entrada) < 15:
                    entrada += evento.unicode.lower()

        # Desenha a tela novamente a cada quadro.
        screen.fill(FUNDO)
        escrever("Jogo da Forca", fonte_titulo, LILAS, 50, 35)
        escrever("Uma letra de cada vez. Você tem 6 chances!",
                 fonte_normal, CINZA, 52, 98)

        pygame.draw.rect(screen, CARTAO, (50, 150, 280, 280), border_radius=20)
        pygame.draw.rect(screen, CARTAO, (350, 150, 500, 280), border_radius=20)
        desenhar_forca(vida)

        escrever("DICA: FRUTAS", fonte_pequena, VERDE, 380, 177)
        escrever("Vidas: " + str(vida) + " / 6", fonte_normal,
                 VERDE if vida > 2 else ROSA, 705, 174)
        escrever(palavra_oculta, fonte_palavra, BRANCO, 380, 237)
        escrever("Digite uma letra ou a palavra (sem acentos):",
                 fonte_pequena, CINZA, 380, 302)

        pygame.draw.rect(screen, FUNDO, (375, 337, 450, 65), border_radius=12)
        pygame.draw.rect(screen, LILAS, (375, 337, 450, 65), 2, border_radius=12)
        escrever(entrada + ("_" if not terminou else ""),
                 fonte_normal, BRANCO, 395, 358)

        escrever(mensagem, fonte_normal, cor_mensagem, 55, 455)
        escrever("Últimas tentativas:", fonte_pequena, CINZA, 55, 505)
        ultimas = "  |  ".join(tentativas[-3:])
        escrever(ultimas, fonte_pequena, LILAS, 55, 535)

        if terminou:
            escrever("ENTER para jogar novamente  •  ESC para sair",
                     fonte_normal, VERDE, 55, 590)
        else:
            escrever("ENTER confirma  •  BACKSPACE apaga  •  ESC sai",
                     fonte_pequena, CINZA, 55, 590)

        pygame.display.flip()
        relogio.tick(60)

pygame.quit()
