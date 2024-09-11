import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.globals import set_debug


# Load info from .env file
load_dotenv()

set_debug(False)


# Name of LLM provider
SOURCE = os.getenv("SOURCE")

def get_models():
    # In this paper we use LLAMA3
    return [ "meta-llama/Meta-Llama-3-70B-Instruct"]
    #return [ "meta-llama/Meta-Llama-3.1-70B-Instruct"]
    
    

def get_llm(model="", response_format="json_object"):
    if not model:
        model = get_models()[0]

    llm = ChatOpenAI(
        model_name=model,
        base_url=os.getenv("BASE_URL"),
        api_key=os.getenv("API_KEY"),
        temperature=0,
        max_tokens=3500,        
        model_kwargs = {
            'frequency_penalty':0,
            'presence_penalty':0,
            'top_p':1.0,
            "response_format": {"type": response_format}
        }
    )


    return llm
