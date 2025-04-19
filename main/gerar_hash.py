import bcrypt

# Este script serve para gerar o hash seguro de uma senha usando o algoritmo bcrypt.
# O sistema de controle de estoque utiliza senhas criptografadas para proteger os dados dos usuários.

# Altere aqui para a senha que deseja registrar no banco de dados (ex: "1234")
senha = "1234".encode('utf-8')

# Gera um hash seguro da senha utilizando bcrypt
hash_gerado = bcrypt.hashpw(senha, bcrypt.gensalt())

# Exibe o hash gerado no terminal
print("Hash gerado':")
print(hash_gerado.decode())

# Instruções para inserção no banco:
#
# 1. Copie o hash gerado acima e use em um comando Mysql para inserir um novo usuário no banco e poder se logar no sistema:
#
#    Exemplo:
#    INSERT INTO TBL_USUARIO (nome_usuario, senha, id_tipo_usuario)
#    VALUES ('admin', '<cole_o_hash_aqui>', 1);
#
# 2. Certifique-se de que o valor "1" em id_tipo_usuario corresponde ao tipo 'administrador' na tabela TBL_TIPO_USUARIO.
#
# 3. Com isso feito, você poderá fazer login no sistema com:
#    Usuário: admin
#    Senha: 1234
