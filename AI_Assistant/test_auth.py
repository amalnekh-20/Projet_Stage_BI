from azure.identity import InteractiveBrowserCredential


print("Ouverture de l'authentification Microsoft...")

credential = InteractiveBrowserCredential()

token = credential.get_token(
    "https://database.windows.net/.default"
)

print("Authentification réussie !")
print("Token obtenu.")
print("Expiration :", token.expires_on)