from .system_specific import *


## YOU SHOULDN'T CHANGE THINGS HERE #########
## Just look in system_specific

### THIS IS THE MAIN SYSTEM MESSAGE #############################

generate_step1_system_message="""

The environment where the robot operates is shown here:
""" + ENVIRONMENT_INFO + """

This environment has these elements:""" + ELEMENTS_IN_SYSTEM + """

The robot has the following characteristics: """ + ROBOT_INFO + """

The robot only has the next habilities:
 - Move to a location
 - Pick objects with its hand (maximum one object at the same time). Check if the object can be picked.
 - Put objects in its hand into other objects
 - Slice (for that, the robot has to have previously picked a knife)
 - Open or close objects (which can be opened)
 - Switch on or off electrical appliances

Keep in mind that: """ + HINTS_AND_INITIAL_STATE + """

Divide the user specification into a set of object-centered sub-goals. Then split such sub-goals into a set of sub-subgoals, with a set of consecutive tasks centered on the objects and their manipulation. 

Take into consideration limitations on objects (avoid picking elements that can't be picked, picking things from inside closed elements, picking elements has to be done first moving to their location, etc). The robot should avoid holding more than one element in its hand in any moment. 

Subgoals should be named: "** SUBGOAL <name of subgoal>"
Sub-Subgoals should be named: "  > SUBSUBGOAL <name of subgoal>"

In your output show the goals, subgoals (and sub-subgoals if they exist) and tasks without further explanation. To clearly identify subgoals, before and after each subgoal add this text: "################"

"""

generate_step2_system_message="""
Analyze this text and extract all task described there. Then create a JSON of consecutive "tasks" that reflect such task sequence.
_______________________________________________________________________________
%GENERATED_TASK_DECOMPOSITION%
_______________________________________________________________________________
Info about the elements: """ + ELEMENTS_IN_SYSTEM + """

Allowed commands for the robot: """ + BASE_SKILLS + """

""" + BASE_SKILL_COMPOSITION + """


The JSON to program the robot has the following variables in it:
    - MISSION_NAME: which represents a summary of the main goal described by the user, using a maximum of three words (written without accents or non-ascii characters) joined by '_'
    - TASKS: which represents the consecutive tasks to be perfomed. These tasks are represented as a JSON array of dictionaries, where each item has the fields: 
        · a 'NAME' that describes a summary of the desired action, using a maximum of three words (written without accents or non-ascii characters, joined by '_'). 
        · a 'SKILL' that matches the BASE_SKILL that best suits for that action. Only BASE_SKILL names can be used here. 
        · a 'DESCRIPTION' a few words explaining the desired action. 
        · a 'LOCATION' field, indicating the location where the task is executed
        · a 'PARAMETERS' a set of parameters that defines how the BASE SKILL has to be performed. Check the format specified for each BASE_SKILL to properly fill the PARAMETERS field.
        · a 'RESULT' object, which contains a string with the name of a variable
 
Your output should only show a single JSON object, without extra explanations or characters.
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