from circus.plugins import CircusPlugin
from zmq.eventloop import ioloop
from mfutil import add_inotify_watch
from mflog import getLogger
from inotify_simple import INotify, flags

log = getLogger("circus_autorestart")


class CircusAutorestart(CircusPlugin):
    """Circus plugin to automatically restart watchers.

    Watchers with a working_dir containing the string "/plugins/" are
    checked every second. If a change is detected in the configured working
    dir, the watcher is restarted.

    Args:
        name : the name of the plugin as a string.
        periodic: a PeriodicCallback object to call the
            ping() method every second.
        periodic10: a PeriodicCallback object to call the
            fill_watchers() method every 10 seconds.
        watchers: a set with watcher names (with "/plugins/" in configured
            working_dir).
        watchers_working_dir: a dict with watcher name as a key and
            corresponding inotify watcher as a value.
    """

    name = 'autorestart'
    periodic = None
    watchers = None
    watchers_working_dir = {}

    def __init__(self, *args, **config):
        """Constructor."""
        super(CircusAutorestart, self).__init__(*args, **config)
        self.watchers = set()
        self.watchers_working_dir = {}
        self.watchers_inotify = {}

    def initialize(self):
        """Initialize method called at plugin start.

        The method register the periodic callback of the ping() method
        and fill the watchers set.
        """
        super(CircusAutorestart, self).initialize()
        self.fill_watchers()
        self.periodic = ioloop.PeriodicCallback(self.ping, 1000, self.loop)
        self.periodic.start()
        self.periodic10 = ioloop.PeriodicCallback(self.fill_watchers, 10000,
                                                  self.loop)
        self.periodic10.start()

    def fill_watchers(self):
        msg = self.call("list")
        if 'watchers' in msg:
            for watcher in msg['watchers']:
                msg = self.call("options", name=watcher)
                if 'options' in msg:
                    working_dir = msg['options'].get('working_dir', '')
                    if '/plugins/' in working_dir:
                        if watcher not in self.watchers_working_dir:
                            log.info("monitoring watcher: %s with "
                                     "working_dir=%s" %
                                     (watcher, working_dir))
                            self.watchers.add(watcher)
                            self.watchers_working_dir[watcher] = working_dir
                            self.watchers_inotify[watcher] = \
                                self.add_inotify(working_dir)

    def add_inotify(self, working_dir):
        inotify = INotify()
        add_inotify_watch(inotify,
                          working_dir,
                          ignores=[
                              "python3_virtualenv",
                              "python3_virtualenv_sources",
                              "python2_virtualenv_sources",
                              "python2_virtualenv",
                              "*.log",
                              "log*",
                              "Log*",
                              "cache*"
                              "Cache*",
                              "Local Storage",
                              "*.sw?",
                              "*~", ".*"])
        return inotify

    def handle_recv(self, data):
        pass

    def is_watcher_active(self, watcher_name):
        """Return True if the watcher is in active state.

        Args:
            watcher_name: the name of the watcher (string).
        """
        msg = self.call("status", name=watcher_name)
        return (msg.get('status', 'unknown') == 'active')

    def ping(self):
        for watcher in self.watchers:
            if self.is_watcher_active(watcher):
                inotify = self.watchers_inotify.get(watcher, None)
                if inotify is None:
                    continue
                restart = False
                # non-blocking read
                for event in inotify.read(0):
                    log.debug("inotify event received for watcher %s: %s" %
                              (watcher, event))
                    restart = True
                    # new directory: we need to watch it
                    if (flags.CREATE & event.mask) and \
                            (flags.ISDIR & event.mask):
                        inotify.close()
                        working_dir = self.watchers_working_dir[watcher]
                        self.watchers_inotify[watcher] = \
                            self.add_inotify(working_dir)
                if restart:
                    log.info("killing watcher %s (modification)" % watcher)
                    self.call("kill", name=watcher)
