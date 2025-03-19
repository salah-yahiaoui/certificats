# Générateur certificats de décès

Ce projet utilise [pydantic-ai](https://ai.pydantic.dev/) pour extraire et structurer automatiquement une séquence de causes de décès à partir d'une entrée textuelle. Le script lit un fichier CSV d'entrée, traite chaque ligne en utilisant un agent configuré avec un modèle Groq, et génère un fichier CSV de sortie avec un identifiant unique pour chaque certificat.

## Prérequis

Installez la bibliothèque `pydantic-ai` avec pip :

```bash
pip install pydantic-ai
```

Pour plus d'informations sur `pydantic-ai`, consultez la [documentation officielle](https://ai.pydantic.dev/).

## Configuration des clés API

Ce script utilise des modèles de langage (LLM) et nécessite la configuration de clés API dans vos variables d'environnement.

### Pour les LLM de OpenAI

- **Windows :**
  ```bash
  set OPENAI_API_KEY=your-api-key
  ```
- **Linux/MacOS :**
  ```bash
  export OPENAI_API_KEY=your-api-key
  ```

### Pour les LLM disponibles via Groq

- **Windows :**
  ```bash
  set GROQ_API_KEY=your-api-key
  ```
- **Linux/MacOS :**
  ```bash
  export GROQ_API_KEY=your-api-key
  ```

## Utilisation

Pour lancer le script, ouvrez un terminal et exécutez la commande suivante :

```bash
python list_to_certificat.py <input_csv> <output_csv>
```

- `<input_csv>` : chemin vers le fichier CSV d'entrée.
- `<output_csv>` : chemin vers le fichier CSV de sortie.

## Description du code

Le script réalise les étapes suivantes :

1. **Lecture du CSV d'entrée**  
   Le script lit le fichier CSV fourni, contenant une colonne nommée `Cause_de_deces`.

2. **Traitement asynchrone des données**  
   Pour chaque ligne, le script :
   - Génère un identifiant unique.
   - Appelle l'agent PydanticAI configuré avec un modèle Groq pour extraire une séquence de causes de décès.
   - Affiche et enregistre le résultat.

3. **Écriture du CSV de sortie**  
   Chaque cause extraite est associée à l'identifiant unique et écrite dans le fichier CSV de sortie.

## Exemple

Pour exécuter le script avec un fichier d'entrée `input.csv` et obtenir un fichier de sortie `output.csv`, utilisez la commande suivante :

```bash
python script.py input.csv output.csv
```

## Remarques

- **Clés API :** Assurez-vous que les variables d'environnement (clé API OpenAI ou Groq) sont correctement configurées avant d'exécuter le script.
- **Fonctionnement asynchrone :** Le script utilise des fonctions asynchrones pour traiter chaque ligne du CSV, améliorant ainsi la gestion des appels vers le LLM.

