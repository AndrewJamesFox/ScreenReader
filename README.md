# ScreenReader

**ScreenReader** is a simple desktop application designed to streamline the process of reading PDF documents and reopening on the last page. It is originally intended to help and promote reading screenplays.

## Features

* **PDF Library Management:** Stores and organizes PDF files locally.
* **Structured Data Storage:** Utilizes a central `library.json` file for structured metadata about all stored documents.
* **Custom Reader UI:** Provides a dedicated interface for selecting and opening files.
* **Simple Configuration:** Easy-to-manage application settings via a `config.py` file.
* **Portable Design:** Designed for simplicity and easy deployment.

## Architecture

The project is structured with a focus on modularity, separating the core application logic from data handling and UI components.

| File | Description |
| :--- | :--- |
| `app.py` | The main application entry point and high-level interaction logic. |
| `reader.py` | Handles the UI and logic for reading/selecting documents. |
| `storage.py` | Manages the file system operations (moving/locating PDFs) and updates to `library.json`. |
| `config.py` | Centralized configuration for file paths and application constants (e.g., `LIBDIR`). |
| `.gitignore` | Defines files and folders (like IDE settings and temporary data) that Git should ignore. |

## Technologies

* **Python:** The core programming language.
* **Tkinter:** Used for the simple, cross-platform graphical user interface (GUI).
* **JSON:** Used for persistent, structured data storage in `library.json`.
* **OS/Shutil:** Used for file system interactions and management.

## Installation & Setup

1.  **Clone the Repository:**
    ```bash
    git clone [Your-Repo-URL]
    cd ScreenReader
    ```
2.  **Install Dependencies:** (If your project uses external libraries, list them here. If it's pure standard library, you can skip or adjust.)
    ```bash
    # Example if you add external libraries later:
    # pip install -r requirements.txt 
    ```
3.  **Run the Application:**
    ```bash
    python app.py
    ```
