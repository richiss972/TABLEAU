// Configuration
const REFRESH_INTERVAL = 30000; // 30 secondes
const JSON_URL = 'matchs_condense.json';

let countdownInterval;
let currentFilter = 'all';

// Initialisation
document.addEventListener('DOMContentLoaded', () => {
    loadMatches();
    startCountdown();
    setupFilters();
});

// Charger les matchs
async function loadMatches() {
    try {
        const response = await fetch(`${JSON_URL}?t=${new Date().getTime()}`);
        const data = await response.json();
        
        updateStats(data.metadata);
        displayMatches(data.en_cours, data.termines);
        updateLastUpdate(data.metadata.derniere_mise_a_jour);
        
    } catch (error) {
        console.error('Erreur de chargement:', error);
        showError();
    }
}

// Mettre à jour les statistiques
function updateStats(metadata) {
    document.getElementById('total-matchs').textContent = metadata.total_matchs;
    document.getElementById('matchs-en-cours').textContent = metadata.matchs_en_cours;
    document.getElementById('matchs-termines').textContent = metadata.matchs_termines;
}

// Afficher les matchs
function displayMatches(enCours, termines) {
    displayMatchList(enCours, 'matchs-en-cours-container', true);
    displayMatchList(termines, 'matchs-termines-container', false);
    applyFilter(currentFilter);
}

// Afficher une liste de matchs
function displayMatchList(matches, containerId, isLive) {
    const container = document.getElementById(containerId);
    
    if (matches.length === 0) {
        container.innerHTML = '<div class="no-matches">Aucun match pour le moment</div>';
        return;
    }
    
    container.innerHTML = matches.map(match => createMatchCard(match, isLive)).join('');
}

// Créer une carte de match
function createMatchCard(match, isLive) {
    const cartonsDom = match.cartons?.dom ? `<span class="cartons">🟥 ${match.cartons.dom}</span>` : '';
    const cartonsExt = match.cartons?.ext ? `<span class="cartons">🟥 ${match.cartons.ext}</span>` : '';
    
    return `
        <div class="match-card ${isLive ? 'live' : ''}" onclick="window.open('${match.lien}', '_blank')">
            <div class="match-header">
                <div class="competition">
                    <span class="competition-badge">${match.pays}</span>
                    ${match.ligue}
                </div>
                <div class="match-time ${isLive ? 'live' : 'finished'}">
                    ${match.heure}
                </div>
            </div>
            <div class="match-content">
                <div class="team home">
                    ${match.dom}
                    ${cartonsDom}
                </div>
                <div class="score ${isLive ? 'live' : ''}">
                    ${match.score || 'vs'}
                </div>
                <div class="team away">
                    ${match.ext}
                    ${cartonsExt}
                </div>
            </div>
        </div>
    `;
}

// Mettre à jour l'heure
function updateLastUpdate(timestamp) {
    document.getElementById('last-update').textContent = `Dernière mise à jour : ${timestamp}`;
}

// Afficher une erreur
function showError() {
    document.getElementById('matchs-en-cours-container').innerHTML = 
        '<div class="no-matches">❌ Erreur de chargement des données</div>';
    document.getElementById('matchs-termines-container').innerHTML = 
        '<div class="no-matches">❌ Erreur de chargement des données</div>';
}

// Countdown pour le refresh
function startCountdown() {
    let seconds = REFRESH_INTERVAL / 1000;
    
    countdownInterval = setInterval(() => {
        seconds--;
        document.getElementById('countdown').textContent = seconds;
        
        if (seconds <= 0) {
            loadMatches();
            seconds = REFRESH_INTERVAL / 1000;
        }
    }, 1000);
}

// Configuration des filtres
function setupFilters() {
    const filterBtns = document.querySelectorAll('.filter-btn');
    
    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            currentFilter = btn.dataset.filter;
            applyFilter(currentFilter);
        });
    });
}

// Appliquer le filtre
function applyFilter(filter) {
    const enCoursSection = document.getElementById('matchs-en-cours-section');
    const terminesSection = document.getElementById('matchs-termines-section');
    
    switch(filter) {
        case 'en-cours':
            enCoursSection.style.display = 'block';
            terminesSection.style.display = 'none';
            break;
        case 'termines':
            enCoursSection.style.display = 'none';
            terminesSection.style.display = 'block';
            break;
        default:
            enCoursSection.style.display = 'block';
            terminesSection.style.display = 'block';
    }
}
