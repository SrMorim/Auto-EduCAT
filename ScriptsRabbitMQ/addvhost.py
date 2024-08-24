import subprocess

def main():
    # Solicitar informações do usuário
    vhost = input("Digite o nome do vhost: ")
    password = input("Digite a senha para o usuário: ")

    # Executar os comandos no RabbitMQ
    commands = [
        f"rabbitmqctl add_vhost {vhost}",
        f"rabbitmqctl add_user {vhost} {password}",
        f"rabbitmqctl set_permissions -p {vhost} {vhost} \".*\" \".*\" \".*\""
    ]

    for command in commands:
        execute_command(command)

def execute_command(command):
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"Comando executado com sucesso: {command}")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o comando {command}: {e}")
        exit(1)

if __name__ == "__main__":
    main()