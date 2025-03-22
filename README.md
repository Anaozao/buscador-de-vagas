Este repositório contém um programe que faz scraping de vagas de trabalho em alguns sites.

Até o momento o programa analisa vagas no Vagas.com e Linkedin.com.

Utilizando Python e Selenium, o programa coleta e salva os dados das vagas em /src/jobs/...

Crie o arquivo .env conforme o exemplo (.env.example) para adicionar os dados de login do LinkedIn para login automatico. Caso não queira, ao rodar o programa será solicitado as credenciais para logar manualmente.

Para utilizar o programa (necessário ter o navegador Firefox):

1 - Clone o repositório

2 - Crie o ambiente virtual com o comando  ( caso esteja no bash do linux ):
    python3 -m venv .venv && source .venv/bin/activate

    !! Caso não esteja no bash do linux, verifique como criar e ativar o ambiente virtural em sua máquina !!

3 - Instale as dependências com o comando:
    pip install -r src/requirements.txt

4 - Rode o aplicativo com o comando:
    python src/scraper/app.py (garanta que o ambiente virtual está ativo para funcionar)
