import datetime
import csv
import psycopg2
'''geimporteerde libraries'''

'''een functie die de moderator vraagt om input. De moderator wordt dan gevraagd om een opmerking goed of af te keuren.
Wanneer dit is gedaan zal er geschreven worden naar de database.'''

def moderatie():
    modID = input('Voer uw naam in: ')
    email = input('Voer uw email adres in: ')
    tijd = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    welkommod = 'Welkom ' + modID + '!'
    print(welkommod)

    '''opent de database in reader mode'''
    with open('database.csv', 'r') as database:
        read = database.readlines()

        '''een for loop die na elke line de opmerking van de gebruiker formatteerd.'''
        for line in read:
            line = line.strip('\n')
            line = line.split(';')
            print('Te modereren bericht: ' + str(line))
            moderator = input('Keurt u het bericht goed? Beantwoord met Y/N:')

            ''''een if statement die wanneer er als input 'Y' wordt getoetst, een line schrijft met
            de goedgekeurde data en schrijft naar de database'''
            if moderator == 'Y':
                with open('goedgekeurd.csv', 'a') as goedgekeurd:
                    goedgekeurd.write("{},{},{},{},{} \n".format(line, modID, email, tijd, 'Goedgekeurd'))
                print('U heeft het bericht goedgekeurd\n')

                connection_string = "host= 'localhost' dbname='stationszuil' user='postgres' password='Mrin123'"

                conn = psycopg2.connect(connection_string)
                cursor = conn.cursor()

                query = """INSERT INTO moderator(naam, email, keuringdatum, keuring)
                           VALUES (%s, %s, %s, %s);"""
                data = (modID, email, tijd, 'goedgekeurd')
                cursor.execute(query, data)
                conn.commit()
                cursor.close()
                conn.close()
                f = open("database.csv", "a")
                f.truncate(0)
                f.close()
                '''een elif statement die wanneer er 'N' wordt ingetoets, de beoordeling afkeurt en schrijft naar
                de afgekeurde csv file en database.'''
            elif moderator == 'N':
                with open('afgekeurd.csv', 'a') as afgekeurd:
                    afgekeurd.write("{},{},{},{},{} \n".format(line, modID, email, tijd, 'Afgekeurd'))
                print('U heeft het bericht afgekeurd')
                connection_string = "host= 'localhost' dbname='stationszuil' user='postgres' password='Mrin123'"

                conn = psycopg2.connect(connection_string)
                cursor = conn.cursor()

                query = """INSERT INTO moderator(naam, email, keuringdatum, keuring)
                                          VALUES (%s, %s, %s, %s);"""
                data = (modID, email, tijd, "afgekeurd")
                cursor.execute(query, data)
                conn.commit()
                cursor.close()
                conn.close()
                f = open("database.csv", "a")
                f.truncate(0)
                f.close()
                ''''wanneer er een verkeerde input is gekozen.'''
            else:
                print('Onjuiste keuze.')
                return moderatie()

moderatie()

