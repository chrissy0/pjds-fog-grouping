# Documentation

## REST API
### Initializing node
#### request
```http
POST /init
```
```json
{
    "cpu_power": 100,
    "storage_byte": 10000000000,
    "ram_byte": 500000000,
    "latitude": 52.520008,
    "longitude": 13.404954
}
```
#### response
```http
200 OK
```
### Requesting node info
#### request
```http
GET /info
```
#### response

```http
200 OK
```

```json
{
    "id": "b159dcc1-4301-4f80-9352-a3601babd420",
    "cpu_power": 100,
    "storage_byte": 10000000000,
    "ram_byte": 500000000,
    "location": {
        "latitude": 52.520008,
        "longitude": 13.404954
    }
}
```
### Updating location
#### request
```http
POST /update_location
```
```json
{
    "latitude": 16.89,
    "longitude": 4.11
}
```
#### response
```http
200 OK
```