from .system_specific import *


## YOU SHOULDN'T CHANGE THINGS HERE #########
## Just look in system_specific

### THIS IS THE MAIN SYSTEM MESSAGE #############################

generate_step1_system_message="""

The environment where the robot operates is shown here:
""" + ENVIRONMENT_INFO + """

This environment has these elements:""" + ELEMENTS_IN_SYSTEM + """

The robot has the following characteristics: """ + ROBOT_INFO + """

Divide the user specification into a set of consecutive steps. Then, for each step, define a sequence of ACTIONSEQUENCEs (applied to a certain element) that the robot can execute. In any ACTIONSEQUENCE, clearly indicate with bulletpoints the different steps required to fulfill it, specify in detail those steps (also indicating which additional robot actions may require)

Your output should show a list steps, divided into a list of ACTIONSEQUENCE on elements. To clearly identify each block, before and after each block add this text: "################"

Keep in mind that: """ + HINTS_AND_INITIAL_STATE + """

"""

generate_step2_system_message="""
Analyze the proposed plan here:
_______________________________________________________________________________
%GENERATED_TASK_DECOMPOSITION%
_______________________________________________________________________________

Consider 'ACTIONSEQUENCE's defined in:
""" + ROBOT_INFO + """

Your goal is to convert every action suggested into the plan into a set of consecutive BASE_SKILLS (only use allowed BASE_SKILL commands) for the robot. The goal here is to try to reproduce the plan using BASE_SKILLS of the robot. The BASE_SKILLS are: 
""" + BASE_SKILLS + """

One action described in the plan may be decomposed into one or more BASE_SKILL consecutive exection. 

Consider that the environment only has these elements: """ + ELEMENTS_IN_SYSTEM + """

Consider that:
""" + BASE_SKILL_COMPOSITION + """


The output format of the JSON you should generate has the following variables in it:
    - MISSION_NAME: which represents a summary of the main goal described by the user, using a maximum of three words (written without accents or non-ascii characters) joined by '_'
    - TASKS: which represents the consecutive tasks to be perfomed. These tasks are represented as a JSON array of dictionaries, where each item has the fields: 
        · a 'NAME' that describes a summary of the desired action, using a maximum of three words (written without accents or non-ascii characters, joined by '_'). 
        · a 'SKILL' that matches the BASE_SKILL that best suits for that action. Only BASE_SKILL names can be used here. 
        · a 'DESCRIPTION' a few words explaining the desired action. 
        · a 'LOCATION' field, indicating the location where the task is executed
        · a 'PARAMETERS' a set of parameters that defines how the BASE SKILL has to be performed. Check the format specified for each BASE_SKILL to properly fill the PARAMETERS field.
        · a 'RESULT' object, which contains a string with the name of a variable
 
Your output should only show a single and correct JSON object, without any comments or extra explanation.
"""


### USER MESSAGE USED FOR VALIDATION #############################
validation_user_message = """
Provided JSON is:
%JSON%

"""

### VALIDATION STEP 1, READS THE PREVIOUSLY GENERATED JSON AND 
validation_system_message_step_1="""
You are a software agent (called "VALIDATOR_AGENT") that validates a JSON object (called "JSON") previously created by another software agent (called "PROGRAMMING_AGENT"). 

Following a certain specification by a user, the "PROGRAMMING_AGENT" has created a sequence of tasks (described in "JSON""). 

You have to check that:

1) Only the following elements of a kitchen are referenced in "JSON":""" + ELEMENTS_IN_SYSTEM + """

2) Only the following SKILL elements are used in the JSON:""" + BASE_SKILLS + """

3)  Some initial states and hints are:
""" + BASE_SKILL_COMPOSITION + """


4) Check that consecutive sequence of such SKILLs achieve what the user desired in his initial specification.

5) Interpret the JSON, think how the robot would sequentially execute each SKILL and check that after executing the JSON, the final state desired by the user is achieved.

6) The output of your analysis will be another JSON object with the following fields:
    - MISSION_NAME: name of the JSON you analyzed (which is contained in the 'MISSION_NAME' of the validated JSON)

    - FINAL_STATE_OBJECTS: a dict of JSON objects, where they 'key' is the name of the object that received each action in the tasks, and the value indicates the FINAL state of the object after the consecutive execution of the tasks in the JSON (and its location, if it's known). The name of such final state of the object is a combination of its state and location, as for example: "closed", "sliced and toasted", "sliced, toasted and in the fridge", "open", "sliced in the fridge", etc). For this final state ALWAYS  prioritize tasks that happen later in the provided JSON sequence (this means that, for example, if something was open, then closed, and then opened again... the final state is "open")
    
    - ALL_ACTIONS_ON_OBJECTS: a dict of JSON objects, where they 'key' is the name of the object and the value is an array of all consecutive actions executed in the object (each action is described as string that contains the action + "_" + the task's NAME field)

    
 
Your output should only show a single JSON object, without extra explanations or characters.

"""