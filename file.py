filename = "file.txt"


def add_id(user_id):
    status = True
    with open(filename, "r+") as f:
        for x in f.readlines():
            print(x.strip())
            if x.strip() in str(user_id):
                status = False
                break
        if status:
            f.write(str(user_id))


add_id(1231)