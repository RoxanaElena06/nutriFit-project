Specificații Simplificate: NutriFit Data Project

1. Ce Face Proiectul? (Ideea Principală)
Construim o platformă automată în cloud care strânge date despre pași, calorii și mese, le curăță, le organizează în tabele clare și generează rapoarte ușor de citit.

 [ 1. DATE BRUTE ]             [ 2. PROCESARE ÎN DATABRICKS ]             [ 3. REZULTAT ]
   Simulăm date din              Preluăm datele ➔ Le curățăm                 Rapoarte și
   fitness & nutriție            ➔ Le grupăm pe niveluri                    Dashboard-uri
2. Cum Sunt Organizate Datele? (Arhitectura Medallion)
În Databricks, procesarea se face în 3 pași simpli (numiți straturi):

┌──────────────────────────────────────────────────────────────────────────────────┐
│                             ARHITECTURA MEDALLION                                │
├──────────────────────────┬──────────────────────────┬────────────────────────────┤
│ 🥉 Stratul BRONZE        │ 🥈 Stratul SILVER        │ 🥇 Stratul GOLD            │
│ (Date Brute)             │ (Date Curate)            │ (Date Finale pentru Raport)│
├──────────────────────────┼──────────────────────────┼────────────────────────────┤
│ • Salvăm datele exacte   │ • Scoatem erorile și     │ • Calculăm mediile și      │
│   așa cum vin din        │   duplicatele.           │   totalurile zilnice.      │
│   aplicație/ceas.        │ • Verificăm dacă caloriile│ • Organizăm datele în      │
│ • Nu ștergem nimic.      │   sunt numere valide.    │   tabele de Raportare.     │
└──────────────────────────┴──────────────────────────┴────────────────────────────┘
3. Ce Componente Construiești Pas cu Pas?
a. Generatorul de Date (Sursa):
	- Un program simplu în Python care creează utilizatori ficționali, mesele lor și pașii făcuți în fiecare zi.
	- Trimite aceste date într-un spațiu de stocare în Cloud (AWS S3).

b. Ingestia Automată (Auto Loader):
	- Un proces din Databricks care "stă la pândă" și detectează automat când apar fișiere noi în Cloud.
	- Salvează fișierele noi direct în Stratul Bronze.

c. Curățarea & Controlul Calității (Delta Live Tables):
	- Reguli automate care elimină înregistrările greșite (de exemplu: un număr negativ de calorii sau utilizatori fără nume).
	- Salvează datele impecabile în Stratul Silver.

d. Modelarea pentru Analiză (Star Schema):
	- Crearea tabelelor finale în Stratul Gold:
		- Tabela Principală (Fapte): Rezumatul zilnic (total pași, total calorii arse vs. consumate).
		- Tabelele Suport (Dimensiuni): Lista utilizatorilor și lista alimentelor.

e. Securitatea & Organizarea (Unity Catalog):
	- Organizăm totul într-un dosar principal (nutrifit_catalog) și stabilim cine are voie să vadă datele (de exemplu: un Data Analyst vede doar Stratul Gold final).

f. Automatizarea (Databricks Workflows):
	- Setăm un "ceas" automat care pune tot pipeline-ul în mișcare o dată pe zi, fără să apeși tu pe niciun buton.

4. Structura Proiectului pe GitHub (Organizarea Fișierelor)
Când creezi proiectul pe GitHub, vei avea doar câteva dosare principale:

nutrifit-data-platform/
│
├── README.md                 # Prezentarea proiectului (ce face și cum funcționează)
│
├── generator_date/           # Programul Python care creează datele despre fitness/nutriție
│
├── databricks_notebooks/     # Pasul 1 (Bronze), Pasul 2 (Silver) și Pasul 3 (Gold)
│
└── securitate_si_joburi/     # Setările de automatizare și securitate în Databricks