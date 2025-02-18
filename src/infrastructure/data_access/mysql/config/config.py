from configparser import ConfigParser
import os

def read_config(filename="app.ini", section="mysql"):
    # Create a ConfigParser object to handle INI file parsing
    current_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(current_dir,filename)
    config = ConfigParser()

    # Read the specified INI configuration file
    config.read(filepath)

    # Empty dictionary to store config data
    data = {}

    if config.has_section(section):
        items = config.items(section)
        for item in items:
            data[item[0]] = item[1]
    else:
        raise Exception(f"{section} section not found in the {filename} file")

    return data


if __name__ == "__main__":
    config = read_config()
    print(config)
