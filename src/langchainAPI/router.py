from datetime import datetime
from uuid import uuid4
from fastapi import APIRouter
from langchain_openai import ChatOpenAI

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

from src.langchainAPI.ModelSingleton import ChatChainSingleton

router = APIRouter()

chat_chain_instance = ChatChainSingleton()


# # USE FOR TESTING
# @router.post("/langchain")
# def chat(message: str, model):
#     chat_chain_instance.change_model(model)
#     chain = chat_chain_instance.chain
#     return {"response": chain.invoke({"input": message})}  # type: ignore


# # USE FOR TESTING
# @router.get("/testing/langchain")
# def get_model():
#     return {"model": chat_chain_instance.get_model()}  # type: ignore


# # USE FOR TESTING
# @router.get("/testing/langchain/change")
# def change_model(model):
#     chat_chain_instance.change_model(model)  # type: ignore
#     return {"model": chat_chain_instance.get_model()}  # type: ignore


# USE FOR TESTING
@router.get("/testing/langchain/chain")
def chain_response():

    messages = [
        {
            "id": "fc0c1a6e-ee79-417e-8933-8270f04037fa",
            "created_at": "2024-03-27T16:57:24.653+00:00",
            "role": "system",
            "content": "Hello you are a Tutoring Chatbot. You will help the user figure out the answer to their coding problems. You will not give the answer directly. You will guide the user in the right direction. You will also have a very nice tone and helpful tone. Below, is the user's query, it should be a baseline to help you guide the user in the right direction.\n\nUser Query:\n\n\n\nTitle:Naive Bayes Algorithm\n\nHelp me through the naive bayes algorithm",
        },
        {
            "id": "3833b7de-9e4e-4aa0-a3db-15ab11733c65",
            "created_at": "2024-03-27T16:57:43.738+00:00",
            "role": "user",
            "content": "Hello! Can you help me through the Naive Bayes Algorithm?",
        },
        {
            "id": "d0dd44f6-fab0-4033-8ed9-3baa12358790",
            "created_at": "2024-03-27T16:57:52+00:00",
            "role": "assistant",
            "content": "Sure! I'd be happy to help you with the Naive Bayes Algorithm. \n\nNaive Bayes is a classification algorithm based on Bayes' Theorem with an assumption of independence among features. In simple terms, it calculates the probability of each class and the conditional probability of each feature given the class. \n\nLet's break down the steps involved in implementing the Naive Bayes Algorithm:\n\n### Steps for implementing the Naive Bayes Algorithm:\n1. **Data Preprocessing**:\n  - Handle missing data, if any.\n  - Encode categorical variables if needed.\n  - Split the data into training and testing sets.\n  \n2. **Calculate Class Probabilities**:\n  - Compute the prior probability of each class.\n  \n3. **Calculate Conditional Probabilities**:\n  - For each feature and class, calculate the conditional probability.\n  \n4. **Make Predictions**:\n  - Use the Bayes Theorem to make predictions based on the highest probability.\n  \n5. **Evaluate the Model**:\n  - Use metrics like accuracy, precision, recall, F1 score, or confusion matrix to evaluate the model's performance.\n\nImplementing the Naive Bayes Algorithm usually involves using the Gaussian Naive Bayes, Multinomial Naive Bayes, or Bernoulli Naive Bayes, depending on the nature of the features in your dataset. \n\nDo you have a specific dataset you are working with, or do you need help with the implementation of a particular type of Naive Bayes Algorithm?",
        },
        {
            "id": "ce5efea3-ba7f-48e3-bf12-6e80d404019f",
            "created_at": "2024-03-27T16:59:50.082+00:00",
            "role": "user",
            "content": "Can you be more specific? ",
        },
    ]

    messages = parseMessages(messages)

    chain = chat_chain_instance.chain  # type: ignore

    res = chain.invoke({"input": "what is this conversation about?", "history": messages})  # type: ignore

    return {
        "response": res,
    }


# USE FOR TESTING
def parse_chain_response(response: AIMessage):

    content = response.content
    metadata = response.response_metadata
    tokenUsage = response.response_metadata.get("token_usage")
    model = metadata["model_name"]
    chat_id = response.id
    metadataID = str(uuid4())  # change this
    # change this

    return {
        "content": content,
        "chat_completion_id": chat_id,
        "completion_tokens": tokenUsage["completion_tokens"] if tokenUsage else None,
        "created": (datetime.now()).replace(microsecond=0).isoformat(),
        "id": metadataID,
        "message": "",
        "model": model,
        "prompt_tokens": tokenUsage["prompt_tokens"] if tokenUsage else None,
        "system_fingerprint": None,
        "total_tokens": tokenUsage["total_tokens"] if tokenUsage else None,
    }


# USE FOR TESTING
def parseMessages(messages):
    finalMessages = []

    strippedMessages = map(
        lambda x: {"role": x["role"], "content": x["content"]}, messages
    )

    print(list(strippedMessages))

    for message in strippedMessages:
        if message["role"] == "human":
            finalMessages.append(HumanMessage(content=message["content"]))
        elif message["role"] == "assistant":
            finalMessages.append(AIMessage(content=message["content"]))
        else:
            finalMessages.append(SystemMessage(content=message["content"]))

    return finalMessages
