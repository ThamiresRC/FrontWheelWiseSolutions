import os

from datetime import datetime

import cx_Oracle

import json

# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configuração CORS para permitir requisições do front-end
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # URL do front-end
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/endpoint")
async def get_data():
    return {"message": "Hello from FastAPI!"}


if not os.path.exists("json_exports"):
    os.makedirs("json_exports")

def conectar_bd():
    try:
        # Ajuste a string de conexão conforme suas informações
        connection = cx_Oracle.connect("rm558833", "200306", "oracle.fiap.com.br/ORCL")
        print("Conexão com o banco de dados Oracle estabelecida com sucesso.")
        return connection
    except cx_Oracle.DatabaseError as e:
        print("Erro ao conectar ao banco de dados:", e)
        return None

# Estabelece a conexão uma vez para uso em várias funções


# Estruturas de dados
veiculos = [ 
    {"nome": "Carro A", "marca": "Toyota", "modelo": "Corolla", "ano": 2020, "combustivel": "Gasolina", "cor": "Preto", "placa": "ABC-1234"},
    {"nome": "Carro B", "marca": "Honda", "modelo": "Civic", "ano": 2021, "combustivel": "Flex", "cor": "Branco", "placa": "DEF-5678"},
    {"nome": "Carro C", "marca": "Ford", "modelo": "Fusion", "ano": 2019, "combustivel": "Gasolina", "cor": "Prata", "placa": "GHI-9012"}
]
manutencoes = []
historico_manutencao = []

def menu():
    while True:
        limpar_tela()
        print("\n=== MENU PRINCIPAL ===")
        print("1. Gerenciar Veículos")
        print("2. Histórico de Manutenção")
        print("3. Diagnóstico do Veículo")
        print("4. Benefícios")
        print("5. Orçamentos")
        print("6. Agendamentos")
        print("7. Sair")
        
        opcao = input("Selecione uma opção: ")

        if opcao == '1':
            menu_automoveis(conexao)
        elif opcao == '2':
            menu_historico_manutencao()
        elif opcao == '3':
            diagnostico_veiculo()
            input("\nPressione Enter para voltar ao menu principal...")
        elif opcao == '4':
            exibir_beneficios()
            input("\nPressione Enter para voltar ao menu principal...")
        elif opcao == '5':
            menu_orcamentos(conexao)
        elif opcao == '6':
            menu_agendamentos(conexao)
        elif opcao == '7':
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")
            input("\nPressione Enter para continuar...")


def adicionar_agendamento(conexao):
    try:
        with conexao.cursor() as cursor:
            # Verifica o maior valor de ID já existente na tabela t_ws_agendamento
            cursor.execute("SELECT NVL(MAX(id_agendamento), 0) + 1 FROM t_ws_agendamento")
            max_id = cursor.fetchone()[0]
            
            # Tenta criar a sequência T_WS_AGENDAMENTO_SEQ para começar após o maior ID encontrado
            try:
                cursor.execute(f"CREATE SEQUENCE T_WS_AGENDAMENTO_SEQ START WITH {max_id} INCREMENT BY 1 NOCACHE")
                print("Sequência T_WS_AGENDAMENTO_SEQ criada com sucesso.")
            except cx_Oracle.DatabaseError as e:
                error_obj, = e.args
                # Caso a sequência já exista, apenas continue
                if error_obj.code == 2289:  # ORA-02289 significa que a sequência não existe
                    print("A sequência T_WS_AGENDAMENTO_SEQ já existe, continuando.")
                else:
                    raise

            # Solicita ao usuário os dados para o novo agendamento
            t_ws_diagnostico_id_diagnóstico = int(input("Informe o ID do diagnóstico: "))
            dt_e_hora = input("Informe a data e hora do agendamento (YYYY-MM-DD HH24:MI): ")
            ds_servico = input("Informe a descrição do serviço: ")

            # Insere o novo agendamento na tabela
            cursor.execute(
                """
                INSERT INTO t_ws_agendamento (id_agendamento, t_ws_diagnostico_id_diagnóstico, dt_e_hora, ds_servico)
                VALUES (T_WS_AGENDAMENTO_SEQ.NEXTVAL, :t_ws_diagnostico_id_diagnóstico, TO_DATE(:dt_e_hora, 'YYYY-MM-DD HH24:MI'), :ds_servico)
                """,
                t_ws_diagnostico_id_diagnóstico=t_ws_diagnostico_id_diagnóstico,
                dt_e_hora=dt_e_hora,
                ds_servico=ds_servico
            )
            conexao.commit()
            print("Agendamento adicionado com sucesso.")
    except cx_Oracle.DatabaseError as e:
        print("Erro ao adicionar agendamento:", e)


def listar_agendamentos(conexao):
    with conexao.cursor() as cursor:
        cursor.execute("SELECT * FROM t_ws_agendamento ORDER BY dt_e_hora")
        for row in cursor.fetchall():
            print(row)

