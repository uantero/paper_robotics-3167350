from .state_machine import STATE_MACHINE
import sys
import time


# This will simulate everything in AI2-THOR
# It will check that the:
#  - Fridge was closed
#  - Bread is toasted
#  - Tomatp is in the fridge
#  - Egg is in bowl
def validate(filename="output.json"):
    #if len(sys.argv)>1:
    #    filename=sys.argv[1]
    #else:
    #    filename="sample.json"

    sm = STATE_MACHINE(filename)

    sm.execute()

    bread_in_fridge = sm.check_object_inside("Fridge","Bread")
    bread_is_cooked = sm.check_object_is_cooked("Bread|-00.78|+01.00|+00.21|BreadSliced_1")

    tomato_in_fridge = sm.check_object_inside("Fridge","Tomato")
    egg_in_bowl = sm.check_object_inside("Bowl","Egg")

    fridge_closed = not sm.check_object_open("Fridge")

    print ("\n")

    # This will look for: fridge closed, bread toasted, tomato in fridge and egg in bowl
    if (fridge_closed and bread_is_cooked and
        tomato_in_fridge and egg_in_bowl):

        print ("[[ ------------------ ]]")
        print ("[[ Success!!!! 👍👍👍 ]]")
        print ("[[ ------------------ ]]")
    else:
        print ("[[ --------- ]]")
        print ("[[ Failed 😔 ]]")
        print ("[[ --------- ]]")
        print ("Fridge closed: %s" %fridge_closed)
        print ("Bread is toasted: %s" %bread_is_cooked)
        print ("Tomato in fridge: %s" %tomato_in_fridge)
        print ("Egg in bowl: %s" %egg_in_bowl)

    # Wait to avoid the display to be closed
    time.sleep(10000)
