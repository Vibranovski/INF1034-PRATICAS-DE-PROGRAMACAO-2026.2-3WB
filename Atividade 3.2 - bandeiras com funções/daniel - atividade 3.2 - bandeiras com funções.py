# Bom dia, professor, decidi fazer o código de 20 BANDEIRAS FÁCEIS

# 10 BANDEIRAS COM LISTRAS NA VERTICAL

# 1 - FRANÇA
# 2 - ITÁLIA
# 3 - BÉLGICA
# 4 - IRLANDA
# 5 - PERU
# 6 - ROMÊNIA
# 7 - MALI
# 8 - GUINÉ
# 9 - NIGÉRIA
# 10 - COSTA DO MARFIM


# 10 BANDEIRAS COM LISTRAS NA HORIZONTAL

# 11 - ALEMANHA
# 12 - RÚSSIA
# 13 - ÁUSTRIA
# 14 - ARMÊNIA
# 15 - HUNGRIA
# 16 - BULGÁRIA
# 17 - HOLANDA
# 18 - ESTÔNIA
# 19 - LITUÂNIA
# 20 - IÉMEN

from turtle import *
from time import sleep

screen = Screen()
screen.setup(width=1000, height=500)

t = Turtle()
t.shape("turtle")
t.speed(0)


# ============================================================
# 10 BANDEIRAS COM FAIXAS VERTICAIS
# Organização: 5 colunas x 2 linhas
# Cada bandeira: 180 x 120
# ============================================================

def desenha_retangulo_vertical(x, y, larg, alt, color):
    
    t.pu()
    t.goto(x, y)
    t.pd()
    
    t.color("black")
    t.begin_fill()
    t.fillcolor(color)
    for _ in range(2):
        t.fd(larg)
        t.rt(90)
        t.fd(alt)
        t.rt(90)
    t.end_fill()

# --- BANDEIRA 1: FRANÇA ---

def desenha_bandeira_franca():
    desenha_retangulo_vertical(-470, 50, 60, 120, "#071F98")
    desenha_retangulo_vertical(-410, 50, 60, 120, "#FFFFFF")
    desenha_retangulo_vertical(-350, 50, 60, 120, "#E62E32")

# --- BANDEIRA 2: ITÁLIA ---

def desenha_bandeira_italia():
    desenha_retangulo_vertical(-280, 50, 60, 120, "#008D45")
    desenha_retangulo_vertical(-220, 50, 60, 120, "#FFFFFF")
    desenha_retangulo_vertical(-160, 50, 60, 120, "#D3222B")

# --- BANDEIRA 3: BÉLGICA ---

def desenha_bandeira_belgica():
    desenha_retangulo_vertical(-90, 50, 60, 120, "#000000")
    desenha_retangulo_vertical(-30, 50, 60, 120, "#FDDA25")
    desenha_retangulo_vertical(30, 50, 60, 120, "#EF3340")

# --- BANDEIRA 4: IRLANDA ---

def desenha_bandeira_irlanda():
    desenha_retangulo_vertical(100, 50, 60, 120, "#179B62")
    desenha_retangulo_vertical(160, 50, 60, 120, "#FFFFFF")
    desenha_retangulo_vertical(220, 50, 60, 120, "#FF883D")

# --- BANDEIRA 5: PERU ---

def desenha_bandeira_peru():
    desenha_retangulo_vertical(290, 50, 60, 120, "#D90F23")
    desenha_retangulo_vertical(350, 50, 60, 120, "#FFFFFF")
    desenha_retangulo_vertical(410, 50, 60, 120, "#D90F23")


# ============================================================
# SEGUNDA LINHA
# ============================================================


# --- BANDEIRA 6: ROMÊNIA ---

def desenha_bandeira_romenia():
    desenha_retangulo_vertical(-470, -80, 60, 120, "#002B80")
    desenha_retangulo_vertical(-410, -80, 60, 120, "#FCD215")
    desenha_retangulo_vertical(-350, -80, 60, 120, "#CE1126")

# --- BANDEIRA 7: MALI ---

def desenha_bandeira_mali():
    desenha_retangulo_vertical(-280, -80, 60, 120, "#15B53A")
    desenha_retangulo_vertical(-220, -80, 60, 120, "#FCD116")
    desenha_retangulo_vertical(-160, -80, 60, 120, "#CE1126")

