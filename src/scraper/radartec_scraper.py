import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from tqdm import tqdm
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from time import sleep
from vagas_scraper import is_looping

options = Options()
options.add_argument("-headless")
firefox = webdriver.Firefox(options=options)
wait = WebDriverWait(firefox, 10)


def search_job(query):
    search_input = wait.until(EC.visibility_of_element_located((By.NAME, "q")))

    search_input.send_keys(query)
    sleep(0.5)
    search_input.send_keys(Keys.ENTER)


def set_filers():
    quantity_select = wait.until(
        EC.visibility_of_element_located((By.NAME, "quantidade"))
    )
    quantity_select.click()
    sleep(0.5)
    quantity_options = quantity_select.find_elements(By.TAG_NAME, "option")
    quantity_options[2].click()
    sleep(0.5)

    sort_select = wait.until(EC.visibility_of_element_located((By.NAME, "ordem")))
    sort_select.click()
    sleep(0.5)
    sort_options = sort_select.find_elements(By.TAG_NAME, "option")
    sort_options[0].click()


def get_jobs():
    jobs_cards = wait.until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "vote-item"))
    )

    formatted_jobs = []

    for job in jobs_cards:
        job_title = job.find_element(By.CLASS_NAME, "vote-title").text
        job_link = job.find_element(By.CLASS_NAME, "vote-title").get_attribute("href")
        job_salary = job.find_element(By.CLASS_NAME, "salario").text
        job_location = job.find_element(By.CLASS_NAME, "cidade").text
        job_post_date = job.find_element(By.CLASS_NAME, "info-data").text

        new_job = {
            "name": job_title,
            "salary": job_salary,
            "location": job_location,
            "post_date": job_post_date.strip(),
            "link": job_link,
        }
        formatted_jobs.append(new_job)
    return formatted_jobs


def save_jobs(jobs):

    file_name = "vagas" + datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = f"src/jobs/radartec/{file_name}.json"

    with open(file_path, mode="w", encoding="utf-8") as file:
        file.write("[\n")

        for i, job in enumerate(tqdm(jobs, "Salvando vagas")):
            json.dump(job, file, ensure_ascii=False, indent=4)

            if i < len(jobs) - 1:
                file.write(",\n")
        file.write("\n]")
    print(f"📁 Arquivo salvo com sucesso em {file_path}!")


def run():
    firefox.get("https://radartec.com.br/")
    query = input("Digite a vaga desejada: ")

    is_loop = is_looping()

    times = 0

    if is_loop is not False:
        while times < is_loop[1]:
            times += 1
            firefox.get("https://radartec.com.br/")
            search_job(query)
            sleep(0.5)
            set_filers()
            sleep(0.5)
            save_jobs(get_jobs())
            sleep(is_loop[0])
    else:
        search_job(query)
        sleep(0.5)
        set_filers()
        sleep(0.5)
        save_jobs(get_jobs())

    firefox.quit()
