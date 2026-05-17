import pyodbc

conexao = pyodbc.connect(
    "DRIVER={SQL Server};"
    "SERVER=notbu645;"
    "DATABASE=estoque;"
    "Trusted_Connection=yes;"
)
cursor = conexao.cursor()

nome_produto=input("digite o nome do produto:")
quantidade_produto=int(input("digite a quantidade do produto:"))
falor_produto=float(input("digite o preço do produto"))
if nome_produto!=isalpha():
    print("digite um nome valido!")
cursor.execute(
    "INSERT INTO produtos (nome, quantidade, preco) VALUES (?, ?, ?)",(nome_produto,quantidade_produto,falor_produto))
conexao.commit()

print("Produto cadastrado!")

