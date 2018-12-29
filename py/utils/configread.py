import configparser
import logging
import os


class ConfigRead():
    """Read config files and parse content"""

    def __init__(self, configfile):
        """Read config file and parse content

        Parameters
        ----------
        configfile : str
            configfile to read
        """

        self.name = "configread"
        self.log = logging.getLogger(__name__ + "." + self.name)
        self.log.debug("Initialising config reader")

        self.file = configfile
        self.is_config = False

        self._config = None
        self.log.debug("Trying to read config from " + self.file)
        try:
            confpsr = configparser.ConfigParser()
            dataset = confpsr.read(self.file)
            if len(dataset) == 1:
                self._config = {s: dict(confpsr.items(s))
                                for s in confpsr.sections()}
                self.log.debug("Successfully read config from " + self.file)
            else:
                self._config = None
                self.log.debug("Did not find any config parameters at " +
                               self.file)
        except Exception as e:
            self.log.exception("Failed to read '" +
                               self.file + "'!")
            self._config = None

        if self._config is not None:
            self.is_config = True
