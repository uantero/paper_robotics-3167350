from langchain.chat_models import ChatOpenAI
import json
from typing import Optional, List

import enum

from llm_request import llm_request


import llm_setup

def parse_request(user_request, previous_user_request="", previous_avatar_answer="", system_message="", response_format=""):

    models = llm_setup.get_models()#[ "meta-llama/Meta-Llama-3-70B-Instruct", "databricks/dbrx-instruct", "microsoft/WizardLM-2-8x22B"]

    value = {}
    for each_model in models:
        #print ("Model: %s" %each_model)
        value = parse_request_run(user_request, each_model, previous_user_request, previous_avatar_answer, system_message, response_format)
        #print (value)
        if value:
            return value
    return value

# Parse the user's request
def parse_request_run(user_request, model, previous_user_request="", previous_avatar_answer="", system_message="", response_format=""):

    if previous_user_request:
        user_request += "\n\nFor your answer, take into account that (in case that previous request is related to the current request) the previous user request was : %s" %previous_user_request

    if previous_avatar_answer:
        user_request += "\n\nFor your answer, take into account that (in case that previous answer is related to the current request) that the previouse question you sent to the user was : %s" %previous_avatar_answer

    if not system_message:
        system_message = """
            You are a robot located in Tecnalia's booth, that has two arms: 'left_arm' and 'right_arm'.

            You should consider that instructions given to you by the user are instructions for you to create a robot program based on the next instructions.

            You have three BASE_SKILLS: 'pick', 'place' and 'greet'.
            - 'pick' and 'place' have to be used for all manipulation related taks.
            - 'greet' for waving, "saludar" or greeting the user.
            Only use these BASE_SKILLS if they're required to meet the user's demand.

            Take into account that "pick" and "place" operations performing on the same object should always use the same "arm". 

            If you the user and context does not provide a clear sequence of actions (for greeting or manipulating objects), just return an empty sequence. 

            You should return a single JSON object without any other extra information.

            The JSON you have to return should represent a decomposition of the user's request into sequences (that are repeated a certain number of times) that combine your BASE_SKILLS ("pick", "place", "greet") as seen in this example:

            {"userrequest":
                [    {"sequence":
                        [
                            {"actions": [
                                    {"unitary_action": "pick", "object": {"name": "hornillo", "number": 1}, "arm": "right_arm"},
                                    {"unitary_action": "place", "position": {"name": "punto", "number": 2}, "arm": "right_arm"},
                                ], "number": 1},
                            {"actions": [
                                    {"unitary_action": "greet", "arm": "left_arm", "time": 1},
                                    {"unitary_action": "greet", "arm": "right_arm", "time": 2}
                                ], "number": 3},
                        ]
                    }
                ]
            }

            If the user does not provide an action sequence for the robot, and asking about the demo or requesting other kind of actions, return an empty 'sequence' list.

        """

    result = llm_request(user_request, system_message=system_message, response_format=response_format)


    #print ("Trying to parse:")
    #print (json.dumps(user_request))
    #print (".........................")
    #print (result)




    #print (" ========= RESULT ================")
    #print (result)        
    #print (" ========= /RESULT ================")

    #print ("")
    #print ("")

    return result
#chain.invoke("play songs by paul simon and led zeppelin and the doors")['data']
