# Servidor de Banco de dados

## Possíveis mensagens a serem enviadas e respectivos retornos

```
msg = f"cartas_disponiveis'
response = "emocao1,emocao2, ... ,emocaoN" ou "Nenhuma Carta Cadastrada"

if response != "Nenhuma Carta Cadastrada":
    vetor_nome_emocoes = response.split(',')
```

```
msg = f"atributos_carta {emocao}"
response =  "{'tempo':'x', 'impacto_social':'x', 'efeito_cognitivo':'x', 'qtd_emocoes_opostas':X, 'qtd_emocoes_relacionadas':X, 'intensidade':X}" ou "Carta não existe!"

if response != "Carta não existe!":
    dicionario_atributos = eval(response)
    acessar_atributo = dicionario_atributos['<nome_atributo>']
```

```
msg = f"adicionar_usuario {username} {senha} {cartas}"
response = "Usuário adicionado com sucesso!" ou "Usuário já existe!" ou "Erro ao adicionar usuário: {excecao}"

obs: cartas deve ser um string como o nome das emocoes separadas por vircula, por exemplo: acartas = alivio, amor, ..., paz (sem colocar aspas)
```

```
msg = f"verificar_username {username}"
response = "Username está disponível!" ou "Username já existe!"
```

```
msg = f"verificar_login {username} {senha}"
response = "Login Correto!" ou "Senha Incorreta!" ou "Username Inválido!"
```

```
msg = f"buscar_usuario {username}"
response = "{ 'username': 'x','status': 'x','colecao_cartas': 'x','qtd_baralhos': X,'baralhos': 'x'}" ou "Usuário não encontrado"
```

```
msg = f"get_status (username)"
response = "status" ou "Usuário não encontrado"
```

```
msg = f"set_status,(username) {status}"
response = "Status atualizado com sucesso!" ou "Usuário não encontrado" ou "Erro ao atualizar status do usuário: {excecao}"
```

```
msg = f"get_colecao (username)"
response = "emocao1,emocao2, ... ,emocaoN" ou "Usuário Não Existe"
```

```
msg = f"adicionar_carta_na_colecao {username} {emocao}"
response =  "Carta adicionada com sucesso!" ou "Usuário não encontrado" ou "Erro ao adicionar carta: {excecao}'
```

```
msg = f"get_baralhos {username}"
response = "" ou "emocao1,emocao2,emocao3,...,emocao9-emocao1,emocao2,emocao3,...,emocao9" ou "Usuário não encontrado" 

if response != "Usuário não encontrado":
    if responde == "":
        print("Usuário ainda não tem baralhos")
    else:
        baralhos = response.split(-)
        for baralho in baralhos:
            cartas = baralho.split(',')

```

```
msg = f"get_qtd_baralhos {username}"
response = "{qtd_baralhos}" ou "Usuário não encontrado" 

if response != "Usuário não encontrado":
    qtd_baralhos = int(response)
```

```
msg = f"adicionar_baralho {username} {baralho}"
response = "Baralho adicionado com sucesso" ou "Usuário não encontrado" ou "Erro ao adicionar baralho: {excecao}"

obs: baralho deve ser um string como o nome das emocoes separadas por vircula, por exemplo: emocao1,emocao2, ... ,emocaoN (sem aspas)
```

```
msg = f"excluir_baralho {username} {indice}"
response =  "Baralho excluído com sucesso" ou "usuário Não Possui Nenhum Baralho" ou "Índice do baralho inválido" ou "Usuário não encontrado" ou  "Erro ao excluir baralho: {excecao}"

obs: indice deve ser 0, 1 ou 2, fazendo referencia a ordem do baralho
```

