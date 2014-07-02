
tgext.elfinder is a Pluggable application for TurboGears2.
=============================================================

`elFinder`_ is a jQuery web file manager providing standard features -such as
uploading, moving, renaming files etc-, as well as a set of advanced features
such as image resizing/cropping/rotation and archive file creation.




.. _elfinder: http://elfinder.org

Installing
-------------------------------


Plugging tgextelfinder
----------------------------

In your application *config/app_cfg.py* import **plug**::

    from tgext.pluggable import plug

Then at the *end of the file* call plug with `tgextelfinder`::

    plug(base_config, 'tgextelfinder')

You will be able to access the plugged application at
*http://localhost:8080/tgextelfinder*.

Available Hooks
----------------------

tgext.elfinder makes available a some hooks which will be
called during some actions to alter the default
behavior of the appplications:

Exposed Partials
----------------------

tgext.elfinder exposes a bunch of partials which can be used
to render pieces of the blogging system anywhere in your
application:

Exposed Templates
--------------------

The templates used by registration and that can be replaced with
*tgext.pluggable.replace_template* are:

