from selenium import webdriver
import sqlite3 as database
import time


def check(a, b):
    for text in a:
        if text in b:
            return 1
    return 0


conn = database.connect('UniHelper.db')
c = conn.cursor()
anno = time.strftime("%Y")
url = f"https://www.unipg.it/didattica/offerta-formativa/offerta-formativa-{anno}-{str(int(anno[2]+anno[3])+1)}?ricerca=on&annoregolamento={anno}&dipartimento=&lingua=&tipocorso=&sede=&nomecorso=&cerca=Cerca"
opt = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
opt.add_experimental_option("prefs", prefs)
opt.headless = True
driver = webdriver.Chrome('chromedriver', options=opt)
driver.get(url)
avoid = ["Accesso:", "Modalità Didattica:", "Lingua: "]
Xpath = "//td"
rows = 1+len(driver.find_elements_by_xpath(Xpath))
cols = len(driver.find_elements_by_xpath(Xpath))

corso = []
x = ""
for field in driver.find_elements_by_xpath(Xpath):
    if field.text and not check(avoid, field.text):
        # print(field.text.strip())
        if not check(["LM-", "L/", "L-"], field.text):
            if x:
                print(corso[0], corso[1], corso[2], x)
                c.execute(
                    'INSERT OR IGNORE INTO CorsoLaurea(corso_laurea,dipartimento,classe) VALUES (?,?,?);', (corso[0], corso[1], x))
                conn.commit()
                x = ""
                corso = []
            corso.append(field.text.strip())
        else:
            x = x+field.text.strip()+"#"
print(rows, cols)
conn.close()