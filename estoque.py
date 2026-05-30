import pyodbc
from datetime import date

conexao = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=notbu645;"
    "DATABASE=estoque;"
    "Trusted_Connection=yes;"
)
cursor = conexao.cursor()
def cadastrar():
    
   

    try:
        nome_produto=input("digite o nome do produto:").strip().lower()
        quantidade_produto=int(input("digite a quantidade do produto:"))
        valor_produto=float(input("digite o preço do produto"))
        data_cadastro = date.today().strftime("%Y-%m-%d")
        cursor.execute(
        "SELECT * FROM produtos WHERE nome = ?",
        (nome_produto,)
        )

        produto = cursor.fetchone()

        if produto:
            print("Produto já está cadastrado")
            return

        cursor.execute(
       "INSERT INTO produtos (nome, quantidade, preco,data_cadastro) VALUES (?, ?, ?,?)",(nome_produto,quantidade_produto,valor_produto,data_cadastro))
        conexao.commit()

        print("Produto cadastrado!")
    except ValueError:
        print("algum dado foi inserido errado")

def listar():
    cursor.execute("SELECT * FROM produtos")

    for linha in cursor.fetchall():

         print( f"ID:{linha[0]}| "
    f"Produto:{linha[1]}| "
    f"Qtd:{linha[2]}| "
    f"preço:R${str(linha[3]).replace(".", ",")}|"
    f"data:{linha[4]}")

def verqnt_estoque():
    try:
        print("escolha 1 para ver os 3 produtos com menor quantidade")
        print("escolha 2 para ver os 3 produtos com maior quantidade")

        Escolhaestoque = int(input("escolha: "))

        if Escolhaestoque == 1:

            cursor.execute("""
                SELECT TOP 3 *
                FROM produtos
                ORDER BY quantidade ASC
            """)

            menor = cursor.fetchall()

            print("Produtos com menor estoque:")

            for linha in menor:
                print(
                    f"Produto:{linha[1]} | "
                    f"Qtd:{linha[2]}"
                )

        elif Escolhaestoque == 2:

            cursor.execute("""
                SELECT TOP 3 *
                FROM produtos
                ORDER BY quantidade DESC
            """)

            maior = cursor.fetchall()

            print("Produtos com maior estoque:")

            for linha in maior:
                print(
                    f"Produto:{linha[1]} | "
                    f"Qtd:{linha[2]}"
                )

        else:
            print("Opção inválida")

    except ValueError:
        print("Digite apenas números.")

def datas_antigas():
    cursor.execute("""
                SELECT TOP 3 *
                FROM produtos
                ORDER BY data_cadastro ASC
            """) 
    produto=cursor.fetchall()
    for linha in produto:
        print( f"Produto:{linha[1]} | "
        f"data:{linha[4]}")             

def buscar_produto():
    try:
        nome = input("Digite o nome do produto: ").strip().lower()

        cursor.execute(
        "SELECT * FROM produtos WHERE nome LIKE ?",
        (f"%{nome}%",)
        )

        produtos = cursor.fetchall()
        if not produtos:
            print("Nenhum produto encontrado.")
            return
        for linha in produtos:

             print(

             
            f"ID:{linha[0]} | "
            f"Produto:{linha[1]} | "
            f"Qtd:{linha[2]} | "
            f"Preço:R$ {str(linha[3]).replace('.', ',')}"
                 )
       
    except ValueError:
        print("o valor que você digitou é incompativel")
def deletar():
    listar() 
    try:
        deletar=int(input("escolha o id do produto que você quer excluir "))
        cursor.execute( "select nome from produtos WHERE id = ?",(deletar,)
     )
        produto = cursor.fetchone()
        if not produto :
            print("Produto não encontrado.")
            return
        nomeId=produto[0]
        cursor.execute(
            "DELETE FROM produtos WHERE id = ?",
            (deletar,)
        )
        conexao.commit()
        print(f"produto  {nomeId}  foi deletado")  
    except ValueError:
        print("dados invalido ")

