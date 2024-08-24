import llm_setup
import llm_parse
import re
import json

#from request_llm import user_message, user_message, validation_user_message, validation_system_message_step_1


def validate(json_filename, user_message, validation_user_message, validation_system_message_step_1):

    with open(json_filename,"r") as f:
        json_plan=f.read()
    
    parsed_json = json.loads(json_plan)

    with open("temp_tasks.txt","r") as f:
        proposed_plan=f.read()
    

    validation_text = """
        Ignore all elements not mentioned in the user specification. 
        Consider element parts (as slices or portions) the same as the element themselves.
        
        For each element mentioned by the user, check that all required actions were performed and that the final state is in line with what the user expects.

        Check that other additional comments about the final state of the system are considered in the plan. Unncessary actions are OK as long as the final result is what the user expected.

        The user request is:
        ----------------------------------------
        """ + user_message + """
        ----------------------------------------

        The proposed plan is:
        ----------------------------------------
        """ + proposed_plan + """
        ----------------------------------------

      The output of your analysis will be another JSON object with the following format:
        - MISSION_NAME: """ + parsed_json["MISSION_NAME"] + """
        - SUCCESS: a boolean ("true" or "false" depending on your validation process)
        - REVISED_ELEMENTS: an array indicating all elements that were considered in the analysis.
        - INFO: if everything is correct should contain the text "everything correct". If not, it should explain why the validation was not succesfull.

        Your output should only show a single JSON object, without extra explanations or characters. Just return a single JSON object.
    """
    

    final_validation=llm_parse.parse_request(validation_text, system_message="Validate the plan")

    print ("=============================")
    print (final_validation)

    return final_validation
