# Menu inicial
def menu():
    menu = """
    ================ MENU ================
    [d]  Depositar
    [s]  Sacar
    [e]  Extrato
    [nc] Nova conta
    [lc] Listar contas
    [nu] Novo usuário
    [q]  Sair

    => """

    return input(menu)
    
def depositar(saldo, valor, extrato, /):
# Lógica do depósito
    if valor < 0:
        print("\nATENÇÃO! Não é possível depositar valor negativo ou zero.")
    else:
        saldo += valor
        extrato += f"- Deposito: \tR$ {valor:.2f}\n"
        print(f"\n- Depósito de R$ {valor:.2f} realizado com sucesso!")

    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques, total_sacado_dia):
    # Lógica do saque
        if valor <= 0:
            print("\nATENÇÃO! Não é possível sacar valor negativo ou zero.")
        elif valor > saldo:
            print("\n- ATENÇÃO! Saldo insuficiente.")
        elif numero_saques >= limite_saques:
            print(f"\n- ATENÇÃO! Você atingiu o limite de {limite_saques} saques diários.")
        elif total_sacado_dia + valor > limite:
            print(f"\n- ATENÇÃO! O valor de saque excede o limite diário de R$ {limite:.2f}.")
            print(f"\n- Você já sacou R$ {total_sacado_dia:.2f} hoje.")
        else:
            saldo -= valor
            extrato += f"- Saque: \tR$ {valor:.2f}\n"
            numero_saques += 1
            total_sacado_dia += valor
            print(f"\n- Saque de R$ {valor} realizado com sucesso!")

        return saldo, extrato, numero_saques, total_sacado_dia

def exibir_extrato(saldo, extrato):
    # Lógica do extrato
        print("\n\t\tExtrato...")
        print("-"*40)
        if not extrato:
            print("\nNão foram realizadas movimentações.\n")
        else:
            print(f"\n{extrato}")
        print("-"*40)
        print(f"- Saldo da conta bancária: \tR$ {saldo:.2f}.")

def sair():
    print("\nSaindo...")
    print("Obrigado por usar nosso serviço. Volte sempre!\n")

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente os números) ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\nAtenção! Já existe usuário com esse CPF!")
        return
    
    nome = input("Informe o nome completo: ")
    data_nascimento = input(f"Certo, {nome}, agora informe a data de nascimento (dd-mm-aaaa): ")
    endereço = input(f"Muito bem, {nome}! Agora informe seu endereço (logradouro - nro - bairro - cidade - UF): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "CPF": cpf, "endereço": endereço})

    print("\n========== Usuário criado com sucesso! ==========")

def filtrar_usuario(cpf, usuarios):
    for usuario in usuarios:
        if usuario["CPF"] == cpf:
            return usuario # Retorna usuário encontrado
    
    return None # retorna None se não encontrar

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n ========== Conta criada com sucesso! ==========")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    
    print("\nAtenção! Usuário não encontrado. FLuxo de conta encerrado com sucesso!")

def listar_contas(contas):
    print("\n========== LISTA DE CONTAS ==========")

    if not contas:
        print("Nenhuma conta cadastrada ainda.")
        return

    for conta in contas:
        usuario = conta["usuario"]
        print(f"""
Agência:        {conta['agencia']}
Conta:          {conta['numero_conta']}
Titular:        {usuario['nome']}
CPF:            {usuario['CPF']}
Endereço:       {usuario['endereço']}
        """)
    print("=====================================")
    
def main():
    # Variáveis Globais
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    extrato = ""
    limite = 500
    total_sacado_dia = 0
    numero_saques = 0
    usuarios = []
    contas = []

    # Loop infinito
    while True:
        opcao = menu()

        if opcao == "d":
            valor = float(input("\nDigite o valor que deseja depositar: R$ "))
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Digite o valor que deseja sacar: R$ "))
            saldo, extrato, numero_saques, total_sacado_dia = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
                total_sacado_dia=total_sacado_dia
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            sair()
            break

        else:
            print("\nOpção inválida, por favor, selecione novamente a operação desejada.")

main()
