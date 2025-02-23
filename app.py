import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import subprocess
import urllib.request
import time

# Full path to the 7z executable
SEVEN_ZIP_PATH = r"C:\Program Files\7-Zip\7z.exe"

# Function to download and install 7zip if it's not detected
def download_and_install_7zip():
    # Define the download URL and target installation path
    download_url = "https://7-zip.org/a/7z2409-x64.msi"
    temp_folder = os.path.join(os.getenv('LOCALAPPDATA'), 'Temp')
    temp_msi_path = os.path.join(temp_folder, '7z2409-x64.msi')

    # Create Temp folder if it doesn't exist
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)

    # Download the MSI file
    try:
        urllib.request.urlretrieve(download_url, temp_msi_path)
        # Run the installer silently using msiexec
        subprocess.run(["msiexec", "/qb", "/i", temp_msi_path], check=True)
        messagebox.showinfo("Installation", "7zip has been installed successfully!")
        time.sleep(2)  # Allow time for the installation to complete
    except Exception as e:
        messagebox.showerror("Error", f"Failed to download or install 7zip: {e}")

# Function to check if 7zip is installed
def is_7zip_installed():
    try:
        subprocess.run([SEVEN_ZIP_PATH, "-h"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

# Function to extract the contents of the ISO file using 7zip
def extract_iso():
    iso_file = filedialog.askopenfilename(filetypes=[("ISO files", "*.iso")])
    if iso_file:
        # Get the LocalAppData path and create the "Extracted ISOS" folder if it doesn't exist
        local_app_data = os.getenv('LOCALAPPDATA')
        extracted_folder = os.path.join(local_app_data, "Extracted ISOS")

        if not os.path.exists(extracted_folder):
            os.makedirs(extracted_folder)

        # Create a subfolder in "Extracted ISOS" with the ISO file's name (without extension)
        iso_name = os.path.splitext(os.path.basename(iso_file))[0]
        extraction_path = os.path.join(extracted_folder, iso_name)

        if not os.path.exists(extraction_path):
            os.makedirs(extraction_path)

        # Extract the ISO contents using 7z (7zip)
        try:
            subprocess.run([SEVEN_ZIP_PATH, "x", iso_file, "-o" + extraction_path], check=True)
            messagebox.showinfo("Success", f"ISO extracted successfully to {extraction_path}")
        
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to extract ISO: {e}")
        except FileNotFoundError:
            messagebox.showerror("Error", "7z.exe not found. Downloading and installing 7zip...")
            download_and_install_7zip()

# About window function
def show_about():
    about_window = tk.Toplevel(root)
    about_window.title("About ISO2ZIP")
    about_window.geometry("300x200")
    
    about_label = ttk.Label(about_window, text="ISO2ZIP\nVersion 1.0\n\nCreated by ZohanHaqu", font=("Arial", 12))
    about_label.pack(pady=20)

    ok_button = ttk.Button(about_window, text="OK", command=about_window.destroy)
    ok_button.pack()

# Create the Tkinter window
root = tk.Tk()
root.title("ISO2ZIP")
root.geometry("500x400")

# Set the window icon to icon.ico (in the same directory as the script)
root.iconbitmap('icon.ico')

# Set a custom background color
root.configure(bg="#2C3E50")

# Create a menu bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Add a File menu to the menu bar
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)

# Add Extract ISO option under File menu
file_menu.add_command(label="Extract ISO", command=extract_iso)

# Add About option under File menu
file_menu.add_command(label="About", command=show_about)

# Create a welcome message in the form of a label
welcome_label = ttk.Label(root, text="Welcome to ISO2ZIP!", font=("Arial", 16, "bold"), foreground="white", background="#2C3E50")
welcome_label.pack(pady=20)

# Create a description about the tool
description_label = ttk.Label(root, text="ISO2ZIP allows you to extract contents from ISO files into a custom directory.\n\n"
                                         "Easily access and manage your ISO file contents by extracting them into a clean, organized folder structure.\n\n"
                                         "Select an ISO, extract it, and view its contents.", font=("Arial", 10), foreground="white", background="#2C3E50", wraplength=400)
description_label.pack(pady=10)

# Create a custom window message
window_label = ttk.Label(root, text="Extract ISO contents to a custom folder.", font=("Arial", 10), foreground="white", background="#2C3E50")
window_label.pack(pady=10)

# Check if 7zip is installed on startup
if not is_7zip_installed():
    download_and_install_7zip()

# Run the Tkinter event loop
root.mainloop()
