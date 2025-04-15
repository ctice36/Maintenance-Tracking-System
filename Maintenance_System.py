import datetime as dt
from datetime import timedelta
import json

class MachineOperation():

    def __init__(self):
        self.today_date = dt.datetime.today()
        self.machines = self.load_json() #**********uncomment


    def load_json(self):
        #pass
        # check whether
        # 1. the file available or not
        # 2. the file in dictionary form
        try:
            with open("Machine List.json", "r") as file_op:
                #self.machines = json.load(file_op)
                data = json.load(file_op)
                if not isinstance(data, dict):  # make sure the file in dictionary form
                    self.machines =  {}
                else:
                    self.machines = {machine_id: details for machine_id, details in data.items()}

        except (FileNotFoundError, json.JSONDecodeError):
            self.machines =  {}  # If file not found or empty, initialize as an empty dictionary"""

        return self.machines #**********add

    def save_to_json(self):

        with open("Machine List.json", "w") as file_op:
            # date, machine name, machine id, last maintenance date, next maintenance date, status
            json.dump(self.machines, file_op, indent=4)

    def add_machine(self, machine_name, machine_id):

        self.machines = self.load_json()

        # today_date = dt.datetime.today()
        next_maintenance_date = (self.today_date + timedelta(weeks=4)).strftime("%Y-%m-%d")

        machine_detail = {
            #"Date": today_date.strftime("%Y-%m-%d"),
            "Machine name": machine_name,
            "Machine ID": machine_id,
            "Next maintenance date": next_maintenance_date,
            "Status": "New"
        }

        self.machines[machine_id] = machine_detail # add new machine and keep machine ID as key
        self.save_to_json()
        print(f"\nMachine detail {self.machines[machine_id]['Machine ID']}: {self.machines[machine_id]['Machine name']} is saved")
        input("\nPress enter to proceed...")

    def update_machine(self,machine_id):

        self.machines = self.load_json()
        print(self.machines[machine_id])
        try:
            maintenance_progress = input("\nMaintenance finish? Y/N: ").capitalize().strip()

            if maintenance_progress == "Y":
                next_maintenance_date = (self.today_date + timedelta(weeks=4)).strftime("%Y-%m-%d")
                status = f"Maintained"
                note = f"Maintenance performed on {self.today_date.strftime("%Y-%m-%d")}"

            elif maintenance_progress == "N":
                next_maintenance_date = (self.today_date + timedelta(days=3)).strftime("%Y-%m-%d")
                status = "Maintenance in progress."
                note = f"Maintenance must be finish on {next_maintenance_date}"

        except ValueError:
            print("Invalid input. Please input Y for yes and N for No")

        # input the update value in the machine detail

        self.machines[machine_id]["Next maintenance date"] = next_maintenance_date  # add new machine and keep machine ID as key
        self.machines[machine_id]["Status"] = status
        self.machines[machine_id]["Note"] = note

        self.save_to_json()

        print(f"Machine detail updated. {note}")
        input("\nPress enter to proceed...")

    def remove_machine(self,machine_id):
        self.machines = self.load_json()
        try:
            delete_machine = input("Do you really want remove the machine? Y/N: ").capitalize()
            if delete_machine == "Y":
                self.machines.pop(machine_id)
                self.save_to_json()
                print(f"Machine ({machine_id}) details has been removed.")

            elif delete_machine == "N":
                return
        except ValueError:
            print("Invalid input. Please input Y for yes and N for No")

        input("\nPress enter to proceed...")

    def view_detail(self):
        self.machines = self.load_json()
        #print(self.machines) <---- will print out all details in one line
        for machine_id, details in self.machines.items(): # <--- will print multiple line with machine id in line
            print({machine_id: details})

        input("\nPress enter to proceed...")

    def upcoming_maintenance(self):
        self.machines = self.load_json()
        print("The machine(s) needed to be maintained within 10 days:")

        #self.machines = {machine_id: details for machine_id, details in data.items()}
        less_than_10_days = {}
        for machine_id,next_maintenance_date in self.machines.items():
            next_maintenance_date = dt.datetime.strptime(self.machines[machine_id]["Next maintenance date"],"%Y-%m-%d")
            day_count = (next_maintenance_date - self.today_date).days
            if day_count < 10:
                less_than_10_days[machine_id] = f"{self.machines[machine_id]["Machine name"]} = {day_count}"

        if less_than_10_days:
            for machine_id,less_than_10_days in less_than_10_days.items():
                print(f"{machine_id}: {less_than_10_days}")
        else:
            print("None")


        input("\nPress enter to proceed...")

# End of Class_______________________________________________________________________


def main_menu():

    print("\n-----------------------------")
    print("Available operation")
    print("-----------------------------")
    print("1. Add new machine")
    print("2. Update machine upcoming maintenance date")
    print("3. Remove machine")
    print("4. View machine details")
    print("5. View upcoming maintenance date")
    print("6. Exit")
    print("-----------------------------")

def repair_id_or_menu(machines,must_exist=True):# check_machine_id,machines): #********** add

    while True:  # ********** delete.self

        print("Input the Machine ID")
        machine_id = input("Machine ID: ").zfill(3) # Machine ID might be the combination of str and int
        exist = machine_id in machines

        if not must_exist and exist:
            print(f"{machine_id} has been registered")

        elif must_exist and not exist:
            print(f"{machine_id} is not registered yet")
        else:
            return machine_id

        print("\nDo you want to:")
        print("1. Re-input the machine id?")
        print("2. Go back to the main menu?")

        while True:
            try:
                proceed_or_not = int(input("= "))
                if proceed_or_not == 1:
                    break  # to repeat checking machine_id while loop
                elif proceed_or_not == 2:
                    print("Going back to main menu")
                    return None
                else:
                    print("Invalid input. Please choose a number between 1 or 2")
                    continue
            except ValueError:
                print("Invalid input. Please choose a number between 1 or 2")
                continue



while True:

    main_menu()

    try:
        selection = MachineOperation()
        user_input = int(input("\nSelect the number for the operation: "))

        if user_input == 1:
            machine_id = repair_id_or_menu(selection.machines, must_exist=False)
            if machine_id is None:
                continue
            machine_name = input("Machine Name: ").title().strip()
            selection.add_machine(machine_name, machine_id)

        elif user_input == 2:
            machine_id = repair_id_or_menu(selection.machines,must_exist=True)
            if machine_id is None:
                continue
            selection.update_machine(machine_id)

        elif user_input == 3:
            machine_id = repair_id_or_menu(selection.machines,must_exist=True)
            if machine_id is None:
                continue
            selection.remove_machine(machine_id)

        elif user_input == 4:
            selection.view_detail()

        elif user_input == 5:
            selection.upcoming_maintenance()

        elif user_input == 6:
            print("-----------------------------")
            print("Exit the Program...")
            break
        else:
            print("Invalid input. Please choose a number between 1-6")
    except ValueError:
        print("Invalid input. Please choose a number between 1-6")