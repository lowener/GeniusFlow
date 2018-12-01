# GeniusFlow

Analyze the flow of Rap Genius artists. This repo contains two scripts:
- `./generator` is supposed to only generate all the lyrics of an artist.
- `./geniusflow` will additionnaly do a frequency analysis to find the most common
  words used by an artist.


# Usage

With your RapGenius API key in the file *key_api.txt*

`./geniusflow [Artist] [Nb tracks]`


# Requirements

`pip install -r requirements.txt`

* Python 3
* BeautifulSoup
* nltk
* requests

You must also have an API key from https://genius.com/.

# Special Notes for TMLN courses

You can use the specially modified script `./json_generator [Artist] [Nb_tracks]`
to create json files already formatted to be inserted in ElasticSearch.

## Example: `
./json_generator Orelsan 10`
Will create the file `Orelsan10.json`. It can be added to ElasticSearch
by using the command:

`curl -vvv -H 'Content-Type: application/x-ndjson' -XPOST 'http://localhost:9200/_bulk?pretty' --data-binary @Orelsan10.json`