def atualizar_agendamento(conexao):
    with conexao.cursor() as cursor:
        id_agendamento = int(input("Digite o ID do agendamento a ser atualizado: "))
        t_ws_diagnostico_id_diagnóstico = int(input("Digite o novo ID do diagnóstico: "))
        dt_e_hora = input("Digite a nova data e hora do agendamento (YYYY-MM-DD HH24:MI): ")
        ds_servico = input("Digite a nova descrição do serviço: ")

        cursor.execute(
            "UPDATE t_ws_agendamento SET t_ws_diagnostico_id_diagnóstico = :t_ws_diagnostico_id_diagnóstico, "
            "dt_e_hora = TO_DATE(:dt_e_hora, 'YYYY-MM-DD HH24:MI'), ds_servico = :ds_servico "
            "WHERE id_agendamento = :id_agendamento",
            t_ws_diagnostico_id_diagnóstico=t_ws_diagnostico_id_diagnóstico, dt_e_hora=dt_e_hora, ds_servico=ds_servico,
            id_agendamento=id_agendamento
        )
        conexao.commit()
        print("Agendamento atualizado com sucesso.")

def deletar_agendamento(conexao):
    try:
        with conexao.cursor() as cursor:
            id_agendamento = int(input("Digite o ID do agendamento a ser deletado: "))

            # Verificar se há registros dependentes em `t_ws_oficina`
            cursor.execute("SELECT COUNT(*) FROM t_ws_oficina WHERE t_ws_agendamento_id_agendamento = :id_agendamento", {'id_agendamento': id_agendamento})
            dependencias = cursor.fetchone()[0]

            if dependencias > 0:
                # Excluir os registros dependentes antes
                cursor.execute("DELETE FROM t_ws_oficina WHERE t_ws_agendamento_id_agendamento = :id_agendamento", {'id_agendamento': id_agendamento})
                print("Registros dependentes em `t_ws_oficina` foram excluídos.")

            # Agora exclui o agendamento
            cursor.execute("DELETE FROM t_ws_agendamento WHERE id_agendamento = :id_agendamento", {'id_agendamento': id_agendamento})
            conexao.commit()
            print("Agendamento deletado com sucesso.")
    except Exception as e:
        print(f"Ocorreu um erro ao tentar deletar o agendamento: {e}")





def menu_agendamentos(conexao):
    while True:
        print("\n--- Menu de Agendamentos ---")
        print("1. Adicionar Agendamento")
        print("2. Listar Agendamentos")
        print("3. Atualizar Agendamento")
        print("4. Deletar Agendamento")
        print("5. Exportar Dados")
        print("0. Voltar ao Menu Principal")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            adicionar_agendamento(conexao)
        elif opcao == '2':
            listar_agendamentos(conexao)
        elif opcao == '3':
            atualizar_agendamento(conexao)
        elif opcao == '4':
            deletar_agendamento(conexao)
        elif opcao == '5':
            exportar_agendamentos_para_json(conexao)
        elif opcao == '0':
            break
        else:
            print("Opção inválida. Tente novamente.")

def ajustar_sequencia_orcamento(conexao):
    try:
        with conexao.cursor() as cursor:
            # Obtenha o maior ID atualmente na tabela t_ws_orcamento
            cursor.execute("SELECT MAX(ID_ORCAMENTO) FROM t_ws_orcamento")
            maior_id = cursor.fetchone()[0]
            if maior_id is None:
                maior_id = 0  # Caso não haja registros, iniciar a sequência em 1

            # Ajuste a sequência para começar depois do maior ID atual
            cursor.execute("DROP SEQUENCE T_WS_ORCAMENTO_SEQ")
            cursor.execute(f"CREATE SEQUENCE T_WS_ORCAMENTO_SEQ START WITH {maior_id + 1} INCREMENT BY 1 NOCACHE")
            conexao.commit()
            print(f"Sequência T_WS_ORCAMENTO_SEQ ajustada para iniciar em {maior_id + 1}")
    except cx_Oracle.DatabaseError as e:
        print("Erro ao ajustar a sequência:", e)

# Função para adicionar orçamento, agora usando a sequência ajustada
def adicionar_orcamento(conexao):
    with conexao.cursor() as cursor:
        dt_emissao = input("Digite a data de emissão (YYYY-MM-DD): ")
        ds_servicos = input("Digite a descrição dos serviços: ")
        ds_pecas = input("Digite a descrição das peças: ")
        vl_custo_total = float(input("Digite o valor total: "))

        # Pegue o próximo valor da sequência para o ID_ORCAMENTO
        cursor.execute("SELECT T_WS_ORCAMENTO_SEQ.NEXTVAL FROM dual")
        novo_id = cursor.fetchone()[0]

        # Insira o novo orçamento com o ID gerado
        cursor.execute(
            "INSERT INTO t_ws_orcamento (ID_ORCAMENTO, DT_EMISSAO, DS_SERVICOS, DS_PECAS, VL_CUSTO_TOTAL) VALUES (:id, TO_DATE(:dt_emissao, 'YYYY-MM-DD'), :ds_servicos, :ds_pecas, :vl_custo_total)",
            id=novo_id, dt_emissao=dt_emissao, ds_servicos=ds_servicos, ds_pecas=ds_pecas, vl_custo_total=vl_custo_total
        )
        conexao.commit()
        print("Orçamento adicionado com sucesso.")
        
        # Confirma a inserção no banco de dados
        conexao.commit()
        print("Orçamento adicionado com sucesso.")


conexao = conectar_bd()
if conexao:
    ajustar_sequencia_orcamento(conexao)
    
