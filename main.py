from cliente import cadastro_cliente
from conta import operacao

print("=================================")
print("= SEJA BEM VINDO O BANCO MISTER =")
print("=================================")
print("\n")

print("Informe seus dados para criarmos a sua conta: \n")


cliente = cadastro_cliente()


saldo = 0

"""A seguir, está a parte de execução das operações disponiveis. 
Como não é permitido o uso de estruturas de repetição, coloquei um numero de operaçoes que julguei valido"""

print(f"{cliente}, VOCÊ TERÁ DIREITO A 5 OPERAÇÕES INICIAIS.\n")
print("Selecione uma das operações e aproveite a sua nova conta: \n")

saldo = operacao(saldo)
print("\n")

print("Selecione a segunda operação:\n")
saldo = operacao(saldo)
print("\n")

print("Selecione a terceira operação:\n")
saldo = operacao(saldo)
print("\n")

print("Selecione a terceira operação:\n")
saldo = operacao(saldo)
print("\n")

print("Selecione a terceira operação:\n")
saldo = operacao(saldo)
print("\n")


print("Ao final das operações, o saldo atual é de: R$",saldo)