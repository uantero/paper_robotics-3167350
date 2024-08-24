### THIS IS THE MAIN USER MESSAGE #############################
user_message = """
I want you to help me creating a flow program for a robot.

The user specification is described here between brackes:
[
  I want the robot to prepare me a breakfast. First I want the robot to pick an egg from the fridge and fry it into the pan, then I want the robot to prepare me a slice of toasted bread and put that into the plate.
   
]
"""

ELEMENTS_IN_SYSTEM = """
  Info about the elements:
  - Egg: is inside the fridge. Location: fridge.
  - Spatula: is on the countertop. Location: spatula.
  - Stove: is a stove for cooking. Location: stove.
  - Pan: a frying pan used for cooking. Location: pan.
  - Plate: an empty plate located on top of the countertop. Location: plate
  - Countertop: a countertop. Location: countertop
  - Basin: a kitchen sink. Location: basin
  - Toaster: is on the countertop. Can be switched on and off. Location: toaster_location
  - Knife: is inside the drawer. Location: drawer
  - Tomato: on the countertop. It's a whole tomato, but it can be sliced. Location: tomato_location
  - Bread: on the countertop. Bread can't be picked until it has been sliced. Location: bread_location
  - Drawer: is initially closed. Location: drawer
  - Fridge: is initially closed. Location: fridge
 """
ENVIRONMENT_INFO = """
  Environment:
  The environment is a kitchen with some elements in it.
"""

ROBOT_INFO = """
    Robot:
      - The robot has one hand to pick and drop things, or to manipulate tools. If the hand is holding one thing, it can not hold any other thing or tool.
      - The robot can only pick things, move to locations, slice things, open and close things, and put objects into other objects.

    The robot only has the next habilities:
    - Move to a location
    - Pick objects with its hand (maximum one object at the same time). Check if the object can be picked.
    - Put objects in its hand into other objects
    - Slice (for that, the robot has to have previously picked a knife). Objects are sliced without having to pick them first (they're sliced in their location). Slices then can be picked (if required)
    - Open or close objects (which can be opened)
    - Switch on or off electrical appliances      

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
        - Slicing an object must be done executing the sequence: pick the slicing tool from its location (open it if it was closed), move the object, slice and then return the slicing tool to its original location (and leave it in its original state)

        - Regarding manipulation of objects: without tools the robot can only pick and drop objects. In order to do any other action, it has to pick a certain tool (knife, scissors, screwdriver... if they're available). After finishing any operation, the used tool should be put back in its initial place.
        
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
      - In order to toast something, you first have to slice it, then pick it, put it into the toaster, switch on the toaster, switch off the toaster, and pick the toasted object from it.
      - In order to slice something you have to pick the knife (check if that position has to be opened), then slice the object. After slicing, return the knife to its location.
      - In order to put an element in a container, we must not pick the container. The robot should pick the element, move to the container's location and put the element in the container
      - If an object is inside a container, the robot should open the container first 
"""