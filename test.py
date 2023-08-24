from config import me

def read():
    print(me["name"])

    if "height" in me:
        print(me["height"])

def modify():
    me["age"] = 41
    print (me)

def create():
    me["preferred_color"] = "green"
    print(me)

def remove():
    me["hobbies"].pop()
    print(me)

#call function
read()
modify()
create()
remove()