# Blackjack Dealer
This Robotic Blackjack Dealer project will be designed to provide users with an interactive experience of playing Blackjack that combines the tangibility of playing in real life with the ease of automation found in online games. This project is for the course ECE 1896 - Senior Design in the Electrical and Computer Engineering department at the University of Pittsburgh

The goal of this project will be to design a robotic system that can function as an effective card dealer at a Blackjack table. Currently, live-human dealers are costly for casinos to employ, and hiring enough dealers to fill tables at a casino may increase this cost. Players may also feel uncomfortable with an experienced dealer possibly manipulating the cards to give the house a favorable advantage in the game. Replacing live dealers with robotic dealers will cut on the casinos expenses, allow for more players to be hosted, and will allow for a better established trust that there is no cheating or manipulation.

Our design takes influence from 3D printers and a common method with which they navigate a plane. We’ll have a gantry setup that is fixed on a table top and covers an x-y plane. Within the center arm of the gantry, will be a vertically mounted component that can move along the z-axis with a vacuum pump to enable the picking up and movement of cards around the table. Beneath the table will be a camera and connected Raspberry Pi, with the camera looking vertically through a piece of clear acrylic. Also connected to the Pi will be a touchscreen display to enable player interactivity, as well as an Arduino Uno which will handle commands from the Pi and output controls to the motors driving the system.

The final product will function as a blackjack dealer that could easily replace a human at a table. The system’s hardware will include a device that can function as an “arm” and will move a “hand” to move cards around the table. To know what cards are being played, the system’s camera can take a picture of cards as they are being dealt. With this input, the software side of the system will interpret the current state of the game and then prompt the player(s) for their input, which would then further continue the flow of the game’s algorithm. The game as a whole will follow a standard Blackjack ruleset and will incorporate the ability to have multiple players, each able to place bets.

## Group Members
- Kyle Cullen
- Nicholas Lowe
- Curtis Maher
- Luca Mahoney
