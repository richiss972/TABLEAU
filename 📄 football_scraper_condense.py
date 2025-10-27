import json
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz

# URL du site
url1 = "https://www.matchendirect.fr/live-foot/"
url = "https://www.matchendirect.fr/resultat-foot-27-10-2025/"
base_url = "https://www.matchendirect.fr"

# DICTIONNAIRE DES LIGUES
ligues_interessantes = {
    "France": {
        "France - Ligue 1": "https://www.matchendirect.fr/classement-foot/france/classement-ligue-1.html",
        "France - Ligue 2": "https://www.matchendirect.fr/classement-foot/france/classement-ligue-2.html"
    },
    "England": {
        "England - Premier League": "https://www.matchendirect.fr/classement-foot/angleterre/classement-barclays-premiership-premier-league.html",
        "England - Championship": "https://www.matchendirect.fr/classement-foot/angleterre/classement-championship.html",
        "England - League One": "https://www.matchendirect.fr/classement-foot/angleterre/classement-league-1.html",
        "England - League Two": "https://www.matchendirect.fr/classement-foot/angleterre/classement-league-2.html"
    },
    "Spain": {
        "Spain - LaLiga": "https://www.matchendirect.fr/classement-foot/espagne/classement-primera-division.html",
        "Spain - LaLiga2": "https://www.matchendirect.fr/classement-foot/espagne/classement-segunda-division-liga-adelante.html"
    },
    "Italy": {
        "Italy - Serie A": "https://www.matchendirect.fr/classement-foot/italie/classement-serie-a.html",
        "Italy - Serie B": "https://www.matchendirect.fr/classement-foot/italie/classement-serie-b.html"
    },
    "Germany": {
        "Germany - Bundesliga": "https://www.matchendirect.fr/classement-foot/allemagne/classement-bundesliga-1.html",
        "Germany - 2. Bundesliga": "https://www.matchendirect.fr/classement-foot/allemagne/classement-bundesliga-2.html"
    },
    "Portugal": {
        "Portugal - Liga Portugal": "https://www.matchendirect.fr/classement-foot/portugal/classement-bwin-liga.html",
        "Portugal - Primeira Liga": "https://www.matchendirect.fr/classement-foot/portugal/classement-bwin-liga.html",
        #"Portugal - Liga Portugal 2": "https://www.matchendirect.fr/classement-foot/portugal/classement-liga-vitalis.html"
    },
    "Netherlands": {
        "Netherlands - Eredivisie": "https://www.matchendirect.fr/classement-foot/pays-bas/classement-eredivisie.html"
    },
    "Scotland": {
        "Scotland - Premiership": "https://www.matchendirect.fr/classement-foot/ecosse/classement-premier-league.html"
    },
    "Turkey": {
        "Turkey - Super Lig": "https://www.matchendirect.fr/classement-foot/turquie/classement-super-lig.html"
    },
    "Belgium": {
        "Belgium - Pro League": "https://www.matchendirect.fr/classement-foot/belgique/classement-jupiler-league.html"
    },
    "Brazil": {
        "Brazil - Série A": "https://www.matchendirect.fr/classement-foot/bresil/classement-serie-a.html",
        #"Brazil - Série B": "https://www.matchendirect.fr/classement-foot/bresil/classement-serie-b.html"
    },
    "Argentina": {
        "Argentina - Liga Profesional - Apertura": "https://www.matchendirect.fr/classement-foot/argentine/classement-torneo-clausura.html"
    },
    "Austria": {
        "Austria - Bundesliga": "https://www.matchendirect.fr/classement-foot/autriche/classement-tipp3-bundesliga.html"
    },
    "China": {
        "China - Super League": "https://www.matchendirect.fr/classement-foot/chine/classement-jia-a.html"
    },
    "Denmark": {
        "Denmark - Superligaen": "https://www.matchendirect.fr/classement-foot/danemark/classement-sas-ligaen.html"
    },
    "Estonia": {
        "Estonia - Meistriliiga": "https://www.matchendirect.fr/classement-foot/estonie/classement-meistriliiga.html"
    },
    "Finland": {
        "Finland - Veikkausliiga": "https://www.matchendirect.fr/classement-foot/finlande/classement-veikkausliiga.html"
    },
    "Greece": {
        "Greece - Super League": "https://www.matchendirect.fr/classement-foot/grece/classement-super-league.html"
    },
    "Hungary": {
        "Hungary - NB I": "https://www.matchendirect.fr/classement-foot/hongrie/classement-borsodi-liga.html"
    },
    "Latvia": {
        "Latvia - Virsliga": "https://www.matchendirect.fr/classement-foot/lettonie/classement-virsliga.html"
    },
    "Lithuania": {
        "Lithuania - A Lyga": "https://www.matchendirect.fr/classement-foot/lituanie/classement-a-lyga.html"
    },
    "Poland": {
        "Poland - Ekstraklasa": "https://www.matchendirect.fr/classement-foot/pologne/classement-orange-ekstraklasa.html"
    },
    "Serbia": {
        "Serbia - Super Liga": "https://www.matchendirect.fr/classement-foot/serbie/classement-super-liga.html"
    },
    "Slovakia": {
        "Slovakia - 1. Liga": "https://www.matchendirect.fr/classement-foot/slovaquie/classement-super-liga.html"
    },
    "Sweden": {
        "Sweden - Allsvenskan": "https://www.matchendirect.fr/classement-foot/suede/classement-allsvenskan.html"
    },
    "Switzerland": {
        "Switzerland - Super League": "https://www.matchendirect.fr/classement-foot/suisse/classement-super-league.html"
    },
    "Bulgaria": {
        "Bulgaria - Parva Liga": "https://www.matchendirect.fr/classement-foot/bulgarie/classement-a-pfg.html"
    },
    "Chile": {
        "Chile - Liga de Primera": "https://www.matchendirect.fr/classement-foot/chili/classement-clausura.html",
        #"Chile - Superliga": "https://www.matchendirect.fr/classement-foot/chili/classement-primera-b.html"
    },
    "Colombia": {
        "Colombia - Primera A - Apertura": "https://www.matchendirect.fr/classement-foot/colombie/classement-copa-mustang-apertura.html",
        #"Colombia - Première B Clôture": "https://www.matchendirect.fr/classement-foot/colombie/classement-primera-b-clausura.html"
    },
    "Croatia": {
        "Croatia - 1. HNL": "https://www.matchendirect.fr/classement-foot/croatie/classement-hnl-ozujsko.html"
    },
    "Czech Republic": {
        "Czech Republic - 1. Liga": "https://www.matchendirect.fr/classement-foot/republique-tcheque/classement-gambrinus-liga.html"
    },
    "Ecuador": {
        "Ecuador - Liga Pro": "https://www.matchendirect.fr/classement-foot/equateur/classement-serie-a-clausura.html",
        #"Ecuador - Première B Tour de Relégation": "https://www.matchendirect.fr/classement-foot/equateur/classement-serie-b.html"
    },
    "Iceland": {
        "Iceland - Besta deild": "https://www.matchendirect.fr/classement-foot/islande/classement-1-deild.html"
    },
    "Ireland": {
        "Ireland - Premier Division": "https://www.matchendirect.fr/classement-foot/irlande/classement-premier-division.html"
    },
    "Japan": {
        "Japan - J1 League": "https://www.matchendirect.fr/classement-foot/japon/classement-j-league.html"
    },
    "Luxembourg": {
        "Luxembourg - National Division": "https://www.matchendirect.fr/classement-foot/luxembourg/classement-fortis-league.html"
    },
    "Mexico": {
        "Mexico - Liga MX - Apertura": "https://www.matchendirect.fr/classement-foot/mexique/classement-primera-division.html"
    },
    "Northern Ireland": {
        "Northern Ireland - NIFL": "https://www.matchendirect.fr/classement-foot/irlande-du-nord/classement-premiership.html"
    },
    "Norway": {
        "Norway - Eliteserien": "https://www.matchendirect.fr/classement-foot/norvege/classement-tippeligaen.html"
    },
    "Paraguay": {
        "Paraguay - Primera Div. - Apertura": "https://www.matchendirect.fr/classement-foot/paraguay/classement-division-profesional-apertura.html",
        #"Paraguay - Professionnel de la Division": "https://www.matchendirect.fr/classement-foot/paraguay/classement-division-profesional.html",
        #"Paraguay - Professionnel de la Division Clausura": "https://www.matchendirect.fr/classement-foot/paraguay/classement-division-profesional-clausura.html"
    },
    "Peru": {
        "Peru - Liga 1": "https://www.matchendirect.fr/classement-foot/perou/classement-primera-division.html",
        #"Peru - Liga 2": "https://www.matchendirect.fr/classement-foot/perou/classement-segunda-division.html",
        #"Peru - Liga 3 Demi-Finale": "https://www.matchendirect.fr/classement-foot/perou/classement-copa-peru.html"
    },
    "South Korea": {
        "South Korea - K League 1": "https://www.matchendirect.fr/classement-foot/coree-du-sud/classement-k-league.html"
    }
}


