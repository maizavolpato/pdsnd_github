import time
import pandas as pd
import numpy as np
import calendar
import datetime

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

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
    city = input('Would you like to see data for Chicago, New York City or Washington?\n').lower()
    while city not in {"chicago", "new york city", "washington"}:
        city = input("Sorry!Invalid name, try again, please!\n").lower()

    # get user input for month (all, january, february, ... , june)
    filter_month = input("Would like to filter the data by month? (y = yes or n = no)\n")
    if filter_month.lower() == 'y':
        month = input("Which month would you like? (January, February, ..., June)\n")
    else:
        month = 'all'
        print("Selected all months")

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    filter_day = input("Would you like to filter by day of week? (y = yes or n = no)\n")
    if filter_day.lower() == 'y':
        day = input("Which day of week would you like? (Sunday, Monday, Tuesday, ..)\n")
    else:
        day = 'all'
        print("Selected all days of week")

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

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.day_name()

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    popular_month = calendar.month_name[popular_month]
    print('Most Common Month: {}.'.format(popular_month))

    # display the most common day of week
    popular_day = df['day'].mode()[0]
    print('Most Common Day of Week: {}.'.format(popular_day))

    # display the most common start hour
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Common Start Hour: {}.'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print('Most Commonly Used Start Station: {}.'.format(start_station))

    # display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print('Most Commonly Used End Station: {}.'.format(end_station))

    # display most frequent combination of start station and end station trip
    df['combination'] = df['Start Station'] + ' to ' + df['End Station']
    frequent_combination = df['combination'].mode()[0]
    print('Most Frequent combination of Start and End Station: {}.'.format(frequent_combination))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel = int(df['Trip Duration'].sum())
    total_travel = str(datetime.timedelta(seconds = total_travel))
    print('The total travel is {}.'.format(total_travel))

    # display mean travel time
    mean_travel = int(df['Trip Duration'].mean())
    mean_travel = str(datetime.timedelta(seconds = mean_travel))
    print('The average travel is {}.'.format(mean_travel))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_user = df['User Type'].value_counts()
    print("Types of counts:\n {}\n".format(count_user))

    # Display counts of gender
    if 'Gender' in df:
        count_gender = df['Gender'].value_counts()
        print("Counts by gender:\n {}".format(count_gender))
    else:
        print("There is no gender information in the city selected.")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest = df['Birth Year'].min()
        print("\nThe earliest year of birth is: {}.".format(earliest))
        recent = df['Birth Year'].max()
        print("The recent year of birth is: {}.".format(recent))
        common = df['Birth Year'].mode()[0]
        print("The common year of birth is: {}.".format(common))
    else:
        print("There is no birth year information in the city selected.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    show_raw_data = input("Woul you like to see 5 lines of raw data? (y = yes and n = not)\n").lower()
    raw_data = 5
    while show_raw_data != 'n':
        print(df.sample(raw_data))
        while show_raw_data != 'n':
            show_raw_data = input("Woul you like to see more 5 lines of raw data? (y = yes and n = not)\n").lower()
            raw_data += 5
            break
            print(df.sample(raw_data))


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
