'''A module that parses data from the PixivAPI.

This module was designed to parse and return only some
  parts of the data fetched from the PixivAPI necessary
  for the Discord bot.

'''
import pixivpy_async
import pixivpy3

import typing

from utils.typing_utils import (
    image_size_literal,
    gender_literal,
    r18_literal,
    limit_type,
    weekly_details_literal
)
from utils.exceptions import (
    IllustrationNotFound,
    IllustrationInvinsible
)

class PixivParser:
    def __init__(self, api: pixivpy_async.AppPixivAPI | pixivpy3.AppPixivAPI):
        self.api = api
    

    def parse_illust_detail(self, illust_detail : dict, image_size: image_size_literal = 'medium'):
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
        
        pass


    async def parse_illust(self, illust_id : int, image_size : image_size_literal):
        illust_detail = await self.api.illust_detail(illust_id)

        if illust_detail.get('error'):
            raise IllustrationNotFound

        if illust_detail.get('illust'):
            illust_detail = illust_detail['illust']

        if not illust_detail['visible']:
            raise IllustrationInvinsible

        username = illust_detail['user']['name']
        title = illust_detail['title']
        tags = self._concat_tags(illust_detail['tags'])
        image_url = self._get_image_url(illust_detail, image_size)

        return username, title, tags, image_url


    def parse_ranking_illust(self, illust_detail : dict, image_size : image_size_literal):
        if illust_detail.get('error'):
            raise IllustrationNotFound

        if illust_detail.get('illust'):
            illust_detail = illust_detail['illust']

        if not illust_detail['visible']:
            raise IllustrationInvinsible

        illust_id = illust_detail['id'] 
        username = illust_detail['user']['name']
        title = illust_detail['title']
        tags = self._concat_tags(illust_detail['tags'])
        image_url = self._get_image_url(illust_detail, image_size)

        return illust_id, username, title, tags, image_url


    async def base_parse_ranking(self, mode, limit : limit_type):
        json_data = await self.api.illust_ranking(mode) 
        json_data = json_data['illusts']

        filtered_json_data = list(filter(lambda artwork: artwork['type'] == 'illust', json_data))

        if limit:
            filtered_json_data = filtered_json_data[:limit]

        return filtered_json_data


    async def parse_daily_rankings(self, gender : gender_literal, r18 : r18_literal, limit : limit_type):
        mode = 'day'
        if gender is not None:
            mode = mode + '_' + gender
        if r18 is not None:
            mode = mode + '_' + 'r18'

        daily_illusts_details = await self.base_parse_ranking(mode=mode, limit=limit)

        return daily_illusts_details 


    async def parse_weekly_rankings(self, details : weekly_details_literal, limit : limit_type):    
        mode = 'week'

        if details:
            mode = mode + '_' + details
        
        weekly_illust_details = await self.base_parse_ranking(mode=mode, limit=limit)

        return weekly_illust_details


    async def parse_monthly_rankings(self, limit : limit_type):
        mode = 'month'
        
        monthly_illust_details = await self.base_parse_ranking(mode=mode, limit=limit)

        return monthly_illust_details


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


    def _get_image_url(self, illust_detail : dict, image_size : typing.Literal['medium', 'large', 'original'] = 'medium'):
        if image_size == 'original':
            if illust_detail.get('meta_single_page'):
                image_url = illust_detail['meta_single_page']['original_image_url']
            else:
                image_url =  illust_detail['meta_pages'][0]['image_urls']['original']
        else:
            image_url = illust_detail['image_urls'][image_size]

        return image_url
