import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
# --------------------------------------------------
# 1. Les inn CSV-filen
# --------------------------------------------------

filnavn = r"C:oppg_5\timestrafikk_sykkelmotorveien_juni_2026.csv"

try:
    # Filen er semikolon-separert og bruker komma som desimaltegn
    df = pd.read_csv(filnavn, sep=";", decimal=",")
    
except FileNotFoundError:
    print("Finner ikke CSV-filen.")
    print("Sjekk at filstien og filnavnet er riktig.")
    exit()

except Exception as e:
    print("Det oppstod en feil da CSV-filen skulle leses.")
    print("Feilmelding:", e)
    exit()


# --------------------------------------------------
# 2. Kontroller at nødvendige kolonner finnes
# --------------------------------------------------

nødvendige_kolonner = [
    "Dato",
    "Felt",
    "Fra tidspunkt",
    "Trafikkmengde"
]

manglende_kolonner = [
    kolonne for kolonne in nødvendige_kolonner
    if kolonne not in df.columns
]

if manglende_kolonner:
    print("CSV-filen mangler følgende kolonner:")
    print(manglende_kolonner)
    exit()


# --------------------------------------------------
# 3. Gjør datoen klar
# --------------------------------------------------

# Gjør Dato-kolonnen om til tekst
df["Dato"] = df["Dato"].astype(str).str.strip()


# --------------------------------------------------
# 4. Be brukeren skrive inn dato
# --------------------------------------------------

while True:

    dato_input = input(
        "Skriv inn dato (format ÅÅÅÅ-MM-DD, f.eks. 2026-06-03): "
    ).strip()

    try:
        # Kontrollerer både format og om datoen faktisk finnes
        dato = datetime.strptime(dato_input, "%Y-%m-%d")

        # Kontroller at datoen ligger i juni 2026-dataene
        if dato < datetime(2026, 6, 1) or dato > datetime(2026, 6, 8):
            print("Datoen må være mellom 2026-06-01 og 2026-06-08.")
            continue

        break

    except ValueError:
        print("Feil format!")
        print("Skriv datoen slik: 2026-06-03")


# --------------------------------------------------
# 5. Filtrer data for valgt dato
# --------------------------------------------------

df_dag = df[df["Dato"] == dato_input]


if df_dag.empty:

    print("Fant ingen data for denne datoen.")
    print("Sjekk at datoen finnes i CSV-filen.")

else:

    # --------------------------------------------------
    # 6. Finn trafikk i hver retning
    # --------------------------------------------------

    stavanger = df_dag[
        df_dag["Felt"] == "Totalt i retning Stavanger"
    ].copy()

    sandnes = df_dag[
        df_dag["Felt"] == "Totalt i retning Sandnes"
    ].copy()


    # --------------------------------------------------
    # 7. Kontroller om det finnes data
    # --------------------------------------------------

    if stavanger.empty:
        print("Advarsel: Ingen data mot Stavanger denne dagen.")

    if sandnes.empty:
        print("Advarsel: Ingen data mot Sandnes denne dagen.")

    if stavanger.empty and sandnes.empty:
        print("Det finnes ingen trafikkdata å vise.")
        exit()


    # --------------------------------------------------
    # 8. Gjør trafikkmengde numerisk
    # --------------------------------------------------

    stavanger["Trafikkmengde"] = pd.to_numeric(
        stavanger["Trafikkmengde"],
        errors="coerce"
    )

    sandnes["Trafikkmengde"] = pd.to_numeric(
        sandnes["Trafikkmengde"],
        errors="coerce"
    )


    # --------------------------------------------------
    # 9. Fjern rader hvor trafikkmengden mangler
    # --------------------------------------------------

    stavanger = stavanger.dropna(
        subset=["Trafikkmengde"]
    )

    sandnes = sandnes.dropna(
        subset=["Trafikkmengde"]
    )


    # --------------------------------------------------
    # 10. Sorter etter tidspunkt
    # --------------------------------------------------

    stavanger = stavanger.sort_values("Fra tidspunkt")

    sandnes = sandnes.sort_values("Fra tidspunkt")


    # --------------------------------------------------
    # 11. Lag graf
    # --------------------------------------------------

    plt.figure(figsize=(10, 5))


    # Tegn Stavanger hvis det finnes data
    if not stavanger.empty:

        plt.plot(
            stavanger["Fra tidspunkt"],
            stavanger["Trafikkmengde"],
            marker="o",
            label="Mot Stavanger"
        )


    # Tegn Sandnes hvis det finnes data
    if not sandnes.empty:

        plt.plot(
            sandnes["Fra tidspunkt"],
            sandnes["Trafikkmengde"],
            marker="o",
            label="Mot Sandnes"
        )


    # --------------------------------------------------
    # 12. Gjør grafen ferdig
    # --------------------------------------------------

    plt.xlabel("Time på døgnet")
    plt.ylabel("Antall sykkelpasseringer")

    plt.title(
        f"Sykkelpasseringer {dato_input} – Sykkelstamvegen"
    )

    plt.xticks(rotation=45)

    plt.legend()

    plt.grid(True, alpha=0.3)

    plt.tight_layout()

    plt.show()
