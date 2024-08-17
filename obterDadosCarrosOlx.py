import datetime
from operator import mod
import pdb
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
import numpy as np
import pandas as pd
from datetime import datetime


# Obtém a URL
def getUrl(indice_pagina):
	'''
	Obtém a URL que abriga os anúncios analisados

	param int paginacao: O número da paginação
	'''
	return "https://www.olx.pt/d/carros-motos-e-barcos/carros/aixam/?page="+str(indice_pagina)


def dictToCsv(item_dic):
	'''	
	Coloca o conjunto de daodos no formato correto e o salva em um arquivo '.csv'
	
	param dara_frame item_dic: O conjunto de dados contendo todos os anúncios
	'''
	csv = []
	print(item_dic)
	# Salvando os itens em um csv
	for i in range(len(item_dic)):
		csv.append([])

		if 'marca' in item_dic[i]:
			csv[i].append(item_dic[i]['marca'])
		else:
			csv[i].append(float('NaN'))

		if 'modelo' in item_dic[i]:
			csv[i].append(item_dic[i]['modelo'])
		else:
			csv[i].append(float('NaN'))

		if 'ano' in item_dic[i]:
			csv[i].append(item_dic[i]['ano'])
		else:
			csv[i].append(float('NaN'))

		if 'quilometros' in item_dic[i]:
			csv[i].append(item_dic[i]['quilometros'])
		else:
			csv[i].append(float('NaN'))

		if 'cilindrada' in item_dic[i]:
			csv[i].append(item_dic[i]['cilindrada'])
		else:
			csv[i].append(float('NaN'))

		if 'combustivel' in item_dic[i]:
			csv[i].append(item_dic[i]['combustivel'])
		else:
			csv[i].append(float('NaN'))

		if 'portas' in item_dic[i]:
			csv[i].append(item_dic[i]['portas'])
		else:
			csv[i].append(float('NaN'))

		if 'matricula' in item_dic[i]:
			csv[i].append(item_dic[i]['matricula'])
		else:
			csv[i].append(float('NaN'))

		if 'url' in item_dic[i]:
			csv[i].append(item_dic[i]['url'])
		else:
			csv[i].append(float('NaN'))

		if 'preco' in item_dic[i]:
			csv[i].append(item_dic[i]['preco'])
		else:
			csv[i].append(float('NaN'))

		if 'data' in item_dic[i]:
			csv[i].append(item_dic[i]['data'])
		else:
			csv[i].append(float('NaN'))

		if 'data_inspecao' in item_dic[i]:
			csv[i].append(item_dic[i]['data_inspecao'])
		else:
			csv[i].append(float('NaN'))		

	header = ['marca', 'modelo', 'ano', 'combustivel', 'quilometros', 'cilindrada','portas', 'matricula', 'url', 'preco', 'data', 'data_inspecao']
	pd.DataFrame(csv).to_csv('carros_olx.csv', header=header, index=False)


def getInformation():
	print("Obtendo os dados")

	chrome = webdriver.Chrome()

	chrome.get(getUrl(1))
	
	last_button = chrome.find_elements(By.CLASS_NAME, 'css-1mi714g')
    #if there is only one page, then this gives an error so we need to check for that
	try:
		print("Encontradas várias páginas: ", last_button[len(last_button)-1].text)
		last_button_number = last_button[len(last_button)-1].text
		last_button_number = int(last_button_number)
	except:
		last_button_number = int(1)


	# Percorre a paginação da categoria para obter os links de todos os anúncios
	url_list = []
	for i in (range(last_button_number)):

		# Obtem a página da categoria na paginação i
		chrome.get(getUrl(i))

		itens = chrome.find_elements(By.CLASS_NAME, 'css-1bbgabe')

		for item in itens:
			item_link = item.get_attribute('href')
			url_list.append(item_link)


	"""
	* Agora que temos todas as URLS dos anúncios, vamos acessar cada um individualmente e obter as 
	* informações que serão analisadas.
	"""
	item_dic = {}
	item_index = 0
	for i, url in enumerate(url_list):	

		# Verifica se a palavra 'olx.pt' existe no 'item', para prevenir propaganda
		if "olx.pt" not in url:
			continue

		chrome.get(url)

		marca = ""
		modelo = ""
		ano = ""
		quilometros = ""
		cilindrada = ""
		combustivel = ""
		portas = ""
		matricula = ""

		try:
			descricao = chrome.find_element(By.XPATH,"//meta[@name='description']").get_attribute("content")
			
			# Encontrar o preço - Ou é um numero ou diz 'Troca' - o resto é a descrição do anúncio, não interessa
			palavras = descricao.split(':')
			preco = palavras[0]
		except:
			preco = float('NaN')
			
		data = chrome.find_element(By.CLASS_NAME,'css-19yf5ek').get_attribute('textContent')

		# Iterar pelos campos e 'descobrir' o que representa (preço, localizaçao, modelo, etc...)
		valores_textuais = chrome.find_elements(By.XPATH, "//*[@class='css-xl6fe0-Text eu5v0x0']")
		for valor in valores_textuais:			
			texto = valor.get_attribute('textContent')

			# texto = 'Quilómetros: 270.000 km'
			if "Quilómetros" in texto:
				quilometros = texto[13:]
			# texto = 'Modelo: Mégane'
			if "Modelo" in texto:
				modelo = texto[8:]
			if "Cilindrada" in texto:
				cilindrada = texto[12:]
			if "Combustível" in texto:
				combustivel = texto[13:]
			if "Tipo de Caixa" in texto:
				caixa = texto[15:]
			if "Ano" in texto:
				ano = texto[5:]
			if "Matrícula" in texto:
				matricula = texto[11:]
			if "Portas" in texto:
				portas = texto[8:]

		# Descobrir a marca a partir da categoria, descrito nos links
		links = chrome.find_elements(By.CLASS_NAME, 'css-7dfllt')

		contador = 0
		for link in links:
			textContent = link.get_attribute('textContent')
			if textContent == "Carros":
				if (contador + 1) <= len(textContent)-1:
					marca = links[contador+1].get_attribute('textContent')
					break
			contador += 1
			
		#datetime string
		now = datetime.now() 
		datetime_string = str(now.strftime("%d%m%Y_%H%M"))
		
		item_dic[item_index] = {}

		item_dic[item_index]['marca'] = marca
		item_dic[item_index]['modelo'] = modelo
		item_dic[item_index]['ano'] = ano
		item_dic[item_index]['quilometros'] = quilometros
		item_dic[item_index]['cilindrada'] = cilindrada
		item_dic[item_index]['combustivel'] = combustivel	
		item_dic[item_index]['portas'] = portas
		item_dic[item_index]['matricula'] = matricula
		item_dic[item_index]['matricula'] = matricula
		item_dic[item_index]['data_inspecao'] = datetime_string


		# Insere a URL nos atributos do anúncio para futuras inspeções manuais
		item_dic[item_index]['data'] = data
		item_dic[item_index]['url'] = url
		item_dic[item_index]['preco'] = preco

		print(item_dic[item_index])


		item_index += 1
		

	print(len(item_dic))
	dictToCsv(item_dic)

	#np.save('dataset.npy', item_dic)
	chrome.quit()


if __name__ == '__main__':
	getInformation()
