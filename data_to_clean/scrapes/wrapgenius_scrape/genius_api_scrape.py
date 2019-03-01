import requests
import urllib3

# Format a request URI for the Genius API
search_term = 'Pharrell Williams'
_URL_API = "https://api.genius.com/"
_URL_SEARCH = "search?q="
querystring = _URL_API + _URL_SEARCH + urllib3.quote(search_term)
request = urllib3.Request(querystring)
request.add_header("Authorization", "Bearer " + "QCTZcs3-blT5SAEl7fNMiDl5akwYg_CPJEPRCESFkucbMw2hIt5lhJnGwtjCQiwf")
request.add_header("User-Agent", "")