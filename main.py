import os
import openai
import regex as re
from apikeys import apiInfo

openai.organization = apiInfo['ORGANIZATION']
openai.api_key = apiInfo['APIKEY']


def welcomePrompt():
    '''Prints out a welcome statement at the beginning of the program

    Parameters:
        None

    Returns:
        None
    '''
    print('')
    print('-------  WELCOME TO CHATGPtravel  -------')
    print('  Lets discover your dream destination!  ')
    print(' ')


def getVacationType():
    '''Asks users what type of vacation they would like

    Parameters:
        None

    Returns:
        tripType (str): type of trip
    '''
    vacationType = input(
        '''Enter the number of the type of vacation you would like to have:
                                    1. Beach (relaxing) vacation
                                    2. City (exploring/museums/architecture) vacation
                                    3. Nature (hiking/national parks) vacation

                                    ''')
    if int(vacationType) == 1:
        tripType = 'Beach vacation'
    elif int(vacationType) == 2:
        tripType = 'City vacation'
    elif int(vacationType) == 3:
        tripType = 'Nature vacation'
    else:
        tripType = 'Fun vacation'
    return tripType


def getActivityType():
    '''Asks users to choose what type of activities they are interested in hearing about

    Parameters:
        None

    Returns:
        activityPrompt (str): statement about choosen activity type
    '''
    activityType = input(
        '''To clarify, please enter the number describing the activity type that you are interested in hearing about:
                                    1. Beach (relaxing)
                                    2. City (exploring/museums/architecture/cultural sightseeing)
                                    3. Nature (hiking/national parks)

                                    ''')
    # This sets up the prompt for ChatGPT for specific activity types. The
    # default is fun activities.
    if int(activityType) == 1:
        activityPrompt = 'activities related to relaxing and being on the beach'
    elif int(activityType) == 2:
        activityPrompt = 'activities related to exploring the city and sightseeing.'
    elif int(activityType) == 3:
        activityPrompt = 'activities related to hiking, being in nature, and/or seeing national parks'
    else:
        activityPrompt = 'activities that are fun'
    return activityPrompt


def getTravelGroup():
    '''Asks user to choose an option for who they'll be traveling with

    Parameters:
        None

    Returns:
        peoples (str): statement about who user will be traveling with
    '''
    people = input(
        '''Enter the number of the option that best describes your trip:
                        1. Traveling solo
                        2. Travel with a partner
                        3. Traveling with family
                        4. Traveling with friends

                        ''')
    # This sets up the response for ChatGPT for specific travel groups. The
    # default is solo travel.
    if int(people) == 1:
        peoples = 'Solo travel'
    elif int(people) == 2:
        peoples = 'Traveling with a partner'
    elif int(people) == 3:
        peoples = 'Traveling with family'
    elif int(people) == 4:
        peoples = 'Traveling with friends'
    else:
        peoples = 'Solo travel'
    return peoples


def getHotelType():
    '''Asks user to select price option for their hotel recommendations

    Parameters:
        None

    Returns:
        budget (str): statement about price option for hotel recommendations
    '''
    hotelType = input(
        '''Enter the number of the option you like to learn about:
                                1. Budget hotels
                                2. Mid-tier hotels
                                3. Luxury hotels

                                ''')
    # This sets up the response for ChatGPT for specific hotel price options.
    # The default is mid-tier priced hotels.
    if int(hotelType) == 1:
        budget = "budget hotels"
    elif int(hotelType) == 2:
        budget = 'mid-tier priced hotels'
    elif int(hotelType) == 3:

        budget = 'luxury hotels'
    else:
        budget = 'mid-tier priced hotels'
    return budget


def getFoodBudget():
    '''Asks user to choose a price option for their restaurant recommendations

    Parameters:
        None

    Returns:
        restaurant (str): statement about price option for restaurant recommendations
    '''
    restaurantType = input(
        '''Enter the number of the option you like to learn about:
                                    1. Cheap/Budget restaurants
                                    2. Mid-tier or nicer restaurants
                                    3. High-end restaurants

                                    ''')
    # This sets up the response for ChatGPT for specific restaurant price
    # options. The default is the most recommended restaurants.
    if int(restaurantType) == 1:
        restaurant = "cheap or low priced restaurants"
    elif int(restaurantType) == 2:
        restaurant = 'mid-priced restaurants'
    elif int(restaurantType) == 3:
        restaurant = 'high-end or luxury restaurants'
    else:
        restaurant = 'the most recommended restaurants'
    return restaurant


