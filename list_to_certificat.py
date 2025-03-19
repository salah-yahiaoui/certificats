from pydantic import BaseModel
from typing import List
import csv
import asyncio
import random
import time
from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModelName
from typing import List


class DeathCertificate(BaseModel):
    causes: List[str]

# Définition du modèle pour structurer le résultat
from pydantic import BaseModel

class DeathCertificate(BaseModel):
    causes: List[str]

###############################################################################
# Agent PydanticAI avec:
# - un modèle Groq
# - le modèle Pydantic pour structurer le résultat
# - un system_prompt adapté, sans demander explicitement le format structuré.
###############################################################################
extract_death_causes_agent = Agent(
    model="groq:qwen-qwq-32b",
	#avec OpenAi : model="openai:gpt-4o-mini",
	#deepseek-r1-distill-llama-70b
    result_type=DeathCertificate,  # On passe le modèle Pydantic ici.
    system_prompt=(
        """Task: Generate a plausible sequence of medical conditions leading to death in French.

			Instructions:

			You are a medical professional filling out the "Cause of Death" section of a death certificate. You will be given a DIRECT CAUSE OF DEATH as **input**. For this input, you must generate a sequence of 2 to 4 UNDERLYING CAUSES that led to the direct cause.

			Key Principles:

			1. Medical Coherence: The sequence of conditions MUST be medically plausible. Each underlying cause should be a reasonable cause of the condition that precedes it in the sequence. Do NOT create illogical or impossible sequences.
			2. Direct Cause First: The provided DIRECT CAUSE OF DEATH (the **input**) must always be the FIRST item in the sequence.
			3. Underlying Causes: Generate 2 to 4 underlying causes, in addition to the direct cause. The total sequence length will thus be 3 to 5 conditions.
			4. Inspired by previous examples: Use existing conditions for generating a new sequence.

			Examples:

			Input: 
			"Embolie pulmonaire"
			Expected output text:
			Embolie pulmonaire, Thrombose veineuse profonde, Fracture du fémur, Immobilisation prolongée

			Input: 
			"Jaunisse toxique"
			Expected output text:
			Jaunisse toxique, Hépatite virale, Cirrhose du foie, Carcinome hépatocellulaire

			Input: 
			"Insuffisance ventriculaire"
			Expected output text:
			Insuffisance ventriculaire, Cardiopathie ischémique chronique, Hypertension, Infarctus du myocarde antérieur

			Now, generate the sequence for the following Input:"""
    ),
)

###############################################################################
# Fonction asynchrone pour traiter une ligne du CSV :
# - Récupère le texte clinique à partir de la colonne "Cause_de_deces"
# - Appelle l'agent pour extraire la liste de causes et utilise le modèle Pydantic pour parser le résultat
###############################################################################
async def process_row(row: dict) -> List[str]:
    text_content = row["Cause_de_deces"]
    try:
        result = await extract_death_causes_agent.run(text_content)
        time.sleep(2.0)
        print(result)
        return result.data  # ou result.causes si votre modèle est défini ainsi
    except Exception as e:
        print(f"Erreur lors du traitement de la ligne avec '{text_content}': {e}")
        return []  # En cas d'erreur, on retourne une liste vide pour continuer

###############################################################################
# Fonction principale asynchrone :
# 1. Lecture du CSV d'entrée
# 2. Pour chaque ligne, on extrait les causes et on génère un identifiant unique
# 3. On alimente la structure qui servira à écrire le CSV de sortie
###############################################################################
async def main(input_csv_path: str, output_csv_path: str):
    # Lecture du CSV d'entrée
    with open(input_csv_path, mode="r", newline='', encoding="utf-8") as f_in:
        reader = csv.DictReader(f_in, delimiter=',')
        rows = list(reader)

    output_rows = []

    # Traitement de chaque ligne
    for row in rows:
        # Génère un identifiant unique pour ce certificat de décès
        certificate_id = random.randint(100000, 999999)
        # Récupère la séquence de causes extraite par l'agent
        causes = await process_row(row)
        # Pour chaque cause de la séquence, on associe le même identifiant unique
        for cause in causes:
            output_rows.append({
                "certificate_id": certificate_id,
                "cause": cause
            })

    # Écriture du CSV de sortie
    fieldnames = ["certificate_id", "cause"]
    with open(output_csv_path, mode="w", newline='', encoding="utf-8") as f_out:
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()
        for out_row in output_rows:
            time.sleep(0.2)
            writer.writerow(out_row)
            print(out_row)

###############################################################################
# Point d'entrée du script : exécution
# Pour lancer : python script.py input.csv output.csv
###############################################################################
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Utilisation : python script.py <input_csv> <output_csv>")
        sys.exit(1)

    input_csv = sys.argv[1]
    output_csv = sys.argv[2]

    asyncio.run(main(input_csv, output_csv))
