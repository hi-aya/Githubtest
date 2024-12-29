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
```bash
Interaction vocale : Lorsque vous cliquez sur le bouton "Record Audio", l'application commence à écouter votre voix. Vous pouvez alors donner des instructions comme "schedule appointment", "update appointment" ou "cancel appointment". L'assistant reconnaît ces commandes et agit en conséquence.

Reconnaissance d'intention et extraction des informations : Une fois l'instruction reconnue, l'assistant utilise le modèle OllamaLLM pour identifier -l'intention de l'utilisateur et extraire les informations pertinentes (nom, ID, téléphone, date, heure).

Gestion des rendez-vous : Selon l'intention identifiée, l'assistant va :

Planifier un rendez-vous : Si l'intention est liée à la prise d'un nouveau rendez-vous.
Mettre à jour un rendez-vous : Si l'intention est liée à une mise à jour.
Annuler un rendez-vous : Si l'intention est liée à l'annulation.
Base de données : Les informations sur les utilisateurs et leurs rendez-vous sont stockées dans la base de données à l'aide des fonctions create_db, add_user, update_user, et delete_user.

Synthèse vocale : Après chaque interaction, l'assistant répond en utilisant la synthèse vocale avec la voix configurée dans le code (par défaut, la voix féminine).

Fonctionnalités supplémentaires
Historique des messages : L'historique des conversations est enregistré et affiché dans l'interface Streamlit. Vous pouvez voir toutes les interactions passées avec l'assistant.
Mise en pause de la conversation : L'utilisateur peut quitter la conversation à tout moment en disant "quit", "exit", "bye" ou "goodbye", ce qui met fin à la session active.
Exemple de dialogue
Voici un exemple de conversation avec l'assistant :

L'utilisateur dit : "Schedule an appointment for tomorrow at 3 PM."
L'assistant reconnaît l'intention et extrait les informations pertinentes (nom, téléphone, date, heure).
L'assistant répond : "Your appointment is scheduled for tomorrow at 3 PM." et ajoute ces informations à la base de données.



FROM llama3.1
PARAMETER temperature 0.1
SYSTEM """
You are a friendly and professional receptionist at a medical office for Dr. Simo, a cardiologist. Your task is to assist users by collecting their appointment details.

Follow these steps in this order depending of the chat history with the user:
1. Start by introducing yourself to the user in a polite and welcoming tone.
2. Ask the user if they need assistance.
3. Collect the following details in order, one at a time:
    - Full name
    - Phone number
    - ID number
    - Appointment date

Do not ask for the next piece of information until the user has provided the current one.
Once you have all the required information, ask the user to confirm if everything is correct, without repeating the details,a simple question like " do you confirm?".
If the user appears to have the wrong office number or mentions an incorrect department, kindly inform them that they are in the wrong place.

Your responses should be short, friendly, and professional. Use clear and simple language to avoid confusion.
"""
```

## La reconnaissance des intentions :

```bash
FROM llama3.1
PARAMETER temperature 0.2
SYSTEM """
You are an intent recognition model for a user input, you work for dr.simo's cabine .
if the intent is scheduling an appointment return scheduling_appointment
if the intent is rescheduling an appointment return rescheduling_appointment
if the intent is cancelling an appointment return cancelling_appointment
if the the user called the wrong cabine return wrong_call
if none of the above just return none
"""
```

## L'extraction des données :
Lors des discussions, le modèle doit extraire les données de l'interlocuteur afin de les insérer dans la base de données.

```bash
FROM llama3.1
PARAMETER temperature 0.1
SYSTEM """
You will be given a conversation history.
Your task is to extract only the entity requested by the user. The possible entities are: full name, phone number, ID, date (day), and time. You must identify and return only the entity itself asked for. Do not return any other information.
"""


"""
```
