import pyodbc

conexao = pyodbc.connect(
    "DRIVER={SQL Server};"
    "SERVER=notbu645;"
    "DATABASE=estoque;"
    "Trusted_Connection=yes;"
)
cursor = conexao.cursor()
def cadastrar():


    nome_produto=input("digite o nome do produto:")
    quantidade_produto=int(input("digite a quantidade do produto:"))
    falor_produto=float(input("digite o preço do produto"))

    cursor.execute(
       "INSERT INTO produtos (nome, quantidade, preco) VALUES (?, ?, ?)",(nome_produto,quantidade_produto,falor_produto))
    conexao.commit()

    print("Produto cadastrado!")
def listar():
    cursor.execute("SELECT * FROM produtos")

    for linha in cursor.fetchall():

         print(linha)
escolha=int(input( "escolha um numero uma obção 1 para cadastra produto e 2 para ver o estoque"   )) 
if escolha==1:
    cadastrar()     
elif escolha==2:
    listar()
else:
    print("nada")



