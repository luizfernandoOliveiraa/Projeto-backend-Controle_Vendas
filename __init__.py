import funcoes as f


f.carregar_estoque()  # Carregar estoque ao iniciar o programa

opcao = ''
while opcao != '6':
    f.menu()
    opcao = input('Digite o número da sua opção: ').strip()
    if opcao == '1':
        f.cadastrar()
    elif opcao == '2':
        f.atualizar()
    elif opcao == '3':
        f.excluir()
    elif opcao == '4':
        f.finalizar_compra()
    elif opcao == '5':
        f.viz_dados_produtos()
    elif opcao == '6':
        print('Finalizando programa...')
        f.gerar_relatorio_vendas()  # Gera o relatório de vendas
        f.gerar_relatorio_estoque()  # Gera o relatório de estoque
    else:
        print('Opção inválida. Tente novamente.')

