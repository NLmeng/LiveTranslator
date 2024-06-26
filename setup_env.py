import os
import platform
import shutil

def setup_environment():
    system = platform.system()
    if system == "Darwin":
        pipfile_source = "Pipfile.mac"
    elif system == "Windows":
        pipfile_source = "Pipfile.win"
    else:
        raise OSError("Unsupported operating system")

    pipfile_destination = "Pipfile"
    shutil.copyfile(pipfile_source, pipfile_destination)
    print(f"Using {pipfile_source} as the Pipfile.")

if __name__ == "__main__":
    setup_environment()
