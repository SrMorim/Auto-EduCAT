import subprocess
import json

def detach_policy_from_entities(policy_arn):
    try:
        # Desanexar de usuários
        result = subprocess.run(
            ["aws", "iam", "list-entities-for-policy", "--policy-arn", policy_arn],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        entities = json.loads(result.stdout)

        # Desanexar de usuários
        for user in entities.get('PolicyUsers', []):
            subprocess.run(
                ["aws", "iam", "detach-user-policy", "--user-name", user['UserName'], "--policy-arn", policy_arn],
                check=True
            )
            print(f"Policy {policy_arn} desanexada do usuário {user['UserName']}.")

        # Desanexar de grupos
        for group in entities.get('PolicyGroups', []):
            subprocess.run(
                ["aws", "iam", "detach-group-policy", "--group-name", group['GroupName'], "--policy-arn", policy_arn],
                check=True
            )
            print(f"Policy {policy_arn} desanexada do grupo {group['GroupName']}.")

        # Desanexar de roles
        for role in entities.get('PolicyRoles', []):
            subprocess.run(
                ["aws", "iam", "detach-role-policy", "--role-name", role['RoleName'], "--policy-arn", policy_arn],
                check=True
            )
            print(f"Policy {policy_arn} desanexada da role {role['RoleName']}.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao desanexar policy {policy_arn}: {e.stderr}")

def delete_policy_version(policy_arn, version_id):
    try:
        subprocess.run(
            ["aws", "iam", "delete-policy-version", "--policy-arn", policy_arn, "--version-id", version_id],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print(f"Versão {version_id} da policy {policy_arn} deletada com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao deletar a versão {version_id} da policy {policy_arn}: {e.stderr}")

def list_policy_versions(policy_arn):
    try:
        result = subprocess.run(
            ["aws", "iam", "list-policy-versions", "--policy-arn", policy_arn],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        versions = json.loads(result.stdout)["Versions"]
        return versions
    except subprocess.CalledProcessError as e:
        print(f"Erro ao listar versões da policy {policy_arn}: {e.stderr}")
        return []

def delete_all_policy_versions(policy_arn):
    versions = list_policy_versions(policy_arn)
    
    for version in versions:
        # Deleta todas as versões que não são padrão (IsDefaultVersion=False)
        if not version["IsDefaultVersion"]:
            delete_policy_version(policy_arn, version["VersionId"])

def delete_aws_policy(policy_arn):
    try:
        # Desanexar a policy de todas as entidades
        detach_policy_from_entities(policy_arn)

        # Deletar todas as versões da policy
        delete_all_policy_versions(policy_arn)
        
        # Deletar a policy
        subprocess.run(
            ["aws", "iam", "delete-policy", "--policy-arn", policy_arn],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print(f"Policy {policy_arn} deletada com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao deletar policy {policy_arn}: {e.stderr}")

def delete_policies(policy_arns):
    for arn in policy_arns:
        delete_aws_policy(arn)
        
if __name__ == "__main__":
    # Lista de ARNs das políticas que você deseja deletar
    policies_to_delete = [
        '',
        '',
        '',
        '',
        '',
        ''
    ]
    # Deleta as políticas listadas
    delete_policies(policies_to_delete)