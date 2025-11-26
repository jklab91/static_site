import shutil, os

#Thiis is a test

from generate_page import generate_page


SOURCE_DIR = "static/"
DEST_DIR = "public/"
PORT = 8888

def main():
    copy_src_to_public(SOURCE_DIR, DEST_DIR, True)

    generate_page("content/index.md", "template.html", dest_path=f'{DEST_DIR}index.html')


def copy_src_to_public(source_dir: str, destination_dir: str, clean_dir: bool):
    if clean_dir:
        if os.path.exists(destination_dir):
            shutil.rmtree(path=DEST_DIR)
            os.mkdir(path=DEST_DIR)

        else:
            os.mkdir(path=DEST_DIR)


    #get contents
    disc_dirs = os.listdir(source_dir)
    child_paths = []
    #iterate over list files/dirs
    for item in disc_dirs:
        if item.startswith("."):
            pass
        else:
            is_file = os.path.isfile(f"{source_dir}/{item}")
            if is_file:
                src_path = f"{source_dir}{item}"
                dest_path = f"{destination_dir}{item}"
                shutil.copy(src_path, dest_path)
            elif not is_file:
                target_dir = f"{destination_dir}{item}"
                existing_dir = f"{source_dir}{item}"
                try:
                    os.mkdir(target_dir)
                except FileExistsError:
                    print(f"Directory '{target_dir}' already exists.")
                except OSError as e:
                    print(f"Error creating directory: {e}")

                child_paths.append(f"{existing_dir}/")

    if child_paths:
        for path in range(len(child_paths)):
            formatted = child_paths[path].split("/")
            copy_src_to_public(f"{child_paths[path]}/", f"{destination_dir}{formatted[-2]}/", clean_dir=False)











if __name__ == "__main__":
    main()
