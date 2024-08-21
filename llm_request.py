from langchain.chat_models import ChatOpenAI
import re
import demjson3 as demjson

from llm_log import *

import llm_setup

# Parse the user's request
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
    
    # Make sure we have a proper JSON object
    #print ("----------------------- RETURNING JSON ---------------------")

    # Try to extract JSON
    #print ("......................................................")
    #print (to_return)
    # Test 1
    if "```json" in to_return and '"answer"' in to_return:
        to_return = re.search(r'.*(\{\s*"answer"[^`]+)', to_return.replace("\n","")).groups()[0]

    # Test 2
    if "```json" in to_return:
        to_return = to_return.split("```json")[1].split("```")[0]

    # Test 3
    if to_return[0] != "{":
        #print (to_return)
        to_return = re.search(r'[^\{]*(\{.+\})', to_return.replace("\n","")).groups()[0]
    
    #logger.debug (">>>>>>>>>>>>>>>>>>>>>")
    #logger.debug (to_return)
    #logger.debug ("<<<<<<<<<<<<<<<<<<<<<")

    try:
        ## DEMJSON is an error tolerant JSON manager
        ret_value = demjson.decode(to_return)
    except Exception as e:
        logger.error ("[[%s]]" %e)
    
    return ret_value
#chain.invoke("play songs by paul simon and led zeppelin and the doors")['data']
