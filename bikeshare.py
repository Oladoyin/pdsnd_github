import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Displays the raw city data upon request by the user.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ''
    while city != 'chicago' and city != 'new york city' and city != 'washington':
        city = (input("would you like to see data for chicago, new york city, or washington ")).lower()

    # get user input for month (all, january, february, ... , june)
    month_day = ''
    month = ''
    day = ''
    raw_data = ''
    while month_day != 'month' and month_day != 'day' and month_day != 'both' and month_day != 'none':
        month_day = (input('would you like to filter the data by "month", "day", or "both". You can also type "none" for no time filter. ')).lower()

    if month_day.lower() == 'both':
        while month != 'january' and month != 'february' and month != 'march' and month != 'april' and month != 'may' and month != 'june':
            month = (input('which month? January, February, March, April, May, or June? ')).lower()
        
        while day != 1 and day != 2 and day != 3 and day != 4 and day != 5 and day != 6 and day != 7:
            day = input('which day? Please, type your response as an integer (e.g., 1=Sunday). ')
            if day.isdigit():
                day = int(day)
    
    elif month_day == 'month':
        while month != 'january' and month != 'february' and month != 'march' and month != 'april' and month != 'may' and month != 'june':
            month = (input('which month? January, February, March, April, May, or June? ')).lower()
    
    elif month_day == 'day':
        while day != 1 and day != 2 and day != 3 and day != 4 and day != 5 and day != 6 and day != 7:
            day = input('which day? Please, type your response as an integer (e.g., 1=Sunday). ')
            if day.isdigit():
                day = int(day)

    elif month_day == 'none':
        pass

    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day (if applicable)
    """
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek

    # filter by month if applicable
    # use the index of the months list to get the corresponding int
    if month != '':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != '': #if filtering data by both day and moth
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    # Define a dictionary to map the integer values to month names
    month_names = {
        1: 'january',
        2: 'february',
        3: 'march',
        4: 'april',
        5: 'may',
        6: 'june'    
    }
    # Use the map() function to convert the 'month' column to strings
    df['month'] = df['month'].map(month_names)
    
    month_mode_result = df['month'].mode()
    if len(month_mode_result) > 0:
        popular_month = df['month'].mode()[0]
    else:
        popular_month = None
    print ("The most common month is", popular_month)

    # display the most common day of week
    weekdays = {
        2: 'monday',
        3: 'tuesday',
        4: 'wednesday',
        5: 'thursday',
        6: 'friday',
        7: 'saturday',
        1: 'sunday'
    }

    df['day_of_week'] = df['day_of_week'].map(weekdays)
    
    day_mode_result = df['day_of_week'].mode()
    if len(day_mode_result) > 0:
        popular_day_of_week = df['day_of_week'].mode()[0]
    else:
        popular_day_of_week = None
    print ("\nThe most common day of the week is", popular_day_of_week)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    hour_mode_result = df['hour'].mode()
    if len(hour_mode_result) > 0:
        popular_start_hour = df['hour'].mode()[0]
    else:
        popular_start_hour = None
    print ("\nThe most common start hour is", popular_start_hour)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station_mode_result = df['Start Station'].mode()
    if len(start_station_mode_result) > 0:
        popular_start_station = df['Start Station'].mode()[0]
    else:
        popular_start_station = None
    print ("The most commonly used start station is", popular_start_station)

    # display most commonly used end station
    end_station_mode_result = df['End Station'].mode()
    if len(end_station_mode_result) > 0:
        popular_end_station = df['End Station'].mode()[0]
    else:
        popular_end_station = None
    print ("\nThe most commonly used end station is", popular_end_station)

    # display most frequent combination of start station and end station trip
    df['start_end_station'] = df['Start Station'] + '/' + df['End Station']
    start_end_station_mode = df['start_end_station'].mode()
    if len(start_end_station_mode) > 0:
        popular_start_end_station_combination = df['start_end_station'].mode()[0]
    else:
        popular_start_end_station_combination = None
    print ("\nThe most frequent combination of start station and end station trip is", popular_start_end_station_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print ("The total travel time is", (df['Trip Duration']/120).sum(), "hours")

    # display mean travel time
    print ("\nThe mean travel time is", df['Trip Duration'].mean()/60, "minutes")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print ("Counts of user types:\n", df['User Type'].value_counts())

    # Display counts of gender
    if 'Gender' in df.columns:
        print ("\nCounts of gender:\n", df['Gender'].value_counts())
    else:
        pass

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print ("\nThe earliest year of birth is", df['Birth Year'].min())
        print ("\nThe most recent year of birth is", df['Birth Year'].max())
        birth_year_mode = df['Birth Year'].mode()
        if len(birth_year_mode) > 0:
            most_common_birth_year = df['Birth Year'].mode()[0]
        else:
            most_common_birth_year = None
        print ("\nThe most common year of birth is", most_common_birth_year)
    else:
        pass


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_datas(city_name):
    raw_data = ''
    while raw_data != 'yes' and raw_data != 'no':
        raw_data = (str(input('would you like to see the first 5 lines of the raw city data? Enter "yes" or "no". '))).lower()
    if raw_data == 'no':
        print ("Goodbye for now!")
        exit()
    else:
        city_info = pd.read_csv(CITY_DATA[city_name])
        old_line = 0
        new_line = 5
        while raw_data == 'yes':
            print(city_info[old_line:new_line])
            old_line += 5
            new_line += 5
            raw_data = ''
            if old_line <= len(city_info):
                while raw_data != 'yes' and raw_data != 'no':
                    raw_data = (str(input('would you like to see the next 5 lines of the raw city data? Enter "yes" or "no". '))).lower()
            else:
                print ("There is no more data to display. Goodbye for now!!")
                exit()
        print ("Goodbye for now!!!")
        exit()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        raw_city_data = ''
        while raw_city_data != 'yes' and raw_city_data != 'no':
            raw_city_data = (input('\nWould you like to see the raw city data? Enter yes or no.\n')).lower()
        if raw_city_data == 'no':
            print ("Goodbye for now!")
            exit()
        city_name = ''
        while city_name != 'chicago' and city_name != 'new york city' and city_name != 'washington':
            city_name = (input("for which city? enter either 'chicago', 'new york city', or 'washington' ")).lower() 
        raw_datas(city_name)

        #restart = input('\nWould you like to restart? Enter yes or no.\n')
        #if restart.lower() != 'yes':
            #break


if __name__ == "__main__":
	main()
