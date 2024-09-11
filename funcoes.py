import datetime
import csv
from functools import reduce
import os

produtos = []
vendas = []

def titulo(msg):
    print('=' * 50)
    print(f'{msg:^50}')
    print('=' * 50)

def linha():
    print('-' * 50)

def menu():
    titulo('MENU')
    print("""Opções disponíveis:

    1) Cadastrar novo produto no sistema
    2) Atualizar dados de um produto
    3) Excluir um produto do sistema
    4) Realizar uma venda
    5) Visualizar produtos cadastrados no sistema
    6) Sair
    """)

def input_validado(mensagem, tipo, erro_mensagem, condicao=lambda x: True):
    while True:
        try:
            valor = tipo(input(mensagem))
            if not condicao(valor):
                raise ValueError
        except (ValueError, TypeError):
            print(erro_mensagem)
        else:
            return valor

def atributo_produto(arg):
    if arg == 'identificador':
        return input_validado(
            'Digite o identificador do produto (5 números inteiros): ',
            str,
            'Ops! O identificador deve ser um número inteiro de 5 dígitos...',
            lambda x: x.isnumeric() and len(x) == 5
        )
    elif arg == 'nome':
        return input_validado(
            'Nome do produto: ',
            str,
            'Ops! O campo "nome" não pode ser vazio...',
            lambda x: x.strip() != ''
        ).lower().strip()
    elif arg == 'marca':
        return input_validado(
            'Marca do produto: ',
            str,
            'Ops! O campo "marca" não pode ser vazio...',
            lambda x: x.strip() != ''
        ).lower().strip()
    elif arg == 'preco':
        return input_validado(
            'Preço do produto (Digite apenas o valor): R$',
            str,
            'Ops! O preço do produto não pode conter letras...',
            lambda x: x.replace(',', '').replace('.', '').isnumeric()
        ).replace(',', '.')
    elif arg == 'estoque':
        return input_validado(
            'Quantidade em estoque (número inteiro): ',
            int,
            'Ops! O estoque do produto deve ser um valor inteiro.'
        )
    elif arg == 'descricao':
        descricao = input('Descrição (Aperte ENTER direto para "sem descrição"): ').lower().strip()
        return descricao if descricao else 'sem descrição'

def verificador(identificador):
    return list(map(lambda produto: identificador in produto.keys(), produtos))

def viz_dados_produto(identificador):
    linha()
    for produto in produtos:
        for key, value in produto.items():
            if identificador == key:
                for key2, value2 in value.items():
                    print(f'{key2}: {value2}')
                linha()

def viz_dados_produtos():
    linha()
    for produto in produtos:
        for key, value in produto.items():
            print(f'id : {key}')
            for key2, value2 in value.items():
                print(f'{key2}: {value2}')
            linha()

def cadastrar():
    titulo('CADASTRAR PRODUTO')
    identificador = atributo_produto('identificador')
    verificacao = verificador(identificador)
    if True in verificacao:
        print('Ops! Esse identificador já foi cadastrado para outro produto... Tente novamente.')
    else:
        produto = {'nome': atributo_produto('nome'),
                   'marca': atributo_produto('marca'),
                   'preco': float(atributo_produto('preco')),
                   'estoque': atributo_produto('estoque'),
                   'descricao': atributo_produto('descricao')}

        produtos.append({identificador: produto})
        linha()
        print('Dados do produto adicionado:')
        print(f'id: {identificador}')
        for k, v in produto.items():
            print(f'{k}: {v}')
        linha()
        print(f'O produto {produto["nome"]} foi cadastrado com sucesso!')

def atualizar():
    titulo('ATUALIZAR PRODUTO')
    identificador = atributo_produto('identificador')
    verificacao = verificador(identificador)
    if True in verificacao:
        for produto in produtos:
            for chave, valor in produto.items():
                if identificador == chave:
                    print(f'id: {chave}')
                    for chave2, valor2 in valor.items():
                        print(f'{chave2}: {valor2}')
                    linha()
                    print('''O que deseja fazer?

1) Atualizar todos os dados do produto
2) Atualizar um campo específico
3) Cancelar atualização''')
                    linha()
                    while True:
                        opcao = input('Digite a sua opção: ')
                        if opcao == '1':
                            valor['nome'] = atributo_produto('nome')
                            valor['marca'] = atributo_produto('marca')
                            valor['preco'] = float(atributo_produto('preco'))
                            valor['estoque'] = atributo_produto('estoque')
                            valor['descricao'] = atributo_produto('descricao')
                            print('Produto atualizado com sucesso!')
                            break
                        elif opcao == '2':
                            print('''Qual elemento deseja atualizar?

1) Nome
2) Marca
3) Preço
4) Estoque
5) Descrição''')
                            linha()
                            dado = input('Digite o número do dado que quer atualizar: ')
                            if dado == '1':
                                valor['nome'] = atributo_produto('nome')
                            elif dado == '2':
                                valor['marca'] = atributo_produto('marca')
                            elif dado == '3':
                                valor['preco'] = float(atributo_produto('preco'))
                            elif dado == '4':
                                valor['estoque'] = atributo_produto('estoque')
                            elif dado == '5':
                                valor['descricao'] = atributo_produto('descricao')
                            else:
                                print('Opção inválida. Tente novamente.')
                            print('Produto atualizado com sucesso!')
                            break
                        elif opcao == '3':
                            print('Ação cancelada.')
                            break
                        else:
                            print('Opção inválida. Digite um dos números do menu.')
        viz_dados_produto(identificador)
    else:
        print('Ops! Não existe nenhum produto cadastrado com esse identificador.')

