from pathlib import Path
import time

BASE_DIR = Path(__file__).resolve().parent
INPUT_FOLDER = BASE_DIR / "input_docs"
OUTPUT_FOLDER = BASE_DIR / "output_docs"
ARCHIVE_FOLDER = BASE_DIR / "archive_docs"

# source file to read
source_file = BASE_DIR / "sample_read.txt"

# request and response filenames
request_name = "test_program_read.txt"
request_path = INPUT_FOLDER / request_name
output_path = OUTPUT_FOLDER / f"read_result_{request_name}"
archived_request = ARCHIVE_FOLDER / request_name

# make sure the source file exists
if not source_file.exists():
    print("TEST FAILED: sample_read.txt was not found.")
    raise SystemExit

# remove leftovers from an earlier run
output_path.unlink(missing_ok=True)
archived_request.unlink(missing_ok=True)

# save the expected contents
expected_content = source_file.read_text(encoding="utf-8")

# send a READ request to the microservice
request_text = f"READ\n{source_file}\n"
request_path.write_text(request_text, encoding="utf-8")

print("READ request sent to Document Manager.")
print("Waiting for the microservice response...")

# wait for the microservice to create the output file
for attempt in range(15):
    if output_path.exists():
        response = output_path.read_text(encoding="utf-8")

        print("\nResponse received:")
        print(response)

        if response == expected_content:
            print("TEST PASSED: Received content matches the source file.")
        else:
            print("TEST FAILED: Received content does not match.")
        break

    time.sleep(1)
else:
    print("TEST FAILED: No response received within 15 seconds.")