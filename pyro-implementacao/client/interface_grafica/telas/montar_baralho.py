import arcade
import arcade.gui # submódulo gui do arcade, que fornece componentes para criar interfaces gráficas.

from ..resources.constantes import LARGURA_TELA, ALTURA_TELA, AZUL, AMARELO, POPPINS, AGRANDIR

import threading

class MontarBaralho(arcade.View):
    def __init__(self, cliente, info_usuario, perfil_view, back_to_login, back_to_criar_partida):
        super().__init__()
        
        self.cliente = cliente
        self.info_usuario = info_usuario
        self.colecao_usuario = info_usuario['colecao_cartas']
        
        # pra poder voltar para tela perfil:
        self.back_to_perfil = perfil_view
        self.login_view = back_to_login
        self.criar_partida_view = back_to_criar_partida
        
        self.mensagem = None

        arcade.set_background_color(AZUL)

        self.botoes = []

        # Carrossel da Coleção
        self.indice_inicial = 0
        self.cartas = []
        self.mapeamento_cartas = {}
        
        # Lista para armazenar os nomes dos emojis selecionados
        self.escolhas = []

        for emocao in self.colecao_usuario:
            carta = arcade.load_texture(f"interface_grafica/resources/cartas/{emocao}.png")
            self.cartas.append(carta)
            self.mapeamento_cartas[carta] = {
                'texture': arcade.load_texture(f"interface_grafica/resources/emojis/{emocao}.png"),
                'nome': emocao
            }

        self.seta_esquerda = arcade.load_texture("interface_grafica/resources/widgets/seta-esquerda.png")
        self.seta_direita = arcade.load_texture("interface_grafica/resources/widgets/seta-direita.png")
        self.fundo_colecao = arcade.load_texture("interface_grafica/resources/widgets/colecao2.png")
    
        # Carrossel do Baralho 
        self.fundo_baralho = arcade.load_texture("interface_grafica/resources/widgets/baralho.png")
        self.baralho = []

        self.b_montar = arcade.load_texture("interface_grafica/resources/widgets/botoes/b-montar.png")
        self.botoes.append({
            'texture': self.b_montar,
            'x': LARGURA_TELA // 2,
            'y': 46,
            'width': 150,
            'height': 50,
            'action': self.salvar_baralho 
        })
        
        self.gerencia_entrada = arcade.gui.UIManager()
        self.setup()

    def setup(self):
        self.b_perfil = arcade.load_texture("interface_grafica/resources/widgets/botoes/b-perfil.png")
        self.botoes.append({
            'texture': self.b_perfil,
            'x': 970,
            'y': 570,
            'width': 35,
            'height': 35,
            'action': self.perfil
        })
                
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

    def on_draw(self):
        arcade.start_render()  
        
        arcade.draw_text(self.cliente.get_username(), 950, 560,
                    AMARELO, font_size=12, font_name=POPPINS,  anchor_x="right")

        # Carrossel da Coleção    
        arcade.draw_text("Coleção", 30, 555, AMARELO, font_size=20, font_name=POPPINS, anchor_x="left")
        arcade.draw_texture_rectangle(LARGURA_TELA // 2, 395, 950, 308, self.fundo_colecao)

        espacamento = 205
        largura_carta = 180
        altura_carta = 270
        cartas_visiveis = 4

        for i in range(cartas_visiveis):
            indice_carta = (self.indice_inicial + i) % len(self.cartas)
            carta = self.cartas[indice_carta]
            pos_x = 190 + i * espacamento
            pos_y = 396

            arcade.draw_texture_rectangle(pos_x, pos_y, largura_carta, altura_carta, carta)

        arcade.draw_texture_rectangle(68, 400, 50, 50, self.seta_esquerda)
        arcade.draw_texture_rectangle(LARGURA_TELA - 70, 400, 50, 50, self.seta_direita)

        # Carrossel do Baralho
        arcade.draw_text("Escolhas", 30, 210, AMARELO, font_size=20, font_name=POPPINS, anchor_x="left")
        arcade.draw_texture_rectangle(LARGURA_TELA // 2, 145, 950, 120, self.fundo_baralho)

        espacamento_baralho = 100
        largura_baralho = 70
        altura_baralho = 70
        pos_x_baralho = 90

        for carta in self.baralho:
            arcade.draw_texture_rectangle(pos_x_baralho, 145, largura_baralho, altura_baralho, carta['texture'])
            pos_x_baralho += espacamento_baralho

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
        if 70 - 25 < x < 70 + 25 and 400 - 25 < y < 400 + 25:
            self.indice_inicial = (self.indice_inicial - 1) % len(self.cartas)

        elif LARGURA_TELA - 70 - 25 < x < LARGURA_TELA - 70 + 25 and 400 - 25 < y < 400 + 25:
            self.indice_inicial = (self.indice_inicial + 1) % len(self.cartas)
        
        #se nao foi nas setas, olhas se foi nas cartas
        else:
            espacamento = 205
            largura_carta = 280
            altura_carta = 300
            cartas_visiveis = 4

            for i in range(cartas_visiveis):
                pos_x = 200 + i * espacamento
                pos_y = 396

                if pos_x - largura_carta // 2 < x < pos_x + largura_carta // 2 and pos_y - altura_carta // 2 < y < pos_y + altura_carta // 2:
                    indice_carta = (self.indice_inicial + i) % len(self.cartas)
                    carta_selecionada = self.cartas[indice_carta]
                    emoji_correspondente = self.mapeamento_cartas[carta_selecionada]

                    if len(self.baralho) < 9: 
                        self.baralho.append(emoji_correspondente)
                        self.escolhas.append(emoji_correspondente['nome'])
                    
                    else:
                        self.mensagem = "Você já escolheu 9 cartas!"

            espacamento_baralho = 100
            largura_carta_baralho = 60
            altura_carta_baralho = 60
            for i, carta in enumerate(self.baralho):
                pos_x = 90 + i * espacamento_baralho
                pos_y = 145

                if (pos_x - largura_carta_baralho / 2 < x < pos_x + largura_carta_baralho / 2 and
                        pos_y - altura_carta_baralho / 2 < y < pos_y + altura_carta_baralho / 2):
                    self.baralho.pop(i)
                    self.escolhas.pop(i)
                    break

        self.on_draw()

    # define o método on_update, chamado a cada atualização do quadro, por exemplo atualiza algum atributo.
    def on_update(self, delta_time: float):
        if self.mensagem:
            self.msg.text = self.mensagem
            self.mensagem = None
    
    def perfil(self):
        #voltar pro perfil
        self.window.show_view(self.back_to_perfil(self.cliente, self.info_usuario, self.login_view, self.criar_partida_view)) 
        
    def salvar_baralho(self):
        s, msg = self.cliente.adicionar_baralho(self.escolhas)
        if s == True:
            #atualizar info:
            print(self.info_usuario['baralhos'])
            self.info_usuario['baralhos'].append(self.escolhas)
            print(self.info_usuario['baralhos'])
            self.info_usuario['qtd_baralhos'] += 1
            
            #voltar pro perfil
            self.window.show_view(self.back_to_perfil(self.cliente, self.info_usuario, self.login_view, self.criar_partida_view)) 
        else:
            self.mensagem = msg
        