def pickDestination():
    '''Asks users to select the type of search they would like to do. Users are then prompted to respond to a series of questions regarding their trip preferences.

    Parameters:
        None

    Returns:
        specifications (list): a list including information on user preferences for location, type of trip, when, length of trip, and people they will be going with
    '''
    # Asks the user if they have a location in mind or if they need help
    # finding a location. The prompts are different depending on the user's
    # response.
    searchType = input('''Enter the number of the option you want:
          1. I have a location in mind that I would like help learning more about
          2. I need help finding a location

          ''')
    # This condition is for if the user has a specific location in mind
    if int(searchType) == 1:
        location = input('Where would you like to travel? ')
        when = input("What month of the year would you like to travel? ")
        length = input('How long would you like to go for? ')
        peoples = getTravelGroup()

        tripType = getVacationType()

        specifications = [location, tripType, when, length, peoples]
        return specifications

    # This condition is for if the user needs help finding a location
    else:
        when = input("What month of the year would you like to travel? ")
        length = input('How long would you like to go for? ')
        climate = input("Would you like to go somewhere warm or cold? ")
        peoples = getTravelGroup()
        tripType = getVacationType()

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": f'What are the 10 best places to travel for a {tripType} in {when} that has a {climate} climate for {length} for {peoples}?'}])
        print(" ")
        print("Here is a list of ten possible options:")
        print(completion.choices[0].message.content)
        return ([when, length, climate, peoples, tripType],
                completion.choices[0].message.content)


def undecidedPickDestinationNum(destinationList):
    '''For users that don't have a destination picked yet, this function asks them to pick a destination from a list of recommendations based on their specified preferences

    Parameters:
        destinationList (list): list of program-generated destination recommendations

    Returns:
        destinationNumber (str): number corresponding to the destination they would like to learn more about
    '''
    destinationNumber = input(
        'From the list of places that fit your criteria, please enter the number of the place you would like to learn more about: ')
    return destinationNumber


def chosenDestActivities(destinationList):
    '''Asks user if they would like to learn about some activities they can do in their chose destination.
    If user says yes, the function provides them with a list of recommended activities based on their preferences

    Parameters:
        destinationList (list): list of program-generated destination recommendations

    Returns:
        completion (str): list of 10 recommended activities
    '''

    yesNoActivity = input(
        f'Would you like to learn about some of the activities you can do in {destinationList[0]}? Enter 1 for yes, or anything else for no! ')
    if yesNoActivity in ['1', ' 1', ' 1']:
        # Clarifies which type of activities the user would like to learn about
        activityType = getActivityType()
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": f'What are the 10 best 10 best {activityType} to do in {destinationList[0]} in {destinationList[2]} for {destinationList[-1]}?'}])

        print(" ")
        print(
            f"Here is a list of 10 things you can do in {destinationList[0]}:")
        print(completion.choices[0].message.content)
        return completion.choices[0].message.content


def undecidedDestActivities(destination, preferenceList):
    '''Asks user if they would like to learn about some activities they can do in their chose destination.
    If user says yes, the function provides them with a list of recommended activities based on their preferences

    Parameters:
        destinationList (list): list of program-generated destination recommendations
        preferenceList (list): list of user-specified trip preferences

    Returns:
        completion (str): list of 10 recommended activities
    '''
    yesNoActivity = input(
        f'Would you like to learn about some of the activities you can do in {destination}? Enter 1 for yes, or anything else for no! ')
    if yesNoActivity in ['1', ' 1', ' 1']:
        # Clarifies which type of activities the user would like to learn about
        activityType = getActivityType()

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": f'What are the 10 best {activityType} to do in {destination} in {preferenceList[0]} for {preferenceList[3]}?'}])
        print(" ")
        print(f"Here is a list of 10 things you can do in {destination}:")
        print(completion.choices[0].message.content)
        return completion.choices[0].message.content


def chosenDestHotels(destinationList):
    '''Asks user if they would like to learn about some hotels they can do in their chose destination.
    If user says yes, the function provides them with a list of recommended hotels based on their preferences

    Parameters:
        destinationList (list): list of program-generated destination recommendations

    Returns:
        completion (str): list of 10 recommended hotels
    '''
    yesNoHotels = input(
        f'Would you like to learn about some of the hotels you can do stay at in {destinationList[0]}? Enter 1 for yes, or anything else for no! ')
    if yesNoHotels in ['1', ' 1', ' 1']:
        # Determines which price range the user would like to learn about for
        # hotels
        budget = getHotelType()

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": f'What are the 10 best {budget} to stay at in {destinationList[0]} for {destinationList[-1]}?'}])
        print(" ")
        print(
            f"Here is a list of 10 places you can stay in {destinationList[0]}:")
        print(completion.choices[0].message.content)
        return completion.choices[0].message.content


