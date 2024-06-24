<p align="center">
  <img src="images/yosemite_entrance.png" alt="Yosemite Peak Reservation Checker Logo" width="400">
</p>

## Yosemite Park Ticketed Entry Availability Checker

This project checks the availability of Yosemite peak reservations on specific dates and sends notifications via Pushover if reservations are available. The code is designed to be deployed using Firebase Functions and requires a Pushover account for push notifications.

### Prerequisites

1. **Firebase CLI**: Make sure you have the Firebase CLI installed. You can install it by following the instructions [here](https://firebase.google.com/docs/cli)

2. **Pushover Account**: Create a [Pushover](https://pushover.net/) account and obtain your User Key and Application Token. Make sure to install the mobile app and sign in so you can recieve the push notifications.

3. **Firebase Project**: Create a Firebase project and set up Firebase Functions. You will need to upgrade the project to blaze to utilize functions, however the cost should be minimal.

### Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/emerysilb/yosemite_entry_checker
   cd yosemite_entry_checker
   ```

2. **Initialize Firebase in your project directory**:

   ```bash
   firebase init
   ```

3. **Replace the Pushover credentials**:

   - Open the code file and replace the `PUSHOVER_USER_KEY` and `PUSHOVER_APP_TOKEN` with your Pushover user key and application token, respectively.

4. **Specify the dates to check**:
   - In the code, update the `specific_dates` variable with the dates you want to check in `YYYY-MM-DD` format.

### Deployment

1. **Deploy the Firebase Functions**:

   ```bash
   firebase deploy --only functions
   ```

2. **Set up a schedule for the function**:
   - The function is set to run every minute by default. You can modify the schedule in the `@scheduler_fn.on_schedule(schedule="* * * * *")` decorator if needed.

### Usage

The function `fetch_availability_data` will run according to the specified schedule and check the availability of Yosemite peak reservations for the dates specified in the `specific_dates` variable. If any of the dates have available reservations, a Pushover notification will be sent to your account.

#### Turn off service

Since the function doesn't have a set end, it will continue to run and you will be charged for the functions running. The easiest way to turn off the service would be to go into the project through the [console](https://console.firebase.google.com/u/0/) and go to functions then just delete the function.

### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
