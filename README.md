# geo_web
First we scrapped info from https://www.seg-social.es/wps/portal/wss/internet/CalendarioLaboral to local JSON
After that I created a little Django project.
1- We get location (it's necessary to activate get location from browser)
2- We get the city from location
3- We get from city if it's holiday to day or not from json
4- We create calendary from json for that city
5- We calculate next holiday
6- We create a form to select city and recalc

I want to create more projects but in future:
How to expand the scope? Next steps?
1- Expand to database (sqlite or PostgreSQL)
2- Set the location from each city in database
3- if location city is not in seg_social calendar, check nearest city and show it
4- Show regions as filter
5- View locations where is holiday that day
6- View stadistics cities with more holidays, days where is holiday in more cities, etc...
