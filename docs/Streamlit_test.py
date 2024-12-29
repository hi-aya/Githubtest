import streamlit as st
from langchain_ollama import OllamaLLM
import pyttsx3
import speech_recognition as sr
from ollama import Client  
from DataBase import *
import json

client = Client()
Info_extract=OllamaLLM(model="testox")
intent_recognition= OllamaLLM(model="intent1")
lista=["name","id","phone","date","time"]
messages =[]
user={"name":"",
       "id":"",
       "phone":"",
       "date":"",
       "time":""
}
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id) 

recognizer = sr.Recognizer()


st.title("Welcome to DR.Simo's Cabine")
st.write("Click the button below to initiate the assistant ! ")


if "messages" not in st.session_state:
    st.session_state.messages = []  
if "conversation_active" not in st.session_state:
    st.session_state.conversation_active = True  



if st.session_state.conversation_active and st.button("Record Audio"):
    st.write("Recording... Speak now.")
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)  
            audio = recognizer.listen(source, timeout=10 ,phrase_time_limit=None)  


        user_input = recognizer.recognize_google(audio,language="en-EN")
        
        st.write(f"Recognized Query: {user_input}")


        if user_input.lower() in ['quit', 'exit', 'bye' , 'goodbye']:
            st.write("Ending the conversation. Goodbye!")
            engine.say("Goodbye!")
            engine.runAndWait()
            st.session_state.conversation_active = False 
            Intent=intent_recognition.invoke(st.session_state.messages)
            st.write("intent --> ",Intent)
            response=Info_extract.invoke(st.session_state.messages)
            st.write("data --> ",response)
            json_response=json.loads(response)
            for data in lista:
                user[data]=json_response[data]
            create_db()
            if "new" in Intent.lower()  :
                st.write("scheduling appointment ...")
                add_user(user["name"],
                        user["id"],
                        user["phone"],
                        user["date"],
                        user["time"])
            elif "update" in Intent.lower():
                st.write("re-scheduling appointment ...")
                update_user(user["name"],
                            user["id"],
                            user["phone"],
                            user["date"],
                            user["time"],)
            elif "cancel" in Intent.lower():
                print("cancelling appointment ...")
                delete_user(user["id"])
        else:
            st.session_state.messages.append({
                'role': 'user',
                'content': user_input
            })

            response = client.chat(model='final', messages=st.session_state.messages)
           
            assistant_reply = response['message']['content']

            st.session_state.messages.append({
                'role': 'assistant',
                'content': assistant_reply
            })

            st.write("Assistant:", assistant_reply)

            engine.say(assistant_reply)
            engine.runAndWait()

    except sr.UnknownValueError:
        st.write("Sorry, I could not understand your voice. Please try again.")
    except sr.RequestError as e:
        st.write(f"Error with the Speech Recognition service: {e}")
    except Exception as e:
        st.write(f"An error occurred: {e}")

if st.session_state.messages:
    st.subheader("Chat History:")
    for msg in st.session_state.messages:
        if msg['role'] == 'user':
            st.markdown(f"**You:** {msg['content']}")
        else:
            st.markdown(f"**Assistant:** {msg['content']}")


