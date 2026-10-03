from random import choice
import pygame


pygame.init()
screen = pygame.display.set_mode((920, 540))
pygame.display.set_caption("Jogo da Forca - Pygame")
clock = pygame.time.Clock()

font_title = pygame.font.SysFont("arial", 38, bold=True)
font_main = pygame.font.SysFont("arial", 28)
font_small = pygame.font.SysFont("arial", 22)


def substitui_palavra_oculta(palavra_aleatoria, palavra_oculta, letra, vida):
    if letra in palavra_aleatoria:
        for i in range(len(palavra_aleatoria)):
            if letra == palavra_aleatoria[i]:
                # substituir o "_ " na palavra oculta pela letra
                palavra_oculta = palavra_oculta[: 2 * i] + letra + palavra_oculta[2 * i + 1 :]
        mensagem = f"{palavra_oculta}"
    else:
        mensagem = "Errou"
        vida = vida - 1
        mensagem = f"{mensagem}! Voce tem {vida} vidas restantes."

    return palavra_oculta, vida, mensagem


def validar_letra(letra):
    while not letra.isalpha():
        return False, "Entrada invalida! Digite apenas letras, sem numeros ou especiais."
    return True, ""


def desenhar_tela(palavra_oculta, vida, entrada, mensagem, fim, reiniciar):
    screen.fill((245, 248, 252))

    titulo = font_title.render("Jogo da Forca", True, (52, 120, 246))
    screen.blit(titulo, (920 // 2 - titulo.get_width() // 2, 28))

    palavra_texto = font_main.render(palavra_oculta, True, (30, 37, 46))
    screen.blit(palavra_texto, (920 // 2 - palavra_texto.get_width() // 2, 140))

    vidas_texto = font_main.render(f"Vidas: {vida}", True, (30, 37, 46))
    screen.blit(vidas_texto, (60, 210))

    instrucao = font_small.render("Digite uma letra ou a palavra inteira:", True, (30, 37, 46))
    screen.blit(instrucao, (60, 260))

    caixa = pygame.Rect(60, 292, 920 - 120, 54)
    pygame.draw.rect(screen, (230, 236, 245), caixa, border_radius=8)
    pygame.draw.rect(screen, (52, 120, 246), caixa, width=2, border_radius=8)

    entrada_texto = font_main.render(entrada, True, (30, 37, 46))
    screen.blit(entrada_texto, (74, 302))

    cor_msg = (30, 37, 46)
    if "Errou" in mensagem or "perdeu" in mensagem:
        cor_msg = (192, 57, 43)
    if "Parabens" in mensagem:
        cor_msg = (39, 174, 96)

    mensagem_texto = font_small.render(mensagem, True, cor_msg)
    screen.blit(mensagem_texto, (60, 370))

    ajuda1 = font_small.render("Enter = confirmar tentativa", True, (30, 37, 46))
    ajuda2 = font_small.render("Backspace = apagar | Esc = sair", True, (30, 37, 46))
    screen.blit(ajuda1, (60, 435))
    screen.blit(ajuda2, (60, 463))

    if fim:
        if reiniciar == "sim":
            rodada = "Pressione S para jogar novamente ou N para sair."
        else:
            rodada = "Pressione N para sair."
        rodada_texto = font_small.render(rodada, True, (52, 120, 246))
        screen.blit(rodada_texto, (60, 491))

    pygame.display.flip()


def main():
    reiniciar = "sim"
    rodando = True

    while rodando and reiniciar == "sim":
        # 1 passo: gerar aleatoriamente a palavra
        lista = ["banana", "laranja", "maca", "abacaxi", "kiwi"]
        palavra_aleatoria = choice(lista)

        palavra_oculta = "_ " * len(palavra_aleatoria)

        vida = 6
        palavra_auxiliar = palavra_oculta
        mensagem = "Digite uma letra ou a palavra inteira e pressione Enter."
        entrada = ""
        fim = False

        while rodando and palavra_auxiliar != palavra_aleatoria and vida > 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    rodando = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        rodando = False

                    elif event.key == pygame.K_BACKSPACE:
                        entrada = entrada[:-1]

                    elif event.key == pygame.K_RETURN:
                        letra = entrada.strip().lower()

                        if not letra:
                            mensagem = "Digite algo antes de confirmar."
                            entrada = ""
                            continue

                        letra_valida, mensagem_validacao = validar_letra(letra)
                        if not letra_valida:
                            mensagem = mensagem_validacao
                            entrada = ""
                            continue

                        if len(letra) == 1:
                            palavra_oculta, vida, mensagem = substitui_palavra_oculta(
                                palavra_aleatoria, palavra_oculta, letra, vida
                            )
                        else:
                            if letra == palavra_aleatoria:
                                # quando o jogador acerta a palavra inteira
                                palavra_oculta = palavra_aleatoria
                                palavra_auxiliar = palavra_aleatoria
                                mensagem = "Parabens! Palavra inteira correta."
                            else:
                                mensagem = "Voce errou a palavra!"
                                vida = vida - 1
                                mensagem = f"{mensagem} Voce tem {vida} vidas restantes."

                        palavra_auxiliar = palavra_oculta.replace(" ", "")
                        entrada = ""

                    else:
                        if event.unicode.isalpha():
                            entrada += event.unicode.lower()

            desenhar_tela(palavra_oculta, vida, entrada, mensagem, fim, reiniciar)
            clock.tick(60)

        if not rodando:
            break

        if vida == 0:
            mensagem = "Forca! Voce perdeu!"
        else:
            mensagem = "Parabens! Voce acertou a palavra!"

        fim = True

        aguardando_reinicio = True
        while rodando and aguardando_reinicio:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    rodando = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        rodando = False
                    elif event.key == pygame.K_s:
                        reiniciar = "sim"
                        aguardando_reinicio = False
                    elif event.key == pygame.K_n:
                        reiniciar = "nao"
                        aguardando_reinicio = False

            desenhar_tela(palavra_oculta, vida, entrada, mensagem, fim, reiniciar)
            clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
