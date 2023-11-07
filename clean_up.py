import os, sys

def clear_folder(folder=".", ignore_folder=["venv", ".git"]):
    for obj in os.listdir(folder):
        if os.path.isdir(os.path.join(folder, obj)) and ("__pycache__" in obj
                        or ".pytest_cache" in obj) or("__pycache__" in folder
                        or ".pytest_cache" in folder) and not True in [ignore in os.path.join(folder, obj) for ignore in ignore_folder]:
            for anything in os.listdir(os.path.join(folder, obj)):
                if not os.path.isdir(os.path.join(folder, obj, anything)):
                    print("Deleting File:", os.path.join(folder, obj, anything))
                    os.remove(os.path.join(folder, obj, anything))
                    print("Deleted File:", os.path.join(folder, obj, anything))
                else:
                    # print("recursively:", folder, obj, anything)
                    clear_folder(os.path.join(folder, obj, anything))
            # print("Deleting Folder:", os.path.join(folder, obj))
            os.removedirs(os.path.join(folder, obj))
            print("Deleted Folder:", os.path.join(folder, obj))
        elif os.path.isdir(os.path.join(folder, obj))  and not True in [ignore in os.path.join(folder, obj) for ignore in ignore_folder]:
            # print("recursive call:", folder, obj)
            clear_folder(os.path.join(folder, obj))
        # else:
            # print("ignoring:", folder, obj)

if len(sys.argv) > 2:
    clear_folder(sys.argv[1], sys.argv[2:])
elif len(sys.argv) > 1:
    clear_folder(sys.argv[1])
else:
    clear_folder()