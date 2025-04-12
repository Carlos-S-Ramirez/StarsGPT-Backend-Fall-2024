from typing import List
from uuid import uuid4
from datetime import datetime
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from src.openAI.models import ClientMessages

from src.langchainAPI.router import chat_chain_instance


def getOpenAIResponse(messages: List[ClientMessages], conversation_id: str, model: str):

    strippedMessages = map(lambda x: {"role": x.role, "content": x.content}, messages)
    systemMessage = [
        {
            "role": "system",
            "content": "Hello! You are my personal coding assistant! Whenever outputing code, please do not say the answer directly. Instead lead me in the correct direction! Also, every response MUST adhere to markdown. To keep things organized try to make use of headings and bullets. Additionally, any code that is output MUST be in a code block. For example: ```python print('Hello World!') ``` Also code blocks MUST BE seperated by at least a single line. Additionally, math equations must be in latex format. For example: $$y = mx + b$$",
        }
    ]
    strippedMessages = list(strippedMessages)

    allMessages = systemMessage + strippedMessages

    chat_chain_instance.initialize_chain(model)
    chain = chat_chain_instance.chain
    parsedMessages = parseMessages(allMessages)

    res = chain.invoke({"input": parsedMessages[-1], "history": parsedMessages})  # type: ignore

    # Old way
    # res = openai.chat.completions.create(
    #     messages=allMessages,  # type: ignore USE CHAIN.INVOKE
    #     model=model.lower(),
    #     n=1,  # type: ignore
    # )

    messageID = str(uuid4())

    time = (datetime.now()).replace(microsecond=0).isoformat()

    parsedResponse = parse_chain_response(res)

    message = {
        "role": "assistant",
        "content": parsedResponse["content"],
        "conversation_id": conversation_id,
        "created_at": time,
        "id": messageID,
    }

    metadata = {
        "chat_completion_id": parsedResponse["id"],
        "completion_tokens": parsedResponse["completion_tokens"],
        "created": time,
        "id": parsedResponse["id"],
        "message": messageID,
        "model": parsedResponse["model"],
        "prompt_tokens": parsedResponse["prompt_tokens"],
        "system_fingerprint": None,
        "total_tokens": parsedResponse["total_tokens"],
    }

    return {"message": message, "metadata": metadata}


def parseMessages(messages):
    finalMessages = []

    for message in messages:
        if message["role"] == "human":
            finalMessages.append(HumanMessage(content=message["content"]))
        elif message["role"] == "assistant":
            finalMessages.append(AIMessage(content=message["content"]))
        else:
            finalMessages.append(SystemMessage(content=message["content"]))

    return finalMessages


def parse_chain_response(response: AIMessage):

    content = response.content
    metadata = response.response_metadata
    tokenUsage = response.response_metadata.get("token_usage")
    model = metadata["model_name"]
    chat_id = response.id
    metadataID = str(uuid4())  # change this
    messageID = str(uuid4())  # change this

    return {
        "content": content,
        "chat_completion_id": chat_id,
        "completion_tokens": tokenUsage["completion_tokens"] if tokenUsage else None,
        "created": (datetime.now()).replace(microsecond=0).isoformat(),
        "id": metadataID,
        "message": messageID,
        "model": model,
        "prompt_tokens": tokenUsage["prompt_tokens"] if tokenUsage else None,
        "system_fingerprint": None,
        "total_tokens": tokenUsage["total_tokens"] if tokenUsage else None,
    }
