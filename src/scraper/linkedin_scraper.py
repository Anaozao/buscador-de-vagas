import getpass
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import json

# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

url = "https://www.linkedin.com/jobs/"
options = Options()
# options.add_argument("--headless")

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


def run():
    firefox.get("https://www.linkedin.com/jobs/")
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

    sleep(3)

    search_input = firefox.find_element(By.CLASS_NAME, "jobs-search-box__text-input")

    query = input("Digite a vaga desejada: ")

    search_input.send_keys(query)
    search_input.send_keys(Keys.ENTER)

    print("Selecione o tempo de postagem da vaga: ")
    print("1 - Qualquer momento")
    print("2 - No último mês")
    print("3 - Na última semana")
    print("4 - Nas últimas 24 horas")

    selected_time_range = int(input())

    time_posted = firefox.find_element(By.ID, "searchFilter_timePostedRange")
    time_posted.click()

    time_options = firefox.find_elements(By.CLASS_NAME, "search-reusables__value-label")

    select_time_range(selected_time_range, time_options)
    print("Carregando...")

    buttons_div = firefox.find_element(By.CLASS_NAME, "reusable-search-filters-buttons")
    filter_btn = buttons_div.find_elements(By.TAG_NAME, "button")[1]
    filter_btn.click()

    jobs_cards = firefox.find_elements(By.CLASS_NAME, "job-card-container__link")

    jobs = []

    for job in jobs_cards:
        # base_url = "https://www.linkedin.com"

        job_name = job.get_attribute("aria-label")
        job_link = job.get_attribute("href")

        job_data = {"vaga": job_name, "link": job_link}

        jobs.append(job_data)

    with open("src/jobs/vagas.json", mode="w", encoding="utf-8") as file:
        json.dump(jobs, file, ensure_ascii=False, indent=4)

    # firefox.quit()
