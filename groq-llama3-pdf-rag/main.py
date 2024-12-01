from util import *
from streamlit_option_menu import option_menu
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Doc Chat", page_icon=":robot_face:", layout="centered")

# --- LOAD ENV VARIABLES ---
load_dotenv()

# --- SESSION STATE VARIABLES ---
for key, default in {
    "vector_store": False,
    "response": None,
    "prompt_activation": False,
    "conversation": None,
    "chat_history": None,
    "prompt": False,
    "messages": [{"role": "assistant", "content": "How can I help you?"}],
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# --- SIDEBAR CONFIGURATION ---
st.sidebar.header("Configuration")
groq_api_key = sidebar_api_key_configuration()
model = sidebar_groq_model_selection()

# --- MAIN PAGE CONFIGURATION ---
st.title("Doc Chat :robot_face:")
st.write("*Interrogate Documents :books:, Ignite Insights: AI at Your Service*")
st.write(":blue[***Powered by Groq AI Inference Technology***]")

# ---- NAVIGATION MENU -----
selected = option_menu(
    menu_title=None,
    options=["Doc Chat", "Reference", "About"],
    icons=["robot", "bi-file-text-fill", "app"],  # https://icons.getbootstrap.com
    orientation="horizontal",
)

# --- LLM and Prompt Setup ---
llm = ChatGroq(groq_api_key=groq_api_key, model_name=model)
prompt_template = ChatPromptTemplate.from_template(
    """
    Answer the question based on the provided context only. If question is not within the context, do not try to answer
    and respond that "Sorry, I didn’t understand your question. Do you want to connect with a live agent?".
    Please provide the most accurate response based on the question.
    <context>
    {context}
    Questions: {input}
    """
)

# ----- SETUP "Doc Chat" MENU ------
if selected == "Doc Chat":
    st.subheader("Upload PDF(s)")
    pdf_docs = st.file_uploader("Upload your PDFs", type=['pdf'], accept_multiple_files=True)

    # Process Button
    if st.button("Process", type="primary", disabled=not pdf_docs):
        with st.spinner("Processing..."):
            try:
                print(pdf_docs)
                print("here0")
                st.session_state.vector_store = create_vectorstore(pdf_docs)
                print("here1")
                st.session_state.prompt = True
                print("here2")
                st.success("Database is ready!")
                print("here3")
            except Exception as e:
                st.error(f"Failed to process PDFs: {e}")

    st.divider()

    # Chat Interface
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    question = st.chat_input(
        placeholder="Enter your question related to uploaded document",
        disabled=not st.session_state.prompt,
    )

    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        st.chat_message("user").write(question)

        with st.spinner("Processing..."):
            try:
                response = get_llm_response(llm, prompt_template, question)
                st.session_state.response = response
                answer = response.get("answer", "No answer provided.")
                st.session_state.messages.append({"role": "assistant", "content": answer})
                st.chat_message("assistant").write(answer)
            except Exception as e:
                st.error(f"Failed to get response: {e}")

# ----- SETUP "Reference" MENU -----
if selected == "Reference":
    st.title("Reference & Context")
    if st.session_state.response and "context" in st.session_state.response:
        for i, doc in enumerate(st.session_state.response["context"]):
            with st.expander(f"Reference #{i + 1}"):
                st.write(doc.page_content)
    else:
        st.info("No references available. Upload documents and ask a question first.")

# ----- SETUP "About" MENU -----
if selected == "About":
    with st.expander("About this App"):
        st.markdown("""
            This app allows you to chat with your PDF documents. It has the following features:
            - Chat with multiple PDF documents.
            - Powered by Groq AI inference technology.
            - Displays response context and document reference.
        """)
    with st.expander("Supported LLMs"):
        st.markdown("""
            This app supports the following LLMs as supported by Groq:
            - Llama3-8b-8192
            - Llama3-70b-8192
            - Mixtral-8x7b-32768
            - Gemma-7b-it
        """)
    with st.expander("Vectorstore Library"):
        st.markdown("This app uses FAISS for AI similarity search and vector storage.")
    with st.expander("Contact"):
        st.markdown("Contact [Jagdish](mailto:jagdishkumar.kar.min21@itbhu.ac.in) for support.")

