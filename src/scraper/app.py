import importlib


def choose_plataform():

    print("Escolha a plataforma de empregos: ")
    print("1 - Linkedin")
    print("2 - Vagas")
    print("3 - Radartec")

    options = {1: "linkedin_scraper", 2: "vagas_scraper", 3: "radartec_scraper"}

    option = int(input())

    if option in options:

        print("Carregando...")
        scraper = importlib.import_module(options[option])
        scraper.run()
    else:
        print("Opção inválida")
        choose_plataform()


if __name__ == "__main__":
    choose_plataform()
