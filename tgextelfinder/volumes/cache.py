"""
The cache settings have to come from the plugged application...

Or will the cache simply be standalone?
After all, is there any real need for this
to be defined in the plugged app itself
"""


from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options

cache_opts = {
    'cache.type': 'file',
    'cache.data_dir': '/tmp/cache/data',
    'cache.lock_dir': '/tmp/cache/lock'
}

cache_mgr = CacheManager(**parse_cache_config_options(cache_opts))
cache = cache_mgr.get_cache('elfinder')


