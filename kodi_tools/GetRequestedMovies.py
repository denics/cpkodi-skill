from mycroft.util.log import LOG
import requests
import json
import re
import splitter
# requires apt-get install libenchant1c2a


def get_requested_movies(kodi_path, search_words):
    """
        Searches the Kodi Library for movies that contain all the words in movie_name
    """
    # Build the filter from each word in the movie_name
    LOG.info('get_requested_movies searching for: ' + str(search_words))
    filter_key = []
    for each_word in search_words:
        search_key = {
            "field": "title",
            "operator": "contains",
            "value": each_word
        }
        filter_key.append(search_key)
    # Make the request
    json_header = {'content-type': 'application/json'}
    method = "VideoLibrary.GetMovies"
    kodi_payload = {
        "jsonrpc": "2.0",
        "method": method,
        "id": 1,
        "params": {
            "properties": [
            ],
            "filter": {
                "and": filter_key
            }
        }
    }
    try:
        kodi_response = requests.post(kodi_path, data=json.dumps(kodi_payload), headers=json_header)
        LOG.info(kodi_response.text)
        movie_list = json.loads(kodi_response.text)["result"]["movies"]
        LOG.info('GetReqeustedMovies found: ' + str(movie_list))
        # remove duplicates
        clean_list = []  # this is a dict
        for each_movie in movie_list:
            movie_title = str(each_movie['label'])
            info = {
                "label": each_movie['label'],
                "movieid": each_movie['movieid']
            }
            if movie_title.lower() not in str(clean_list).lower():
                clean_list.append(info)
            else:
                if len(each_movie['label']) == len(movie_title):
                    print('found duplicate')
                else:
                    clean_list.append(info)
        return clean_list  # returns a dictionary of matched movies
    except Exception as e:
        print(e)
        return None
