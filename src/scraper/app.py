import importlib


def choose_plataform():

    print("Escolha  a plataforma de empregos: ")
    print("1 - Linkedin")
    print("2 - Glassdoor")
    print("3 - Infojobs")
    print("4 - Vagas")

    options = {
        1: "linkedin_scraper",
        2: "glassdoor_scraper",
        3: "infojobs_scraper",
        4: "vagas_scraper",
    }

    option = int(input())

    if option in options:

        print("Carregando...")
        scraper = importlib.import_module(options[option])
        scraper.run()


if __name__ == "__main__":
    choose_plataform()
