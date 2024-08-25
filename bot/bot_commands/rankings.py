
from config import bot, parser
from .illust import send_illustration
from utils.typing_utils import *
from utils.exceptions import IllustrationNotFound, IllustrationInvinsible

@bot.command(description='Get daily rankings from pixiv')
async def daily(ctx, 
                gender: gender_literal = None,
                r18: r18_literal = None,
                limit : limit_type = None, 
                image_size: image_size_literal = 'medium'): 
    '''Sends daily rankings from pixiv to a Discord channel on /daily
        
    Supports ranking specifications 
      such as gender and filtering R18 arts.

    Args:
        gender: Literal['male', 'female']. Optional. Either male
          or female. Specifies ranking's gender criteria
        r18: Literal['r18']. Optional. Can be specified as r18
          to show r18 artoworks
        limit: int. Optional. Number of illustrations to send
        image_size: Literal['medium', 'large', 'original'].
          By default, set to 'medium'.


    Returns:
        None
    
    Raises (sends Exception message to the channel):
        Illusration not Found if the page for the illustration
          is missing

        Illusration Set to Invinsible if the illust is set to Invinsible
          by either the user or the author   
    '''
    
    
    
    daily_illusts_details = await parser.parse_daily_rankings(gender, r18, limit)


    for illust in daily_illusts_details:
        try:
            illust_id, username, title, tags, image_url = parser.parse_ranking_illust(illust, image_size)
        except (IllustrationInvinsible, IllustrationNotFound) as e:
            await ctx.send(e)
            return

        await send_illustration(ctx, illust_id, username, title, tags, image_url)



@bot.command(description = 'Get weekly rankings from pixiv')
async def weekly(ctx,
                 details: weekly_details_literal,
                 limit: limit_type,
                 image_size: image_size_literal = 'medium'):
    '''Sends weekly rankings from pixiv to a Discord channel on /weekly
    
    Supports ranking specifications 
      such as artist experience and filtering R18 arts.

    Args:
        details: Literal['rookie', 'r18']. Optinal. Weekly ranking specification.
          Either rookie (arts by amateur artists) or r18
        limit: int. Optional. Number of illustrations to send
        image_size: Literal['medium', 'large', 'original'].
          By default, set to 'medium'.

    Returns:
        None

    Raises:
        Illusration not Found if the page for the illustration
          is missing

        Illusration Set to Invinsible if the illust is set to Invinsible
          by either the API user or the author 
    '''

    weekly_illusts_details = await parser.parse_weekly_rankings(details, limit)

    for illust in weekly_illusts_details:
        try:
            illust_id, username, title, tags, image_url = parser.parse_ranking_illust(illust, image_size)
        except (IllustrationInvinsible, IllustrationNotFound) as e:
            await ctx.send(e)
            return

        await send_illustration(ctx, illust_id, username, title, tags, image_url)
   


@bot.command(description = 'Get monthly rankings from pixiv')
async def monthly(ctx, 
                  limit: limit_type, 
                  image_size: image_size_literal = 'medium'):
    '''Sends monthly rankings from pixiv to a Discord channel on /monthly

      Does not support specifications

    Args:
        limit: int. Optional. Number of illustrations to send
        image_size: str. By default, set to 'medium'

    Returns:
        None
    
    Raises:
        Illusration not Found if the page for the illustration
          is missing

        Illusration Set to Invinsible if the illust is set to Invinsible
          by either the user or the author   
    '''

    monthly_illust_details = await parser.parse_monthly_rankings(limit)

    for illust in monthly_illust_details:
        try:
            illust_id, username, title, tags, image_url = parser.parse_ranking_illust(illust, image_size)
        except (IllustrationInvinsible, IllustrationNotFound) as e:
            await ctx.send(e)
            return

        await send_illustration(ctx, illust_id, username, title, tags, image_url)
