# sääennusteen visualisointi, asennus ohjeet ja päivitysideoita.
Sovellus hakee OpenWeatherMap API:sta 7 päivän sääennusteen käyttäjän valitsemasta kaupungista ja käyttöliittymä näyttää taulukon sekä kaavion lämpötilojen kehityksestä Chart.js-kirjaston avulla.

Sovellus toimii sivulla: https://saaennusteen-visualisointi.onrender.com/?city=2

# Step by step asennus omalle koneelle:

1. Varmista, että sinulla on Python (Minulla oli projektia tehdessä 3.13.6) ja tämän voit tarkistaa VS Coden terminaalista komennolla:      
 `python --version` tai `python3 --version`

3. Kloonaa repositorio täältä painamalla vihreää code nappia: <img width="910" height="451" alt="image" src="https://github.com/user-attachments/assets/e67c6ef9-71d3-476f-8cc4-915c6f48df03" />

4. Avaa VS Code ja Welcome ruudussa voit painaa "Clone Git Repository..." joka avaa kentän mihin voit kopioida repositorion linkin:<img width="1201" height="793" alt="image" src="https://github.com/user-attachments/assets/e9970513-4322-48d3-ad46-58dd2cab5578" />

5. Sinun pitäisi päästä suoraan projektin juureen jossa sijaitsee manage.py tiedosto:<img width="1917" height="1079" alt="image" src="https://github.com/user-attachments/assets/d3920f94-b265-4ec7-b21f-2327d6efebef" />

6. Varmista vielä, että olet projektin juurikansiossa. Esimerkiksi oikea klikkaamalla projektin juurikansiota (ylemmässä kuvassa nimellä saaennusteen-visualisointi-Django-Chart.js jossa sijaitsee manage.py) ja valitsemalla Open in Integrated Terminal
   
7. Kun olet juuressa luo venv terminaalissa komennolla: `python -m venv venv` voit sulkea terminaalin ja avaa se uudelleen yllä olevan ohjeen mukaan, jonka jälkeen aktivoi venv komennolla: `venv\Scripts\activate` tai Mac/Linux: `source venv/bin/activate` kun venv on päällä, terminaalissa yleensä näkyy suluissa (venv)
   
8.  Asenna tarvittavat paketit terminaalissa komennolla: `pip install -r requirements.txt`

9.  Seuraavaksi aja terminaalissa: `python manage.py migrate` ja jos haluat valmiiksi asetetut kaupungit (Turku, Tampere, Helsinki) näkyvän sivulla niin aja myös: `python manage.py loaddata cities.json` tämä ajaa json tiedoston, joka lisää kaupungit sqliteen weather_city osioon: <img width="901" height="379" alt="image" src="https://github.com/user-attachments/assets/3fdc9ee1-4a9f-49a2-84fa-c74e4fb51201" />

10. Projektin pitäisi näillä lähteä käyntiin komennolla `python manage.py runserver` ja näkyy sivulla: http://127.0.0.1:8000/
   
# Päivitys ja korjaus ideoita:
1. Siirtyminen PostgreSQL-tietokantaan (Data ei katoa ja paljon käytännöllisempi jos halutaan laajentaa sovellusta).
2. Koko suomen kaupunkien lisääminen sovellukseen, esimerkiksi käyttäen CSV-tiedostoja hyväksi.
3. Näytä tuntikohtainen sateen mahdollisuus ja tuulen nopeus (nyt näyttää vasta tuntikohtaisen lämpötilan päiväkorttia napauttamalla).
4. LÄMPÖTILA NYT, näyttää virheellisesti päivän korkeimman lämpötilan, eikä tämänhetkistä lämpötilaa.
