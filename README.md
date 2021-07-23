# geo_web
First we scrapped info from https://www.seg-social.es/wps/portal/wss/internet/CalendarioLaboral to local JSON<p>
After that I created a little Django project.<p>
<div><ul>  
  <li>1- We get location (it's necessary to activate get location from browser)</li>
  <li>2- We get the city from location</li>
  <li>3- We get from city if it's holiday to day or not from json</li>
  <li>4- We create calendary from json for that city</li>
  <li>5- We calculate next holiday</li>
  <li>6- We create a form to select city and recalc</li>
  <ul><p></div>
  
I want to create more projects but in future:<p>
How to expand the scope? Next steps?<p>
  <ol>
    <li>Expand to database (sqlite or PostgreSQL)</li>
    <li>Set the location from each city in database</li>
    <li>If location city is not in seg_social calendar, check nearest city and show it</li>
    <li>Show regions as filter</li>
    <li>View locations where is holiday that day</li>
    <li>View stadistics cities with more holidays, days where is holiday in more cities, etc...</li>
  </ol>
