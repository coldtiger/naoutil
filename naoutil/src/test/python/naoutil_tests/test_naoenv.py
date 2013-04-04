'''
Created on 1 Apr 2013

@author: dsnowdon
'''

import types
import unittest

from naoutil.naoenv import NaoEnvironment, make_environment
from naoutil_tests.mock import *

def set_mock_add_proxy(obj, func):
    obj.add_proxy = types.MethodType(func, obj)

def make_environment_with_fake_proxy(func):
    env = make_environment(MockBox())
    set_mock_add_proxy(env, func)
    return env

'''
don't attempt to create a real proxy because we can't. In the tests as we are not running in an
environment with an ALBroker so we just make the value of the proxy the name. 
We can't call proxy methods on this but we can tell the right proxy would have been created.
'''
def fake_add_proxy(self, longName):
        self.log('Creating proxy: ' + longName)
        self.proxies[longName] = longName

class ResourcesPath(unittest.TestCase):
    def test_find_implicit_resources_dir(self):
        env = make_environment(MockBox())
        rp = env.resources_dir()
        print "Implicit resources path = " + rp
        self.assertNotEqual(None, rp, "Resources path should not be None")

class ProxyManagement(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.env = make_environment_with_fake_proxy(fake_add_proxy)

    def test_create_tts(self):
        self.assertEqual('ALTextToSpeech', self.env.tts)

    def test_create_motion(self):
        self.assertEqual('ALMotion', self.env.motion)

    def test_create_memory(self):
        self.assertEqual('ALMemory', self.env.memory)
    
    def test_create_ALTextToSpeech(self):
        self.assertEqual('ALTextToSpeech', self.env.ALTextToSpeech)
    
    def test_invalid_name(self):
        self.assertRaises(AttributeError, lambda : self.env.foo)

class EnvironmentInitialization(unittest.TestCase):
    # test that we can create an environment with some proxies already specified
    def test_create_environment_with_map(self):
        env = NaoEnvironment(MockBox(),
                             { "ALMemory" : MockMemory(), 
                              "ALMotion" : MockMotion(), 
                              "ALTextToSpeech" : MockTextToSpeech() })
        self.assertIsNotNone(env)

if __name__ == '__main__':
    unittest.main()