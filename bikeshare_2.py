import time
import pandas as pd
import numpy as np

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

# Lists for month and day to check user input validity
month_list = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
weekday_list = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']

# Function to validate user input
def check_user_input(user_input, input_type):
    while True:
        input_user_entered = input(user_input).lower()
        try:
            if input_user_entered in ['chicago', 'new york city', 'washington'] and input_type == 'c':
                break
            elif input_user_entered in month_list and input_type == 'm':
                break
            elif input_user_entered in weekday_list and input_type == 'd':
                break
            else:
                if input_type == 'c':
                    print("Invalid Input!, input must be: chicago, new york city, or washington")
                if input_type == 'm':
                    print("Invalid Input!, input must be: january, february, march, april, may, june or all")
                if input_type == 'd':
                    print("Invalid Input!, input must be: sunday, ... friday, saturday or all")
        except ValueError:
            print("Sorry, your input is wrong")
    return input_user_entered

def get_filters():
    print('Hello! Let\'s explore some US bikeshare data!')

    # Get user input for city (chicago, new york city, washington), and check user input validity
    city = check_user_input("Would you like to see the data for chicago, new york city or washington?\n", 'c')

    # Get user input for month (all, january, february, ... , june), and check user input validity
    month = check_user_input("For filtering data by specific month, please enter a month name from (january, february, march, april, may, june) otherwise enter 'all'\n", 'm')

    # Get user input for day of the week (all, sunday, monday, ... saturday), and check user input validity
    day = check_user_input("For filtering data by specific day, please enter a day name from (sunday, monday, tuesday, wednesday, thursday, friday, saturday) otherwise enter 'all'\n", 'd')

    print('-' * 40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of the week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Load data file into a DataFrame
    df = pd.read_csv(CITY_DATA[city])

    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month, day of week, and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.strftime('%A')  # Use strftime to get the weekday name
    df['hour'] = df['Start Time'].dt.hour

    # Filter by month if applicable
    if month != 'all':
        # Use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # Filter by month to create the new DataFrame
        df = df[df['month'] == month]

    # Filter by day of the week if applicable
    if day != 'all':
        # Filter by day of the week to create the new DataFrame
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    most_common_month = df['month'].mode()[0]
    print('Most Common Month is: ', most_common_month)

    # Display the most common day of the week
    most_common_day = df['day_of_week'].mode()[0]
    print('Most Common Day Of The Week is: ', most_common_day)

    # Display the most common start hour
    most_common_hour = df['hour'].mode()[0]
    print('Most Common Start Hour Of The Day is: ', most_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print('Most Common Start Station is: ', most_common_start_station)

    # Display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('Most Common End Station is: ', most_common_end_station)

    # Display most frequent combination of start station and end station trip
    # Here we can't use mode, instead we will use groupby
    # But the result won't be sorted, and for the most frequent combination, we need the result to be in descending order
    combination_group = df.groupby(['Start Station', 'End Station'])
    most_frequent_combination_station = combination_group.size().sort_values(ascending=False).head(1)
    print('Most frequent combination of Start Station and End Station trip is: ', most_frequent_combination_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total Travel Time is: ', total_travel_time)

    # Display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean Travel Time is: ', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('User Types in Data are: ', df['User Type'].value_counts())

    # Check if the columns Gender and Birth Year exist in the DataFrame (not available in Washington data)
    if 'Gender' in df.columns and 'Birth Year' in df.columns:
        # Display counts of gender
        print('Counts Of Gender: ', df['Gender'].value_counts())

        # Display earliest, most recent, and most common year of birth
        earliest_year = df['Birth Year'].min()
        print('Earliest Year is: ', earliest_year)

        most_recent_year = df['Birth Year'].max()
        print('Most Recent Year is: ', most_recent_year)

        most_common_year = df['Birth Year'].mode()[0]
        print('Most Common Year is: ', most_common_year)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

# View raw data to the user
def show_raw_data(df):
    row = 0
    while True:
        view_raw_data = input("Would you like to see the raw data? For 'Yes', enter 'Y', and for 'No', enter 'N'.\n").lower()
        if view_raw_data == "y":
            print(df.iloc[row : row + 6])
            row += 6
        elif view_raw_data == "n":
            break
        else:  # Validate user input
            print("Sorry! You entered the wrong input. Kindly try again!")

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        show_raw_data(df)
        restart = input('\nWould you like to restart? Enter "y" for yes or "n" for no.\n').lower()
        if restart.lower() != 'y':
            break

if __name__ == "__main__":
    main()
