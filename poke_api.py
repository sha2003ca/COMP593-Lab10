'''
Library for interacting with the PokeAPI.
https://pokeapi.co/
'''
import requests
import image_lib
import os
 
POKE_API_URL = 'https://pokeapi.co/api/v2/pokemon/'
 
def main():
    # Test out the get_pokemon_into() function
    # Use breakpoints to view returned dictionary
    #poke_info = get_pokemon_info("Rockruff")
    #poke_info = get_pokemon_info(123)
    names= get_pokemon_names()
    download_pokemon_artwork('ditto', r'D:\py\lab 10\images')

    return
 
def get_pokemon_info(pokemon_name):
    """Gets information about a specified Pokemon from the PokeAPI.
 
    Args:
        pokemon_name (str): Pokemon name (or Pokedex number)
 
    Returns:
        dict: Dictionary of Pokemon information, if successful. Otherwise None.
    """
    # Clean the Pokemon name parameter by:
    # - Converting to a string object, 
    # - Removing leading and trailing whitespace, and
    # - Converting to all lowercase letters
    pokemon_name = str(pokemon_name).strip().lower()
 
    # Build the clean URL for the GET request
    url = POKE_API_URL + pokemon_name
 
    # Send GET request for Pokemon info
    print(f'Getting information for {pokemon_name}...', end='')
    resp_msg = requests.get(url)
 
    # Check if request was successful
    if resp_msg.status_code == requests.codes.ok:
        print('success')
        # Return dictionary of Pokemon info
        return resp_msg.json()
    else:
        print('failure')
        print(f'Response code: {resp_msg.status_code} ({resp_msg.reason})')         
        return
 
def get_pokemon_names(offset=0, limit=100000):
    query_str_params = {
        'offset' :offset,
        'limit' :limit
    }
    print(f'Getting list of pokemon names...', end='')
    resp_msg = requests.get(POKE_API_URL, params=query_str_params)

    if resp_msg.status_code == requests.codes.ok:
        poke_dict = resp_msg.json()
        poke_names_list = [p['name'] for p in poke_dict['results']]
        return poke_names_list
    else:
        print('failure')
        print(f'Response code: {resp_msg.status_code} ({resp_msg.reason})')
        return
    
def download_pokemon_artwork(pokemon_name, save_dir):

    #Get all info for the specified Pokemon
    pokemon_info = get_pokemon_info(pokemon_name)
    if pokemon_info is None:
        return
    
    #Extract the artwork URL from the info dictionary
    artwork_url = pokemon_info['sprites']['other']['official-artwork']['front_default']

    # Download the artwork
    image_bytes = image_lib.download_image(artwork_url)
    if image_bytes is None:
        return
    
    # Determine the image file path
    file_ext =  artwork_url.split('.')[-1]
    image_path = os.path.join(save_dir, f'{pokemon_name}.{file_ext}')

    # Save the image file
    if image_lib.save_image_file(image_bytes, image_path):
        return image_path

if __name__ == '__main__':
    main()