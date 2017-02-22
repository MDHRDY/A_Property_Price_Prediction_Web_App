#### A Price Prediction Web App
I recently created a web app,'City Property', that creates price predictions for all residential 
units in New York City. The goal is to outperform Zillow. Zillow's Zestimate is a great tool, 
but it fails to take advantage of the rich geospatial relationships that exist in dense metropolitan areas. 
By accounting for geospatial data, this tool has the capacity to be a more accurate price-predictor
in cities. Currently, only a few features have been built into the model, and the tool already
operates comparatively well against Zillow's. 


The app was deployed with heroku:
https://mdh.herokuapp.com/

It takes awhile for heroku to load the application into memory on their servers, so be
 patient if you click on the link (it's darn slow).
 
The files here contain the front end and the back end for the site. The principal machine learning
algorithms used thus far are k-neareset neighbors and k-means.