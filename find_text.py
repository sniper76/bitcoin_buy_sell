import re

def find_last_row_uuid_and_state(file_path):
    # 로그 파일 설정
    with open(file_path, 'r') as file:
        # Read all lines from the file
        lines = file.readlines()

        if not lines:
            return None  # If file is empty, return None

        last_line = lines[-1].strip()

        # Use regex to extract UUID and state
        uuid_match = re.search(r"'uuid': '([A-Z0-9]+)'", last_line)
        state_match = re.search(r"'state': '(\w+)'", last_line)
        side_match = re.search(r"'side': '(\w+)'", last_line)
        created_at_match = re.search(r"'created_at': '([\d\-T:+]+)'", last_line)

        if uuid_match and state_match:
            return {
                "uuid": uuid_match.group(1),  # Extracted UUID
                "state": state_match.group(1),  # Extracted state
                "side": side_match.group(1),  # Extracted side
                "created_at": created_at_match.group(1)  # Extracted created_at
            }
        return None  # Return None if no "ask" side is found
