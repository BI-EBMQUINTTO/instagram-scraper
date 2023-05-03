# encoding: utf-8

from pathlib import Path
import time
import sys
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

import pandas as pd
from dotenv import dotenv_values

from bi_ebmquintto.instagram.instagram_bot import instagram_bot


def criar_pasta():
    path = Path.cwd()
    #pasta = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop', "Dados")
    pasta = os.path.join(path, "Dados")
    if os.path.isdir(pasta):
        print('O caminho {} existe'.format(pasta)) 
    else:
        try:
            os.makedirs(pasta)
        except OSError:
            pass

def extrair_comentarios(url_text: str, arquivo_text: str, cliques_text: str) -> int:
    """ Função para extrair os comentarios de um post do instagram"""

    # Acessar usuário e senha da conta do instagram
    #config  =  dotenv_values(r'C:\Users\EBMquintto\Desktop\app\config\credentials.env')
    config  =  dotenv_values(r"config\credentials.env")
    email = config['EMAIL']
    senha = config['PASSWORD']

    # Argumentos de entrada para extração 

    # Link do post
    link_do_post = url_text
    print(link_do_post)
   
    # Nome do arquivo para salvar os dados em excel
    nome_do_arquivo = arquivo_text
    
    # Numero de clicks no botão que mostra mais comentários
    num_de_clicks = int(cliques_text)
    
    #caminho_do_arquivo = str(Path.cwd() / 'Dados'/ nome_do_arquivo) + '.xlsx'
    criar_pasta()
    path = Path.cwd()
    caminho_pasta = os.path.join(path, "Dados")
    caminho_do_arquivo = caminho_pasta + "\\" + nome_do_arquivo + '.xlsx'
    
    
    
    # Configurar o chromedriver
    options = webdriver.ChromeOptions()
    service = Service(r'C:\Program Files (x86)\chromedriver\chromedriver.exe')
    options.add_argument("--start-maximized")
    #options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(service=service, options=options)
    
    # Acessar instagram
    driver.get("https://www.instagram.com/")

    #login
    time.sleep(3)
    bot = instagram_bot(driver)

    bot.login(email, senha)
    
    # Passar notificação
    time.sleep(5)
    #pipbot.passar_notificacao()
    time.sleep(5)
    print(link_do_post)
    bot.ir_para_post(link_do_post)
    time.sleep(5)

    bot.carregar_mais_comentarios(num_de_clicks)

    comentarios = [ comentario for comentario in bot.extrair_comentarios()]
    
    bot.close()
    # Cria o dataframe para armazenar os comentários
    df = pd.DataFrame.from_records(comentarios)

    # Escreve os dados inseridos no dataframe em um arquivo do Excel
    with pd.ExcelWriter(caminho_do_arquivo, mode='w', engine='openpyxl') as writer: 

        df.to_excel(writer, sheet_name='comentários', index=False)
    
    return len(comentarios)



