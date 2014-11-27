
import tw2.core as twc
import tw2.forms as twf
from tw2.jqplugins.ui.base import JQueryUIWidget
from . import base

class ElfinderWidget(JQueryUIWidget):
    '''
    Widget displaying the main Elfinder file manager
    '''
    resources = [base.elfinder_js, base.elfinder_css]

    template = 'mako:tgextelfinder.templates.file_manager'

    options = twc.Param(
            '(dict) A dict of options to pass to the widget', default={})


# This is what's currently used...
# I'm not sure that I'm too keen on ImageButton... It's not a button!!
# class StudentNoPhoto(twf.ImageButton):
#     filename = "/public/images/NoPicture.gif"
#     modname="akadime"

''' tw2.forms.templates.input_field is simply:

<%namespace name="tw" module="tw2.core.mako_util"/>\
<input ${tw.attrs(attrs=w.attrs)}/>
'''

class IDImage(twc.Link, twf.InputField):
    type = "image"
    width = twc.Param('Width of image in pixels',attribute=True, default=None)
    height = twc.Param('Height of image in pixels', attribute=True, default=None)
    alt = twc.Param('Alternate text', attribute=True, default='')
    src = twc.Variable(attribute=True)
    template = "tw2.forms.templates.input_field"

    def prepare(self):
        super(ImageButton, self).prepare()
        self.src = self.link
        self.safe_modify('attrs')
        self.attrs['src'] = self.src  # TBD: hack!



NOIMAGE = "/tw2/resources/akadime/public/images/NoPicture.gif"
IMAGE = "/data/Student/3a068b5b-573b-45f5-ad53-1d737a9615d2/id_image.jpg"


# class PersonIDWidget(twf.ImageButton):
#     modname = 'akadime'
#     filename = '/public/images/NoPicture.gif'

#     person = twc.Param('Person object', default=None)

#     src = twc.Param("image source", default=NOIMAGE)

#     def prepare(self):
#         assert self.person, "A Person object is required"
#         self.filename = IMAGE
#         super(PersonIDWidget, self).prepare()


class PersonIDWidget(twc.Widget):
    '''
    Widget showing a thumbnail image of a `Person`

    This is used for displaying the image used for principal
    identification ie displayed on the Person's main page and used
    for creating id cards.
    Used for students, teachers, staff (and eventually exam candidates)

    '''

    person = twc.Param('Person object', default=None)

    src = twc.Param("image source", default=NOIMAGE)
    
    # a template is required here
    template = 'mako:tgextelfinder.templates.id_image'

    def prepare(self):

        # assert self.person, "A Person object is required"
        # self.src =IMAGE
        # if self.person.id_image:
        #     # will return a `PersonIDImage` model object
        #     # from which you can get the image.
        #     # As the relationship is scalar, we can use this if/else
        #     image = self.person.id_image.image
        #     #self.src = <some image>
            
        # else:
        #     # image not found, then set image to the placeholder
        #     image = "some blank person image"

        super(PersonIDWidget, self).prepare()