from os import link
import sqlite3

def main():
    conn=sqlite3.connect('UniHelper.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE CorsoLaurea
                ([corso_laurea] text,[dipartimento] text,[classe] text, PRIMARY KEY (corso_laurea))''')
    c.execute('''CREATE TABLE Lezione
                ([insegnamento] text,[docenti] text, [corso_laurea] text, [link] text, PRIMARY KEY (insegnamento), FOREIGN KEY (corso_laurea) REFERENCES CorsoLaurea (corso_laurea))''')
    c.execute('''CREATE TABLE Utente
                ([id_utente] text,[ultimo_comando] integer,[corso_laurea] text, PRIMARY KEY (id_utente), FOREIGN KEY (corso_laurea) REFERENCES CorsoLaurea (corso_laurea))''')
    c.execute('''CREATE TABLE Esame
                ([insegnamento] text,[docenti] text,[corso_laurea] text,[data_orario] text, [link] text, PRIMARY KEY (insegnamento), FOREIGN KEY (corso_laurea) REFERENCES CorsoLaurea (corso_laurea))''')
    c.execute('''CREATE TABLE Laurea
                ([dipartimento] text,[corso_laurea] text,[data_orario] text,[codice] text, PRIMARY KEY (data_orario, codice), FOREIGN KEY (corso_laurea) REFERENCES CorsoLaurea (corso_laurea))''')    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()
