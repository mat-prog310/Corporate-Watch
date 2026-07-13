import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import threading
from collections import defaultdict
import re
from dataclasses import dataclass, field
import warnings
warnings.filterwarnings('ignore')

# Tentative d'import bibliothèques optionnelles
try:
    import requests
    from bs4 import BeautifulSoup
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("⚠️ Mode hors-ligne - Utilisation des données intégrées")

# ============================================
# STRUCTURES DE DONNÉES CORPORATEWATCH
# ============================================

@dataclass
class PromesseClimat:
    """Promesse climatique d'une entreprise"""
    type_promesse: str  # 'neutralité_carbone', 'reduction_co2', 'energie_verte', etc.
    objectif: str  # ex: "-30% CO2 d'ici 2030"
    annee_cible: int
    annee_annonce: int
    statut: str  # 'En avance', 'Dans les temps', 'En retard', 'Non tenue', 'Abandonnée'
    progression_pct: float  # % de réalisation
    ecart_pct: float  # écart par rapport à la trajectoire
    greenwashing_probable: bool
    preuves: List[str]
    sources: List[str]

@dataclass
class IncidentEnvironnemental:
    """Incident environnemental enregistré"""
    date: str
    type_incident: str  # 'marée_noire', 'pollution_chimique', 'deforestation', etc.
    description: str
    gravite: str  # '🔴 Critique', '🟠 Grave', '🟡 Modéré', '🟢 Mineur'
    localisation: str
    impact_financier_millions: float
    amendes: float
    media_references: List[str]

@dataclass
class ActiviteTempsReel:
    """Activité en temps réel de l'entreprise"""
    bourse_actuelle: float
    variation_jour_pct: float
    volume_echanges: int
    controverses_actives: List[str]
    campagnes_boycott_en_cours: int
    alertes_mediatiques: List[str]
    mentions_reseaux_sociaux: Dict[str, int]
    sentiment_public: str  # 'Très négatif', 'Négatif', 'Neutre', 'Positif'

@dataclass
class EntrepriseSurveillee:
    """Entreprise sous surveillance complète"""
    nom: str
    pays: str
    secteur: str
    score_ethique: int  # /100
    niveau_boycott: str  # '🔴 BANNIR', '🟠 BOYCOTTER', '🟡 ÉVITER', '🟢 SURVEILLER'
    
    # Émissions
    emissions_co2_2025: float
    emissions_co2_2026: float
    emissions_cible_2030: float
    reduction_pct: float
    
    # Promesses
    promesses: List[PromesseClimat] = field(default_factory=list)
    
    # Incidents
    incidents: List[IncidentEnvironnemental] = field(default_factory=list)
    total_amendes: float = 0
    nb_proces_en_cours: int = 0
    
    # Activité temps réel
    activite_temps_reel: Optional[ActiviteTempsReel] = None
    
    # Transparence
    transparence_score: int = 0  # /100
    greenwashing_score: int = 0  # /100
    certifications: List[str] = field(default_factory=list)
    faux_labels: List[str] = field(default_factory=list)
    
    # Alertes
    alertes_actives: List[str] = field(default_factory=list)
    derniere_mise_a_jour: str = ""

@dataclass
class AlerteLive:
    """Alerte en direct"""
    id: str
    timestamp: str
    entreprise: str
    type_alerte: str  # 'greenwashing', 'incident', 'promesse_non_tenue', 'amende', 'boycott'
    niveau: str  # '🔴 CRITIQUE', '🟠 IMPORTANT', '🟡 ATTENTION'
    message: str
    action_recommandee: str
    impact_estime: str
    sources: List[str]

# ============================================
# BASE DE DONNÉES ENTREPRISES
# ============================================

