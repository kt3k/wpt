from .base import Browser, ExecutorBrowser, require_arg
from ..webdriver_server import ChromeDriverServer
from ..executors import executor_kwargs as base_executor_kwargs
from ..executors.executorselenium import (SeleniumTestharnessExecutor,
                                          SeleniumRefTestExecutor)
from ..executors.executorchrome import ChromeDriverWdspecExecutor


__wptrunner__ = {"product": "chrome_android",
                 "check_args": "check_args",
                 "browser": "ChromeAndroidBrowser",
                 "executor": {"testharness": "SeleniumTestharnessExecutor",
                              "reftest": "SeleniumRefTestExecutor",
                              "wdspec": "ChromeDriverWdspecExecutor"},
                 "browser_kwargs": "browser_kwargs",
                 "executor_kwargs": "executor_kwargs",
                 "env_extras": "env_extras",
                 "env_options": "env_options"}


def check_args(**kwargs):
    require_arg(kwargs, "webdriver_binary")


def browser_kwargs(test_type, run_info_data, **kwargs):
    return {"binary": kwargs["binary"],
            "webdriver_binary": kwargs["webdriver_binary"],
            "webdriver_args": kwargs.get("webdriver_args")}


def executor_kwargs(test_type, server_config, cache_manager, run_info_data,
                    **kwargs):
    from selenium.webdriver import DesiredCapabilities

    executor_kwargs = base_executor_kwargs(test_type, server_config,
                                           cache_manager, **kwargs)
    executor_kwargs["close_after_done"] = True
    capabilities = dict(DesiredCapabilities.CHROME.items())
    capabilities["chromeOptions"] = {}
    # required to start on mobile
    capabilities["chromeOptions"]["androidPackage"] = "com.android.chrome"
    print(capabilities)
    for (kwarg, capability) in [("binary", "binary"), ("binary_args", "args")]:
        if kwargs[kwarg] is not None:
            capabilities["chromeOptions"][capability] = kwargs[kwarg]
    if test_type == "testharness":
        capabilities["useAutomationExtension"] = False
        capabilities["excludeSwitches"] = ["enable-automation"]
    if test_type == "wdspec":
        capabilities["chromeOptions"]["w3c"] = True
    executor_kwargs["capabilities"] = capabilities
    return executor_kwargs


def env_extras(**kwargs):
    return []


def env_options():
    return {"host": "web-platform.test",
            "bind_hostname": "true"}


class ChromeAndroidBrowser(Browser):
    """Chrome is backed by chromedriver, which is supplied through
    ``wptrunner.webdriver.ChromeDriverServer``.
    """

    def __init__(self, logger, binary, webdriver_binary="chromedriver",
                 webdriver_args=None):
        """Creates a new representation of Chrome.  The `binary` argument gives
        the browser binary to use for testing."""
        Browser.__init__(self, logger)
        self.binary = binary
        self.server = ChromeDriverServer(self.logger,
                                         binary=webdriver_binary,
                                         args=webdriver_args)

    def start(self, **kwargs):
        self.server.start(block=False)

    def stop(self, force=False):
        self.server.stop(force=force)

    def pid(self):
        return self.server.pid

    def is_alive(self):
        # TODO(ato): This only indicates the driver is alive,
        # and doesn't say anything about whether a browser session
        # is active.
        return self.server.is_alive()

    def cleanup(self):
        self.stop()

    def executor_browser(self):
        return ExecutorBrowser, {"webdriver_url": self.server.url}
