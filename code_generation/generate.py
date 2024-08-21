import llm_parse
import json

#from request_llm import system_message, user_message

# Main function

def generate_code(user_message, system_message, output_filename):

    result=llm_parse.parse_request(user_message, system_message=system_message)

    with open(output_filename, "w") as f:
        f.write(json.dumps(result, indent=2))

    #print ("================================================")
    #print (json.dumps(result, indent=2))
    #print ("================================================")

    return result

