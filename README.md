## Mars Rover Photo Downloader

This small app downloads the photos from the Mars Rover API and save it in the local files system arranged by the Year/month/day manner. 

API - https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/latest_photos

API Key - Generate from https://api.nasa.gov

### Run the application - With Docker

This application uses Docker and Docker Compose. Make sure you have docker in your local system and then run the following command in your terminal


```
docker-compose up -d
```

This will execute the script, download the photos and insert them to the db. 
