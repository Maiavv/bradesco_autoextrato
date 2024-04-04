# %%
from selenium import webdriver
from datetime import datetime as dt
from datetime import time as tm
if __name__ == "__main__":
    from bradesco_autoextrato import executar
else:
    from .bradesco_autoextrato import executar
import os
import schedule
import time

# %%
link = "https://www.ne12.bradesconetempresa.b.br/ibpjlogin/login.jsf"
username = os.environ.get("login_bradesco")
passwd = os.environ.get("senha_bradesco")

# %%
def job():
    agora = dt.now()
    if agora.time() <= tm(20) and agora.hour >= 8:
        try:
            executar(username, passwd, link)
        except Exception as e:
            print("Erro ao executar o job: ", e, agora)

#D
try:
    executar(username, passwd, link)
except Exception as e:
    print("Erro ao executar o job: ", e)

schedule.every(10).minutes.do(job)
while True:
    schedule.run_pending()
    time.sleep(30)
