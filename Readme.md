# **Documentation for AI Chatbot "DOC chat" with PDF Knowledge Base**

## **Overview**

This application is designed to interact with users and answer questions based on the content of uploaded PDF documents. The chatbot is equipped with fallback logic to handle out-of-context questions gracefully. The application leverages Groq AI inference technology, FAISS for similarity search, and a user-friendly interface created with Streamlit.

---

## **Key Features**
1. **PDF Knowledge Base**:
   - Users can upload multiple PDFs to serve as the chatbot's knowledge base.
   - The application processes the PDFs to extract content and create a vector database for efficient querying.

2. **Intelligent Question Answering**:
   - Answers user queries based on the PDF content.
   - Utilizes Groq AI models for generating responses.

3. **Fallback Handling**:
   - When a question is out of context or unrelated to the PDF content, the chatbot responds:
     *“Sorry, I didn’t understand your question. Do you want to connect with a live agent?”*

4. **Interactive Interface**:
   - Provides a seamless, text-based chat interface.
   - Allows users to upload PDFs, ask questions, and view answers.

5. **Reference Context**:
   - Displays the source of information for each response when available.

---

## **Architecture and Workflow**

### 1. **PDF Upload and Processing**
   - **Step**: Users upload one or more PDFs via the interface.
   - **Action**: The uploaded PDFs are processed using FAISS to create a vector database for fast similarity-based search.

### 2. **Chat Interface**
   - **Step**: Users ask questions through the chat input.
   - **Action**:
     - The question is processed against the vector database.
     - Relevant context is retrieved and passed to the LLM via a prompt template.
     - The LLM generates a response based on the context.

### 3. **Fallback Mechanism**
   - **Step**: If no relevant context is retrieved or the question is unrelated, the chatbot generates a fallback response.

### 4. **Reference Display**
   - **Step**: Users can view the references for responses.
   - **Action**: Contextual excerpts from the PDFs are displayed for transparency.

---

## **Tools and Libraries Used**

1. **Streamlit**: 
   - Used for building the user interface.
   - Provides features like file upload, chat interface, and navigation menus.

2. **Groq AI**:
   - Powers the chatbot's inference capabilities.
   - Supports various advanced LLMs such as Llama3-8b-8192 and Mixtral-8x7b-32768.

3. **FAISS**:
   - Handles vector storage and similarity search for efficient information retrieval.

4. **LangChain**:
   - Utilized for prompt management and integration with Groq AI.

5. **Python**:
   - Core programming language used to implement the solution.

---

## **Implementation Details**

### 1. **File Upload and Processing**
- **Code**:
```python
st.subheader("Upload PDF(s)")
pdf_docs = st.file_uploader("Upload your PDFs", type=['pdf'], accept_multiple_files=True)

if st.button("Process", type="primary", disabled=not pdf_docs):
    with st.spinner("Processing..."):
        try:
            st.session_state.vector_store = create_vectorstore(pdf_docs)
            st.session_state.prompt = True
            st.success("Database is ready!")
        except Exception as e:
            st.error(f"Failed to process PDFs: {e}")
```

- **Explanation**:
  - PDFs are uploaded and processed into a vector database using the `create_vectorstore` function.
  - The application indicates success or failure during processing.

---

### 2. **Chat Functionality**
- **Code**:
```python
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
            answer = response.get("answer", "No answer provided.")
            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.chat_message("assistant").write(answer)
        except Exception as e:
            st.error(f"Failed to get response: {e}")
```

- **Explanation**:
  - User input is processed to retrieve context and generate an answer.
  - Responses are displayed in the chat interface.

---

### 3. **Fallback Logic**
- **Code**:
```python
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
```

- **Explanation**:
  - The prompt ensures the chatbot only responds if the question is within the provided context.
  - If not, a fallback response is generated.

---

### 4. **References**
- **Code**:
```python
if st.session_state.response and "context" in st.session_state.response:
    for i, doc in enumerate(st.session_state.response["context"]):
        with st.expander(f"Reference #{i + 1}"):
            st.write(doc.page_content)
else:
    st.info("No references available. Upload documents and ask a question first.")
```

- **Explanation**:
  - References are extracted from the context and displayed in an expandable section.

---

## **Challenges and Solutions**

1. **Handling Large PDFs**:
   - **Challenge**: Processing large documents efficiently.
   - **Solution**: FAISS was used for similarity-based querying to speed up content retrieval.

2. **Ensuring Accurate Responses**:
   - **Challenge**: Preventing irrelevant answers.
   - **Solution**: Context-bound prompts were used to limit the chatbot's responses.

3. **User-Friendly Interface**:
   - **Challenge**: Designing an intuitive interface.
   - **Solution**: Streamlit was used to create a clear, interactive UI.

---

## **Instructions to Run the Application**

1. Install dependencies:
   ```bash
   pip install streamlit langchain groq-python faiss-cpu python-dotenv
   ```

2. Set up environment variables in a `.env` file:
   ```env
   GROQ_API_KEY=your_api_key
   ```
   
3. Set up environment variables in a `.env` file:
   ```env
   INFERENCE_API_KEY=your_api_key
   ```

4. Run the application:
   ```bash
   streamlit run app.py
   ```

5. Upload PDFs and start asking questions!

---

## **Future Improvements**

1. Add support for other document formats (e.g., Word, Excel).
2. Enhance accuracy by fine-tuning the prompt or model.
3. Implement a live agent connection for unresolved queries.
