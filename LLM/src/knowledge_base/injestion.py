from knowledgebase import MyKnowledgeBase
from knowledgebase import (
    DOCUMENT_SOURCE_DIRECTORY
)

# kb is here knowledge base
kb = MyKnowledgeBase(
        pdf_source_folder_path=DOCUMENT_SOURCE_DIRECTORY
)

kb.initiate_document_injetion_pipeline()