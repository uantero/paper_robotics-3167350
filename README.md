
# Harnessing the Power of Large Language Models for Automated Code Generation and Verification


## Description

This project aims to show how programming complex robot behavior can be simplified using the latest innovations from the Generative AI field, such as Large Language Models (LLMS).
The code here shows:
· Data comparing time required by human developers vs an (LLM based) automated system
· The sample code that was used in the paper "Harnessing the Power of Large Language Models for Automated Code Generation and Verification"
  

## Getting started

git clone (the repo) 

**To setup everything:**
First create (and activate) a Python3 virtual env:

    python3 -m -venv env
    source ./env/bin/activate
 Then install required libraries and set up your credentials:
    
    pip install -r requirements.txt
    copy _env.sample .env
  (then edit the .env file you created)

**Edit the file knowledge_base/system_specific.py and add there all the LLMs should know about your system:**

 - A list of available items to interact with
 - A list of possible actions that the robot can perform
 - Hints and initial state of the system
 - Add the required 'user_message' (what should the robot do?)

**To run the system:**

    python main.py

This will:
 
 1. Run the "code generating LLM" and generate the code
 2. Validate this new code with a second "code validating LLM". If something goes wrong, the system will go back to step 1
 3. If this initial validation is OK, the system will be simulated under AI2-THOR (see https://ai2thor.allenai.org/)

(Note: the file 'known_info.json' contains the ID and the location of different items in the environment)        

