# how-to-linguistics
Usage of Pareto Principle to automate vocabulary selection when learning languages using Leipzig Corpora collection
This project is a tool to download, extract, and process corpora from the Leipzig Corpora Collection. It allows the user to:
- Choose a language from a predefined set.
- Fetch available corpus file links (tar.gz files) from the Leipzig website.
- Download multiple corpus files simultaneously.
- Extract the downloaded archives into a common extraction directory.
- Process all extracted text files as one unified corpus.
- Tokenize the text, compute word frequency counts (excluding numbers), and export the top tokens (with their English translations) to a CSV file.
- Print a summary of each token’s frequency during CSV writing.

## Features
- **Multi-Source Download:** Select multiple corpus files and process them as one combined corpus.
- **Automatic Processing:** Recursively processes all text files from extracted directories.
- **Translation:** Uses a translation API (via deep_translator) to translate words into English.
- **Reuse Existing Downloads:** Checks for already downloaded archives and extracted directories to save time.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/pareto-corpus.git
   cd pareto-corpus
2. Install this inside of a virtual environnement
   ```bash
   python3 -m venv venv
   source venv/bin/activate
3. Install the requirements
   ```bash
   pip install -r requirements.txt
===============================================================================

Utilisation du Principe de Pareto pour Automatiser la Sélection du Vocabulaire lors de l'Apprentissage des Langues avec la Collection de Corpus de Leipzig
Ce projet est un outil permettant de télécharger, extraire et traiter des corpus issus de la Leipzig Corpora Collection. Il permet à l'utilisateur de :
- Choisir une langue parmi un ensemble prédéfini.
- Récupérer les liens des fichiers corpus disponibles (fichiers tar.gz) depuis le site de Leipzig.
- Télécharger simultanément plusieurs fichiers de corpus.
- Extraire les archives téléchargées dans un répertoire d'extraction commun.
- Traiter tous les fichiers texte extraits comme un corpus unifié.
- Tokeniser le texte, calculer les fréquences des mots (en excluant les nombres) et exporter les tokens les plus fréquents (avec leurs traductions en anglais) dans un fichier CSV.
- Afficher un résumé de la fréquence de chaque token lors de l'écriture du CSV.

## Fonctionnalités
- **Téléchargement multi-sources :** Sélectionnez plusieurs fichiers de corpus et traitez-les comme un corpus combiné.
- **Traitement automatique :** Traite récursivement tous les fichiers texte des répertoires extraits.
- **Traduction :** Utilise une API de traduction (via deep_translator) pour traduire les mots en anglais.
- **Réutilisation des téléchargements existants :** Vérifie si les archives ont déjà été téléchargées et si les répertoires d'extraction existent afin de gagner du temps.

## Installation

1. Clonez le dépôt :
   ```bash
   git clone https://github.com/<votre-nom-utilisateur>/pareto-corpus.git
   cd pareto-corpus
2. Mettre en place un environnement virtuel
   ```bash
   python3 -m venv venv
   source venv/bin/activate
3. Installer les librairies
   ```bash
   pip install -r requirements.txt
