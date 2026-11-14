# Document Manager Microservice

## Description
The Document Manager microservice is a headless background process that monitors an input directory for command request files (`.txt`). It provides file-based text processing services, allowing client programs to programmatically **WRITE** raw code snippets/text into formatted output documents or **READ** existing target text files and retrieve their contents without direct code coupling.

---

## 1. How to REQUEST & RECEIVE Data
Client programs communicate with the Document Manager by creating and dropping a structured text file into the monitored `input_docs/` folder.

### File Formats:
* **WRITE Operation:** Line 1 must be `WRITE`, Line 2 must be the destination filename (EX: `generated_code.txt`), and Line 3 onwards is the text/code payload.
* **READ Operation:** Line 1 must be `READ`, and Line 2 must be the path to the target file you want to read.

### Request Data Example:
```python
import os

# Define the input directory monitored by the microservice
INPUT_FOLDER = "input_docs"
request_filename = os.path.join(INPUT_FOLDER, "req_write_01.txt")

# Construct the payload according to the communication contract
code_payload = """WRITE
my_exported_code.txt
def add_numbers(a, b):
    return a + b
"""

# Programmatically drop the request file into the input pipe
with open(request_filename, "w", encoding="utf-8") as f:
    f.write(code_payload)
```

## RECEIVE Data Example
```python
import os
import time

OUTPUT_FOLDER = "output_docs"
expected_output = os.path.join(OUTPUT_FOLDER, "my_exported_code.txt")

# Wait briefly for processing, then check output directory
time.sleep(1)

if os.path.exists(expected_output):
    with open(expected_output, "r", encoding="utf-8") as f:
        file_data = f.read()
    print(f"Received data from microservice:\n{file_data}")
else:
    print("Pending response...")
```
## 2: UML Sequence Diagram

```text

[Client Program]                       [File System / Folders]                [Document Manager Microservice]
      |                                           |                                           |
      |--- 1. Write request file (.txt) --------->|                                           |
      |    (into input_docs/)                     |                                           |
      |                                           |--- 2. Poll & detect request file -------->|
      |                                           |                                           |-- 3. Parse operation (READ/WRITE)
      |                                           |                                           |-- 4. Execute file read/write
      |                                           |<-- 5. Save result file (into output_docs)-|
      |                                           |<-- 6. Move request file (to archive_docs)-|
      |                                           |                                           |
      |--- 7. Poll & read result file ----------->|                                           |
      |    (from output_docs/)                    |                                           |
      |<-  8. Receive retrieved data -------------|                                           |
```
