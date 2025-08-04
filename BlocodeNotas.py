import tkinter as tk
import pymysql

def entrar(janela=None, usuario_id=None):
    if janela:
        janela.withdraw()

    janela_bloco = tk.Toplevel()
    janela_bloco.title("Bloco de notas")
    janela_bloco.geometry("400x300")

    def salvar(conteudo, janela_criar, entradaNotas):
        if conteudo:
            #aqui vai ter que fazer o mesmo processo que ver no arquivo Login
            #vai ter que alterar as informações com forme o seu banco de dados.
            try:
                conexao = pymysql.connect(
                    host='127.0.0.1',
                    user='root',
                    password='',
                    database='cadastro',
                    port=3306
                )
                cursor = conexao.cursor()
                sql = "INSERT INTO notas (usuario_id, conteudo) VALUES (%s, %s)"
                cursor.execute(sql, (usuario_id, conteudo))
                conexao.commit()
            except pymysql.MySQLError as erro:
                print(f"Erro ao salvar nota: {erro}")
            finally:
                cursor.close()
                conexao.close()
            entradaNotas.delete("1.0", tk.END)
            janela_criar.destroy()
            janela_bloco.deiconify()

    def verNotas():
        janela_bloco.withdraw()

        janela_notas = tk.Toplevel()
        janela_notas.title("Notas Salvas")
        janela_notas.geometry("400x600")

        try:
            #aqui vai ter que fazer o mesmo processo que ver no arquivo Login
            #vai ter que alterar as informações com forme o seu banco de dados.
            conexao = pymysql.connect(
                host='127.0.0.1',
                user='root',
                password='',
                database='cadastro',
                port=3306
            )
            cursor = conexao.cursor()
            sql = "SELECT id, conteudo FROM notas WHERE usuario_id = %s"
            cursor.execute(sql, (usuario_id,))
            resultados = cursor.fetchall()
        except pymysql.MySQLError as erro:
            print(f"Erro ao buscar notas: {erro}")
            return
        finally:
            cursor.close()
            conexao.close()

        for nota_id, conteudo in resultados:
            texto = tk.Text(janela_notas, width=40, height=5)
            texto.insert(tk.END, conteudo)
            texto.config(state="disabled")
            texto.pack(pady=5)

            frame_botoes = tk.Frame(janela_notas)
            frame_botoes.pack()

            botaoEditar = tk.Button(
                frame_botoes, text="Editar",
                command=lambda nid=nota_id, c=conteudo: editar_nota(nid, c, janela_notas)
            )
            botaoEditar.pack(side="left", padx=5)

            botaoApagar = tk.Button(
                frame_botoes, text="Apagar",
                command=lambda nid=nota_id: apagarNotas(nid, janela_notas)
            )
            botaoApagar.pack(side="left", padx=5)

        def voltar():
            janela_notas.destroy()
            janela_bloco.deiconify()

        botaoVoltar = tk.Button(janela_notas, text="Voltar", command=voltar)
        botaoVoltar.pack(pady=10)

    def apagarNotas(nid, janela_notas):
            #aqui vai ter que fazer o mesmo processo que ver no arquivo Login
            #vai ter que alterar as informações com forme o seu banco de dados.
        try:
            conexao = pymysql.connect(
                host='127.0.0.1',
                user='root',
                password='',
                database='cadastro',
                port=3306
            )
            cursor = conexao.cursor()
            sql = "DELETE FROM notas WHERE id = %s"
            cursor.execute(sql, (nid,))
            conexao.commit()
            print("Nota apagada com sucesso.")
            janela_notas.destroy()
            verNotas()
        except pymysql.MySQLError as erro:
            print(f"Erro ao apagar nota: {erro}")
        finally:
            cursor.close()
            conexao.close()

    def editar_nota(nid, textoOriginal, janela_notas):
        janelaEditar = tk.Toplevel()
        janelaEditar.title("Editar Nota")

        campo = tk.Text(janelaEditar, width=49, height=10)
        campo.insert(tk.END, textoOriginal)
        campo.pack(pady=10)

        def salvar_edicao():
            novo_conteudo = campo.get("1.0", tk.END).strip()
            
            #aqui vai ter que fazer o mesmo processo que ver no arquivo Login
            #vai ter que alterar as informações com forme o seu banco de dados.
            try:
                conexao = pymysql.connect(
                    host='127.0.0.1',
                    user='root',
                    password='',
                    database='cadastro',
                    port=3306
                )
                cursor = conexao.cursor()
                sql = "UPDATE notas SET conteudo = %s WHERE id = %s"
                cursor.execute(sql, (novo_conteudo, nid))
                conexao.commit()
                print("Nota atualizada com sucesso.")
                janelaEditar.destroy()
                janela_notas.destroy()
                verNotas()
            except pymysql.MySQLError as erro:
                print(f"Erro ao atualizar nota: {erro}")
            finally:
                cursor.close()
                conexao.close()

        botaoSalvar = tk.Button(janelaEditar, text="Salvar", command=salvar_edicao)
        botaoSalvar.pack(pady=5)

    def criarNotas():
        janela_bloco.withdraw()

        janela_criar = tk.Toplevel()
        janela_criar.title("Criar Notas")
        janela_criar.geometry("500x450")

        entradaNotas = tk.Text(janela_criar, width=30, height=15)
        entradaNotas.pack(pady=20)

        frame_botoes = tk.Frame(janela_criar)
        frame_botoes.pack(pady=10)

        botaoSalvar = tk.Button(
            frame_botoes,
            text="Salvar",
            command=lambda: salvar(
                entradaNotas.get("1.0", tk.END).strip(),
                janela_criar,
                entradaNotas
            )
        )
        botaoSalvar.pack(side="left", padx=10)

        botaoApagar = tk.Button(
            frame_botoes,
            text="Apagar",
            command=lambda: entradaNotas.delete("1.0", tk.END)
        )
        botaoApagar.pack(side="left", padx=10)

        def voltar():
            janela_criar.destroy()
            janela_bloco.deiconify()

        botaoVoltar = tk.Button(frame_botoes, text="Voltar", command=voltar)
        botaoVoltar.pack(side="left", padx=10)

    def logout():
        janela_bloco.destroy()
        if janela:
            janela.deiconify()

    # Botões principais
    botaoCriar = tk.Button(janela_bloco, text="Criar notas", command=criarNotas)
    botaoCriar.pack(pady=25)

    botaoVerNotas = tk.Button(janela_bloco, text="Ver notas", command=verNotas)
    botaoVerNotas.pack(pady=25)

    botaoLogout = tk.Button(janela_bloco, text="Sair", command=logout)
    botaoLogout.pack(pady=25)
