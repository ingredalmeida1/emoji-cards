import arcade
import os

LARGURA_TELA = 1000
ALTURA_TELA = 600
TITULO = "EmojiCards"
AZUL = arcade.color_from_hex_string("#2C346B")
AMARELO = arcade.color_from_hex_string("#F6BA2C")

arcade.load_font(os.path.join(os.path.dirname(__file__), 'fontes', 'Poppins.ttf'))
POPPINS = "Poppins"

arcade.load_font( os.path.join(os.path.dirname(__file__), 'fontes', 'Agrandir.otf'))
AGRANDIR = "Agrandir"

# AGRANDIR_BOLD = os.path.join(os.path.dirname(__file__), 'fontes', 'AgrandirBold.ttf')
arcade.load_font(os.path.join(os.path.dirname(__file__), 'fontes', 'AgrandirBold.ttf'))
AGRANDIR_BOLD = "AgrandirBold"