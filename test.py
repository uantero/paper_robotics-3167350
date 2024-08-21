import llm_parse
import json

from request_llm import system_message, user_message

result=llm_parse.parse_request(user_message, system_message=system_message)

print ("================================================")
print (json.dumps(result, indent=2))
print ("================================================")
