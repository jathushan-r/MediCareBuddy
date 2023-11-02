# uvicorn llm_api:app --host 0.0.0.0 --port 8000

from langchain.llms import OpenAI
from fastapi import FastAPI, Request
from pydantic import BaseModel
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import Replicate
import os

# Import your custom modules
from src.models.gpt4all_model import MyGPT4ALL
from src.knowledge_base.knowledgebase import MyKnowledgeBase, DOCUMENT_SOURCE_DIRECTORY

app = FastAPI()

# Define request and response models
class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    answer: str

# Initialize your components here
# os.environ["OPENAI_API_KEY"] = 'sk-fdfd'
os.environ["REPLICATE_API_TOKEN"] = "r8_6rXolartKZeUccahg23a7e9rrUMMUyU241P5V"
llm = Replicate(
    model="meta/llama-2-13b-chat:f4e2de70d66816a838a89eeeb621910adffb0dd0baba3976c96980970978018d",
    input={"temperature": 0.7, "max_length": 100, "top_p": 1},
)

# chat_model = MyGPT4ALL(
#     model_folder_path=r'.\src\models',
#     model_name='llama-2-7b-chat.ggmlv3.q4_0.bin',
#     allow_download=False,
#     allow_streaming=True,
# )

kb = MyKnowledgeBase(
    pdf_source_folder_path=DOCUMENT_SOURCE_DIRECTORY,vector_db= 'vect'
)

kb.initiate_document_injetion_pipeline()


# get the retriver object from the vector db 

retriever = kb.return_retriever_from_persistant_vector_db()

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

custom_prompt_template = """
As a hospital customer care agent, I'm here to provide information about diseases, wellness tips, and answer general medical questions. try to answer shortly\n
visitor question is "{query}?"
"""



prompt_template = """Use the following pieces of context to answer the question.

{context}

Question: {question}
"""
PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)

chain_type_kwargs = {"prompt": PROMPT}

qa_chain = RetrievalQA.from_chain_type(
llm = llm,
chain_type='stuff',
retriever=retriever,
chain_type_kwargs=chain_type_kwargs,
verbose=True
)
vectdb = kb.get_vector_db()
chat_history = []

# Implement your conversation logic
@app.post("/chat")
async def chat_with_bot(request: Request, chat_request: ChatRequest):
    query = chat_request.query
    if query == 'exit':
        return {"answer": "Goodbye!"}

    result = qa_chain({"query": query})
    # chat_history.extend([(query, result["answer"])])
    return ChatResponse(answer=result["result"])

@app.get("/chat-history")
async def get_chat_history():
    return chat_history

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
