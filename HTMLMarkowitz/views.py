from django.shortcuts import render
import requests

def button(request):
    return render(request, 'home.html')

def output(request):
    import pandas as pd
    import numpy as np
    import pandas_datareader.data as web
    import mpld3
    from datetime import datetime

    start = datetime(2018, 1, 1)
    end = datetime(2018, 12, 31)
    acoes = ['PETR4.SA', 'ENBR3.SA', 'BBSE3.SA', 'VIVT4.SA', 'ITSA4.SA', 'ABCB4.SA', 'TAEE11.SA']
    dados = web.get_data_yahoo(acoes, start, end)['Adj Close']


    retorno_diario = dados.pct_change()
    retorno_anual = retorno_diario.mean() * 250


    cov_diaria = retorno_diario.cov()
    cov_anual = cov_diaria * 250


    retorno_carteira = []
    peso_acoes = []
    volatilidade_carteira = []
    sharpe_ratio = []

    numero_acoes = len(acoes)
    numero_carteiras = 100000

    np.random.seed(101)

    for cada_carteira in range(numero_carteiras):
        peso = np.random.random(numero_acoes)
        peso /= np.sum(peso)
        retorno = np.dot(peso, retorno_anual)
        volatilidade = np.sqrt(np.dot(peso.T, np.dot(cov_anual, peso)))
        sharpe = retorno / volatilidade
        sharpe_ratio.append(sharpe)
        retorno_carteira.append(retorno)
        volatilidade_carteira.append(volatilidade)
        peso_acoes.append(peso)

    carteira = {'Retorno': retorno_carteira,
                 'Volatilidade': volatilidade_carteira,
                 'Sharpe Ratio': sharpe_ratio}

    for contar,acao in enumerate(acoes):
        carteira[acao+' Peso'] = [Peso[contar] for Peso in peso_acoes]

    df = pd.DataFrame(carteira)

    colunas = ['Retorno', 'Volatilidade', 'Sharpe Ratio'] + [acao+' Peso' for acao in acoes]
    df = df[colunas]

    menor_volatilidade = df['Volatilidade'].min()
    maior_sharpe = df['Sharpe Ratio'].max()

    carteira_sharpe = df.loc[df['Sharpe Ratio'] == maior_sharpe]
    carteira_min_variancia = df.loc[df['Volatilidade'] == menor_volatilidade]


    data = "Essa é a carteira de Mínima Variância:" + '\n' + str(carteira_min_variancia.T)
    data = data + '\n'
    data = data + "Essa é a carteira com maior Sharpe Ratio:" + '\n' + str(carteira_sharpe.T)
    return render(request,'home.html',{'data':data})
