# -*- coding: utf-8 -*-
"""AnaliseRegressaoLogistica.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Llbj_02Kka1vIcMDH9_uLMkwg33xSJcv

# **REGRESSÃO LOGÍSTICA BINÁRIA**
"""

import numpy as np
import pandas as pd

# Carrega a base de dados
from google.colab import files
uploaded = files.upload()

doenca_pre = pd.read_csv('casos_obitos_doencas_preexistentes.csv',
                    sep=';', encoding='utf-8')

"""## **ANÁLISE INICIAL**"""

doenca_pre.head()

doenca_pre.shape

"""**Objetivo: Analisar se existe uma tendência de óbito entre pessoas do sexo feminino e masculino.**"""

doenca_pre['cs_sexo'].value_counts()

"""Valores Missing (NAN)"""

doenca_pre.isnull().sum()

# Excluir valor NAN de cs_sexo
doenca_pre.dropna(subset=['cs_sexo'], inplace=True)

# Excluir Ignorado
relacao = doenca_pre.loc[doenca_pre.cs_sexo != 'IGNORADO']

# Excluir Indefinido
relacao = relacao.loc[relacao.cs_sexo != 'INDEFINIDO']

relacao['cs_sexo'].value_counts()

import plotly.express as px

px.pie(relacao, names='cs_sexo')

"""**Análise dos óbitos**"""

relacao['obito'].value_counts()

px.pie(relacao, names='obito')

"""**Análise da classificação dos atributos**"""

relacao.dtypes

"""**Renomeando os registros da variável obito**"""

relacao['obito'] = relacao['obito'].replace({0:'nao', 1:'sim'})

relacao['obito'].value_counts()

"""**Transformando em variáveis categóricas**"""

relacao['cs_sexo'] = relacao['cs_sexo'].astype('category')

relacao['obito'] = relacao['obito'].astype('category')

relacao.dtypes

"""## **Modelo 1: Uma variável independente**

Variável dependente binária (dicotômica).

Categorias mutuamente exclusivas (uma pessoa não pode estar em duas situações).

Independência das observações (sem medidas repetidas).
"""

import statsmodels.api as sm
import statsmodels.formula.api as smf

"""Análise do modelo

Estatisticamente significativo: p <= 0,05

Estatisticamente não é significativo: p > 0,05

Análise da Ausência de outliers e pontos de alavancagem

Deve estar entre -3 e 3
"""

modelo1 = smf.glm(formula='obito ~ cs_sexo', data=relacao, family = sm.families.Binomial()).fit()
print(modelo1.summary())

# Razão de chance com Intervalo de confiança de 95%
razao = np.exp(modelo1.params[1])
razao

"""CONCLUSÃO:

Estatisticamente, com intervalo de confiança de 95%, os homens tem 63,97% menos chances de sobrevivência do que mulheres.

"""

coef = 1/razao
coef

"""CONCLUSÃO:

Estatisticamente, com intervalo de confiança de 95%,
a chance de uma pessoa do sexo masculino ir a óbito é
1,56 vezes maior do que a chance de uma pessoa do sexo feminino.

## **Modelo 2: Mais de uma variável independente**

Diabetes e sexo
"""

import statsmodels.api as sm
import statsmodels.formula.api as smf

relacao['diabetes'].value_counts()

import plotly.express as px

px.pie(relacao, names="diabetes")

relacao2 = relacao.loc[relacao.diabetes != 'IGNORADO']

px.pie(relacao2, names="diabetes")

# Antes da exclusão de ignorados em diabetes
px.pie(relacao, names="obito")

# Depois da exclusão de ignorados em diabetes
px.pie(relacao2, names="obito")

relacao2.dtypes

relacao2['diabetes'] = relacao2['diabetes'].astype('category')

"""### **Criação do modelo 2**

Ausência de Multicolinearidade entre as variáveis independentes

Análise do modelo

Estatisticamente significativo: p <= 0,05

Estatisticamente não é significativo: p > 0,05

Análise da Ausência de outliers e pontos de alavancagem

Deve estar entre -3 e 3
"""

modelo2 = smf.glm(formula='obito ~ cs_sexo + diabetes', data=relacao2, family = sm.families.Binomial()).fit()
print(modelo2.summary())

modelo2.params