def excluir():
    titulo('EXCLUIR PRODUTO')
    identificador = atributo_produto('identificador')
    verificacao = verificador(identificador)
    if True in verificacao:
        viz_dados_produto(identificador)
        print('''Tem certeza que deseja excluir este produto?

1) Excluir produto
2) Cancelar exclusão''')

        while True:
            escolha = input('Digite o número da sua escolha: ')
            if escolha == '1':
                indexador = [i for i, produto in enumerate(produtos) if identificador in produto][0]
                produtos.pop(indexador)
                print('Produto excluído com sucesso!')
                break
            elif escolha == '2':
                print('Exclusão cancelada.')
                break
            else:
                print('Ops! Valor inválido... Tente novamente.')

def buscar_produto(identificador, args):
    chaves = [list(produto.keys())[0] for produto in args]
    indice = chaves.index(identificador)
    return indice

def verifica_estoque(identificador):
    produto = produtos[buscar_produto(identificador, produtos)]
    estoque = produto[identificador]['estoque']
    return input_validado(
        'Digite a quantidade desejada: ',
        int,
        'A quantidade desejada deve ser um inteiro maior que zero e dentro do estoque.',
        lambda x: 0 < x <= estoque
    )

def adicionar_ao_carrinho():
    identificador = atributo_produto('identificador')
    verificacao = verificador(identificador)
    if True in verificacao:
        data = datetime.date.today()
        hora = datetime.datetime.now().time()
        indice = buscar_produto(identificador, produtos)
        produto = produtos[indice][identificador]
        quantidade = verifica_estoque(identificador)

        venda = {
            'data': data,
            'hora': hora,
            'id': identificador,
            'nome': produto['nome'],
            'marca': produto['marca'],
            'preco': produto['preco'],
            'quantidade': quantidade,
            'valor total': produto['preco'] * quantidade,
        }

        vendas.append(venda)
        return venda

def montar_carrinho():
    viz_dados_produtos(produtos)
    carrinho = []
    opcao = None
    while opcao != "3":
        opcao = input('''Digite a opção desejada:
    1) Adicionar produto ao carrinho
    2) Remover item do carrinho
    3) Sair\n''').strip()

        if opcao == "1":
            carrinho.append(adicionar_ao_carrinho())
            print("Produto adicionado com sucesso!")
        elif opcao == "2":
            excluir(carrinho)
        elif opcao == "3":
            print("Carrinho montado com sucesso!")

    return carrinho

def finalizar_compra():
    print('Estes são os produtos disponíveis:')
    carrinho = montar_carrinho()

    if not carrinho:
        print("O carrinho está vazio.")
        return

    valor_total = reduce(lambda a, b: a + b['valor total'], carrinho, 0)
    titulo('RESUMO DA COMPRA')

    for item in carrinho:
        print(f"{item['nome']} - {item['quantidade']} unidades - Total: R${item['valor total']:.2f}")

    linha()
    print(f"Valor total da compra: R${valor_total:.2f}")

    with open('relatorio_vendas.csv', 'w', newline='') as arquivo:
        campo_nomes = ['data', 'hora', 'id', 'nome', 'marca', 'preco', 'quantidade', 'valor total']
        writer = csv.DictWriter(arquivo, fieldnames=campo_nomes)
        writer.writeheader()
        for item in vendas:
            writer.writerow(item)

    print("Relatório de vendas gerado com sucesso!")

def gerar_relatorio_vendas():
    if vendas:
        with open('relatorio_vendas.csv', 'w', newline='') as arquivo:
            campo_nomes = ['data', 'hora', 'id', 'nome', 'marca', 'preco', 'quantidade', 'valor total']
            writer = csv.DictWriter(arquivo, fieldnames=campo_nomes)
            writer.writeheader()
            for item in vendas:
                writer.writerow(item)
        print("Relatório de vendas gerado com sucesso!")
    else:
        print("Não há vendas para gerar relatório.")


def gerar_relatorio_estoque():
    if produtos:
        with open('relatorio_estoque.csv', 'w', newline='') as arquivo:
            campo_nomes = ['identificador', 'nome', 'marca', 'preco', 'quantidade', 'descricao']
            writer = csv.DictWriter(arquivo, fieldnames=campo_nomes)
            writer.writeheader()
            for produto_dict in produtos:
                for identificador, produto in produto_dict.items():
                    writer.writerow({
                        'identificador': identificador,
                        'nome': produto['nome'],
                        'marca': produto['marca'],
                        'preco': produto['preco'],
                        'quantidade': produto['estoque'],
                        'descricao': produto['descricao']
                    })
        print("Relatório de estoque gerado com sucesso!")
    else:
        print("Não há produtos cadastrados para gerar relatório.")

def carregar_estoque():
    if os.path.exists('relatorio_estoque.csv'):
        with open('relatorio_estoque.csv', newline='') as arquivo:
            reader = csv.DictReader(arquivo)
            for row in reader:
                produto = {
                    'nome': row['nome'],
                    'marca': row['marca'],
                    'preco': float(row['preco']),
                    'estoque': int(row['quantidade']),
                    'descricao': row['descricao']
                }
                produtos.append({row['identificador']: produto})
        print("Estoque carregado com sucesso.")
    else:
        print("Nenhum arquivo de estoque encontrado. Novo estoque será criado.")



