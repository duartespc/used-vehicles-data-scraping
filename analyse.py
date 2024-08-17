import pdb
import numpy as np
import pandas as pd
import matplotlib as mpl 
## agg backend is used to create plot as a .png file
mpl.use('agg')
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf

def cilindradaXpreco(data, modelo=None):	

	# Substitui as strings vazias por NaN, para que depois possamos eliminá-las
	data['modelo'].replace('', np.nan, inplace=True)
	data['modelo'].replace(' ', np.nan, inplace=True)

	data['cilindrada'].replace('', np.nan, inplace=True)
	data['cilindrada'].replace(' ', np.nan, inplace=True)
	data['cilindrada'].replace('0', np.nan, inplace=True)

# Substitui as strings vazias por NaN, para que depois possamos eliminá-las
	data['preco'].replace('.', '', inplace=True)
	data['preco'].replace(',', '', inplace=True)

	# Substitui as strings vazias por NaN, para que depois possamos eliminá-las
	data['preco'].replace('', np.nan, inplace=True)
	data['preco'].replace(' ', np.nan, inplace=True)

	# Retira motos acima de 1000 cilindradas pois não temos a informação precisa
	# TODO: Verificar a cilindrada atrvés de outras informações, como título, modelo e descrição do anúncio
	data['cilindrada'] = data['cilindrada'].replace('Acima de 1.000', np.nan)

	# Exclui todas as linhas em que possuam NaN nas colunas 'preco' e modelo
	data.dropna(subset=['preco', 'modelo', 'cilindrada'], inplace=True)

	if modelo != None:
		# Seleciona as motos com o modelo definido por 'modelo'
		data = data.loc[data['modelo'] == modelo]

	fig, ax = plt.subplots()

	cilindrada = data['cilindrada'].astype('int', copy=True)
	preco = data['preco'].astype('int', copy=True)

	ax.scatter(cilindrada, preco, s=30)
	
	if modelo == None:
		ax.set(xlabel='Cilindrada', ylabel='Preço',
    		   title='Cilindrada x Preço (todos os modelos)')	
	else:
		ax.set(xlabel='quilometros', ylabel='Preço',
    		   title='quilometros x Preço ('+modelo+')')	
	ax.grid()

	fig.savefig("cilindradaXpreco.png")
	plt.show()


def quilometrosXpreco(data, modelo):
	# Substitui as strings vazias por NaN, para que depois possamos eliminá-las
	data['modelo'].replace('', np.nan, inplace=True)
	data['modelo'].replace(' ', np.nan, inplace=True)

	# Substitui os pontos finais por virgulas
	#data['quilometros'].replace('.', '', inplace=True)
	data['quilometros'].replace('', np.nan, inplace=True)
	data['quilometros'].replace(' ', np.nan, inplace=True)
	data['quilometros'].replace('0', np.nan, inplace=True)

	# Retira os pontos nos numeros > 1000
	data['preco'].replace('.', '', inplace=True)
	data['preco'].replace(',', '', inplace=True)


	# Substitui as strings vazias por NaN, para que depois possamos eliminá-las
	data['preco'].replace('', np.nan, inplace=True)
	data['preco'].replace(' ', np.nan, inplace=True)
	#print('--'+data['modelo'][0]+'--')

	# Exclui todas as linhas em que possuam NaN nas colunas 'preco' e modelo
	data.dropna(subset=['preco', 'modelo', 'quilometros'], inplace=True)

	# Seleciona as motos com o modelo definido por 'modelo'
	data = data.loc[data['modelo'] == modelo]

	# Tratar outliers
	# TODO: Implementar um método de detecção de outliers mais eficaz
	#data = data[data['quilometros'] < 200000]
	#data = data[data['quilometros'] > 100]

	fig, ax = plt.subplots()

	quilometros = data['quilometros'].astype('int', copy=True)
	preco = data['preco'].astype('int', copy=True)

	ax.scatter(quilometros, preco)
	
	ax.set(xlabel='quilometros', ylabel='Preço',
    	   title='quilometros x Preço ('+modelo+')')	
	ax.grid()

	fig.savefig("graficos/quilometrosXpreco.png")
	plt.show()	


