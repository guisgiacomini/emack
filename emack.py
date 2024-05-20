
import operator

def carregarDados():
    dados = []
    with open('emack.csv', 'r', encoding='utf-8') as file:
        linhas = file.readlines()
        #Remover da lista de dados a primeira linha que contém o nome das colunas
        linhas.pop(0)
        for linha in linhas:
            valores = linha.strip().split(',')
            #Adicionar os valores a um dicionário com chaves correspondentes às categorias apresentadas na primeira linha do CSV
            valores = {'id':valores[0], 
                       'title':valores[1], 
                       'price':float(valores[2]),
                       'listPrice':valores[3],
                       'categoryName':valores[4],
                       'isBestSeller':valores[5],
                       'boughtInLastMonth':int(valores[6])
                       }
            dados.append(valores)

    return dados

def qtdPorCategoria(dados):
    #Dicionário de contadores para cada categoria
    quantidades = {'Livros' : 0, 'Esportes' : 0, 'Moda' : 0, 'Casa' : 0, 'Eletrônicos' : 0}
    for produto in dados:
        quantidades[produto['categoryName']] += 1
    
    return quantidades

def percentualPorCategoria(dados):
    #Executa a função que retorna dicionário contendo o número de itens em cada quantidade
    qtdCategoria = qtdPorCategoria(dados)
    qtdTotal = len(dados)
    percentuais = {}
    #Loop que preenche o dicionário "percentuais" com as chaves representando as categorias
    #Os valores recebem a porcentagem que cada categoria representa dentro do número total (1000) de produtos
    for categoria in qtdCategoria.keys():
        percentuais.update({categoria: 100 * qtdCategoria[categoria] / qtdTotal})
    return percentuais

def proporcaoBestSellers(dados):
    bestSellersPorCategoria = {'Livros':0, 'Esportes':0, 'Moda':0, 'Eletrônicos':0, 'Casa':0}
    for produto in dados:
        categoria = produto['categoryName']
        if produto['isBestSeller'] == 'true':
            #Passa produto por produto, caso seja um Best-Seller o respectivo valor da categoria no dicionário "BestSellersPorCategoria" é adicionado em 1
            bestSellersPorCategoria[categoria] += 1
    #Executa a função que retorna dicionário contendo o número de itens em cada quantidade
    qtdCategoria = qtdPorCategoria(dados)
    proporcoes = {}
    #Loop que preenche o dicionário "proporcoes" com as chaves representando as categorias
    #Cada valor representa a porcentagem referente ao número de Best-Sellers em comparação com o número de itens da categoria em questão
    for categoria in bestSellersPorCategoria.keys():  
        proporcaoBestSeller = 100 * bestSellersPorCategoria[categoria] / qtdCategoria[categoria]
        proporcoes.update({categoria: proporcaoBestSeller })

    return proporcoes


         
def dezMaisCarosEMaisBaratos(dados):
    #A variável produtosOrdenadosPorPreco recebe o retorno da função sorted(), que ordena valores
    #O primeiro parâmetro recebe o conjunto de valores que será iterado para a ordenação
    #O parâmetro "key" recebe uma função, onde o valor de seu retorno será utilizado como valor para ordenação
    #Nesse caso, o "key" recebe a função itemgetter() da biblioteca padrão "operator"
    #Recebendo o parâmetro "price",a cada iteração de sorted() a função retornará o valor relativo à chave "price" no dicionário "dados"
    #Dessa forma, os produtos serão ordenados pelo preço de forma crescente
    produtosOrdenadosPorPreco = sorted(dados, key=operator.itemgetter('price') )
    #maisBaratos recebe os 10 primeiros itens de produtosOrdenadosPorPreco, que são os 10 produtos mais baratos
    maisBaratos= produtosOrdenadosPorPreco[:10]
    #maisCaros recebe os 10 últimos itens de produtosOrdenadosPorPreco, que são os 10 produtos mais caros
    maisCaros = produtosOrdenadosPorPreco[-10:]
    return maisBaratos, maisCaros

def relatorioPorCategoria(dados, opcao):
    listaOpcoes = ['Livros', 'Esportes', 'Moda', 'Casa', 'Eletrônicos']
    arquivoSaida = f'relatorio_{listaOpcoes[opcao-1]}.html'
    relatorio = f'<html><head><meta charset = "UTF-8"><title>Relatório - {listaOpcoes[opcao-1]} </title></head><body>'
    relatorio += f'<h2>Produtos da categoria {listaOpcoes[opcao-1]}</h2><ul>'
    #Loop que registra no texto HTML os produtos que tenham a mesma categoria escolhida pela entrada do usuário 
    for produto in dados:
        if produto['categoryName'] == listaOpcoes[opcao-1]:
            relatorio += f'<li>Nome: {produto['title']}, ID: {produto['id']}</li>'
        
    relatorio += '</ul></body></html>'

    with open(arquivoSaida, 'w', encoding='utf-8') as arquivo:
        arquivo.write(relatorio)


