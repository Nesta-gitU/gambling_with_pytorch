import Metrica_IO as mio
import Metrica_Viz as mviz
from pandas import Series
import pandas as pd
import numpy as np

# set up initial path to data
DATADIR = 'C:/Nesta/side projects/gambling_with_vscode/data'

def get_goal_times(game_id):

    # read in the event data
    events = mio.read_event_data(DATADIR,game_id)
    print(events.head())

    # Bit of housekeeping: unit conversion from metric data units to meters
    events = mio.to_metric_coordinates(events)

    # get the time of each goal 
    goals = events[events['Type']=='SHOT']
    goals = goals[goals['Subtype'].str.contains('-GOAL')].copy()
    
    return goals["Start Time [s]"] 

def append_goal_times_to_tracking_data(goal_times, game_id):
    
    # read in the tracking data for home & away teams 
    tracking_home = mio.tracking_data(DATADIR,2,'Home')#.iloc[0:1000]
    tracking_away = mio.tracking_data(DATADIR,2,'Away')#.iloc[0:1000]

    # Look at the column namems
    #print( tracking_home.columns )

    # Convert positions from metrica units to meters 
    tracking_home = mio.to_metric_coordinates(tracking_home)
    tracking_away = mio.to_metric_coordinates(tracking_away)

    print(tracking_away.head())

    print(tracking_home.head())

    # add a collumn for every frame with if there is a goal in the next x minutes or not 
    x = 5 # minutes

    tracking_home["".join(["goal_in_next_", str(x), "_minutes"])] = tracking_home.apply(lambda row: goal_in_next_x_minutes(x, row["Time [s]"], goal_times), axis=1)

    print(tracking_home[tracking_home["goal_in_next_5_minutes"] == True])

    tracking_away["".join(["goal_in_next_", str(x), "_minutes"])] = tracking_away.apply(lambda row: goal_in_next_x_minutes(x, row["Time [s]"], goal_times), axis=1)

    return tracking_home, tracking_away


    #tracking_home["".join(["goal_in_next_", str(x), "_minutes"])] = 

def goal_in_next_x_minutes(x, current_time, goal_times):
    boolean = any(goal_times.between(current_time, current_time + x*60))
    return boolean

def get_distance_to_goal(player_position, goal_position):
    return np.linalg.norm(np.array(player_position) - np.array(goal_position))

def get_distance_features(tracking_home, tracking_away, home_goal_position, away_goal_position):
    """
    Calculate distance features for each frame of tracking data.
    
    Parameters:
    tracking_data (DataFrame): DataFrame containing tracking data.
    home_goal_position (tuple): (x, y) position of the home team's goal.
    away_goal_position (tuple): (x, y) position of the away team's goal.
    
    Returns:
    DataFrame: The input tracking data DataFrame with additional columns for distance features.
    """
    # Calculate distance to home goal for all players in the home team
    home_to_homegoal = pd.DataFrame()

    for x in range(1, 15):
        home_to_homegoal["{}".format(x)] = tracking_home.apply(
        lambda row: get_distance_to_goal((row["Home_{}_x".format(x)], row["Home_{}_y".format(x)]), home_goal_position),
        axis=1
    )
    
    print(home_to_homegoal)
    closest_home_to_homegoal_per_frame = home_to_homegoal.apply(second_smallest, axis=1)
    print(closest_home_to_homegoal_per_frame)

    # Calculate distance to away goal for all players in the home team
    home_to_awaygoal = pd.DataFrame()

    for x in range(1, 15):
        home_to_awaygoal["{}".format(x)] = tracking_home.apply(
        lambda row: get_distance_to_goal((row["Home_{}_x".format(x)], row["Home_{}_y".format(x)]), away_goal_position),
        axis=1
    )
    
    closest_home_to_awaygoal_per_frame = home_to_awaygoal.min(axis=1)

    # calculate distance to away goal for all players in the away team

    away_to_awaygoal = pd.DataFrame()

    for x in range(15, 27):
        away_to_awaygoal["{}".format(x)] = tracking_away.apply(
        lambda row: get_distance_to_goal((row["Away_{}_x".format(x)], row["Away_{}_y".format(x)]), away_goal_position),
        axis=1
    )
        
    closest_away_to_awaygoal_per_frame = away_to_awaygoal.apply(second_smallest, axis=1)

    # calculate distance to home goal for all players in the away team

    away_to_homegoal = pd.DataFrame()

    for x in range(15, 27):
        away_to_homegoal["{}".format(x)] = tracking_away.apply(
        lambda row: get_distance_to_goal((row["Away_{}_x".format(x)], row["Away_{}_y".format(x)]), home_goal_position),
        axis=1
    )
        
    closest_away_to_homegoal_per_frame = away_to_homegoal.min(axis=1)

    features = pd.DataFrame(columns=["closest_home_to_homegoal", "closest_home_to_awaygoal", "closest_away_to_awaygoal", "closest_away_to_homegoal"])
    features["closest_home_to_homegoal"] = closest_home_to_homegoal_per_frame
    features["closest_home_to_awaygoal"] = closest_home_to_awaygoal_per_frame
    features["closest_away_to_awaygoal"] = closest_away_to_awaygoal_per_frame
    features["closest_away_to_homegoal"] = closest_away_to_homegoal_per_frame
    
    return features

def second_smallest(row):
    sorted_values = row.sort_values()
    return sorted_values.iloc[1]



def main():
    goal_times_game2 = get_goal_times(game_id=2)
    goal_times_game2 = goal_times_game2.reset_index(drop=True)
    print(goal_times_game2) 

    tracking_home, tracking_away = append_goal_times_to_tracking_data(goal_times_game2, game_id=2)
    

    home_goal_position = (-53, 0)  # Replace with the actual home team goal position
    away_goal_position = (53, 0)  # Replace with the actual away team goal position

    #first_do_first_period
    tracking_home_p1 = tracking_home[tracking_home["Period"] == 1]
    tracking_away_p1 = tracking_away[tracking_away["Period"] == 1]

    tracking_home_p2 = tracking_home[tracking_home["Period"] == 2]
    tracking_away_p2 = tracking_away[tracking_away["Period"] == 2]
    
    features1 = get_distance_features(tracking_home_p1, tracking_away_p1, home_goal_position = away_goal_position, away_goal_position = home_goal_position)
    features2 = get_distance_features(tracking_home_p2, tracking_away_p2, home_goal_position = home_goal_position, away_goal_position = away_goal_position)

    features = pd.concat([features1, features2], ignore_index=True)
    
    features.to_csv("C:/Nesta/side projects/gambling_with_vscode/data/features.csv")








if __name__ == "__main__":
    # test
    main()