# --- BANDEIRA 8: GUINÉ ---

def desenha_bandeira_guine():
    desenha_retangulo_vertical(-90, -80, 60, 120, "#CE1126")
    desenha_retangulo_vertical(-30, -80, 60, 120, "#FCD215")
    desenha_retangulo_vertical(30, -80, 60, 120, "#009460")

# --- BANDEIRA 9: NIGÉRIA ---

def desenha_bandeira_nigeria():
    desenha_retangulo_vertical(100, -80, 60, 120, "#008751")
    desenha_retangulo_vertical(160, -80, 60, 120, "#FFFFFF")
    desenha_retangulo_vertical(220, -80, 60, 120, "#008751")

# --- BANDEIRA 10: COSTA DO MARFIM ---

def desenha_bandeira_costa_do_marfim():
    desenha_retangulo_vertical(290, -80, 60, 120, "#FF8201")
    desenha_retangulo_vertical(350, -80, 60, 120, "#FFFFFF")
    desenha_retangulo_vertical(410, -80, 60, 120, "#019A44")


# ============================================================
# 10 BANDEIRAS COM FAIXAS HORIZONTAIS
# Organização: 5 colunas x 2 linhas
# Cada bandeira: 180 x 120
# ============================================================

def desenha_retangulo_horizontal(x, y, larg, alt, color):
    
    t.pu()
    t.goto(x, y)
    t.pd()
    
    t.color("black")
    t.begin_fill()
    t.fillcolor(color)
    for _ in range(2):
        t.fd(larg)
        t.rt(90)
        t.fd(alt)
        t.rt(90)
    t.end_fill()

# --- BANDEIRA 11: ALEMANHA ---

def desenha_bandeira_alemanha():
    desenha_retangulo_horizontal(-470, 170, 180, 40, "#000000")
    desenha_retangulo_horizontal(-470, 130, 180, 40, "#DD0000")
    desenha_retangulo_horizontal(-470, 90, 180, 40, "#FFCE01")

# --- BANDEIRA 12: RÚSSIA ---

def desenha_bandeira_russia():
    desenha_retangulo_horizontal(-280, 170, 180, 40, "#FFFFFF")
    desenha_retangulo_horizontal(-280, 130, 180, 40, "#0039A6")
    desenha_retangulo_horizontal(-280, 90, 180, 40, "#D52B1E")

# --- BANDEIRA 13: ÁUSTRIA ---

def desenha_bandeira_austria():
    desenha_retangulo_horizontal(-90, 170, 180, 40, "#C8112E")
    desenha_retangulo_horizontal(-90, 130, 180, 40, "#FFFFFF")
    desenha_retangulo_horizontal(-90, 90, 180, 40, "#C8112E")

# --- BANDEIRA 14: ARMÊNIA ---

def desenha_bandeira_armenia():
    desenha_retangulo_horizontal(100, 170, 180, 40, "#D90113")
    desenha_retangulo_horizontal(100, 130, 180, 40, "#0033A0")
    desenha_retangulo_horizontal(100, 90, 180, 40, "#F2A800")

# --- BANDEIRA 15: HUNGRIA ---

def desenha_bandeira_hungria():
    desenha_retangulo_horizontal(290, 170, 180, 40, "#CE2939")
    desenha_retangulo_horizontal(290, 130, 180, 40, "#FFFFFF")
    desenha_retangulo_horizontal(290, 90, 180, 40, "#477050")


# ============================================================
# SEGUNDA LINHA
# ============================================================


# --- BANDEIRA 16: BULGÁRIA ---

def desenha_bandeira_bulgaria():
    desenha_retangulo_horizontal(-470, 30, 180, 40, "#FFFFFF")
    desenha_retangulo_horizontal(-470, -10, 180, 40, "#00966E")
    desenha_retangulo_horizontal(-470, -50, 180, 40, "#D62612")

# --- BANDEIRA 17: HOLANDA ---

def desenha_bandeira_holanda():
    desenha_retangulo_horizontal(-280, 30, 180, 40, "#AE1C28")
    desenha_retangulo_horizontal(-280, -10, 180, 40, "#FFFFFF")
    desenha_retangulo_horizontal(-280, -50, 180, 40, "#21468B")

# --- BANDEIRA 18: ESTÔNIA ---

