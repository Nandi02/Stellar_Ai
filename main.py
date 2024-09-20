import os

from PIL import Image
import streamlit as st
from streamlit_option_menu import option_menu
import firebase_admin
from firebase_admin import credentials, auth
from gemini_utility import (load_gemini_pro_model,
                            gemini_pro_response,
                            gemini_pro_vision_response,
                            embeddings_model_response)


working_dir = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(
    page_title="Stellar AI",
    page_icon="🧠",
    layout="centered",
)

with st.sidebar:
    selected = option_menu('Stellar AI',
                           ['Account',
                            'ChatBot',
                            'Image Captioning',
                            'Embed text',
                            'Ask me anything'],
                           menu_icon='robot', icons=['textarea-t','chat-dots-fill', 'image-fill',  'patch-question-fill'],
                           default_index=0
                           )


# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

#cred = credentials.Certificate("gemini-f7036-140d83e5d286.json")
#firebase_admin.initialize_app(cred)

    
#Create your account
def app():
    
    if 'username' not in st.session_state:
        st.session_state.username = ' '
    if 'useremail' not in st.session_state:
        st.session_state.useremail = ' '
        
    def authenticate():
        try:
            user = auth.get_user_by_email(email)
            #print(user.uid)
            st.success('Login Successfully') 
            st.session_state.username = user.uid
            st.session_state.useremail = user.email
            st.session_state.signout = True
            st.session_state.signedout = True 
        except:
            st.warning('Login Failed') 
            
            
    def logout():
        st.session_state.signedout = False
        st.session_state.signout = False
        st.session_state.username = '' 
                  
         
    if 'signedout' not in st.session_state:
        st.session_state.signedout = False
    if 'signout' not in st.session_state:
        st.session_state.signout = False
        
        
    if not st.session_state['signedout']:
         st.title("Create a Account")
         Choice = st.selectbox('Login\Signup',['Login','Sign Up'])       
         
             
         
         if Choice == 'Login':
             email = st.text_input('Email Address')
             password = st.text_input('Password', type='password')
             st.button('Login',on_click=authenticate)
         else:
             email = st.text_input('Email Address')
             password = st.text_input('Password', type='password')
             username = st.text_input('User Name')
             if st.button('Sign Up'):
                 user = auth.create_user(email = email, password = password, uid = username ) 
                 st.success('Account Created Successfully')
                 st.markdown('Please Login using your email and password')
                 st.balloons()
            
    
    
    if st.session_state.signout:
        st.title('Welcom To :violrt[Stellar LLM Model] 🤖')
        st.text('Name : '+st.session_state.username)
        st.text('Email : '+st.session_state.useremail)
        st.button('Sign Out', on_click=logout)   


if selected == 'Account':
    app()
           



# chatbot page
if selected == 'ChatBot':
    model = load_gemini_pro_model()

    # Initialize chat session in Streamlit if not already present
    if "chat_session" not in st.session_state:  # Renamed for clarity
        st.session_state.chat_session = model.start_chat(history=[])

    # Display the chatbot's title on the page
    st.title("🤖 ChatBot")

    # Display the chat history
    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)

    # Input field for user's message
    user_prompt = st.chat_input("Ask Stellar-Pro... ")  # Renamed for clarity
    if user_prompt:
        # Add user's message to chat and display it
        st.chat_message("user").markdown(user_prompt)

        # Send user's message to Gemini-Pro and get the response
        gemini_response = st.session_state.chat_session.send_message(user_prompt)  # Renamed for clarity

        # Display Gemini-Pro's response
        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)


# Image captioning page
if selected == "Image Captioning":

    st.title("📷 Snap Narrate")

    uploaded_image = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])

    if st.button("Generate Caption"):
        image = Image.open(uploaded_image)

        col1, col2 = st.columns(2)

        with col1:
            resized_img = image.resize((800, 500))
            st.image(resized_img)

        default_prompt = "write a short caption for this image"  # change this prompt as per your requirement

        # get the caption of the image from the gemini-pro-vision LLM
        caption = gemini_pro_vision_response(default_prompt, image)

        with col2:
            st.info(caption)


# text embedding model
if selected == "Embed text":

    st.title("🔡 Embed Text")

    # text box to enter prompt
    user_prompt = st.text_area(label='', placeholder="Enter the text to get embeddings")

    if st.button("Get Response"):
        response = embeddings_model_response(user_prompt)
        st.markdown(response)


# text embedding model
if selected == "Ask me anything":

    st.title("❓ Ask me a question")

    # text box to enter prompt
    user_prompt = st.text_area(label='', placeholder="Ask me anything...")

    if st.button("Get Response"):
        response = gemini_pro_response(user_prompt)
        st.markdown(response)
