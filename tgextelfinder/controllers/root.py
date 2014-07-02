# -*- coding: utf-8 -*-
"""Main Controller"""
import logging
import webob
import simplejson as json
from tg import TGController
from tg import expose, flash, response, require, request, redirect,\
               validate, tmpl_context, url, lurl
from tg.i18n import ugettext as _

# import the plugged application's model
from tgext.pluggable import app_model

from tgextelfinder import model
from tgextelfinder.model import DBSession

from ..widgets import ElfinderWidget
from ..conf import settings as ls
from ..connector import ElfinderConnector

# we may want a local version of this decorator
from akadime.controllers.sundry_functions import dump_args

log = logging.getLogger(__name__)

class EntityDocsController(TGController):

    @expose('tgextelfinder.templates.vanilla')
    def index(self, entity_id=None, optionset='default'):
        ''' here you can do the stubs style substitution of the
        template so that the local `master` template can be used
        keeping the whole thing in context
        '''
        # and here you would set your `start_path` based on the entity's
        # doc location
        pass

class RootController(TGController):
    '''
    The root controller should be reserved for generic methods....
    '''

    docs = EntityDocsController()

    # THIS controller is going to move to 'stubs' and
    # but it will still point at url="tgextelfinder/elfinder_controller",
    @expose('tgextelfinder.templates.vanilla')
    def index(self, entity_id=None, optionset='default', start_path='default', alias="Elfinder Files", options=None):
        '''display elfinder widget

        :param optionset string: [default='default']
        :param start_path string: [default='default']
        :param options dict: [default=None] if this is set, it will override
                             the standard options, so use with care!!
                             It would make sense to use json.loads() if
                             this is ever used...

        it would make sense for root folder to be an `Entity.id`.
        By querying Entity.query.get('id') you can use its
        property/method to determine what its 'root' folder is.
        '''

        if entity_id:
            # the plugged application can definitely be called.
            entity = app_model.DBSession\
                            .query(app_model.Entity)\
                            .filter(app_model.Entity.id==entity_id).one()
            E = entity.firstname
            # if we have an entity (and we do !!!! )
            # we can point at the start path...
        else:
            E = "no id supplied"

        # the following class level variables are set so that they're
        # available for use by self.elfinder_controller()
        self.start_path = start_path
        self.optionset = optionset

        # we're going to try and overwrite the 'alias' used in the widget
        self.widgetalias = alias

        if not options:
            options = dict(
                        url="tgextelfinder/elfinder_controller",
                        rememberLastDir=False,
                        lang='en',
                        resizable=False,
                        )

        #tmpl_context.ent = E
        tmpl_context.wdg = ElfinderWidget(id='elfinder-widget', options=options)

        return dict(page="DOCUMENTS", ent_name=E)

    @dump_args
    def render_to_response(self, context, **kw):
        """

        take another look at the **kw above. needed??
        """

        resp = webob.Response()

        kw = {}
        additional_headers = {}

        #create response headers
        if 'header' in context:
            log.info("'header' is in `context`")
            for key in context['header']:
                if key == 'Content-Type':
                    log.info("'key' == `Content-Type`")
                    kw['content_type'] = context['header'][key]
                    resp.headers.update({'Content-type': context['header'][key]})
                elif key.lower() == 'status':
                    log.info("key == 'status'")
                    kw['status'] = context['header'][key]
                    resp.status_int = int(data['header'][key])
                else:
                    additional_headers[key] = context['header'][key]
            del context['header']

        if additional_headers:
            log.info("additional headers: %s", additional_headers)

        #return json if not header
        if not 'content_type' in kw:
            kw['content_type'] = 'application/json'
            resp.headers.update({'Content-type': 'application/json'})

        if 'pointer' in context: #return file
            context['pointer'].seek(0)
            kw['content'] = context['pointer'].read()
            context['volume'].close(context['pointer'], context['info']['hash'])

        elif 'raw' in context and context['raw'] \
                       and 'error' in context and context['error']: #raw error, return only the error list
            kw['content'] = context['error']

        elif kw['content_type'] == 'application/json': #return json
            kw['content'] = json.dumps(context)
            resp.body = json.dumps(context)

        else: #return context as is!
            kw['content'] = context
            resp.body = json.dumps(context)


        for key, value in additional_headers.items():
            resp[key] = value

        return resp

    @dump_args
    def output(self, cmd, src):
        """
        Collect command arguments, operate and return self.render_to_response()

        * `cmd`:  like 'open', 'upload' etc
        * `src`:  the req.GET or req.POST  a <class 'webob.multidict.GetDict'>

        """
        kw = {}

        for name in self.elfinder.commandArgsList(cmd):
            if name == 'request':
                # this line can't be right
                kw['request'] = self.request

            elif name == 'FILES':
                # django uses self.request.FILES, a list of UploadedFile(s)
                # kw['FILES'] = self.request.FILES
                kw['FILES'] = src.getall('upload[]')

            elif name == 'targets':
                #kw[name] = src.getlist('targets[]')
                kw[name] = src.getall('targets[]')
            else:
                arg = name
                if name.endswith('_'):
                    name = name[:-1]
                if name in src:
                    try:
                        kw[arg] = src.get(name).strip()
                    except:
                        kw[arg] = src.get(name)
        kw['debug'] = src['debug'] if 'debug' in src else False

        return self.render_to_response(self.elfinder.execute(cmd, **kw))

    def get_command(self, src):
        """
        Get requested command
        """
        try:
            return src['cmd']
        except KeyError:
            return 'open'

    @dump_args
    def get_optionset(self, **kw):
        set_ = ls.ELFINDER_CONNECTOR_OPTION_SETS[kw['optionset']]

        # override the alias -- this works but you need to
        # destroy thr cache...
        for root in set_['roots']:
            root['alias'] = self.widgetalias

        if kw['start_path'] != 'default':
            for root in set_['roots']:
                root['startPath'] = kw['start_path']
        return set_

    @expose()
    @dump_args
    def elfinder_controller(self, **kw):
        '''
        As we're in TG `request` land rather than WSGI `context` land
        we have to deal with the request type accordingly.

        .. note::
           `ElfinderConnector` takes, as its final parameter, `session`
           to which request.session was sent.  However, `session` is
           unused by the connector and so this parameter is being
           explicitly sent as `None` -- for the avoidance of any doubt
           it was originally passed as `request.session`
        '''


        if 'start_path' not in kw:
            # and there's no reason to suggest that it ever will be...
            kw['start_path'] = self.start_path
        else:
            log.warn("start_path `%s` found in kw", kw['start_path'])

        if 'optionset' not in kw:
            # and (again) there's no reason to suggest that it ever will be...
            kw['optionset'] = self.optionset
        else:
            log.warn("optionset `%s` found in kw", kw['optionset'])

        if request.method == 'GET':
            log.debug("request.GET: %s", request.GET)
            optionset = self.get_optionset(**kw)
            self.elfinder = ElfinderConnector(optionset, None)
            cmd = self.get_command(request.GET)
            return self.output(cmd, request.GET)

        elif request.method == 'POST':
            """
            called in post method calls.
            It only allows for the 'upload' command
            """
            log.info("request.POST: %s", request.POST)
            optionset = self.get_optionset(**kw)
            self.elfinder = ElfinderConnector(optionset, None)

            cmd = self.get_command(request.POST)
            if not cmd in ['upload']:
                self.render_to_response({'error' : self.elfinder.error(ElfinderErrorMessages.ERROR_UPLOAD, ElfinderErrorMessages.ERROR_UPLOAD_TOTAL_SIZE)})

            return self.output(cmd, request.POST)

        else:
            raise NotImplementedError, \
                 "'%s' request.method is not handled" % request.method


