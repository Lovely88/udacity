import time
import pandas as pd
import numpy as np

from os import system, name

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

# define clear function to clear the screen
def clear(): 
  
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 			  
			  
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("\n\t\t\t*******************************************************************************")
    print("\n\t\t\t*        Hello! Let's explore some US bikeshare data!                         *")
    print("\n\t\t\t*******************************************************************************")
	# get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('\n\t\tWould you like to see data for Chicago, New York or Washington?\n\n\t\tType here : ')
        if city.lower() not in ('chicago','new york','washington'):
            print("\n\n\t\tPlease type a correct city name (	Chicago, New York or Washington ).")
            continue
        break
    print("\n\n\t\tLooks like you want to hear about {}! If this is not true, restart the program now!".format(city))
    city=city.lower()
	
    selection=input("\n\t\tWould you like to filter the data by month, day , both or not at all? Type 'none' for no time filter.\n\t\tType here :")
    print("\n\t\tWe'll make sure to filter by {}".format(selection))
	
    # get user input for month (all, january, february, ... , june)
    if selection == "month" or selection == "both":
        month=input("\n\t\tWhich month? January, February, March, April, May or June? \n\t\tPlease type out the full month name :").lower()
    
	# get user input for day of week (all, monday, tuesday, ... sunday)
    if selection == "day" or selection == "both":
        day=input("\n\t\tWhich day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday.\n\t\tType here : ").lower()
        while True:
            if day.lower() not in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
                print("\n\t\tIncorrect Day input.\n")
                day=input("\n\t\tWhich day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday?\n\t\tType here : ")    
            break			
            day=day.lower()
		
    if selection == "day" or  selection == "none":
        month="all"
		
    if selection == "month" or  selection == "none":	
        day="all"
    
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
        df - pandas DataFrame containing city data filtered by month and day
    """
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new data frame
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    pop_month = df['month'].mode()[0]
    popular_month = months[pop_month-1]
    print("\nThe Popular Month is : " + str(popular_month))
	
    # display the most common day of week

    popular_day_of_week = df['day_of_week'].mode()[0]
    print("\nThe Popular Day of Week : " + str(popular_day_of_week))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour

    popular_hour = df['hour'].mode()[0]
    print("\nThe Most Common Hour of day : " + str(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print("\nThe Most Common Start Station : " + popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print("\nThe Most Common End Station : " + popular_end_station)

    # display most frequent combination of start station and end station trip
    df['Start End Station']=df['Start Station'] + '|' + df['End Station'] 
    popular_start_end_station = df['Start End Station'].mode()[0]
    print("\nThe Most Common Start and End Station : " + popular_start_end_station)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Travel Time'] = df['End Time'] - df['Start Time']
    total_travel_time = df['Travel Time'].sum()
    print("\nTotal Travel Time is : " + str(total_travel_time))

    # display mean travel time
    mean_travel_time = df['Travel Time'].mean()
    print("\nMean Travel Time is : " + str(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    for user in user_types.index:
	    print("\nThe Count of User of Type " + str(user) + " : " + str(user_types[user]))

    # Display counts of gender
    if 'Gender' in df.columns:
        gender = df['Gender'].value_counts()
        for gndr in gender.index:
	        print("\nThe Count of " + gndr + " : " + str(gender[gndr]))

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_birth_year = df['Birth Year'].min()	
        print("\nEarliest Birth Year : " + str(earliest_birth_year))
	
        recent_birth_year = df['Birth Year'].max()
        print("\nRecent Birth Year : " + str(recent_birth_year))
	
        common_birth_year = df['Birth Year'].mode()[0]
        print("\nCommon Birth Year : " + str(common_birth_year))
	
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        clear() #This function call will clear the screen
        city, month, day = get_filters()
        df = load_data(city, month, day)	
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
# Added this line for git project
