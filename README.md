🏦 Sistema Bancário em Python

Sistema bancário simples desenvolvido em Python, com cadastro de usuários, criação de contas e operações de depósito, saque e extrato. O projeto tem duas versões: uma no terminal (menu de texto) e outra com interface gráfica (Tkinter).

🎯 Objetivo

Praticar lógica de programação, funções, estruturas de dados (listas e dicionários) e construção de interfaces gráficas, simulando as operações básicas de um banco.

✨ Funcionalidades
Novo usuário: cadastro com nome, CPF, data de nascimento e endereço (não permite CPF repetido).
Nova conta: cria uma conta vinculada a um usuário já cadastrado, com agência 0001 e número sequencial.
Listar contas: exibe agência, número, titular, CPF e saldo.
Depositar: aceita apenas valores maiores que zero.
Sacar: respeita as regras de saque descritas abaixo.
Extrato: mostra todas as movimentações e o saldo atual.

📏 Regras de negócio
Regra	Valor
Limite de saques por dia	3
Limite de valor sacado por dia	R$ 500,00
Saque maior que o saldo	Bloqueado
Depósito/saque com valor zero ou negativo	Bloqueado

🗂️ Estrutura
.
├── Sistema_Bancário_3.py   # versão no terminal (menu de texto)
├── banco_gui.py            # versão com interface gráfica (Tkinter)
└── README.md

🛠️ Tecnologias
Python 3
Tkinter (biblioteca padrão do Python, não precisa instalar nada)

🚀 Como executar
Tenha o Python 3 instalado.
Clone o repositório:
bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
Execute a versão desejada: Interface gráfica
bash
python banco_gui.py

Terminal

bash
python Sistema_Bancário_3.py

🖥️ Como usar

Interface gráfica

Na aba Usuários, cadastre um usuário.
Na aba Contas, escolha o titular e clique em Criar conta.
Na aba Operações, selecione a conta, digite o valor e use Depositar ou Sacar. O saldo e o extrato são atualizados na hora.

Terminal

Digite a letra da opção no menu e pressione Enter:

[d]  Depositar
[s]  Sacar
[e]  Extrato
[nc] Nova conta
[lc] Listar contas
[nu] Novo usuário
[q]  Sair

Cadastre o usuário (nu) antes de criar a conta (nc), e digite o CPF exatamente igual nas duas etapas.

⚠️ Limitações
Os dados ficam apenas na memória: ao fechar o programa, usuários e contas são perdidos.
Na versão de terminal, saldo e extrato são compartilhados entre todas as contas. Na versão gráfica, cada conta tem o seu.

🔮 Próximos passos
Salvar os dados em arquivo JSON ou banco de dados (ex.: SQLite).
Reorganizar o código com programação orientada a objetos (Cliente, Conta, Banco).
Validar o CPF e a data de nascimento.
Adicionar transferência entre contas.
Criar testes automatizados.

👤 Autor

José Carlos Da Silva Júnior
