import pandas as pd
import matplotlib.pyplot as plt

filnavn = r"C:Skole\oppg_5\timestrafikk_sykkelmotorveien_juni_2026.csv"

# Filen er semikolon-separert, og bruker komma som desimaltegn
df = pd.read_csv(filnavn, sep=";", decimal=",")

dato_input = input("Skriv inn dato (format ÅÅÅÅ-MM-DD, f.eks. 2026-06-03): ").strip()

# Filtrer ut kun rader for den valgte datoen
df_dag = df[df["Dato"] == dato_input]

if df_dag.empty:
    print("Fant ingen data for denne datoen. Sjekk at datoen er mellom 2026-06-01 og 2026-06-08.")
else:
    # Plukk ut de to summerte retningene, sortert på klokkeslett
    stavanger = df_dag[df_dag["Felt"] == "Totalt i retning Stavanger"].sort_values("Fra tidspunkt")
    sandnes = df_dag[df_dag["Felt"] == "Totalt i retning Sandnes"].sort_values("Fra tidspunkt")

    plt.figure(figsize=(10, 5))
    plt.plot(stavanger["Fra tidspunkt"], stavanger["Trafikkmengde"], marker="o", label="Mot Stavanger")
    plt.plot(sandnes["Fra tidspunkt"], sandnes["Trafikkmengde"], marker="o", label="Mot Sandnes")

    plt.xlabel("Time på døgnet")
    plt.ylabel("Antall sykkelpasseringer")
    plt.title(f"Sykkelpasseringer {dato_input} – Sykkelstamvegen")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()