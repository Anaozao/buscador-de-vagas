import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from tqdm import tqdm
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

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
        job_location = (
            card_footer.find_element(By.CLASS_NAME, "vaga-local")
            .find_element(By.TAG_NAME, "i")
            .text
        )

        job_release_date = (
            card_footer.find_element(By.CLASS_NAME, "data-publicacao")
            .find_element(By.TAG_NAME, "i")
            .text
        )

        job_data = {
            "name": job_name,
            "location": job_location,
            "release_date": job_release_date,
            "link": job_link,
        }

        jobs_list.append(job_data)
    return jobs_list


def save_jobs(jobs: list):

    file_path = f"src/jobs/vagas/vagas-{datetime.now().date()}.json"

    with open(file_path, mode="w", encoding="utf-8") as file:
        file.write("[\n")

        for i, job in enumerate(tqdm(jobs, desc="Salvando vagas:")):
            json.dump(job, file, ensure_ascii=False, indent=4)
            if i < len(jobs) - 1:
                file.write(",\n")
        file.write("\n]")
    print(f"📁 Arquivo salvo com sucesso em {file_path}!")


def run():

    query = input("Digite a vaga desejada: ")
    print("carregando...")
    firefox.get("https://www.vagas.com.br/vagas-de-" + query)

    save_jobs(format_jobs_data())
