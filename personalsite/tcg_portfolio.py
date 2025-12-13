import requests
from datetime import datetime
import re
import time
import os
import json

# Name of the file where I store raw data
DATA_FILE = "portfolio_data.json"
HTML_FILE = "generated_cards.html"

def get_card_data(card_input):
    base_url = "https://api.pokemontcg.io/v2/cards"
    headers = {'User-Agent': 'PokemonPortfolioTracker/3.0'}
    
    # --- 1. PARSING LOGIC ---
    parts = card_input.split()
    number = parts[-1]
    
    if len(parts) > 2 and parts[-2].isupper() and len(parts[-2]) <= 4 and not any(char.isdigit() for char in parts[-2]):
        name_parts = parts[:-2] 
    else:
        name_parts = parts[:-1] 
        
    name = " ".join(name_parts)
    
    # --- 2. SEARCH STRATEGIES ---
    strategies = []
    
    # Strict
    strict_query = f'name:"{name}" number:"{number}"'
    if "/" in number and "GG" in number:
        clean_num = number.split("/")[0]
        strict_query = f'name:"{name}" number:"{clean_num}"'
    strategies.append({'q': strict_query, 'type': 'strict'})
    
    # Loose
    strategies.append({'q': f'name:"{name}"', 'type': 'loose'})

    # --- 3. EXECUTION LOOP ---
    for strategy in strategies:
        for attempt in range(3):
            try:
                resp = requests.get(base_url, params={'q': strategy['q']}, headers=headers)
                
                if resp.status_code in [429, 500, 502, 503, 504]:
                    wait = 5 + (attempt * 5)
                    print(f"   [API Busy {resp.status_code}, wait {wait}s]", end=" ", flush=True)
                    time.sleep(wait)
                    continue
                
                if resp.status_code == 404:
                    break 

                if resp.status_code == 200:
                    data = resp.json()['data']
                    if not data: break 
                    
                    if strategy['type'] == 'strict':
                        return data[0]
                    
                    if strategy['type'] == 'loose':
                        for card in data:
                            if card['number'] == number or card['number'].lstrip('0') == number.lstrip('0'):
                                return card
                        break 
                break

            except Exception as e:
                print(f"[Err: {e}]", end=" ")
                time.sleep(2)
                continue
    return None

def extract_price(card_data):
    if not card_data: return 0.0
    tcg = card_data.get('tcgplayer', {}).get('prices', {})
    priorities = ['holofoil', 'normal', 'reverseHolofoil', 'unlimitedHolofoil']
    for p in priorities:
        if p in tcg and tcg[p].get('market'):
            return tcg[p].get('market')
    return 0.0

