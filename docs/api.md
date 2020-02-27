# Usage collector API

### POST /api/activate/<key>

Track an "activate" event for a given key

### POST /api/deactivate/<key>

Track a "deactivate" event for a given key

### POST /api/use/<key>/<duration>

Track a "usage" fr a given key. Duration values will just be summed up. 
There is no defined semantics for duration. It only has to be a non-negative number. 
You can track time (e.g. seconds, hours, days), but feel free to use it for whatever
you like. Yes, you can also count apples and oranges with this.

### POST /api/clear

Clears all data

### POST /api/store

Data are being stored in memory and only saves to disc form time to time. This means, you might
loose some values if the system stops. 
This is a design choice as loosing some data is not be critical. If you want to store the 
data to disk at a specific point in time, this API call the way to do this. 
If the daemon gets killed gracefully (using the TERM signal), it automatically stored the 
database to disk. There is no need to use the API in this case.

## POST /api/restore

Restores the database from disk. Settings in memory will be lost. There is usually no need at 
all to use this. 

### GET /api/record/<key>

Retrieves data for a given key

### GET /api/keys

Retrives all keys

### GET /api/dump

Gets the whole database
