import React, { useState } from "react";
import axios from "axios";

const App = () => {
  const [pdfFile, setPdfFile] = useState(null);
  const [pdfName, setPdfName] = useState("");
  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState("");

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    setPdfName(file.name);
    const formData = new FormData();
    formData.append("pdf", file);

    try {
      const res = await axios.post("http://localhost:5000/upload-pdf", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      if (res.data.success) {
        alert("PDF uploaded and processed successfully!");
      } else {
        alert("Failed to process PDF.");
      }
    } catch (error) {
      console.error("Error uploading PDF:", error);
    }
  };

  const handleAskQuestion = async () => {
    try {
      const res = await axios.post("http://localhost:5000/ask", { question, pdfName });
      setResponse(res.data.answer);
    } catch (error) {
      console.error("Error asking question:", error);
      setResponse("Error connecting to server.");
    }
  };

  return (
    <div className="container">
      <h1 className="header">AI Chatbot</h1>
      <div className="upload-section">
        <label className="upload-label">Upload PDF:</label>
        <input 
          type="file" 
          accept="application/pdf" 
          onChange={handleFileUpload} 
          className="file-input"
        />
      </div>

      <div className="question-section">
        <label className="question-label">Ask a question:</label>
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          className="question-input"
          placeholder="Enter your question"
        />
        <button onClick={handleAskQuestion} className="ask-btn">Ask</button>
      </div>

      {response && (
        <div className="response-box">
          <strong>Response:</strong> {response}
        </div>
      )}
    </div>
  );
};

export default App;
