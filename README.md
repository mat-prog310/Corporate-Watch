# 🏢 CorporateWatch Bot

![Version](https://img.shields.io/badge/version-2.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8%2B-green)
![Licence](https://img.shields.io/badge/licence-MIT-orange)
![Status](https://img.shields.io/badge/status-active-success)

> 🌍 Surveillance en temps réel des entreprises polluantes - Détection de greenwashing - Système de boycott éthique

---

## 📖 Table des matières

- [Aperçu](#-aperçu)
- [Fonctionnalités](#-fonctionnalités)
- [Installation](#-installation)
- [Utilisation](#-utilisation)
- [Entreprises surveillées](#-entreprises-surveillées)
- [Système de boycott](#-système-de-boycott)
- [Sources de données](#-sources-de-données)
- [Architecture](#-architecture)
- [Contribution](#-contribution)
- [Licence](#-licence)

---

## 🌟 Aperçu

**CorporateWatch Bot** est une intelligence artificielle écologique qui surveille en continu les pratiques environnementales des plus grandes entreprises mondiales. Elle analyse leurs émissions de CO₂, détecte le greenwashing, vérifie le respect de leurs promesses climatiques et recommande des actions de boycott ciblées.

### 🎯 Objectifs

- **Surveiller** les 50 entreprises les plus polluantes au monde
- **Détecter** le greenwashing et les fausses promesses
- **Informer** sur les alternatives éthiques
- **Agir** via des recommandations de boycott

---

## ⚡ Fonctionnalités

### 📊 Tableau de bord complet
- Score éthique sur 100 pour chaque entreprise
- Émissions CO₂ détaillées (Scope 1, 2, 3)
- Niveau de boycott : 🔴 BANNIR / 🟠 BOYCOTTER / 🟡 ÉVITER
- Historique des incidents environnementaux

### 🚨 Détection de greenwashing
- Comparaison promesses vs réalité
- Analyse des écarts par rapport aux objectifs climatiques
- Détection automatique des fausses promesses
- Indice de greenwashing calculé en temps réel

### ⚠️ Incidents environnementaux
- Suivi des marées noires, pollutions chimiques, déforestation
- Cumul des amendes environnementales
- Procès en cours contre les entreprises
- Estimation de l'impact financier des dégâts

### 🚫 Système de boycott intelligent
- **🔴 BANNIR** : Impact catastrophique, aucune volonté de changement
- **🟠 BOYCOTTER** : Impact grave, efforts insuffisants
- **🟡 ÉVITER** : Problèmes documentés, transition possible
- **✅ ALTERNATIVES** : Suggestions éthiques pour chaque produit

### 📡 Surveillance en direct
- Alertes live sur les controverses
- Sentiment public sur les réseaux sociaux
- Actualités en temps réel
- Campagnes de boycott en cours

### 📄 Export de rapports
- Rapports détaillés par entreprise
- Comparaisons sectorielles
- Statistiques globales
- Export au format TXT

---

## 🚀 Installation

### Prérequis

- **Python** 3.8 ou supérieur
- **pip** (gestionnaire de paquets Python)

### Installation rapide

```bash
# Cloner le dépôt
git clone https://github.com/votre-username/corporate-watch.git
cd corporate-watch

# Installation minimale (fonctionne sans dépendances externes)
pip install requests beautifulsoup4

# Installation complète (recommandée)
pip install requests beautifulsoup4 pandas matplotlib seaborn
Vérification de l'installation
bash
python -c "import corporatewatch; print('✅ Installation réussie !')"
💻 Utilisation
Lancement
bash
python corporatewatch.py
Menu principal
text
📋 MENU CORPORATEWATCH
==================================================
1.  📊 Tableau de bord complet (toutes entreprises)
2.  🏢 Fiche détaillée TotalEnergies
3.  🥤 Fiche détaillée Coca-Cola
4.  👗 Fiche détaillée Shein
5.  🚨 Détection greenwashing
6.  📊 Comparaison sectorielle
7.  ⚠️ Top incidents environnementaux
8.  🔴 Flux d'alertes en direct
9.  🟢 DÉMARRER SURVEILLANCE CONTINUE (live)
10. 📄 Exporter rapport complet
11. 🔍 Rechercher une entreprise
12. 🚫 MENU BOYCOTT (produits à bannir/éviter)
13. 🚪 Quitter
Exemple d'utilisation
python
from corporatewatch import CorporateWatchBot

# Initialiser le bot
bot = CorporateWatchBot()

# Afficher le tableau de bord complet
bot.afficher_dashboard_complet()

# Vérifier une entreprise spécifique
bot.afficher_fiche_entreprise("TotalEnergies")

# Détecter le greenwashing
bot.afficher_greenwashing_detecte()

# Voir les produits à boycotter
bot.base_boycott.afficher_produits_a_boycotter("Fast Fashion")
