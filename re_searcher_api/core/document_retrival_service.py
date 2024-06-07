"""
file: document_retrival_service.py
description: response citations processing
"""


import boto3
import re
from srtools import cyrillic_to_latin

from consts import knowledge_base_id, aws_access_key_id, aws_secret_access_key

session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
)

knowledge_base_client = session.client(service_name="bedrock-agent-runtime")

"""
name: get_document_citations
params: user_message, document_file_name
description: returns the citations array with formatted text from response body JSON
"""


def get_document_citations(user_message, document_file_name):
    citations = []

    response = knowledge_base_client.retrieve(
        knowledgeBaseId=knowledge_base_id,
        retrievalQuery={
            'text': user_message
        },
        retrievalConfiguration={
            'vectorSearchConfiguration': {
                'numberOfResults': 5,
                # 'overrideSearchType': "HYBRID",
            }
        }
    )

    for retrievedResult in response["retrievalResults"]:
        citations.append(format_document_text(retrievedResult['content']['text']))

    return citations


"""
name: format_document_text
params: text sentence
response: returns a formatted sentence so the content fed to the OpenAI API is uniform
"""


def format_document_text(text):
    t_sentence = ""
    # In case cyrillic alphabet is used, convert it to latin
    if re.search('[\u0400-\u04FF]', text):
        t_sentence = cyrillic_to_latin(text)
    return t_sentence
