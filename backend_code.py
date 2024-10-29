import scratchattach as sa
import json
import sys

import cloud
import os

# print()

with open("password.txt", "r") as file:
    password = file.read()
session = sa.login("thedavidh", os.environ["SCRATCH_PASSWORD"])
project_id = "985046953"  # "1049516445"
conn: sa.BaseCloud = session.connect_scratch_cloud(project_id)
# events = cloud.events()
events = conn.events()

handled = []


@events.event
def on_set(variable):  # Called when a cloud var is set
    global project_id, conn, handled
    in_var = "in"
    out_var = "out"
    if variable.name == out_var:
        value = str(variable.value)
        print(f"Set the variable {variable.var} to the value {variable.value}")
        action = value[0]
        print("Action:", action)
        if action == "1":
            i = 1
            user = value[i + 2 : i + 2 + int(value[i : i + 2])]
            i += int(value[i : i + 2]) + 2
            column = value[i + 1 : i + 1 + int(value[i])]
            i += int(value[i]) + 1
            data = int(value[i:])
            print("User:", user, "Column:", column, "Data:", data)
            cloud.set_slot(str(user), str(column), str(data))
            conn.set_var(in_var, int("2"))
        elif action == "2":
            i = 1
            user = value[i + 2 : i + 2 + int(value[i : i + 2])]
            i += int(value[i : i + 2]) + 2
            column = value[i + 1 : i + 1 + int(value[i])]
            i += int(value[i]) + 1
            print("User:", user, "Column:", column)
            if cloud.user_exists(str(user)) and cloud.slot_exists(
                str(user), str(column)
            ):
                data = cloud.get_slot(str(user), str(column))
                print("data", data)
                print("setting", in_var, "to", "3" + str(data))
                conn.set_var(in_var, int("2" + str(data)))
            else:
                print("setting", in_var, "to 3")
                print("nothing to do")
                conn.set_var(in_var, int("2"))


# @events.event
# def on_del(event):
#     print(f"{event.user} deleted variable {event.var}")


# @events.event
# def on_create(event):
#     print(f"{event.user} created variable {event.var}")


@events.event
def on_ready():
    print("Event listener ready!")


# events.start(
#     update_interval=0.1,
#     thread=False,
# )  # Make sure this is ALWAYS at the bottom of your Python file!
def run():
    # while True:
    #     try:
    events.start()
    # except IndexError as e:
    #     print(e)
    #     continue


# input("Press enter to stop: ")
# sys.exit()
run()
