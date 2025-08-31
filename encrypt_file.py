import yaml
from cryptography.fernet import Fernet


def encrypting():

    key=Fernet.generate_key()
    with open('secret.key','wb') as key_file:
        key_file.write(key)

    with open('config.yaml','rb') as f:
        yaml_data=f.read()

    fernet=Fernet(key)
    encrypted_data=fernet.encrypt(yaml_data)

    with open("config.yaml.enc", "wb") as f:
        f.write(encrypted_data)


def decrypt():
    with open('secret.key',"rb") as key_file:
        key=key_file.read()

    with open("config.yaml.enc") as f:
        encrypt_data=f.read()

    fernet=Fernet(key)
    decrypted_data=fernet.decrypt(encrypt_data)
    return decrypted_data







