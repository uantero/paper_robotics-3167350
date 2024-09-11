import llm_parse
import json


# Main function
def generate_code(user_message, system_message_step1, system_message_step2, output_filename):

    # Step 1: create text-based task decomposition
    task_decomposition=llm_parse.parse_request(user_message, system_message=system_message_step1, response_format="text")

    with open("temp_tasks.txt", "w") as f:
        f.write(task_decomposition)

    with open("temp_tasks.txt", "r") as f:
       task_decomposition= f.read()

    system_message_step2 = system_message_step2.replace("%GENERATED_TASK_DECOMPOSITION%", task_decomposition)
    
    # Step 2: Create JSON
    result=llm_parse.parse_request(user_message, system_message=system_message_step2, response_format="json")

    with open(output_filename, "w") as f:
        f.write(json.dumps(result, indent=2))

    return result

