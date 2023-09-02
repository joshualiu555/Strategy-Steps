# Strategy Steps
A recreation of the Wii Party Minigame, "Strategy Steps" Allows unlimited players (preferably 4) Each round, players select a number: 1, 3, 5 After each round, if a player is the only number to select that number, they move up that number of steps. First to 10 wins

The program uses the discord API and discord buttons library. The entire game is asynchronous as it relies on user inputs. 

It cannot support multiple games being played. I did not understand the concept of turning each game into an instance and putting it into an array of games. 
When an request to start the game is entered, an array of players is made in this format.

- Player array
  - Score, Number Chosen

<img width="288" alt="Screen Shot 2023-01-02 at 4 05 32 PM" src="https://user-images.githubusercontent.com/53412192/210280920-39aaec86-9456-4edf-b857-54af5af875e3.png">

## How To Play
1) Begin The Game

> .start @player1 @player2

<img width="258" alt="Screen Shot 2023-01-02 at 4 06 31 PM" src="https://user-images.githubusercontent.com/53412192/210280969-2fc89ef2-c4fd-4ed8-943b-7644f1ed1e8f.png">

2) Start The Round

> .next

<img width="197" alt="Screen Shot 2023-01-02 at 4 08 29 PM" src="https://user-images.githubusercontent.com/53412192/210281068-51fd3ee9-ccd6-46c2-b8e1-f91c6069bde4.png">

3) Choose Your Number

> Simply click a button. The results will appear once everyone has chosen a number

<img width="290" alt="Screen Shot 2023-01-02 at 4 10 19 PM" src="https://user-images.githubusercontent.com/53412192/210281152-30847a53-6e50-473b-83af-a3838a6323ac.png">

4) End The Game

> .end

<img width="259" alt="Screen Shot 2023-01-02 at 4 11 13 PM" src="https://user-images.githubusercontent.com/53412192/210281188-c822c9b2-4411-4ad7-b77d-6470b72ce39f.png">
