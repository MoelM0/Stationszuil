from tkinter import *
from PIL import Image, ImageFont, ImageDraw, ImageTk
import psycopg2
import json
import requests
'''we importeren alle libraries die we nodig hebben.'''


'''verbinding maken met onze database'''
root = Tk()
root.title('Stationszuil')
root.geometry('1920x1080')
root.config(bg='#FFC917')
root.attributes("-fullscreen", True)


'''attributen voor de ns logo op het scherm'''
img = PhotoImage(file="ns.png")
my_label = Label(root, image=img, bg='#FFC917')
my_label.place(x=1200, y=50)


'''Een api functie waarmee we de plain data callen van het weer obv van station'''
def api(station):
    resource_uri = f"https://api.openweathermap.org/data/2.5/weather?q={station}&appid=77da6dfe5d30b373fc029bbcb920b890"
    response = requests.get(resource_uri)
    response_data = response.json()
    weer = response_data['main']
    return round((float(weer['temp']) - 273.15), 1) #De API geeft de temperatuur in Kelvin weer ipv Celcius.
    # Dus zie hier berekening

'''Een functie waarmee we logos van de api callen'''
def logos(station):
    resource_uri = f"https://api.openweathermap.org/data/2.5/weather?q={station}&appid=77da6dfe5d30b373fc029bbcb920b890"
    response = requests.get(resource_uri)
    response_data = response.json()
    weer = ((response_data['weather'])[0])
    return weer['icon']

'''De hoofd functie van de weersmodule. Laat obv stationsnaam en directory het logo en het weer zien.'''
def hetweer(station):
    img = PhotoImage(file=f'weather_icons/{logos(station)}@2x.png')
    weer = Label(master=root, background='#FFC917', foreground='#FFC917', width=300, height=175, image=img)
    weer.img = img
    weer.place(x=1350, y=400)
    weer2 = Label(master=root, text=f"{api(station)} C° in {station}", background='#FFC917', foreground='#003082',
                  font=('Helvetica', 20, 'bold'))
    weer2.place(x=1350, y=530)

'''Hier bevindt zich alle 3 de buttons om het weer op te halen voor elk station.'''
amsterdamButton = Button(master=root, text='Amsterdam', height=3, width=15, fg='white', font=15, bg='#003082',
                             command=lambda: hetweer("Amsterdam"))
amsterdamButton.place(x=1500, y=300)

denhaagButton = Button(master=root, text='Den Haag', height=3, width=15, fg='white', font=15, bg='#003082',
                           command=lambda: hetweer('Den Haag'))
denhaagButton.place(x=1350, y=300)

utrechtButton = Button(master=root, text='Utrecht', height=3, width=15, fg='white', font=15, bg='#003082',
                           command=lambda: hetweer('Utrecht'))
utrechtButton.place(x=1200, y=300)



'''Een functie die de database opent en een query uitvoert die de laatste 5 opmerkingen laat zien.'''
connection_string = "host= 'localhost' dbname='stationszuil' user='postgres' password='Mrin123'"

conn = psycopg2.connect(connection_string)
cursor = conn.cursor()
query = "SELECT * FROM opmerking ORDER BY bericht_id DESC LIMIT 5;"
cursor.execute(query)
conn.commit()

'''Variabel om alle data op te vragen. Dit is nodig om de data in tkinter te zetten. We maken hier alvast een list van
zodat we kunnen indexen.'''
berichten = cursor.fetchall()
berichten = list(berichten)



'''Geimporteerde logos van NS faciliteiten.'''
lift_img = PhotoImage(file=f'ov_icons/img_lift.png')
ov_fiets_img = PhotoImage(file=f'ov_icons/img_ovfiets.png')
pr_img = PhotoImage(file=f'ov_icons/img_pr.png')
toilet_img = PhotoImage(file=f'ov_icons/img_toilet.png')




'''
Dit is een for loop die we maken zodat we de queries kunnen formateren en in tkinter kunnen zetten.
Het is een for loop dat steeds +1 groter wordt voor de layout van tkinter en automatisch verschuift
door de rij en kolom variables.
'''
rij = 0
for row in berichten:
    rij += 1
    cursor.execute(f"SELECT * FROM station_service "
                   f"WHERE station_city = '{row[6]}'; ")

    '''

    De nsfaciliteiten variabel hebben we gemaakt om de data op te slaan van de query execute hierboven.
    We hebben hierbij de 6e row gebruikt omdat die over de stad gaat. Echter halen we alle data
    eruit zodat we dit op kunnen slaan in onze nieuwe nsfaciliteiten variable.
    '''
    nsfaciliteiten = (cursor.fetchall())[0]
    station_city, country, ov_bike, elevator, toilet, park_and_ride = nsfaciliteiten

    kolom = 0

    '''Hier maken we de labels voor de faciliteiten. We zorgen ervoor dus met behulp van de variable 'kolom' en 'rij'
    dat steeds een kolom en rij opschuift bij elke faciliteit.'''
    if ov_bike:
        ov_fiets_logo = Label(master=root, image=ov_fiets_img, background='#003082', width=128, height=128, )
        ov_fiets_logo.grid(column=kolom, row=rij)
        kolom += 1
    if elevator:
        lift_logo = Label(master=root, image=lift_img, background='#003082', width=128, height=128, )
        lift_logo.grid(column=kolom, row=rij)
        kolom += 1
    if toilet:
        toilet_logo = Label(master=root, image=toilet_img, background='#003082', width=128, height=128, )
        toilet_logo.grid(column=kolom, row=rij)
        kolom += 1
    if park_and_ride:
        pr_logo = Label(master=root, image=pr_img, background='#003082', width=128, height=128, )
        pr_logo.grid(column=kolom, row=rij)
        kolom += 1
#We resetten de kolom weer naar 0 omdat we niet willen dat onze comment betrekking heeft tot de kolomverschuivingen.
    kolom = 0

    '''De label die de comments laat zien. Dit wordt 5 keer geloopt.'''
    comment_label = Label(master=root,
                          text=f"Bericht van {row[0]} met als opmerking '{row[1]}' op station {row[6]} op {row[4]}",
                          background='#003082',  # NS geel
                          foreground='white',  # NS blauw
                          font=('Helvetvica', 13, 'bold'),
                          width=90,
                          height=2,
                          )
    comment_label.grid(column=5, row=rij, columnspan=1, ipady=40)


root.mainloop()
