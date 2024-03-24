import requests
import datetime
import time

# Global variable
exit_program = False


# TODO - add url/website to a variable and make dotenv file
# TODO - Test if else variables are necessary
# TODO - Make UI (Optional)
# TODO - Make a function to get the wait time for a specific location & Search for a specific location using REGEX
# TODO - Add Fn to update the wait times x seconds / minutes (running script)


def getWaitTimes():
    """Retrieves wait times from the API."""

    # retrieves only WaitTimeMinutes, elosMinutes, Location, and Status
    url = "https://www.edwaittimes.ca/api/wait-times"
    # Fake user agent to avoid being blocked
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    # timeout to avoid waiting too long for a response
    timeout = 10  # Timeout in seconds

    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
        data = response.json()

        waitTimes = []
        for entry in data:
            location = entry["location"]["name"]
            wait_time_minutes = entry.get("waitTimeMinutes")

            # Retrive wait time only in seconds if less than an hour
            if wait_time_minutes is not None:
                if wait_time_minutes < 60:
                    wait_time_str = f"{wait_time_minutes} minutes"

                else:
                    hours = wait_time_minutes // 60
                    minutes = wait_time_minutes % 60
                    wait_time_str = f"{hours} hours and {minutes} minutes"

            else:
                wait_time_str = "Unknown, please check with hospital"

            waitTimes.append(
                {
                    "Location": location,
                    "WaitTimeMinutes": wait_time_minutes,
                    "FormattedWaitTime": wait_time_str,
                    # "Status": entry["status"],
                }
            )

        return waitTimes

    except requests.RequestException as e:
        print("Error fetching wait times:", e)
        return []


def displayWaitTimes(waitTimes):
    """Displays / prints wait times for all locations."""
    for wait_time in waitTimes:
        print(f"{wait_time['Location']}\nWait time: {wait_time['FormattedWaitTime']}\n")
    print("Last updated:", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S\n"))


def refreshWaitTimes():
    """Refreshes the wait times every 5 minutes."""

    global exit_program

    while not exit_program:
        waitTimes = getWaitTimes()
        displayWaitTimes(waitTimes)
        print("Next update in 5 minutes...\n")

        for _ in range(300):
            if exit_program:
                break
            time.sleep(1)


def main():
    """Main function to run the script."""
    refreshWaitTimes()

    # DEBUGGING
    # number of locations
    # print(f"Number of locations: {len(waitTimes)}")


if __name__ == "__main__":
    main()
