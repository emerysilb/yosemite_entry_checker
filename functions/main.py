import requests
import json
from collections import defaultdict

from firebase_functions import scheduler_fn
from firebase_admin import initialize_app

initialize_app()

# Specify the dates you want to check in YYYY-MM-DD format
specific_dates = {"2024-06-29", "2024-06-30", "2024-07-10", "2024-07-11"}

API_ENDPOINT = "https://www.recreation.gov/api/timedentry/availability/facility/10086745/monthlyAvailabilitySummaryView"
API_HEADERS = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
}

PUSHOVER_API_ENDPOINT = "https://api.pushover.net/1/messages.json"
PUSHOVER_USER_KEY = ""  # Your Pushover user key
PUSHOVER_APP_TOKEN = ""  # Your Pushover application token


def send_pushover_notification(message):
    pushover_data = {
        "token": PUSHOVER_APP_TOKEN,
        "user": PUSHOVER_USER_KEY,
        "message": message,
    }
    response = requests.post(PUSHOVER_API_ENDPOINT, data=pushover_data)
    response.raise_for_status()


@scheduler_fn.on_schedule(schedule="* * * * *")
def fetch_availability_data(event: scheduler_fn.ScheduledEvent) -> None:
    try:
        # Extract months and years from specific dates
        date_groups = defaultdict(list)
        for date in specific_dates:
            year, month, _ = date.split("-")
            date_groups[f"{year}-{month}"].append(date)

        available_dates = []

        # Fetch data for each month
        for year_month, dates in date_groups.items():
            year, month = year_month.split("-")
            API_PARAMS = {"year": year, "month": month, "inventoryBucket": "FIT"}
            response = requests.get(
                API_ENDPOINT, params=API_PARAMS, headers=API_HEADERS
            )
            response.raise_for_status()  # Raise an exception if the request failed

            data = response.json()

            # Check the returned data against the specified dates
            for date, details in data.get(
                "facility_availability_summary_view_by_local_date", {}
            ).items():
                if date in dates:
                    for tour_id, tour_details in details.get(
                        "tour_availability_summary_view_by_tour_id", {}
                    ).items():
                        if tour_details.get("has_reservable", False) and any(
                            tour_details.get("available_times", [])
                        ):
                            available_dates.append(date)
                            break  # Once we find one available tour, no need to check further tours for this date

        # Send Pushover notification
        if available_dates:
            message = f"""Available dates: {', '.join(available_dates)}
Book at: https://www.recreation.gov/timed-entry/10086745"""
            send_pushover_notification(message)

        return

    except requests.RequestException as e:
        error_message = f"Error fetching data: {e}"
        print(error_message)
        return

    except ValueError as e:
        error_message = f"Error parsing JSON: {e}"
        print(error_message)
        return

    except Exception as e:
        error_message = f"Unexpected error: {e}"
        print(error_message)
        return
