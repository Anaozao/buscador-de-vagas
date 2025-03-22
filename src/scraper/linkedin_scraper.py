import getpass
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import json
from dotenv import load_dotenv
import os
from tqdm import tqdm
from datetime import datetime

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()

url = "https://www.linkedin.com/jobs/"
options = Options()
options.add_argument("--headless")

firefox = webdriver.Firefox(options=options)


def select_time_range(selected_time_range, time_options):
    if selected_time_range == 1:
        time_options[0].click()
    elif selected_time_range == 2:
        time_options[1].click()
    elif selected_time_range == 3:
        time_options[2].click()
    elif selected_time_range == 4:
        time_options[3].click()
    else:
        print("Opção inválida. Digite uma das opções acima")
        new_option = int(input())
        select_time_range(new_option, time_options)


def login(wait: WebDriverWait, env_email="", env_pass=""):
    if env_email and env_pass:
        email_input = wait.until(EC.presence_of_element_located((By.ID, "session_key")))
        email_input.send_keys(env_email)

        password_input = wait.until(
            EC.presence_of_element_located((By.ID, "session_password"))
        )
        password_input.send_keys(env_pass)

    else:
        print("Necessário fazer login")
        email = input("Digite seu e-mail: ")
        password = getpass.getpass("Digite sua senha: ")

        email_input = wait.until(EC.presence_of_element_located((By.ID, "session_key")))
        email_input.send_keys(email)

        password_input = wait.until(
            EC.presence_of_element_located((By.ID, "session_password"))
        )
        password_input.send_keys(password)

    enter_btn = firefox.find_element(
        By.CLASS_NAME, "sign-in-form__submit-btn--full-width"
    )

    enter_btn.send_keys(Keys.ENTER)

    try:
        wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "global-nav__me-photo"))
        )
        print("✅ Login bem-sucedido!")
        return True
    except:
        print("Senha ou usuário inválidos")
        return False


def search(wait: WebDriverWait):
    search_input = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "jobs-search-box__text-input"))
    )

    query = input("Digite a vaga desejada: ")

    search_input.send_keys(query)
    search_input.send_keys(Keys.ENTER)

    print("Selecione o tempo de postagem da vaga: ")
    print("1 - Qualquer momento")
    print("2 - No último mês")
    print("3 - Na última semana")
    print("4 - Nas últimas 24 horas")

    selected_time_range = int(input())

    time_posted = wait.until(
        EC.element_to_be_clickable(((By.ID, "searchFilter_timePostedRange")))
    )
    time_posted.click()

    time_options = firefox.find_elements(By.CLASS_NAME, "search-reusables__value-label")

    select_time_range(selected_time_range, time_options)
    print("Carregando...")

    buttons_div = firefox.find_element(By.CLASS_NAME, "reusable-search-filters-buttons")
    filter_btn = buttons_div.find_elements(By.TAG_NAME, "button")[1]
    filter_btn.click()


def scrape_jobs():
    jobs_cards = firefox.find_elements(By.CLASS_NAME, "job-card-container")

    while True:
        last_job = jobs_cards[-1]
        last_job.location_once_scrolled_into_view
        sleep(2)

        new_jobs_cards = firefox.find_elements(By.CLASS_NAME, "job-card-container")

        if len(new_jobs_cards) == len(jobs_cards):
            break

        jobs_cards = new_jobs_cards

    jobs = []
    for job in jobs_cards:
        jobs_links = job.find_element(By.CLASS_NAME, "job-card-container__link")

        job_name = jobs_links.get_attribute("aria-label")
        job_link = jobs_links.get_attribute("href")

        job_card_metadata = job.find_element(
            By.CLASS_NAME, "job-card-container__metadata-wrapper"
        )
        metadata_info = job_card_metadata.find_element(By.TAG_NAME, "span").text

        job_data = {"name": job_name, "location": metadata_info, "link": job_link}

        jobs.append(job_data)
        return jobs


def save_jobs(jobs):

    file_path = f"src/jobs/linkedin/vagas-{datetime.now()}.json"

    with open(file_path, mode="w", encoding="utf-8") as file:

        file.write("[\n")

        for i, job in enumerate(tqdm(jobs, desc="Salvando vagas")):
            json.dump(job, file, ensure_ascii=False, indent=4)
            if i < len(jobs) - 1:
                file.write(",\n")
        file.write("\n]")

    print(f"📁 Arquivo salvo com sucesso em {file_path}!")


def run():
    firefox.get("https://www.linkedin.com/jobs/")
    wait = WebDriverWait(firefox, 10)
    env_email = os.getenv("LINKEDIN_EMAIL") or ""
    env_pass = os.getenv("LINKEDIN_PASSWORD") or ""

    if login(wait, env_email=env_email, env_pass=env_pass) is True:

        search(wait)

        jobs = scrape_jobs()

        save_jobs(jobs)

        firefox.quit()
    else:
        login(wait)
