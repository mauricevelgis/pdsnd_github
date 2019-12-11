import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
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

    cities = ["chicago", "new york", "washington"]
    months = {
            "all": 0,
            "january": 1,
            "february": 2,
            "march": 3,
            "april": 4,
            "may": 5,
            "june": 6
        }
    days = {
            "monday": 0,
            "tuesday": 1,
            "wednesday": 2,
            "thursday": 3,
            "friday": 4,
            "saturday": 5,
            "sunday": 6,
            "all": 7
        }
    valid = False

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while valid == False:
        city = input("Wpuld you like to see data for Chicago, New York, or Washington?").lower()
        if city in cities:
            valid = True            
        else:
            print("Invalid input: choose an appropriate city")

    # get user input for month (all, january, february, ... , june)
    valid = False
    while valid == False:
        month_input = input("Enter a month (January - June) or type \"all\"  to apply no month filter: ").lower()
        if month_input in months:
            month = months[month_input]
            valid = True
        else:
            print("Invalid input: choose an appropriate month or type \"all\"")       

    # get user input for day of week (all, monday, tuesday, ... sunday)
    valid = False   
    while valid == False:
        day_input = input("Enter a day of the week (Monday-Sunday) or type \"all\" to apply no day filter: ").lower()
        if day_input in days:
            day = days[day_input]
            valid = True
        else:
            print("Invalid input: choose an appropriate day or type \"all\"")


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

    # The following line specifies how many rows of data to read in from the chosen CSV
    df = pd.read_csv(CITY_DATA[city], nrows=10000)

    # The following line converts the Start time into the date_time format to use special functions later
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # The following block filters the data if a specific month was selected
    df['month'] = df['Start Time'].dt.month
    if(month != 0):             
        df = df[df['month'] == month]

    # The following block filters the data if a specific day of the week was selected
    df['day'] = df['Start Time'].dt.dayofweek
    if(day != 7):       
        df = df[df['day'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month   
    months = ["January", "February", "March", "April", "May", "June"]
    df['month'] = df['Start Time'].dt.month 
    popular_month = df['month'].mode()[0]     
    print("The most common month is " + months[popular_month - 1])

    # display the most common day of week
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    df['day'] = df['Start Time'].dt.dayofweek
    popular_day = df['day'].mode()[0]    
    print("The most common day of the week is " + days[popular_day])

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Common Start Hour:', popular_hour)

    print("\nThis took %s seconds to calculate." % (time.time() - start_time))


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0] 
    print("Most popular start station: " + popular_start_station) 

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]  
    print("Most popular end station: " + popular_end_station)

    # display most frequent combination of start station and end station trip
    routes = {}

    for index, row in df.iterrows():
        cur = row['Start Station'] + " to " +  row['End Station']
        if cur in routes.keys():
            routes[cur] += 1
        else:
            routes[cur] = 1

    popular_route = max(routes, key=routes.get)
    print("The most popular route: " + popular_route)  
    
    print("\nThis took %s seconds to calculate." % (time.time() - start_time))


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration_time = df['Trip Duration'].sum()
    print("Total trip duration: " + str(total_duration_time))

    # display mean travel time
    average_duration_time = df['Trip Duration'].mean()
    print("Average trip duration: " + str(average_duration_time))

    print("\nThis took %s seconds to calculate." % (time.time() - start_time))

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types for riders in the selected city
    print(df['User Type'].value_counts().to_frame())
    print()

    # Display counts of gender if that category exists in the CSV for the selected city
    if 'Gender' in df.columns:
        print(df['Gender'].value_counts().to_frame())
        print()  

    # Display earliest, most recent, and most common year of birth for riders in the selected city
    if 'Birth Year' in df.columns:
        earliest_birth_year = int(df["Birth Year"].min())
        most_recent_birth_year = int(df["Birth Year"].max())
        most_common_birth_year = int(df["Birth Year"].mode()[0])
        print("The earliest birth year is " + str(earliest_birth_year)) 
        print("The most recent birth year is " + str(most_recent_birth_year)) 
        print("The most common birth year is " + str(most_common_birth_year)) 

    print("\nThis took %s seconds to calculate." % (time.time() - start_time))

def main():
    while True:
        city, month, day = get_filters()      
        df = load_data(city, month, day)
        
        # The following four function calls display the analysis performed on the raw CSV data for the chosen city
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # The following block of code displays raw CSV data in groups of 5 lines if prompted by the user
        start_index = 0
        end_index = 4
        while True :            
            restart = input('\nWould you like to view 5 lines of raw data? Enter yes or no.\n')
            if restart.lower() != 'yes':
                break
            else:               
                if(end_index >= df.shape[0] - 1):
                    raw_data = df.loc[start_index:end_index, ] 
                    print(raw_data, "\n")
                    print("No more raw data to output")
                    break
                else:
                    raw_data = df.loc[start_index:end_index, ] 
                    print(raw_data, "\n") 
                    start_index += 5
                    end_index += 5

        # The following block refreshes the execution of the program if prompted by the user
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

print("first commit here")