from more_itertools.more import side_effect

from poetry_tutorial_project import *
from poetry_tutorial_project import __version__

from unittest.mock import patch, MagicMock

def test_version():
    assert __version__ == '0.1.0'

def test_system_boot_time():
    from datetime import datetime
    test_time = MagicMock(return_value=datetime(2025,6, 19, 12, 30, 0).timestamp())

    with patch("psutil.boot_time", return_value=test_time.return_value) as mock_boot_time:
        result = system_boot_time()
        assert mock_boot_time.call_count == 1
        assert isinstance(result, str)
        assert "Boot Time: 2025/6/19 12:30" in result

def test_system_cpu_usage():
    with patch("psutil.cpu_count", side_effect=[2,4]) as mock_cpu_count:
        with patch("psutil.cpu_percent", return_value=75) as mock_cpu_percent:
            result = system_cpu_usage()
            assert mock_cpu_count.call_count == 2
            assert mock_cpu_percent.call_count == 1
            assert isinstance(result, str)
            assert "CPU: 75% utilized of 2 physical CPU cores (4 total)" in result

def test_system_virtual_mem_usage():
    test_svmem = MagicMock()
    test_svmem.total = 1024
    test_svmem.available = 512
    test_svmem.used = 512
    test_svmem.percent = 50
    with patch("psutil.virtual_memory", return_value=test_svmem) as mock_virtual_memory:
        result = system_virtual_mem_usage()
        assert mock_virtual_memory.call_count == 1
        assert isinstance(result, str)
        assert "Virtual Memory: 50% of 1.00KB total system memory available (512.00B used with 512.00B remaining)." in result

def test_system_disk_usage():
    test_partition = MagicMock()
    test_partition.mountpoint = "/test/"

    test_partition_usage = MagicMock()
    test_partition_usage.total = 1024
    test_partition_usage.free = 512
    test_partition_usage.percent = 50

    with patch("psutil.disk_partitions", return_value=[test_partition]) as mock_partition:
        with patch("psutil.disk_usage", return_value=test_partition_usage) as mock_partition_usage:
            result = system_disk_usage()
            assert mock_partition.call_count == 1
            assert mock_partition.call_count == 1
            assert isinstance(result, str)
            assert "Disk: 50% used of 1.00KB total, with 512.00B remaining."