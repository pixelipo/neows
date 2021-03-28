# NeoWs

## About
This is a simple project to practice writing API consumers in Python3.

It is using [NASA](https://api.nasa.gov/)'s NeoWs web service to fecth data locally.

Plan is to store this data in a local database and later visualize it with some JS library

## Usage
Application will work out of the box with the predefined demo API key, with very limited request count.
You should sign up for a free API key at [NASA](https://api.nasa.gov/) for a generous 1000 requests/hour.
API key should be placed in a `env/conf.py` file like this:

```
config = {
    "api_key": "your-private-api-key"
}
```

App offers 4 modes:
- **[1] Browse**: Get data from API and into DB
- **[2] Lookup**: TODO
- **[3] Feed**: TODO
- **[4] Generate plot data**: Format data into Google Charts readable format

Start the app by running `python3 main.py` from root folder. Select appropriate mode and wait for "success".


## Example

![alt text](sample.png?raw=true)
