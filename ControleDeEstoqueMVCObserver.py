# Model

class Produto:
	def __init__(self, nome, quantidade, preco):
		self.nome = nome
		self.quantidade = quantidade
		self.preco = preco

	def __str__(self):
		return f"Produto: {self.nome}, Quantidade: {self.quantidade}, Preço: R${self.preco:.2f}"


class Estoque:
	def __init__(self):
		self.listaProdutos = []
		self.listaObservers = []

	def adicionarProduto(self, produto):
		self.listaProdutos.append(produto)
		self.notificar(produto)

	def removerProduto(self, nome):
		for produto in self.listaProdutos:
			if produto.nome == nome:
				self.listaProdutos.remove(produto)
				return produto
		return None

	def atualizarProduto(self, nome, quantidade=None, preco=None):
		for produto in self.listaProdutos:
			if produto.nome == nome:
				if quantidade is not None:
					produto.quantidade = quantidade
					self.notificar(produto)
				if preco is not None:
					produto.preco = preco
				return produto
		return None

	def listarProdutos(self):
		return self.listaProdutos

	def adicionarObserver(self, observer):
		self.listaObservers.append(observer)

	def removerObserver(self, observer):
		self.listaObservers.remove(observer)

	def notificar(self, produto):
		for observer in self.listaObservers:
			observer.atualizar(produto)

# Observers

class EstoqueBaixoObserver:
	def __init__(self, controller):
		self.controller = controller

	def atualizar(self, produto):
		if produto.quantidade < 5:
			self.controller.avisarEstoqueBaixo(produto.nome)

class EstoqueCheioObserver:
	def __init__(self, controller):
		self.controller = controller

	def atualizar(self, produto):
		if produto.quantidade > 10:
			self.controller.avisarEstoqueCheio(produto.nome)

# Controller

class EstoqueController:
	def __init__(self, estoque, view):
		self.estoque = estoque
		self.view = view

	def adicionarProduto(self, nome, quantidade, preco):
		produto = Produto(nome, quantidade, preco)
		self.estoque.adicionarProduto(produto)

	def removerProduto(self, nome):
		return self.estoque.removerProduto(nome)

	def atualizarProduto(self, nome, quantidade=None, preco=None):
		return self.estoque.atualizarProduto(nome, quantidade, preco)

	def listarProdutos(self):
		return self.estoque.listarProdutos()

	def avisarEstoqueBaixo(self, nomeProduto):
		self.view.exibirMensagem(f"ALERTA: A quantidade do produto '{nomeProduto}' está abaixo de 5!")

	def avisarEstoqueCheio(self, nomeProduto):
		self.view.exibirMensagem(f"ALERTA: Estoque cheio para o produto '{nomeProduto}'!")

# View

class EstoqueView:
	def exibirMenu(self):
		print("\nMenu de Controle de Estoque")
		print("1. Adicionar Produto")
		print("2. Remover Produto")
		print("3. Atualizar Produto")
		print("4. Listar Produtos")
		print("5. Sair")
		return int(input("Escolha uma opção: "))

	def exibirProdutos(self, produtos):
		if produtos:
			for produto in produtos:
				print(produto)
		else:
			print("Nenhum produto no estoque.")

	#def solicitarNomeProduto(self, acao=""):
	#	return input(f"Nome do produto a {acao}: ")

	def solicitarDadosProduto(self, acao=""):
		nome = input(f"Nome do produto a {acao}: ")
		if acao == "adicionar":
			quantidade = int(input("Quantidade: "))
			preco = float(input("Preço: "))
			return nome, quantidade, preco
		if acao == "atualizar":
			quantidade = int(input("Nova quantidade (ou -1 para não alterar): "))
			preco = float(input("Novo preço (ou -1 para não alterar): "))
			quantidade = None if quantidade == -1 else quantidade
			preco = None if preco == -1 else preco
			return nome, quantidade, preco
		if acao == "remover":
			return nome


	def exibirMensagem(self, mensagem):
		print(mensagem)

# Main

def main():
	view = EstoqueView()
	estoque = Estoque()
	controller = EstoqueController(estoque, view)

	observerEstoqueBaixo = EstoqueBaixoObserver(controller)
	observerEstoqueCheio = EstoqueCheioObserver(controller)
	
	estoque.adicionarObserver(observerEstoqueBaixo)
	estoque.adicionarObserver(observerEstoqueCheio)

	while True:
		opcao = view.exibirMenu()

		if opcao == 1:
			nome, quantidade, preco = view.solicitarDadosProduto(acao="adicionar")
			controller.adicionarProduto(nome, quantidade, preco)
			view.exibirMensagem(f"Produto '{nome}' adicionado com sucesso.")
		
		elif opcao == 2:
			nome = view.solicitarDadosProduto(acao="remover")
			produto = controller.removerProduto(nome)
			if produto:
				view.exibirMensagem(f"Produto '{nome}' removido.")
			else:
				view.exibirMensagem(f"Produto '{nome}' não encontrado.")
		
		elif opcao == 3:
			nome, quantidade, preco = view.solicitarDadosProduto(acao="atualizar")
			produto = controller.atualizarProduto(nome, quantidade, preco)
			if produto:
				view.exibirMensagem(f"Produto '{nome}' atualizado.")
			else:
				view.exibirMensagem(f"Produto '{nome}' não encontrado.")
		
		elif opcao == 4:
			#produtos = controller.listarProdutos()
			view.exibirProdutos(controller.listarProdutos())
		
		elif opcao == 5:
			break

		else:
			view.exibirMensagem("Opção inválida! Tente novamente.")

if __name__ == "__main__":
	main()