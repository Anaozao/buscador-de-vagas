import getpass
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import json
from dotenv import load_dotenv
import os

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


def login(env_email, env_pass):
    if env_email and env_pass:
        email_input = firefox.find_element(By.ID, "session_key")
        email_input.send_keys(env_email)

        password_input = firefox.find_element(By.ID, "session_password")
        password_input.send_keys(env_pass)

    else:
        print("Necessário fazer login")
        email = input("Digite seu e-mail: ")
        password = getpass.getpass("Digite sua senha: ")

        email_input = firefox.find_element(By.ID, "session_key")
        email_input.send_keys(email)

        password_input = firefox.find_element(By.ID, "session_password")
        password_input.send_keys(password)

    enter_btn = firefox.find_element(
        By.CLASS_NAME, "sign-in-form__submit-btn--full-width"
    )

    enter_btn.send_keys(Keys.ENTER)


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
    jobs_cards = firefox.find_elements(By.CLASS_NAME, "job-card-container__link")

    while True:
        last_job = jobs_cards[-1]
        last_job.location_once_scrolled_into_view
        sleep(2)

        new_jobs_cards = firefox.find_elements(
            By.CLASS_NAME, "job-card-container__link"
        )

        if len(new_jobs_cards) == len(jobs_cards):
            break

        jobs_cards = new_jobs_cards

    jobs = []

    for job in jobs_cards:

        job_name = job.get_attribute("aria-label")
        job_link = job.get_attribute("href")

        job_data = {"vaga": job_name, "link": job_link}

        jobs.append(job_data)

    with open("src/jobs/vagas.json", mode="w", encoding="utf-8") as file:
        json.dump(jobs, file, ensure_ascii=False, indent=4)


def run():
    firefox.get("https://www.linkedin.com/jobs/")
    wait = WebDriverWait(firefox, 10)
    env_email = os.getenv("LINKEDIN_EMAIL")
    env_pass = os.getenv("LINKEDIN_PASSWORD")

    login(env_email, env_pass)

    search(wait)

    scrape_jobs()

    firefox.quit()
