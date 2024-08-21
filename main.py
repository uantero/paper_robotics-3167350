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
    "generate": False,
    "validate": False,
    "simulate": True
}

## Code generation
if TESTS["generate"]:
    generate.generate_code(knowledge_base.user_message, knowledge_base.system_message, OUTPUT_JSON_FILENAME)
    logger.debug ("Code generated on '%s'" %OUTPUT_JSON_FILENAME)

## Code validation
if TESTS["validate"]:
    validation_result = validate_json.validate(OUTPUT_JSON_FILENAME, knowledge_base.user_message, knowledge_base.validation_user_message, knowledge_base.validation_system_message_step_1)
    if not validation_result["SUCCESS"]:
        logger.error ("Code can't be validated! Info: %s" %validation_result["INFO"])
        sys.exit(1)    
    else:
        logger.debug ("Code has been validated!")
    

## Simulate system for final validation
if TESTS["simulate"]:
    final_state_validation.validate(OUTPUT_JSON_FILENAME)



