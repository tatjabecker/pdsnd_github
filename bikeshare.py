import time
import datetime
import calendar
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
month_list = list(calendar.month_name)
del month_list[0] #clean up empty key
day_list = list(calendar.day_name)

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle  invalid inputs
    city_list = list(CITY_DATA.keys())
    while True:
        try:
            city = input('Which city are you interested in: Chicago, New York City or Washington?: ').lower()
            if city in city_list:
                break
            else:   
                print('Acceptable inputs: capitalized or lower-case city names(e.g.chicago)')
                continue
             
        except Exception as e:
            print('The following error occurred. ' + e)
            continue
    
    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = input('Please type in month, type "all" for all months: ')
            if month.title() in month_list:
                break
            elif month.lower() ==  'all': 
                break
            else:
                print ('Acceptable inputs: capitalized or lower-case month names (e.g. january) or all')
        except Exception as e:
            print('The following error occurred. ' + e)
            continue
    
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = input('Please type in day of the week, type "all" for all weekdays: ')
            if day.title() in day_list:
                break
            elif day.lower() ==  'all': 
                break
            else:
                print ('Acceptable inputs: capitalized or lower-case weekday names (e.g. sunday) or all')
        except Exception as e:
            print('The following error occurred. ' + e)
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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = month_list.index(month.title()) + 1 # january is month 1 in reality but indexed 0 

        # filter by month to create the new dataframe
        df = df[df['month'] == month] # We are filtering the dataframe df so that it only contains those rows, which have the month of the row the same as the month variable.

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()] # We are filtering the dataframe df so that it only contains those rows, which have the day of week rows same as the day variable.

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    df['month'] = df['Start Time'].dt.month
    mode_month = df['month'].mode()[0]
    mode_month_name = calendar.month_name[mode_month]
    print('The most common month to travel is: {}'.format(mode_month_name))

    # display the most common day of week
    df['weekday'] = df['Start Time'].dt.dayofweek
    mode_weekday = df['weekday'].mode()[0]
    mode_weekday_name = calendar.day_name[mode_weekday]
    print('The most common day to travel is: {}'.format(mode_weekday_name))
    
    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    mode_hour = df['hour'].mode()[0]
    print('The most common hour to start travelling is: {}:00'.format(mode_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    mode_startstation = df['Start Station'].mode()[0]
    print('The most commonly used start station is: {}'.format(mode_startstation))

    # display most commonly used end station
    mode_endstation = df['End Station'].mode()[0]
    print('The most commonly used end station is: {}'.format(mode_endstation))

    # display most frequent combination of start station and end station trip
    station_combo = df['Start Station'] + " to " + df['End Station']
    mode_station_combo = station_combo.mode()[0]
    print('The most frequent trip is: {}'.format(mode_station_combo))
   
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_seconds = df['Trip Duration'].sum()
    total_travel_time = datetime.timedelta(seconds=int(total_travel_seconds))
    print('Total travel time is {}(hrs:min:sec)'.format(total_travel_time))

    # display mean travel time
    mean_travel_seconds = df['Trip Duration'].mean()
    mean_travel_time = datetime.timedelta(seconds=int(mean_travel_seconds))
    print('Average travel time is {}(hrs:min:sec)'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types_count = df['User Type'].value_counts()
    print('Counts per user types: \n{}'.format(user_types_count))

    # Display counts of gender
    if(city != 'washington'):
        gender_count = df['Gender'].value_counts()
        print('Counts per gender: \n{}'.format(gender_count))
    
        # Display earliest, most recent, and most common year of birth
        oldest_birthyear = df['Birth Year'].dropna().min()
        youngest_birthyear = df['Birth Year'].dropna().max()
        mode_birthyear = df['Birth Year'].dropna().mode()
        print('The oldest user was born in: {}'.format(int(oldest_birthyear)))
        print('The youngest user was born in: {}'.format(int(youngest_birthyear)))
        print('The most common birth year is: {}'.format(int(mode_birthyear)))

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)


def raw_df(df):
    """Display 5 lines of raw data."""
    
    raw_line = 0
    while True:
        raw_request = input('Would you like to see 5 lines of raw data?(Yes or No): ').lower()
        y_n_list = ['yes','no']
        if raw_request in y_n_list:
            if raw_request == 'yes':
                print(df.iloc[raw_line:raw_line+5])
                raw_line += 5
                continue
        else:
            print('is that a yes or no?')
            continue
        break
   
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        raw_df(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
    
