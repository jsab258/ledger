"""pytest set-up for the prototype tests: names the markers rules_test.py uses."""


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "bundle_names: the check searches the bundle by the bundler's shortened names; "
        "re-point it when Fable's readable source replaces the bundle")