def load_progress():
    """Loads existing progress to avoid starting over."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_progress(portfolio_list):
    """Saves raw data to JSON and formatted display to HTML."""
    # 1. Save JSON (The brain)
    with open(DATA_FILE, 'w') as f:
        json.dump(portfolio_list, f, indent=2)

    # 2. Save HTML (The face)
    date_str = datetime.now().strftime("%B %d, %Y")
    total_val = sum(c['market_price'] for c in portfolio_list)
    
    html_content = f"""
    <html>
    <head>
        <title>Pokemon Portfolio</title>
        <style>
            body {{ font-family: sans-serif; background: #f0f2f5; padding: 20px; }}
            .header {{ background: white; padding: 20px; border-radius: 12px; margin-bottom: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
            .card-grid {{ display: flex; flex-wrap: wrap; gap: 15px; justify-content: center; }}
            .card-item {{ 
                background: white; border-radius: 10px; padding: 15px; width: 220px; 
                text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1); 
                transition: transform 0.2s;
            }}
            .card-item:hover {{ transform: translateY(-5px); }}
            .card-item img {{ width: 100%; border-radius: 8px; margin-bottom: 10px; }}
            .price-tag {{ background: #d1fae5; color: #065f46; padding: 5px 10px; border-radius: 15px; font-weight: bold; display: inline-block; margin-top: 5px; }}
            h3 {{ margin: 5px 0; font-size: 1.1rem; }}
            .meta {{ color: #6b7280; font-size: 0.9rem; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>My Pokemon Collection</h1>
            <p>Total Value: <strong style="color: #059669; font-size: 1.5rem;">${total_val:.2f}</strong></p>
            <p>Cards Found: {len(portfolio_list)} | Date: {date_str}</p>
        </div>
        <div class="card-grid">
    """
    
    for card in portfolio_list:
        display_number = f"{card['number']}/{card['total_printed']}"
        html_content += f"""
        <div class="card-item">
            <img src="{card['image']}" alt="{card['name']}">
            <h3>{card['name']}</h3>
            <div class="meta">{card['set']} ({display_number})</div>
            <div class="price-tag">${card['market_price']:.2f}</div>
        </div>
        """
        
    html_content += "</div></body></html>"
    
    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(html_content)

def main():
    my_collection_queries = [
        "Bulbasaur MEG 133", "Ivysaur MEG 134", "Venusaur MEG 177", "Caterpie MEW 172", 
        "Crustle DRI 186", "Hydrapple DRI 188", "Iron Leaves TEF 203", "Maractus JTG 160", 
        "Ninjask MEG 137", "Nymble PFL 096", "Poltchageist TWM 171", "Servine BLK 088", 
        "Shaymin DRI 185", "Shuckle MEG 136", "Tarountula SVI 199", "Vulpix 197", 
        "Clamperl DRI 195", "Clawitzer MEG 141", "Dondozo SVI 207", "Gyarados SVI 225", 
        "Inteleon MEG 142", "Keldeo GG07/GG70", "Lumineon GG39/GG70", "Manaphy GG06/GG70", 
        "Palafin PAF 225", "Piplup PFL 098", "Poliwhirl MEW 176", "Psyduck MEW 175", 
        "Snover MEG 140", "Spheal SSP 199", "Vanillish WHT 112", "Vanillish PAR 190", 
        "Vaporeon TG02/TG30", "Wailord JTG 162", "Wiglett SVI 206", "Charcadet MEP 022",
        "Ceruledge SSP 197", "Charmander SVP 044", "Charmander MEW 168", "Charmeleon MEW 169", 
        "Darmanitan BLK 098", "Litleo MEG 139", "Oricorio GG04/GG70", "Rapidash DRI 189", 
        "Simisear GG37/GG70", "Turtonator SCR 146", "Victini SVP 208", "Vulpix MEG 138", 
        "Garvantula SCR 168", "Jolteon TG04/TG30", "Magneton SVP 159", "Pikachu TG05/TG30", 
        "Pikachu MEW 173", "Pikachu 005/025", "Pikachu SSP 057", "Pikachu SWSH143", 
        "Pikachu SWSH063", "Pikachu SWSH062", "Zeraora SCR 151", "Zeraora GG42/GG70", 
        "Zeraora GG43/GG70", "Flygon PFL 101", "Flygon SSP 222", "Hoopa PAR 226", 
        "Klawf SVI 217", "Larvitar OBF 203", "Lycanroc JTG 166", "Marshadow MEG 146", 
        "Meditite SCR 153", "Riolu MEP 010", "Alakazam MEP 009", "Dedenne TG07/TGG30", 
        "Deoxys GG46/GG70", "Gothitelle SVP 211", "Houndstone MEG 145", "Latias SSP 203", 
        "Meloetta MEP 026", "Mesprit SSP 204", "Mew GG10/GG70", "Mew SVP 053", 
        "Mewtwo SVP 052", "Sandygast PAL 214", "Shedinja MEG 144", "Wobbuffet SVP 203", 
        "Charizard OBF 228", "Charizard OBF 215", "Perrserker 184/196", "Haunter MEP 027", 
        "Kingambit SVI 220", "Skuntank 181/195", "Spiritomb MEG 148", "Weezing DRI 199", 
        "Trubbish WHT 140", "Vullaby WHT 144", "Yveltal PAR 205", "Dugtrio SSP 208", 
        "Kingambit SVP 130", "Scizor OBF 205", "Togedemaru PFL 104", "Zamazenta GG54/GG70", 
        "Zamazenta SWSH077", "Appletun SSP 211", "Applin TWM 185", "Latias GG20/GG70", 
        "Altaria TG11/TG30", "Bouffalant WHT 170", "Ditto GG20/GG70", "Drampa 184/162", 
        "Eevee SVP 173", "Furret JTG 168", "Wooloo JTG 170", "Kangaskhan 204", 
        "Lechonk OBF 209", "Loudred PAR 212", "Lopunny PFL 128", "Noibat JTG 169", 
        "Pidgey OBF 207", "Pidgeotto OBF 208", "Pidgeot OBF 225", "Pidove BLK 148", 
        "Slakoth SSP 212", "Snorlax SVP 051", "Spearow MEG 151", "Stufful MEG 154"
    ]
    
    # Load previous progress
    portfolio = load_progress()
    found_queries = {item['original_query'] for item in portfolio if 'original_query' in item}
    
    print(f"--- RESUMABLE TRACKER ---")
    print(f"Already Found: {len(portfolio)} cards")
    print("-" * 50)
    
    for i, query in enumerate(my_collection_queries):
        # SKIP if we already have it
        if query in found_queries:
            # I print a dot just to show it's working but skipping
            if i % 10 == 0: print(".", end="", flush=True) 
            continue
            
        print(f"\n[{i+1}/{len(my_collection_queries)}] {query:<25}", end=" ", flush=True)
        
        # Delay for API safety
        time.sleep(1.2)
        
        data = get_card_data(query)
        
        if data:
            price = extract_price(data)
            card_obj = {
                "original_query": query, # Save this to skip next time
                "name": data['name'],
                "set": data['set']['name'],
                "number": data['number'],
                "total_printed": data['set']['printedTotal'],
                "image": data['images']['small'],
                "market_price": price
            }
            portfolio.append(card_obj)
            
            # Save IMMEDIATELY
            save_progress(portfolio)
            
            if price > 0:
                print(f"-> Found! \033[92m${price:.2f}\033[0m", end="")
            else:
                print(f"-> Found! (No Price)", end="")
        else:
            print(f"-> \033[91mFailed (Skipping)\033[0m", end="")

    print("\n" + "-" * 50)
    print(f"DONE! Total Value: ${sum(c['market_price'] for c in portfolio):.2f}")
    print(f"Open '{HTML_FILE}' to see your portfolio.")

if __name__ == "__main__":
    main()