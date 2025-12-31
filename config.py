import os
import sys
import platform

## FOR EXECUTABLE
def resource_path(relative_path):
    """
    Finds resources (like library.json) for both the bundled app
    and the dev environment.
    """
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller bundled app base path
        base_path = sys._MEIPASS
    else:
        # Development environment base path
        base_path = os.path.abspath(os.path.dirname(__file__))

    return os.path.join(base_path, relative_path)


def get_writable_data_path(app_name="ScreenReader"):
    """
    Returns the appropriate writable directory for user data based on OS.
    """
    if platform.system() == "Darwin":  # macOS
        # Path: ~/Library/Application Support/ScreenReader/
        return os.path.join(
            os.path.expanduser('~'),
            'Library',
            'Application Support',
            app_name
        )

    # Fallback to the current working directory for dev environment
    return os.path.abspath(os.path.dirname(__file__))

## CONSTANTS
# LIBDIR = resource_path("library")
# LIBPATH = os.path.join(LIBDIR, "library.json")

LIBDIR = get_writable_data_path("ScreenReader")
LIBPATH = os.path.join(LIBDIR, "library.json")

# Always ensure the directory exists before trying to read/write from it
try:
    if not os.path.exists(LIBDIR):
        os.makedirs(LIBDIR, exist_ok=True)
except Exception as e:
    # This block should capture any permission issues if they occur
    print(f"Error creating library directory: {e}")

'''
RUN in terminal:

clear before compiling:
pyinstaller --clean app.py

OR manually delete build folder, dist folder, and .spec file

to compile executable:
pyinstaller \
  --clean \
  --windowed \
  --name ScreenReader \
  --icon icon.icns \
  app.py
.py


Use app.app for MacOS or Linux; .exe for Windows.
'''