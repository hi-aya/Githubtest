# Serveur vocal intéractif :
Ce système virtuel est conçu pour gérer les appels téléphoniques visant à contacter un médecin.

Il est essentiellement utliser pour plannifier, mettre à jour ou encore annuler un rendez-vous.

Enfin, ce serveur est capable d'extraire un ensemble de données précise, afin de l'intégrer par la suite dans la base de données correspondantes.

## Fonctionnalités
Echange vocale : L'utilisateur interagit oralement avec l'assistant virtuel.

Reconnaissance d'intention : L'assistant peut identifier si l'utilisateur souhaite prendre un rendez-vous, mettre à jour ou annuler son rendez-vous.

Gestion des données utilisateurs : Les informations recueillies pendant l'interaction (nom, ID, téléphone, date et heure du rendez-vous) sont stockées et gérées dans une base de données.

## Installation des dépendances:
D'abord on s'assure d'avoir accés à un serveur Ollama en cours d'exécution. Il faut qu'il soit correctement configuré.

Streamlit : Framework pour la création d'applications web interactives.
Langchain : Bibliothèque utilisée pour la gestion des modèles de langage (LLM).
SpeechRecognition : Bibliothèque pour la reconnaissance vocale.
pyttsx3 : Bibliothèque pour la synthèse vocale hors ligne.
DataBase : Fichier personnalisé pour gérer les opérations sur la base de données.

```bash
pip install streamlit langchain pyttsx3 SpeechRecognition ollama
```
## Fonctionnement :

Le modèle ci-dessous génère des conversations avec l'utilisateur sans avoir recours à l'historique de la discussion. 

Lancez l'application Streamlit en exécutant la commande suivante dans votre terminal :

```bash
streamlit run app.py
```

Interaction vocale : Lorsque vous cliquez sur le bouton "Record Audio", l'application reçoit votre voix. Vous pouvez alors exprimer vos besoins.L'assistant reconnaît vos commandes et agit en conséquence.

Reconnaissance d'intention et extraction des informations : Une fois l'instruction reconnue, l'assistant utilise le modèle OllamaLLM pour identifier -l'intention de l'utilisateur et extraire les informations pertinentes (nom, ID, téléphone, date, heure).

Gestion des rendez-vous : Selon l'intention identifiée, l'assistant va :

- Planifier un rendez-vous : Si l'intention est liée à la prise d'un nouveau rendez-vous.
- Mettre à jour un rendez-vous : Si l'intention est liée à une mise à jour.
- Annuler un rendez-vous : Si l'intention est liée à l'annulation.

Base de données : Les informations sur les utilisateurs et leurs rendez-vous sont stockées dans la base de données à l'aide des fonctions create_db, add_user, update_user, et delete_user.

Synthèse vocale : Après chaque interaction, l'assistant répond en utilisant la synthèse vocale.
