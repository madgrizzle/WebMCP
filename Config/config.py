"""

This file provides a single dict which contains all of the details about the
various settings.  It also has a number of helper functions for interacting
and using the data in this dict.

"""
import json
import os
from shutil import copyfile
from pathlib import Path

from __main__ import app
from DataStructures.makesmithInitFuncs import MakesmithInitFuncs


class Config(MakesmithInitFuncs):
    settings = {}
    home = ""

    def __init__(self):
        self.home = str(Path.home())
        print("Initializing Configuration")
        if not os.path.isdir(self.home + "/.WebControl"):
            print("creating " + self.home + "/.WebControl directory")
            os.mkdir(self.home + "/.WebControl")
        if not os.path.exists(self.home + "/.WebControl/webMCP.json"):
            print("copying webMCP.json to " + self.home + "/.WebControl/")
            copyfile("webMCP.json", self.home + "/.WebControl/webMCP.json")
        with open(self.home + "/.WebControl/webMCP.json", "r") as infile:
            self.settings = json.load(infile)

    def getJSONSettings(self):
        return self.settings

    def setValue(self, section, key, value):
        updated = False
        found = False
        for x in range(len(self.settings[section])):
            if self.settings[section][x]["key"].lower() == key.lower():
                found = True
                if self.settings[section][x]["type"] == "float":
                    try:
                        self.settings[section][x]["value"] = float(value)
                        updated = True
                    except:
                        pass
                elif self.settings[section][x]["type"] == "int":
                    try:
                        self.settings[section][x]["value"] = int(value)
                        updated = True
                    except:
                        pass
                elif self.settings[section][x]["type"] == "bool":
                    try:
                        if isinstance(value, bool):
                            if value:
                                value = "on"
                            else:
                                value = "off"
                        if value == "on":
                            self.settings[section][x]["value"] = 1
                            updated = True
                        else:
                            self.settings[section][x]["value"] = 0
                            updated = True
                    except:
                        pass
                else:
                    self.settings[section][x]["value"] = value
                    updated = True
        if not found:
            print("Did not find " + str(section) + ", " + str(key) + ", " + str(value))
        if updated:
            with open(self.home+"/.WebControl/webMCP.json", "w") as outfile:
                json.dump(
                    self.settings, outfile, sort_keys=True, indent=4, ensure_ascii=False
                )

    def updateSettings(self, section, result):
        print("at update Settings")
        updated = False
        for x in range(len(self.settings[section])):
            found = False
            for setting in result:
                if self.settings[section][x]["key"] == setting:
                    if self.settings[section][x]["type"] == "float":
                        try:
                            self.settings[section][x]["value"] = float(result[setting])
                            updated = True
                        except:
                            pass
                    elif self.settings[section][x]["type"] == "int":
                        try:
                            self.settings[section][x]["value"] = int(result[setting])
                            updated = True
                        except:
                            pass
                    elif self.settings[section][x]["type"] == "bool":
                        try:
                            if result[setting] == "on":
                                self.settings[section][x]["value"] = 1
                                updated = True
                            else:
                                self.settings[section][x]["value"] = 0
                                updated = True
                        except:
                            pass
                    elif self.settings[section][x]["type"] == "options":
                        try:
                            self.settings[section][x]["value"] = str(result[setting])
                            updated = True
                        except:
                            pass
                    else:
                        self.settings[section][x]["value"] = result[setting]
                        updated = True
                    found = True
                    break
            if not found:
                # must be a turned off checkbox.. what a pain to figure out
                if self.settings[section][x]["type"] == "bool":
                    self.settings[section][x]["value"] = 0
                    updated = True
        if updated:
            with open(self.home+"/.WebControl/webMCP.json", "w") as outfile:
                json.dump(
                    self.settings, outfile, sort_keys=True, indent=4, ensure_ascii=False
                )

    def getJSONSettingSection(self, section):
        """
        This generates a JSON string which is used to construct the settings page
        """
        options = []
        if section in self.settings:
            options = self.settings[section]
        for option in options:
            option["section"] = section
            if "desc" in option and "default" in option:
                if (
                    not "default setting:" in option["desc"]
                ):  # check to see if the default text has already been added
                    option["desc"] += "\ndefault setting: " + str(option["default"])
        return options

    def getDefaultValueSection(self, section):
        """
        Returns a dict with the settings keys as the key and the default value
        of that setting as the value for the section specified
        """
        ret = {}
        if section in self.settings:
            for option in self.settings[section]:
                if "default" in option:
                    ret[option["key"]] = option["default"]
                    break
        return ret

    def getDefaultValue(self, section, key):
        """
        Returns the default value of a setting
        """
        ret = None
        if section in self.settings:
            for option in self.settings[section]:
                if option["key"] == key and "default" in option:
                    ret = option["default"]
                    break
        return ret

    def getValue(self, section, key):
        """
        Returns the actual value of a setting
        """
        ret = None
        if section in self.settings:
            for option in self.settings[section]:
                if option["key"] == key:
                    ret = option["value"]
                    break
        return ret