def listar_orcamentos(conexao):
    with conexao.cursor() as cursor:
        cursor.execute("SELECT * FROM t_ws_orcamento")
        for row in cursor.fetchall():
            print(row)

def atualizar_orcamento(conexao):
    with conexao.cursor() as cursor:
        id_orcamento = int(input("Digite o ID do orçamento a ser atualizado: "))
        dt_emissao = input("Digite a nova data de emissão (YYYY-MM-DD): ")
        ds_servicos = input("Digite a nova descrição dos serviços: ")
        ds_pecas = input("Digite a nova descrição das peças: ")
        vl_custo_total = float(input("Digite o novo valor total: "))

        # SQL atualizado com o nome correto da coluna ID_ORCAMENTO
        cursor.execute(
            """
            UPDATE t_ws_orcamento 
            SET dt_emissao = TO_DATE(:dt_emissao, 'YYYY-MM-DD'), 
                ds_servicos = :ds_servicos, 
                ds_pecas = :ds_pecas, 
                vl_custo_total = :vl_custo_total 
            WHERE id_orcamento = :id_orcamento
            """,
            dt_emissao=dt_emissao, ds_servicos=ds_servicos, ds_pecas=ds_pecas, 
            vl_custo_total=vl_custo_total, id_orcamento=id_orcamento
        )
        conexao.commit()
        print("Orçamento atualizado com sucesso.")


def deletar_diagnosticos_por_orcamento(conexao, id_orcamento):
    with conexao.cursor() as cursor:
        cursor.execute("DELETE FROM t_ws_diagnostico WHERE T_WS_ORCAMENTO_ID_ORCAMENTO = :id_orcamento", id_orcamento=id_orcamento)
        conexao.commit()
        print("Todos os diagnósticos relacionados foram deletados.")

def deletar_produtos_por_orcamento(conexao, id_orcamento):
    with conexao.cursor() as cursor:
        cursor.execute("DELETE FROM t_ws_produto WHERE T_WS_ORCAMENTO_ID_ORCAMENTO = :id_orcamento", id_orcamento=id_orcamento)
        conexao.commit()
        print("Todos os produtos relacionados foram deletados.")

def deletar_orcamento(conexao):
    with conexao.cursor() as cursor:
        id_orcamento = int(input("Digite o ID do orçamento a ser deletado: "))
        
        # Primeiro, delete os produtos relacionados
        deletar_produtos_por_orcamento(conexao, id_orcamento)
        
        # Delete os diagnósticos relacionados
        deletar_diagnosticos_por_orcamento(conexao, id_orcamento)

        # Agora, delete o orçamento
        cursor.execute("DELETE FROM t_ws_orcamento WHERE id_orcamento = :id_orcamento", id_orcamento=id_orcamento)
        conexao.commit()
        print("Orçamento deletado com sucesso.")




def menu_orcamentos(conexao):
    while True:
        print("\n--- Menu de Orçamentos ---")
        print("1. Adicionar Orçamento")
        print("2. Listar Orçamentos")
        print("3. Atualizar Orçamento")
        print("4. Deletar Orçamento")
        print("5. Exportar Dados")
        print("0. Voltar ao Menu Principal")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            adicionar_orcamento(conexao)
        elif opcao == '2':
            listar_orcamentos(conexao)
        elif opcao == '3':
            atualizar_orcamento(conexao)
        elif opcao == '4':
            deletar_orcamento(conexao)
        elif opcao == '5':
            exportar_orcamentos_para_json(conexao)
        elif opcao == '0':
            break
        else:
            print("Opção inválida. Tente novamente.")
            
def exportar_automoveis_para_json(conexao):
    try:
        cursor = conexao.cursor()
        
        # Consulta SQL para obter dados da tabela `t_ws_automovel`
        cursor.execute("SELECT id_automovel, nr_placa, ds_combustivel, nr_renavam, dt_ano_carro, ds_modelo_car, ds_marca, dt_data_compra FROM t_ws_automovel")
        automoveis = cursor.fetchall()

        # Transformar os dados em uma lista de dicionários e formatar datetime para string
        automoveis_json = [
            {
                "id_automovel": automovel[0],
                "nr_placa": automovel[1],
                "ds_combustivel": automovel[2],
                "nr_renavam": automovel[3],
                "dt_ano_carro": automovel[4].strftime("%Y-%m-%d") if automovel[4] else None,
                "ds_modelo_car": automovel[5],
                "ds_marca": automovel[6],
                "dt_data_compra": automovel[7].strftime("%Y-%m-%d") if automovel[7] else None
            }
            for automovel in automoveis
        ]

        # Exportar para JSON
        with open("json_exports/automoveis.json", "w", encoding="utf-8") as f:
            json.dump(automoveis_json, f, ensure_ascii=False, indent=4)

        print("Exportação de automóveis para JSON concluída com sucesso.")
    except Exception as e:
        print("Erro ao exportar automóveis para JSON:", e)

            
