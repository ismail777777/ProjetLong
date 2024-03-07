#https://u3sswjvurlqjnc9g5fwzy5.streamlit.app/
import streamlit as st
import requests
from streamlit_lottie import st_lottie
import pickle
from pathlib import Path
import hashlib
import time
import torch
# DB Management
import psycopg2
conn = psycopg2.connect(
        dbname="wxcqkqvn",
        user="wxcqkqvn",
        password="1MmU3atbUECYw4sp3Aq21Xu417JJN9HU",
        host="flora.db.elephantsql.com"
    )
c = conn.cursor()
def create_usertable():
    c.execute('''CREATE TABLE IF NOT EXISTS utilisateurs
               (id SERIAL PRIMARY KEY,
               nom VARCHAR(255) NOT NULL,
               email VARCHAR(255) UNIQUE NOT NULL,
               mot_de_passe VARCHAR(255) NOT NULL)''')

def add_userdata(nom,email,password):
   c.execute("INSERT INTO utilisateurs (nom, email, mot_de_passe) VALUES (%s, %s, %s)", (nom, email,password))
   conn.commit()

def login_user(nom,email,password):
   c.execute("SELECT * FROM utilisateurs WHERE nom=%s  AND email=%s AND mot_de_passe=%s", (nom,email,password))
   data = c.fetchall()
   return data
def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def login():
    create_usertable()
    hashed_pswd = make_hashes(password)

    if login_user(username,email,check_hashes(password,hashed_pswd)):
        
        x=st.success("Login successful")
        x.empty()
        st.markdown("""<h1 style='text-align: center; color: #f63366;'>Chatbot for C code generation</h1>""", unsafe_allow_html=True)
        lottie_coding1 = load_lottieurl("https://lottie.host/d86275a4-8cc5-4463-a8d1-03071f02f7ee/UnwrqECWFD.json")
        lottie_coding2=load_lottieurl("https://lottie.host/f408e134-0f03-454c-9468-0dcb1b64a8a1/X0EptyFKmn.json")
        lottie_coding3=load_lottieurl("https://lottie.host/62c6ff04-774a-4817-8320-3887ca6b0b09/3HrubUT7AR.json")
        col1,col2,col3=st.columns(3)
        with col1:
            st_lottie(lottie_coding2,height=250,key="co")
        with col2:
            st_lottie(lottie_coding1, height=250, key="coding")
        with col3:
            st_lottie(lottie_coding3,height=250,key="c")



        with st.sidebar:
            # Create a sidebar
            st.title('Hello  '+username)
            st.write("---")
            st.sidebar.header("Send your feedback ! ")
            st.sidebar.write("##")

            contact_form = """
            <form action="https://formsubmit.co/zakarialahmouz@gmail.com" method="POST">
                <input type="hidden" name="_captcha" value="false">
                <input type="text" name="name" placeholder="Your name" required>
                <input type="email" name="email" placeholder="Your email" required>
                <textarea name="message" placeholder="Your message here" required></textarea>
                <button type="submit">Send</button>
            </form>
            """
            st.markdown(contact_form, unsafe_allow_html=True)
            local_css("/content/style.css")
            #local_css("style.css")
            # Add logout button to the sidebar
            
                #st.warning("You have logged out.")
                # Add logout logic here (e.g., redirect to login page, clear session data, etc.)
            #authenticator.logout("Logout","sidebar")
        from transformers import AutoModelForCausalLM
        from peft import PeftModel
        import torch


        # Specify the path where your model is saved
        model_path = "/content/drive/MyDrive/ProjetLong/model-5-epochs"
        # /content/drive/MyDrive/ProjetLong/Codes/model-5-epochs

        # Reload the model from the specified path
        # new_model = AutoModelForCausalLM.from_pretrained(model_path)

        model_name = "NousResearch/Llama-2-7b-chat-hf"
        base_model = AutoModelForCausalLM.from_pretrained(
            model_name,
            low_cpu_mem_usage=True,
            return_dict=True,
            torch_dtype=torch.float16,
            device_map={"": 0}#device_map,
        )
        model = PeftModel.from_pretrained(base_model, model_path)
        model = model.merge_and_unload()
        from transformers import logging, pipeline, AutoTokenizer
        logging.set_verbosity(logging.CRITICAL)
        tokenizer = AutoTokenizer.from_pretrained("NousResearch/Llama-2-7b-chat-hf", trust_remote_code=True, use_fast=False)
        tokenizer.pad_token = tokenizer.eos_token
        tokenizer.padding_side = "right"
                  


        # Store LLM generated responses
        if "messages" not in st.session_state.keys():
            st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

        # Display or clear chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        def clear_chat_history():
            st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
        st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

        # Function for generating LLaMA2 response
        def generate_llama2_response(prompt):
            pipe = pipeline(task="text-generation", model=model, tokenizer=tokenizer, max_length=1000)
            result = pipe(f"<s>[INST] {prompt} [/INST]")
            return result[0]['generated_text'].replace('\\n', '\n')

        # User-provided prompt
        if prompt := st.chat_input():
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)

        # Generate a new response if last message is not from assistant
        if st.session_state.messages[-1]["role"] != "assistant":
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = generate_llama2_response(prompt)
                    placeholder = st.empty()
                    full_response = ''
                    for item in response:
                        full_response += item
                        placeholder.markdown(full_response)
                    placeholder.markdown(full_response)
            message = {"role": "assistant", "content": full_response}
            st.session_state.messages.append(message)
    else:
      st.error("Error username/password")
# Use local CSS
def local_css(file_name):
    with open(file_name) as f:
       st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


##User authentification
st.set_page_config(page_title="ProjetLong", page_icon=":tada:", layout="wide")
choice = st.sidebar.radio("Navigation", ["Login", "Signup"])
if choice=="Login":
  username=st.sidebar.text_input("username")
  email=st.sidebar.text_input("email")
  password=st.sidebar.text_input("password",type="password")
  if st.sidebar.checkbox("Login"):
      login()

if choice=="Signup":
   new_user=st.sidebar.text_input("username")
   new_email=st.sidebar.text_input("email")
   new_password=st.sidebar.text_input("password",type="password")
   if st.sidebar.button("Signup"):
      create_usertable()
      add_userdata(new_user,new_email,make_hashes(new_password))
      st.success("You have successfully created an account.Go to the Login Menu to login")




      