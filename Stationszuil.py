import datetime
import random
import psycopg2
''''geimporteerde libraries'''

'''Een functie die de user vraagt om input. Op basis van de input zal dit geschreven worden naar een file en database.'''
def bericht():
    station = ['Amsterdam', 'Den Haag', 'Utrecht']
    randomstation = random.choice(station)
    database = open('database.csv', 'a')
    tijd = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    naam = input('Welkom!\nVoer uw naam in a.u.b.: ')
    '''als de naam niet wordt ingevuld. wordt de user als anoniem aangemeld.'''
    if naam == '':
        naam = 'Anoniem'
    bericht = input('Welkom! ' + naam +'\n' + 'Voer uw bericht van maximaal 140 karakters in dit venster.: ')
    '''print een bericht als de karakters langer zijn dan 140'''
    if len(bericht) > 140:
        print('Uw bericht is te lang. Hanteer de 140 karakters. ')
        '''write naar een file met een input format. Daarna wordt het geschreven naar een sql database.'''
    else:
        database.write("{},{},{},{}".format(naam,bericht,str(tijd),randomstation))
        database.write('\n')
        connection_string = "host= 'localhost' dbname='stationszuil' user='postgres' password='Mrin123'"

        conn = psycopg2.connect(connection_string)
        cursor = conn.cursor()

        query = """INSERT INTO opmerking(naam, bericht, berichtdatum, station_servicestation_city)
                                   VALUES (%s, %s, %s, %s);"""
        data = (naam, bericht, tijd, randomstation)
        cursor.execute(query, data)
        conn.commit()
        cursor.close()
        conn.close()
        database.close()
        print('Bedankt ' + naam + ' voor het helpen om de NS te verbeteren!')
        return bericht




