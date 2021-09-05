#!/usr/bin/python3
# -*- coding: utf-8 -*-
import time, re, telebot
from telebot import types
import UniHelper_library as lib

def deEmojify(text):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)

def main():
    API_TOKEN = 'Insert your token'  # @unipghelperbot
    bot = telebot.TeleBot(API_TOKEN)

    @bot.message_handler(commands=['start'])
    def send_welcome(message, exText=[]):
        text = "Ciao! Io sono Unipg Helper!\n\nPuoi utilizzarmi per ricercare i link delle stanze virtuali delle lezioni.\nClicca /help per scoprire come trovare un link!"
        if exText:
            text = exText
        utente = lib.GestioneUtente(message.chat.id)
        utente.setLast(0)
        mkup = types.InlineKeyboardMarkup(row_width=4)
        buttons = [types.InlineKeyboardButton("Help 🆘", callback_data="help")]
        buttons.append(types.InlineKeyboardButton(
            "Ricerca lezioni 🔍", callback_data="ricerca_lezioni"))
        buttons.append(types.InlineKeyboardButton(
            "Ricerca Esami 🔍", callback_data="ricerca_esami"))
        buttons.append(types.InlineKeyboardButton(
            "Ricerca Lauree 🔍", callback_data="ricerca_lauree"))
        if not utente.getCorso():
            buttons.append(types.InlineKeyboardButton(
                "Imposta il tuo Corso 📖", callback_data="imposta_corso"))
        else:
            buttons.append(types.InlineKeyboardButton(
                "Reimposta/Elimina il tuo Corso 📖", callback_data="imposta_corso"))
        for button in buttons:
            mkup.add(button)
        bot.send_message(message.chat.id, text, reply_markup=mkup)
        del utente

    @bot.callback_query_handler(func=lambda call: call.data == 'annulla')
    def annulla(call):
        utente = lib.GestioneUtente(call.message.chat.id)
        utente.setLast(0)
        send_welcome(call.message, "🔝Sei tornato al menù principale\n👇🏻Se vuoi effettuare un'altra operazione premi qua sotto👇🏻")
        del utente

    @bot.message_handler(commands=['esterno'])
    def utente_esterno(message):
        text = " Per l'accesso come utente esterno collegati al sito [Unistudium Ricerca Lauree](https://www.unistudium.unipg.it/cercacorso.php?p=245) per visionare il regolamento, acconsentire al trattamento dei dati e richiedere l'accesso inoltrando la propria email"
        bot.send_message(message.chat.id, text, parse_mode='MarkdownV2')

    @bot.callback_query_handler(func=lambda call: call.data == 'imposta_corso')
    def imposta_corso(call):
        utente = lib.GestioneUtente(call.message.chat.id)
        utente.setLast(4)
        corso=utente.getCorso()
        if corso:
            text=f"Corso attuale: {corso}\nInserisci il nome del tuo corso per filtrare le tue ricerche o utilizza il bottone per eliminare quello attuale"
        else:
            text="Nessun corso attualmente impostato\nInserisci il nome del tuo corso per filtrare le tue ricerche:"
        mkup = types.InlineKeyboardMarkup(row_width=2)
        mkup.add(types.InlineKeyboardButton("Elimina Corso ❌", callback_data="del_corso"))
        mkup.add(types.InlineKeyboardButton("Annulla 🔙", callback_data="annulla"))
        bot.send_message(call.message.chat.id, text, reply_markup=mkup)
        del utente

    @bot.callback_query_handler(func=lambda call: call.data == 'del_corso')
    def del_corso(call):
        utente = lib.GestioneUtente(call.message.chat.id)
        utente.setLast(0)
        if utente.getCorso():
            utente.setCorso(None,True)
            send_welcome(call.message, "✅Corso eliminato con successo!\n👇🏻Se vuoi effettuare un'altra operazione premi qua sotto👇🏻")
        else:
            send_welcome(call.message, "❌Nessun corso attualmente impostato\n👇🏻Se vuoi effettuare un'altra operazione premi qua sotto👇🏻")
        del utente

    @bot.callback_query_handler(func=lambda call: call.data == 'ricerca_lezioni')
    def ricerca_lezioni_call(call):
        utente = lib.GestioneUtente(call.message.chat.id)
        utente.setLast(1)
        mkup = types.InlineKeyboardMarkup(row_width=1)
        mkup.add(types.InlineKeyboardButton("Annulla 🔙", callback_data="annulla"))
        text = "Inserisci il nome del professore o dell'insegnamento da ricercare: "
        bot.send_message(call.message.chat.id, text, reply_markup=mkup)
        del utente

    @bot.callback_query_handler(func=lambda call: call.data == 'ricerca_esami')
    def ricerca_esami_call(call):
        utente = lib.GestioneUtente(call.message.chat.id)
        utente.setLast(2)
        mkup = types.InlineKeyboardMarkup(row_width=1)
        mkup.add(types.InlineKeyboardButton("Annulla 🔙", callback_data="annulla"))
        text = "Inserisci il nome del professore o dell'insegnamento da ricercare: "
        bot.send_message(call.message.chat.id, text, reply_markup=mkup)
        del utente

    @bot.callback_query_handler(func=lambda call: call.data == 'ricerca_lauree')
    def ricerca_lauree_call(call):
        utente = lib.GestioneUtente(call.message.chat.id)
        utente.setLast(3)
        mkup = types.InlineKeyboardMarkup(row_width=1)
        mkup.add(types.InlineKeyboardButton("Annulla 🔙", callback_data="annulla"))
        text = f"Inserisci il nome del Corso di Studi e/o nome del Dipartimento da ricercare: "
        bot.send_message(call.message.chat.id, text, reply_markup=mkup)
        del utente

    @bot.callback_query_handler(func=lambda call: call.data == 'help')
    def help_handler(call):
        utente = lib.GestioneUtente(call.message.chat.id)
        utente.setLast(0)
        bot.send_message(call.message.chat.id, "Ciao! Utilizza /start per cominciare, ti verranno inviati i comandi del bot. \n\n🔍 Per ricercare lezioni/esami e lauree usa il bottone 'Ricerca Lezioni/Esami/Lauree' e digita il nome del docente o del corso che vuoi ricercare\n\n📖 Il tuo corso verrà usato per filtrare e personalizzare le ricerche, per impostarlo, modificarlo o eliminarlo usa il bottone imposta/reimposta/elimina corso")

    @bot.message_handler(commands=['help'])
    def send_help(message):
        utente = lib.GestioneUtente(message.chat.id)
        utente.setLast(0)
        bot.send_message(message.chat.id, "Ciao! Utilizza /start per cominciare, ti verranno inviati i comandi del bot. \n\n🔍 Per ricercare lezioni/esami e lauree usa il bottone 'Ricerca Lezioni/Esami/Lauree' e digita il nome del docente o del corso che vuoi ricercare\n\n📖 Il tuo corso verrà usato per filtrare e personalizzare le ricerche, per impostarlo, modificarlo o eliminarlo usa il bottone imposta/reimposta/elimina corso")

    @bot.message_handler(func=lambda message: True)
    def argument_handler(message):
        try:
            utente = lib.GestioneUtente(message.chat.id)
            corso=utente.getCorso()
            if corso:
                corso=corso.lower()
            if utente.getLast() == 1:
                ricerca = lib.Lezioni()
                lezioni,status = ricerca.getLezione(deEmojify(message.text),1)
                
                if corso:
                    tempLezioni=[]
                    for lezione in lezioni:
                        try:
                            if corso == lezione[2].split("]")[1].strip().lower():
                                tempLezioni.append(lezione)
                        except:
                            if corso and (corso in lezione[2].lower()):
                                tempLezioni.append(lezione)
                    print(message.chat.id,"Ricerca:",message.text,"in lezioni con corso:",corso,"filtrate:",len(lezioni)-len(tempLezioni),"di",len(lezioni))
                    lezioni=tempLezioni
                else:
                    print(message.chat.id,"Ricerca:",message.text,"in lezioni senza corso, n. risultati:",len(lezioni))
                if lezioni:
                    c = 0
                    for lezione in lezioni:
                        if c % 20 == 0:
                            time.sleep(1)
                        c = c+3
                        mkup = types.InlineKeyboardMarkup(row_width=1)
                        itembtn1 = types.InlineKeyboardButton(
                            "Link meeting", url=lezione[3])

                        mkup.add(itembtn1)
                        text = f'<b>Insegnamento</b>: {lezione[0]}\n<b>Docente</b>: {lezione[1]}\n<b>Corso di laurea</b>: {lezione[2]}'
                        bot.send_message(message.chat.id, text,
                                        reply_markup=mkup, parse_mode='html')
                    utente.setLast(0)

                    mkup = types.InlineKeyboardMarkup(row_width=1)
                    itembtn1 = types.InlineKeyboardButton(
                        "Ricerca lezioni", callback_data="ricerca_lezioni")
                    mkup.add(itembtn1)
                    text = "👇🏻Se vuoi effettuare un'altra ricerca premi qua sotto👇🏻\n      altrimenti premi /start"
                    bot.send_message(message.chat.id, text, reply_markup=mkup)

                elif not status==-1:
                    mkup = types.InlineKeyboardMarkup(row_width=1)
                    mkup.add(types.InlineKeyboardButton("Annulla 🔙", callback_data="annulla"))
                    text = f'Non sono stati trovati risultati...\nInserisci un Docente/Insegnamento valido'
                    bot.send_message(message.chat.id, text, reply_markup=mkup)
                else:
                    bot.reply_to(
                        message, f'Non sono stati trovati risultati nel database locale, unistudium è al momento irraggiungibile...\nRiprova più tardi')
                del ricerca

            elif utente.getLast() == 2:
                ricerca = lib.Esami()
                esami, status = ricerca.getEsame(deEmojify(message.text),1)
                if corso:
                    tempEsami=[]
                    for esame in esami:
                        if (corso == esame[2].lower()):
                            tempEsami.append(esame)
                    print(message.chat.id,"Ricerca:",message.text,"in esami con corso:",corso,"filtrati:",len(esami)-len(tempEsami),"di",len(esami))
                    esami=tempEsami
                else:
                    print(message.chat.id,"Ricerca:",message.text,"in esami senza corso, n. risultati:",len(esami))
                c = 0
                if esami:
                    for esame in esami:
                        if c % 20 == 0:
                            time.sleep(1)
                        c = c+3
                        mkup = types.InlineKeyboardMarkup(row_width=1)
                        itembtn1 = types.InlineKeyboardButton(
                            "Link meeting", url=esame[4])
                        mkup.add(itembtn1)
                        text = f'<b>Insegnamento</b>: {esame[0]}\n<b>Docente</b>: {esame[1]}\n<b>Corso di laurea</b>: {esame[2]}\n<b>Data ed ora appello</b>: {esame[3]}'
                        bot.send_message(message.chat.id, text,
                                        reply_markup=mkup, parse_mode='html')
                    utente.setLast(0)
                    mkup = types.InlineKeyboardMarkup(row_width=1)
                    itembtn1 = types.InlineKeyboardButton(
                        "Ricerca esami", callback_data="ricerca_esami")
                    mkup.add(itembtn1)
                    text = "👇🏻Se vuoi effettuare un'altra ricerca premi qua sotto👇🏻\n      altrimenti premi /start"
                    bot.send_message(message.chat.id, text, reply_markup=mkup)

                elif not status==-1:
                    mkup = types.InlineKeyboardMarkup(row_width=1)
                    mkup.add(types.InlineKeyboardButton("Annulla 🔙", callback_data="annulla"))
                    text = f'Non sono stati trovati risultati...\nInserisci un Docente/Insegnamento valido'
                    bot.send_message(message.chat.id, text, reply_markup=mkup)
                else:
                    bot.reply_to(
                        message, f'Non sono stati trovati risultati nel database locale, unistudium è al momento irraggiungibile...\nRiprova più tardi')
                del ricerca

            elif utente.getLast() == 3:
                ricerca = lib.Lauree()
                lauree, status = ricerca.getLauree(deEmojify(message.text),1)
                if corso:
                    tempLauree=[]
                    for laurea in lauree:
                        if corso in laurea[1].lower():
                            tempLauree.append(laurea)
                    print(message.chat.id,"Ricerca:",message.text,"in lauree con corso:",corso,"filtrate:",len(lauree)-len(tempLauree),"di",len(lauree))
                    lauree=tempLauree
                else:
                    print(message.chat.id,"Ricerca:",message.text,"in lauree senza corso, n. risultati:",len(lauree))
                if lauree:
                    text = " E' necessario aver preso visione del [Regolamento](https://www\.unipg\.it/files/statuto-regolamenti/regolamenti/reg-esami-online\.pdf) di Ateneo per lo svolgimento degli esami di profitto e delle sedute di laurea in modalità a distanza dell'Università degli Studi di Perugia, ed, in particolare, dell'art\.5 comma 5 e 6"
                    bot.send_message(message.chat.id, text, parse_mode='MarkdownV2')
                    c = 0
                    for laurea in lauree:
                        if c % 20 == 0:
                            time.sleep(1)
                        c = c+3
                        text = f'<b>Dipartimento</b>: {laurea[0]}\n<b>Corso di Laurea in</b>: {laurea[1]}\n<b>Seduta - Data ed ora</b>: {laurea[2]} \n<b>ACCESSO utente INTERNO UniPg</b>: {laurea[3]}\n<b>RICHIESTA ACCESSO utente ESTERNO</b>: /esterno '
                        bot.send_message(message.chat.id, text, parse_mode='html')
                    utente.setLast(0)
                    mkup = types.InlineKeyboardMarkup(row_width=1)
                    itembtn1 = types.InlineKeyboardButton(
                        "Ricerca lauree", callback_data="ricerca_lauree")
                    mkup.add(itembtn1)
                    text = "👇🏻Se vuoi effettuare un'altra ricerca premi qua sotto👇🏻\n      altrimenti premi /start"
                    bot.send_message(message.chat.id, text, reply_markup=mkup)

                elif not status==-1:
                    mkup = types.InlineKeyboardMarkup(row_width=1)
                    mkup.add(types.InlineKeyboardButton("Annulla 🔙", callback_data="annulla"))
                    text = f'Non sono stati trovati risultati...\nInserisci un Corso di Laurea o nome del Dipartimento valido'
                    bot.send_message(message.chat.id, text, reply_markup=mkup)
                else:
                    bot.reply_to(
                        message, f'Non sono stati trovati risultati nel database locale, unistudium è al m omento irraggiungibile...\nRiprova più tardi')
                del ricerca        

            elif utente.getLast() == 4:
                text,status=utente.setCorso(deEmojify(message.text))
                if status:
                    utente.setLast(0)
                    send_welcome(message,text+"\n👇🏻Se vuoi effettuare un'altra operazione premi qua sotto👇🏻")
                else:
                    bot.reply_to(message,text)
            else:
                text = "Mi spiace, non ho capito cosa mi hai chiesto.\nUsa i bottoni inline per interagire con il bot"
                send_welcome(message, text)
            del utente
        except  Exception:
            print('Telegram timeout API... waiting few seconds')
            time.sleep(1)
    bot.polling()


if __name__ == "__main__":
    main()
