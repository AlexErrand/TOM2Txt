import tkinter as tk
from tkinter import filedialog
from bs4 import BeautifulSoup

def extract_unique_pairings(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    tables = soup.find_all('table', class_='report')
    pairings = []
    seen_tables = set()  # A set to keep track of table numbers we've already added

    for table in tables:
        rows = table.find_all('tr')[1:]  # Skip the header row
        for row in rows:
            cells = row.find_all('td')
            # Check if row has enough cells with player data
            if len(cells) == 4:
                table_number = cells[0].get_text(strip=True)
                # If we've already processed this table number, skip it
                if table_number in seen_tables:
                    continue
                seen_tables.add(table_number)
                
                player1_data = cells[1].get_text(strip=True)
                player2_data = cells[3].get_text(strip=True)
                # Extract the player's name and record, excluding match points
                player1 = ' '.join(player1_data.split(' ')[:-1]).rsplit(' (', 1)[0] + ')'
                player2 = ' '.join(player2_data.split(' ')[:-1]).rsplit(' (', 1)[0] + ')'
                pairing = f"{player1} vs. {player2}"
                pairings.append(pairing)

    # Join all pairings into one line of text, separated by a comma
    return ', '.join(pairings)

def select_input_file():
    file_path = filedialog.askopenfilename(filetypes=[("HTML files", "*.html"), ("All files", "*.*")])
    if file_path:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, file_path)

def select_output_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, folder_path)

def process_files():
    input_file_path = input_entry.get()
    output_folder_path = output_entry.get()
    output_file_path = f"{output_folder_path}/pairings_output.txt"  # Define your output filename
    
    with open(input_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    formatted_unique_pairings = extract_unique_pairings(html_content)
    
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(formatted_unique_pairings)
    
    status_label.config(text="Pairings have been written to the output file.")

# Set up the main application window
root = tk.Tk()
root.title("Pairings Extractor")

# Create a frame for the input file selection
input_frame = tk.Frame(root)
input_frame.pack(padx=10, pady=5)
input_label = tk.Label(input_frame, text="Input HTML File:")
input_label.pack(side=tk.LEFT)
input_entry = tk.Entry(input_frame, width=50)
input_entry.pack(side=tk.LEFT, padx=5)
input_button = tk.Button(input_frame, text="Browse", command=select_input_file)
input_button.pack(side=tk.LEFT)

# Create a frame for the output folder selection
output_frame = tk.Frame(root)
output_frame.pack(padx=10, pady=5)
output_label = tk.Label(output_frame, text="Output Folder:")
output_label.pack(side=tk.LEFT)
output_entry = tk.Entry(output_frame, width=50)
output_entry.pack(side=tk.LEFT, padx=5)
output_button = tk.Button(output_frame, text="Browse", command=select_output_folder)
output_button.pack(side=tk.LEFT)

# Create a frame for the process button
process_frame = tk.Frame(root)
process_frame.pack(padx=10, pady=10)
process_button = tk.Button(process_frame, text="Process Files", command=process_files)
process_button.pack()

# Status label
status_label = tk.Label(root, text="", relief=tk.SUNKEN, anchor=tk.W)
status_label.pack(fill=tk.X, padx=10, pady=5)

root.mainloop()