def exportar_agendamentos_para_json(conexao):
    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT id_agendamento, t_ws_diagnostico_id_diagnóstico, dt_e_hora, ds_servico FROM t_ws_agendamento")
        agendamentos = cursor.fetchall()

        # Transformar os dados em uma lista de dicionários e formatar datetime para string
        agendamentos_json = [
            {
                "id_agendamento": agendamento[0],
                "id_diagnostico": agendamento[1],
                "data_e_hora": agendamento[2].strftime("%Y-%m-%d %H:%M:%S") if agendamento[2] else None,
                "descricao_servico": agendamento[3]
            }
            for agendamento in agendamentos
        ]

        # Exportar para JSON
        with open("json_exports/agendamentos.json", "w", encoding="utf-8") as f:
            json.dump(agendamentos_json, f, ensure_ascii=False, indent=4)

        print("Exportação de agendamentos para JSON concluída com sucesso.")
    except Exception as e:
        print("Erro ao exportar agendamentos para JSON:", e)


def exportar_orcamentos_para_json(conexao):
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT id_orcamento, dt_emissao, ds_servicos, ds_pecas, vl_custo_total
        FROM t_ws_orcamento
    """)

    orcamentos = cursor.fetchall()

    # Formatação para JSON e conversão de datetime
    orcamentos_json = []
    for orcamento in orcamentos:
        orcamento_dict = {
            "id_orcamento": orcamento[0],
            "dt_emissao": orcamento[1].strftime("%Y-%m-%d") if orcamento[1] else None,
            "ds_servicos": orcamento[2],
            "ds_pecas": orcamento[3],
            "vl_custo_total": float(orcamento[4])
        }
        orcamentos_json.append(orcamento_dict)

    # Verificar se o diretório "json_exports" existe; se não, cria
    if not os.path.exists("json_exports"):
        os.makedirs("json_exports")

    # Exportação para JSON
    with open('json_exports/orcamentos.json', 'w', encoding='utf-8') as f:
        json.dump(orcamentos_json, f, ensure_ascii=False, indent=4)

    print("Exportação de orçamentos concluída com sucesso.")


def exibir_beneficios():
    print("\n=== Benefícios ===")
    print("1. Guincho gratuito")
    print("2. Descontos em estacionamentos")
    print("3. Check-ups grátis")
    print("4. Descontos em serviços de lavagem")

# Funções CRUD para veículos
def adicionar_veiculo(veiculos, nome, marca, modelo, ano, combustivel, cor, placa):
    """Adiciona um novo veículo à lista de veículos."""
    veiculo = {
        "nome": nome,
        "marca": marca,
        "modelo": modelo,
        "ano": ano,
        "combustivel": combustivel,
        "cor": cor,
        "placa": placa
    }
    veiculos.append(veiculo)
    return veiculo

def listar_veiculos(veiculos):
    """Retorna a lista de todos os veículos."""
    if len(veiculos) == 0:
        return "Nenhum veículo encontrado."
    return veiculos

#alterar
# Função para alterar os dados de um veículo
def alterar_veiculo():
    if len(veiculos) == 0:
        print("Nenhum veículo cadastrado. Por favor, cadastre um veículo primeiro.")
        return
    
    print("\n=== Lista de Veículos Cadastrados ===")
    listar_todos_veiculos()  # Mostra a lista de veículos com números
    
    # Selecionar veículo
    while True:
        try:
            opcao = int(input("Escolha o número do veículo que deseja alterar: "))
            if 1 <= opcao <= len(veiculos):
                veiculo_selecionado = veiculos[opcao - 1]
                break
            else:
                print("Opção inválida. Escolha um número dentro da lista de veículos.")
        except ValueError:
            print("Entrada inválida. Digite um número válido.")
    
    # Coletar novos dados
    print(f"\nAlterando dados do veículo {veiculo_selecionado['nome']} - {veiculo_selecionado['placa']}")
    veiculo_selecionado['nome'] = input(f"Digite o novo nome (Atual: {veiculo_selecionado['nome']}): ") or veiculo_selecionado['nome']
    veiculo_selecionado['marca'] = input(f"Digite a nova marca (Atual: {veiculo_selecionado['marca']}): ") or veiculo_selecionado['marca']
    veiculo_selecionado['modelo'] = input(f"Digite o novo modelo (Atual: {veiculo_selecionado['modelo']}): ") or veiculo_selecionado['modelo']
    
    while True:
        try:
            ano = input(f"Digite o novo ano (Atual: {veiculo_selecionado['ano']}): ") or veiculo_selecionado['ano']
            veiculo_selecionado['ano'] = int(ano)
            if 2014 <= veiculo_selecionado['ano'] <= 2025:
                break
            else:
                print("O ano deve ser entre 2014 e 2025.")
        except ValueError:
            print("Por favor, digite um ano válido.")
    
    veiculo_selecionado['combustivel'] = input(f"Digite o novo combustível (Atual: {veiculo_selecionado['combustivel']}): ") or veiculo_selecionado['combustivel']
    veiculo_selecionado['cor'] = input(f"Digite a nova cor (Atual: {veiculo_selecionado['cor']}): ") or veiculo_selecionado['cor']

    while True:
        nova_placa = input(f"Digite a nova placa (Atual: {veiculo_selecionado['placa']}, formato ABC-1234): ").upper() or veiculo_selecionado['placa']
        if validar_placa(nova_placa):
            veiculo_selecionado['placa'] = nova_placa
            break
        else:
            print("Placa inválida. Siga o formato ABC-1234.")

    print(f"\nVeículo '{veiculo_selecionado['nome']}' alterado com sucesso!")
    input("Pressione Enter para continuar...")
    
# Função para excluir um veículo
def excluir_veiculo():
    if len(veiculos) == 0:
        print("Nenhum veículo cadastrado. Por favor, cadastre um veículo primeiro.")
        return
    
    print("\n=== Lista de Veículos Cadastrados ===")
    listar_todos_veiculos()  # Mostra a lista de veículos com números

    # Selecionar veículo
    while True:
        try:
            opcao = int(input("Escolha o número do veículo que deseja excluir: "))
            if 1 <= opcao <= len(veiculos):
                veiculo_selecionado = veiculos.pop(opcao - 1)
                print(f"Veículo '{veiculo_selecionado['nome']}' excluído com sucesso!")
                break
            else:
                print("Opção inválida. Escolha um número dentro da lista de veículos.")
        except ValueError:
            print("Entrada inválida. Digite um número válido.")
    
    input("Pressione Enter para continuar...")

# Funções para o Histórico de Manutenção
def registrar_manutencao(manutencoes, veiculo_nome, tipo, data, detalhes):
    """Registra uma manutenção para um veículo específico."""
    manutencao = {
        "veiculo": veiculo_nome,
        "tipo": tipo,
        "data": data,
        "detalhes": detalhes
    }
    manutencoes.append(manutencao)
    return manutencao

def listar_manutencoes(manutencoes, veiculo_nome):
    """Lista todas as manutenções de um veículo específico."""
    resultado = [manutencao for manutencao in manutencoes if manutencao["veiculo"].lower() == veiculo_nome.lower()]
    return resultado if resultado else "Nenhuma manutenção encontrada para esse veículo."

# Diagnóstico de veículo
# Função para diagnosticar o veículo com base em perguntas de sim/não
def diagnostico_veiculo():
    if len(veiculos) == 0:
        print("Nenhum veículo cadastrado. Por favor, cadastre um veículo primeiro.")
        return

    print("\n=== Diagnóstico de Veículo ===")
    print("Selecione um veículo para diagnóstico:")
    
    # Listar veículos disponíveis para escolha
    for i, veiculo in enumerate(veiculos):
        print(f"{i + 1}. {veiculo['nome']} - {veiculo['placa']}")
    
    # Selecionar veículo
    while True:
        try:
            opcao = int(input("Escolha o número do veículo: "))
            if 1 <= opcao <= len(veiculos):
                veiculo_escolhido = veiculos[opcao - 1]
                break
            else:
                print("Opção inválida. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Digite um número válido.")

    print(f"Veículo selecionado para diagnóstico: {veiculo_escolhido['nome']} - {veiculo_escolhido['placa']}")

    # Perguntas de diagnóstico
    print("\nResponda as perguntas abaixo para diagnosticarmos o problema do veículo.")
    resposta_motor = input("O motor está fazendo ruído estranho? (s/n): ").lower()
    resposta_fumaca = input("Está saindo fumaça do escapamento? (s/n): ").lower()
    resposta_freios = input("Os freios estão falhando? (s/n): ").lower()

    # Lógica de diagnóstico com base nas respostas
    if resposta_motor == 's' and resposta_fumaca == 's':
        print("Possível problema no motor. Recomendado verificar o óleo e o radiador.")
    elif resposta_motor == 's' and resposta_fumaca == 'n':
        print("Pode haver um problema no motor, mas sem sinais de superaquecimento. Verifique os cabos e a correia.")
    elif resposta_freios == 's':
        print("Possível problema nos freios. Recomendado verificar o fluido de freio e as pastilhas.")
    elif resposta_motor == 'n' and resposta_fumaca == 'n' and resposta_freios == 'n':
        print("Nenhum problema evidente detectado. O veículo parece estar em boas condições.")
    else:
        print("Diagnóstico inconclusivo. Recomendado levar o veículo a um mecânico especializado.")

    input("\nPressione Enter para voltar ao menu principal...")

# Benefícios
def beneficios():
    """Exibe os benefícios disponíveis."""
    print("Benefícios disponíveis:")
    print("1. Guincho gratuito para associados.")
    print("2. Desconto de 10% em estacionamentos parceiros.")
    print("3. Check-up anual gratuito para clientes premium.")
    print("4. Serviço de lavagem gratuita a cada 6 meses.")

# Função para limpar o terminal (dependendo do sistema operacional)
def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

# Menu para gerenciar veículos
def criar_sequencia_automovel(conexao):
    with conexao.cursor() as cursor:
        try:
            cursor.execute("SELECT T_WS_AUTOMOVEL_SEQ.NEXTVAL FROM dual")
        except cx_Oracle.DatabaseError as e:
            if "ORA-02289" in str(e):  # Código para sequência inexistente
                cursor.execute("CREATE SEQUENCE T_WS_AUTOMOVEL_SEQ START WITH 11")  # Assume que IDs vão até 10
                conexao.commit()
            else:
                raise e

# Função para adicionar um novo veículo
def adicionar_automovel(conexao):
    criar_sequencia_automovel(conexao)
    with conexao.cursor() as cursor:
        t_ws_cliente_id_cliente = int(input("ID do Cliente: "))
        nr_placa = input("Placa do Veículo: ")
        ds_combustivel = input("Tipo de Combustível: ")
        nr_renavam = int(input("Número do Renavam: "))
        dt_ano_carro = input("Ano do Carro (YYYY-MM-DD): ")
        ds_modelo_car = input("Modelo do Carro: ")
        ds_marca = input("Marca do Carro: ")
        dt_data_compra = input("Data da Compra (YYYY-MM-DD): ")
        
        cursor.execute(
            """
            INSERT INTO t_ws_automovel (
                id_automovel, t_ws_cliente_id_cliente, nr_placa, ds_combustivel,
                nr_renavam, dt_ano_carro, ds_modelo_car, ds_marca, dt_data_compra
            ) VALUES (
                T_WS_AUTOMOVEL_SEQ.NEXTVAL, :t_ws_cliente_id_cliente, :nr_placa,
                :ds_combustivel, :nr_renavam, TO_DATE(:dt_ano_carro, 'YYYY-MM-DD'),
                :ds_modelo_car, :ds_marca, TO_DATE(:dt_data_compra, 'YYYY-MM-DD')
            )
            """,
            t_ws_cliente_id_cliente=t_ws_cliente_id_cliente,
            nr_placa=nr_placa,
            ds_combustivel=ds_combustivel,
            nr_renavam=nr_renavam,
            dt_ano_carro=dt_ano_carro,
            ds_modelo_car=ds_modelo_car,
            ds_marca=ds_marca,
            dt_data_compra=dt_data_compra
        )
        conexao.commit()
        print("Veículo adicionado com sucesso!")

# Função para visualizar os veículos
def listar_automoveis(conexao):
    with conexao.cursor() as cursor:
        cursor.execute("SELECT * FROM t_ws_automovel ORDER BY id_automovel")
        for linha in cursor:
            print(linha)

# Função para atualizar dados de um veículo existente
def atualizar_automovel(conexao):
    listar_automoveis(conexao)
    id_automovel = int(input("Digite o ID do veículo a ser atualizado: "))
    
    t_ws_cliente_id_cliente = int(input("Novo ID do Cliente: "))
    nr_placa = input("Nova Placa do Veículo: ")
    ds_combustivel = input("Novo Tipo de Combustível: ")
    nr_renavam = int(input("Novo Número do Renavam: "))
    dt_ano_carro = input("Novo Ano do Carro (YYYY-MM-DD): ")
    ds_modelo_car = input("Novo Modelo do Carro: ")
    ds_marca = input("Nova Marca do Carro: ")
    dt_data_compra = input("Nova Data da Compra (YYYY-MM-DD): ")

    with conexao.cursor() as cursor:
        cursor.execute(
            """
            UPDATE t_ws_automovel
            SET t_ws_cliente_id_cliente = :t_ws_cliente_id_cliente,
                nr_placa = :nr_placa,
                ds_combustivel = :ds_combustivel,
                nr_renavam = :nr_renavam,
                dt_ano_carro = TO_DATE(:dt_ano_carro, 'YYYY-MM-DD'),
                ds_modelo_car = :ds_modelo_car,
                ds_marca = :ds_marca,
                dt_data_compra = TO_DATE(:dt_data_compra, 'YYYY-MM-DD')
            WHERE id_automovel = :id_automovel
            """,
            t_ws_cliente_id_cliente=t_ws_cliente_id_cliente,
            nr_placa=nr_placa,
            ds_combustivel=ds_combustivel,
            nr_renavam=nr_renavam,
            dt_ano_carro=dt_ano_carro,
            ds_modelo_car=ds_modelo_car,
            ds_marca=ds_marca,
            dt_data_compra=dt_data_compra,
            id_automovel=id_automovel
        )
        conexao.commit()
        print("Veículo atualizado com sucesso!")

# Função para excluir agendamentos relacionados ao diagnóstico antes de excluir o diagnóstico
def excluir_agendamentos_por_diagnostico(conexao, id_diagnostico):
    with conexao.cursor() as cursor:
        cursor.execute("DELETE FROM t_ws_agendamento WHERE t_ws_diagnostico_id_diagnóstico = :id_diagnostico", id_diagnostico=id_diagnostico)
        conexao.commit()

# Função para excluir diagnósticos e agendamentos relacionados ao veículo antes de excluir o próprio veículo
def excluir_diagnosticos_por_automovel(conexao, id_automovel):
    try:
        with conexao.cursor() as cursor:
            # Seleciona os IDs dos diagnósticos que pertencem ao automóvel
            cursor.execute("SELECT id_diagnóstico FROM t_ws_diagnostico WHERE t_ws_automovel_id_automovel = :id_automovel", id_automovel=id_automovel)
            diagnosticos = cursor.fetchall()

            # Exclui os agendamentos vinculados aos diagnósticos selecionados
            for diagnostico in diagnosticos:
                cursor.execute("DELETE FROM t_ws_agendamento WHERE t_ws_diagnostico_id_diagnóstico = :id_diagnostico", id_diagnostico=diagnostico[0])

            # Exclui os diagnósticos
            cursor.execute("DELETE FROM t_ws_diagnostico WHERE t_ws_automovel_id_automovel = :id_automovel", id_automovel=id_automovel)
            conexao.commit()

    except cx_Oracle.DatabaseError as e:
        print("Erro ao excluir diagnósticos por automóvel:", e)


# Função para excluir um veículo com exclusão em cascata manual
def excluir_automovel(conexao):
    try:
        id_automovel = int(input("Digite o ID do automóvel que deseja excluir: "))
        with conexao.cursor() as cursor:
            # Excluir registros em t_ws_relato_manut relacionados ao automóvel
            cursor.execute("DELETE FROM t_ws_relato_manut WHERE t_ws_automovel_id_automovel = :id_automovel", id_automovel=id_automovel)

            # Excluir registros de diagnósticos e agendamentos relacionados ao automóvel
            excluir_diagnosticos_por_automovel(conexao, id_automovel)

            # Agora exclui o automóvel
            cursor.execute("DELETE FROM t_ws_automovel WHERE id_automovel = :id_automovel", id_automovel=id_automovel)
            conexao.commit()

        print("Automóvel e registros associados excluídos com sucesso.")
    except cx_Oracle.IntegrityError as e:
        print("Erro de integridade referencial:", e)
    except cx_Oracle.DatabaseError as e:
        print("Erro ao excluir o automóvel:", e)


# Menu de gerenciamento de veículos
def menu_automoveis(conexao):
    while True:
        print("\nMenu de Gerenciamento de Veículos")
        print("1. Adicionar Veículo")
        print("2. Listar Veículos")
        print("3. Atualizar Veículo")
        print("4. Excluir Veículo")
        print("5. Exportar Dados")
        print("0. Voltar ao Menu Principal")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            adicionar_automovel(conexao)
        elif opcao == "2":
            listar_automoveis(conexao)
        elif opcao == "3":
            atualizar_automovel(conexao)
        elif opcao == "4":
            excluir_automovel(conexao)
        elif opcao == "5":
            exportar_automoveis_para_json(conexao)
        elif opcao == "0":
            break
        else:
            print("Opção inválida. Tente novamente.")

# Integração do me

# Menu de Histórico de Manutenção
def menu_historico_manutencao():
    while True:
        limpar_tela()
        print("\n=== Histórico de Manutenção ===")
        print("1. Registrar Manutenção")
        print("2. Listar Manutenções de um Veículo")
        print("3. Alterar Manutenção")
        print("4. Excluir Manutenção")
        print("0. Voltar ao Menu Principal")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            registrar_manutencao_veiculo()
        elif opcao == "2":
            listar_manutencoes_veiculo()
        elif opcao == "3":
            alterar_manutencao()
        elif opcao == "4":
            excluir_manutencao()
        elif opcao == "0":
            break
        else:
            print("Opção inválida!")
            input("Pressione Enter para continuar...")

# Função para alterar uma manutenção
def alterar_manutencao():
    if len(manutencoes) == 0:
        print("Nenhuma manutenção cadastrada.")
        return
    
    listar_manutencoes_veiculo()
    
    # Selecionar manutenção
    while True:
        try:
            opcao = int(input("Escolha o número da manutenção que deseja alterar: "))
            if 1 <= opcao <= len(manutencoes):
                manutencao_selecionada = manutencoes[opcao - 1]
                break
            else:
                print("Opção inválida. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Digite um número válido.")

    # Alterar dados da manutenção
    print(f"Alterando manutenção do veículo {manutencao_selecionada['veiculo']} - {manutencao_selecionada['placa']}")
    manutencao_selecionada['tipo'] = input(f"Digite o novo tipo de manutenção (Atual: {manutencao_selecionada['tipo']}): ") or manutencao_selecionada['tipo']
    
    while True:
        nova_data = input(f"Digite a nova data (Atual: {manutencao_selecionada['data']}, formato DD/MM/AAAA): ") or manutencao_selecionada['data']
        if validar_data(nova_data):
            manutencao_selecionada['data'] = nova_data
            break
    
    manutencao_selecionada['detalhes'] = input(f"Digite os novos detalhes (Atual: {manutencao_selecionada['detalhes']}): ") or manutencao_selecionada['detalhes']
    
    print(f"Manutenção do veículo '{manutencao_selecionada['veiculo']}' alterada com sucesso!")
    input("Pressione Enter para continuar...")

# Função para excluir uma manutenção
def excluir_manutencao():
    if len(manutencoes) == 0:
        print("Nenhuma manutenção cadastrada.")
        return

    listar_manutencoes_veiculo()

    # Selecionar manutenção
    while True:
        try:
            opcao = int(input("Escolha o número da manutenção que deseja excluir: "))
            if 1 <= opcao <= len(manutencoes):
                manutencao_selecionada = manutencoes.pop(opcao - 1)
                print(f"Manutenção '{manutencao_selecionada['tipo']}' excluída com sucesso!")
                break
            else:
                print("Opção inválida. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Digite um número válido.")
    
    input("Pressione Enter para continuar...")

# Função para validar a placa
def validar_placa(placa):
    if len(placa) == 8 and placa[3] == '-' and placa[:3].isalpha() and placa[4:].isdigit():
        return True
    return False

# Funções de operação
def cadastrar_veiculo():
    nome = input("Digite o nome do veículo: ")
    marca = input("Digite a marca do veículo: ")
    modelo = input("Digite o modelo do veículo: ")

    # Validação do ano do carro (2014-2025)
    while True:
        try:
            ano = int(input("Digite o ano do veículo (entre 2014 e 2025): "))
            if 2014 <= ano <= 2025:
                break
            else:
                print("O ano deve ser entre 2014 e 2025.")
        except ValueError:
            print("Por favor, digite um ano válido.")

    combustivel = input("Digite o tipo de combustível: ")
    cor = input("Digite a cor do veículo: ")

    # Validação da placa
    while True:
        placa = input("Digite a placa do veículo (formato ABC-1234): ").upper()
        if validar_placa(placa):
            break
        else:
            print("Placa inválida. Siga o formato ABC-1234.")

    veiculo = adicionar_veiculo(veiculos, nome, marca, modelo, ano, combustivel, cor, placa)
    print(f"\nVeículo '{veiculo['nome']}' cadastrado com sucesso!")
    input("Pressione Enter para continuar...")

def veiculo_existe(nome_veiculo):
    for veiculo in veiculos:
        if veiculo["nome"].lower() == nome_veiculo.lower():
            return True
    return False

def listar_todos_veiculos():
    lista = listar_veiculos(veiculos)
    if isinstance(lista, str):
        print(f"\n{lista}")
    else:
        print("\n=== Lista de Veículos ===")
        for veiculo in lista:
            print(f"Nome: {veiculo['nome']}, Marca: {veiculo['marca']}, Modelo: {veiculo['modelo']}, Ano: {veiculo['ano']}, Combustível: {veiculo['combustivel']}, Cor: {veiculo['cor']}, Placa: {veiculo['placa']}")
    input("\nPressione Enter para continuar...")

def registrar_manutencao_veiculo():
    if len(veiculos) == 0:
        print("Nenhum veículo cadastrado. Por favor, cadastre um veículo primeiro.")
        return

    print("\n=== Registro de Manutenção ===")
    print("Selecione um veículo:")
    
    # Listar veículos disponíveis para escolha
    for i, veiculo in enumerate(veiculos):
        print(f"{i + 1}. {veiculo['nome']} - {veiculo['placa']}")
    
    # Selecionar veículo
    while True:
        try:
            opcao = int(input("Escolha o número do veículo: "))
            if 1 <= opcao <= len(veiculos):
                veiculo_escolhido = veiculos[opcao - 1]
                break
            else:
                print("Opção inválida. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Digite um número válido.")

    print(f"Veículo selecionado: {veiculo_escolhido['nome']} - {veiculo_escolhido['placa']}")

    # Coletar tipo de manutenção
    tipo = input("Digite o tipo de manutenção (troca de óleo, calibragem, etc.): ")

    # Coletar e validar a data da manutenção
    while True:
        data = input("Digite a data da manutenção (formato DD/MM/AAAA): ")
        if validar_data(data):
            break

    # Coletar detalhes adicionais da manutenção
    detalhes = input("Digite detalhes adicionais da manutenção: ")

    # Registrar a manutenção
    manutencao = {
        "veiculo": veiculo_escolhido['nome'],
        "placa": veiculo_escolhido['placa'],
        "tipo": tipo,
        "data": data,
        "detalhes": detalhes
    }
    manutencoes.append(manutencao)
    print(f"Manutenção para o veículo {veiculo_escolhido['nome']} registrada com sucesso!")

def validar_data(data):
    try:
        # Verifica se a data está no formato correto (dd/mm/aaaa)
        data_formatada = datetime.strptime(data, "%d/%m/%Y")
        ano = data_formatada.year
        # Verifica se o ano está no intervalo permitido
        if 2014 <= ano <= 2025:
            return True
        else:
            print("Erro: O ano deve ser entre 2014 e 2025.")
            return False
    except ValueError:
        print("Erro: A data deve estar no formato DD/MM/AAAA.")
        return False

def listar_manutencoes_veiculo():
    if len(veiculos) == 0:
        print("Nenhum veículo cadastrado. Por favor, cadastre um veículo primeiro.")
        return

    print("\n=== Listar Manutenções ===")
    print("Selecione um veículo para ver o histórico de manutenções:")
    
    # Listar veículos disponíveis para escolha
    for i, veiculo in enumerate(veiculos):
        print(f"{i + 1}. {veiculo['nome']} - {veiculo['placa']}")
    
    # Selecionar veículo
    while True:
        try:
            opcao = int(input("Escolha o número do veículo: "))
            if 1 <= opcao <= len(veiculos):
                veiculo_escolhido = veiculos[opcao - 1]
                break
            else:
                print("Opção inválida. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Digite um número válido.")

    # Listar manutenções do veículo escolhido
    manutencoes_veiculo = [m for m in manutencoes if m["veiculo"] == veiculo_escolhido["nome"]]
    
    if manutencoes_veiculo:
        print(f"\nManutenções do veículo {veiculo_escolhido['nome']}:")
        for manutencao in manutencoes_veiculo:
            print(f"Data: {manutencao['data']}, Tipo: {manutencao['tipo']}, Detalhes: {manutencao['detalhes']}")
    else:
        print(f"Nenhuma manutenção registrada para o veículo {veiculo_escolhido['nome']}.")
    input("Pressione Enter para continuar...")


# Inicia o sistema
if __name__ == "__main__":
    menu()
