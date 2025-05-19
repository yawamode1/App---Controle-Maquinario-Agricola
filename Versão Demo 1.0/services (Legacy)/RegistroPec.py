from pathlib import Path
import sys


sys.path.append(str(Path(__file__).parent.parent))

from database.core import DBAgricola
from legacy.RegistroMaq import Maquina # Importa do legacy

class Peca:
    @staticmethod

    # Associa a peça a máquinas existentes
    def associar_maquinas(db, peca_id):
        while True:
            print("\n=== ASSOCIAR A MÁQUINAS ===")
            print("1. Associar a máquina(s) existente(s)")
            print("2. Cadastrar nova máquina")
            print("3. Finalizar associações")
            opcao = input("Opção: ")

            if opcao == "1":
                maquinas = Maquina.listar(db)
                if not maquinas:
                    print("Nenhuma máquina cadastrada!")
                    continue

                print("\nDigite o(s) ID(s) das máquinas separados por espaço:")
                ids_input = input("IDs: ").strip()

                if not ids_input:
                    print("Nenhum ID informado!")
                    continue

                ids_maquinas = []
                for id_str in ids_input.split():
                    if id_str.isdigit():
                        ids_maquinas.append(int(id_str))
                    else:
                        print(f"ID inválido ignorado: {id_str}")

                if not ids_maquinas:
                    print("Nenhum ID válido informado!")
                    continue

                try:
                    # Verifica se máquinas existem
                    placeholders = ','.join(['%s'] * len(ids_maquinas))
                    maquinas_existentes = db.executar(
                        f"SELECT id FROM maquinas WHERE id IN ({placeholders})",
                        tuple(ids_maquinas)
                    )

                    if len(maquinas_existentes) != len(ids_maquinas):
                        print("Atenção: Alguns IDs não correspondem a máquinas cadastradas!")

                    # Insere associações válidas
                    associacoes = 0
                    for maq in maquinas_existentes:
                        try:
                            db.executar(
                                "INSERT IGNORE INTO pecas_maquinas (id_peca, id_maquina) VALUES (%s, %s)",
                                (peca_id, maq['id'])
                            )
                            associacoes += 1
                        except:
                            continue

                    print(f"\n✅ {associacoes} associação(ões) realizada(s)!")

                except Exception as e:
                    print(f"Erro ao associar: {e}")

            elif opcao == "2":
                if Maquina.cadastrar(db):
                    # Pega o ID da máquina recém-criada
                    result = db.executar("SELECT LAST_INSERT_ID() as id")
                    nova_maquina_id = result[0]['id']
                    try:
                        db.executar(
                            "INSERT INTO pecas_maquinas (id_peca, id_maquina) VALUES (%s, %s)",
                            (peca_id, nova_maquina_id)
                        )
                        print("✅ Nova máquina cadastrada e associada automaticamente!")
                    except Exception as e:
                        print(f"Erro ao associar nova máquina: {e}")

            elif opcao == "3":
                break

    @staticmethod
    # Cadastra peças com validação básica de estoque
    def cadastrar(db):
        try:
            print("\n=== CADASTRO DE PEÇA ===")
            # Dados básicos
            nome = input("Nome da peça: ").strip()
            if not nome:
                print("Erro: Nome é obrigatório!")
                return False

            try:
                quantidade = int(input("Quantidade em estoque: "))
                if quantidade < 0:
                    print("Erro: Quantidade não pode ser negativa!")
                    return False
            except ValueError:
                print("Erro: Digite um número válido!")
                return False

            # Dados opcionais
            vida_util = input("Vida útil em horas (opcional): ").strip()
            fornecedor = input("Fornecedor (opcional): ").strip()
            quantidade_minima = input("Quantidade mínima (padrão: 5): ").strip()

            # Cadastra a peça
            query = """
                INSERT INTO pecas 
                (nome, quantidade_estoque, vida_util_horas, fornecedor, quantidade_minima) 
                VALUES (%s, %s, %s, %s, %s)
            """
            params = (
                nome,
                quantidade,
                int(vida_util) if vida_util.isdigit() else None,
                fornecedor if fornecedor else None,
                int(quantidade_minima) if quantidade_minima.isdigit() else 5
            )

            db.executar(query, params)

            # Pega o ID da peça recém-criada
            result = db.executar("SELECT LAST_INSERT_ID() as id")
            peca_id = result[0]['id']
            print(f"\n✅ Peça cadastrada! (ID: {peca_id})")

            # Associações com máquinas
            print("\nDeseja associar a máquinas agora? (S/N)")
            if input().strip().upper() == 'S':
                Peca.associar_maquinas(db, peca_id)

            return True

        except Exception as e:
            print(f"Erro inesperado: {e}")
            return False


if __name__ == "__main__":
    with DBAgricola() as db:
        Peca.cadastrar(db)