def get_timestamp_paris():
    """Retourne le timestamp actuel au format Paris"""
    paris_tz = pytz.timezone('Europe/Paris')
    return datetime.now(paris_tz).strftime('%Y-%m-%d %H:%M:%S')


def normaliser_texte(texte):
    """Normalise le texte pour la comparaison (supprime sauts de ligne et espaces multiples)"""
    # Remplacer les sauts de ligne et tabulations par des espaces
    texte = texte.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    # Supprimer les espaces multiples et mettre en minuscules
    return ' '.join(texte.split()).lower()


def est_ligue_interessante(pays, ligue):
    """Vérifie si une compétition correspond aux ligues définies"""
    cle_complete = f"{pays} - {ligue}"
    cle_normalisee = normaliser_texte(cle_complete)
    
    for pays_dict, ligues_dict in ligues_interessantes.items():
        for ligue_complete in ligues_dict.keys():
            if normaliser_texte(ligue_complete) == cle_normalisee:
                return True
            
            ligue_dict_norm = normaliser_texte(ligue_complete.split(' - ', 1)[1] if ' - ' in ligue_complete else ligue_complete)
            ligue_norm = normaliser_texte(ligue)
            
            if ligue_dict_norm in ligue_norm or ligue_norm in ligue_dict_norm:
                pays_dict_norm = normaliser_texte(pays_dict)
                pays_norm = normaliser_texte(pays)
                
                mappings_pays = {
                    'angleterre': 'england', 'allemagne': 'germany', 'espagne': 'spain',
                    'italie': 'italy', 'pays-bas': 'netherlands', 'ecosse': 'scotland',
                    'turquie': 'turkey', 'belgique': 'belgium', 'bresil': 'brazil',
                    'brésil': 'brazil', 'argentine': 'argentina', 'autriche': 'austria', 
                    'chine': 'china', 'danemark': 'denmark', 'estonie': 'estonia', 
                    'finlande': 'finland', 'grece': 'greece', 'hongrie': 'hungary', 
                    'lettonie': 'latvia', 'lituanie': 'lithuania', 'pologne': 'poland', 
                    'serbie': 'serbia', 'slovaquie': 'slovakia', 'suede': 'sweden', 
                    'suisse': 'switzerland', 'bulgarie': 'bulgaria', 'chili': 'chile', 
                    'colombie': 'colombia', 'croatie': 'croatia', 'equateur': 'ecuador', 
                    'équateur': 'ecuador', 'islande': 'iceland', 'irlande': 'ireland', 
                    'japon': 'japan', 'mexique': 'mexico', 'norvege': 'norway', 
                    'paraguai': 'paraguay', 'paraguay': 'paraguay', 'perou': 'peru', 
                    'pérou': 'peru', 'coree du sud': 'south korea',
                    'republique tcheque': 'czech republic', 'irlande du nord': 'northern ireland'
                }
                
                if pays_norm == pays_dict_norm:
                    return True
                if pays_norm in mappings_pays and mappings_pays[pays_norm] == pays_dict_norm:
                    return True
                if pays_dict_norm in mappings_pays and mappings_pays[pays_dict_norm] == pays_norm:
                    return True
    
    return False


