import time
import json
from order_check import get_order  # Assuming this function exists in api.py

def buy_state_check(uuid):

    #print(f"Checking buy status for UUID: {uuid}")
    # Simulate checking process
    while True:
        time.sleep(10)
        print("Checking status...")
        result = get_order(uuid)
        #print(result)
        if result["state"] == 'done' and result["remaining_volume"] == 0:  # Replace with actual API call
            print(f"Buy completed UUID: {uuid}")

            data = {
                "is_completed": True,
                "buy_price": float(result["buy_price"])
            }
            return data

# Example usage
#if __name__ == "__main__":
#    print(buy_state_check('C0101000002070778601'))