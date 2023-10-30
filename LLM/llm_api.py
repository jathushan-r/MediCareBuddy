# uvicorn llm_api:app --host 0.0.0.0 --port 8000

from fastapi import FastAPI, Request
from pydantic import BaseModel
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from langchain.chains.conversation.memory import ConversationBufferMemory
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
# os.environ["REPLICATE_API_TOKEN"] = "dwejfwe"

# llm = Replicate(
#     model="replicate/llama-2-70b-chat:2796ee9483c3fd7aa2e171d38f4ca12251a30609463dcfd4cd76703f22e96cdf",
#     input={"temperature": 0.7, "max_length": 150, "top_p": 1},
# )

chat_model = MyGPT4ALL(
    model_folder_path=r'.\src\models',
    model_name='llama-2-7b-chat.ggmlv3.q4_0.bin',
    allow_download=False,
    allow_streaming=True,
)

kb = MyKnowledgeBase(
    pdf_source_folder_path=DOCUMENT_SOURCE_DIRECTORY,vector_db= 'vect'
)

kb.initiate_document_injetion_pipeline()


# get the retriver object from the vector db 

retriever = kb.return_retriever_from_persistant_vector_db()

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

custom_prompt_template = """
I want you to act as a hospital chatbot.  "{query}."
"""



CUSTOM_QUESTION_PROMPT = PromptTemplate(input_variables = ['query'], template=custom_prompt_template)



qa_chain = ConversationalRetrievalChain.from_llm(
llm = chat_model,
chain_type='stuff',
retriever=retriever,
return_source_documents=False, 
return_generated_question = False,
verbose=True,
memory = memory
)
vectdb = kb.get_vector_db()
chat_history = []

# Implement your conversation logic
@app.post("/chat")
async def chat_with_bot(request: Request, chat_request: ChatRequest):
    query = chat_request.query
    if query == 'exit':
        return {"answer": "Goodbye!"}

    result = qa_chain({"question": CUSTOM_QUESTION_PROMPT.format(query=query), "chat_history": chat_history})
    chat_history.extend([(query, result["answer"])])
    return ChatResponse(answer=result["answer"])

@app.get("/chat-history")
async def get_chat_history():
    return chat_history

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
