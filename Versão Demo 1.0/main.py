import sys
import tkinter as tk
from pathlib import Path

# Caminho absoluto do projeto
PROJETO_ROOT = Path(__file__).parent
sys.path.append(str(PROJETO_ROOT))

# Ativa o menu legado no terminal
def modo_console():
    from database.core import DBAgricola
    from legacy.RegistroMaq import Maquina  # Importa do legacy
    from legacy.RegistroPec import Peca     # Importa do legacy

    def menu_principal():
        print("\n=== SISTEMA AGRÍCOLA (MODO CONSOLE) ===")
        print("1. Cadastrar Máquina")
        print("2. Cadastrar Peça")
        print("3. Listar Peças por Máquina")
        print("4. Sair")
        return input("Opção: ")

    with DBAgricola() as db:
        while True:
            opcao = menu_principal()
            if opcao == "1":
                Maquina.cadastrar(db)
            elif opcao == "2":
                Peca.cadastrar(db)
            elif opcao == "3":
                Maquina.listar_pecas(db)
            elif opcao == "4":
                break
            else:
                print("Opção inválida!")

# Ativa a interface gráfica Tkinter
def modo_grafico():
    from interface.WelcomeWindow import AgricolaApp
    root = tk.Tk()
    app = AgricolaApp(root)
    root.mainloop()

if __name__ == "__main__":
    if "--cli" in sys.argv:
        print("\n🔧 Modo Console Ativado (Legado)")
        modo_console()
    else:
        print("\n🖥️ Iniciando Interface Gráfica...")
        modo_grafico()