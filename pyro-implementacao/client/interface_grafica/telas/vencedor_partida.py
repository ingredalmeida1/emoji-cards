import arcade
import arcade.gui # submódulo gui do arcade, que fornece componentes para criar interfaces gráficas.

from ..resources.constantes import LARGURA_TELA, ALTURA_TELA, AZUL, AMARELO, POPPINS, AGRANDIR

class VencedorPartida(arcade.View):
    def __init__(self, cliente, vencedor,carta_adicionada, pontuacao, criar_partida_view, back_to_login):
        super().__init__()

        arcade.set_background_color(AZUL)
        
        self.cliente = cliente
        self.vencedor = vencedor
        self.carta_adicionada = carta_adicionada
        self.pontuacao = pontuacao
        
        self.username_usuario = self.cliente.get_username()
        
        #reiniciar contador turnos
        self.cliente.count_turnos = 0
         
        self.criar_partida_view = criar_partida_view
        self.back_to_login = back_to_login

        self.centro = None

        self.fundo_vencedor = arcade.load_texture("interface_grafica/resources/widgets/campo.png")

        self.botoes = []

        self.b_sair = arcade.load_texture("interface_grafica/resources/widgets/botoes/b-excluir.png")
        self.botoes.append({
            'texture': self.b_sair,
            'x': LARGURA_TELA - 100,
            'y': 100,
            'width': 40,
            'height': 40,
            'action': self.mudar_tela
        })

    def setup(self):
        if self.vencedor != "empate":
            self.centro = arcade.load_texture(f"interface_grafica/resources/cartas/{self.carta_adicionada}.png")
    
    def on_show(self):
        self.setup()     

    def on_draw(self):
        arcade.start_render()
        
        if self.vencedor != "empate":
            if self.vencedor == self.username_usuario:
                arcade.draw_text(f"Parabéns!", LARGURA_TELA//2, ALTURA_TELA//2 + 200, AMARELO, 
                                font_size=30, font_name=AGRANDIR, anchor_x="center")
                
                arcade.draw_text("você venceu a partida e ganhou uma nova carta:", LARGURA_TELA//2, ALTURA_TELA//2 + 90, arcade.color.WHITE, 
                                font_size=15, font_name=POPPINS, anchor_x="center")
            
            else:
                arcade.draw_text(self.username_usuario, LARGURA_TELA//2, ALTURA_TELA//2 + 250, arcade.color.WHITE, 
                                font_size=15, font_name=POPPINS, anchor_x="center")
                
                arcade.draw_text(f"a partida foi vencida por:", LARGURA_TELA//2, ALTURA_TELA//2 + 200, AMARELO, 
                                font_size=20, font_name=AGRANDIR, anchor_x="center")
                
                arcade.draw_text("e por isso el@ ganhou uma nova carta:", LARGURA_TELA//2, ALTURA_TELA//2 + 90, arcade.color.WHITE, 
                                font_size=15, font_name=POPPINS, anchor_x="center")
                
        else:
            arcade.draw_text("Empatou!", LARGURA_TELA//2, ALTURA_TELA//2 + 200, AMARELO, 
                            font_size=30, font_name=AGRANDIR, anchor_x="center")
    

        if self.fundo_vencedor and self.vencedor:
            if self.vencedor != 'empate':
                arcade.draw_texture_rectangle(LARGURA_TELA//2, ALTURA_TELA // 2 - 50, 180, 250, self.centro)

                arcade.draw_texture_rectangle(LARGURA_TELA//2, ALTURA_TELA// 2 + 150, 350, 60, self.fundo_vencedor)
                arcade.draw_text(self.vencedor, LARGURA_TELA//2, ALTURA_TELA// 2 + 143, arcade.color.WHITE, 
                            font_size=15, font_name=POPPINS, anchor_x="center")
        
        for botao in self.botoes:
            if 'texture' in botao:
                arcade.draw_texture_rectangle(botao['x'], botao['y'], botao['width'], botao['height'], botao['texture'])
            
    def on_mouse_press(self, x, y, button, modifiers):
        for botao in self.botoes:
            if 'texture' in botao:
                if (botao['x'] - botao['width'] / 2 < x < botao['x'] + botao['width'] / 2 and
                        botao['y'] - botao['height'] / 2 < y < botao['y'] + botao['height'] / 2):
                    botao['action']()
                    break

    def mudar_tela(self):
        self.window.show_view(self.criar_partida_view(self.cliente, self.back_to_login))