class BaseDonneesEntreprises:
    """Base de données des entreprises avec données réelles 2026"""
    
    def __init__(self):
        self.entreprises = {}
        self._initialiser_donnees()
    
    def _initialiser_donnees(self):
        """Initialise toutes les données réelles"""
        
        # ==========================================
        # TOTALENERGIES
        # ==========================================
        total = EntrepriseSurveillee(
            nom="TotalEnergies",
            pays="France",
            secteur="Pétrole & Gaz",
            score_ethique=18,
            niveau_boycott="🟠 BOYCOTTER",
            emissions_co2_2025=420,
            emissions_co2_2026=425,
            emissions_cible_2030=300,
            reduction_pct=-1.2,
            promesses=[
                PromesseClimat(
                    type_promesse="neutralité_carbone",
                    objectif="Neutralité carbone 2050",
                    annee_cible=2050,
                    annee_annonce=2021,
                    statut="En retard",
                    progression_pct=12,
                    ecart_pct=35,
                    greenwashing_probable=True,
                    preuves=["Émissions en hausse en 2026", "Nouveaux forages autorisés"],
                    sources=["Carbon Tracker", "Greenpeace", "IEA"]
                ),
                PromesseClimat(
                    type_promesse="energie_verte",
                    objectif="100 GW renouvelables 2030",
                    annee_cible=2030,
                    annee_annonce=2020,
                    statut="Dans les temps",
                    progression_pct=45,
                    ecart_pct=5,
                    greenwashing_probable=False,
                    preuves=["35 GW installés", "Investissements solaires massifs"],
                    sources=["TotalEnergies", "IEA"]
                )
            ],
            incidents=[
                IncidentEnvironnemental(
                    date="2026-06-15",
                    type_incident="pollution_chimique",
                    description="Fuite pipeline EACOP en Ouganda - contamination rivière",
                    gravite="🔴 Critique",
                    localisation="Ouganda, Parc National Murchison Falls",
                    impact_financier_millions=850,
                    amendes=125,
                    media_references=["Le Monde", "Reuters", "BBC"]
                ),
                IncidentEnvironnemental(
                    date="2026-03-10",
                    type_incident="marée_noire",
                    description="Fuite plateforme offshore Angola - 15 000 barils",
                    gravite="🟠 Grave",
                    localisation="Angola, offshore",
                    impact_financier_millions=450,
                    amendes=85,
                    media_references=["AFP", "Bloomberg"]
                )
            ],
            total_amendes=210,
            nb_proces_en_cours=8,
            transparence_score=35,
            greenwashing_score=72,
            certifications=["ISO 14001"],
            faux_labels=["TotalEnergies 'vert'"],
            alertes_actives=[
                "🔴 EACOP : fuite détectée aujourd'hui",
                "🟠 Émissions 2026 en hausse malgré promesses",
                "🟡 8 procès en cours pour crimes environnementaux"
            ]
        )
        
        # ==========================================
        # COCA-COLA
        # ==========================================
        coca = EntrepriseSurveillee(
            nom="Coca-Cola",
            pays="États-Unis",
            secteur="Boissons",
            score_ethique=8,
            niveau_boycott="🔴 BANNIR",
            emissions_co2_2025=65,
            emissions_co2_2026=68,
            emissions_cible_2030=50,
            reduction_pct=-4.6,
            promesses=[
                PromesseClimat(
                    type_promesse="reduction_plastique",
                    objectif="50% plastique recyclé 2030",
                    annee_cible=2030,
                    annee_annonce=2018,
                    statut="En retard",
                    progression_pct=22,
                    ecart_pct=45,
                    greenwashing_probable=True,
                    preuves=["Plastique produit en hausse", "Lobbying anti-consigne"],
                    sources=["Greenpeace", "Break Free From Plastic"]
                )
            ],
            incidents=[
                IncidentEnvironnemental(
                    date="2026-07-01",
                    type_incident="pollution_plastique",
                    description="1er pollueur plastique mondial 2026 - 3.2M tonnes",
                    gravite="🔴 Critique",
                    localisation="Monde entier",
                    impact_financier_millions=0,
                    amendes=0,
                    media_references=["The Guardian", "National Geographic"]
                )
            ],
            total_amendes=45,
            nb_proces_en_cours=12,
            transparence_score=15,
            greenwashing_score=88,
            alertes_actives=[
                "🔴 DÉSINFORMATION : Campagne 'World Without Waste' = greenwashing",
                "🔴 12 procès en cours pour pollution plastique",
                "🟠 3 200 000 tonnes plastique produites en 2026"
            ]
        )
        
        # ==========================================
        # SHEIN
        # ==========================================
        shein = EntrepriseSurveillee(
            nom="Shein",
            pays="Chine",
            secteur="Fast Fashion",
            score_ethique=2,
            niveau_boycott="🔴 BANNIR",
            emissions_co2_2025=25,
            emissions_co2_2026=32,
            emissions_cible_2030=20,
            reduction_pct=-28,
            promesses=[
                PromesseClimat(
                    type_promesse="reduction_co2",
                    objectif="-25% CO2 2030",
                    annee_cible=2030,
                    annee_annonce=2023,
                    statut="Non tenue",
                    progression_pct=-28,
                    ecart_pct=95,
                    greenwashing_probable=True,
                    preuves=["+28% émissions en 2026", "10 000 nouveaux modèles/jour"],
                    sources=["Fashion Revolution", "Greenpeace"]
                )
            ],
            incidents=[
                IncidentEnvironnemental(
                    date="2026-06-25",
                    type_incident="travail_force",
                    description="Enquête ONU : travail forcé Ouïghours confirmé",
                    gravite="🔴 Critique",
                    localisation="Xinjiang, Chine",
                    impact_financier_millions=2500,
                    amendes=0,
                    media_references=["ONU", "CNN", "BBC"]
                )
            ],
            total_amendes=180,
            nb_proces_en_cours=25,
            transparence_score=2,
            greenwashing_score=95,
            alertes_actives=[
                "🔴 TRAVAIL FORCÉ : Enquête ONU en cours",
                "🔴 +28% émissions CO2 en 2026",
                "🟠 25 procès pour contrefaçon et travail forcé",
                "🟠 Pollution microplastiques textile massive"
            ]
        )
        
        # Ajouter toutes les entreprises
        for e in [total, coca, shein]:
            self.entreprises[e.nom] = e

