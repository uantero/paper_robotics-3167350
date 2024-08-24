import json
import time
import sys
import re
from ai2thor.controller import Controller

class STATE_MACHINE:
    def __init__(self, filename='sample.json'):
        self.object_in_hand = None
        self.current_location = ""
        self.filename = filename
        self.controller = Controller()
        self.load()

    def load(self):
        # This reads the information that should be known 
        # (ID of required objects, such as the fridge or the tomato)
        with open('./known_info.json') as user_file:
            file_contents = user_file.read()
            self.known_info = json.loads(file_contents)

        # If no filename is specified, the system will use the name 'sample.json'
        with open('./%s' %self.filename) as user_file:
            file_contents = user_file.read()
            self.machine_json = json.loads(file_contents)    

        self.look_down()
        print (" ---- STATE MACHINE STARTED -----")        

    # In some linux machines, some "empty" action is required to refresh the display
    def refresh(self):

        event = self.controller.step("RotateRight", degrees=0)
        event = self.controller.step("RotateRight", degrees=0)
        return event

    def get_ceiling_image(self):
        # puts the camera in the ceiling, then puts it back with the robot
        event = self.controller.step('ToggleMapView')
        self.controller.step('ToggleMapView')
        frame = event.frame        
        from PIL import Image
        im = Image.fromarray( frame )
        im.save("/mnt/c/temp/1.jpg")                        

    # Check if an object is cooked
    def check_object_is_cooked(self, object_id):
        event = self.refresh()
        is_cooked=False
        for each in event.metadata["objects"]:
            if each["objectId"].lower()==object_id.lower():
                is_cooked=each["isCooked"]
                return is_cooked
        return is_cooked

    # Teleport to a position where the robot can interact with an object
    def teleport_to(self, object_name):        
        object_info = self.known_info["OBJECT_DATA"][object_name]
        event=self.controller.step(action="Teleport",position=object_info["action_location"]["position"],rotation=object_info["action_location"]["rotation"])
        self.current_location = object_name
        print (event)
        event = self.refresh()
        
    # Update object's location
    def update_object_location(self, object_id):
        event = self.refresh()
        self.known_info["OBJECT_DATA"][object_id]["action_location"]["position"]= event.metadata["agent"]["position"]
        self.known_info["OBJECT_DATA"][object_id]["action_location"]["rotation"]= event.metadata["agent"]["rotation"]

    # Check if an object is inside another element
    def check_object_inside(self, receptacle_object_type, object_type):
        event = self.refresh()
        object_inside=False
        for each in event.metadata["objects"]:
            if each["objectType"].lower()==receptacle_object_type.lower():
                for each_object_inside in each["receptacleObjectIds"]:
                    if object_type.lower() in each_object_inside.lower():
                        object_inside=True
                        break
        return object_inside
       
    # Check if an element is open or closed
    def check_object_open(self, object_type):
        event = self.refresh()        
        for each in event.metadata["objects"]:
            if each["objectType"].lower()==object_type.lower():
                return each["isOpen"]
        return False

    # Look down
    def look_down(self):
        event=self.controller.step(dict(action='LookDown'))

    # Look up
    def look_up(self):
        event=self.controller.step(dict(action='LookUp'))

    # Regexp to use known_data
    def interpret_variable(self, what):
        if "$" in str(what):
            value = re.sub("\$\{id_([^\}]+)\}",r'\g<1>', what)
            value = value.lower()
            OBJECT_DATA = self.known_info["OBJECT_DATA"]
            object_info = OBJECT_DATA.get(value.replace("id_",""),{})        
            return object_info        
        return what

    # Interpret different skills
    # this is used to "translate" between our skills and the simulator actions
    def interpret_skill(self, each_task, step_by_step):
        controller = self.controller

        if each_task.get("LOCATION",""):
            if self.current_location!=each_task.get("LOCATION",""):
                print ("FIRST NEED TO MOVE TO SKILL LOCATION...")
                self.teleport_to(each_task.get("LOCATION","").replace("_location",""))

        #"location: fridge_location"

        if each_task["SKILL"] == "MoveRobot":
            print ("*")
            location = each_task["PARAMETERS"]["location"]
            location_name = location.split("_")[0]
            self.teleport_to(location_name)

        elif each_task["SKILL"] == "MoveHeldObjectAhead":
            controller.step(action="MoveHeldObjectAhead", moveMagnitude=each_task["PARAMETERS"].get("moveMagnitude",0.3) )
        
        elif each_task["SKILL"] == "MoveRight":
            print ("->")
            if each_task["PARAMETERS"].get("steps",""):
                for each_step in range(each_task["PARAMETERS"].get("steps","")):
                    event=controller.step("MoveRight")        
                    if "blocking" in event.metadata["errorMessage"] and  "from moving" in event.metadata["errorMessage"]:
                        return {"collision": True}
            else:
                event=controller.step("MoveRight")        
                if "blocking" in event.metadata["errorMessage"] and  "from moving" in event.metadata["errorMessage"]:
                        return {"collision": True}
            return {"collision": False}
        elif each_task["SKILL"] == "MoveLeft":
            print ("<-")
            if each_task["PARAMETERS"].get("steps",""):
                for each_step in range(each_task["PARAMETERS"].get("steps","")):
                    event=controller.step("MoveLeft")        
                    if "blocking" in event.metadata["errorMessage"] and  "from moving" in event.metadata["errorMessage"]:
                        return {"collision": True}                    
            else:            
                event=controller.step("MoveLeft")       
                if "blocking" in event.metadata["errorMessage"] and  "from moving" in event.metadata["errorMessage"]:
                    return {"collision": True}                
            return {"collision": False}
                       
        elif each_task["SKILL"] == "MoveBack":
            print (".")
            if each_task["PARAMETERS"].get("steps",""):
                for each_step in range(each_task["PARAMETERS"].get("steps","")):
                    event=controller.step("MoveBack")        
                    if "blocking" in event.metadata["errorMessage"] and  "from moving" in event.metadata["errorMessage"]:
                        return {"collision": True}                    
            else:                           
                event=controller.step("MoveBack")       
                if "blocking" in event.metadata["errorMessage"] and  "from moving" in event.metadata["errorMessage"]:
                    return {"collision": True}                
            return {"collision": False}
        elif each_task["SKILL"] == "MoveAhead":
            print ("^")
            if each_task["PARAMETERS"].get("steps",""):
                for each_step in range(each_task["PARAMETERS"].get("steps","")):
                    event=controller.step("MoveAhead")        
                    if "blocking" in event.metadata["errorMessage"] and  "from moving" in event.metadata["errorMessage"]:
                        return {"collision": True}                                    
            else:                
                event=controller.step("MoveAhead")       
                if "blocking" in event.metadata["errorMessage"] and  "from moving" in event.metadata["errorMessage"]:
                    return {"collision": True}                                
            return {"collision": False}

        elif each_task["SKILL"] == "RotateRight":
            controller.step("RotateRight", degrees=self.interpret_variable(each_task["PARAMETERS"]["degrees"]))

        elif each_task["SKILL"] == "SEQUENCE":
            for each_time in range(each_task["PARAMETERS"].get("REPEAT_TIMES",1)):
                for each_subtask in each_task["PARAMETERS"]["CHILDREN"]:
                    self.interpret_skill(each_subtask, step_by_step)

        elif each_task["SKILL"] == "SliceObject":
            event=controller.step(
                action="SliceObject",
                objectId=self.interpret_variable(each_task["PARAMETERS"]["objectId"])["object_id"],#"Fridge|+00.97|+00.00|+01.25",
                forceAction=False
            )     
            print(event  )

        elif each_task["SKILL"] == "OpenObject":
            event=controller.step(
                action="OpenObject",
                objectId=self.interpret_variable(each_task["PARAMETERS"]["objectId"])["object_id"],#"Fridge|+00.97|+00.00|+01.25",
                forceAction=False
            )     
            print (event)  

        elif each_task["SKILL"] == "CloseObject":
            controller.step(
                action="CloseObject",
                objectId=self.interpret_variable(each_task["PARAMETERS"]["objectId"])["object_id"],#"Fridge|+00.97|+00.00|+01.25",
                forceAction=False
            )            

        elif each_task["SKILL"] == "Wait":            
            
            print ("...WAITING...")    

        elif each_task["SKILL"] == "PickupObject":
            self.object_in_hand=self.interpret_variable(each_task["PARAMETERS"]["objectId"])
            event=controller.step(
                action="PickupObject",
                objectId=self.interpret_variable(each_task["PARAMETERS"]["objectId"])["object_id"],#"Fridge|+00.97|+00.00|+01.25",
                forceAction=False
            )     
            print (event)       

        elif each_task["SKILL"] == "DropHandObject":
            # Update object position
            if (self.object_in_hand["name"]):
                self.update_object_location(self.object_in_hand["name"])

                controller.step(
                    action="DropHandObject",
                    forceAction=False
                )            
            self.object_in_hand=None

        elif each_task["SKILL"] == "PutObject":
            
            # Update object position
            if self.object_in_hand["name"]:
                self.update_object_location(self.object_in_hand["name"])

            controller.step(action="MoveHeldObjectAhead", moveMagnitude=0.55 )

            event=controller.step(
                action="PutObject",
                objectId=self.interpret_variable(each_task["PARAMETERS"]["objectId"])["object_id"],#"Fridge|+00.97|+00.00|+01.25",
            )     

            event=controller.step(
                action="DropHandObject"
            )     
            
            print (event)       
            self.object_in_hand=None


        elif each_task["SKILL"] == "TurnOn":
            event=controller.step(
                action="ToggleObjectOn",
                objectId=self.interpret_variable(each_task["PARAMETERS"]["objectId"])["object_id"],#"Fridge|+00.97|+00.00|+01.25",
                forceAction=False
            )
            print (event)

        elif each_task["SKILL"] == "TurnOff":
            controller.step(
                action="ToggleObjectOff",
                objectId=self.interpret_variable(each_task["PARAMETERS"]["objectId"])["object_id"],#"Fridge|+00.97|+00.00|+01.25",
                forceAction=False
            )            

        elif each_task["SKILL"] == "Watch":
            event=self.refresh()
            cv2_image = event.cv2image()
        
        else:
            print ("UNKNOWN ACTION!!!!")
            sys.exit(1)

        self.refresh()
        time.sleep(1)

    # Execute state machine
    def execute(self, step_by_step=True):
        machine_json = self.machine_json
        controller = self.controller
        self.refresh()
        time.sleep(0)

        for each_task in machine_json["TASKS"]:
            ## -------------------
            self.refresh()
            time.sleep(0.5)
            if step_by_step:
                print ("GOING TO EXECUTE:--------------")
                print (each_task)
                event=self.refresh()
                user_input=input("\nPress 'enter' to continue, or 'q' to exit:: ")
                if user_input=="q":
                    break
            else:
                print (each_task)

            self.interpret_skill(each_task, step_by_step)       

            

            

