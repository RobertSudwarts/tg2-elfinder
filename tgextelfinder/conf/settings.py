from os.path import join

import tg

from tgextelfinder.utils.accesscontrol import fs_standard_access
from tgextelfinder.volumes.filesystem import ElfinderVolumeLocalFileSystem

class Settings(object):
    '''acts as a proxy for django.conf global settings

    the original asks for 'settings' ie
    `from django from django.conf import settings`

    Essentially this object acts as a proxy for that conf file to which
    ELFINDER_CONNECTOR_OPTION_SETS refers for 'base' settings

    Any parameters here would almost certainly be best coming from
    the .ini file of the **plugged** app

    Note on archivers: as the majority of use will be from windows
    I think it'd be best to limit this to .zip

    'archivers': {
        'create': ['application/zip'],
        'extract': ['application/zip']
        }

    And now we can see why we need to get stuff from the plugged
    application's .ini (or some settings/conf file).
    **The default  path is going to differ for each plugged application**
    '''
    MEDIA_ROOT = 'akadime/public/data'
    MEDIA_URL = 'data'
settings = Settings()

CONNECTOR_OPTION_SETS_DEBUG = True

# here's a thought... Do you want an item in
# roots for every entity???
# Probably not -- the cache would be a nightmare.

ELFINDER_CONNECTOR_OPTION_SETS = {
    # default used with our entity model
    'entity': {
        'debug' : CONNECTOR_OPTION_SETS_DEBUG,
        'roots': [
            {
                'id': 'lffent',
                'driver' : ElfinderVolumeLocalFileSystem,
                'alias' : 'Documents',
                # `path` and 'URL' are both used with
                # os.path.join() to create the correct
                # path for the entity's directory to be established
                # as the 'root'
                'path' : 'akadime/public/data',
                'URL' : '/data/',
                'uploadAllow' : ['all',],
                'uploadDeny' : ['all',],
                'uploadOrder' : ['deny', 'allow'],
                'uploadMaxSize' : '128m',
                'accessControl' : fs_standard_access,
                'attributes' : [
                    {
                        'pattern' : r'\.tmb$',
                        'read' : True,
                        'write': True,
                        'hidden' : True,
                        'locked' : True
                    },
                    {
                        'pattern' : r'\/photos$',
                        'write' : False,
                        'read' : False,
                        'hidden' : False,
                        'locked' : True
                    },
                ],
                'archivers' : {},
                'cache' : 60 * 5,  # seconds * minutes
            }
        ]
    },
    #the default keywords demonstrates all possible configuration options
    #it allowes all file types, except from hidden files
    'default' : {
        'debug' : CONNECTOR_OPTION_SETS_DEBUG, #optionally set debug to True for additional debug messages
        'roots' : [
            #{
            #    'driver' : ElfinderVolumeLocalFileSystem,
            #    'path'  : join(settings.MEDIA_ROOT, 'files'),
            #},
            {
                'id' : 'lff',
                'driver' : ElfinderVolumeLocalFileSystem,
                #'path' : join(settings.MEDIA_ROOT, 'Teacher/399019d4-d025-4a06-b292-4c5a7e78c220'),
                'path' : settings.MEDIA_ROOT, #join(settings.MEDIA_ROOT, 'Teacher/399019d4-d025-4a06-b292-4c5a7e78c220'),
                'alias' : 'Documents',
                #open this path on initial request instead of root path
                #'startPath' : '',
                'URL' : settings.MEDIA_URL,
                #'URL' : '%s/test_plug/public/elfinder_files/' % settings.MEDIA_URL,
                #the depth of sub-directory listings that should return per request
                #'treeDeep' : 1,
                #directory separator. required by client to show paths correctly
                #'separator' : os.sep,
                #directory for thumbnails
                #'tmbPath' : '.tmb',
                #Thumbnails dir URL. Set this if you're storing thumbnails outside the root directory
                #'tmbURL' : '',
                #Thumbnail size (in px)
                #'tmbSize' : 48,
                #Whether to crop (scale image to fit) thumbnails or not.
                #'tmbCrop' : True,
                #thumbnails background color (hex #rrggbb or 'transparent')
                #'tmbBgColor' : '#ffffff',
                #on paste file -  if True - old file will be replaced with new one, if False new file get name - original_name-number.ext
                #'copyOverwrite' : True,
                #if True - join new and old directories content on paste
                #'copyJoin' : True,
                #filter mime types to show
                #'onlyMimes' : [],
                #on upload -  if True - old file will be replaced with new one, if False new file get name - original_name-number.ext
                #'uploadOverwrite' : True,
                #mimetypes allowed to upload
                'uploadAllow' : ['all',],
                #mimetypes not allowed to upload
                'uploadDeny' : ['all',],
                #order to proccess uploadAllow and uploadDeny options
                'uploadOrder' : ['deny', 'allow'],
                #maximum upload file size. NOTE - this is size for every uploaded files
                'uploadMaxSize' : '128m',
                #if True - every folder will be check for children folders, otherwise all folders will be marked as having subfolders
                #'checkSubfolders' : True,
                #allow to copy from this volume to other ones?
                #'copyFrom' : True,
                #allow to copy from other volumes to this one?
                #'copyTo' : True,
                #Regular expression against which all new file names will be validated.
                #'disabled' : [],
                #regexp against which new file names will be validated
                #enable this to allow creating hidden files
                #'acceptedName' : r'.*',
                #callable to control file permissions
                #`fs_standard_access` hides all files starting with .
                'accessControl' : fs_standard_access,
                #default permissions. not set hidden/locked here - take no effect
                #'defaults' : {
                #    'read' : True,
                #    'write' : True
                #},
                'attributes' : [
                    {
                        'pattern' : r'\.tmb$',
                        'read' : True,
                        'write': True,
                        'hidden' : True,
                        'locked' : True
                    },
                    {
                        'pattern' : r'\/photos$',
                        'write' : False,
                        'read' : False,
                        'hidden' : False,
                        'locked' : True
                    },
                    #{
                    #    'pattern' : r'\/my-inaccessible-folder$',
                    #    'write' : False,
                    #    'read' : False,
                    #    'hidden' : True,
                    #    'locked' : True
                    #},
                ],
                #quarantine folder name - required to check archive (must be hidden)
                #'quarantine' : '.quarantine',
                #Allowed archive's mimetypes to create. Leave empty for all available types.
                #'archiveMimes' : [],
                #Manual config for archivers. Leave as an empty dict for auto detect ie
                'archivers' : {},
                # I think that if you want to restrict/specify, the
                # 'archiveMimes' may need to be set...
                # 'archivers': {
                #               'create': ['application/zip'],
                #               'extract': ['application/zip']
                # },
                # #seconds to cache the file and dir data used by the driver
                #'cache' : 600
            }
        ]
    },
    #option set to only allow image files
    'image' : {
        'debug' : CONNECTOR_OPTION_SETS_DEBUG,
        'roots' : [
            {
                'id' : 'lffim',
                'driver' : ElfinderVolumeLocalFileSystem,
                'path' : join(settings.MEDIA_ROOT, u'images'),
                'alias' : 'Elfinder images',
                'URL' : '%simages/' % settings.MEDIA_URL,
                'onlyMimes' : ['image',],
                'uploadAllow' : ['image',],
                'uploadDeny' : ['all',],
                'uploadMaxSize' : '128m',
                'disabled' : ['mkfile', 'archive'],
                'accessControl' : fs_standard_access,
                'attributes' : [
                    {
                        'pattern' : r'\.tmb$',
                        'read' : True,
                        'write': True,
                        'hidden' : True,
                        'locked' : True
                    },
                ],
            }
        ]
    },
    'pdf' : {
        'debug' : CONNECTOR_OPTION_SETS_DEBUG,
        'roots' : [
            {
             'id' : 'pdfset',
                'driver' : ElfinderVolumeLocalFileSystem,
                'path' : join(settings.MEDIA_ROOT, 'pdf'),
                'alias' : 'PDF only',
                'URL' : '%spdf/' % settings.MEDIA_URL,
                'onlyMimes' : ['application/pdf',],
                'uploadAllow' : ['application/pdf',],
                'uploadDeny' : ['all',],
                'uploadMaxSize' : '128m',
                'disabled' : ['mkfile', 'archive'],
                'accessControl' : fs_standard_access,
                'attributes' : [
                    {
                        'pattern' : r'\.tmb$',
                        'read' : True,
                        'write': True,
                        'hidden' : True,
                        'locked' : True
                    },
                ],
             }
        ]
    }
}

# This is not needed unless you want to import an additional
# optionset from elsewhere (ie another conf/settings file)
#ELFINDER_CONNECTOR_OPTION_SETS.update(getattr(settings, 'ELFINDER_CONNECTOR_OPTION_SETS', {}))

# or, you could get this by parsing a distinct conf file.
# try:
#     #var = tg.config.get('elfinder_optionset.default')
#     #print var

#     var = tg.config.items('elfinder_optionset')
#     print var
# except:
#     print "You have a problem..."
