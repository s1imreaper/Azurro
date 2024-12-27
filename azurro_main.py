

# Main Streamlit page

# IMPORTS

import streamlit as st
import pandas as pd
import numpy as np

from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.endpoints import playercareerstats
from nba_api.live.nba.endpoints import scoreboard
from nba_api.stats.endpoints import playergamelog

player_id, team_id = None, None

player_img = f"https://cdn.nba.com/headshots/nba/latest/1040x760/{player_id}.png"
team_logo = f"https://cdn.nba.com/logos/nba/{team_id}/global/L/logo.svg"

def display_scores(scores):
        
    for game in scores:
        # Extracting details for home and away teams
        home_team_id, home_team_name, home_team_score = (
            game["homeTeam"]["teamId"], 
            f"{game['homeTeam']['teamCity']} {game['homeTeam']['teamName']}", 
            game["homeTeam"]["score"]
        )
        away_team_id, away_team_name, away_team_score = (
            game["awayTeam"]["teamId"], 
            f"{game['awayTeam']['teamCity']} {game['awayTeam']['teamName']}", 
            game["awayTeam"]["score"]
        )
        time_left = f"{game['gameStatusText']} {game['gameClock']}"
        date = game['gameCode'].split('/')[0]
        
        # Constructing logo URLs
        home_team_logo =  f"https://cdn.nba.com/logos/nba/{home_team_id}/global/L/logo.svg"
        away_team_logo = f"https://cdn.nba.com/logos/nba/{away_team_id}/global/L/logo.svg"

        # Displaying the game details in columns
        cols = st.columns([2, 1, 2])  # Adjust column widths for better layout
        with cols[0]:
            st.markdown(
                f"<div style='text-align: center;'><img src='{home_team_logo}' width='100'></div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<div style='text-align: center; font-size: 32px; font-weight: bold;'>{home_team_score}</div>",
                unsafe_allow_html=True,
            )       
        with cols[1]:
            st.markdown(
                f"""
                <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; height: 150px;">
                    <span style="font-size: 15px;">{time_left}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with cols[2]:
            st.markdown(
                f"<div style='text-align: center;'><img src='{away_team_logo}' width='100'></div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<div style='text-align: center; font-size: 32px; font-weight: bold;'>{away_team_score}</div>",
                unsafe_allow_html=True,
            )
        
        # Optional: Add a horizontal separator between games
        st.markdown("---")

def display_scores_two(scores):
    st.title("NBA Live Scores")

    # Calculate the number of games
    num_games = len(scores)

    # Process games in pairs (two games per row)
    for i in range(0, num_games, 2):
        # If we're at the last game and it has no pair, display it alone
        game_pair = scores[i:i + 2]  # Get two games for each row

        # Create a row with six columns (for two games per row)
        cols = st.columns([2, 1, 2, 2, 1, 2])  # Adjust column widths for each game (home, time, away)

        for j, game in enumerate(game_pair):
            # Extracting details for home and away teams
            home_team_id, home_team_name, home_team_score = (
                game["homeTeam"]["teamId"], 
                f"{game['homeTeam']['teamCity']} {game['homeTeam']['teamName']}", 
                game["homeTeam"]["score"]
            )
            away_team_id, away_team_name, away_team_score = (
                game["awayTeam"]["teamId"], 
                f"{game['awayTeam']['teamCity']} {game['awayTeam']['teamName']}", 
                game["awayTeam"]["score"]
            )
            time_left = f"{game['gameStatusText']} {game['gameClock']}"

            # Constructing logo URLs
            home_team_logo = f"https://cdn.nba.com/logos/nba/{home_team_id}/global/L/logo.svg"
            away_team_logo = f"https://cdn.nba.com/logos/nba/{away_team_id}/global/L/logo.svg"

            # Displaying the game details in columns
            with cols[j * 3]:  # First column for home team
                st.markdown(
                    f"<div style='text-align: center;'><img src='{home_team_logo}' width='100'></div>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"<div style='text-align: center; font-size: 32px; font-weight: bold;'>{home_team_score}</div>",
                    unsafe_allow_html=True,
                )       
            
            with cols[1 + j * 3]:  # Middle column for time
                st.markdown(
                    f"""
                    <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; height: 150px;">
                        <span style="font-size: 15px;">{time_left}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            
            with cols[2 + j * 3]:  # Second column for away team
                st.markdown(
                    f"<div style='text-align: center;'><img src='{away_team_logo}' width='100'></div>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"<div style='text-align: center; font-size: 32px; font-weight: bold;'>{away_team_score}</div>",
                    unsafe_allow_html=True,
                )
        
        # Optional: Add a horizontal separator between rows of games
        st.markdown("---")

def espn_mapper(query):
    API_KEY = "AIzaSyAl87Z6PNPROSTbbFaeI-j9zCnD9jmudAE"
    time.sleep(3)
    # API configuration
    CX_ID = "76135ca5e492f4722"
    QUERY = f"{query}"

    # API endpoint
    url = "https://customsearch.googleapis.com/customsearch/v1"

    # Parameters
    params = {
        "q": QUERY,
        "cx": CX_ID,
        "key": API_KEY,
        "num": 10,  # Number of results per page
    }

    # Make the request
    response = requests.get(url, params=params)

    # Check the response
    if response.status_code == 200:
        results = response.json()
        results = dict(results)
        for item in results.get("items", []):
            print(f"Title: {item['title']}")
            print(f"Link: {item['link']}")
            print(f"Snippet: {item['snippet']}\n")
    else:
        print(f"Error: {response.status_code}, {response.text}")
    response
    link = results['items'][0]['link']
    link
    return link

def espn_scraper(link):



    # URL of the ESPN page
    url = link

    # Headers to mimic a browser request

    # Fetch the webpage with headers
    response = requests.get(url)
    response
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    soup
    # Extract the span element with the specific class
    win_prob_element = soup.find("span", class_="WinProbabilityGraphHeader__Percent__Number")

    # Extract and print the text (e.g., "100")
    if win_prob_element:
        win_probability = win_prob_element.text.strip()
        print("Win Probability:", win_probability)
    else:
        print("Win Probability not found.")

def display_scores_three(scores):
    st.title("NBA Live Score Board")

    # Calculate the number of games
    num_games = len(scores)

    # Process games in triplets (three games per row)
    for i in range(0, num_games, 3):
        # If we're at the last row and there are fewer than 3 games, just show the remaining games
        game_triplet = scores[i:i + 3]  # Get three games for each row

        # Create a row with 9 columns (3 columns for each game)
        cols = st.columns([2, 1, 2, 2, 1, 2, 2, 1, 2])  # Adjust column widths for each game (home, time, away)

        for j, game in enumerate(game_triplet):
            # Extracting details for home and away teams
            home_team_id, home_team_name, home_team_score = (
                game["homeTeam"]["teamId"], 
                f"{game['homeTeam']['teamCity']} {game['homeTeam']['teamName']}", 
                game["homeTeam"]["score"]
            )
            away_team_id, away_team_name, away_team_score = (
                game["awayTeam"]["teamId"], 
                f"{game['awayTeam']['teamCity']} {game['awayTeam']['teamName']}", 
                game["awayTeam"]["score"]
            )
            time_left = f"{game['gameStatusText']} {game['gameClock']}"

            # Constructing logo URLs
            home_team_logo = f"https://cdn.nba.com/logos/nba/{home_team_id}/global/L/logo.svg"
            away_team_logo = f"https://cdn.nba.com/logos/nba/{away_team_id}/global/L/logo.svg"

            # Displaying the game details in columns
            with cols[j * 3]:  # First column for home team
                st.markdown(
                    f"<div style='text-align: center;'><img src='{home_team_logo}' width='100'></div>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"<div style='text-align: center; font-size: 32px; font-weight: bold;'>{home_team_score}</div>",
                    unsafe_allow_html=True,
                )       
            
            with cols[1 + j * 3]:  # Middle column for time
                st.markdown(
                    f"""
                    <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; height: 150px;">
                        <span style="font-size: 15px;">{time_left}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            
            with cols[2 + j * 3]:  # Second column for away team
                st.markdown(
                    f"<div style='text-align: center;'><img src='{away_team_logo}' width='100'></div>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"<div style='text-align: center; font-size: 32px; font-weight: bold;'>{away_team_score}</div>",
                    unsafe_allow_html=True,
                )
        
        # Add a small separation between rows of games using <hr> (horizontal rule)
        st.markdown("<hr style='margin-top: 20px; margin-bottom: 20px;' />", unsafe_allow_html=True)







def main():
    st.set_page_config(layout="wide")

    st.write("")


    # Today's Score Board
    games = scoreboard.ScoreBoard()

    print("space")
    # json
    games.get_json()

    # dictionary
    test = games.get_dict()
    #test

    scores = test['scoreboard']['games']
        # Fetch live scores
    #display_scores(scores)


    

    # Display scores if data is available
    if scores:
        display_scores_three(scores)

    else:
        st.warning("No live games availablet the moment.")




if __name__ == "__main__":
    main()