def est_match_en_cours(heure):
    """Détermine si un match est EN COURS (pas terminé)"""
    if not heure:
        return False
    
    heure = heure.strip()
    
    if "TER" in heure.upper():
        return False
    
    if "'" in heure:
        return True
    
    if re.match(r'^\d{1,2}:\d{2}$', heure):
        return False
    
    return False


def est_match_termine(heure):
    """Détermine si un match est TERMINÉ"""
    if not heure:
        return False
    
    heure = heure.strip()
    
    if "TER" in heure.upper():
        return True
    
    return False


def extraire_match_condense(match_row, pays, ligue):
    """Extrait un match au format condensé"""
    match_info = {}
    
    match_info['id'] = match_row.get('data-matchid')
    match_info['pays'] = pays
    match_info['ligue'] = ligue
    
    time_elem = match_row.find('span', class_='lm2_timeXxX')
    if time_elem:
        match_info['heure'] = time_elem.text.strip()
    
    eq1 = match_row.find('span', class_='lm3_eq1')
    eq2 = match_row.find('span', class_='lm3_eq2')
    
    if eq1 and eq2:
        match_info['dom'] = eq1.text.strip()
        match_info['ext'] = eq2.text.strip()
    
    score_elem = match_row.find('span', class_=re.compile(r'lm3_score'))
    if score_elem:
        score_text = score_elem.text.strip()
        if score_text != 'v':
            scores = re.findall(r'\d+', score_text)
            if len(scores) == 2:
                match_info['score'] = f"{scores[0]}-{scores[1]}"
    
    links = match_row.find_all('a', href=re.compile(r'/live-score/.*\.html'))
    if links:
        lien_relatif = links[0].get('href')
        match_info['lien'] = base_url + lien_relatif
    
    red_cards_team1 = match_row.find('i', class_='redcart redcart-team1')
    red_cards_team2 = match_row.find('i', class_='redcart redcart-team2')
    
    cartons = {}
    if red_cards_team1 and red_cards_team1.find_all('span'):
        cartons['dom'] = len(red_cards_team1.find_all('span'))
    if red_cards_team2 and red_cards_team2.find_all('span'):
        cartons['ext'] = len(red_cards_team2.find_all('span'))
    
    if cartons:
        match_info['cartons'] = cartons
    
    return match_info


