# Immoweb Scraper

## Description

Ce script Python permet de récupérer les liens d'annonces immobilières à partir du site [Immoweb](https://www.immoweb.be/fr) et de scruter les détails de chaque annonce pour les stocker dans un fichier CSV.

## Prérequis

1. **Environnement Python :** Assurez-vous d'avoir Python installé sur votre machine. Vous pouvez le télécharger depuis [le site officiel de Python](https://www.python.org/).

2. **Dépendances :** Installez les dépendances nécessaires en utilisant la commande suivante :
    ```bash
    pip install beautifulsoup4 pandas requests selenium
    ```

3. **WebDriver Selenium :** Le script utilise Selenium pour charger dynamiquement les pages web. Assurez-vous d'avoir un WebDriver compatible avec votre navigateur installé. Vous pouvez télécharger [ChromeDriver](https://sites.google.com/chromium.org/driver/) pour Google Chrome, par exemple.

## Utilisation

### 1. Récupération des URLs
La première partie du script récupère les liens des annonces immobilières et les enregistre dans un fichier texte (`url_list.txt`). Pour exécuter cette partie, utilisez la commande suivante :
    ```bash
    python retrieve_urls.py
    ```

### 2. Extraction des détails
La deuxième partie du script charge chaque URL, extrait les détails de l'annonce et les stocke dans un fichier CSV (`records_<timestamp>.csv`). Pour exécuter cette partie, utilisez la commande suivante :
    ```bash
    python ImmoKad.py
    ```

Assurez-vous d'avoir le fichier `url_list.txt` généré par la première partie du script dans le même répertoire.

## Structure des fichiers

- **retrieve_urls.py :** Contient le code pour récupérer les liens d'annonces immobilières.
- **ImmoKad.py :** Contient le code pour extraire les détails des annonces immobilières en utilisant les liens récupérés.
- **RECORDS/ :** Dossier où les fichiers CSV avec les détails des annonces sont enregistrés.
- **url_list.txt :** Fichier texte contenant les liens d'annonces immobilières.

## Remarques

- Le script utilise BeautifulSoup pour l'analyse HTML statique et Selenium pour le chargement dynamique des pages web.
- Assurez-vous d'avoir un accès internet stable pendant l'exécution du script.


