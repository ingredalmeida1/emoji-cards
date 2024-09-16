import arcade
import arcade.gui # submódulo gui do arcade, que fornece componentes para criar interfaces gráficas.

from ..resources.constantes import LARGURA_TELA, ALTURA_TELA, AZUL, AMARELO, POPPINS, AGRANDIR

import threading
from ..telas.montar_baralho import MontarBaralho

class Perfil(arcade.View):
    def __init__(self, cliente, info_perfil, login_view, criar_partida_view):
        super().__init__()
        
        self.back_to_login = login_view
        self.criar_partida = criar_partida_view
               
        #atributos comunicacao:
        self.cliente = cliente
        self.mensagem = None
        
        '''
        info_perfil = {
                'colecao_cartas': colecao_cartas,
                'baralhos': baralhos,
                'qtd_baralhos': qtd_baralhos
        }
        '''
        self.info_perfil = info_perfil
        self.colecao = info_perfil['colecao_cartas']
        self.qtd_baralhos = info_perfil['qtd_baralhos']
        self.baralhos = info_perfil['baralhos']

        self.gerencia_entrada = arcade.gui.UIManager()

        arcade.set_background_color(AZUL)

        # Carrossel da Coleção
        self.indice_inicial = 0
        self.cartas = []
        self.botoes = []

        for emocao in self.colecao:
            self.cartas.append(arcade.load_texture(f"interface_grafica/resources/cartas/{emocao}.png"))

        self.seta_esquerda = arcade.load_texture("interface_grafica/resources/widgets/seta-esquerda.png")
        self.seta_direita = arcade.load_texture("interface_grafica/resources/widgets/seta-direita.png")
        self.fundo_colecao = arcade.load_texture("interface_grafica/resources/widgets/colecao.png")
            
        # Carrossel do Baralhos
        self.indice_inicial_b1 = 0
        self.baralho_1 = []

        self.indice_inicial_b2 = 0
        self.baralho_2 = []
        
        self.indice_inicial_b3 = 0
        self.baralho_3 = []
        
        # Carrossel do Baralho 1
        if self.qtd_baralhos >= 1:
            for emocao in self.baralhos[0]:
                self.baralho_1.append(arcade.load_texture(f"interface_grafica/resources/cartas/{emocao}.png"))
        
        # Carrossel do Baralho 2
        if self.qtd_baralhos >= 2:
            for emocao in self.baralhos[1]:
                self.baralho_2.append(arcade.load_texture(f"interface_grafica/resources/cartas/{emocao}.png"))

        # Carrossel do Baralho 3
        if self.qtd_baralhos == 3:
            for emocao in self.baralhos[2]:
                self.baralho_3.append(arcade.load_texture(f"interface_grafica/resources/cartas/{emocao}.png"))

        # Se existe os baralhos eles são apresentados, se só existem 2 o botão montar é apresentado
        if self.baralho_1:
            self.seta_esquerda_b1 = arcade.load_texture("interface_grafica/resources/widgets/seta-esquerda.png")
            self.seta_direita_b1 = arcade.load_texture("interface_grafica/resources/widgets/seta-direita.png")
            self.fundo_b1 = arcade.load_texture("interface_grafica/resources/widgets/baralhos.png")
            self.b_excluir_b1 = arcade.load_texture("interface_grafica/resources/widgets/botoes/b-excluir.png")

            self.botoes.append({
                'texture': self.b_excluir_b1,
                'x': 320,
                'y': 260,
                'width': 38,
                'height': 38,
                'action': lambda: self.excluir_baralho(0)
            })

        if self.baralho_2:
            self.seta_esquerda_b2 = arcade.load_texture("interface_grafica/resources/widgets/seta-esquerda.png")
            self.seta_direita_b2 = arcade.load_texture("interface_grafica/resources/widgets/seta-direita.png")
            self.fundo_b2 = arcade.load_texture("interface_grafica/resources/widgets/baralhos.png")
            self.b_excluir_b2 = arcade.load_texture("interface_grafica/resources/widgets/botoes/b-excluir.png")

            self.botoes.append({
                'texture': self.b_excluir_b2,
                'x': 640,
                'y': 260,
                'width': 38,
                'height': 38,
                'action': lambda: self.excluir_baralho(1)
            })

        if self.baralho_3:
            self.seta_esquerda_b3 = arcade.load_texture("interface_grafica/resources/widgets/seta-esquerda.png")
            self.seta_direita_b3 = arcade.load_texture("interface_grafica/resources/widgets/seta-direita.png")
            self.fundo_b3 = arcade.load_texture("interface_grafica/resources/widgets/baralhos.png")
            self.b_excluir_b3 = arcade.load_texture("interface_grafica/resources/widgets/botoes/b-excluir.png")

            self.botoes.append({
                'texture': self.b_excluir_b3,
                'x': 965,
                'y': 260,
                'width': 38,
                'height': 38,
                'action': lambda: self.excluir_baralho(2)
            })

        else:
            self.b_montar = arcade.load_texture("interface_grafica/resources/widgets/botoes/b-montar.png")

            self.botoes.append({
                'texture': self.b_montar,
                'x': 825,
                'y': 180,
                'width': 150,
                'height': 50,
                'action': self.tela_montar_baralho # tela de montar baralhos
            })

        self.b_jogar = arcade.load_texture("interface_grafica/resources/widgets/botoes/b-jogar.png")
        self.botoes.append({
            'texture': self.b_jogar,
            'x': LARGURA_TELA // 2,
            'y': 46,
            'width': 200,
            'height': 70,
            'action': self.tela_criar_partida 
        })

        self.b_logout = arcade.load_texture("interface_grafica/resources/widgets/botoes/b-excluir.png")
        self.botoes.append({
            'texture': self.b_logout,
            'x': 970,
            'y': 570,
            'width': 35,
            'height': 35,
            'action': self.fazer_logout 
        })
        
        self.setup() # chama o método setup para configurar a interface gráfica da visão.

        
    def setup(self):
        #auxiliar:
        vbox = arcade.gui.UIBoxLayout()
        self.msg = arcade.gui.UITextArea(
            text="", height=40, font_size=12, font_name=POPPINS, text_color=arcade.color.RED
        )
        vbox.add(self.msg)
        
        self.gerencia_entrada.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center", anchor_y="top", child=vbox
            )
        )

    def on_show_view(self):
        # habilita o gerenciador de interface, tornando os widgets interativos.
        self.gerencia_entrada.enable()

    # define o método on_hide_view, chamado quando a visão é escondida. Desativa o gerenciador de interface.
    def on_hide_view(self):
        # desativa o gerenciador de interface, tornando os widgets não interativos.
        self.gerencia_entrada.disable()
    
    # ações a serem executadas quando a janela é fechada
    def on_close(self):
        self.cliente.logout()
    
    # define o método on_update, chamado a cada atualização do quadro, por exemplo atualiza algum atributo.
    def on_update(self, delta_time: float):
        if self.mensagem:
            self.msg.text = self.mensagem
            self.mensagem = None
        
    def on_draw(self):
        arcade.start_render()  
        
        arcade.draw_text(self.cliente.get_username(), 945, 560,
                    arcade.color.WHITE, font_size=12, font_name=POPPINS,  anchor_x="right")

        # Carrossel da Coleção
        arcade.draw_texture_rectangle(LARGURA_TELA // 2, 430, 950, 220, self.fundo_colecao)
        
        arcade.draw_text(f"Coleção", 30, 555, AMARELO, font_size=20, font_name=POPPINS, anchor_x="left")
        arcade.draw_text(f"Você possui {len(self.colecao)} cartas =)", 945, 545, AMARELO, font_size=8, font_name=POPPINS, anchor_x="right")

        espacamento = 160
        largura_carta = 125
        altura_carta = 180
        cartas_visiveis = 5

        for i in range(cartas_visiveis):
            indice_carta = (self.indice_inicial + i) % len(self.cartas)
            carta = self.cartas[indice_carta]
            pos_x = 180 + i * espacamento
            pos_y = 430

            arcade.draw_texture_rectangle(pos_x, pos_y, largura_carta, altura_carta, carta)

        arcade.draw_texture_rectangle(75, 430,
                                      50, 50, self.seta_esquerda)
        arcade.draw_texture_rectangle(LARGURA_TELA - 75, 430,
                                      50, 50, self.seta_direita)
        
        arcade.draw_text("Baralhos", 30, 280, AMARELO, font_size=20, font_name=POPPINS, anchor_x="left")
        
        if len(self.baralhos) == 0:
            arcade.draw_text("Você ainda não possui nenhum baralho montado =(", 30, 240, arcade.color.WHITE, font_size=10, font_name=POPPINS, anchor_x="left")

        # Carrossel do Baralho 1
        if self.baralho_1:
            arcade.draw_texture_rectangle(179, 180, 300, 180, self.fundo_b1)
            
            espacamento = 116
            largura_carta = 100
            altura_carta = 145
            cartas_visiveis_baralhos = 2

            for i in range(cartas_visiveis_baralhos):
                indice_carta_b1 = (self.indice_inicial_b1 + i) % len(self.baralho_1)
                carta = self.baralho_1[indice_carta_b1]
                pos_x = 125 + i * espacamento
                pos_y = 180

                arcade.draw_texture_rectangle(pos_x, pos_y, largura_carta, altura_carta, carta)

            arcade.draw_texture_rectangle(55, 180,
                                        20, 20, self.seta_esquerda_b1)
            arcade.draw_texture_rectangle(305, 180,
                                        20, 20, self.seta_direita_b1)
            
        # Carrossel do Baralho 2
        if self.baralho_2 and self.fundo_b2:
            arcade.draw_texture_rectangle(499, 180, 300, 180, self.fundo_b2)
            
            espacamento = 116
            largura_carta = 100
            altura_carta = 145
            cartas_visiveis_baralhos = 2

            for i in range(cartas_visiveis_baralhos):
                indice_carta_b2 = (self.indice_inicial_b2 + i) % len(self.baralho_2)
                carta = self.baralho_2[indice_carta_b2]
                pos_x = 443 + i * espacamento
                pos_y = 178

                arcade.draw_texture_rectangle(pos_x, pos_y, largura_carta, altura_carta, carta)

            arcade.draw_texture_rectangle(378, 180,
                                        20, 20, self.seta_esquerda_b2)
            arcade.draw_texture_rectangle(623, 180,
                                        20, 20, self.seta_direita_b2)

        # Carrossel do Baralho 3
        if self.baralho_3 and self.fundo_b3:
            arcade.draw_texture_rectangle(825, 180, 300, 180, self.fundo_b3)
            
            espacamento = 116
            largura_carta = 100
            altura_carta = 145
            cartas_visiveis_baralhos = 2

            for i in range(cartas_visiveis_baralhos):
                indice_carta_b3 = (self.indice_inicial_b3 + i) % len(self.baralho_3)
                carta = self.baralho_3[indice_carta_b3]
                pos_x = 765 + i * espacamento
                pos_y = 180

                arcade.draw_texture_rectangle(pos_x, pos_y, largura_carta, altura_carta, carta)

            arcade.draw_texture_rectangle(700, 180,
                                        20, 20, self.seta_esquerda_b3)
            arcade.draw_texture_rectangle(945, 180,
                                        20, 20, self.seta_direita_b3)
            
        for botao in self.botoes:
            if 'texture' in botao:
                arcade.draw_texture_rectangle(botao['x'], botao['y'], botao['width'], botao['height'], botao['texture'])
        
        self.gerencia_entrada.draw()
        
    def on_mouse_press(self, x, y, button, modifiers):
        self.msg.text = ""
        for botao in self.botoes:
            if 'texture' in botao:
                if (botao['x'] - botao['width'] / 2 < x < botao['x'] + botao['width'] / 2 and
                        botao['y'] - botao['height'] / 2 < y < botao['y'] + botao['height'] / 2):
                    botao['action']()
                    break

        # Setas para Coleção
        if 75 - 25 < x < 75 + 25 and 430 - 25 < y < 430 + 25:
            self.indice_inicial = (self.indice_inicial - 1) % len(self.cartas)

        elif LARGURA_TELA - 75 - 25 < x < LARGURA_TELA - 75 + 25 and 430 - 25 < y < 430 + 25:
            self.indice_inicial = (self.indice_inicial + 1) % len(self.cartas)

        # Setas para Baralho 1
        if 55 - 10 < x < 55 + 10 and 180 - 10 < y < 180 + 10:
            self.indice_inicial_b1 = (self.indice_inicial_b1 - 1) % len(self.baralho_1)

        elif 305 - 10 < x < 305 + 10 and 180 - 10 < y < 180 + 10:
            self.indice_inicial_b1 = (self.indice_inicial_b1 + 1) % len(self.baralho_1)

        # Setas para Baralho 2
        if 378 - 10 < x < 378 + 10 and 180 - 10 < y < 180 + 10:
            self.indice_inicial_b2 = (self.indice_inicial_b2 - 1) % len(self.baralho_2)

        elif 623 - 10 < x < 623 + 10 and 180 - 10 < y < 180 + 10:
            self.indice_inicial_b2 = (self.indice_inicial_b2 + 1) % len(self.baralho_2)

        # Setas para Baralho 3
        if 700 - 10 < x < 700 + 10 and 180 - 10 < y < 180 + 10:
            self.indice_inicial_b3 = (self.indice_inicial_b3 - 1) % len(self.baralho_3)

        elif 945 - 10 < x < 945 + 10 and 180 - 10 < y < 180 + 10:
            self.indice_inicial_b3 = (self.indice_inicial_b3 + 1) % len(self.baralho_3)

        self.on_draw()

    def fazer_logout(self):
        self.cliente.logout()
        self.window.show_view(self.back_to_login(self.cliente)) 
    
    def tela_montar_baralho(self):
        self.window.show_view(MontarBaralho(self.cliente,self.info_perfil, Perfil, self.back_to_login, self.criar_partida)) 
    
    def tela_criar_partida(self):
        self.window.show_view(self.criar_partida(self.cliente, self.back_to_login)) 
    
    def excluir_baralho(self, indice):
        s, msg = self.cliente.excluir_baralho(indice)
        if s == True:
            info_perfil = msg
            self.window.show_view(Perfil(self.cliente, info_perfil, self.back_to_login, self.criar_partida)) 
        else:
            self.mensagem = msg
        