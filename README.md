# Summary
 The website and app for ListingsThatFit. ListingsThatFit is a website that emails you ebay clothing listings that fit your sizing information, weekly, from specific sellers. Built as a final project for Harvard's CS50 MOOC. 

Roadmap
------
1. Make database tables
  * Users
    * Shirt size specifics + brands/price guidelines
    * Shoe size specics + brands/price guidelines
    * Jacket size specifics + brands/price guidelines
    * Suit size specifics + brands/price guidelines
    * Pants size specifics + brands/price guidelines
    * Custom keyword watch list
    * Subscribed sellers
  * Sellers
2. Write functions to query ebay with user preferences
3. Write site
  * Registration
  * Preferences
    * Size preferences
    * Subscribed sellers
    * Notification schedule 
4. Have a MVP for the site I've wanted to build since 2014

Rough MVP todo for the minimum needed to email people matches by hand
-----
* [X] BeautifulSoup patterns to match sportcoat measurement templates
* [X] measurementType model
* [X] measurements link table
* [X] fully flesh out items table
* [X] script to scour template using BS and create item entry (only sportcoats for now)
* [X] script to pull down all items and create entries for items
  * [X] parser for suits
  * [X] parser for sportcoats
  * [X] parser for casual shirts
  * [X] parser for dress shirts
  * [X] parser for pants
  * [X] parser for coats and jackets
  * [X] parser for sweaters
* [ ] Script to remove old listings from db
* [X] Measurement + tolerance association table
* [X] Foreign key linkup to above association table
* [X] Query to search for matching listings for User's measurements + tolerances
* [X] Query for listings matching ad-hoc measurements + tolerances
* [ ] plaintext report generation for query results that can be output to an email

Steps to buildout rest of app and deploy
-----
* [ ] Proper logging
* [ ] Some test coverage
* [ ] User account with measurements
* [ ] Integrate user measurements form with site
* [ ] UI to display matching items from current week
* [ ] UI to display matching items for current week PLUS next week
* [ ] UI for results from ad hoc measurements search
* [ ] proper login/out
* [ ] Plaintest report template for emails
* [ ] Email report script and schedule
* [ ] Dev server
* [ ] Prod server
* [ ] CI pipeine for deployment
* [ ] buy URL
* [ ] deploy to server
* [ ] link URL to server