def main():
    """Fonction principale"""
    timestamp = get_timestamp_paris()
    
    print("🔄 Extraction des matchs en cours/terminés...")
    
    try:
        response = requests.get(url, timeout=10)
        response.encoding = 'utf-8'
        html_content = response.text
    except Exception as e:
        print(f"✗ Erreur : {e}")
        return
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    matchs_en_cours = []
    matchs_termines = []
    
    panels = soup.find_all('div', class_='panel-heading livescore_head')
    
    for panel in panels:
        competition_link = panel.find('a', title=re.compile(r'.*'))
        if not competition_link:
            continue
        
        competition_titre = competition_link.text.strip()
        
        # Utiliser une regex plus simple pour extraire le pays
        match_pays = re.search(r'(.+?):', competition_titre)
        pays = match_pays.group(1).strip() if match_pays else "Inconnu"
        ligue = competition_titre.split(':', 1)[1].strip() if ':' in competition_titre else competition_titre
        
        if not est_ligue_interessante(pays, ligue):
            continue
        
        panel_parent = panel.find_parent('div', class_='panel')
        if panel_parent:
            table = panel_parent.find('table')
            if table:
                matches = table.find_all('tr', attrs={'data-matchid': True})
                
                for match in matches:
                    time_elem = match.find('span', class_='lm2_timeXxX')
                    if time_elem:
                        heure = time_elem.text.strip()
                        
                        if est_match_en_cours(heure):
                            match_condense = extraire_match_condense(match, pays, ligue)
                            matchs_en_cours.append(match_condense)
                        elif est_match_termine(heure):
                            match_condense = extraire_match_condense(match, pays, ligue)
                            matchs_termines.append(match_condense)
    
    json_condense = {
        "metadata": {
            "description": "Matchs en cours et terminés",
            "derniere_mise_a_jour": timestamp,
            "total_matchs": len(matchs_en_cours) + len(matchs_termines),
            "matchs_en_cours": len(matchs_en_cours),
            "matchs_termines": len(matchs_termines)
        },
        "en_cours": matchs_en_cours,
        "termines": matchs_termines
    }
    
    with open('matchs_condense.json', 'w', encoding='utf-8') as f:
        json.dump(json_condense, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ {len(matchs_en_cours)} match(s) en cours")
    print(f"✓ {len(matchs_termines)} match(s) terminés")
    print(f"✓ Fichier 'matchs_condense.json' créé\n")
    
    if matchs_en_cours:
        print("🔴 MATCHS EN COURS :")
        for match in matchs_en_cours:
            print(f"  [{match['pays']}] {match['ligue']}")
            print(f"    {match['heure']:8s} {match['dom']} {match.get('score', 'v')} {match['ext']}")
    else:
        print("ℹ️  Aucun match en cours actuellement")


if __name__ == "__main__":
    main()
