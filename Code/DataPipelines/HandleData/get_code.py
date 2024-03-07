from datasets import load_dataset
import os
import shutil
from pathlib import Path
import threading

# Define embedded systems keywords
embedded_keywords = [
    "#include <avr/io.h>",  # AVR microcontroller programming
    "#include <stm32f4xx.h>",  # STM32F4 series microcontroller programming
    "DDRB",  # AVR programming Data Direction Register
    "RCC_AHB1PeriphClockCmd",  # STM32 programming Clock enable function
    "HAL_GPIO_WritePin",  # STM32 HAL library GPIO function
    "ISR",  # Interrupt Service Routine, common in embedded systems
    "__attribute__((interrupt))",  # GCC attribute for interrupt handlers
    "void setup()",  # Arduino setup function
    "void loop()",  # Arduino main loop function
]

# Function to check if code is related to embedded systems
def is_embedded_code(code):
    return any(keyword in code for keyword in embedded_keywords)

# Generator function to filter embedded code
def get_embedded_code_stream(dataset_stream):
    for item in dataset_stream:
        code = item["code"]
        if is_embedded_code(code):
            yield code

# Load the dataset
ds = load_dataset("codeparrot/github-code", streaming=True, split="train", languages=["C"])

# Function to move files in a separate thread
def move_files(src_directory, target_directory, file_prefix, start_index, end_index):
    for idx in range(start_index, end_index + 1):
        src_filename = src_directory / f"{file_prefix}{idx}.txt"
        target_filename = target_directory / f"{file_prefix}{idx}.txt"
        if src_filename.exists():
            shutil.move(src_filename, target_filename)
    print(f"Moved files {start_index} to {end_index} to {target_directory}")

# Function to save code to files and initiate file moving
def save_embedded_code_to_file(embedded_code_stream, output_dir, file_prefix="embedded_code_"):
    target_dir = Path("D:/1GenAI/out-c")
    os.makedirs(target_dir, exist_ok=True)

    def check_and_move_files(idx):
        if idx % 1000 == 0 and idx > 0:  # Every 1000 files, initiate moving in a separate thread
            start_index = idx - 999
            end_index = idx
            threading.Thread(target=move_files, args=(output_dir, target_dir, file_prefix, start_index, end_index)).start()

    for idx, code in enumerate(embedded_code_stream, start=1):
        filename = output_dir / f"{file_prefix}{idx}.txt"
        with open(filename, "w", encoding='utf-8') as file:
            file.write(code)
        if idx % 100 == 0:
            print(f"Processed {idx} files.")  # Print a message every 100 files
        check_and_move_files(idx)

# Define the output directory
output_dir = Path("./out-c")
os.makedirs(output_dir, exist_ok=True)

# Assuming embedded_code_stream is a generator from the previous steps
embedded_code_stream = get_embedded_code_stream(ds)
save_embedded_code_to_file(embedded_code_stream, output_dir)
