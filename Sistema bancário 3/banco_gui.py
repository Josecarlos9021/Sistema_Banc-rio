import tkinter as tk
from tkinter import ttk, messagebox

LIMITE_SAQUES = 3
LIMITE_VALOR_DIA = 500
AGENCIA = "0001"


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema Bancário")
        self.geometry("680x520")
        self.minsize(620, 480)

        self.usuarios = []
        self.contas = []

        abas = ttk.Notebook(self)
        abas.pack(fill="both", expand=True, padx=8, pady=8)

        self.aba_operacoes = ttk.Frame(abas, padding=12)
        self.aba_usuarios = ttk.Frame(abas, padding=12)
        self.aba_contas = ttk.Frame(abas, padding=12)
        abas.add(self.aba_operacoes, text="Operações")
        abas.add(self.aba_usuarios, text="Usuários")
        abas.add(self.aba_contas, text="Contas")

        self.montar_aba_usuarios()
        self.montar_aba_contas()
        self.montar_aba_operacoes()

    # ---------------- Abas ----------------
    def montar_aba_usuarios(self):
        f = self.aba_usuarios
        self.ent_nome = self.campo(f, "Nome completo", 0)
        self.ent_cpf = self.campo(f, "CPF (somente números)", 1)
        self.ent_nasc = self.campo(f, "Nascimento (dd-mm-aaaa)", 2)
        self.ent_end = self.campo(f, "Endereço", 3)
        ttk.Button(f, text="Cadastrar usuário", command=self.criar_usuario).grid(
            row=4, column=1, sticky="e", pady=8
        )
        self.tree_usuarios = ttk.Treeview(
            f, columns=("nome", "cpf", "end"), show="headings", height=8
        )
        for col, titulo in (("nome", "Nome"), ("cpf", "CPF"), ("end", "Endereço")):
            self.tree_usuarios.heading(col, text=titulo)
        self.tree_usuarios.grid(row=5, column=0, columnspan=2, sticky="nsew")
        f.columnconfigure(1, weight=1)
        f.rowconfigure(5, weight=1)

    def montar_aba_contas(self):
        f = self.aba_contas
        ttk.Label(f, text="Titular:").grid(row=0, column=0, sticky="w")
        self.cmb_usuario = ttk.Combobox(f, state="readonly", width=40)
        self.cmb_usuario.grid(row=0, column=1, sticky="we", padx=6)
        ttk.Button(f, text="Criar conta", command=self.criar_conta).grid(row=0, column=2)
        self.tree_contas = ttk.Treeview(
            f, columns=("ag", "num", "titular", "cpf", "saldo"), show="headings", height=10
        )
        for col, titulo in (
            ("ag", "Agência"), ("num", "Conta"), ("titular", "Titular"),
            ("cpf", "CPF"), ("saldo", "Saldo"),
        ):
            self.tree_contas.heading(col, text=titulo)
            self.tree_contas.column(col, width=90)
        self.tree_contas.grid(row=1, column=0, columnspan=3, sticky="nsew", pady=10)
        f.columnconfigure(1, weight=1)
        f.rowconfigure(1, weight=1)

    def montar_aba_operacoes(self):
        f = self.aba_operacoes
        ttk.Label(f, text="Conta:").grid(row=0, column=0, sticky="w")
        self.cmb_conta = ttk.Combobox(f, state="readonly", width=40)
        self.cmb_conta.grid(row=0, column=1, columnspan=2, sticky="we", padx=6)
        self.cmb_conta.bind("<<ComboboxSelected>>", lambda e: self.atualizar_extrato())

        ttk.Label(f, text="Valor (R$):").grid(row=1, column=0, sticky="w", pady=8)
        self.ent_valor = ttk.Entry(f, width=15)
        self.ent_valor.grid(row=1, column=1, sticky="w", padx=6)

        botoes = ttk.Frame(f)
        botoes.grid(row=1, column=2, sticky="e")
        ttk.Button(botoes, text="Depositar", command=self.depositar).pack(side="left", padx=2)
        ttk.Button(botoes, text="Sacar", command=self.sacar).pack(side="left", padx=2)

        self.lbl_saldo = ttk.Label(f, text="Saldo: R$ 0.00", font=("Segoe UI", 12, "bold"))
        self.lbl_saldo.grid(row=2, column=0, columnspan=3, sticky="w", pady=(4, 8))

        self.txt_extrato = tk.Text(f, height=14, state="disabled")
        self.txt_extrato.grid(row=3, column=0, columnspan=3, sticky="nsew")
        f.columnconfigure(1, weight=1)
        f.rowconfigure(3, weight=1)

    def campo(self, frame, rotulo, linha):
        ttk.Label(frame, text=rotulo).grid(row=linha, column=0, sticky="w", pady=3)
        entrada = ttk.Entry(frame)
        entrada.grid(row=linha, column=1, sticky="we", padx=6)
        return entrada

    # ---------------- Regras de negócio ----------------
    def filtrar_usuario(self, cpf):
        return next((u for u in self.usuarios if u["cpf"] == cpf), None)

    def criar_usuario(self):
        nome = self.ent_nome.get().strip()
        cpf = "".join(c for c in self.ent_cpf.get() if c.isdigit())
        if not nome or not cpf:
            messagebox.showwarning("Atenção", "Informe pelo menos nome e CPF.")
            return
        if self.filtrar_usuario(cpf):
            messagebox.showwarning("Atenção", "Já existe usuário com esse CPF.")
            return
        self.usuarios.append({
            "nome": nome,
            "cpf": cpf,
            "nascimento": self.ent_nasc.get().strip(),
            "endereco": self.ent_end.get().strip(),
        })
        for e in (self.ent_nome, self.ent_cpf, self.ent_nasc, self.ent_end):
            e.delete(0, "end")
        self.atualizar_telas()
        messagebox.showinfo("Pronto", "Usuário criado com sucesso!")

    def criar_conta(self):
        i = self.cmb_usuario.current()
        if i < 0:
            messagebox.showwarning("Atenção", "Selecione um titular (cadastre um usuário antes).")
            return
        self.contas.append({
            "agencia": AGENCIA,
            "numero": len(self.contas) + 1,
            "usuario": self.usuarios[i],
            "saldo": 0.0,
            "extrato": [],
            "saques": 0,
            "total_sacado": 0.0,
        })
        self.atualizar_telas()
        messagebox.showinfo("Pronto", "Conta criada com sucesso!")

    def conta_selecionada(self):
        i = self.cmb_conta.current()
        if i < 0:
            messagebox.showwarning("Atenção", "Selecione uma conta.")
            return None
        return self.contas[i]

    def valor_digitado(self):
        try:
            valor = float(self.ent_valor.get().replace(",", "."))
        except ValueError:
            messagebox.showwarning("Atenção", "Digite um valor numérico válido.")
            return None
        if valor <= 0:
            messagebox.showwarning("Atenção", "O valor deve ser maior que zero.")
            return None
        return valor

    def depositar(self):
        conta = self.conta_selecionada()
        valor = conta and self.valor_digitado()
        if not valor:
            return
        conta["saldo"] += valor
        conta["extrato"].append(f"Depósito:  R$ {valor:.2f}")
        self.ent_valor.delete(0, "end")
        self.atualizar_telas()

    def sacar(self):
        conta = self.conta_selecionada()
        valor = conta and self.valor_digitado()
        if not valor:
            return
        if valor > conta["saldo"]:
            msg = "Saldo insuficiente."
        elif conta["saques"] >= LIMITE_SAQUES:
            msg = f"Limite de {LIMITE_SAQUES} saques diários atingido."
        elif conta["total_sacado"] + valor > LIMITE_VALOR_DIA:
            msg = (f"Excede o limite diário de R$ {LIMITE_VALOR_DIA:.2f}. "
                   f"Já sacado hoje: R$ {conta['total_sacado']:.2f}.")
        else:
            conta["saldo"] -= valor
            conta["saques"] += 1
            conta["total_sacado"] += valor
            conta["extrato"].append(f"Saque:     R$ {valor:.2f}")
            self.ent_valor.delete(0, "end")
            self.atualizar_telas()
            return
        messagebox.showwarning("Saque não realizado", msg)

    # ---------------- Atualização da tela ----------------
    def atualizar_telas(self):
        self.tree_usuarios.delete(*self.tree_usuarios.get_children())
        for u in self.usuarios:
            self.tree_usuarios.insert("", "end", values=(u["nome"], u["cpf"], u["endereco"]))

        self.tree_contas.delete(*self.tree_contas.get_children())
        for c in self.contas:
            self.tree_contas.insert("", "end", values=(
                c["agencia"], c["numero"], c["usuario"]["nome"],
                c["usuario"]["cpf"], f"R$ {c['saldo']:.2f}",
            ))

        self.cmb_usuario["values"] = [f"{u['nome']} - {u['cpf']}" for u in self.usuarios]
        atual = self.cmb_conta.current()
        self.cmb_conta["values"] = [
            f"{c['agencia']} / {c['numero']} - {c['usuario']['nome']}" for c in self.contas
        ]
        if self.contas:
            self.cmb_conta.current(atual if atual >= 0 else len(self.contas) - 1)
        self.atualizar_extrato()

    def atualizar_extrato(self):
        i = self.cmb_conta.current()
        self.txt_extrato.configure(state="normal")
        self.txt_extrato.delete("1.0", "end")
        if i < 0:
            self.lbl_saldo.config(text="Saldo: R$ 0.00")
        else:
            conta = self.contas[i]
            linhas = conta["extrato"] or ["Não foram realizadas movimentações."]
            self.txt_extrato.insert("end", "\n".join(linhas))
            self.lbl_saldo.config(text=f"Saldo: R$ {conta['saldo']:.2f}")
        self.txt_extrato.configure(state="disabled")


if __name__ == "__main__":
    App().mainloop()
