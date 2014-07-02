from nose.tools import *
from tgextelfinder.connector import ElfinderConnector
from tgextelfinder.conf import settings as ls
from tgextelfinder.exceptions import ElfinderErrorMessages

class TestConnectorInit(object):

    def test_init(self):

        # fault tolerant initialisation
        connector = ElfinderConnector({})
        assert_false( connector.loaded() )

        # initialise with the default optionset
        connector = ElfinderConnector(ls.ELFINDER_CONNECTOR_OPTION_SETS['default'])
        assert_true( connector.loaded() )


    def test_execute_with_invalid_configuration(self):

        connector = ElfinderConnector({})
        assert_in(ElfinderErrorMessages.ERROR_CONF, connector.execute('open')['error'])

    def test_execute(self):

        connector = ElfinderConnector(ls.ELFINDER_CONNECTOR_OPTION_SETS['default'])

        #test that invalid command throws ERROR_UNKNOWN_CMD
        assert_in(ElfinderErrorMessages.ERROR_UNKNOWN_CMD, connector.execute('dummy')['error'])

        #test missing arguments
        assert_in(ElfinderErrorMessages.ERROR_INV_PARAMS, connector.execute('ls')['error'])

        ###test it is actually doing something
        # The reason that this is failing is that it doesn't have a 'context'
        assert_not_in('error', connector.execute('open', mimes=['image'], init=True))

        ###test debug keyword
        #eq_('debug' in connector.execute('open', init=True), False)
        #eq_('debug' in connector.execute('open', init=True, debug=True), True)
