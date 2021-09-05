from os import stat
import sqlite3
import UniHelper_library as lib
from selenium import webdriver as Unistudium

def main():
    # istanzio un unico driver in quanto c'è un unico thread
    opt = Unistudium.ChromeOptions()
    # Disabilita caricamento immagini
    prefs = {"profile.managed_default_content_settings.images": 2}
    opt.add_experimental_option("prefs", prefs)
    opt.headless = True
    driver = Unistudium.Chrome('chromedriver', options=opt)

    lezione = lib.Lezioni(driver)
    esame = lib.Esami(driver)
    laurea = lib.Lauree(driver)
    conn = sqlite3.connect('UniHelper.db')
    c = conn.cursor()

    print('\nUpdate Lezione:')
    c.execute('SELECT insegnamento FROM Lezione')
    conn.commit()
    insegnamenti = c.fetchall()
    for insegnamento in insegnamenti:
        res, status = lezione.getLezione(insegnamento[0].split(
            " -- ", 1)[1], True)  # ottengo un risultato univoco
        if (status == -1):
            break
        if(not res):
            c.execute('DELETE FROM Lezione WHERE insegnamento=?'(insegnamento[0]))
            conn.commit()

    print('\nUpdate Esame:')
    c.execute('SELECT insegnamento FROM Esame')
    conn.commit()
    insegnamenti = c.fetchall()
    for insegnamento in insegnamenti:
        res, status = esame.getEsame(insegnamento[0].split(
            " -- ", 1)[1], True)  # ottengo un risultato univoco
        if (status == -1):
            break
        if(not res):
            c.execute('DELETE FROM Esame WHERE insegnamento=?'(insegnamento[0]))
            conn.commit()

    print('\nUpdate Laurea:')
    # ottengo una lista di dipartimenti del db senza ripetizioni e aggiorno tutti i record associati
    c.execute('SELECT DISTINCT dipartimento FROM Laurea')
    conn.commit()
    dipartimenti = c.fetchall()
    for dipartimento in dipartimenti:
        res, status = laurea.getLauree(dipartimento[0], True)
        if (status == -1):
            break
        if(not res):
            c.execute('DELETE FROM Laurea WHERE dipartimento=?'(dipartimento[0]))
            conn.commit()

    del lezione, esame, laurea
    conn.close()

if __name__ == "__main__":
    main()
