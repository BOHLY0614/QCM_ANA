import os
import json
import random

# Nom du fichier de stats
STATS_FILE = "question_stats.json"

def get_json_dir(base_path):
    """Retourne le chemin du dossier JSON"""
    return os.path.join(os.path.dirname(os.path.abspath(base_path)), "JSON")

def load_chapters(json_dir):
    """Charge tous les chapitres JSON du dossier spécifié"""
    chapter_files = []
    chapters_data = {}
    
    if os.path.exists(json_dir):
        files = [f for f in os.listdir(json_dir) if f.endswith('.json')]
        files.sort()
        chapter_files = [os.path.join(json_dir, f) for f in files]
    else:
        print(f"Erreur : Le dossier {json_dir} est introuvable.")
        return [], {}

    for file_path in chapter_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                chapter_data = json.load(f)
                # On s'assure que chaque question connait son fichier source
                for question in chapter_data:
                    question["source_file"] = file_path
                chapters_data[file_path] = chapter_data
        except Exception as e:
            print(f"Erreur lors du chargement de {file_path}: {e}")
            
    return chapter_files, chapters_data

def load_stats():
    """Charge les statistiques depuis le fichier JSON"""
    if os.path.exists(STATS_FILE):
        try:
            with open(STATS_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_stats(stats):
    """Sauvegarde les statistiques"""
    try:
        with open(STATS_FILE, "w") as f:
            json.dump(stats, f)
    except Exception as e:
        print(f"Erreur sauvegarde stats: {e}")

def get_question_key(question_data):
    """Génère une clé unique pour une question (Source + ID)"""
    source = question_data.get("source_file", "unknown")
    q_id = question_data.get("id", "0")
    return f"{source}|{q_id}"

def smart_select_questions(question_list, number_to_select, stats):
    """Sélectionne intelligemment les questions (priorité aux erreurs/non vues)"""
    # Copie pour ne pas modifier la liste originale
    shuffled_list = list(question_list)
    random.shuffle(shuffled_list)

    def get_seen_count(q):
        key = get_question_key(q)
        q_stats = stats.get(str(key), {"correct": 0, "incorrect": 0})
        # On peut pondérer ici : une erreur "pèse" moins lourd qu'une réussite
        # pour qu'on retombe dessus plus vite, mais restons simple pour l'instant:
        # On trie par nombre total de vues (moins vue = prioritaire)
        return q_stats["correct"] + q_stats["incorrect"]

    shuffled_list.sort(key=get_seen_count)
    
    return shuffled_list[:min(number_to_select, len(shuffled_list))]

def update_question_in_file(question_data, new_q, new_opts, new_correct):
    """Met à jour une question directement dans le fichier source JSON"""
    source_file = question_data.get("source_file")
    if source_file and os.path.exists(source_file):
        try:
            with open(source_file, "r", encoding="utf-8") as f:
                full_data = json.load(f)
            
            found = False
            for idx, q in enumerate(full_data):
                if q["id"] == question_data["id"]:
                    full_data[idx]["question"] = new_q
                    full_data[idx]["options"] = new_opts
                    full_data[idx]["correct_answers"] = new_correct
                    found = True
                    break
            
            if found:
                with open(source_file, "w", encoding="utf-8") as f:
                    json.dump(full_data, f, indent=4, ensure_ascii=False)
                return True, f"Sauvegardé dans {os.path.basename(source_file)}"
            else:
                return False, "Question non trouvée dans le fichier source."
        except Exception as e:
            return False, str(e)
    return False, "Fichier source introuvable."

def get_incorrect_questions(all_questions, stats):
    incorrect_questions = []
    
    if not stats:
        return []

    for q in all_questions:
        key = get_question_key(q)
        q_stats = stats.get(str(key))
        
        if q_stats and q_stats.get("incorrect", 0) > 0:
            incorrect_questions.append(q)
            
    return incorrect_questions