# Serveur vocal intéractif 
Ce système est conçu pour intéragir avec les appels téléphoniques qui vise à contacter un médecin.

## Installation du LLM
Installation des bibliothèques :
D'abord on s'assure d'avoir accés à un serveur Ollama en cours d'exécution. Il faut qu'il soit correctement configuré.

Puis on installe langchain, langchain_ollama afin de connecter Ollama comme llm :
```bash
pip install langchain langchain-ollama
```
### configuration de cet LLM :

Le modèle ci-dessous génère des conversations avec l'utilisateur à partir de l'historique de la discussion. 
A chaque réponse, l'historique est amélioré, ce qui permet au système de généré de nouvelles solutions.
Au cours de la discussion, notre modèle doit etre capable de détecter l'intention de l'interlocuteur et savoir si il veut fixer un rendez-vous ou changer sa date.

```bash
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from db_manage import create_database,add_user,remove_user,edit_user

template="""
the chat history is {context}
User: {question}
"""

Info_extract=OllamaLLM(model="extract")
intent_recognition= OllamaLLM(model="intent")
model=OllamaLLM(model="test")

lista=["Full_name","ID","phone number","DATE","TIME"]

user={"Full_name":"",
       "ID":"",
       "phone_number":"",
       "DATE":"",
       "TIME":""
}



prompt=ChatPromptTemplate.from_template(template)
chain = prompt | model


History=""
context=""
print("Hello there,i am your AI assistant for today.")
while True:
    user_input=input("you: ")
    if user_input.lower() in ["exit","bye"]:
        break
    History+=user_input+"\n"
    result=chain.invoke({"context":context,"question":user_input})
    print("Bot: ",result)
    context += f"\nUser: {user_input}\nAI: {result}"



Intent=intent_recognition(History)

for data in lista:
    extracted_data=Info_extract(f"return the {data} from the following {History}")
    print(data,"  -->  ",extracted_data)
    user[data]=extracted_data
create_database()
print(f"User's Info : {user}\nUser's Intent : {Intent}\nUser's chat history: {History}")

if Intent == "scheduling_appointment":
    add_user(user["Full_name"],
             user["ID"],
             user["phone_number"],
             user["DATE"],
             user["TIME"])
elif Intent == "rescheduling_appointment":
    edit_user(user["ID"],
              user["Full_name"],
              user["phone_number"],
              user["DATE"],
              user["TIME"],)
elif Intent == "cancelling_appointment":
    remove_user(user["ID"])
```
