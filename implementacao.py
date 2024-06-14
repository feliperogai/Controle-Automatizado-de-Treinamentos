import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import os

# Função para inicializar o banco de dados SQLite
def init_db():
    conn = sqlite3.connect('training_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trainings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_name TEXT NOT NULL,
            procedure_name TEXT NOT NULL,
            status TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Função para importar dados de um arquivo Excel para o banco de dados
def import_data(file_path):
    df = pd.read_excel(file_path)
    conn = sqlite3.connect('training_data.db')
    df.to_sql('trainings', conn, if_exists='append', index=False)
    conn.close()

# Função para visualizar todos os dados de treinamentos
def view_data():
    conn = sqlite3.connect('training_data.db')
    df = pd.read_sql_query('SELECT * FROM trainings', conn)
    conn.close()
    print(df)

# Função para gerar gráficos de visualização
def generate_dashboard():
    conn = sqlite3.connect('training_data.db')
    df = pd.read_sql_query('SELECT * FROM trainings', conn)
    conn.close()

    pending_trainings = df[df['status'] == 'pending'].groupby('procedure_name').size()

    plt.figure(figsize=(10, 6))
    pending_trainings.plot(kind='bar')
    plt.xlabel('Procedure Name')
    plt.ylabel('Pending Count')
    plt.title('Pending Trainings by Procedure')
    plt.tight_layout()

    if not os.path.exists('output'):
        os.makedirs('output')
    
    plt.savefig('output/pending_trainings_dashboard.png')
    plt.show()

# Função para exportar dados filtrados para um novo arquivo Excel
def export_filtered_data(status, output_file):
    conn = sqlite3.connect('training_data.db')
    df = pd.read_sql_query('SELECT * FROM trainings WHERE status = ?', conn, params=(status,))
    conn.close()
    df.to_excel(output_file, index=False)
    print(f'Dados exportados para {output_file}')

# Função principal para o menu da CLI
def main():
    init_db()
    while True:
        print("\nSistema de Controle de Treinamentos")
        print("1. Importar dados de Excel")
        print("2. Visualizar dados")
        print("3. Gerar dashboard de treinamentos pendentes")
        print("4. Exportar dados filtrados")
        print("5. Sair")
        
        choice = input("Escolha uma opção: ")
        
        if choice == '1':
            file_path = input("Digite o caminho do arquivo Excel: ")
            import_data(file_path)
            print("Dados importados com sucesso.")
        elif choice == '2':
            view_data()
        elif choice == '3':
            generate_dashboard()
        elif choice == '4':
            status = input("Digite o status para filtrar (e.g., pending, completed): ")
            output_file = input("Digite o nome do arquivo de saída (e.g., filtered_data.xlsx): ")
            export_filtered_data(status, output_file)
        elif choice == '5':
            print("Saindo do sistema.")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == '__main__':
    main()
