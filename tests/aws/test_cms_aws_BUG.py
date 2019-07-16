###############################################################
# pytest -v --capture=no tests/aws/test_aws_BUG.py
# pytest -v  tests/aws/test_aws_BUG.py
# pytest -v --capture=no -v --nocapture tests/aws/test_aws_BUG.py:Test_aws.<METHIDNAME>
###############################################################
import pytest
from cloudmesh.common.Shell import Shell
from cloudmesh.common.StopWatch import StopWatch
from cloudmesh.common.debug import VERBOSE
from cloudmesh.common.util import HEADING
from cloudmesh.management.configuration.config import Config


@pytest.mark.incremental
class Test_aws:

    def setup(self):
        conf = Config("~/.cloudmesh/cloudmesh4.yaml")["cloudmesh"]
        cred = conf["cloud"]['aws']["credentials"]
        self.key = (cred['EC2_PRIVATE_KEY_FILE_NAME']).split('.')[0]

    def test_04_stop(self):
        HEADING("this test will fail, press Ctrl-C to skip")

        StopWatch.start("cms vm stop")
        result = Shell.execute(
            "cms vm stop test_boot_02 --parallel --processors=3", shell=True)
        StopWatch.stop("cms vm stop")

        VERBOSE(result)

        assert "'name': 'test_boot_02'" in result

    def test_04_start(self):
        HEADING("this test will fail, press Ctrl-C to skip")

        StopWatch.start("cms vm start")
        result = Shell.execute(
            "cms vm start test_boot_02 --parallel --processors=3", shell=True)
        StopWatch.stop("cms vm start")

        VERBOSE(result)

        assert "'name': 'test_boot_02'" in result

    def test_04_terminate(self):
        HEADING("this test will fail, press Ctrl-C to skip")

        StopWatch.start("cms vm terminate")
        result = Shell.execute(
            "cms vm terminate test_boot_01 --parallel --processors=3",
            shell=True)
        StopWatch.stop("cms vm terminate")

        VERBOSE(result)

        assert "'name': 'test_boot_01'" in result

    def test_04_delete(self):
        HEADING("this test will fail, press Ctrl-C to skip")

        StopWatch.start("cms vm delete")
        result = Shell.execute(
            "cms aws vm test_boot_02 --parallel --processors=3", shell=True)
        StopWatch.stop("cms vm delete")

        VERBOSE(result)

        assert "'name': 'test_boot_02'" in result