def atualizar_preco():
    listar()
    try:
        id_produto = int(input("Digite o ID do produto: "))
        novo_preco = float(input("Digite o novo preço: "))
        cursor.execute( " SELECT * FROM produtos WHERE id = ?",
         (id_produto,))
          

        produto = cursor.fetchone()

        if not produto:

         print("Produto não encontrado.")
         return
        cursor.execute("UPDATE produtos SET preco = ? WHERE id = ?",
        (novo_preco, id_produto))
        

        conexao.commit()


        print("Preço atualizado!") 
    except ValueError:
        print("dados incorretos ")     
def atualizar_nome():
    listar()
    try:
        id_produto = int(input("Digite o ID do produto: ")).strip().lower()
        novo_nome = input("Digite o novo nome: ")
        
        cursor.execute ( " SELECT * FROM produtos WHERE id = ?",
         (id_produto,)
        )   
       

        produto = cursor.fetchone()

        if not produto:

         print("Produto não encontrado.")
         return
        cursor.execute(
        "UPDATE produtos SET nome = ? WHERE id = ?",
        (novo_nome, id_produto)
        )

        conexao.commit()


        print("nome atualizado!") 
    except ValueError:
        print("dados incorretos")      
def atualizar_quantidaeEstoque():
    listar()

    try:
        id_produto = int(input("Digite o ID do produto: "))

        cursor.execute("SELECT nome, quantidade FROM produtos WHERE id = ?",
            (id_produto,))
            
        

        produto = cursor.fetchone()

        if not produto:
            print("Produto não encontrado.")
            return

        nome = produto[0]
        quantidade_atual = produto[1]

        print(f"\nProduto: {nome}")
        print(f"Quantidade atual: {quantidade_atual}")

        tipo = int(input(
            "\n1 - Entrada de estoque\n"
            "2 - Saída de estoque\n"
            "Escolha: "
        ))

        quantidade = int(input("Quantidade: "))

        if tipo == 1:
            nova_quantidade = quantidade_atual + quantidade

        elif tipo == 2:
            if quantidade > quantidade_atual:
                print("Estoque insuficiente!")
                return

            nova_quantidade = quantidade_atual - quantidade

        else:
            print("Opção inválida.")
            return

        cursor.execute(
            "UPDATE produtos SET quantidade = ? WHERE id = ?",
            (nova_quantidade, id_produto)
        )

        conexao.commit()

        print(f"Nova quantidade: {nova_quantidade}")
    except ValueError:
        print("dados invalidos") 

def buscar_qtd():
    try:
        quantidade = int(input("Digite a quantidade que deseja buscar: "))

        cursor.execute(
            "SELECT * FROM produtos WHERE quantidade = ?",
            (quantidade,)
        )

        produtos = cursor.fetchall()

        if not produtos:
            print("Nenhum produto encontrado.")
            return

        for linha in produtos:
            print(
                f"ID:{linha[0]} | "
                f"Produto:{linha[1]} | "
                f"Qtd:{linha[2]} | "
                f"Preço:R$ {str(linha[3]).replace('.', ',')}"
            )

    except ValueError:
        print("dados inseridos incorretos")
try:
    while True:
        print("escolha uma opção:")
        print("1-cadastre o produto")
        print("2-verifique o estoque")
        print("3-delete um produto")
        print("4-atualize o preço do produto")
        print("5-atulize o nome do produto")
        print("6-atualize a quantidade do produto")
        print("7-pesquisar produto")
        print("8-buscar por quantidade")
        print("9-verificar produtos com maiores e menores quantidae de estoque")
        print("10-verificar datas antigas")
        print("11-sair")
        escolha=int(input( "escolha um numero: ")) 
        if escolha==1:
            cadastrar() 
        elif escolha==2:
            listar()    
        elif escolha==3:
            deletar()
        elif escolha==4:
            atualizar_preco() 
        elif escolha==5:
            atualizar_nome()   
        elif escolha==6:
            atualizar_quantidaeEstoque() 
        elif escolha==7:
           buscar_produto()
        elif escolha==8:
            buscar_qtd()
        elif escolha==9:
            verqnt_estoque() 
        elif escolha==10:
            datas_antigas()          
        elif escolha==11:
             print("saindo...") 
             break         
except ValueError:
    print("dado invalido") 
    





