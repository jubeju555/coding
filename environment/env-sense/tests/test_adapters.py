import unittest
from src.adapters.lighting import Lighting
from src.adapters.sound import Sound
from src.adapters.workspace import Workspace

class TestAdapters(unittest.TestCase):

    def setUp(self):
        self.lighting = Lighting()
        self.sound = Sound()
        self.workspace = Workspace()

    def test_lighting_adjustment(self):
        self.lighting.set_brightness(70)
        self.assertEqual(self.lighting.get_brightness(), 70)

    def test_sound_adjustment(self):
        self.sound.set_volume(50)
        self.assertEqual(self.sound.get_volume(), 50)

    def test_workspace_configuration(self):
        self.workspace.set_layout('open')
        self.assertEqual(self.workspace.get_layout(), 'open')

    def tearDown(self):
        self.lighting.reset()
        self.sound.reset()
        self.workspace.reset()

if __name__ == '__main__':
    unittest.main()