def undecidedDestHotels(destination, preferenceList):
    '''Asks user if they would like to learn about some hotels they can do in their chose destination.
    If user says yes, the function provides them with a list of recommended hotels based on their preferences

    Parameters:
        destinationList (list): list of program-generated destination recommendations
        preferenceList (list): list of user-specified trip preferences

    Returns:
        completion (str): list of 10 recommended hotels
    '''

    yesNoHotels = input(
        f'Would you like to learn about some of the hotels you can do stay at in {destination}? Enter 1 for yes, or anything else for no! ')
    if yesNoHotels in ['1', ' 1', ' 1']:
        # Determines which price range the user would like to learn about for
        # hotels
        budget = getHotelType()

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": f'What are the 10 best {budget} to stay at in {destination} for {preferenceList[3]}? '}])
        print(" ")
        print(f"Here is a list of 10 places you can stay in {destination}:")
        print(completion.choices[0].message.content)
        return completion.choices[0].message.content


def chosenDestFood(destinationList):
    '''Asks user if they would like to learn about some restaurants they can do in their chose destination.
    If user says yes, the function provides them with a list of recommended restaurants based on their preferences

    Parameters:
        destinationList (list): list of program-generated destination recommendations

    Returns:
        completion (str): list of 10 recommended restaurants
    '''

    yesNoFood = input(
        f'Would you like to learn about some of the restaurants in {destinationList[0]}? Enter 1 for yes, or anything else for no! ')
    if yesNoFood in ['1', ' 1', ' 1']:
        # Determines which price range the user would like to learn about for
        # restaurant options
        foodPrice = getFoodBudget()
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": f'What are the 10 best {foodPrice} in {destinationList[0]} for {destinationList[-1]}?'}])
        print(" ")
        print(
            f"Here is a list of 10 restaurants you can try out in {destinationList[0]}:")
        print(completion.choices[0].message.content)
        return completion.choices[0].message.content


def undecidedDestFood(destination, preferenceList):
    '''Asks user if they would like to learn about some restaurants they can do in their chose destination.
    If user says yes, the function provides them with a list of recommended restaurants based on their preferences

    Parameters:
        destinationList (list): list of program-generated destination recommendations

    Returns:
        completion (str): statement about the estimated total cost
    '''

    yesNoFood = input(
        f'Would you like to learn about some of the restaurants in {destination}? Enter 1 for yes, or anything else for no! ')
    if yesNoFood in ['1', ' 1', ' 1']:
        # Determines which price range the user would like to learn about for
        # restaurant options
        foodPrice = getFoodBudget()
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": f'What are the 10 best {foodPrice} in {destination} for {preferenceList[3]}?'}])
        print(" ")
        print(
            f"Here is a list of 10 restaurants you can try out in {destination}:")
        print(completion.choices[0].message.content)
        return completion.choices[0].message.content


def chosenDestTotalCost(destinationList):
    '''Asks user if they would like to learn about the estimated total cost for their trip based on their specifications.
    If user says yes, the function provides them with a an estimated total cost.

    Parameters:
        destinationList (list): list of program-generated destination recommendations

    Returns:
        completion (str): statement about the estimated total cost
    '''
    yesNoCost = input(
        f'Would you like to learn about the estimated cost for a trip to {destinationList[0]}? Enter 1 for yes, or anything else for no! ')
    if yesNoCost in ['1', ' 1', ' 1']:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": f'What is the estimated cost per person for a {destinationList[1]} in {destinationList[0]} for {destinationList[3]} in {destinationList[2]} for {destinationList[-1]}?'}])
        print(" ")
        print(
            f"Here is the estimated cost per person for a {destinationList[1]} in {destinationList[0]} for {destinationList[3]} in {destinationList[2]} for {destinationList[-1]}?")
        print(completion.choices[0].message.content)
        return completion.choices[0].message.content


def undecidedDestTotalCost(destination, preferenceList):
    '''Asks user if they would like to learn about the estimated total cost for their trip based on their specifications.
    If user says yes, the function provides them with a an estimated total cost.

    Parameters:
        destinationList (list): list of program-generated destination recommendations
        preferenceList (list): list of user-specified trip preferences

    Returns:
        completion (str): statement about the estimated total cost
    '''

    yesNoCost = input(
        f'Would you like to learn about the estimated cost for a trip to {destination}? Enter 1 for yes, or anything else for no! ')
    if yesNoCost in ['1', ' 1', ' 1']:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": f'What is the estimated cost per person for a {preferenceList[4]} in {destination} for {preferenceList[1]} in {preferenceList[0]} for {preferenceList[-1]}?'}])
        print(" ")
        print(
            f"Here is the estimated cost per person for a {preferenceList[4]} in {destination} for {preferenceList[1]} in {preferenceList[0]} for {preferenceList[-1]}?")
        print(completion.choices[0].message.content)
        return completion.choices[0].message.content


