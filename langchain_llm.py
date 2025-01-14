import os
import warnings
from datetime import datetime
import pandas as pd
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain_community.callbacks.manager import get_openai_callback
from send_email import send_email
import logging
from questions import rand_choose

warnings.filterwarnings("ignore")


os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY")

query = """
Please process and present the content in data.txt to improve its readability and fix formatting issues for both the logic and statistics questions and answers. Present the information in clear and professional plain text, avoiding the use of LaTeX or any overly complex notation. Simplify any mathematical expressions into easily understandable text-based representations (e.g., write fractions as 'x/y' and break down summations into plain-text steps).

Requirements:

1) Question Clarity: Rewrite each question in a professional and structured format while maintaining its original meaning and intent.
2) Original Answer Preservation: Rewrite the original answers for better readability without altering their meaning or technical accuracy. Use concise and professional language.
3) Improved Solutions: For each question, add an improved solution immediately after the original answer. The improved solution should:
    - Clarify and simplify the explanation.
    - Use structured formatting (e.g., bulleted or numbered steps where necessary).
    - Provide additional context or insight where helpful.

4) Structure:
    - Question Number: Clearly state the question number and present the question.
    - Original Answer Number: Clearly indicate and present the original answer.
    - Improved Solution: Provide an enhanced, clarified version of the solution immediately after the original answer.
"""
rand_choose()

loader = TextLoader("C:\\Users\\tee_m\\Desktop\\gpt\\data.txt", encoding="ISO-8859-1")
embedding_model = OpenAIEmbeddings()
index_creator = VectorstoreIndexCreator(embedding=embedding_model)
index = index_creator.from_loaders([loader])
llm=ChatOpenAI(model="gpt-4o", temperature=0)

# Configure logging
logging.basicConfig(
    filename="C:\\Users\\tee_m\\Desktop\\gpt\\script.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("Script started.")

try:
    with get_openai_callback() as callback:
        # Query the index
        response = index.query(question=query, llm=llm)
        logging.info("LLM response: %s", response)
        
        # Print the response
        print("Response:", response)

        # Collect token usage data
        prompt_tokens = callback.prompt_tokens
        completion_tokens = callback.completion_tokens
        total_tokens = callback.total_tokens
        total_cost = callback.total_cost
            
        # Display the DataFrame
        print("\nToken Usage Data:")
        print(f"Prompt Tokens: {callback.prompt_tokens}")
        print(f"Completion Tokens: {callback.completion_tokens}")
        print(f"Total Tokens: {callback.total_tokens}")
        print(f"Total Cost (USD): ${callback.total_cost:.6f}")
        
        # Create a DataFrame to store the data
        new_data = pd.DataFrame([{
            "Date": datetime.now(),
            "Query": query,
            "Response": response,
            "Prompt Tokens": prompt_tokens,
            "Completion Tokens": completion_tokens,
            "Total Tokens": total_tokens,
            "Total Cost (USD)": f"${total_cost:.6f}"
        }])
        
        input = pd.read_csv("C:\\Users\\tee_m\\Desktop\\gpt\\generated_qns.csv")
        input.to_csv("C:\\Users\\tee_m\\Desktop\\gpt\\generated_qns_backup.csv", index=False)
        output = pd.concat([input, new_data],ignore_index=True)
        output.to_csv("C:\\Users\\tee_m\\Desktop\\gpt\\generated_qns.csv", index=False)
        
        send_email(query, response, prompt_tokens, completion_tokens, total_tokens, total_cost)

except Exception as e:
    logging.error("Error occurred: %s", str(e))
    
