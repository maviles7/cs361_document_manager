import os
import time
import shutil # built-in module for file management 

# folders
INPUT_FOLDER = "input_docs"
OUTPUT_FOLDER = "output_docs"
ARCHIVE_FOLDER = "archive_docs"

# create folders (if they don't exist) 
os.makedirs(INPUT_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(ARCHIVE_FOLDER, exist_ok=True)

print("document manager is running...")
print("looking for request files in the input folder...")

# main loop --> keep microservice running 
while True:
    # check files in the input folder
    for filename in os.listdir(INPUT_FOLDER):
        if filename.endswith(".txt"):
            file_path = os.path.join(INPUT_FOLDER, filename)

            # pause - making time to ensure file is finished writting 
            time.sleep(0.1)

            print(f"\nprocessing request file: {filename}")

            try:
                # read the request file 
                with open(file_path, "r", encoding="utf-8") as file:
                    lines = file.readlines()

                if not lines:
                    print(f"error: request file {filename} is empty.")
                    continue

                # parse instruction 
                operation = lines[0].strip().upper() # "READ" or "WRITE"
                print(f"operation: {operation}")

                if operation == "WRITE":
                    # format: 
                    # WRITE
                    # destination_filename.txt
                    # [code content]
                    destination_filename = lines[1].strip()
                    content = "".join(lines[2:]) # rest of the lines = content

                    output_file_path = os.path.join(OUTPUT_FOLDER, destination_filename)

                    # write code content to the output file
                    with open(output_file_path, "w", encoding="utf-8") as output_file:
                        output_file.write(content)

                    print(f"success:code content written to: {output_file_path}")

                elif operation == "READ":
                    # format:
                    # READ
                    # source_filename.txt
                    source_filename = lines[1].strip()

                    if os.path.exists(source_filename):
                        with open(source_filename, "r", encoding="utf-8") as source_file:
                            file_data = source_file.read()

                        # define output file path for read result
                        output_file_path = os.path.join(OUTPUT_FOLDER, f"read_result_{filename}")
                        with open(output_file_path, "w", encoding="utf-8") as output_file:
                            output_file.write(file_data)

                        print(f"success: content read from: {source_filename} & saved to {output_file_path}")

                    else:
                        print(f"error: source file {source_filename} does not exist.")

            except Exception as e:
                print(f"error: failed to process request file {filename}. Exception: {e}")  
            # move processed request file to archive folder - ensure it doesn't run twice
            archive_file_path = os.path.join(ARCHIVE_FOLDER, filename)
            shutil.move(file_path, archive_file_path)
            print(f"request file {filename} moved to archive folder.")

    # wait before checking for new files again
    time.sleep(1)

