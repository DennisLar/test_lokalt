import csv
import matplotlib.pyplot as plt

def hent_sykkeldata():
    filnavn = r"C:oppg_5\timestrafikk_sykkelmotorveien_juni_2026.csv"
    
    print("Tilgjengelige datoer: 01.06.2026 til 08.06.2026")
    bruker_dato = input("Skriv inn dato (f.eks. 03.06.2026 eller 2026-06-03): ").strip()
    
    # Trygg handtering av datoformat (f.eks. "03.06.2026" -> "2026-06-03")
    søke_dato = bruker_dato
    if "." in bruker_dato:
        deler = [d for d in bruker_dato.split(".") if d]  # Fjerner tomme elementer
        if len(deler) == 3:
            d, m, y = deler
            søke_dato = f"{y}-{m.zfill(2)}-{d.zfill(2)}"

    stavanger_per_time = {t: 0 for t in range(24)}
    sandnes_per_time = {t: 0 for t in range(24)}
    
    funnet = False

    try:
        with open(filnavn, mode="r", encoding="utf-8-sig") as fila:
            eksempel = fila.read(2048)
            skilletegn = ";" if ";" in eksempel else ","
            fila.seek(0)
            
            leser = csv.DictReader(fila, delimiter=skilletegn)
            
            for rad in leser:
                dato_i_fil = rad.get("Dato", "").strip()
                
                # Sammenlign mot både omformatert dato og opprinnelig brukerinput
                if dato_i_fil == søke_dato or dato_i_fil == bruker_dato:
                    funnet = True
                    
                    # Hent time fra 'Fra tidspunkt' (f.eks. "08:00" -> 8)
                    fra_tid = rad.get("Fra tidspunkt", "")
                    if ":" in fra_tid:
                        time_num = int(fra_tid.split(":")[0])
                    else:
                        continue
                    
                    # Hent antall syklister
                    try:
                        mengde = int(float(rad.get("Trafikkmengde", 0)))
                    except ValueError:
                        mengde = 0
                    
                    # Identifiser retning basert paa 'Felt' eller 'Til'
                    felt_info = (rad.get("Felt", "") + " " + rad.get("Til", "")).lower()
                    
                    if "stavanger" in felt_info:
                        stavanger_per_time[time_num] += mengde
                    elif "sandnes" in felt_info:
                        sandnes_per_time[time_num] += mengde
                    else:
                        # Fallback basert på felt-nummerering
                        if "1" in rad.get("Felt", ""):
                            stavanger_per_time[time_num] += mengde
                        else:
                            sandnes_per_time[time_num] += mengde

    except FileNotFoundError:
        print(f"Feil: Fant ikke filen '{filnavn}'. Sjekk filbanen.")
        return

    if not funnet:
        print(f"\nFant ingen data for datoen '{bruker_dato}'.")
        print("Husk at dataene kun gjelder for juni 2026 (f.eks. 03.06.2026).")
        return

    timer = list(range(24))
    mot_stavanger = [stavanger_per_time[t] for t in timer]
    mot_sandnes = [sandnes_per_time[t] for t in timer]

    # Plott kurvene
    plt.figure(figsize=(10, 5))
    plt.plot(timer, mot_stavanger, marker="o", color="#005A9C", label="Mot Stavanger", linewidth=2)
    plt.plot(timer, mot_sandnes, marker="s", color="#E30613", label="Mot Sandnes", linewidth=2)
    
    plt.title(f"Sykkelpasseringer per time – {bruker_dato}", fontsize=13, fontweight="bold")
    plt.xlabel("Time på døgnet (00–23)", fontsize=10)
    plt.ylabel("Antall sykkelpasseringer", fontsize=10)
    plt.xticks(range(0, 24))
    plt.grid(True, linestyle=":", alpha=0.7)
    plt.legend(title="Kjøreretning")
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    hent_sykkeldata()