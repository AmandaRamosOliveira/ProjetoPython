import tkinter as tk
import pymysql
from Cadastrar import abrir_cadastro # aqui estou fazendo a importação da função do arquivo Cadastra.py
from BlocodeNotas import entrar

janela = tk.Tk()
janela.title("login")
janela.geometry("400x300") #Largura e Altura

def logar(email, senha):
    try:
        conexao = pymysql.connect(
            host='127.0.0.1', # Aqui vc vai colocar o seu host
            user='root', # aqui vc vai colocar o nome do seu user no banco de dados
            password='', # aqui vai ser a senha do seu banco de dados, se caso não tiver senha, deixe em branco
            database='cadastro', #aqui é o nome do banco de dados 
            port=3306, # aqui é a porta que o meu banco de dados está
            connect_timeout=5
        )
        cursor = conexao.cursor()
        sql = "SELECT * FROM cadastroinfor WHERE email = %s and senha= %s"
        valores = (email, senha)

        cursor.execute(sql, valores)
        resultado = cursor.fetchone()

        
        if resultado:
          print("Login bem-sucedido!")
          usuario_id = resultado[0]  
          entrar(janela, usuario_id)
        else:
            erroLabel=tk.Label(janela,text="Email/Nome ou senha incorretos.")
            erroLabel.pack()
    except pymysql.MySQLError as erro:
        print(f"Erro no MySQL: {erro}")
    finally:
        if conexao.open:
            cursor.close()
            conexao.close()
# Função do Botão Entrar

labelLogin = tk.Label(janela, text="Bem-vinda a tela de Login!")
labelLogin.pack(pady=30)

blocoEmail = tk.Label(janela, text="Nome do Usuário/Email:")
blocoEmail.pack()

email =tk.Entry(janela, width=30)
email.pack()

blocoSenha = tk.Label(janela, text="Senha:")
blocoSenha.pack()

senha = tk.Entry(janela, width=30, show='*')
senha.pack()

frame_botoes = tk.Frame(janela)
frame_botoes.pack(pady=20)

def autenticar():
    email_valor = email.get()
    senha_valor = senha.get()
    logar(email_valor, senha_valor)

botaoEntrar = tk.Button(frame_botoes, text="Entrar", command=autenticar, width=10)
botaoEntrar.pack(side="left", padx=10)

botaoCadastrar = tk.Button(frame_botoes, text="Cadastrar-se", command=lambda: abrir_cadastro(janela), width=10)
botaoCadastrar.pack(side="left", padx=10)

janela.mainloop()