# Chance com Intervalo de confiança de 95% DOS HOMENS COM RELAÇÃO ÀS MULHERES

chance = 1 / (np.exp(modelo2.params[1]))
chance

# Chance com Intervalo de confiança de 95% DOS DIABÉTICOS COM RELAÇÃO AOS NÃO DIABÉTICOS
chance = 1 / (np.exp(modelo2.params[2]))
chance

"""CONCLUSÃO:

O resultado da diabetes está inconsistente devido a presença enorme de
dados ignorados.

## **Modelo 3: Variável independente numérica**

Variável Idade
"""

relacao3 = doenca_pre.loc[doenca_pre.nome_munic == 'Santos']

relacao3.head()

relacao3.shape

relacao3.dtypes

"""Valores Missing (NAN)"""

relacao3.isnull().sum()

# Excluir valores missing
relacao3.dropna(subset=['idade'], inplace=True)

import matplotlib.pyplot as plt
plt.scatter(relacao3.idade,relacao3.obito)
plt.xlabel('IDADE')
plt.ylabel('ÓBITO')
plt.grid(False)
plt.show()

"""**Ausência de multicolinearidade**"""

np.corrcoef(relacao3.obito, relacao3.idade)

"""### **Criação do modelo 3 com StatsModels**"""

import statsmodels.api as sm
import statsmodels.formula.api as smf

modelo3 = smf.glm(formula='obito ~ idade', data=relacao3, family = sm.families.Binomial()).fit()
print(modelo3.summary())

# Razão de chance com Intervalo de confiança de 95%
np.exp(modelo3.params[1])

"""CONCLUSÃO:

Para cada ano mais velho, o indivíduo fica com 1,12 das chances de outro indivíduo com um ano a menos.

### **Criação do modelo 3 com Sklearn**
"""

from sklearn.linear_model import LogisticRegression

relacao3.head()

# Criação das variávies x (independente) e y (dependente)
# Transformação de X para o formato de matriz.
x = relacao3.iloc[:, 2].values
y = relacao3.iloc[:, 6].values

x

y

# Transformação de X para o formato de matriz
x = x.reshape(-1,1)
x

modelo3s = LogisticRegression()
modelo3s.fit(x, y)

modelo3s.coef_

modelo3s.intercept_

# Razão de chance com Intervalo de confiança de 95%
np.exp(modelo3s.coef_)

"""CONCLUSÃO:

Para cada ano mais velho, o indivíduo fica com 1,12 das chances de outro indivíduo com um ano a menos.
"""

plt.scatter(x, y)
# Geração de novos dados para gerar a função sigmoide
x_teste = np.linspace(0, 130, 100)

def model(w):   # função sigmoide
    return 1 / (1 + np.exp(-w))
# Geração de previsões (variável r) e visualização dos resultados
previsao = model(x_teste * modelo3s.coef_ + modelo3s.intercept_).ravel()
plt.plot(x_teste, previsao, color = 'red');

"""**Testando o modelo com os resultados de outra cidade (Jundiaí)**"""

jundiai = doenca_pre.loc[doenca_pre.nome_munic == 'Jundiaí']

jundiai.head()

jundiai.shape

"""Valores Missing (NAN)"""

jundiai.isnull().sum()

# Excluir valores missing
jundiai.dropna(subset=['idade'], inplace=True)

# Mudança dos dados para formato de matriz
idade = jundiai.iloc[:, 2].values
idade = idade.reshape(-1, 1)

idade

# Previsões e geração de nova base de dados com os valores originais e as previsões
previsoes_teste = modelo3s.predict(idade)
previsoes_teste

jundiai['previsões'] = previsoes_teste

jundiai.head(15)

jundiai = jundiai.drop(columns=['obito', 'previsões']).assign(obito=jundiai['obito'], previsoes=jundiai['previsões'])

jundiai.head(30)

jundiai['resultado'] = jundiai['obito'] + jundiai['previsoes']

jundiai.head(25)

jundiai["resultado"] = jundiai["resultado"].replace({0:"acertou", 1:"errou", 2:"acertou"})
jundiai.head(25)

jundiai['resultado'].value_counts()

px.pie(jundiai, names="resultado")

jundiai.to_csv('resultados_jundiai.csv', encoding = 'iso-8859-1', index = False)