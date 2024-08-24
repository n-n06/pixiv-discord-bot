'''A module that parses data from the PixivAPI.

This module was designed to parse and return only some
  parts of the data fetched from the PixivAPI necessary
  for the Discord bot.

'''
import typing
import pixivpy3

class PixivParser():
    def __init_(self, api: pixivpy3.AppPixivAPI):
        self.api = api
    

    def parse_illust_detail(self, illust_detail, image_size: typing.Literal['medium', 'large', 'original'] = 'medium'):
        '''Parses the illust json and return necessary data.

        Returns the title of the artwork, its author's username,
          image URLS and tags. Can be used for both single illustrations
          and multiple illustrations(in case of daily rankings)

        Args:
            illust_detail: ParsedJson from PixivAPI's response.
            image_size: str. Possible values: medium, large, square, etc.
        
        Returns:
            values: A tuple of all of the aforementioned information about 
              the illustration.

        Raises:
            Illusration not Found Exception if the page for the illustration
              is missing

            Illusration Set to Invinsible if the visible key of illust_detail is False
        '''
        
        if illust_detail.get('error'):
            raise(Exception('Illusration Not Found'))

        if illust_detail.get('illust'):
            illust_detail = illust_detail['illust']

        if not illust_detail['visible']:
            raise(Exception('Illusration Set to Invinsible'))


        illust_id = illust_detail['id']
        username = illust_detail['user']['name']
        title = illust_detail['title']
        if image_size == 'original':
            if illust_detail.get('meta_single_page'):
                image_url = illust_detail['meta_single_page']['original_image_url']
            else:
                image_url =  illust_detail['meta_pages'][0]['image_urls']['original']
        else:
            image_url = illust_detail['image_urls'][image_size]
        tags = self._concat_tags(illust_detail['tags'])
        values = (illust_id, username, title, image_url, tags)


        return values
    
    def parse_daily_rankings(self, gender, r18, limit):
        mode = 'day'
        if gender:
            mode = mode + '_' + gender
        if r18:
            mode = mode + '_' + 'r18'

        json_data = self.api.illust_ranking(mode)['illusts']

        #filtering out non-illust artworks
        daily_illusts_details = list(filter(lambda artwork: artwork['type'] == 'illust', json_data))
            
        if limit:
            daily_illusts_details = daily_illusts_details[:limit]

        return daily_illusts_details

    def _parse_daily_args(self, args: str):
        args = args.lower()
        mode = 'day'

        if 'male' in args:
            mode += '_male'
        elif 'female' in args:
            mode += '_female'
        
        if 'r18' in args :
            mode += '_r18'

        return mode
            
    def parse_weekly_rankings(self):
        pass

    def parse_monthly_rankings(self):
        pass

    def _concat_tags(self, tags) -> str:
        '''Adds tags up into a sinlge string

        Args:
            tags: a list of dict objects with 2 keys: 
              name and translated_name

        Returns:
            tags_text: A string of concatenated tags

        '''
        tags_text = 'Tags: '

        tags_list = []
        for tag in tags:
            if tag['translated_name']:
                tags_list.append(tag['name'] + ' - ' + tag['translated_name'])
            else:
                tags_list.append(tag['name'])
        tags_text += ', '.join(tags_list)
        return tags_text
