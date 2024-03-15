'''
Udacity bikeshare project ... running...
If data is not found when running this code,
copy the .csv files to the current working directory.
'''


import time
import pandas as pd


CITY_DATA = { 'chicago': local_dir + 'chicago.csv',
              'new york city': local_dir + 'new_york_city.csv',
              'washington': local_dir + 'washington.csv'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington).
    # HINT: Use a while loop to handle invalid inputs
    city = input('Please specify one of the cities from (chicago, new york city, washington): ').lower()
    while city not in CITY_DATA.keys():
        city = input('Sorry, the chosen city is not found. \n'
                     'Please specify one of the cities from (chicago, new york city, washington): ').lower()
    print('Great! You just selected the city: {}'.format(city.lower()))

    # TO DO: get user input for month (all, january, february, ... , june)
    month = input("Select a month to investigate (e.g., january, february, etc), \n"
                  "or to select all months, type 'all' or just press Enter: ").lower()

    while month not in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
        if month == '':
            month = 'all'
            print('Great! You just selected all months.')
            break
        else:
            month = input("Invalid. Select a month to investigate (e.g., january, february, etc), \n"
                          "or to select all months, type 'all' or just press Enter: ").lower()
    if month != 'all':
        print('Great! You just selected the month: {}'.format(month.title()))

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Select a day to investigate (e.g., monday, tuesday, etc.), \n"
                "or to select all days, type 'all' or just press Enter: ").lower()
    while (day not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']):
        if day == '':
            day = 'all'
            print('Great! You just selected all days.')
            break
        else:
            day = input("Select a day to investigate (e.g., monday, tuesday, etc.), \n"
                        "or to select all days, type 'all' or just press Enter: ").lower()
    if day != 'all':
        print('Great! You just selected the day: {}'.format(day.title()))

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
    df = pd.read_csv(CITY_DATA[city], index_col=0, delimiter=',')
    # convert the Start Time column to datetime
    df['Start Time'] = df['Start Time'].apply(pd.to_datetime)
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()
    # filter by month if applicable
    if month != 'all':
        # filter by month to create the new dataframe
        df = df[df['month'] == month.title()]
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def head_iter(df):
    """
        load the dataframe and iterate every 5 rows of the raw data
    """
    # whether to show raw data
    if_raw = input('Do you want to see the selected raw data? \n'
                   '(type yes or no or press enter directly): ')
    iter_times = 0
    start_indx, end_indx = 5*iter_times, 5*(iter_times+1)
    while if_raw.lower() != 'no':
        if if_raw.lower() == 'yes' or if_raw == '':
            print(df.iloc[start_indx:end_indx])
            iter_times += 1
            start_indx, end_indx = 5 * iter_times, 5 * (iter_times + 1)
            if_raw = input('Do you want to see more selected raw data? \n'
                   '(type yes or no or press enter directly): ')
        else:
            if_raw = input('Invalid. Type yes or no or press enter directly: ')
        if start_indx > df.shape[0]:
            print('There are not more rows.... quit viewing....')
            break


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    print("The most common month is {}".format(df['month'].mode()[0]))

    # TO DO: display the most common day of week
    print("The most common day of week is {}".format(df['day_of_week'].mode()[0]))

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].apply(pd.to_datetime).dt.hour
    print('The most common start clock hour (24h) is {}:00'.format(df['hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print('The most commonly used start station is {}'.format(df['Start Station'].mode()[0]))

    # TO DO: display most commonly used end station
    print('The most commonly used end station is {}'.format(df['End Station'].mode()[0]))

    # TO DO: display most frequent combination of start station and end station trip
    df['Station Combination'] = df[['Start Station', 'End Station']].apply(list, axis=1)
    print('The most frequent combination of the start and end station trip\n'
          ' is :{}'.format(df['Station Combination'].mode()[0]))
    # combine the start and end station and sorted the combo in case of any repeated routes
    df['Route'] = df[['Start Station', 'End Station']].apply(lambda x: sorted(x), axis=1)
    print('The most frequent trip route\n'
          ' is :{}'.format(df['Route'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    try:
        # TO DO: display total travel time
        print('The total travel time is {}'.format(df['Trip Duration'].sum()))

        # TO DO: display mean travel time
        print('The mean travel time is {}'.format(df['Trip Duration'].mean()))
    except KeyError:
        print('There is no travel time info.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    try:
        print('The counts per user types are: {}'.format(df['User Type'].value_counts()))
    except KeyError:
        print('There is not users info.')

    # TO DO: Display counts of gender
    try:
        print('The counts per gender are: {}'.format(df['Gender'].value_counts()))
    except KeyError:
        print('There is no gender info.')

    try:
        # TO DO: Display earliest, most recent, and most common year of birth
        print('The earliest year of birth is {:d}'.format(int(df['Birth Year'].min())))
        print('The most recent year of birth is {:d}'.format(int(df['Birth Year'].max())))
        print('The most common year of birth is {:d}'.format(int(df['Birth Year'].mode()[0])))
    except KeyError:
        print('There is no birth year info.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        head_iter(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes (y) or no (n).\n').lower()
        while restart not in ['yes', 'no', 'y', 'n']:
            restart = input('\nInvalid. Enter yes (y) or no (n).\n').lower()
        else:
            if restart.lower() in ['no', 'n']:
                break

if __name__ == "__main__":
    main()
