import http.client

conn = http.client.HTTPSConnection("serauth.eu.auth0.com")

payload = "{\"client_id\":\"C5JM57aUDL4AriIi6KSYde79hJ0f1b8V\",\"client_secret\":\"8A5qtyFKXWBIhc9n7Ul847iPa22KaOjjx2F0dpIQB1dr-Lpx4sCylvUPHiUEjjvg\",\"audience\":\"drinks\",\"grant_type\":\"client_credentials\"}"

headers = { 'content-type': "application/json" }

conn.request("POST", "/oauth/token", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
