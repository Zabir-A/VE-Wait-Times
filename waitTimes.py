import requests
import datetime


# Example of data:

# 0:
#     id:	"cltti49d20wprt64ukhaw635q"
#     locationId:	"clp033k9o0000qo413bjy9a91"
#     createdAt:	"2024-03-16T03:01:24.708Z"
#     reportId:	"cltti49d00wopt64uj80vcbet"
#     waitTimeMinutes:	375
#     elosMinutes:	434
#     status:	"normal"
#     location:
#         slug:	"VGH"
#         name:	"Vancouver General Hospital"

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

                # is else necessary?
                else:
                    hours = wait_time_minutes // 60
                    minutes = wait_time_minutes % 60
                    wait_time_str = f"{hours} hours and {minutes} minutes"

            # is else necessary?
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

        # return location, formatted wait time
        return waitTimes

    except requests.RequestException as e:
        print("Error fetching wait times:", e)
        return []


def displayWaitTimes(waitTimes):
    """Displays / prints wait times for all locations."""
    for wait_time in waitTimes:
        print(f"{wait_time['Location']}\nWait time: {wait_time['FormattedWaitTime']}\n")
    print("Last updated:", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


def main():
    """Main function to run the script."""
    waitTimes = getWaitTimes()
    displayWaitTimes(waitTimes)

    # DEBUGGING
    # number of locations
    # print(f"Number of locations: {len(waitTimes)}")


if __name__ == "__main__":
    main()
