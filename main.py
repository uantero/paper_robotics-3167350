import os
from dotenv import load_dotenv

import knowledge_base
from code_generation import generate
from code_validation import validate_json
from code_validation import final_state_validation
import sys
from llm_log import *

# Load info from .env file
load_dotenv()

OUTPUT_JSON_FILENAME = "output.json"


TESTS={
    "generate": 1,
    "validate": 1,
    "simulate": 0
}

if "simulate" in sys.argv:
    TESTS={
        "generate": 0,
        "validate": 0,
        "simulate": 1
    }

input_from_validation_phase = ""
succesfull_validation=False
retry_number = -1
## Code generation
if not succesfull_validation and (TESTS["generate"] or TESTS["validate"]):
    while not succesfull_validation:
        retry_number = retry_number + 1

        if (retry_number>4):
            logger.error("Could not create code")
            sys.exit(1)

        logger.info("RETRY NUMBER: %s" %retry_number)
        if TESTS["generate"]:
            extra_info = ""
            if input_from_validation_phase:
                extra_info = "\nKeep in mind that when you previously generated code, it failed because: %s" %input_from_validation_phase

            generate.generate_code(knowledge_base.user_message + extra_info, knowledge_base.generate_step1_system_message, knowledge_base.generate_step2_system_message, OUTPUT_JSON_FILENAME)            
            logger.debug ("👍 Code generated on '%s'" %OUTPUT_JSON_FILENAME)

        ## Code validation
        if TESTS["validate"]:
            validation_result = validate_json.validate(OUTPUT_JSON_FILENAME, knowledge_base.user_message, knowledge_base.validation_user_message, knowledge_base.validation_system_message_step_1)
            print ("---------------------")
            print (validation_result)
            print ("---------------------")
            if not validation_result["SUCCESS"]:
                json_code = ""
                with open(OUTPUT_JSON_FILENAME, "r") as f:
                    json_code = f.read()
                logger.error ("Code can't be validated! Info: %s" %validation_result["INFO"])
                input_from_validation_phase = "\n" + "You previously generated some code with errors (shown below): %s" %json_code + "\n\n" + "Consider the user specification and modify the code according the comments about why it failed:\n" + validation_result["INFO"]
                if not TESTS["generate"]:
                    break
            else:
                logger.info ("Code has been validated!")
                break
        else:
            break
    

## Simulate system for final validation
if TESTS["simulate"]:
    print ("💻💻 --> Now I'm going to simulate the program!")
    final_state_validation.validate(OUTPUT_JSON_FILENAME)



