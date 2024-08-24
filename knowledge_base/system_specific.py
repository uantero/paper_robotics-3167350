### THIS IS THE MAIN USER MESSAGE #############################
user_message = """
I want you to help me creating a flow program for a robot.

The user specification is described here between brackes:
[
  Make a toasted slice of bread, with a slice of tomato on top of it.
   
]
"""

ELEMENTS_IN_SYSTEM = """
  Info about the elements:
  - Egg: is inside the fridge. Location: fridge.
  - Spatula: is a tool on the countertop. Location: spatula.
  - Stove: is a an appliance for cooking. Location: stove.
  - StoveBurner: the burner of the stove. Location: stove_burner.
  - Pan: a frying pan is a tool used for cooking. Location: pan.
  - Plate: an empty plate located on top of the countertop. Location: plate
  - Countertop: a countertop. Location: countertop
  - Basin: a kitchen sink. Location: basin
  - Toaster: is an appliance on the countertop. Can be switched on and off. It can only toast slices of bread. Location: toaster_location
  - Knife: is a tool inside the drawer. Location: drawer
  - Tomato: on the countertop. It's a whole tomato, but it can be sliced. Location: tomato_location
  - Bread: a whole loaf. It's a whole bread, but it can be sliced. Bread has to be sliced in the bread slicing pad before toasted. Location: bread_slicing_pad
  - Drawer: is initially closed. Location: drawer
  - Fridge: is an appliance initially closed. Location: fridge
 """
ENVIRONMENT_INFO = """
  Environment:
  The environment is a kitchen with some elements (objects) in it.
"""

ROBOT_INFO = """
    The robot can do four kinds of "ACTIONSEQUENCE". Each "ACTIONSEQUENCE" is "atomic" this means that the action sequence has to be finished before doing another action. The allowed "ACTIONSEQUENCE" for the robot are shown here:

     1.- MOVING: Moving to new location: the robot can move into new locations. 

     2.- PICK_TOOL: Is a sequence to pick a tool from its location: the robot should move to the tools location and then pick it. If the tool is in a place that is closed, open the container before picking the tool. 

     3.- ELEMENT_MODIFICATION: an operation (such as "slice", "cut", "break" or "chop") that changes an element using a tool (for example: a knife). The robot should execute the sequence: drop any element (that is not a tool) it may have in its hand, pick a tool from its location (using PICK_TOOL), and do the manipulation action. 
    
     4.- ACT: Act on elements: change the state of an element with actions like: open or close elements (which can be opened), "switch on" or "switch off" (electrical appliances). 
    
     5.- PICK&PLACE: Is a sequence of: move the robot to where the element is located, "pick an element", "move the robot to a destination location" and "place" the element in a position. At the end of PICK&PLACE the robot should have no element in its hand

     When the robot has to perform a MANIPULATE on an object, that object should not be moved (PICK&PLACE) until the MANIPULATE has finished.

     In its initial state, the robot's hand is empty.
"""

BASE_SKILLS = """
  Only the following BASE_SKILLs are allowed.
      · 'MoveRobot': which has one parameter called 'location'. Each 'location' has the form '<object>_location' where <object> is a reference to the object close to that location

      · 'PickupObject': skill to pick an object by the robot (the object must be pickable by the robot). This skill has one parameter: 'objectId' (which defines the ID of the object to pick). Always move to the location of the element to be picked, before picking something. 
      
      · 'OpenObject': skill to open an object by the robot (the object must be able to be opened). This skill has one parameter: 'objectId' (which defines the ID of the object to open).

      · 'Wait': waits some time.
      
      · 'CloseObject': skill to close an object by the robot (the object must be open). This skill has one parameter: 'objectId' (which defines the ID of the object to open).
      
      · 'PutObject': this skill puts (or drops) the object (that you now have in your hand) into another specified object. Can be used to drop one object into another one. This skill has two parameters: 'objectId' (which defines the ID of the destination object), and 'subjectId' (the element we're manipulating). Make sure that the robot moved to the location of the destination object before putting the object there.
      
      · 'SliceObject': skill to slice an object. This skill has one parameter: 'objectId' (which defines the ID of the object to slice). After being sliced, an object's ID changes and "_sliced" should be attached to its ID. In order to slice, the robot must have previously picked a tool for cutting or slicing.
      
      · 'TurnOn': skill to switch on a kitchen appliance. This skill has one parameter: 'objectId' (which defines the ID of the object to switch on).
      
      · 'TurnOff': skill to switch off a kitchen appliance. This skill has one parameter: 'objectId' (which defines the ID of the object to switch off).
      
      · 'MoveHeldObjectAhead": a skill to move forward a certain amount the object we picked. It has one parameter: 'moveMagnitude' (a number indicating the amount to move forward)
      
    All "objectId" values always have to be written as ${id_<name of the object>} (where you have to substitue <name of the object> by its name).
"""

BASE_SKILL_COMPOSITION = """
    BASE_SKILLS can be combined to create more complex actions, like for example:
        - Slicing an object must be done executing the sequence: pick the slicing tool from its location (open it if it was closed), move to the object to be sliced, slice the object and then return the slicing tool to its original location (and leave it in its original state)

        - Regarding manipulation of objects: without tools the robot can only pick and drop objects. In order to do any other action, it has to pick a certain tool (knife, scissors, screwdriver... if they're available). After finishing the manipulation operation, the used tool should be put back in its initial place (for that, it may be necessary to check if its container is open or closed and act on it).
        
        - The robot can only pick items for moving them to other locations. When the object is in the final destination it should be put there to avoid manipulating more than one object at a time.
        
        - In order to do any manipulation on the object (pick it, slice it, open it, close it, switch it on, ... ) we first have to move where the object is located, and execute the action on the object without moving it (we may have picked a tool to achieve that). 

        - Before droping an object, first move to its final destination

        Some examples:
        · To put an object somewhere (or to drop it somewhere), the sequence should be: move to object's location, pick object, put it in the final destination
        · Before picking any object the robots should move to the location of the object that is being picked    
        · For each specified task, indicate the robot's location, and when picking or droping something indicate state of hand (and amount of elements it holds). This information should be shown as: - <short description of task> ["location: "xxxx", "nb_objects": "0"]

"""
HINTS_AND_INITIAL_STATE = """
    Some hints:
      - In order to slice something you have to pick the knife (check if that position has to be opened), then slice the object. After slicing, return the knife to its location.
      - In order to put an element in a container, we must not pick the container. The robot should pick the element, move to the container's location and put the element in the container
      - If an object is inside a container, the robot should open the container first 
"""