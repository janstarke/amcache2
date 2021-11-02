import sys
import logging
import datetime
from collections import namedtuple

import argparse
import regipy

g_logger = logging.getLogger("amcache2")

class NotAnAmcacheHive(Exception):
    pass

class InventoryApplicationFileEntry:
    def __init__(self, entry: regipy.registry.NKRecord):
        self.__timestamp = regipy.convert_wintime(entry.header.last_modified, as_json=False)

        for value in entry.iter_values():
            if value.name.lower() == 'lowercaselongpath':
                self.__lower_case_long_path = value.value
            elif value.name.lower() == 'originalfilename':
                self.__original_filename = value.value

    def __str__(self):
        return "{MD5}|{name}|{inode}|{mode_as_string}|{UID}|{GID}|{size}|{atime}|{mtime}|{ctime}|{crtime}".format(
            MD5 = "0",
            name = ("%s (%s) "% (self.__lower_case_long_path, self.__original_filename)),
            inode = "0",
            mode_as_string = "0",
            UID = "0",
            GID = "0",
            size = "0",
            atime = "-1",
            mtime = self.__timestamp.strftime('%s'),
            ctime = "-1",
            crtime = "-1"
        )

class InventoryApplicationFileList:
    def __init__(self, hive):
        self.__files = list()
        root_key = hive.get_key("Root")
        iaf_key = root_key.get_subkey("InventoryApplicationFile")
        self.__parse_iaf(iaf_key)

    def __parse_iaf(self, iaf):
        for file_key in iaf.iter_subkeys():
            self.__files.append(InventoryApplicationFileEntry(file_key))

    def __iter__(self):
        return self.__files.__iter__()


def parse_execution_entries(hive):
    for f in InventoryApplicationFileList(hive):
        print(str(f))

def main(argv=None):
    if argv is None:
        argv = sys.argv

    parser = argparse.ArgumentParser(
        description="Parse program execution entries from the Amcache.hve Registry hive")
    parser.add_argument("registry_hive", type=str,
                        help="Path to the Amcache.hve hive to process")
    args = parser.parse_args(argv[1:])

    hive = regipy.registry.RegistryHive(args.registry_hive)
    try:
        ee = parse_execution_entries(hive)
    except NotAnAmcacheHive:
        g_logger.error("doesn't appear to be an Amcache.hve hive")
        return


if __name__ == "__main__":
    main(argv=sys.argv)