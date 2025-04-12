import streamlit as st
from groq import Groq
from src.langchainAPI.newSing import ChatChainSingleton, GroqChainSingleton
import uuid
from langchain_openai import ChatOpenAI
import gc
from langchain_core.messages import HumanMessage, SystemMessage
#works for both openai and groq correctly now
#1)!!!SOLVED!!! the case that user enters an invalid api key (create some checker before attempting chain I guess) also figure out scenarios where users switches between the apis, currently if wrong api key is entered into openai causes issue (since chain is initialized already? create method maybe to reinitialize in case or research more how to reset a singleton)
#2)!!!STILL NEED TO BEGIN!!! begin considering implementation of "New Conversation", see how we plan to implement uploading the session state to our current database
#3)!!!SOLVED!!!Research to see how to keep the conversation from dissappearing every time new response is being generated (just looks ugly)
#4)!!!STILL DOESNT CLEAR BUT DOESNT HIDE ITSELF ANYMORE!!!  make user input box actually clear itself ( currently doesnt and also the issue where if you clear it and then click on the page the conversation dissapears until next submission)
#5)!!!SINGLETON IMPLEMENTED FOR GROQ, STILL NEED TO ADD EXTRA EXAMPLES FOR GUIDELINE PROMPTS!!! actually implement same singleton for groq (Are we going to widen the examples we are feeding this thing? Currently is set up with focusing on computer science but we wanted to widen scope, add new examples or reword final promp to just be more encompassing?)
#Note: maybe once user enters correct api key and begins conversation , store that conversation separately, make some button that allows them to switch to other service, store each conversation separately and combine them together in a third so they can later view the entire convo with both)
#Probably doesn't matter but, if you just ran openAI and entered api key, if you ask it what was the first message you asked as your first submission it replies one of the examples from the singleton class, not sure if this matters


def format_message(messages):
    formatted = []
    for msg in messages:
        if not isinstance(msg, dict):
            #case that msg is not a dict
            continue
        #check 'role' and 'content' keys are present
        role = msg.get("role", "unknown")
        content = msg.get("content", "[No content available]")
        formatted.append({"role": role, "content": content})
    return formatted

#this function runs a mini-query to validate that the provided API key
def openAi_key_check(key):
    try:
        messages = [SystemMessage(content="You only reply 'Yes'."),HumanMessage(content="Yes?"),]
        test = ChatOpenAI(model="gpt-4o-mini", temperature=0.0, api_key=key)
        response =test.invoke(messages)
        del response
        del test
        del messages
        gc.collect()
        return True
    except Exception as e:
        return False
    
#this function runs a mini-query to validate that the provided API key
def groq_key_check (key):
    try:
        client = Groq(api_key=key,)
        chat_completion = client.chat.completions.create(messages=[{"role": "user","content": "Explain the importance of fast language models",}], model="llama3-8b-8192",)
        response = chat_completion.choices[0].message.content
        del client
        del chat_completion
        del response
        gc.collect()
        return True
    except Exception as e:
        return False
    
    

st.title("StarsGPT")
api_choice = st.sidebar.selectbox("Select API Provider", ["Groq", "OpenAI"])

#to store conversation before later saving to database to create "conversation" log as well as setting up session state variables for validating logic and simpler swapping between the two
if "openaiConvo" not in st.session_state:
    st.session_state.openaiConvo = []
if "groqConvo" not in st.session_state:
    st.session_state.groqConvo = []
if "groqEnteredKey" not in st.session_state:
    st.session_state.groqEnteredKey = None
if "openAIEnteredKey" not in st.session_state:
    st.session_state.openAIEnteredKey = None
if "groqValidated" not in st.session_state:
    st.session_state.groqValidated = False
if "openValidated" not in st.session_state:
    st.session_state.openValidated = False


    
#format messages correctly
st.session_state.openaiConvo = format_message(st.session_state.openaiConvo)
st.session_state.groqConvo = format_message(st.session_state.groqConvo)

#API key/chat chain initialization
if api_choice == "Groq":
    groqApi = st.sidebar.text_input("Groq API Key", type="password", value=st.session_state.groqEnteredKey or "")
    
    if groqApi and not st.session_state.groqValidated:
        if groq_key_check(groqApi):
            st.session_state.groqValidated = True
            st.session_state.groqEnteredKey = groqApi
            GroqChainSingleton.model = "llama3-8b-8192"
            GroqChainSingleton.input_api_key = groqApi
            st.session_state.groqChat = GroqChainSingleton().chain
        else:
            st.session_state.groqValidated = False
            st.warning("Invalid Groq API key. Please enter a valid key!")
            
elif api_choice == "OpenAI":
    openaiApi = st.sidebar.text_input("OpenAI API Key", type="password", value=st.session_state.openAIEnteredKey or "")
    
    if openaiApi and not st.session_state.openValidated:
        if openAi_key_check(openaiApi):
            st.session_state.openValidated = True
            st.session_state.openAIEnteredKey = openaiApi
            ChatChainSingleton.model = "gpt-4o-mini"
            ChatChainSingleton.input_api_key = openaiApi
            st.session_state.chat = ChatChainSingleton().chain
        else:
            st.session_state.openValidated = False
            st.warning("Invalid OpenAI API key. Please enter a valid key!")
            
    #create container to display conversation
message_container = st.container()
user_input = st.text_area("Please enter your message below:", "")
if st.button("Submit"):
    with st.spinner("Generating response..."):
        if api_choice == "OpenAI" and st.session_state.openValidated:
            #OpenAI scenario
            #just adding user input to respective conversation and storing assistant output as well
            st.session_state.openaiConvo.append({"role": "user", "content": user_input})
            history = [{"role": msg["role"], "content": msg["content"]} for msg in st.session_state.openaiConvo[:-1]]
            session_id = str(uuid.uuid4())
            response = st.session_state.chat.invoke({"input": user_input, "history": history}, {"configurable": {"session_id": session_id}})
            st.session_state.openaiConvo.append({"role": "assistant", "content": response.content})
                    
        elif api_choice == "Groq" and st.session_state.groqValidated:
            #Groq scenario
            #just adding user input to respective conversation and storing assistant output as well
            st.session_state.groqConvo.append({"role": "user", "content": user_input})
            history2 = [{"role": msg["role"], "content": msg["content"]} for msg in st.session_state.groqConvo[:-1]]
            groqSessionId = str(uuid.uuid4())
            response = st.session_state.groqChat.invoke({"input": user_input, "history": history2})
            st.session_state.groqConvo.append({"role": "assistant", "content": response.content})

                #!!!SOLVED!!!currently shows all messages, maybe set up separate ones for each scenario to keep separate (maybe set up separate for instance but keep and upload into database to mix both convos??)
        with message_container:
                    if api_choice =="OpenAI":
                        displayed_chat = st.session_state.openaiConvo 
                        for msg in displayed_chat:
                            st.markdown(f"**{msg['role'].capitalize()}:** {msg['content']}")
                    elif api_choice =="Groq":
                        displayed_chat = st.session_state.groqConvo
                        for msg in displayed_chat:
                            st.markdown(f"**{msg['role'].capitalize()}:** {msg['content']}")

if api_choice == "Groq" and not groqApi:
        st.warning("Please enter a your Groq API key.")
elif api_choice == "OpenAI" and not openaiApi:
        st.warning("Please enter your OpenAI API key.")