def saveTravelInfo(preferences, activities, hotels, food, cost):
    '''Saves the results of searches into a file

    Parameters:
        activities (str): text containing activities for user-decided location
        hotels (str): text containing hotel options for user-decided location
        food (str): text containing restaurant options for user-decided location
        cost (str): text containing the estimate cost of trip to user-decided location

    Returns:
        None
    '''
    # Saves the results of searches into a file and appends to the file instead of writing over it each time in case the user wants to save multiple trips
    with open("TripInfo.txt", "a") as f:
        f.write("Where: {}\n".format(preferences[0]))
        f.write("Type: {}\n".format(preferences[1]))
        f.write("Month: {}\n".format(preferences[2]))
        f.write("Length of trip: {}\n".format(preferences[3]))
        f.write("With who: {}\n".format(preferences[4]))
        f.write("Activities: {}\n".format(activities))
        f.write("Hotels: {}\n".format(hotels))
        f.write("Food: {}\n".format(food))
        f.write("Cost: {}\n\n".format(cost))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    welcomePrompt()
    while True:
        preferences = pickDestination()

        if isinstance(preferences, list):
            # The chosen pathway returns a list of the user's preferences for
            # the trip
            activities = chosenDestActivities(preferences)
            print(" ")
            hotels = chosenDestHotels(preferences)
            print(" ")
            food = chosenDestFood(preferences)
            print(" ")
            cost = chosenDestTotalCost(preferences)

        else:
            # The undecided pathway returns a tuple of the user's preferences for the trip and the ChatGPT-generated destinations
            # This allows the program to decipher which destination the user
            # would like to learn more about
            destinationList = preferences[1]
            userPreferences = preferences[0]
            # Performs regex to assemble the destinations provided by ChatGPT
            # into a list of strings
            cleanedDestinationList = re.findall(
                r'([\d]+\.\s[(\w+)|(\w+, \w+))]*\b)', destinationList)
            print(" ")
            destinationNum = undecidedPickDestinationNum(destinationList)
            # Obtains the specific destination the user would like to learn
            # more about
            chosenDestination = cleanedDestinationList[int(
                destinationNum) - 1][3:]
            print(" ")
            activities = undecidedDestActivities(
                chosenDestination, userPreferences)
            print(" ")
            hotels = undecidedDestHotels(chosenDestination, userPreferences)
            print(" ")
            food = undecidedDestFood(chosenDestination, userPreferences)
            print(" ")
            cost = undecidedDestTotalCost(chosenDestination, userPreferences)
            print(" ")
            # Recreates the user's preferences list with the chosen destination
            # as the first element to be used in the saveTravelInfo function
            undecidedPreferences = [
                chosenDestination,
                userPreferences[4],
                userPreferences[0],
                userPreferences[1],
                userPreferences[3]]

        print(" ")
        playAgain = input('Would you like to start a new search? If you would like to learn about other options for your destination, this is your chance to. Or you can explore somewhere new! Enter 1 for yes, or anything else for no! ')
        if playAgain in ['1', ' 1', ' 1']:
            save = input(
                'Would you like to save your search results?  Enter 1 for yes, or anything else for no! ')
            # Saves the results of the search if the user wants to. 
            # If the user had a chosen location, the saveTravelInfo function will use the preferences list. 
            # If the user had an undecided location, the saveTravelInfo function will use the undecidedPreferences list.
            if save in ['1', ' 1', ' 1'] and (isinstance(preferences, list)):
                saveTravelInfo(preferences, activities, hotels, food, cost)
                print(" ")
                print("Your trip information has been saved to TripInfo.txt")
            elif save in ['1', ' 1', ' 1'] and (not isinstance(preferences, list)):
                saveTravelInfo(
                    undecidedPreferences,
                    activities,
                    hotels,
                    food,
                    cost)
                print(" ")
                print("Your trip information has been saved to TripInfo.txt")
            continue
        else:
            save = input(
                'Would you like to save your search results? Enter 1 for yes, or anything else for no! ')
            if save in ['1', ' 1', ' 1'] and (isinstance(preferences, list)):
                saveTravelInfo(preferences, activities, hotels, food, cost)
                print(" ")
                print("Your trip information has been saved to TripInfo.txt")
            elif save in ['1', ' 1', ' 1'] and (not isinstance(preferences, list)):
                saveTravelInfo(
                    undecidedPreferences,
                    activities,
                    hotels,
                    food,
                    cost)
                print(" ")
                print("Your trip information has been saved to TripInfo.txt")
            print("")
            print("Thank you for trying out ChatGPtravel! Come again soon!")
            print("")
            break
