import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from tqdm import tqdm
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from time import sleep

options = Options()
options.add_argument("--headless")

firefox = webdriver.Firefox(options=options)
wait = WebDriverWait(firefox, 10)


def get_jobs():
    jobs_cards = wait.until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "vaga"))
    )
    return jobs_cards


def format_jobs_data():
    jobs = get_jobs()

    jobs_list = []

    for job in jobs:

        job_name = job.find_element(By.TAG_NAME, "a").get_attribute("title")
        job_link = job.find_element(By.TAG_NAME, "a").get_attribute("href")
        card_footer = job.find_element(By.TAG_NAME, "footer")
        job_location = card_footer.find_element(By.CLASS_NAME, "vaga-local").text

        job_release_date = card_footer.find_element(
            By.CLASS_NAME, "data-publicacao"
        ).text

        job_data = {
            "name": job_name,
            "location": job_location,
            "release_date": job_release_date,
            "link": job_link,
        }

        jobs_list.append(job_data)
    return jobs_list


def save_jobs(jobs: list):
    filename = "vagas-" + datetime.now().strftime("%Y%m%d_%H%M%S")

    file_path = f"src/jobs/vagas/{filename}.json"

    with open(file_path, mode="w", encoding="utf-8") as file:
        file.write("[\n")

        for i, job in enumerate(tqdm(jobs, desc="Salvando vagas:")):
            json.dump(job, file, ensure_ascii=False, indent=4)
            if i < len(jobs) - 1:
                file.write(",\n")
        file.write("\n]")
    print(f"📁 Arquivo salvo com sucesso em {file_path}!")


def is_looping():
    response = input("Deseja rodar o programa em loop (S/N)? ").strip().lower()

    if response not in ["s", "n"]:
        print("Opção inválida, tente novamente")
        return is_looping()

    if response == "s":
        while True:
            try:
                loop_time = float(
                    input(
                        "Digite o tempo em minutos, para cada loop (Ex: 1 ou 3.5 etc.): "
                    )
                )
                if loop_time > 0:
                    break
                else:
                    print("O tempo deve ser um número positivo.")
            except ValueError:
                print("Entrada inválida! Digite um número válido.")

        while True:
            try:
                loop_times = int(input("Digite a quantidade de loops: "))
                if loop_times > 0:
                    break
                else:
                    print("A quantidade de loops deve ser um número positivo inteiro.")
            except ValueError:
                print("Entrada inválida! Digite um número inteiro válido.")

        minutes_to_seconds = loop_time * 60
        return (minutes_to_seconds, loop_times)

    return False


def run():

    query = input("Digite a vaga desejada: ")
    print("carregando...")
    firefox.get("https://www.vagas.com.br/vagas-de-" + query)

    times = 0

    is_loop = is_looping()

    if is_loop is not False:

        while times < is_loop[1]:
            times += 1
            firefox.get("https://www.vagas.com.br/vagas-de-" + query)
            save_jobs(format_jobs_data())
            sleep(is_loop[0])
    else:
        save_jobs(format_jobs_data())

    firefox.quit()
