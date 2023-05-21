```
docker network create app_main 
docker-compose up -d --build
```

API Documentation

http://0.0.0.0:8000/docs

Backend Implementation:

* [X] Set up a FastAPI project.
* [ ] Create an endpoint at `/iss/sun` that fetches the ISS data from the provided API and calculates the time windows when the ISS was exposed to the sun.
* [X] Implement rate limiting logic to ensure the API is not called more than once every 20 seconds.
* [X] Create an endpoint at `/iss/position` that retrieves the latitude and longitude of the ISS at the present time.
* [X] Implement in-memory storage to store the ISS data or use a database if desired.
* [ ] Write unit tests to ensure the correctness of the endpoints and functionality.
* [ ] Document the architecture of the solution with a diagram.

Frontend Implementation:

1. [X] Set up a Vue 3 project with Nuxt 3 and Tailwind CSS.
2. [X] Create a full-screen map using a map library like Mapbox or OpenLayers.
3. [X] Fetch the live position of the ISS from the backend endpoint `/iss/position`.
4. [X] Display the ISS position on the map in real-time.
5. [ ] Fetch the time windows when the ISS was exposed to the sun from the backend endpoint `/iss/sun`.
6. [ ] Present the sun exposure information in a neat and clear format, such as popups on hover or a list on the side.