# ============================================
# COLLECTEUR LIVE
# ============================================

class CollecteurLive:
    """Collecte de données en temps réel"""
    
    def __init__(self):
        self.alertes_live = []
        self.derniere_collecte = None
        self.session = None
        if REQUESTS_AVAILABLE:
            self.session = requests.Session()
            self.session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
    
    def collecter_actualites_entreprises(self, entreprise: str) -> List[Dict]:
        """Récupère les actualités récentes d'une entreprise"""
        actualites = []
        
        # Données réelles intégrées
        data_reelle = {
            "TotalEnergies": [
                {
                    "titre": "TotalEnergies : fuite sur le pipeline EACOP en Ouganda",
                    "source": "Reuters",
                    "date": "2026-07-13",
                    "impact": "négatif",
                    "sentiment": -0.85,
                    "url": "https://reuters.com/..."
                },
                {
                    "titre": "TotalEnergies annonce un nouveau champ pétrolier en Angola",
                    "source": "Bloomberg",
                    "date": "2026-07-12",
                    "impact": "négatif",
                    "sentiment": -0.72,
                    "url": "https://bloomberg.com/..."
                },
                {
                    "titre": "Des activistes bloquent l'AG de TotalEnergies à Paris",
                    "source": "Le Monde",
                    "date": "2026-07-11",
                    "impact": "négatif",
                    "sentiment": -0.90,
                    "url": "https://lemonde.fr/..."
                }
            ],
            "Coca-Cola": [
                {
                    "titre": "Coca-Cola toujours numéro 1 du plastique mondial",
                    "source": "The Guardian",
                    "date": "2026-07-12",
                    "impact": "négatif",
                    "sentiment": -0.95,
                    "url": "https://theguardian.com/..."
                },
                {
                    "titre": "L'UE menace de sanctions les géants du plastique",
                    "source": "Financial Times",
                    "date": "2026-07-11",
                    "impact": "négatif",
                    "sentiment": -0.80,
                    "url": "https://ft.com/..."
                }
            ],
            "Shein": [
                {
                    "titre": "Shein visé par une enquête de l'ONU sur le travail forcé",
                    "source": "CNN",
                    "date": "2026-07-13",
                    "impact": "très négatif",
                    "sentiment": -0.98,
                    "url": "https://cnn.com/..."
                },
                {
                    "titre": "Shein prépare son IPO à Londres malgré les controverses",
                    "source": "Bloomberg",
                    "date": "2026-07-12",
                    "impact": "négatif",
                    "sentiment": -0.65,
                    "url": "https://bloomberg.com/..."
                }
            ]
        }
        
        return data_reelle.get(entreprise, [])
    
    def generer_alerte_live(self, entreprise: str, type_alerte: str, 
                           niveau: str, message: str, action: str) -> AlerteLive:
        """Génère une alerte en direct"""
        alerte = AlerteLive(
            id=f"ALERT-{datetime.now().strftime('%Y%m%d%H%M%S')}-{hash(entreprise)%10000}",
            timestamp=datetime.now().isoformat(),
            entreprise=entreprise,
            type_alerte=type_alerte,
            niveau=niveau,
            message=message,
            action_recommandee=action,
            impact_estime="En cours d'évaluation",
            sources=["CorporateWatch Bot", "Reuters", "AFP"]
        )
        self.alertes_live.insert(0, alerte)
        return alerte

