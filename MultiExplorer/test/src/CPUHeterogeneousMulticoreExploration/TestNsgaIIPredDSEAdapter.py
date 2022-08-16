import unittest
from MultiExplorer.src.CPUHeterogeneousMulticoreExploration.Adapters import NsgaIIPredDSEAdapter


class TestMcPATAdapter(unittest.TestCase):
    def setUp(self):
        self.adapter = NsgaIIPredDSEAdapter()

        self.adapter.inputs['exploration_space']['original_cores_for_design'] = (1, 25)

        self.adapter.inputs['exploration_space']['ip_cores_for_design'] = (1, 25)

        self.adapter.inputs['constraints']['maximum_power_density'] = 0.4

        self.adapter.inputs['constraints']['maximum_area'] = 226

    def test_set_dse_settings_from_inputs(self):
        self.adapter.set_dse_settings_from_inputs([
            'exploration_space',
            'constraints',
            'original_cores_for_design',
            'ip_cores_for_design',
            'maximum_power_density',
            'maximum_area',
        ])

        print self.adapter.dse_settings

    def test_read_dse_settings(self):
        self.adapter.read_dse_settings()

        print self.adapter.dse_settings

    def test_execute(self):
        self.adapter.execute()


if __name__ == '__main__':
    unittest.main()
