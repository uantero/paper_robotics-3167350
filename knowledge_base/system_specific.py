### THIS IS THE MAIN USER MESSAGE #############################
user_message = """
I want the robot to make me a toasted slice of bread, and then put it into the fridge.

Once you finished, take the tomato and put it into the fridge.

I also want to put the egg that is in the fridge into the bowl.

The initial state of the elements in the kitchen is: the fridge is closed, the toaster is switched off.
Make sure that in the end, elements are back in their initial state, and that the sliced bread is toasted and inside the fridge.

"""

#################################################################


###
ELEMENTS_IN_SYSTEM = """
 - Toaster
 - Knife
 - Tomato
 - Drawer
 - Bread
 - Egg
 - Bowl
 - Fridge
 """

BASE_SKILLS = """
    · 'MoveRobot': which has one parameter called 'location'. Each 'location' has the form '<object>_location' where <object> is a reference to the object close to that location (for example: 'fridge_location')
    · 'PickupObject': skill to pick an object by the robot. This skill has one parameter: 'objectId' (which defines the ID of the object to pick).
    · 'OpenObject': skill to open an object by the robot. This skill has one parameter: 'objectId' (which defines the ID of the object to open).
    · 'CloseObject': skill to close an object by the robot. This skill has one parameter: 'objectId' (which defines the ID of the object to open).
    · 'PutObject': this skill puts the object previously picked inside another object, and so the robot is no longer in possesion of the  picked object. This skill has one parameter: 'objectId' (which defines the ID of the container object). 
    · 'SliceObject': skill to slice an object. This skill has one parameter: 'objectId' (which defines the ID of the object to slice).
    · 'TurnOn': skill to switch on a kitchen appliance. This skill has one parameter: 'objectId' (which defines the ID of the object to switch on).
    · 'TurnOff': skill to switch off a kitchen appliance. This skill has one parameter: 'objectId' (which defines the ID of the object to switch off).
    · 'MoveHeldObjectAhead": a skill to move forward a certain amount the object we picked. It has one parameter: 'moveMagnitude' (a number indicating the amount to move forward)
    · 'DropHandObject': a skill to drop the object the robot had in its gripper. Can't use it if the robot is no longer holding the object, or after putting an object in another. Before using it, it is required to use a previous skill of MoveHeldObjectAhead (0.3).

  Before every action, you have to move to a location where you have access the object required for the action (using the "MoveRobot" BASE_SKILL).
  Unless specified otherwise, all "objectId" values have to be written as ${id_<name of the object>} (where you have to substitue <name of the object> by its name).
"""

BASE_SKILL_COMPOSITION = """
  · Performing any action on an object means that first we have to move close to it
    · In order to toast something, the order of actions is: pick the object to be toasted, move it to the toaster, put it in the toaster, switch on the toaster, switch off the toaster and pick the toasted object from the toaster
  · In order to "slice" an object, it is required that first we pick a cutting device (such as knife), and then move to close to the object to be sliced. It's not necessary to pick the object to be sliced. After being sliced, an object's ID changes and "_sliced" should be attached to its ID.
"""

HINTS_AND_INITIAL_STATE = """
 - the knife is inside the drawer. Be sure to close the drawer when the knife is picked.
 - the bread can't be moved or picked until it has been sliced
 - the egg is inside the fridge
 - it is recommended to close the fridge every time you pick something from it
 - the right sequence to slice the bread is: pick the knife, move the where the bread's location, slice the bread, and then drop the knife on the countertop.
 - It's not possible to pick more than one object at the same time.
 - The toaster only accepts bread slices
 - Initial states are: drawer is closed, toaster is switched off, fridge is closed.
"""

