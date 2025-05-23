import datetime as dt
from datetime import timedelta
import pandas as pd


class MachineOperation():

    def __init__(self):
        self.today_date = dt.datetime.today()
        self.machines = self.load_json()  # **********uncomment

    def load_json(self):

        try:
            self.machines = pd.read_json("Machine List4.json", orient='index')
            # self.machines.set_index("Machine ID", inplace=True)

        except FileNotFoundError:
            print("File not found. Initialize empty DataFrame")
            self.machines = pd.DataFrame(
                columns=["Machine ID", "Machine name", "Next maintenance date", "Status", "Note"])

        except ValueError:
            print("Invalid JSON format. Initialize empty DataFrame")
            self.machines = pd.DataFrame(
                columns=["Machine ID", "Machine name", "Next maintenance date", "Status", "Note"])

        return self.machines

    def save_to_json(self):

        self.machines.to_json("Machine List4.json", orient="index", indent=4)

    def add_machine(self, machine_name, machine_id):

        next_maintenance_date = (self.today_date + timedelta(weeks=4)).strftime("%Y-%m-%d")

        # Need to change to panda format

        new_row = pd.DataFrame({
            # "Date": today_date.strftime("%Y-%m-%d"),
            # "Machine ID": [machine_id],
            "Machine name": [machine_name],
            "Next maintenance date": [next_maintenance_date],
            "Status": ["New"],
            "Note": [""]
        }, index=[machine_id])

        self.machines = pd.concat([self.machines, new_row])  # , ignore_index=True)
        # self.machines[machine_id] = machine_detail  # add new machine and keep machine ID as key
        self.save_to_json()
        print(f"\nMachine detail: \n {new_row} \n---is saved")
        input("\nPress enter to proceed...")

    def update_machine(self, machine_id):


        # print(self.machines[machine_id])
        try:
            maintenance_progress = input("\nMaintenance finish? Y/N: ").capitalize().strip()

            if maintenance_progress == "Y":
                next_maintenance_date = (self.today_date + timedelta(weeks=4)).strftime("%Y-%m-%d")
                status = f"Maintained"
                note = f"Performed on {self.today_date.strftime("%Y-%m-%d")}"

            elif maintenance_progress == "N":
                next_maintenance_date = (self.today_date + timedelta(days=3)).strftime("%Y-%m-%d")
                status = "Maintenance in progress..."
                note = f"Finish by {next_maintenance_date}"

        except ValueError:
            print("Invalid input. Please input Y for yes and N for No")

        # input the update value in the machine detail

        self.machines.loc[machine_id, ["Next maintenance date", "Status", "Note"]] = [next_maintenance_date, status,
                                                                                      note]

        self.save_to_json()

        print("Machine detail updated.")
        print("------------------------------------------------------------------------------")
        print(self.machines.loc[machine_id])
        print("------------------------------------------------------------------------------")
        input("\nPress enter to proceed...")

    def remove_machine(self, machine_id):

        try:
            print(f"Machine ({machine_id}) details will be removed.")
            delete_machine = input("Confirm to remove the machine? Y/N: ").capitalize()
            if delete_machine == "Y":
                self.machines.drop(index=machine_id, inplace=True)
                self.save_to_json()
                print("--------------------------------------------------------------")
                print(f"Machine ({machine_id}) details has been removed.")
                print("--------------------------------------------------------------")

            elif delete_machine == "N":
                return
        except ValueError:
            print("Invalid input. Please input Y for yes and N for No")

        print("Returning to main menu....")
        input("\nPress enter to proceed...")

    def view_detail(self):

        pd.set_option('display.max_columns', None)
        print(self.machines)

        input("\nPress enter to proceed...")

    def upcoming_maintenance(self):


        self.machines["Next maintenance date"] = pd.to_datetime(self.machines["Next maintenance date"])
        self.machines["Day Remaining"] = (self.machines["Next maintenance date"] - self.today_date).dt.days
        upcoming = self.machines[self.machines["Day Remaining"] < 10]
        # np_date = np.array(maintenance_date)
        print("--------------------------------------------------------------------------")
        print("Machine to be maintained within 10 days:")
        print("--------------------------------------------------------------------------")
        if not upcoming.empty:
            pd.set_option('display.max_columns', None)
            print(upcoming.loc[:, ["Machine name", "Note", "Day Remaining"]])
        else:
            print("None")
        print("--------------------------------------------------------------------------")


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


def repair_id_or_menu(machines, must_exist=True):  # check_machine_id,machines): #********** add

    while True:  # ********** delete.self

        print("Input the Machine ID")
        machine_id_input = input("Machine ID: ").zfill(3)  # Machine ID might be the combination of str and int
        machine_id_input = "MS" + machine_id_input
        exist = machine_id_input in machines.values

        if not must_exist and exist:
            print(f"{machine_id_input} has been registered")

        elif must_exist and not exist:
            print(f"{machine_id_input} is not registered yet")
        else:
            return machine_id_input

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


selection = MachineOperation()
selection.upcoming_maintenance()

while True:

    main_menu()

    try:

        user_input = int(input("\nSelect the number for the operation: "))
        id_list = selection.machines.index

        if user_input == 1:
            machine_id = repair_id_or_menu(id_list, must_exist=False)
            if machine_id is None:
                continue
            # print(machine_id)
            machine_name = input("Machine Name: ").title().strip()
            # print(machine_name)
            selection.add_machine(machine_name, machine_id)

        elif user_input == 2:
            machine_id = repair_id_or_menu(id_list, must_exist=True)
            if machine_id is None:
                continue
            selection.update_machine(machine_id)

        elif user_input == 3:
            machine_id = repair_id_or_menu(id_list, must_exist=True)
            if machine_id is None:
                continue
            selection.remove_machine(machine_id)

        elif user_input == 4:
            selection.view_detail()

        elif user_input == 5:
            selection.upcoming_maintenance()
            input("\nPress enter to proceed...")

        elif user_input == 6:
            print("-----------------------------")
            print("Exit the Program...")
            break
        # elif user_input == 7:
        else:
            print("Invalid input. Please choose a number between 1-6")
    except ValueError:
        print("Invalid input. Please choose a number between 1-6")
