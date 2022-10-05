import os

def get_env_or_raise(environment_variable_name: str) -> str:
    env_value = os.getenv(environment_variable_name)
    if not env_value:
        raise Exception(f'You have to define an environment variable called {environment_variable_name}.')
    return env_value