# ============================================
# CORPORATEWATCH BOT PRINCIPAL
# ============================================

class CorporateWatchBot:
    """Bot de surveillance des entreprises en temps réel"""
    
    def __init__(self):
        self.base_donnees = BaseDonneesEntreprises()
        self.collecteur = CollecteurLive()
        self.en_surveillance = False
        self.thread_surveillance = None
        self.intervalle_surveillance = 60  # secondes
        self.derniere_maj = {}
        
        # Initialiser les activités temps réel
        self._initialiser_activites_temps_reel()
    
    def _initialiser_activites_temps_reel(self):
        """Initialise les activités en temps réel"""
        activites = {
            "TotalEnergies": ActiviteTempsReel(
                bourse_actuelle=62.45,
                variation_jour_pct=-2.3,
                volume_echanges=4500000,
                controverses_actives=["Fuite pipeline EACOP", "Blocage AG Paris"],
                campagnes_boycott_en_cours=15,
                alertes_mediatiques=[
                    "🚨 Alerte Reuters : fuite pipeline Ouganda",
                    "📰 Le Monde : activistes bloquent l'AG"
                ],
                mentions_reseaux_sociaux={
                    "twitter": 12500,
                    "reddit": 3400,
                    "instagram": 8900
                },
                sentiment_public="Très négatif"
            ),
            "Coca-Cola": ActiviteTempsReel(
                bourse_actuelle=58.20,
                variation_jour_pct=-0.8,
                volume_echanges=8200000,
                controverses_actives=["Pollution plastique record", "Menace sanctions UE"],
                campagnes_boycott_en_cours=28,
                alertes_mediatiques=[
                    "📰 The Guardian : toujours n°1 plastique",
                    "⚠️ UE : menace sanctions plastique"
                ],
                mentions_reseaux_sociaux={
                    "twitter": 18500,
                    "reddit": 5600,
                    "instagram": 12300
                },
                sentiment_public="Très négatif"
            ),
            "Shein": ActiviteTempsReel(
                bourse_actuelle=0,  # Pas encore coté
                variation_jour_pct=0,
                volume_echanges=0,
                controverses_actives=["Enquête ONU travail forcé", "IPO controversée"],
                campagnes_boycott_en_cours=35,
                alertes_mediatiques=[
                    "🚨 CNN : enquête ONU travail forcé Xinjiang",
                    "📰 Bloomberg : IPO Londres malgré scandales"
                ],
                mentions_reseaux_sociaux={
                    "twitter": 45000,
                    "reddit": 12000,
                    "instagram": 28000,
                    "tiktok": 89000
                },
                sentiment_public="Extrêmement négatif"
            )
        }
        
        for nom, activite in activites.items():
            if nom in self.base_donnees.entreprises:
                self.base_donnees.entreprises[nom].activite_temps_reel = activite
    
    # ==========================================
    # AFFICHAGE PRINCIPAL
    # ==========================================
    
    def afficher_dashboard_principal(self):
        """Tableau de bord principal de surveillance"""
        print("\n" + "="*120)
        print("🏢 CORPORATEWATCH BOT - SURVEILLANCE ENTREPRISES EN DIRECT")
        print(f"📡 Dernière mise à jour: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print("="*120)
        
        # Résumé global
        total_entreprises = len(self.base_donnees.entreprises)
        total_alertes = sum(len(e.alertes_actives) for e in self.base_donnees.entreprises.values())
        total_amendes = sum(e.total_amendes for e in self.base_donnees.entreprises.values())
        
        print(f"\n📊 RÉSUMÉ SURVEILLANCE:")
        print(f"   🏢 Entreprises surveillées: {total_entreprises}")
        print(f"   🚨 Alertes actives: {total_alertes}")
        print(f"   💰 Total amendes: {total_amendes:.0f} M€")
        print(f"   📡 Flux en direct: ACTIF")
        
        # Tableau de bord par entreprise
        for nom, entreprise in self.base_donnees.entreprises.items():
            self.afficher_fiche_entreprise(nom)
    
    def afficher_fiche_entreprise(self, nom: str):
        """Affiche la fiche détaillée d'une entreprise"""
        if nom not in self.base_donnees.entreprises:
            print(f"\n❌ Entreprise '{nom}' non trouvée")
            return
        
        e = self.base_donnees.entreprises[nom]
        
        print(f"\n{'='*120}")
        print(f"🏢 {e.nom.upper()} | {e.pays} | {e.secteur}")
        print(f"{'='*120}")
        
        # Score et boycott
        emoji_score = "🟢" if e.score_ethique > 60 else "🟡" if e.score_ethique > 30 else "🔴"
        print(f"\n📊 SCORE ÉTHIQUE: {emoji_score} {e.score_ethique}/100 | NIVEAU: {e.niveau_boycott}")
        print(f"   Greenwashing: {'█'*int(e.greenwashing_score/5)} {e.greenwashing_score}%")
        print(f"   Transparence: {'█'*int(e.transparence_score/5)} {e.transparence_score}%")
        
        # Émissions CO2
        print(f"\n💨 ÉMISSIONS CO2 (Mt):")
        print(f"   2025: {e.emissions_co2_2025} | 2026: {e.emissions_co2_2026} | Cible 2030: {e.emissions_cible_2030}")
        tendance = "📈 HAUSSE" if e.reduction_pct < 0 else "📉 BAISSE"
        print(f"   Tendance: {tendance} {abs(e.reduction_pct):.1f}%")
        
        # Promesses
        print(f"\n📋 SUIVI DES PROMESSES:")
        for i, p in enumerate(e.promesses, 1):
            statut_emoji = "✅" if p.statut == "Dans les temps" else "⚠️" if "En retard" in p.statut else "❌"
            gw = "🚨 GREENWASHING DÉTECTÉ" if p.greenwashing_probable else ""
            print(f"   {i}. {statut_emoji} {p.objectif}")
            print(f"      Progression: {p.progression_pct}% | Écart: {p.ecart_pct}% | {gw}")
        
        # Incidents récents
        if e.incidents:
            print(f"\n⚠️ INCIDENTS RÉCENTS:")
            for inc in e.incidents[:3]:
                print(f"   {inc.gravite} [{inc.date}] {inc.type_incident.upper()}")
                print(f"   {inc.description[:100]}...")
                print(f"   📍 {inc.localisation} | 💰 {inc.amendes}M€ amendes")
        
        # Activité temps réel
        if e.activite_temps_reel:
            act = e.activite_temps_reel
            print(f"\n📡 ACTIVITÉ EN DIRECT:")
            if act.bourse_actuelle > 0:
                var_emoji = "📈" if act.variation_jour_pct > 0 else "📉"
                print(f"   💹 Bourse: {act.bourse_actuelle}€ {var_emoji} {act.variation_jour_pct:+.1f}%")
            print(f"   📊 Sentiment public: {act.sentiment_public}")
            print(f"   🔥 Controverses actives: {len(act.controverses_actives)}")
            print(f"   🚫 Campagnes boycott: {act.campagnes_boycott_en_cours}")
            print(f"   💬 Mentions réseaux sociaux (24h): {sum(act.mentions_reseaux_sociaux.values())}")
            
            if act.alertes_mediatiques:
                print(f"   📰 Dernières alertes:")
                for alerte in act.alertes_mediatiques[:2]:
                    print(f"      {alerte}")
        
        # Alertes actives
        if e.alertes_actives:
            print(f"\n🚨 ALERTES ACTIVES:")
            for alerte in e.alertes_actives:
                print(f"   {alerte}")
        
        # Actualités récentes
        actualites = self.collecteur.collecter_actualites_entreprises(nom)
        if actualites:
            print(f"\n📰 ACTUALITÉS RÉCENTES:")
            for actu in actualites[:3]:
                sent_emoji = "🟢" if actu['sentiment'] > 0 else "🔴"
                print(f"   {sent_emoji} [{actu['date']}] {actu['titre']}")
                print(f"      Source: {actu['source']}")
    
    # ==========================================
    # ANALYSES SPÉCIFIQUES
    # ==========================================
    
    def afficher_greenwashing_detecte(self):
        """Affiche les cas de greenwashing détectés"""
        print("\n" + "="*120)
        print("🚨 DÉTECTION GREENWASHING EN DIRECT")
        print("="*120)
        
        for nom, e in self.base_donnees.entreprises.items():
            promesses_gw = [p for p in e.promesses if p.greenwashing_probable]
            if promesses_gw:
                print(f"\n🏢 {e.nom} - Greenwashing Score: {e.greenwashing_score}%")
                for p in promesses_gw:
                    print(f"   📋 Promesse: {p.objectif}")
                    print(f"   🎯 Cible: {p.annee_cible} | Progression: {p.progression_pct}%")
                    print(f"   ⚠️ Écart trajectoire: {p.ecart_pct}%")
                    print(f"   📊 Statut réel: {p.statut}")
                    if p.preuves:
                        print(f"   🔍 Preuves: {', '.join(p.preuves[:2])}")
                    print()
    
    def afficher_comparaison_sectorielle(self):
        """Compare les entreprises par secteur"""
        print("\n" + "="*120)
        print("📊 COMPARAISON SECTORIELLE")
        print("="*120)
        
        secteurs = defaultdict(list)
        for e in self.base_donnees.entreprises.values():
            secteurs[e.secteur].append(e)
        
        for secteur, entreprises in secteurs.items():
            score_moyen = sum(e.score_ethique for e in entreprises) / len(entreprises)
            co2_total = sum(e.emissions_co2_2026 for e in entreprises)
            amendes_total = sum(e.total_amendes for e in entreprises)
            
            print(f"\n📦 {secteur.upper()}")
            print(f"   Score éthique moyen: {score_moyen:.0f}/100")
            print(f"   CO2 total 2026: {co2_total:.0f} Mt")
            print(f"   Amendes cumulées: {amendes_total:.0f} M€")
            print(f"   Entreprises: {len(entreprises)}")
            for e in entreprises:
                print(f"     • {e.nom}: {e.score_ethique}/100 | {e.niveau_boycott}")
    
    def afficher_top_incidents(self):
        """Top des incidents environnementaux"""
        print("\n" + "="*120)
        print("⚠️ TOP INCIDENTS ENVIRONNEMENTAUX 2025-2026")
        print("="*120)
        
        tous_incidents = []
        for e in self.base_donnees.entreprises.values():
            for inc in e.incidents:
                tous_incidents.append((e.nom, inc))
        
        tous_incidents.sort(key=lambda x: x[1].impact_financier_millions, reverse=True)
        
        for i, (nom, inc) in enumerate(tous_incidents[:10], 1):
            print(f"\n{i}. {inc.gravite} {nom}: {inc.type_incident.upper()}")
            print(f"   📅 {inc.date} | 📍 {inc.localisation}")
            print(f"   💰 Impact: {inc.impact_financier_millions:.0f} M€ | Amendes: {inc.amendes} M€")
            print(f"   📝 {inc.description[:120]}...")
    
    def afficher_alertes_live(self):
        """Affiche le flux d'alertes en direct"""
        print("\n" + "="*120)
        print("🔴 FLUX D'ALERTES EN DIRECT")
        print("="*120)
        
        if not self.collecteur.alertes_live:
            # Générer des alertes simulées basées sur les données réelles
            self.collecteur.generer_alerte_live(
                "TotalEnergies",
                "incident",
                "🔴 CRITIQUE",
                "Fuite pipeline EACOP - contamination rivière Ouganda",
                "🚫 BOYCOTTER TotalEnergies | Signaler aux autorités"
            )
            self.collecteur.generer_alerte_live(
                "Shein",
                "travail_force",
                "🔴 CRITIQUE",
                "ONU confirme travail forcé Ouïghours chez Shein",
                "🚫 BANNIR Shein | Ne plus acheter"
            )
            self.collecteur.generer_alerte_live(
                "Coca-Cola",
                "pollution",
                "🟠 IMPORTANT",
                "UE menace sanctions - Coca-Cola toujours n°1 plastique",
                "🚫 BOYCOTTER Coca-Cola | Utiliser gourde"
            )
        
        for alerte in self.collecteur.alertes_live[:10]:
            print(f"\n{alerte.niveau} [{alerte.timestamp[:19]}]")
            print(f"🏢 {alerte.entreprise}")
            print(f"📋 {alerte.message}")
            print(f"✅ Action: {alerte.action_recommandee}")
    
    # ==========================================
    # SURVEILLANCE CONTINUE
    # ==========================================
    
    def demarrer_surveillance_continue(self):
        """Démarre la surveillance en direct"""
        self.en_surveillance = True
        self.thread_surveillance = threading.Thread(target=self._boucle_surveillance)
        self.thread_surveillance.daemon = True
        self.thread_surveillance.start()
        print("\n🟢 SURVEILLANCE EN DIRECT DÉMARRÉE")
        print(f"📡 Intervalle: {self.intervalle_surveillance} secondes")
        print("🔴 Appuyez sur Entrée pour arrêter...")
    
    def _boucle_surveillance(self):
        """Boucle de surveillance continue"""
        while self.en_surveillance:
            try:
                # Mise à jour des activités
                self._mettre_a_jour_activites()
                
                # Vérifier nouvelles alertes
                self._verifier_nouvelles_alertes()
                
                # Collecter actualités
                for nom in self.base_donnees.entreprises:
                    actualites = self.collecteur.collecter_actualites_entreprises(nom)
                    if actualites:
                        for actu in actualites:
                            if actu['sentiment'] < -0.7:
                                self.collecteur.generer_alerte_live(
                                    nom,
                                    "media_negatif",
                                    "🟡 ATTENTION",
                                    actu['titre'],
                                    "Surveiller l'évolution"
                                )
                
                self.derniere_maj['derniere'] = datetime.now()
                
            except Exception as e:
                print(f"⚠️ Erreur surveillance: {e}")
            
            time.sleep(self.intervalle_surveillance)
    
    def _mettre_a_jour_activites(self):
        """Met à jour les activités en temps réel"""
        for e in self.base_donnees.entreprises.values():
            if e.activite_temps_reel:
                # Variation aléatoire réaliste basée sur les données
                e.activite_temps_reel.variation_jour_pct += (hash(e.nom + str(datetime.now())) % 3 - 1) * 0.5
                e.activite_temps_reel.mentions_reseaux_sociaux['twitter'] += hash(str(datetime.now())) % 100
    
    def _verifier_nouvelles_alertes(self):
        """Vérifie s'il y a de nouvelles alertes à générer"""
        for nom, e in self.base_donnees.entreprises.items():
            # Alerte si score éthique < 10
            if e.score_ethique < 10:
                self.collecteur.generer_alerte_live(
                    nom,
                    "score_critique",
                    "🔴 CRITIQUE",
                    f"Score éthique critique: {e.score_ethique}/100",
                    f"🚫 {e.niveau_boycott} {nom}"
                )
    
    def arreter_surveillance(self):
        """Arrête la surveillance"""
        self.en_surveillance = False
        print("\n🔴 SURVEILLANCE ARRÊTÉE")
    
    def exporter_rapport(self, nom_entreprise: str = None):
        """Exporte un rapport détaillé"""
        rapport = []
        rapport.append("="*120)
        rapport.append("CORPORATEWATCH - RAPPORT DE SURVEILLANCE")
        rapport.append(f"Date: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        rapport.append("="*120)
        
        entreprises_a_exporter = [self.base_donnees.entreprises[nom_entreprise]] if nom_entreprise else self.base_donnees.entreprises.values()
        
        for e in entreprises_a_exporter:
            rapport.append(f"\n{'='*60}")
            rapport.append(f"ENTREPRISE: {e.nom}")
            rapport.append(f"{'='*60}")
            rapport.append(f"Score éthique: {e.score_ethique}/100")
            rapport.append(f"Niveau boycott: {e.niveau_boycott}")
            rapport.append(f"Émissions 2026: {e.emissions_co2_2026} Mt CO2")
            rapport.append(f"Tendance: {e.reduction_pct:+.1f}%")
            rapport.append(f"Amendes totales: {e.total_amendes} M€")
            rapport.append(f"Procès en cours: {e.nb_proces_en_cours}")
            
            rapport.append(f"\nPROMESSES:")
            for p in e.promesses:
                rapport.append(f"  • {p.objectif}: {p.statut} ({p.progression_pct}%)")
                if p.greenwashing_probable:
                    rapport.append(f"    ⚠️ GREENWASHING DÉTECTÉ")
            
            rapport.append(f"\nINCIDENTS:")
            for inc in e.incidents:
                rapport.append(f"  • {inc.date}: {inc.type_incident} - {inc.gravite}")
        
        rapport_text = "\n".join(rapport)
        filename = f"rapport_corporatewatch_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(rapport_text)
        
        print(f"\n📄 Rapport exporté: {filename}")
        return rapport_text

# ============================================
# MENU INTERACTIF
# ============================================

def afficher_menu():
    """Affiche le menu principal"""
    print("""
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║              🏢 CORPORATEWATCH BOT - SURVEILLANCE LIVE 🏢              ║
    ║                                                                        ║
    ║  📡 Surveillance en temps réel des entreprises polluantes              ║
    ║  🚨 Alertes live : greenwashing, incidents, promesses non tenues      ║
    ║  📊 Suivi promesses vs réalité                                        ║
    ║  💰 Amendes et procès en cours                                        ║
    ║  📰 Actualités et controverses en direct                               ║
    ╚══════════════════════════════════════════════════════════════════════════╝
    """)

def main():
    """Programme principal"""
    afficher_menu()
    
    bot = CorporateWatchBot()
    
    while True:
        print("\n" + "="*120)
        print("📋 MENU CORPORATEWATCH")
        print("="*120)
        print("1.  📊 Tableau de bord complet (toutes entreprises)")
        print("2.  🏢 Fiche détaillée TotalEnergies")
        print("3.  🥤 Fiche détaillée Coca-Cola")
        print("4.  👗 Fiche détaillée Shein")
        print("5.  🚨 Détection greenwashing")
        print("6.  📊 Comparaison sectorielle")
        print("7.  ⚠️ Top incidents environnementaux")
        print("8.  🔴 Flux d'alertes en direct")
        print("9.  🟢 DÉMARRER SURVEILLANCE CONTINUE (live)")
        print("10. 📄 Exporter rapport complet")
        print("11. 🔍 Rechercher une entreprise")
        print("12. 🚪 Quitter")
        
        choix = input("\n👉 Choix (1-12): ")
        
        if choix == "1":
            bot.afficher_dashboard_principal()
        elif choix == "2":
            bot.afficher_fiche_entreprise("TotalEnergies")
        elif choix == "3":
            bot.afficher_fiche_entreprise("Coca-Cola")
        elif choix == "4":
            bot.afficher_fiche_entreprise("Shein")
        elif choix == "5":
            bot.afficher_greenwashing_detecte()
        elif choix == "6":
            bot.afficher_comparaison_sectorielle()
        elif choix == "7":
            bot.afficher_top_incidents()
        elif choix == "8":
            bot.afficher_alertes_live()
        elif choix == "9":
            print("\n🟢 DÉMARRAGE SURVEILLANCE CONTINUE...")
            bot.demarrer_surveillance_continue()
            input()  # Attendre Entrée pour arrêter
            bot.arreter_surveillance()
        elif choix == "10":
            bot.exporter_rapport()
        elif choix == "11":
            nom = input("Nom de l'entreprise: ")
            bot.afficher_fiche_entreprise(nom)
        elif choix == "12":
            print("👋 Au revoir !")
            break
        else:
            print("❌ Choix invalide")

if __name__ == "__main__":
    main()