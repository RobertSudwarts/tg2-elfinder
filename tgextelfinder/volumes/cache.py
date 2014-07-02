"""

from django.core.cache import cache
Gives you a cache...
TG uses beaker -- so we know that that's going to be there
already...

# see: http://beaker.readthedocs.org/en/latest/configuration.html#cache-options
>>> type(cache_mgr)
<class 'beaker.cache.CacheManager'>

>>> type(cache)
<class 'beaker.cache.Cache'>

I'm not happy with any of this....
"""


from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options

# cache_opts = {
#     'cache.type': 'ext:memcached',
#     'cache.url': '127.0.0.1:11211',
#     'cache.data_dir': '/tmp/cache/data',
#     'cache.lock_dir': '/tmp/cache/lock'
# }

cache_opts = {
    'cache.type': 'file',
    'cache.data_dir': '/tmp/cache/data',
    'cache.lock_dir': '/tmp/cache/lock'
}

cache_mgr = CacheManager(**parse_cache_config_options(cache_opts))
cache = cache_mgr.get_cache('elfinder')


#import os
#main_dir = '/home/robertsudwarts/virtualenvs/tg222/src/akadime-v1.0/data/elfinder'

#cache_opts = {
#    'cache.type': 'file',
#    'cache.data_dir': os.path.join(main_dir, 'data'),
#    'cache.lock_dir': os.path.join(main_dir, 'lock')
#}


#cache_opts = {
#    'cache.type': 'ext:memcached',
#    'cache.url': '127.0.0.1:11211',
    # I don't fully understand why these need to be here...
    #'cache.data_dir': os.path.join(main_dir, 'data'),
    #'cache.lock_dir': os.path.join(main_dir, 'lock')
#}
