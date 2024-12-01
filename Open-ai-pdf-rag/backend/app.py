import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from llama_index.llms.openai import OpenAI
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

# Load environment variables
load_dotenv()

# Flask app setup
app = Flask(__name__)
CORS(app)

# Store indexes in memory (keyed by PDF name)
indexes = {}

# Set OpenAI API Key
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


def extract_content_from_pdf(pdf_path):
    # Load the documents from the given path
    documents = SimpleDirectoryReader(pdf_path).load_data()
    
    # Create an index from the documents
    index = VectorStoreIndex(documents)
    
    # Create a query engine from the index
    query_engine = index.as_query_engine()
    
    # Query the index for the summary of the paper
    response = query_engine.query("What is the summary of paper?")
    return response


@app.route('/upload-pdf', methods=['POST'])
def upload_pdf():
    try:
        print("Uploading PDF...")
        print(request.files)
        # Ensure a file is uploaded
        if 'pdf' not in request.files:
            return jsonify({'success': False, 'message': 'No PDF file provided.'}), 400

        pdf_file = request.files['pdf']
        pdf_name = pdf_file.filename

        # Save PDF temporarily
        temp_dir = "./temp"
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        temp_pdf_path = os.path.join(temp_dir, pdf_name)
        pdf_file.save(temp_pdf_path)

        # Read and process the PDF content
        summary = extract_content_from_pdf(temp_dir)

        # Store the index in memory (keyed by PDF name)
        indexes[pdf_name] = summary

        # Clean up the temporary PDF file
        os.remove(temp_pdf_path)

        return jsonify({'success': True, 'message': 'PDF processed successfully', 'pdfName': pdf_name, 'summary': summary}), 200

    except Exception as e:
        print(f"Error processing PDF: {e}")
        return jsonify({'success': False, 'message': 'Error processing PDF.', 'error': str(e)}), 500


@app.route('/ask', methods=['POST'])
def ask_question():
    try:
        # Get question and PDF name from the request
        data = request.json
        question = data.get('question')
        pdf_name = data.get('pdfName')

        if not question or not pdf_name:
            return jsonify({'success': False, 'message': 'Missing question or pdfName.'}), 400

        # Check if the index exists
        if pdf_name not in indexes:
            return jsonify({'success': False, 'message': 'PDF not found.'}), 404

        # Fetch the summary from the stored index
        summary = indexes[pdf_name]

        # Return the response or fallback message
        if summary:
            return jsonify({'success': True, 'answer': summary}), 200
        else:
            return jsonify({'success': False, 'answer': 'Sorry, I didn’t understand your question. Do you want to connect with a live agent?'}), 200

    except Exception as e:
        print(f"Error answering question: {e}")
        return jsonify({'success': False, 'message': 'Error answering question.', 'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
