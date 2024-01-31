import requests
import matplotlib.pyplot as pl

# Chave de acesso à API da Alpha Vantage
api_key = "{chave_api}" # Limite de 25 requisições por dia

def salvar_dados_arquivo(dados, nome_arquivo):
    try:
        # Salva os dados em um arquivo
        with open(f'Finanças_{nome_arquivo}.txt', 'w') as file:
            file.write(dados)
    # Salva os dados em um arquivo
    except Exception as e:
        print(f'Erro ao salvar arquivo: {e}')
        
def plotar_grafico(dados):
    # Extrai as informações do dicionário de dados
    datas = [dado['Data'] for dado in dados]
    aberturas = [float(dado['Abertura']) for dado in dados]
    fechamentos = [float(dado['Fechado']) for dado in dados]
    
    # Plota o gráfico de aberturas e fechamentos
    pl.plot(datas, aberturas, label='Abertura')
    pl.plot(datas, fechamentos, label='Fechamento')
    
    # Configurações do gráfico
    pl.xlabel('Data')
    pl.ylabel('Valor')
    pl.title('Variação de Abertura e Fechamento')
    pl.legend()
    
    # Exibe o gráfico
    pl.show()


def extrair_acoes(nome_acao):
    # URL da API para obter informações da ação
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={nome_acao}&apikey={api_key}"
    
    try:
        # Faz a requisição à API
        response = requests.get(url)
        # Verifica se a requisição foi bem-sucedida
        if response.status_code == 200:
            # Extrai os dados da resposta JSON
            data = response.json()
            dados = data['Time Series (Daily)']
            
            # Transforma os dados em uma lista
            lista_dados = []
            for date, info in dados.items():
                lista_dados.append({
                    'Data': date,
                    'Abertura': info['1. open'],
                    'Baixa': info['3. low'],
                    'Fechado': info['4. close'],
                    'Volume': info['5. volume']
                })
            
            
            plotar_grafico(lista_dados)
            # Formata a lista de dados
            dadosFormatados = ('\n\n'.join([f'Data: {dado['Data']}\nAbertura: {dado['Abertura']}\nBaixa: {dado['Baixa']}\nFechado: {dado['Fechado']}\nVolume: {dado['Volume']}'for dado in lista_dados]))
            return dadosFormatados
        
        else:
            print(str(data['Information']))
            return None
    except Exception as e:
        # Caso a requisição não seja bem-sucedida, retorna o Erro
        print(str(data['Information']))
        return None
    
dadosFormatados = extrair_acoes('TRPL4.SAO')
if dadosFormatados is not None:
    salvar_dados_arquivo(dadosFormatados, 'TRPL4')