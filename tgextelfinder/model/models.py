from sqlalchemy import Table, ForeignKey, Column, types
from sqlalchemy.types import TypeDecorator, String
from sqlalchemy.orm import backref, relationship

from tgextelfinder.utils.volumes import get_path_driver
from tgextelfinder.model import DeclarativeBase
from tgext.pluggable import app_model, primary_key, LazyForeignKey

from .guid import GUID

import logging

# class ElfinderFormField(django.forms.CharField):
#     '''
#     django.forms.CharField is a form widget ie something like <input>

#     This may be very useful later...
#     '''
#     pass

log = logging.getLogger(__name__)


class ElfinderFile(object):
    '''
    Represents an Elfinder file
    '''
    def __init__(self, hash_, optionset):
        self.hash = hash_
        self.optionset = optionset
        self._info = None

    def _get_info(self):
        if self._info is None:

            if not self.hash:
                self._info = {}
            else:
                driver = get_path_driver(self.hash, self.optionset)
                try:
                    info = driver.options(self.hash)
                    info.update(driver.file(self.hash))

                    #get image dimensions
                    if not 'dim' in info and 'mime' in info and info['mime'].startswith('image'):
                        info['dim'] = driver.dimensions(self.hash)

                    #calculate thumbnail url
                    if 'tmb' in info and 'tmbUrl' in info:
                        info['tmb'] = '%s%s' % (info['tmbUrl'], info['tmb'])
                        del info['tmbUrl']

                    if 'archivers' in info:
                        del info['archivers']

                    if 'extract' in info:
                        del info['extract']

                    self._info = info
                except:
                    self._info = { 'error' : _('This file is no longer valid') }

        return self._info

    @property
    def url(self):
        """
        Get the file url.
        """
        info = self._get_info()
        return info['pathUrl'] if 'pathUrl' in info else ''

    @property
    def info(self):
        """
        Returns:
            a **dictionary** holding information about the file,
            as returned by the volume driver.
        """
        return self._get_info()

    def __unicode__(self):
        return self.hash


class ElfinderField(TypeDecorator):
    '''Custom SQLAlchemy field type which returns an ElfinderFile object

    The database record here is simply a string (VARCHAR 100)

    http://docs.sqlalchemy.org/en/rel_0_9/core/types.html#augmenting-existing-types

    .. code-block:: python

       import transaction
       from tgextelfinder.model import ProjectFile
       from test_plug.model import *
       proj = ProjectFile(name="cherries", content="some really long string", myfield=u"cherries")
       DBSession.add(proj)
       transaction.commit()

    This still isn't doing the right thing... somehow, `length` (ie 100)
    is being popped off and inserted where `optionset` should be.
    '''

    impl = String

    #def __init__(self, optionset='default', start_path=None, *args, **kw):
    def __init__(self, wibble=None, optionset='default', *args, **kw):
        TypeDecorator.__init__(self, *args, **kw)
        #super(ElfinderField, self).__init__()
        self.optionset = optionset
        self.wibble = wibble
        
        #self.start_path = kw['start_path']

    def process_bind_param(self, value, dialect):
        return value

    def process_result_value(self, value, dialect):
        '''
        Convert ``value`` to an ElfinderFile object.

        effectively the same as the `to_python` method in the yawd version
        '''

        if isinstance(value, ElfinderFile):
            # I cant see *when* this would ever be the case
            return value

        return ElfinderFile(hash_=value, optionset=self.optionset) if value \
                                                                   else None

    def copy(self):
        return ElfinderField(self.impl.length)



class PersonIDImage(DeclarativeBase):
    '''A one-to-one relationship to Person.

    .. note::
       `uselist=False creates a scalar relationship 

    Notice that rather than using the Postgresql specific column type, 
    here, were using the (agnostic) GUID Type Decorator. The reason for 
    this is simply that for testing purposes (and hence when using 
    sqlite as the database) this is the easier option...
    There's no real reason not to come back and change this.

    .. code-block:: python

from akadime.model import *      
import transaction
from tgextelfinder.model import PersonIDImage
P = Person.query.get('3a068b5b-573b-45f5-ad53-1d737a9615d2')
P.id_image = PersonIDImage(image="xyz")
transaction.commit()
P = Person.query.get('3a068b5b-573b-45f5-ad53-1d737a9615d2')
pid = P.id_image
im = pid.image

from test_plug.model import *
proj = ProjectFile(name="cherries", content="some really long string", myfield=u"cherries")
DBSession.add(proj)
transaction.commit()


    '''
    __tablename__ = 'people_images'
    
    id = Column(types.Integer, primary_key=True)

    #person_id = Column(GUID, 
    #                   LazyForeignKey(lambda:app_model.Person.id))

    
    image = Column(ElfinderField(length=100, optionset='image'))
    

    #person = relationship(lambda: app_model.Person, 
    #                      backref=backref('id_image', uselist=False))



# class ProjectFile(DeclarativeBase):
#     '''
#     :param name string:
#     :param content text:
#     :param anyfile ElfinderField:
#     :param image ElfinderField:
#     :param pdf ElfinderField:

#     You may also want to consider adding a UUID with a
#     many to one relationship to `Entity`.

#     The proxy for this is found in yawd example_project/test+app/models.py
#     (in other words, this)

#     Question: why do we need 3 ElfinderFields ?
#     '''
#     __tablename__ = 'project_files'
#     id = Column(types.Integer, primary_key=True)
#     name = Column(types.String(100))
#     content = Column(types.Text)

#     # once you have this custom field type working properly,
#     # you should then be able to add the three fields below.
#     myfield = Column(ElfinderField(length=100))

    #anyfile = Column(ElfinderField(help_text='This is the default configuration'))
    #image = Column(ElfinderField(optionset='image',
    #                      help_text='This field uses the "image" optionset'))
    #pdf = Column(ElfinderField(optionset='pdf', blank=True, null=True,
    #                    help_text='This field uses the "pdf" custom optionset, ' \
    #                    'set in the project settings file'))
