import scratchattach as sa
import json
import sys

with open("password.txt", "r") as file:
    password = file.read()
session = sa.Session(password, username="thedavidh")
project_id = "985046953"  # "1049516445"
conn: sa.CloudConnection = session.connect_cloud(project_id)
# events = cloud.events()
events = sa.CloudEvents(project_id)

handled = []


@events.event
def on_set(variable):  # Called when a cloud var is set
    global project_id, conn, handled
    in_var = "in"
    out_var = "out"
    if variable.name == out_var:
        value = str(variable.value)
        print(f"Set the variable {variable.var} to the value {variable.value}")

        with open("data.json", "r") as file:
            users = json.load(file)
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
            if user not in users.keys():
                users[user] = {}
            users[user][column] = data
            conn.set_var(in_var, int("2"))
        elif action == "2":
            i = 1
            user = value[i + 2 : i + 2 + int(value[i : i + 2])]
            i += int(value[i : i + 2]) + 2
            column = value[i + 1 : i + 1 + int(value[i])]
            i += int(value[i]) + 1
            print("User:", user, "Column:", column)
            if str(user) in users.keys() and str(column) in users[user].keys():
                data = users[user][column]
                print("data", data)
                print("setting", in_var, "to", "3" + str(data))
                conn.set_var(in_var, int("2" + str(data)))
            else:
                print("setting", in_var, "to 3")
                print("nothing to do")
                conn.set_var(in_var, int("2"))
        # await conn.set_cloud_variable(out_var, int("3"))
        with open("data.json", "w") as file:
            json.dump(users, file)


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
    while True:
        try:
            events.start()
        except IndexError as e:
            print(e)
            continue


# input("Press enter to stop: ")
# sys.exit()