def anoXpreco(data, modelo):		
	# Substitui as strings vazias por NaN, para que depois possamos eliminá-las
	data['modelo'].replace('', np.nan, inplace=True)
	data['modelo'].replace(' ', np.nan, inplace=True)

	data['ano'].replace('', np.nan, inplace=True)
	data['ano'].replace(' ', np.nan, inplace=True)
	data['ano'].replace('0', np.nan, inplace=True)

	# Retira os pontos nos numeros > 1000
	data['preco'].replace('.', '', inplace=True)
	data['preco'].replace(',', '', inplace=True)

	# Substitui as strings vazias por NaN, para que depois possamos eliminá-las
	data['preco'].replace('', np.nan, inplace=True)
	data['preco'].replace(' ', np.nan, inplace=True)
	#print('--'+data['modelo'][0]+'--')


	# Exclui todas as linhas em que possuam NaN nas colunas 'preco' e modelo
	data.dropna(subset=['preco', 'modelo', 'ano'], inplace=True)

	# Seleciona as motos com o modelo definido por 'modelo'
	data = data.loc[data['modelo'] == modelo]

	fig, ax = plt.subplots()

	ano = data['ano'].astype('int', copy=True)
	preco = data['preco'].astype('int', copy=True)

	ax.scatter(ano, preco)
	
	ax.set(xlabel='Ano', ylabel='Preço',
    	   title='Ano x Preço ('+modelo+')')	
	ax.grid()

	fig.savefig("graficos/anoXpreco.png")
	plt.show()	



"""

Constrói gráficos do tipo boxplot levando em consideração os modelos x preços e salva como .png
@param data dataframe contendo os dados
@param numModelos quantidade de boxplots na imagem.
@return none

"""
def modeloXpreco(data, numModelos):


	# Substitui as strings vazias por NaN, para que depois possamos eliminá-las
	data['modelo'].replace('', np.nan, inplace=True)
	data['modelo'].replace(' ', np.nan, inplace=True)
	#print('--'+data['modelo'][0]+'--')

	# Exclui todas as linhas em que possuam NaN nas colunas 'preco' e modelo
	data.dropna(subset=['preco', 'modelo'], inplace=True)

	
	# Percorre os valores únicos de modelos de motos
	modelNames = []
	modelPrices = []
	for modelo in data.modelo.unique():

		modelNames.append(modelo)

		# Obtém todos os preços das motos que são deste modelo
		precos = data.loc[data['modelo'] == modelo]['preco'].tolist()
		modelPrices.append(precos)


	# Ordena as categorias por quantidade de motos
	newModelNames = []
	newModelPrices = []
	indexCount = []
	for index, item in enumerate(modelPrices):
		maior = float('-Inf')
		indexMaior = 0
		for index2, item2 in enumerate(modelPrices):
			size = len(item2)
			if size > maior:
				maior = size
				indexMaior = index2

		newModelNames.append(modelNames[indexMaior])
		newModelPrices.append(modelPrices[indexMaior])
		del modelNames[indexMaior]
		del modelPrices[indexMaior]

	#print(modelNames)

	# Cria uma instância de figura. A largura da imagem é relacionada ao número de boxplots
	fig = plt.figure(1, figsize=(numModelos*4, 6))

	# Cria uma instância de eixos
	ax = fig.add_subplot(111)	

	# Cria o boxplot
	bp = ax.boxplot(newModelPrices[:numModelos])

	ax.set_xticklabels(newModelNames[:numModelos])
	
	# Salva a Figura
	fig.savefig('modeloXpreco.png', bbox_inches='tight')



def modelo_linear(x, results):
	y = 0
	params = list(results.params)

	# O vetor x tem 1 elemento a menos. Portanto, devemos somar o coeficiente livre da função após o looping
	for i in range(len(x)):
		y += x[i]*params[i+1]

	# Somando o coeficiente livre
	y += params[0]

	return y

def analytic():
	print("Analisando os dados")

	# Carregando os dados
	data = pd.read_csv('motas_olx.csv')
	modelo = 'BWs'
	print(data)

	#pdb.set_trace()

	# Vamos gerar os gráficos
	#modeloXpreco(data, 4)
	anoXpreco(data, modelo)
	quilometrosXpreco(data, modelo)
	#cilindradaXpreco(data, 'MT-07')


if __name__ == '__main__':
	#getInformation()
	analytic()


