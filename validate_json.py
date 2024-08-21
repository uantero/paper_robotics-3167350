import llm_setup
import llm_parse
import json

from request_llm import user_message, user_message, validation_user_message, validation_system_message_step_1


def main():
    global validation_user_message, system_message
    json_content = ""
    with open("llm_created.json","r") as f:
        json_content=f.read()
    
    parsed_json_content = json.loads(json_content)

    validation_user_message = validation_user_message.replace("%JSON%", json_content)

    # First loop: think about final states of different elements
    first_validation=llm_parse.parse_request(validation_user_message, system_message=validation_system_message_step_1)
    print ("________________________________________")
    print (first_validation)
    print ("________________________________________")

    second_validation=llm_parse.parse_request("Write a short summary using bullet points where you describe the final state of all elements described in the provided JSON: %s" %(json.dumps(first_validation)), system_message="Read and intepret the JSON and generate a detailed answer", response_format="text" )

    # Second loop: check if this is what the user wanted
    final_validation_user="""
    Initially, the user indicated the next specification (between ________):
    ________
    %USER_SPEC%
    ________

    Check if this information for the system's final state is acceptable:
    ________
    %FINAL_STATE%
    ________

    In the JSON, check the next fields:
        - FINAL_STATE_OBJECTS: a dict of JSON objects, where they 'key' is the name of the object that received each action in the tasks, and the value indicates the final state of the object (name of the final state of the object which is a combination of its state and location, as for example: "closed", "sliced and toasted", "open", "sliced in the fridge", etc)
        - ALL_ACTIONS_ON_OBJECTS: a dict of JSON objects, where they 'key' is the name of the object and the value is an array of all consecutive actions executed in the object
        - DESIRED_FINAL_STATE_OF_OBJECTS: considering the user specification, a dict of JSON objects mentioned by the user, where they 'key' is the name of the objects and the value is the final state indicated by the user.

    If the desired final state of an element is not specified, any final state is correct. Don't consider initial states in your analysis.


    """
    final_validation_user=final_validation_user.replace("%USER_SPEC%", user_message)
    final_validation_user=final_validation_user.replace("%FINAL_STATE%",  second_validation)

    final_validation_system = """
        The output of your analysis will be another JSON object with the following format:
        - MISSION_NAME: name of the JSON you analyzed (which is contained in the 'MISSION_NAME' of the validated JSON)
        - SUCCESS: a boolean ("true" or "false" depending on your validation process)
        - INFO: if everything is correct should contain the text "everything corret". If not, it should explain why the validation was not succesfull.
    """


    second_validation=llm_parse.parse_request(final_validation_user, system_message=final_validation_system)

    print ("=============================")
    print (second_validation)



    

if __name__ == "__main__":
    main()



