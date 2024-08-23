import llm_setup
import llm_parse
import re
import json

#from request_llm import user_message, user_message, validation_user_message, validation_system_message_step_1


def validate(json_filename, user_message, validation_user_message, validation_system_message_step_1):
    from knowledge_base.system_specific import ELEMENTS_IN_SYSTEM
    json_content = ""

    # Using the JSON generated by the first LLM, we make a summary of actions on objects in order to try to estimate their final state
    elements= {}
    for each in ELEMENTS_IN_SYSTEM.split("\n"):
        if " - " not in each:
            continue        
        element_name = re.search("\s*-\s*([^:]+)\:.+", each).groups()[0]
        element_name=element_name.lower()


        if element_name.replace(" ",""):
            elements[element_name]={
                "actions": []
            }

    with open(json_filename,"r") as f:
        json_content=f.read()
    
    parsed_json_content = json.loads(json_content)

    for each_task in parsed_json_content["TASKS"]:
        
        #if any(substring in each_task["NAME"].lower() for substring in elements):
        subject_element=""
        destination_element=""
        if each_task["PARAMETERS"].get("subjectId",""):
            value = re.sub("\$\{id_([^\}]+)\}",r'\g<1>', each_task["PARAMETERS"].get("subjectId",""))
            subject_element = value.split("_")[0]
        
        if each_task["PARAMETERS"].get("objectId",""):
            value = re.sub("\$\{id_([^\}]+)\}",r'\g<1>', each_task["PARAMETERS"].get("objectId",""))
            destination_element = value.split("_")[0]

        element = subject_element
        if not subject_element:
            element = destination_element

        if element in elements:
            if "moverobot" not in each_task["SKILL"].lower():
                # Element 1 (action may involve 2 elements)
                element_name = element
                action_name = "%s::%s" %("_".join(each_task["NAME"].split("_")[:2]).lower(), element_name)
                if subject_element:
                    action_name = action_name + " into " + destination_element
                elements[element_name]["actions"].append(action_name)            


    json_for_validation = {
        "MISSION_NAME": parsed_json_content["MISSION_NAME"],
        "ELEMENT_INFO": elements
    }

    print ("********************************")
    print (json_for_validation)
    print ("********************************")


    # We'll use this new structure, where we identify objects used in our scenario and actions performed on them
    validation_user_message = validation_user_message.replace("%JSON%", json.dumps(json_for_validation, indent=2))

    # First loop: think about final states of different elements
    #first_validation=llm_parse.parse_request(validation_user_message, system_message=validation_system_message_step_1)
    #print ("________________________________________")
    #print (validation_user_message)
    #print ("________________________________________")

    second_validation_text = """
        Ignore all elements not mentioned in the user specification. 
        Consider element parts (as slices or portions) the same as the element themselves.
        
        For each element mentioned by the user, write a short summary using bullet points with the following lines:
          - One line "Actions" line where you describe (in order) every action on that element.             

          - Another "Final state" line with the element's final state after all actions
          
          - A final 'Check for order actions errors' line. In this line, check for errors following this guide (if an error is found, add '* ERROR FOUND *' in the begininning of the line, and explain such error): 
             · Check for required precedence in the following actions (if not met, remark there's an error): 
                - You can't put an element somewhere if you did not pick it before (every "put" needs a previous "pick")
                - Moving an placing an element somewhere needs a previous action where the element is picked.
                - Every action to close an element needs a previous action to open the element
                - Every deactivation or switching off action needs a previous switching on action
                - In order to pick things from closed elements we have to open them first
                            
        
        Use the provided JSON: 
        %JSON%

    """.replace("%JSON%", "%s" %(json.dumps(json_for_validation)))

    second_validation=llm_parse.parse_request(second_validation_text, system_message="Read and intepret the JSON and generate a detailed answer", response_format="text" )

    print ("________________________________________")
    print (second_validation)
    print ("________________________________________")

    # Second loop: check if this is what the user wanted
    final_validation_user="""
    Initially, the user indicated the next specification (between ________):
    USER SPECIFICATION: ________
    %USER_SPEC%
    ________

    Check if this information for the system's final state (check the line 'Final state' for each element) is acceptable according the user specification (for the validation, ignore elments not mentioned by the user. Also ignore final state of objects whose final state was not explicitly specified by the user. Don't consider initial states in your analysis).

    Consider also if the action sequence on objects is logical and correct. 
    For every manipulated element, check order action errors, pay special attention to the lines 'Check for order actions errors'

    ACHIEVED FINAL STATE: ________
    %FINAL_STATE%
    ________


    """
    final_validation_user=final_validation_user.replace("%USER_SPEC%", user_message)
    final_validation_user=final_validation_user.replace("%FINAL_STATE%",  second_validation)

    final_validation_system = """
      Check if the ACHIEVED FINAL STATE matches what the user request, and pay special attention to user requirements about how the system should be as as final state.

      The output of your analysis will be another JSON object with the following format:
        - MISSION_NAME: name of the JSON you analyzed (which is contained in the 'MISSION_NAME' of the validated JSON)
        - SUCCESS: a boolean ("true" or "false" depending on your validation process)
        - REVISED_ELEMENTS: an array indicating all elements that were considered in the analysis.
        - INFO: if everything is correct should contain the text "everything correct". If not, it should explain why the validation was not succesfull.

        Your output should only show a single JSON object, without extra explanations or characters. Just return a single JSON object.
    """

    # Avoid calling another LLM if the error is there...
    if "* ERROR FOUND *" in second_validation:
        return {
            'MISSION_NAME': json_for_validation["MISSION_NAME"], 
            'SUCCESS': False, 
            'REVISED_ELEMENTS': [], 
            'INFO': second_validation.split("* ERROR FOUND *")[1].split("\n")[0]
        }

    final_validation=llm_parse.parse_request(final_validation_user, system_message=final_validation_system)

    #print ("=============================")
    

    return final_validation
