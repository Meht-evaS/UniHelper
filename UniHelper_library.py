from selenium import webdriver as Unistudium
import sqlite3 as ConnessioneDatabase

class GestioneUtente:
    def __init__(self, id: str):
        self.__conn = ConnessioneDatabase.connect('UniHelper.db')
        self.__c = self.__conn.cursor()
        self.__id = id
        self.__corso=None
        self.__c.execute('SELECT * FROM Utente WHERE id_utente = ?;', (id,))
        self.__conn.commit()
        results = self.__c.fetchall()
        if(results):
            self.__last = results[0][1]  # ultimo comando richiesto
            self.__corso = results[0][2]
        else:
            self.__c.execute(
                "INSERT INTO Utente(id_utente,ultimo_comando) VALUES (?,?);", (id, 0))
            self.__conn.commit()
            self.__last = 0  # se non esiste in db non ha ancora richiesto comandi

    def setLast(self, last: int):
        self.__last = last
        self.__c.execute(
            'UPDATE Utente SET ultimo_comando=? WHERE id_utente=?;', (last, self.__id))
        self.__conn.commit()
    
    def setCorso(self, corso: str, delete=False): 
        if(delete):
            self.__c.execute(
                'UPDATE Utente SET corso_laurea=? WHERE id_utente=?;', (None, self.__id))
            self.__conn.commit()
            self.__corso=None
            return None
        if (len(corso)>3): 
            self.__c.execute(
                'SELECT corso_laurea FROM CorsoLaurea WHERE corso_laurea LIKE ?;', (f"%{corso}%",))
            self.__conn.commit()
            corsi = self.__c.fetchall()
            if len(corsi)>1:
                for res in corsi:
                    if res[0]==corso:
                        self.__corso=res[0]
                        self.__c.execute(
                            'UPDATE Utente SET corso_laurea=? WHERE id_utente=?;', (self.__corso, self.__id))
                        return f"✅Ho impostato il corso {self.__corso}",1
                text="Non ho capito :(\n\nIntendevi per caso uno di questi? \n"
                for res in corsi:
                    text=text+res[0]+"\n"
                return text+"(Se sì inseriscilo in chat o inserisci un corso specifico)",0
            elif len(corsi)==1:
                self.__corso=corsi[0][0]
                self.__c.execute(
                    'UPDATE Utente SET corso_laurea=? WHERE id_utente=?;', (self.__corso, self.__id))
                return f"✅Ho impostato il corso {self.__corso}",1
            return "Nessun corso trovato, inseriscine uno valido:",0
        return "Imposta un corso valido:",0

    def getCorso(self):
        return self.__corso

    def getLast(self) -> int:
        return self.__last

    def __del__(self):  # chiudo la connessione
        self.__conn.close()

class Ricerca:
    def __init__(self):
        self._conn = ConnessioneDatabase.connect('UniHelper.db')
        self._c = self._conn.cursor()

    def _ricerca_unistudium(self, url, ricerca):
        try:
            if self._driver == None:
                opt = Unistudium.ChromeOptions()
                # Disabilita caricamento immagini
                prefs = {"profile.managed_default_content_settings.images": 2}
                opt.add_experimental_option("prefs", prefs)
                opt.headless = True
                self._driver = Unistudium.Chrome('chromedriver', options=opt)
            self._driver.get(url)
            form = self._driver.find_element_by_xpath(
                '/html/body/form/input[1]')
            form.send_keys(ricerca)
            link = self._driver.find_element_by_xpath(
                '/html/body/form/input[2]')
            link.click()

            page_source = self._driver.page_source
            tables = page_source.split('/tr>')
            counter = 0
        except Exception as e:
            print('errore connessione unistudium: ', e)
            return [], -1
        for table in tables:
            counter = counter + 1

        result = []
        if counter == 1:
            return result, 0
            # return f'Per {ricerca} non sono stati trovati risultati'
        # mi creo la lista delle lezioni a partire dall'indice 0
        for i in range(1, counter-1, 1):  # 1° e ultimo elemento counter non sono lezioni
            result.append('')
            result[i-1] = ((tables[i].split('<tr>'))[1]).split('<td>')
            result[i-1].pop(0)
            # Elimino lo spazio che c'è sempre prima del nome dei prof
            result[i-1][1] = result[i-1][1].strip()
        return result, counter

    def __del__(self):  # chiudo la connessione
        self._conn.close()


