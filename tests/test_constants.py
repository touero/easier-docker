import unittest

from src.easierdocker.constants import ContainerStatus, ExtraConfigModel


class TestConstants(unittest.TestCase):
    def test_container_status_values(self):
        self.assertEqual(ContainerStatus.RUNNING.value, 1)
        self.assertEqual(ContainerStatus.EXITED.value, 2)
        self.assertEqual(ContainerStatus.CREATED.value, 3)

    def test_validate_dict_accepts_expected_types(self):
        config = {"is_remove": 1, "days_ago_remove": 3, "remove_now": 0}

        self.assertIsNone(ExtraConfigModel.validate_dict(config))

    def test_validate_dict_rejects_unexpected_field(self):
        with self.assertRaisesRegex(ValueError, "Unexpected field: 'unknown'"):
            ExtraConfigModel.validate_dict({"unknown": 1})

    def test_validate_dict_rejects_wrong_type(self):
        with self.assertRaisesRegex(TypeError, "Field 'is_remove' expects type 'int'"):
            ExtraConfigModel.validate_dict({"is_remove": "1"})
