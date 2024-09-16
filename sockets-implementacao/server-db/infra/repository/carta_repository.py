from infra.configs.connection import DBConnectionHandler
from infra.entities.carta import Carta

class CartaRepository: #vai ser como a interface para a tabela Carta
    def select_all(self):
        with DBConnectionHandler() as db: #as instanciar o objeto assim:
            #chama o método enter: retorna self, que vai estar em db
            cartas = db.session.query(Carta).all()
            return cartas
            #chama o método exit
    
    def get_emocoes(self):
        with DBConnectionHandler() as db:
            emocoes = db.session.query(Carta.emocao).all()
            return [emocao[0] for emocao in emocoes]
    
    #metodo para buscar informacoesd e uma carta atraves da emocao
    def get_carta(self, emocao):
        with DBConnectionHandler() as db:
            carta = db.session.query(Carta).filter_by(emocao=emocao).first()
            return carta #se retornar None: carta não existe no banco de dados  
    
    #metodo para iniciar o banco de dados com as cartas disponíveis no jogo
    def add_all_cartas(self):
        try:
            with DBConnectionHandler() as db:
                cartas = [Carta(emocao='autoestima',  atributos="{'tempo':'anos', 'impacto_social':'positivo', 'efeito_cognitivo':'certeza', 'qtd_emocoes_opostas':1, 'qtd_emocoes_relacionadas':1, 'intensidade':5}"), 
                          Carta(emocao='raiva',       atributos="{'tempo':'minutos', 'impacto_social':'negativo', 'efeito_cognitivo':'confusao', 'qtd_emocoes_opostas':2, 'qtd_emocoes_relacionadas':6, 'intensidade':3}"),
                          Carta(emocao='alegria',     atributos="{'tempo':'dias', 'impacto_social':'positivo', 'efeito_cognitivo':'clareza', 'qtd_emocoes_opostas':2, 'qtd_emocoes_relacionadas':5, 'intensidade':5}"),
                          Carta(emocao='tristeza',    atributos="{'tempo':'dias', 'impacto_social':'negativo', 'efeito_cognitivo':'duvida', 'qtd_emocoes_opostas':2, 'qtd_emocoes_relacionadas':4, 'intensidade':2}"),
                          Carta(emocao='medo',        atributos="{'tempo':'minutos', 'impacto_social':'negativo', 'efeito_cognitivo':'confusao', 'qtd_emocoes_opostas':1, 'qtd_emocoes_relacionadas':1, 'intensidade':4}"),
                          Carta(emocao='amor',        atributos="{'tempo':'anos', 'impacto_social':'positivo', 'efeito_cognitivo':'certeza', 'qtd_emocoes_opostas':2, 'qtd_emocoes_relacionadas':3, 'intensidade':4}"),
                          Carta(emocao='desgosto',    atributos="{'tempo':'minutos', 'impacto_social':'negativo', 'efeito_cognitivo':'clareza', 'qtd_emocoes_opostas':2, 'qtd_emocoes_relacionadas':4, 'intensidade':3}"),
                          Carta(emocao='surpresa',    atributos="{'tempo':'minutos', 'impacto_social':'positivo', 'efeito_cognitivo':'confusao', 'qtd_emocoes_opostas':1, 'qtd_emocoes_relacionadas':2, 'intensidade':4}"),
                          Carta(emocao='desprezo',    atributos="{'tempo':'dias', 'impacto_social':'negativo', 'efeito_cognitivo':'clareza', 'qtd_emocoes_opostas':2, 'qtd_emocoes_relacionadas':3, 'intensidade':1}"),
                          Carta(emocao='gratidao',    atributos="{'tempo':'anos', 'impacto_social':'positivo', 'efeito_cognitivo':'certeza', 'qtd_emocoes_opostas':2, 'qtd_emocoes_relacionadas':5, 'intensidade':3}"),
                          Carta(emocao='culpa',       atributos="{'tempo':'dias', 'impacto_social':'negativo', 'efeito_cognitivo':'duvida', 'qtd_emocoes_opostas':1, 'qtd_emocoes_relacionadas':4, 'intensidade':3}"),
                          Carta(emocao='esperanca',   atributos="{'tempo':'dias', 'impacto_social':'positivo', 'efeito_cognitivo':'certeza', 'qtd_emocoes_opostas':1, 'qtd_emocoes_relacionadas':2, 'intensidade':4}"),
                          Carta(emocao='vergonha',    atributos="{'tempo':'minutos', 'impacto_social':'negativo', 'efeito_cognitivo':'confusao', 'qtd_emocoes_opostas':1, 'qtd_emocoes_relacionadas':1, 'intensidade':4}"),
                          Carta(emocao='alivio',      atributos="{'tempo':'minutos', 'impacto_social':'positivo', 'efeito_cognitivo':'clareza', 'qtd_emocoes_opostas':2, 'qtd_emocoes_relacionadas':3, 'intensidade':2}"),
                          Carta(emocao='frustracao',  atributos="{'tempo':'dias', 'impacto_social':'negativo', 'efeito_cognitivo':'confusao', 'qtd_emocoes_opostas':2, 'qtd_emocoes_relacionadas':4, 'intensidade':3}"),
                          Carta(emocao='empatia',     atributos="{'tempo':'dias', 'impacto_social':'positivo', 'efeito_cognitivo':'clareza', 'qtd_emocoes_opostas':1, 'qtd_emocoes_relacionadas':3, 'intensidade':3}"),
                          Carta(emocao='ciume',       atributos="{'tempo':'minutos', 'impacto_social':'negativo', 'efeito_cognitivo':'confusao', 'qtd_emocoes_opostas':2, 'qtd_emocoes_relacionadas':4, 'intensidade':4}"),
                          Carta(emocao='ansiedade',   atributos="{'tempo':'dias', 'impacto_social':'negativo', 'efeito_cognitivo':'confusao', 'qtd_emocoes_opostas':2, 'qtd_emocoes_relacionadas':4, 'intensidade':4}"),
                          Carta(emocao='paz',         atributos="{'tempo':'dias', 'impacto_social':'positivo', 'efeito_cognitivo':'clareza', 'qtd_emocoes_opostas':2, 'qtd_emocoes_relacionadas':3, 'intensidade':1}"),
                          Carta(emocao='curiosidade', atributos="{'tempo':'minutos', 'impacto_social':'positivo', 'efeito_cognitivo':'clareza', 'qtd_emocoes_opostas':1, 'qtd_emocoes_relacionadas':3, 'intensidade':3}"),
                          Carta(emocao='euforia',     atributos="{'tempo':'minutos', 'impacto_social':'positivo', 'efeito_cognitivo':'clareza', 'qtd_emocoes_opostas':1, 'qtd_emocoes_relacionadas':3, 'intensidade':5}"),
                          Carta(emocao='desespero',   atributos="{'tempo':'minutos', 'impacto_social':'negativo', 'efeito_cognitivo':'confusao', 'qtd_emocoes_opostas':2, 'qtd_emocoes_relacionadas':4, 'intensidade':5}"),
                          Carta(emocao='respeito',    atributos="{'tempo':'anos', 'impacto_social':'positivo', 'efeito_cognitivo':'clareza', 'qtd_emocoes_opostas':1, 'qtd_emocoes_relacionadas':2, 'intensidade':3}"),
                          Carta(emocao='solidao',     atributos="{'tempo':'dias', 'impacto_social':'negativo', 'efeito_cognitivo':'duvida', 'qtd_emocoes_opostas':2, 'qtd_emocoes_relacionadas':2, 'intensidade':2}")
                        ]
                
                db.session.add_all(cartas)
                db.session.commit()
                return True, 'Cartas adicionadas com sucesso!'
                
        except Exception as e:
            db.session.rollback() #volte o banco ao estado anterior, caso ela tenha sido alterado
            return False, f"Erro ao adicionar cartas: {str(e)}"


    #metodo para adicionar uma carta ao baralho, se ainda não existir carta com mesmo nome de emocao
    def add_carta(self, emocao, atributos):
        try:
            with DBConnectionHandler() as db:
                if db.session.query(Carta).filter_by(emocao=emocao).first():
                    return False, 'Carta já existe!'
                
                nova_carta = Carta( emocao=emocao,
                                    atributos=atributos
                )
                db.session.add(nova_carta)
                db.session.commit()
                return True, 'Carta adicionada com sucesso!'
                
        except Exception as e:
            db.session.rollback() #volte o banco ao estado anterior, caso ela tenha sido alterado
            return False, f"Erro ao adicionar carta: {str(e)}"
    

        