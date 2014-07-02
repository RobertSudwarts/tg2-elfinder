import os, re
from nose.tools import *
from tgextelfinder.conf import settings
from tgextelfinder.volumes.filesystem import ElfinderVolumeLocalFileSystem

class TestElfinderVolumeLocalFileSystem(object):

    volume_class = ElfinderVolumeLocalFileSystem

    def setUp(self):
        settings.MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media')

        self.driver = self.volume_class()
        self.options = {
            'id' : 'lfTest1',
            'path' : settings.MEDIA_ROOT,
            'alias' : 'Elfinder files',
            'URL' : '', # settings.MEDIA_URL,
            'uploadAllow' : ['all',],
            'uploadDeny' : ['all',],
            'uploadOrder' : ['deny', 'allow'],
            'attributes' : [
                    {
                        'pattern' : '^%(sep)sfiles%(sep)sdirectory' % {'sep' : os.sep},
                        'read' : True,
                        'write': True,
                        'hidden' : True,
                        'locked' : True
                    },
            ]
        }

        self.driver.mount(self.options)
        self.default_path = self.driver.default_path()
        self.realPath = self.driver.decode(self.default_path)

    def tearDown(self):
        self.driver.reset_removed()

    def test_defaultpath(self):
        assert_true(isinstance(self.default_path, basestring))
        assert_true(len(self.default_path) > 0)

    def test_dir(self):
        root = self.driver.dir(self.default_path, False)
        eq_ (root['read'], 1)
        eq_ (root['write'], 1)
        eq_ (root['mime'], 'directory')
        assert_in('volumeid', root)
        assert_in('ts', root)
        assert_in('name', root)
        assert_in('hash', root)
        assert_in('size', root)
        assert_in('locked', root)

    def test_stat_dir(self):
        stat = self.driver.stat(self.realPath)
        eq_(stat['size'], 'unknown')
        eq_(stat['mime'], 'directory')
        eq_(stat['read'], 1)
        eq_(stat['write'], 1)
        assert_is_instance(stat['ts'], float)
        eq_(stat['dirs'], 1)

    def test_stat_file(self):
        stat = self.driver.stat(self.driver._join_path(self.driver._options['path'], self.driver._join_path('files','2bytes.txt')))
        eq_(stat['name'], '2bytes.txt')
        eq_(stat['read'], 1)
        eq_(stat['write'], 1)
        eq_(stat['mime'].startswith('text/'), True)
        eq_(stat['size'], 2)
        eq_(stat['hash'], self.driver.encode(self.driver._join_path(self.options['path'], self.driver._join_path('files','2bytes.txt'))))
        eq_(stat['phash'], self.driver.encode(self.driver._join_path(self.options['path'],'files')))
        assert_is_instance(stat['ts'], float)
        assert_not_in('dirs', stat)

    def test_dimensions(self):
        dim = self.driver.dimensions(self.driver.encode(self.driver._join_path(self.driver._options['path'], self.driver._join_path('files', self.driver._join_path('directory', 'yawd-logo.png')))))
        eq_(dim, '260x35')

    def test_tree(self):
        tree = self.driver.tree(self.default_path, 2)
        eq_(len(tree), 2)
        eq_(tree[0]['hash'], self.default_path)
        eq_(tree[1]['hash'], self.driver.encode(self.driver._join_path(self.driver._options['path'],'files')))
        #eq_(tree[2]['hash'], self.driver.encode(self.driver._join_path(self.driver._options['path'],'test')))

    def test_open_close(self):
        hash_ = self.driver.encode(self.driver._join_path(self.options['path'], self.driver._join_path('files','2bytes.txt')))
        fp = self.driver.open(hash_)
        eq_(fp.read(), '01')
        self.driver.close(fp, hash_)

    def test_mkfile_unlink(self):
        path = self.driver._join_path(self.options['path'], 'files')
        name = 'tmpfile'
        joined_path = self.driver._join_path(path, name)

        enc_path = self.driver.encode(path)
        enc_joined_path = self.driver.encode(joined_path)

        stat = self.driver.mkfile(enc_path, name)
        self.driver.rm(enc_joined_path)
        removed = self.driver.removed()

        eq_(stat['hash'], enc_joined_path)
        eq_(len(removed), 1)
        eq_(removed[0]['name'], name)
        eq_(removed[0]['hash'], enc_joined_path)
        eq_(removed[0]['phash'], enc_path)
        eq_(removed[0]['realpath'], joined_path)
        eq_(removed[0]['read'], 1)
        eq_(removed[0]['write'], 1)
        eq_(removed[0]['size'], 0)
        assert_in('mime', removed[0])
        assert_in('ts', removed[0])

    def test_mkdir_rmdir(self):
        path = self.driver._join_path(self.options['path'], 'files')
        name = 'tmpdir'
        joined_path = self.driver._join_path(path, name)

        enc_path = self.driver.encode(path)
        enc_joined_path = self.driver.encode(joined_path)

        stat = self.driver.mkdir(enc_path, name)
        self.driver.rm(enc_joined_path)
        removed = self.driver.removed()

        eq_(stat['hash'], enc_joined_path)
        eq_(len(removed), 1)
        eq_(removed[0]['name'], name)
        eq_(removed[0]['hash'], enc_joined_path)
        eq_(removed[0]['phash'], enc_path)
        eq_(removed[0]['realpath'], joined_path)
        eq_(removed[0]['read'], 1)
        eq_(removed[0]['write'], 1)
        eq_(removed[0]['size'], 'unknown')
        eq_(removed[0]['mime'], 'directory')
        assert_in('ts', removed[0])

    def test_locked(self):
        stat = self.driver.stat(self.driver._join_path(self.options['path'], self.driver._join_path('files', 'directory')))
        eq_(stat['locked'], 1)

        stat = self.driver.stat(self.driver._join_path(self.options['path'], 'files'))
        eq_(stat['locked'], 0)

    def test_hidden(self):
        stat = self.driver.stat(self.driver._join_path(self.options['path'], self.driver._join_path('files', 'directory')))
        eq_(stat['hidden'], 1)

        stat = self.driver.stat(self.driver._join_path(self.options['path'], 'files'))
        eq_(stat['hidden'], 0)
