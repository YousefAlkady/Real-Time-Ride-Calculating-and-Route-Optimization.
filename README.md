Driver Route Optimization and Live GPS Tracking
What This Project Does
This project started with a simple question: "How do I figure out the best driving route while considering real-world costs?"
I didn’t just want the shortest route; I wanted the one that makes the most sense when I factor in fuel costs, time spent, and potential revenue (similar to how ride-hailing companies like Uber think about trips).

The system fetches driving routes between two locations using the OpenRouteService (ORS) API. Then, I wrote logic to score each route and pick the most optimal one. After that, I added live GPS tracking, so I can simulate (or eventually use real) driver movements along the route.

Why I Built This
I wanted to get hands-on experience working with APIs, data from GPS, and implement this in a future Uber like app project, and something real-world like route optimization. I realized that just using raw coordinates and subtracting numbers doesn’t work because the Earth is curved. So, I implemented the Haversine formula to calculate accurate distances between the driver and the next step in the route. It’s not just a math trick—this is how actual navigation apps measure distances behind the scenes.

Key Features
Route Fetching: Uses ORS geocoding to turn place names (like "Cairo") into GPS coordinates and then fetches possible routes between them.

Route Scoring: Each route is ranked by a score that balances:

Fuel cost (based on distance and fuel efficiency).

Time cost (total driving time).

Estimated revenue (like a simple ride fare model).

Live GPS Tracking: I added a Flask API to simulate a driver’s location in real time. This could easily be replaced by actual GPS data from a phone or car tracker.

Step-by-Step Navigation: The driver’s position is constantly compared to the next step using the Haversine formula to know when they’ve reached it.

How It Works
I input the start and end locations.

The script uses ORS to get coordinates and fetch all route options.

Each route’s cost and time are calculated, and the best one is chosen.

While "driving," the script keeps checking how far I am from the next turn (or step). Once I’m close enough, it moves to the next step.

Why Haversine?
If I just did (lat2 - lat1) and (lon2 - lon1) to find distances, I’d be wrong most of the time because degrees of longitude and latitude don’t translate to equal distances on Earth. The Haversine formula solves this by accounting for Earth’s curvature and gives an accurate straight-line distance between two points on a sphere.

Tech Used
Python (main language).

Requests (to call ORS APIs).

Flask (to simulate live GPS endpoints).

Math module (for Haversine’s trigonometric calculations).

Time module (to simulate real-time updates while moving between steps).

What I Learned
Working with external APIs is all about structuring your requests correctly and handling errors (like when ORS times out).

Haversine is a must-know formula for geospatial projects.

Flask makes it easy to set up a quick local server for GPS updates.

Combining distance, time, and cost into one "score" is how route optimization really works—it’s never just about "shortest distance."

Future Improvements
Add real-time traffic data into the score calculation.

Build a simple mobile app that sends live GPS coordinates to this backend.

Save all trips and analytics into a database for reporting.

## License
This project is proprietary.  
**All rights reserved.**  
You may not copy, modify, or use this project without written permission.

