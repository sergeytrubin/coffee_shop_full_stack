import http.client

conn = http.client.HTTPConnection("127.0.0.1:5000")

headers = { 'authorization': "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InVKZkpWTUEyb2FDWDFuaERwWGpFOSJ9.eyJpc3MiOiJodHRwczovL3NlcmF1dGguZXUuYXV0aDAuY29tLyIsInN1YiI6IkM1Sk01N2FVREw0QXJpSWk2S1NZZGU3OWhKMGYxYjhWQGNsaWVudHMiLCJhdWQiOiJkcmlua3MiLCJpYXQiOjE1OTIzMjg1NzEsImV4cCI6MTU5MjQxNDk3MSwiYXpwIjoiQzVKTTU3YVVETDRBcmlJaTZLU1lkZTc5aEowZjFiOFYiLCJndHkiOiJjbGllbnQtY3JlZGVudGlhbHMifQ.dK0OZHlFyft26nzrXdfVeBNi3_sHOjNC3-7x_CgFpmzl0CJA6A_IxaxVtGut3augM2N1E4qQ2KpcZptl5UQjDxl4u4y1gGlb-DbF1zc-V5sQwL1RgF0TnhFo4O4AJ9oiGBtyZHen4UwzivghxTLzYM2C-y5XFUddN6JT--9qYLsZQqHnh4Lyuj6NdzRYRXr0uV-sH1jD3VFrrN4pcibrxfkfySiRvRaeS7Pemp3jZaeKr8aCwOTGpjsLVYTPZ6oroRhw_mnB7GEZW5B7b19ONG1GanxHPnI717ai85I-Z713fRcYQDbhJWaqTvLFVusfaC9y5Xm99krpG00ffJNgAg" }

conn.request("GET", "/drinks-detail", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