def relatorioTopDezBestSellers(dados):
    bestSellersPorCategoria = {'Livros':[], 'Esportes':[], 'Moda':[], 'Eletrônicos':[], 'Casa':[]}
    topDezBestSellersPorCategoria = {'Livros':[], 'Esportes':[], 'Moda':[], 'Eletrônicos':[], 'Casa':[]}
    #Loop que insere todos os produtos classificados como best-seller em uma dicionário que os separa por categoria
    for produto in dados:
        if produto['isBestSeller'] == 'true':
            bestSellersPorCategoria[produto['categoryName']].append(produto)
    #Loop que ordena cada lista de produtos por categoria com base nas vendas do último mês e salva os 10 primeiros valores em uma chave 
    #de mesmo nome no dicionário "topDezBestSellersPorCategoria";
    for categoria, produtos in bestSellersPorCategoria.items():
        #Função de ordenação "sorted()"" com parâmetro "operator.itemgetter()" utilizada da mesma forma como na função dezMaisCarosEMaisBaratos
        #Agora, utilizando os valores da chave "boughtInLastMonth" como referências para a ordenação
        ordenados = sorted(produtos, key=operator.itemgetter('boughtInLastMonth'), reverse=True)
        topDezBestSellersPorCategoria[categoria] = ordenados[:10]


    arquivoSaida = 'bestsellers.html'
    relatorio = '<html><head><meta charset = "UTF-8"><title>Best-Sellers</title></head><body>'
    #Loop que acessa cada categoria e registra todos os seus produtos em listas não ordenadas HTML
    for categoria, produtos in topDezBestSellersPorCategoria.items():
        relatorio += f'<h2>Top 10 Best-Sellers em {categoria}</h2><ul>'
        for i in range(len(produtos)):
            relatorio += f'<li>Nome: {produtos[i]['title']}, ID: {produtos[i]['id']}, Vendas no último mês: {produtos[i]['boughtInLastMonth']}</li>'
        relatorio += '</ul>'
    relatorio += '</body></html>'

    with open(arquivoSaida, 'w', encoding='utf-8') as arquivo:
        arquivo.write(relatorio)



        
#Principal

#Guarda os dados obtidos do arquivo CSV na variável dadosProdutos
dadosProdutos = carregarDados()
end = False

while not end:
    print("""
------------------------------------------------------------------
    [1] - Quantidade de Produtos por Categoria
    [2] - Percentual de Produtos por Categoria
    [3] - Proporção de Best Sellers por Categoria
    [4] - Os 10 produtos mais caros e mais baratos
    [5] - Gerar relatório HTML de produtos por categoria
    [6] - Gerar relatório HTML com os top 10 Best Sellers
    [7] - Sair
 ------------------------------------------------------------------
          """)
    option = int(input('Opção >>> '))
    
    if option == 1:

        qtdCategoria = qtdPorCategoria(dadosProdutos)
        print("\nQUANTIDADE DE PRODUTOS POR CATEGORIA\n")
        for categoria, quantidade in qtdCategoria.items():
            print(f'{categoria}: {quantidade}')
        print('\n')
        print('Pressione ENTER para retornar ao menu')
        input()

    elif option == 2:
        percentuais = percentualPorCategoria(dadosProdutos)
        print('\nPERCENTUAL DE PRODUTOS POR CATEGORIA\n')

        for categoria, percentual in percentuais.items():
            print(f'{categoria}: {percentual:.2f}%')
        print('\n')
        print('Pressione ENTER para retornar ao menu')
        input()

    elif option == 3:
        proporcoes = proporcaoBestSellers(dadosProdutos)
        print('\nPROPORÇÃO DE BEST-SELLERS POR CATEGORIA\n')

        for categoria, proporcao in proporcoes.items():
            print(f'{categoria}: {proporcao:.2f}% ')
        print('\n')
            
        print("Pressione ENTER para retornar ao menu")
        input()

    elif option == 4:
        maisBaratos, maisCaros = dezMaisCarosEMaisBaratos(dadosProdutos)
        print('\n10 PRODUTOS MAIS BARATOS\n')
        for produto in maisBaratos:
            print(f'ID: {produto['id']}, Nome: {produto['title']}, Categoria: {produto['categoryName']}, Preço: R$ {produto['price']:.2f}')
        print('\n10 PRODUTOS MAIS CAROS\n')
        for produto in maisCaros:
            print(f'ID: {produto['id']}, Nome: {produto['title']}, Categoria: {produto['categoryName']}, Preço: R$ {produto['price']:.2f}')

        print('\nPressione ENTER para retornar ao menu')
        input()

    elif option == 5:
        print("""
        Escolha uma categoria para gerar relatório HTML:
              
        [1] - Livros
        [2] - Esportes
        [3] - Moda
        [4] - Casa
        [5] - Eletrônicos
              """)
        
        categoriaEscolhida = int(input('Opção >>> '))
        if categoriaEscolhida not in range(1, 6):
            input('\nOpção inválida. Pressione ENTER para retornar ao MENU\n')
        else:
            relatorioPorCategoria(dadosProdutos, categoriaEscolhida)
            input('\nRelatório gerado. Pressione ENTER para retornar ao MENU\n')

    elif option == 6:
        relatorioTopDezBestSellers(dadosProdutos)
        input('\nRelatório gerado. Pressione ENTER para retornar ao MENU\n')
    
    elif option == 7:
        end = True

    else:
        print('Opção Inválida')


    
    
    