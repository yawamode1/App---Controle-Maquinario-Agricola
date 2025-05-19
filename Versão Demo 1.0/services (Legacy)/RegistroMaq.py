from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))


class Maquina:
    @staticmethod
    # Lista todas as máquinas cadastradas
    def listar(db):
        try:
            maquinas = db.executar("SELECT id, nome, modelo FROM maquinas")
            print("\n=== MÁQUINAS CADASTRADAS ===")
            for maq in maquinas:
                print(f"ID: {maq['id']} | {maq['nome']} ({maq['modelo']})")
            return maquinas
        except Exception as e:
            print(f"Erro ao listar máquinas: {e}")
            return []

    @staticmethod
    # Cadastra uma máquina com validação básica
    def cadastrar(db):
        nome = input("Nome da máquina: ").strip()
        if not nome:
            print("Erro: Nome é obrigatório!")
            return False

        modelo = input("Modelo: ").strip()

        try:
            db.executar(
                "INSERT INTO maquinas (nome, modelo) VALUES (%s, %s)",
                (nome, modelo)
            )
            # Pega o ID recém-criado
            result = db.executar("SELECT LAST_INSERT_ID() as id")
            print(f"\n✅ Máquina cadastrada! (ID: {result[0]['id']})")
            return True
        except Exception as e:
            print(f"Erro ao cadastrar: {e}")
            return False

    @staticmethod
    # Lista peças compatíveis com uma máquina
    def listar_pecas(db):
        try:
            # Mostra as máquinas disponíveis
            maquinas = Maquina.listar(db)
            if not maquinas:
                print("Nenhuma máquina cadastrada!")
                return

            maquina_id = input("\nDigite o ID da máquina: ")
            if not maquina_id.isdigit():
                print("ID inválido!")
                return

            pecas = db.executar("""
                SELECT p.id, p.nome, p.quantidade_estoque 
                FROM pecas p
                JOIN pecas_maquinas pm ON p.id = pm.id_peca 
                WHERE pm.id_maquina = %s
            """, (int(maquina_id),))

            print(f"\n=== PEÇAS PARA MÁQUINA ID {maquina_id} ===")
            for peca in pecas:
                print(f"ID: {peca['id']} | {peca['nome']} (Estoque: {peca['quantidade_estoque']})")

        except Exception as e:
            print(f"Erro ao listar peças: {e}")