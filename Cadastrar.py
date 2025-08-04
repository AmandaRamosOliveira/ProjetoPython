import tkinter as tk
import pymysql

def criar(email, senha): 
    try:
        conexao = pymysql.connect(
            #aqui vai ter que fazer o mesmo processo que ver no arquivo Login
            #vai ter que alterar as informações com forme o seu banco de dados.
            host='127.0.0.1', 
            user='root',
            password='',
            database='cadastro',
            port=3306,
            connect_timeout=5
        )
        cursor = conexao.cursor()
        sql = "INSERT INTO cadastroinfor (email, senha) VALUES (%s, %s)"
        valores = (email, senha)

        cursor.execute(sql, valores)
        conexao.commit()
        print("Cadastro realizado com sucesso!")

    except pymysql.MySQLError as erro:
        print(f"Erro ao conectar ou inserir no MySQL: {erro}")

    finally:
        if conexao.open:
            cursor.close()
            conexao.close()

def abrir_cadastro(janela=None):
    if janela:
        janela.withdraw()

    janela_cadastro = tk.Toplevel()
    janela_cadastro.title("Cadastro")
    janela_cadastro.geometry("400x300")

    labelCadastro = tk.Label(janela_cadastro, text="Bem-vinda à tela de Cadastro!")
    labelCadastro.pack(pady=30)

    blocoNome = tk.Label(janela_cadastro, text="Nome Usuário/Email:")
    blocoNome.pack()

    email = tk.Entry(janela_cadastro, width=30)
    email.pack()

    blocoSenha = tk.Label(janela_cadastro, text="Senha:")
    blocoSenha.pack()

    senha = tk.Entry(janela_cadastro, width=30, show='*')
    senha.pack()

    def criando():
        try:
            print("Botão clicado!")
            email_valor = email.get()
            senha_valor = senha.get()
            print(f"Email digitado: {email_valor}")
            print(f"Senha digitada: {senha_valor}")
            criar(email_valor, senha_valor)
        except Exception as erro:
            print(f"Erro ao clicar no botão Criar conta: {erro}")

    def voltar():
         janela_cadastro.destroy()
         if janela:
            janela.deiconify()


    botaoCriarConta = tk.Button(
        janela_cadastro,
        text="Criar conta",
        command=criando
    )
    botaoCriarConta.pack(pady=15)

    botaoVoltar = tk.Button( janela_cadastro, text= "já tenho cadastro", command =voltar)
    botaoVoltar.pack()
    