import os
from cloudmesh.common.util import path_expand
from cloudmesh.common.dotdict import dotdict
from cloudmesh.terminal.Terminal import VERBOSE
import platform
from getpass import getpass
from cloudmesh.common.console import Console
from cloudmesh.common.Shell import Shell


# security import yourfile.pem -k ~/Library/Keychains/login.keychain

# $ brew install openssl
# $ brew link openssl --force
# brew install openssh --with-libressl

class EncryptFile(object):
    def __init__(self, filename, secret):
        self.data = dotdict({
            'file': filename,
            'secret': secret,
            'pem': path_expand('~/.ssh/id_rsa.pem'),
            'key': path_expand('~/.ssh/id_rsa')
        })
        VERBOSE.print(self.data, verbose=9)
        if not os.path.exists(self.data["pem"]):
            self.pem_create()

    def _execute(self, command):
        VERBOSE.print(command, verbose=9)
        os.system(command)

    def check_passphrase(self):
        """
        cecks if the ssh key has a password
        :return:
        """

        self.data["passphrase"] = getpass("Passphrase:")

        if self.data.passphrase is None or self.data.passphrase == "":
            Console.error("No passphrase specified.")
            raise ValueError('No passphrase specified.')

        try:
            command = "ssh-keygen -p -P {passphrase} -N {passphrase} -f {key}".format(
                **self.data)
            r = Shell.execute(command, shell=True, traceflag=False)

            if "Your identification has been saved with the new passphrase." in r:
                Console.ok("Password ok.")
                return True
        except:
            Console.error("Password not correct.")

        return False

    def pem_verify(self):

        if platform.system().lower() == 'darwin':
            command = "security verify-cert -c {key}.pem".format(**self.data)
            self._execute(command)

        command = "openssl verify  {key}.pem".format(**self.data)
        self._execute(command)

    def pem_create(self):
        if platform.system().lower() == "darwin":
            command = "ssh-keygen -f {key}.pub -m pem -e > {key}.pem".format(
                **self.data)

        else:
            command = path_expand(
                "openssl rsa -in {key} -pubout  > {pem}".format(**self.data))

        # command = path_expand("openssl rsa -in id_rsa -pubout  > {pem}".format(**self.data))
        self._execute(command)
        command = "chmod go-rwx {key}.pem".format(**self.data)
        self._execute(command)

    #
    # TODO: BUG
    #
    def pem_cat(self):
        command = path_expand("cat {pem}".format(**self.data))
        self._execute(command)

    def encrypt(self):
        # encrypt the file into secret.txt
        print(self.data)
        command = path_expand(
            "openssl rsautl -encrypt -pubin -inkey {pem} -in {file} -out {secret}".format(**self.data))
        self._execute(command)

    def decrypt(self, filename=None):
        if filename is not None:
            self.data['secret'] = filename

        command = path_expand(
            "openssl rsautl -decrypt -inkey {pem} -in {secret} -out {file}".format(
                **self.data))
        self._execute(command)


if __name__ == "__main__":

    for filename in ['file.txt', 'secret.txt']:
        try:
            os.remove(filename)
        except Exception as e:
            pass

    # Creating a file with data

    with open("file.txt", "w") as f:
        f.write("Big Data is here.")

    e = EncryptFile('file.txt', 'secret.txt')
    e.encrypt()
    e.decrypt()
