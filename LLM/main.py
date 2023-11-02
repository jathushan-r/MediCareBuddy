
from src.models.gpt4all_model import MyGPT4ALL
from src.knowledge_base.knowledgebase import MyKnowledgeBase
from src.knowledge_base.knowledgebase import (
    DOCUMENT_SOURCE_DIRECTORY
)
from langchain.chains import RetrievalQA
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate


from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.llms import Replicate
import os


def main():
   
    os.environ["REPLICATE_API_TOKEN"] = "r8_6rXolartKZeUccahg23a7e9rrUMMUyU241P5V"
    llm = Replicate(
    model="replicate/llama-2-70b-chat:2796ee9483c3fd7aa2e171d38f4ca12251a30609463dcfd4cd76703f22e96cdf",
    input={"temperature": 0.2,
           "max_length": 150,
           "top_p": 1},
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
As a hospital chatbot, I'm here to provide information about diseases, wellness tips, and answer general medical questions.\n
your question is "{query}?"
"""

    
    
    CUSTOM_QUESTION_PROMPT = PromptTemplate(input_variables = ['query'], template=custom_prompt_template)


    qa_chain = ConversationalRetrievalChain.from_llm(
    llm = llm,
    chain_type='stuff',
    retriever=retriever,
    return_source_documents=False, 
    return_generated_question = False,
    verbose=True,
    # memory = memory
    )
    
    vectdb = kb.get_vector_db()
    chat_history = []

    while True:
        query = input("User: ")
        if query == 'exit':
            break

        result = qa_chain({"question": CUSTOM_QUESTION_PROMPT.format(query=query), "chat_history": chat_history})
        print(result["answer"])
        # chat_history.extend([(query, result["answer"])])


if __name__ == '__main__':
    main()