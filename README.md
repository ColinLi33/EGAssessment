**Problem 2A)** This strategy was used 1 time(s) which is 6.666666666666667 % of rounds played based on this Team2 does not enter the light blue boundary very often on T side. I can trust this answer because if I change the side to CT, I observed a very high rate of this strategy being used and because the boundary is one of the ways CT side gets to BombsiteB it should be pretty commonly used.

**Problem 2B)** # The average time Team2 entered Bombsite B on T side is: 33.625 seconds into the round. I can trust this answer because if I change the site to BombsiteA I can see little to no overlap in round numbers that this strategy is used since it would be quite difficult to have multiple people enter both sites in the same round. Another reason I can trust this answer is because BombsiteA is the CT spawn so I get values of basically 0 seconds into the round that the CT side enters the site.

**Problem 2C)** The heatmap is located in the /heatmap folder. 

I am not extremely confident in the result I got because I found this task to be quite challenging for some reason. I think while my heatmap looks slightly accurate, it is a bit squished in the x direction. I thought it should've been a pretty simple task to translate the coordinates from the game to the image so I can overlay the heatmap, but it seemed to be much harder than I anticipated. I'm not sure how I would make this script work for CSGO every map and every site without some manual inputs because of the challenge to overlay the heatmap on top of the map in order to make it understandable 

**Problem 3)** I would use a library called pyinstaller https://pyinstaller.org/en/stable/ to package the script into an executable. I could add a simple interface that allows for input of a parquet file, and map and lets you outline and label the differnet boundary of interest(s) directly onto the map. I can then take the coordinates from the outline to use for the boundaries to check from while taking
an input for what team/side/area is requested.
