from langchain.chat_models import ChatOpenAI
from langchain.globals import set_debug

import re
import demjson3 as demjson

from llm_log import *

import llm_setup

set_debug(False)

# Parse the user's request and return a JSON object
def llm_request(user_request, system_message="", previous_context="", previous_user_request="", response_format=""):

    models = llm_setup.get_models()
    error_info=""
    for each_model in models:
        logger.debug ("[[ TRYING WITH MODEL: %s]]" %each_model)
        try:
            return llm_request_run(user_request, system_message, previous_context, previous_user_request, each_model, response_format)
        except Exception as error_info:
            return {
                "type": "error",
                "error": "LLM error",
                "error_info": error_info,
                "message": "I could not understand that"
            }
    
    return {
        "type": "error",
        "error": "LLM error",
        "message": "I could not understand that"
    }


# The actual request
def llm_request_run(user_request, system_message="", previous_context="", previous_user_request="", model="", response_format=""):

    if previous_context:
        system_message += "\n\nFor your answer, consider this context information to provide context to the user's request (it's not necessary to repeat previously requested answers): %s" %previous_context

    if previous_user_request: 
        system_message += "\n\nFor your answer, take into account that (in case that request is related to the current request) the previous user request was : %s" %previous_user_request

    llm = llm_setup.get_llm(response_format=response_format)


    #print (schema)
    messages = [
        ("system", system_message),
        ("human", user_request),
    ]

    ret = llm.invoke(messages)    
    to_return = ret.content

    # Default is JSON...
    if "text" in response_format:
        #print ("----------------------- RETURNING TEXT ---------------------")
        return to_return
    
    # Test 0 for proper JSON
    if "```{" in to_return.replace("\n",""):
        to_return = re.search(r'```(\{[^`]+\})', to_return.replace("\n","")).groups()[0]

    # Test 1
    if "```json" in to_return and '"answer"' in to_return:
        to_return = re.search(r'.*(\{\s*"answer"[^`]+)', to_return.replace("\n","")).groups()[0]

    # Test 2
    elif "```json" in to_return:
        to_return = to_return.split("```json")[1].split("```")[0]

    # Test 3
    else:
        #print (to_return)
        to_return = re.search(r'[^\{]*(\{.+\})', to_return.replace("\n","")).groups()[0]
    
    try:
        ## DEMJSON is an error tolerant JSON manager
        ret_value = demjson.decode(to_return)
    except Exception as e:
        logger.error ("\n--------------\n%s\n----------------\n" %to_return)
        logger.error ("[[%s]]" %e)
    
    return ret_value

