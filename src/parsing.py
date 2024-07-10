'''A module that parses data from the PixivAPI.

This module was designed to parse and return only some
  parts of the data fetched from the PixivAPI necessary
  for the Discord bot.

'''

async def parse_illust_detail(illust_detail, image_size):
    '''Parses the illust json and return necessary data.

    Returns the name of the artwork, its author's username,
      image URLS and tags.

    Args:
        illust_detail: ParsedJson from PixivAPI's response.
        image_size: str. Possible values: medium, large, square, etc.
    
    Returns:
        A tuple of all of the aforementioned information about 
          the illustration.

        Example:
        ('username108', 'First art', 'pximg.net/228.png', 
        [
          {'name': '...',
          'translated_name': '...'} 
        ])

    Raises:
        Illusration not Found Exception if the page for the illustration
          is missing

        Illusration Set to Invinsible if the visible key of illust_detail is False
    '''
    
    if illust_detail.get('error'):
        raise(Exception('Illusration not Found'))
    if not illust_detail['illust']['visible']:
        raise(Exception('Illusration Set to Invinsible'))

    username = illust_detail['illust']['user']['name']
    title = illust_detail['illust']['caption']
    image_url = illust_detail['illust']['image_urls'][image_size]
    tags = illust_detail['illust']['tags']

    return username, title, image_url, tags


def display_tags(ctx, tags: dict):
    '''Sends a string of tags to the Discord channel

    Iterates over each tag and attaches its translation
      if provided on Pixiv. Then, all of the tags are
      concatenated into a single string

    Args:
        tags: a list of dict objects with 2 keys: 
          name and translated_name

    Returns:
        A string of concatenated tags

    '''
    tags_text = 'Tags: '

    tags_list = []
    for tag in tags:
        if tag['translated_name']:
            tags_list.append(tag['name'] + ' - ' + tag['translated_name'])
        else:
            tags_list.append(tag['name'])
    tags_text += ', '.join(tags_list)
    return ctx.send(tags_text)
