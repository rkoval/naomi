# Licensed under the Apache License, Version 2.0 (the “License”); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an “AS IS” BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

from Naomi.system.fs import (
    delete_dir_contents,
    list_files,
    load_yaml,
    write_file,
)

from Naomi.system.paths import (
    COMMANDS_BUILD_DIR,
    COMMANDS_SRC_DIR,
    package_path,
)

from Naomi.system.headers import command as command_header
from Naomi.system.logging import get_logger
from Naomi.system.util import to_json_string
from sublime_plugin import ApplicationCommand


logger = get_logger()


def build():
    logger.info('Cleaning: %s' % package_path(COMMANDS_BUILD_DIR))

    delete_dir_contents(COMMANDS_BUILD_DIR)

    logger.info('Building command files...')

    for file in list_files(COMMANDS_SRC_DIR):
        destination = file
        destination = destination.replace('src', 'build')
        destination = destination.replace('.yml', '.sublime-commands')

        logger.debug('Building file: %s' % package_path(file))

        data = load_yaml(file)
        jsonString = to_json_string(data)
        write_file(destination, command_header() + jsonString)

    logger.info('Done building commands.')


class NaomiBuildCommandsCommand(ApplicationCommand):
    def run(self):
        build()
