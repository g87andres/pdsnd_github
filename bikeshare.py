import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = {
    1: 'january',
    2: 'february',
    3: 'march',
    4: 'april',
    5: 'may',
    6: 'june',
    7: 'july',
    8: 'august',
    9: 'september',
    10: 'october',
    11: 'november',
    12: 'december'
}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    
    while True:
        city = input("Which city do you want to analyze? Your options are Chicago, New York City, or Washington\n").lower()
        if city in ('chicago', 'new york city', 'washington'):
            break            
        else:
            print("Invalid response. Your options are Chicago, New York City, or Washington\n")
            continue


    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Which month do you want to analyze? Your options range from January through June. If you'd like all months, type 'all'\n").lower()
        if month in ('january', 'february', 'march' 'april', 'may', 'june', 'all'):
            break            
        else:
            print("Invalid response.")
            print("Which month do you want to analyze? Your options range from January through June. If you'd like all months, type 'all'\n")
            continue


    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Which day do you want to analyze? If you'd like all days, type 'all'\n").lower()
        if day in ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all'):
            break            
        else:
            print("Invalid response.")
            print("Which day do you want to analyze? If you'd like all days, type 'all'\n")
            continue

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime so that we can use the dt method
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # create a month column
    df['Start Time_month'] = df['Start Time'].dt.month

    # create a date column
    df['Start Time_day'] = df['Start Time'].dt.day_name()

    # apply month filter
    if month != 'all':
        df = df[df['Start Time_month'] == ['january', 'february', 'march', 'april', 'may', 'june'].index(month)+1]

    # apply day filter. convert the lower() string for day into proper case
    if day != 'all':
        df = df[df['Start Time_day'] == day.title()]

    #print(df.head())

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("The most common month is: " + MONTHS[df['Start Time_month'].mode()[0]].title())

    # display the most common day of week
    print("The most common day of the week is: " + format(df['Start Time_day'].mode()[0]))


    # display the most common start hour
    print("The most common start hour is: " + format(df['Start Time'].dt.hour.mode()[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("The most commonly used start station is: " + format(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print("The most commonly used end station is: " + format(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    station_concat = df.groupby(['Start Station', 'End Station']).size().reset_index(name='Station Concat')
    station_concat = station_concat.sort_values(by='Station Concat', ascending=False).reset_index(drop=True).head(1)
    print("The most frequent combination of start/end stations is: " + station_concat['Start Station'][0] + " and " + station_concat['End Station'][0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_seconds = df['Trip Duration'].sum()
    days = int(total_seconds / (24 * 3600))
    total_seconds = int(total_seconds % (24 * 3600)) # get the remainder after days
    hours = int(total_seconds / 3600)
    total_seconds = int(total_seconds % 3600)
    minutes = int(total_seconds / 60)
    seconds = int(total_seconds % 60)
    print(f"\nThe total travel time was: {days} days, {hours} hours, {minutes} minutes, and {seconds} seconds")

    # display mean travel time
    print("\nThe mean travel time was: " + format(df['Trip Duration'].mean()) + " seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("\nUser Type counts are:\n")
    user_types = df.groupby('User Type').size().reset_index(name='Count')
    print(user_types)

    # Display counts of gender
    # Washington doesnt have gender counts, so we need to capture the exception 
    print("\nGender counts are:\n")
    try:
        gender_counts = df.groupby('Gender').size().reset_index(name='Count')
        print(gender_counts)

        # Display earliest, most recent, and most common year of birth
        print("\nThe earliest birth year is: " + format(int(df['Birth Year'].min())))
        print("\nThe most recent birth year is: " + format(int(df['Birth Year'].max())))
        print("\nThe most common birth year is: " + format(int(df['Birth Year'].mode()[0])))

    except Exception:
        print("There are no gender counts for this market")

    


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """Display raw data if the user wants to see sample data"""

    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
    start_loc = 0
    while True:
        if view_data.lower() != 'yes':
            break
        print(df.iloc[start_loc:start_loc+5])
        start_loc += 5
        view_data = input("Do you wish to continue?: ").lower()

def main():
    while True:
        #city, month, day = get_filters()
        city, month, day = 'chicago', 'all', 'all'
        df = load_data(city, month, day)
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
        break


if __name__ == "__main__":
	main()
