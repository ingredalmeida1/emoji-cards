import arcade
import arcade.gui # submódulo gui do arcade, que fornece componentes para criar interfaces gráficas.

from ..resources.constantes import LARGURA_TELA, ALTURA_TELA, AZUL, AMARELO, POPPINS, AGRANDIR

from ..telas.criar_partida import CriarPartida

import threading

class Login(arcade.View):
    def __init__(self, cliente):
        super().__init__()

        arcade.set_background_color(AZUL)

        self.logo = None
        self.botoes = []
        self.fundo_campo_nome = None
        self.fundo_campo_senha = None

        self.gerencia_entrada = arcade.gui.UIManager()
        # self.gerencia_entrada.enable()

        #atributos comunicacao:
        self.cliente = cliente
        self.mensagem = None
        
        self.setup() # chama o método setup para configurar a interface gráfica da visão.

    def setup(self):
        
        self.campo_nome = arcade.gui.UIInputText(
            text = '',
            width = 270,
            text_color = arcade.color.WHITE,
            font_name = POPPINS
        )
        
        self.gerencia_entrada.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="left",
                anchor_y="bottom",
                align_x=635,
                align_y=313,
                child=self.campo_nome
            )
        )

        self.campo_senha = arcade.gui.UIInputText(
            text='',
            width=270,
            text_color = arcade.color.WHITE,
            font_name = POPPINS
        )
        
        self.gerencia_entrada.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="left",
                anchor_y="bottom",
                align_x=635,
                align_y=213,
                child=self.campo_senha
            )
        )
        
        self.logo = arcade.load_texture("interface_grafica/resources/widgets/logo.png")
        self.b_login = arcade.load_texture("interface_grafica/resources/widgets/botoes/b-login.png")
        self.fundo_campo_nome = arcade.load_texture("interface_grafica/resources/widgets/campo.png")
        self.fundo_campo_senha = arcade.load_texture("interface_grafica/resources/widgets/campo.png")

        self.botoes.append({
            'texture': self.b_login,
            'x': 770,
            'y': 180,
            'width': 200,
            'height': 70,
            'action': self.login
        })
        self.botoes.append({
            'text': "criar conta",
            'x': 770,
            'y': 110,
            'font_size': 15,
            'font_name': POPPINS,
            'action': self.criar_conta
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
  
    def on_draw(self):
        arcade.start_render()

        if self.logo:
            arcade.draw_texture_rectangle(300, ALTURA_TELA // 2, self.logo.width, 
                                          self.logo.height, self.logo)
        if self.fundo_campo_nome:
            arcade.draw_texture_rectangle(770, 355, 350, 
                                          60, self.fundo_campo_nome)
        if self.fundo_campo_senha:
            arcade.draw_texture_rectangle(770, 255, 350, 
                                          60, self.fundo_campo_senha)

        for botao in self.botoes:
            if 'texture' in botao:
                arcade.draw_texture_rectangle(botao['x'], botao['y'], botao['width'], botao['height'], 
                                              botao['texture'])
            elif 'text' in botao:
                arcade.draw_text(botao['text'], botao['x'], botao['y'], AMARELO, 
                                 font_size=botao['font_size'], font_name=botao['font_name'], anchor_x="center")

        arcade.draw_text("username", 770, 395,
                         arcade.color.WHITE, font_size=15, font_name=POPPINS, anchor_x="center")
        arcade.draw_text("senha", 770, 295,
                         arcade.color.WHITE, font_size=15, font_name=POPPINS, anchor_x="center")

        self.gerencia_entrada.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        self.msg.text = ""
        for botao in self.botoes:
            if 'texture' in botao:
                if (botao['x'] - botao['width'] / 2 < x < botao['x'] + botao['width'] / 2 and
                        botao['y'] - botao['height'] / 2 < y < botao['y'] + botao['height'] / 2):
                    botao['action']()
                    break
            elif 'text' in botao:
                text_width = 100
                text_height = botao['font_size']
                if (botao['x'] - text_width / 2 < x < botao['x'] + text_width / 2 and
                        botao['y'] - text_height / 2 < y < botao['y'] + text_height / 2):
                    # prox_tela = botao['action']()
                    # self.window.show_view(prox_tela)
                    botao['action']()
                    break 
       
    # define o método on_update, chamado a cada atualização do quadro, por exemplo atualiza algum atributo.
    def on_update(self, delta_time: float):
        if self.mensagem:
            if self.mensagem == 'Login feito com sucesso!' or self.mensagem == 'Usuário adicionado com sucesso!':
                self.window.show_view(CriarPartida(self.cliente, Login))
            
            self.msg.text = self.mensagem
            self.mensagem = None
        
    def on_show_view(self):
        # habilita o gerenciador de interface, tornando os widgets interativos.
        self.gerencia_entrada.enable()

    # define o método on_hide_view, chamado quando a visão é escondida. Desativa o gerenciador de interface.
    def on_hide_view(self):
        # desativa o gerenciador de interface, tornando os widgets não interativos.
        self.gerencia_entrada.disable()
   
    def login(self):
        try:
            threading.Thread(target=self.comunicar_confirmar_login).start()
        except Exception as e:
            self.mensagem = f"Ocorreu um erro: {str(e)}"

    def comunicar_confirmar_login(self):
        username = self.campo_nome.text
        password = self.campo_senha.text       
        if username != "" and password != "":
            s, msg = self.cliente.login(username, password)
            self.mensagem = msg
        else:
            self.mensagem = "Preencha Todos os Campos!"
    
    def criar_conta(self):
        try:
            threading.Thread(target=self.comunicar_criar_conta).start()
        except Exception as e:
            self.mensagem = f"Ocorreu um erro: {str(e)}"

    def comunicar_criar_conta(self):
        username = self.campo_nome.text
        senha = self.campo_senha.text       
        if username != "" and senha != "":
            s, msg = self.cliente.criar_conta(username, senha)
            self.mensagem = msg
        else:
            self.mensagem = "Preencha Todos os Campos!"
