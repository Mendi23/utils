from selenium import webdriver
import os, shutil, json
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class PersistentDriver(object):

    _LOCAL_STORAGE_FILE = "localStorage.json"
    driver = None
    _profile = None

    def get_local_storage(self):
        return self.driver.execute_script("return window.localStorage;")
    
    
    def set_local_storage(self, data):
        self.driver.execute_script(
            "indexedDB.deleteDatabase('wawc');".join(
                [
                    "window.localStorage.setItem('{}', '{}');".format(
                        k, v.replace("\n", "\\n") if isinstance(v, str) else v
                    )
                    for k, v in data.items()
                ]
            )
        )

    def save_firefox_profile(self, remove_old=False):
        """Function to save the firefox profile to the permanant one"""

        if remove_old:
            if os.path.exists(self._profile_path):
                try:
                    shutil.rmtree(self._profile_path)
                except OSError:
                    pass

            shutil.copytree(
                os.path.join(self._profile.path),
                self._profile_path,
                ignore=shutil.ignore_patterns("parent.lock", "lock", ".parentlock"),
            )
        else:
            for item in os.listdir(self._profile.path):
                if item in ["parent.lock", "lock", ".parentlock"]:
                    continue
                s = os.path.join(self._profile.path, item)
                d = os.path.join(self._profile_path, item)
                if os.path.isdir(s):
                    shutil.copytree(
                        s,
                        d,
                        ignore=shutil.ignore_patterns(
                            "parent.lock", "lock", ".parentlock"
                        ),
                    )
                else:
                    shutil.copy2(s, d)

        with open(os.path.join(self._profile_path, self._LOCAL_STORAGE_FILE), "w") as f:
            f.write(json.dumps(self.get_local_storage()))

    def close(self):
        self.driver.close()

    def __init__(
        self,
        loadstyles=False,
        profile=None,
        headless=False,
        extra_params=None,
        executable_path=None,
    ):
        extra_params = extra_params or {}

        self._profile_path = profile
        self._profile = webdriver.FirefoxProfile(self._profile_path)
        if not loadstyles:
            # Disable CSS
            self._profile.set_preference("permissions.default.stylesheet", 2)
            # Disable images
            self._profile.set_preference("permissions.default.image", 2)
            # Disable Flash
            self._profile.set_preference(
                "dom.ipc.plugins.enabled.libflashplayer.so", "false"
            )

            options = Options()

            if headless:
                options.set_headless()

            options.profile = self._profile

            capabilities = DesiredCapabilities.FIREFOX.copy()
            capabilities["webStorageEnabled"] = True

            if executable_path is not None:
                executable_path = os.path.abspath(executable_path)
            extra_params['executable_path'] = executable_path

            self.driver = webdriver.Firefox(capabilities=capabilities, options=options, **extra_params)
            self.connect()

    def connect(self):
        self.driver.get('https://www.google.com')
        profilePath = self._profile.path

        local_storage_file = os.path.join(profilePath, self._LOCAL_STORAGE_FILE)
        if os.path.exists(local_storage_file):
            with open(local_storage_file) as f:
                self.set_local_storage(json.loads(f.read()))
            self.driver.refresh()