def desenha_bandeira_estonia():
    desenha_retangulo_horizontal(-90, 30, 180, 40, "#0072CE")
    desenha_retangulo_horizontal(-90, -10, 180, 40, "#000000")
    desenha_retangulo_horizontal(-90, -50, 180, 40, "#FFFFFF")

# --- BANDEIRA 19: LITUÂNIA ---

def desenha_bandeira_lituania():
    desenha_retangulo_horizontal(100, 30, 180, 40, "#FDB913")
    desenha_retangulo_horizontal(100, -10, 180, 40, "#006A44")
    desenha_retangulo_horizontal(100, -50, 180, 40, "#C1272D")

# --- BANDEIRA 20: IÉMEN ---

def desenha_bandeira_iemen():
    desenha_retangulo_horizontal(290, 30, 180, 40, "#CE1126")
    desenha_retangulo_horizontal(290, -10, 180, 40, "#FFFFFF")
    desenha_retangulo_horizontal(290, -50, 180, 40, "#000000")

def aciona_todas_as_bandeiras():
    desenha_bandeira_franca()
    desenha_bandeira_italia()
    desenha_bandeira_belgica()
    desenha_bandeira_irlanda()
    desenha_bandeira_peru()
    desenha_bandeira_romenia()
    desenha_bandeira_mali()
    desenha_bandeira_guine()
    desenha_bandeira_nigeria()
    desenha_bandeira_costa_do_marfim()
    
    # As 10 bandeiras permanecem juntas por 5 segundos
    sleep(5)

    # Apaga todas de uma vez
    t.clear()

    desenha_bandeira_alemanha()
    desenha_bandeira_russia()
    desenha_bandeira_austria()
    desenha_bandeira_armenia()
    desenha_bandeira_hungria()
    desenha_bandeira_bulgaria()
    desenha_bandeira_holanda()
    desenha_bandeira_estonia()
    desenha_bandeira_lituania()
    desenha_bandeira_iemen()

    # As 10 bandeiras permanecem juntas por 5 segundos
    sleep(5)

    # Apaga todas de uma vez
    t.clear()

aciona_todas_as_bandeiras()

# Escolher a bandeira que vai ser desenhada pelo textinput.
bandeira_escolhida = textinput("escolha_bandeira", "Digite o nome da bandeira que deseja desenhar (ex: França, Itália, Bélgica, Irlanda, Peru, Romênia, Mali, Guiné, Nigéria, Costa do Marfim, Alemanha, Rússia, Áustria, Armênia, Hungria, Bulgária, Holanda, Estônia, Lituânia, Iémen): ")

# Desenhar a bandeira escolhida
if bandeira_escolhida == "França":
    desenha_bandeira_franca()
elif bandeira_escolhida == "Itália":
    desenha_bandeira_italia()
elif bandeira_escolhida == "Bélgica":
    desenha_bandeira_belgica()
elif bandeira_escolhida == "Irlanda":
    desenha_bandeira_irlanda()
elif bandeira_escolhida == "Peru":
    desenha_bandeira_peru()
elif bandeira_escolhida == "Romênia":
    desenha_bandeira_romenia()
elif bandeira_escolhida == "Mali":
    desenha_bandeira_mali()
elif bandeira_escolhida == "Guiné":
    desenha_bandeira_guine()
elif bandeira_escolhida == "Nigéria":
    desenha_bandeira_nigeria()
elif bandeira_escolhida == "Costa do Marfim":
    desenha_bandeira_costa_do_marfim()
elif bandeira_escolhida == "Alemanha":
    desenha_bandeira_alemanha()
elif bandeira_escolhida == "Rússia":
    desenha_bandeira_russia()
elif bandeira_escolhida == "Áustria":
    desenha_bandeira_austria()
elif bandeira_escolhida == "Armênia":
    desenha_bandeira_armenia()
elif bandeira_escolhida == "Hungria":
    desenha_bandeira_hungria()
elif bandeira_escolhida == "Bulgária":
    desenha_bandeira_bulgaria()
elif bandeira_escolhida == "Holanda":
    desenha_bandeira_holanda()
elif bandeira_escolhida == "Estônia":
    desenha_bandeira_estonia()
elif bandeira_escolhida == "Lituânia":
    desenha_bandeira_lituania()
elif bandeira_escolhida == "Iémen":
    desenha_bandeira_iemen()

mainloop()