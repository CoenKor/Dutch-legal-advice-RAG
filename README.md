# Thesis Project: Integrating RAG Models in the Dutch Legal System

Welcome to the GitHub page for the thesis of Coen Korevaar (13441728). This project focuses on creating a Retrieval-Augmented Generation (RAG) model to answer the following question: 

**To what extent can a Retrieval-Augmented Generation (RAG) model be integrated in the creation of verdicts in the Dutch legal system?**

The dataset used for this project is `parsed_data.csv`.

## Setting Up the Model

To set up the model, follow these steps:

1. **Install Dependencies**:
   - Install the required libraries listed in `requirements.txt`:
     ```bash
     pip install -r requirements.txt
     ```

2. **Generate Embeddings**:
   - Use the `Embedding.ipynb` notebook to generate embeddings for every indictment in the dataset. This is necessary for realizing the vector search capability in Neo4J.
   - The embeddings are generated using OpenAI's `text-embedding-3-small` model.
   - The resulting CSV from the notebook should be integrated into the Neo4J database and added as a new value to all the indictment nodes in the graph.

3. **Run the Application**:
   - Start the application using the `streamlit run` command:
     ```bash
     streamlit run bot.py
     ```
   - The app will be available at [http://localhost:8501/](http://localhost:8501/).

## Results

The results of this project are organized into several folders:

1. **RAG-model-Quality**:
   - Contains the input and output prompts of the model.
   - Includes prompts for similar cases (cases that are similar to those in the Neo4J database) and non-similar cases (cases that are not similar to those in the Neo4J database).

    **End Results**:
      - An Excel file comparing the verdicts created by the RAG model to the actual verdicts from `rechtspraak.nl`.

3. **Robustness**:
   - Contains 50 outputs of the model from the same case description to test robustness.
   - The code used for the calculation of robustness results can be found in `Robustness.ipynb` in the same folder.

## Running the Application

To run the application, you must install the libraries listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

Then, start the app using the following command:

```bash
streamlit run bot.py
```

The application will be available at [http://localhost:8501/](http://localhost:8501/).