class Lezioni(Ricerca):

    def __init__(self, driver=None):
        super().__init__()
        self._driver = driver

    def getLezione(self, ricerca: str, update=False):
        if (len(ricerca)<4):
            return [],0
        if(not update):
            self._c.execute(
                "SELECT * FROM Lezione WHERE insegnamento LIKE ? OR docenti LIKE ?", ('%'+ricerca+'%', '%'+ricerca+'%'))
            self._conn.commit()
            results = self._c.fetchall()
            if(results):
                return results, 1
        res, counter = self._ricerca_unistudium(
            "https://www.unistudium.unipg.it/cercacorso.php?p=0", ricerca)
        if(res):
            for i in range(1, counter-1, 1):
                # ogni elemento in result conterrà 4 campi
                for x in range(0, 4, 1):
                    res[i-1][x] = (res[i-1][x].split('</td>'))[0]
                    if x == 3:
                        res[i-1][x] = (((res[i-1][x].split('<a href="'))
                                       [1]).split('"'))[0]
            for i in range(0, len(res), 1):
                insegnamento = res[i][0]
                docenti = res[i][1]
                corso_laurea = res[i][2]
                link = res[i][3]
                self._c.execute(
                    'INSERT OR REPLACE INTO Lezione(insegnamento,docenti,corso_laurea,link) VALUES (?,?,?,?);', (insegnamento, docenti, corso_laurea, link))
                self._conn.commit()
        return res, counter


class Esami(Ricerca):

    def __init__(self, driver=None):
        super().__init__()
        self._driver = driver

    def getEsame(self, ricerca: str, update=False):
        if (len(ricerca)<4):
            return [],0
        if(not update):
            self._c.execute(
                'SELECT * FROM Esame WHERE insegnamento LIKE ? OR docenti LIKE ?', ('%'+ricerca+'%', '%'+ricerca+'%'))
            self._conn.commit()
            results = self._c.fetchall()
            if(results):
                return results, 1
        res, counter = self._ricerca_unistudium(
            "https://www.unistudium.unipg.it/cercacorso.php?p=1", ricerca)
        if(res):
            for i in range(1, counter-1, 1):
                # ogni elemento conterrà 5 campi
                for x in range(0, 5):
                    res[i-1][x] = (res[i-1][x].split('</td>'))[0]
                    if x == 4:
                        res[i-1][x] = (((res[i-1][x].split('<a href="'))
                                       [1]).split('"'))[0]
            for i in range(0, len(res), 1):
                insegnamento = res[i][0]
                docenti = res[i][1]
                corso_laurea = res[i][2]
                data_orario = res[i][3]
                link = res[i][4]
                self._c.execute(
                    'INSERT OR REPLACE INTO Esame(insegnamento,docenti,corso_laurea,data_orario,link) VALUES (?,?,?,?,?);', (insegnamento, docenti, corso_laurea, data_orario, link))
                self._conn.commit()
        return res, counter


class Lauree(Ricerca):

    def __init__(self, driver=None):
        super().__init__()
        self._driver = driver

    def getLauree(self, ricerca: str, update=False):
        if (len(ricerca)<4):
            return [],0
        if(not update):
            self._c.execute(
                'SELECT * FROM Laurea WHERE dipartimento LIKE ? OR corso_laurea LIKE ?', ('%'+ricerca+'%', '%'+ricerca+'%'))
            self._conn.commit()
            results = self._c.fetchall()
            if(results):
                return results, 1
        res, counter = self._ricerca_unistudium(
            "https://www.unistudium.unipg.it/cercacorso.php?p=245", ricerca)
        if(res):
            for i in range(1, counter-1, 1):
                # ogni elemento conterrà 4 campi
                for x in range(0, 4, 1):
                    res[i-1][x] = (res[i-1][x].split('</td>'))[0]
                    if x == 3:
                        res[i-1][x] = ((((res[i-1][x].split('"'))[49]).split(': '))[1])
                    elif x == 4:
                        res[i-1][x] = ((res[i-1][x].split('"'))[55])
            for i in range(0, len(res), 1):
                dipartimento = res[i][0]
                corso_laurea = res[i][1]
                data_orario = res[i][2]
                utente_interno = res[i][3]
                self._c.execute(
                    'INSERT OR REPLACE INTO Laurea(dipartimento,corso_laurea,data_orario,codice) VALUES (?,?,?,?);', (dipartimento, corso_laurea, data_orario, utente_interno))
                self._conn.commit()
        return res, counter
