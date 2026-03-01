from playwright.sync_api import sync_playwright
from faker import Faker
import csv
import time

fake = Faker("pt_BR")

TOTAL_USERS = 1000

def gerar_dados():
    return {
        "nome": fake.name(),
        "senha": fake.password(length=10),
        "mensagem": fake.text(max_nb_chars=50)
    }

def salvar_dados(dados):
    with open("resultado.csv", mode="w", newline="", encoding="utf-8") as arquivo:
        writer = csv.DictWriter(arquivo, fieldnames=["nome", "senha", "mensagem"])
        writer.writeheader()
        writer.writerows(dados)

def main():
    dados_gerados = []
    
    with sync_playwright() as p:
        navegador = p.chromium.launch(headless=True)
        pagina = navegador.new_page()

        for i in range(TOTAL_USERS):
            dados = gerar_dados()

            pagina.goto("https://www.selenium.dev/selenium/web/web-form.html")

            pagina.get_by_label("Text input").fill(dados["nome"])
            pagina.get_by_label("Password").fill(dados["senha"])
            pagina.get_by_label("Textarea").fill(dados["mensagem"])

            pagina.get_by_role("button", name="Submit").click()
            pagina.wait_for_load_state()

            dados_gerados.append(dados)

            print(f"Usuário {i+1}/{TOTAL_USERS} - Usuário caddastrado: {dados['nome']} ")
        navegador.close()
    salvar_dados(dados_gerados)
    print("Processo concluído. Dados salvos em resultado.csv")
if __name__ == "__main__":    
    main()