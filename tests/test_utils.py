import unittest
from unittest.mock import mock_open, patch
import json
from utils import write_to_json


class TestUtils(unittest.TestCase):
    @patch("json.dump")
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.load")
    def test_write_to_json(self, mock_load, mock_file, mock_dump):
        mock_load.return_value = {"existing_key": "existing_value"}
        data = ["City", "Street", "1234"]

        write_to_json(data)

        mock_load.assert_called_once_with(mock_file.return_value)
        mock_dump.assert_called_once_with(
            {"existing_key": "existing_value", "City Street 1234": data},
            mock_file.return_value,
            indent=4
        )


if __name__ == "__main__":
    unittest.main()
