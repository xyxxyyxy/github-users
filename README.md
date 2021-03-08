# github-users
## Github Flask Project

[Digital Ocean Deployment](https://test.leonardomoya.xyz/?)

## Usage of API and Web Interface:

### GET PROFILES API
`GET https://test.leonardomoya.xyz/api/profiles`

It returns paginated list of user profiles in JSON format, you can change page and page size along with order by changing parameters:

- ?page=1

- ?limit=25

- ?direction=asc

- ?sort=id

Defaults are shown above. The total is shown too as is the standard.

One can also query the list of users by utilzing the `?username` parameter, it then returns a list of users that partially match the username.

### GET PROFILES HTML
`GET https://test.leonardomoya.xyz/`

It returns paginated list of user profiles, one can change the pagination size and direction of sorting throught the interface as well as by changing URL params:

## Misc
A session was used to be able to keep pagination size and sorting intact throughout requests and reloads.
The file seed.py can be used as follows to populate the database:

`# ./seed.py --total <number>`

It fetches the specified number of records from GitHub's own API and stores them in the DB.

The project is hosted on my personal Droplet in DO and is served through uWSGI and Nginx.

### Technologies Used

- SQLite as DB
- Flask as server
- Pytest for testing
- Bulma for CSS styling
