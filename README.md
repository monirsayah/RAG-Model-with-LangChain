# RAG Model with LangChain

A Retrieval-Augmented Generation (RAG) chatbot built with Streamlit that allows users to upload text documents and ask questions about their content. The application uses LangChain, ChromaDB, and Groq's language model to provide intelligent responses based on the uploaded documents.

## Features

- **Document Upload**: Support for multiple `.txt` files
- **Text Processing**: Automatic text chunking with overlap for better context retention
- **Vector Storage**: Uses ChromaDB with HuggingFace embeddings for efficient document retrieval
- **Smart Retrieval**: Retrieves top-k most relevant document chunks for each query
- **Interactive Chat**: Clean Streamlit interface with chat input and spinner feedback
- **Powered by Groq**: Uses Groq's `compound-beta-mini` model for fast inference

## Prerequisites

- Python 3.8+
- Groq API key

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd rag-chatbot
```

2. Install required dependencies:
```bash
pip install streamlit langchain-groq langchain-chroma langchain-huggingface langchain-community
```

3. Set up your Groq API key:
   - Get your API key from [Groq Console](https://console.groq.com/)
   - Replace `"YOUR_GROQ_API KEY"` in the code with your actual API key
   - Alternatively, set it as an environment variable:
   ```bash
   export GROQ_API_KEY="your_api_key_here"
   ```

## Usage

1. Run the Streamlit application:
```bash
streamlit run app.py
```

2. Open your browser and navigate to the provided local URL (typically `http://localhost:8501`)

3. Upload one or more `.txt` files using the file uploader

4. Once files are processed, use the chat input to ask questions about your documents

5. The chatbot will retrieve relevant information from your documents and provide contextual answers

## How It Works

### 1. Document Processing
- Uploaded text files are read and concatenated
- Text is split into chunks of 1000 characters with 250 character overlap using `RecursiveCharacterTextSplitter`

### 2. Vector Storage
- Document chunks are embedded using HuggingFace's `sentence-transformers/all-MiniLM-L6-v2` model
- Embeddings are stored in ChromaDB for efficient similarity search

### 3. Retrieval-Augmented Generation
- User queries are processed to find the top 3 most relevant document chunks
- Retrieved context is combined with the query and sent to Groq's language model
- The model generates responses based on the provided context

## Configuration

### Model Settings
- **LLM**: Groq's `compound-beta-mini` model
- **Temperature**: 0 (deterministic responses)
- **Embedding Model**: `sentence-transformers/all-MiniLM-L6-v2`
- **Chunk Size**: 1000 characters
- **Chunk Overlap**: 250 characters
- **Retrieval**: Top 3 relevant chunks

### Customization Options

You can modify these parameters in the code:

```python
# Text splitting
chunk_size=1000,
chunk_overlap=250,

# Retrieval
top_k = 3

# LLM settings
temperature=0
model="compound-beta-mini"
```

## File Structure

```
├── app.py                 # Main Streamlit application
├── README.md             # This file
└── requirements.txt      # Python dependencies (optional)
```

## Dependencies

- `streamlit` - Web application framework
- `langchain-groq` - Groq integration for LangChain
- `langchain-chroma` - ChromaDB integration
- `langchain-huggingface` - HuggingFace embeddings
- `langchain-community` - Community document loaders
- `langchain` - Core LangChain functionality

## Limitations

- Currently supports only `.txt` files
- Requires internet connection for Groq API and HuggingFace model downloads
- Vector store is not persisted between sessions (stored in memory only)
- No conversation history - each query is independent

## Troubleshooting

### Common Issues

1. **API Key Error**: Ensure your Groq API key is correctly set
2. **Empty Document Error**: Make sure uploaded files contain text content
3. **Model Loading**: First run may take time to download the embedding model
4. **Memory Issues**: Large documents may require chunking parameter adjustments

### Error Messages
- "Uploaded document(s) are empty" - Check that your text files contain content
- API connection errors - Verify your Groq API key and internet connection

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

- [LangChain](https://langchain.com/) for the RAG framework
- [Streamlit](https://streamlit.io/) for the web interface
- [Groq](https://groq.com/) for fast language model inference
- [HuggingFace](https://huggingface.co/) for embedding models
- [ChromaDB](https://www.trychroma.com/) for vector storage
