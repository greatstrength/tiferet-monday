# *** imports

# ** infra
from tiferet import App

# *** run

# Load the Tiferet Monday app interface.
app = App(settings=dict(
    app_repo_module_path='tiferet.proxies.yaml.app',
    app_repo_class_name='AppYamlProxy',
    app_repo_params=dict(
        app_config_file='tiferet_monday/configs/app.yml',
    )
)).load_interface('tiferet_monday')