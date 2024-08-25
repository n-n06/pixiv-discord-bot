import typing

image_size_literal = typing.Literal['medium', 'large', 'original'] 
gender_literal = typing.Optional[typing.Literal['male', 'female']] 
r18_literal = typing.Optional[typing.Literal['r18']]  
limit_type = typing.Optional[int] 

weekly_details_literal = typing.Optional[typing.Literal['rookie', 'r18']]
