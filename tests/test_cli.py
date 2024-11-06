from wejherowo.cli import main
from unittest.mock import patch

def test_main():
    test_args = ["--param1", "value1", "--param2", "value2"]
    with patch("sys.argv", ["wejherowo"] + test_args):
        main()
