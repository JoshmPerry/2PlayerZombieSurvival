This game was created as a final project for Engineering 102.
All of the code and logic was created by me, but the sprites, level design, and wave design was created by my groupmates.

This game was created entirely in python weighing heavily on a class hierarchy, Pygames is used purely for the display and nothing else.

Because I coded the calculations for collision, movement, and made it redraws the sprites of everything every frame, the game will get rather slow when there is a mob of enemies on the screen. However, thanks to multithreading, it is still infinetly faster than when it was on a single thread.

To run the game you must have python 3.10 or higher installed. Then navigate to the installed folder and run python3 fun_game.py.

The goal of the game is to survive 15 waves. To help you with this journey there are powerups that spawn around the map. Just touch them and you will gain a permanent effect.

Is the game to hard or easy? just edit the zombies.txt or map1.txt/map2.txt to your liking then reload the game.
