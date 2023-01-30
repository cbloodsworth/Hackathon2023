# SwampInvestigator
In a procedurally generated swamp, one Investigator is determined to find the fabled Golden Gator statue. Can you brave the unknown and gather the resources necessary to bring you closer to the idol? 

# To Install
Clone the repository using `git clone https://github.com/cbloodsworth/SwampInvestigator`. Run main.py and you should be good to go!

Inspiration
When we were considering the concept of "exploring the unknown," the first thing that came to mind was procedural generation. We eventually came to the conclusion that it would be most fun if we were to make a game around it.

## What it does
This Python project uses Perlin algorithms to generate pseudo-random static that is then layered on top of itself and given elevation and temperature values to simulate real-world ecology and biomes. This creates the environment that the player can explore. There are materials to find in certain biomes and a minimap to keep track of where the player has been.

## How we built it
The first order of business was to familiarize ourselves with the central Python library behind most of this: pygame. We used this as our front-end and were able to make it to our liking. Additionally, it was necessary to familiarize ourselves with the concept of Perlin algorithms and how they work, so we could take the "meaningless" static it generates and create realistic, automatically generated worlds.

## Challenges we ran into
One of the drawbacks that we found with pygame was the fact that rather than having a viewport that you could move around with your character, you had to move the entire background in the opposite direction as the player. For the pieces of land that slow down your character we needed some way to translate player screen position to grid location data, which was harder than expected. Nonetheless, we were able to reverse a few values and we got it working great.

## Accomplishments that we're proud of
We are really proud of how the use of the algorithm turned out. Procedural generation has always been kind of a black box for us, so it was great to get some hands-on experience with it. We are also both relatively inexperienced in Python, so it we are really proud of ourselves for sticking through.

## What we learned
We learned that game development libraries for programming languages are far more difficult to interact with than full game development program suites like Unreal or Unity. Additionally, we learned how to use libraries and read documentation that we have very little experience with, as well as the ins and outs of Python.

## What's next for Swamp Investigator
We would like to add more of pretty much everything. We want to create a larger world with more randomly generated items, more crafting recipes, some enemies and a battle system, caves, a proper end-game (outside of finding the trophy, of course) and much more. Additionally, we want to work on adding music and proper spritework.
