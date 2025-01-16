import bcrypt

# Criptografar senha para armazenar no banco de dados
def hash_password(plain_password):
    # Gerar o hash a partir da senha
    hashed = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')  # Conversão para string


# Checar se a senha está correta
def check_password(plain_password, hashed_password):
    # Comparar a senha fornecida com o hash armazenado
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
