from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="AMPERE",
    settings_files=["settings.toml", ".secrets.toml"],
    environments=True,
    load_dotenv=True,
)