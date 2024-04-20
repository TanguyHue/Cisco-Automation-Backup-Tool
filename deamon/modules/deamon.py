from ping import pingDetect
import daemon
import os

class pingDaemon:
    def __init__(self) -> None:
        pass

    def start_daemon(self):
        self.pid = os.getpid()
        with daemon.DaemonContext(
            stdout=open('/tmp/stdout.txt', 'w+'),
            stderr=open('/tmp/stderr.txt', 'w+'),
            stdin=open('/dev/null', 'r')
        ):
            pingDetect().start()

if __name__ == "__main__":
    pingDaemon().start_daemon()