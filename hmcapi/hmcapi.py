from ssh_client.ssh_client import SshClient
import re
from dateutil import parser


class HMCAPI(SshClient):
    """
    Extends the SshClient Class
    """
    def get_power_server_memory_information(self, managed_system_name):
        """
        :param managed_system_name: Managed system name as a String
        :return: Dictionary with status and message and memory installed, available, configurable information
        """
        cmd_result = self.execute_remote_command(['lshwres -r mem -m {0} --level sys -F '
                                                  'installed_sys_mem,'
                                                  'curr_avail_sys_mem,'
                                                  'configurable_sys_mem'.format(managed_system_name)])

        if not cmd_result.get('status') or not cmd_result.get('exit_code') == 0:
            if not cmd_result.get('status'):
                return {'status': False,
                        'msg': cmd_result.get('msg'),
                        'power_server_memory_info': []}
            elif not cmd_result.get('exit_code') == 0 and (cmd_result.get('stderr') or cmd_result.get('stdout')):
                if cmd_result.get('stderr'):
                    return {'status': False,
                            'msg': cmd_result.get('stderr').strip('\n'),
                            'power_server_memory_info': []}
                else:
                    return {'status': False,
                            'msg': cmd_result.get('stdout').strip('\n'),
                            'power_server_memory_info': []}
            else:
                return {'status': False,
                        'msg': u"Failed to retrieve Power Server memory information unknown reason.",
                        'power_server_memory_info': []}

        # Split into list delimiter new line
        stdout = cmd_result['stdout'].splitlines()

        # Remove empty list items
        power_server_information_list = []
        for item in stdout:
            if filter(bool, item):
                power_server_information_list.append(item)

        # Flatten out list
        power_server_information_list = ''.join(power_server_information_list)

        # Split string based on comma
        power_server_information_list = power_server_information_list.split(',')

        temp_dict = {'installed_sys_mem': 0, 'curr_avail_sys_mem': 0, 'configurable_sys_mem': 0}
        for i, item in enumerate(power_server_information_list):
            if i == 0:
                temp_dict['installed_sys_mem'] = item if item else 0
            elif i == 1:
                temp_dict['curr_avail_sys_mem'] = item if item else 0
            elif i == 2:
                temp_dict['configurable_sys_mem'] = item if item else 0
        power_server_information_list = temp_dict

        return {'status': True,
                'msg': u"Successfully retrieved Power Server memory information.",
                'power_server_memory_info': power_server_information_list}

    def get_installed_memory(self, managed_system_name):
        """
        :param managed_system_name: Managed system name as a String
        :return: Dictionary with status and message and number of installed memory
        """
        cmd_result = self.execute_remote_command(['lshwres -r mem -m {0} --level sys -F '
                                                 'installed_sys_mem'.format(managed_system_name)])

        # Strip new lines and white space
        if cmd_result['stdout']:
            cmd_result['stdout'] = cmd_result['stdout'].rstrip()

        if not cmd_result.get('status') or not cmd_result.get('exit_code') == 0:
            if not cmd_result.get('status'):
                return {'status': False,
                        'msg': cmd_result.get('msg'),
                        'num_memory': 0}
            elif not cmd_result.get('exit_code') == 0 and (cmd_result.get('stderr') or cmd_result.get('stdout')):
                if cmd_result.get('stderr'):
                    return {'status': False,
                            'msg': cmd_result.get('stderr').strip('\n'),
                            'num_memory': 0}
                else:
                    return {'status': False,
                            'msg': cmd_result.get('stdout').strip('\n'),
                            'num_memory': 0}
            else:
                return {'status': False,
                        'msg': u"Failed to retrieve the amount of installed memory unknown reason.",
                        'num_memory': 0}

        # Convert to int
        stdout = int(float(cmd_result['stdout']))

        return {'status': True,
                'msg': u"Successfully retrieved the amount of installed memory.",
                'num_memory': stdout}

    def get_current_available_memory(self, managed_system_name):
        """
        :param managed_system_name: Managed system name as a String
        :return: Dictionary with status and message and number of available memory
        """
        cmd_result = self.execute_remote_command(['lshwres -r mem -m {0} --level sys -F '
                                                 'curr_avail_sys_mem'.format(managed_system_name)])

        # Strip new lines and white space
        if cmd_result['stdout']:
            cmd_result['stdout'] = cmd_result['stdout'].rstrip()

        if not cmd_result.get('status') or not cmd_result.get('exit_code') == 0:
            if not cmd_result.get('status'):
                return {'status': False,
                        'msg': cmd_result.get('msg'),
                        'num_memory': 0}
            elif not cmd_result.get('exit_code') == 0 and (cmd_result.get('stderr') or cmd_result.get('stdout')):
                if cmd_result.get('stderr'):
                    return {'status': False,
                            'msg': cmd_result.get('stderr').strip('\n'),
                            'num_memory': 0}
                else:
                    return {'status': False,
                            'msg': cmd_result.get('stdout').strip('\n'),
                            'num_memory': 0}
            else:
                return {'status': False,
                        'msg': u"Failed to retrieve the amount of available memory unknown reason.",
                        'num_memory': 0}

        # Convert to int
        stdout = int(float(cmd_result['stdout']))

        return {'status': True,
                'msg': u"Successfully retrieved the amount of available memory.",
                'num_memory': stdout}

    def get_permanently_activated_memory(self, managed_system_name):
        """
        :param managed_system_name: Managed system name as a String
        :return: Dictionary with status and message and number of activated memory
        """
        cmd_result = self.execute_remote_command(['lshwres -r mem -m {0} --level sys -F '
                                                 'configurable_sys_mem'.format(managed_system_name)])

        # Strip new lines and white space
        if cmd_result['stdout']:
            cmd_result['stdout'] = cmd_result['stdout'].rstrip()

        if not cmd_result.get('status') or not cmd_result.get('exit_code') == 0:
            if not cmd_result.get('status'):
                return {'status': False,
                        'msg': cmd_result.get('msg'),
                        'num_memory': 0}
            elif not cmd_result.get('exit_code') == 0 and (cmd_result.get('stderr') or cmd_result.get('stdout')):
                if cmd_result.get('stderr'):
                    return {'status': False,
                            'msg': cmd_result.get('stderr').strip('\n'),
                            'num_memory': 0}
                else:
                    return {'status': False,
                            'msg': cmd_result.get('stdout').strip('\n'),
                            'num_memory': 0}
            else:
                return {'status': False,
                        'msg': u"Failed to retrieve the amount of activated memory unknown reason.",
                        'num_memory': 0}

        # Convert to int
        stdout = int(float(cmd_result['stdout']))

        return {'status': True,
                'msg': u"Successfully retrieved the amount of activated memory.",
                'num_memory': stdout}

    def get_power_server_processor_information(self, managed_system_name):
        """
        :param managed_system_name: Managed system name as a String
        :return: Dictionary with status and message and processors installed, available, configurable proc units
        """
        cmd_result = self.execute_remote_command(['lshwres -r proc -m {0} --level sys -F '
                                                 'installed_sys_proc_units,'
                                                 'curr_avail_sys_proc_units,'
                                                 'configurable_sys_proc_units'.format(managed_system_name)])

        if not cmd_result.get('status') or not cmd_result.get('exit_code') == 0:
            if not cmd_result.get('status'):
                return {'status': False,
                        'msg': cmd_result.get('msg'),
                        'power_server_processor_info': []}
            elif not cmd_result.get('exit_code') == 0 and (cmd_result.get('stderr') or cmd_result.get('stdout')):
                if cmd_result.get('stderr'):
                    return {'status': False,
                            'msg': cmd_result.get('stderr').strip('\n'),
                            'power_server_processor_info': []}
                else:
                    return {'status': False,
                            'msg': cmd_result.get('stdout').strip('\n'),
                            'power_server_processor_info': []}
            else:
                return {'status': False,
                        'msg': u"Failed to retrieve Power Server processor information unknown reason.",
                        'power_server_processor_info': []}

        # Split into list delimiter new line
        stdout = cmd_result['stdout'].splitlines()

        # Remove empty list items
        power_server_information_list = []
        for item in stdout:
            if filter(bool, item):
                power_server_information_list.append(item)

        # Flatten out list
        power_server_information_list = ''.join(power_server_information_list)

        # Split string based on comma
        power_server_information_list = power_server_information_list.split(',')

        temp_dict = {'installed_sys_proc_units': 0, 'curr_avail_sys_proc_units': 0, 'configurable_sys_proc_units': 0}
        for i, item in enumerate(power_server_information_list):
            if i == 0:
                temp_dict['installed_sys_proc_units'] = int(float(item)) if item else 0
            elif i == 1:
                temp_dict['curr_avail_sys_proc_units'] = item if item else 0
            elif i == 2:
                temp_dict['configurable_sys_proc_units'] = int(float(item)) if item else 0
        power_server_information_list = temp_dict

        return {'status': True,
                'msg': u"Successfully retrieved Power Server processor information.",
                'power_server_processor_info': power_server_information_list}

    def get_installed_processors(self, managed_system_name):
        """
        :param managed_system_name: Managed system name as a String
        :return: Dictionary with status and message and number of installed processors
        """
        cmd_result = self.execute_remote_command(['lshwres -r proc -m {0} --level sys -F '
                                                 'installed_sys_proc_units'.format(managed_system_name)])

        # Strip new lines and white space
        if cmd_result['stdout']:
            cmd_result['stdout'] = cmd_result['stdout'].rstrip()

        if not cmd_result.get('status') or not cmd_result.get('exit_code') == 0:
            if not cmd_result.get('status'):
                return {'status': False,
                        'msg': cmd_result.get('msg'),
                        'num_processors': 0}
            elif not cmd_result.get('exit_code') == 0 and (cmd_result.get('stderr') or cmd_result.get('stdout')):
                if cmd_result.get('stderr'):
                    return {'status': False,
                            'msg': cmd_result.get('stderr').strip('\n'),
                            'num_processors': 0}
                else:
                    return {'status': False,
                            'msg': cmd_result.get('stdout').strip('\n'),
                            'num_processors': 0}
            else:
                return {'status': False,
                        'msg': u"Failed to retrieve the number of installed processors unknown reason.",
                        'num_processors': 0}

        # Convert to int
        stdout = int(float(cmd_result['stdout']))

        return {'status': True,
                'msg': u"Successfully retrieved the number of installed processors.",
                'num_processors': stdout}

    def get_current_available_processors(self, managed_system_name):
        """
        :param managed_system_name: Managed system name as a String
        :return: Dictionary with status and message and number of available processors
        """
        cmd_result = self.execute_remote_command(['lshwres -r proc -m {0} --level sys -F '
                                                 'curr_avail_sys_proc_units'.format(managed_system_name)])

        # Strip new lines and white space
        if cmd_result['stdout']:
            cmd_result['stdout'] = cmd_result['stdout'].rstrip()

        if not cmd_result.get('status') or not cmd_result.get('exit_code') == 0:
            if not cmd_result.get('status'):
                return {'status': False,
                        'msg': cmd_result.get('msg'),
                        'num_processors': 0}
            elif not cmd_result.get('exit_code') == 0 and (cmd_result.get('stderr') or cmd_result.get('stdout')):
                if cmd_result.get('stderr'):
                    return {'status': False,
                            'msg': cmd_result.get('stderr').strip('\n'),
                            'num_processors': 0}
                else:
                    return {'status': False,
                            'msg': cmd_result.get('stdout').strip('\n'),
                            'num_processors': 0}
            else:
                return {'status': False,
                        'msg': u"Failed to retrieve the amount of available processors unknown reason.",
                        'num_processors': 0}

        # Convert to float
        stdout = float(cmd_result['stdout'])

        return {'status': True,
                'msg': u"Successfully retrieved the amount of available processors.",
                'num_processors': stdout}

    def get_permanently_activated_processors(self, managed_system_name):
        """
        :param managed_system_name: Managed system name as a String
        :return: Dictionary with status and message and number of activated processors
        """
        cmd_result = self.execute_remote_command(['lshwres -r proc -m {0} --level sys -F '
                                                 'configurable_sys_proc_units'.format(managed_system_name)])

        # Strip new lines and white space
        if cmd_result['stdout']:
            cmd_result['stdout'] = cmd_result['stdout'].rstrip()

        if not cmd_result.get('status') or not cmd_result.get('exit_code') == 0:
            if not cmd_result.get('status'):
                return {'status': False,
                        'msg': cmd_result.get('msg'),
                        'num_processors': 0}
            elif not cmd_result.get('exit_code') == 0 and (cmd_result.get('stderr') or cmd_result.get('stdout')):
                if cmd_result.get('stderr'):
                    return {'status': False,
                            'msg': cmd_result.get('stderr').strip('\n'),
                            'num_processors': 0}
                else:
                    return {'status': False,
                            'msg': cmd_result.get('stdout').strip('\n'),
                            'num_processors': 0}
            else:
                return {'status': False,
                        'msg': u"Failed to retrieve the number of activated processors unknown reason.",
                        'num_processors': 0}

        # Convert to int
        stdout = int(float(cmd_result['stdout']))

        return {'status': True,
                'msg': u"Successfully retrieved the number of activated processors.",
                'num_processors': stdout}

    def get_hmc_power_servers(self):
        """
        :return: Dictionary with status and message and a list of dictionaries with Power Server names and information
        """
        cmd_result = self.execute_remote_command(['lssyscfg -r sys -F name,type_model,serial_num,'
                                                 'state,cod_proc_capable,cod_mem_capable'])

        if cmd_result['status'] and not cmd_result['exit_code'] == 0:
            cmd_result = self.execute_remote_command(['lssyscfg -r sys -F name,model,serial_number,'
                                                     'state,cuod_capability,cuod_capability --all'])

        if not cmd_result.get('status') or not cmd_result.get('exit_code') == 0:
            if not cmd_result.get('status'):
                return {'status': False,
                        'msg': cmd_result.get('msg'),
                        'power_servers': []}
            elif not cmd_result.get('exit_code') == 0 and (cmd_result.get('stderr') or cmd_result.get('stdout')):
                if cmd_result.get('stderr'):
                    return {'status': False,
                            'msg': cmd_result.get('stderr').strip('\n'),
                            'power_servers': []}
                else:
                    return {'status': False,
                            'msg': cmd_result.get('stdout').strip('\n'),
                            'power_servers': []}
            else:
                return {'status': False,
                        'msg': u"Failed to retrieve list of HMC Power Servers unknown reason.",
                        'power_servers': []}

        # Split into list delimiter new line
        stdout = cmd_result['stdout'].splitlines()

        # Split list items based , character
        power_servers_list = []
        for item in stdout:
                power_servers_list.append(item.split(','))

        # Remove empty list items
        for i, item in enumerate(power_servers_list):
            power_servers_list[i] = filter(bool, item)

        type_model_regex = r'^\w{4}-\w{3}$'
        serial_num_regex = r'^\w{7}$'
        state_regex = r'^Operating$|^Standby$|^Ready$'

        # Assign list items to a dict key
        # name returns name
        # type_model returns a regex exact match of type model or none
        # serial_num returns a regex exact match of serial_num or none
        # state returns a True for available and False for not available
        # cod_proc_capable returns True for cod capable and False for not cod capable
        for n, power_server in enumerate(power_servers_list):
            temp_dict = {'name': None, 'type_model': None, 'serial_num': None, 'state': None, 'cod_proc_capable': None}
            for i, item in enumerate(power_server):
                if i == 0:
                    temp_dict['name'] = item
                elif i == 1:
                    temp_dict['type_model'] = item if re.match(type_model_regex, item) else None
                elif i == 2:
                    temp_dict['serial_num'] = item if re.match(serial_num_regex, item) else None
                elif i == 3:
                    temp_dict['state'] = True if re.match(state_regex, item) else False
                elif i == 4:
                    temp_dict['cod_proc_capable'] = True if item.isdigit() and int(item) == 1 else False
                elif i == 5:
                    temp_dict['cod_mem_capable'] = True if item.isdigit() and int(item) == 1 else False
            power_servers_list[n] = temp_dict
        return {'status': True,
                'msg': u"Successfully retrieved list of HMC Power Servers.",
                'power_servers': power_servers_list}

    def capacity_on_demand(self, managed_system_name, capacity_on_demand_code):
        """
        :param managed_system_name: Managed system name as a String
        :param capacity_on_demand_code: CoD code as a String
        :return: Dictionary with status and message
        """
        cmd_result = self.execute_remote_command(['chcod -o e -m {0} -k {1}'.format(managed_system_name,
                                                                                    capacity_on_demand_code)])

        from datetime import datetime
        self.log_results(datetime_logged=datetime.now(),
                         username=self.username,
                         action='Applying COD Code',
                         returncode=cmd_result.get('exit_code'),
                         stdout=cmd_result.get('stdout'),
                         stderr=cmd_result.get('stderr'),
                         server=self.hostname)

        if not cmd_result.get('status') or not cmd_result.get('exit_code') == 0:
            if not cmd_result.get('status'):
                return {'status': False,
                        'msg': cmd_result.get('msg')}
            elif not cmd_result.get('exit_code') == 0 and (cmd_result.get('stderr') or cmd_result.get('stdout')):
                if cmd_result.get('stderr'):
                    return {'status': False,
                            'msg': cmd_result.get('stderr').strip('\n')}
                else:
                    return {'status': False,
                            'msg': cmd_result.get('stdout').strip('\n')}
            else:
                return {'status': False,
                        'msg': u"CoD code was not applied unknown error occurred unknown reason."}

        return {'status': True,
                'msg': u"CoD code applied successfully."}

    def log_results(self, datetime_logged, username, action, returncode, stdout, stderr, server):
        log_directory = '/opt/pfa/pap/provisioning_automation_portal/' \
                        'provisioning_automation_portal/apps/powersystems/'
        log_file_name = 'capacity_on_demand_execution_logs.txt'

        with open(log_directory + log_file_name, "a") as myLog:
            myLog.write("===============================================================\n")
            myLog.write("---------------------------------------------------------------\n")
            myLog.write("DATETIME:\t\t{0}\n".format(datetime_logged))
            myLog.write("USERNAME:\t\t{0}\n".format(username))
            myLog.write("ACTION:\t\t\t{0}\n".format(action))
            myLog.write("RETURN CODE:\t{0}\n".format(returncode))
            myLog.write("SERVER:\t{0}\n".format(server))
            myLog.write("STANDARD OUT:\n")
            myLog.write("{0}".format(stdout))
            myLog.write("STANDARD ERROR:\n")
            myLog.write("{0}".format(stderr))
            myLog.write("---------------------------------------------------------------\n")
            myLog.write("===============================================================\n")
            myLog.write("\n")
            myLog.close()
        return

    def get_processor_vital_product_data(self, managed_system_name):
        """
        :param managed_system_name:
        :return: Dictionary with status and message and a Vital Product Data dictionary
        """
        cmd_result = self.execute_remote_command(['lscod -m {0} -t code -r proc -c mobile'.format(managed_system_name)])

        if cmd_result['status'] and not cmd_result['exit_code'] == 0:
            cmd_result = self.execute_remote_command(['lscod -m {0} -t code -r proc -c cuod'.format(managed_system_name)])

        if not cmd_result.get('status') or not cmd_result.get('exit_code') == 0:
            if not cmd_result.get('status'):
                return {'status': False,
                        'msg': cmd_result.get('msg'),
                        'vpd_data': {}}
            elif not cmd_result.get('exit_code') == 0 and (cmd_result.get('stderr') or cmd_result.get('stdout')):
                if cmd_result.get('stderr'):
                    return {'status': False,
                            'msg': cmd_result.get('stderr').strip('\n'),
                            'vpd_data': {}}
                else:
                    return {'status': False,
                            'msg': cmd_result.get('stdout').strip('\n'),
                            'vpd_data': {}}
            else:
                return {'status': False,
                        'msg': u"Failed to retrieve Processor Vital Product Data unknown reason.",
                        'vpd_data': {}}

        vpd_data = {}
        # Split into list. Delimiter is a semi-colon
        stdout = cmd_result['stdout'].strip().split(',')
        for item in stdout:
            try:
                k, v = item.split('=')
                vpd_data[k] = v
            except ValueError:
                return {'status': False,
                        'msg': cmd_result['stdout'].strip('\n') if cmd_result['stdout'] else u"Failed to retrieve "
                                                                                             u"Processor Vital Product "
                                                                                             u"Data.",
                        'vpd_data': {}}
        return {'status': True,
                'msg': u"Successfully retrieved Processor Vital Product Data.",
                'vpd_data': vpd_data}

    def get_memory_vital_product_data(self, managed_system_name):
        """
        :param managed_system_name: Managed system name as a string
        :return: Dictionary with status and message and Vital Product Data dictionary
        """
        cmd_result = self.execute_remote_command(['lscod -m {0} -t code -r mem -c mobile'.format(managed_system_name)])

        if cmd_result['status'] and not cmd_result['exit_code'] == 0:
            cmd_result = self.execute_remote_command(['lscod -m {0} -t code -r mem -c cuod'.format(managed_system_name)])

        if not cmd_result.get('status') or not cmd_result.get('exit_code') == 0:
            if not cmd_result.get('status'):
                return {'status': False,
                        'msg': cmd_result.get('msg'),
                        'vpd_data': {}}
            elif not cmd_result.get('exit_code') == 0 and (cmd_result.get('stderr') or cmd_result.get('stdout')):
                if cmd_result.get('stderr'):
                    return {'status': False,
                            'msg': cmd_result.get('stderr').strip('\n'),
                            'vpd_data': {}}
                else:
                    return {'status': False,
                            'msg': cmd_result.get('stdout').strip('\n'),
                            'vpd_data': {}}
            else:
                return {'status': False,
                        'msg': u"Failed to retrieve Memory Vital Product Data unknown reason.",
                        'vpd_data': {}}

        vpd_data = {}
        # Split into list. Delimiter is a semi-colon
        stdout = cmd_result['stdout'].strip().split(',')
        for item in stdout:
            try:
                k, v = item.split('=')
                vpd_data[k] = v
            except ValueError:
                return {'status': False,
                        'msg': cmd_result['stdout'].strip('\n') if cmd_result['stdout'] else u"Failed to retrieve "
                                                                                             u"Memory Vital Product "
                                                                                             u"Data.",
                        'vpd_data': {}}
        return {'status': True,
                'msg': u"Successfully retrieved Memory Vital Product Data.",
                'vpd_data': vpd_data}

    def change_account_password(self, username, old_password, new_password):
        """
        :param username: Username as a String
        :param old_password: Old password as a String
        :param new_password: New password as a String
        :return: Dictionary with status and message
        """
        cmd = 'chhmcusr -u {USERNAME} -t passwd -v {PASSWORD}'.format(USERNAME=username,
                                                                      PASSWORD=new_password)
        cmd_result = self.execute_remote_command([cmd, old_password])

        # Try alternate command to change password
        if not cmd_result['status'] or not cmd_result['exit_code'] == 0:
            cmd = 'chhmcusr -i name={USERNAME},passwd={PASSWORD}'.format(USERNAME=username,
                                                                         PASSWORD=new_password)
            cmd_result = self.execute_remote_command([cmd, old_password])

        if not cmd_result.get('status') or not cmd_result.get('exit_code') == 0:
            if not cmd_result.get('status'):
                return {'status': False,
                        'msg': cmd_result.get('msg')}
            elif not cmd_result.get('exit_code') == 0 and (cmd_result.get('stderr') or cmd_result.get('stdout')):
                if cmd_result.get('stderr'):
                    return {'status': False,
                            'msg': cmd_result.get('stderr').strip('\n')}
                else:
                    return {'status': False,
                            'msg': cmd_result.get('stdout').strip('\n')}
            else:
                return {'status': False,
                        'msg': u"Failed to change password unknown reason."}

        return {'status': True,
                'msg': u"Successfully changed password."}

    def get_cod_code_history(self, managed_system_name):
        """
        :param managed_system_name: Power server name as a String
        :return: List of dictionaries representing an entry in the CoD Code history. Dictionary contains timestamp,
         type memory or processor, and number of resources

        Only supports MOD, POD, RPROC, RMEM codes

        HSCL to Code Type Mappings
        HSCL0328 = RMEM
        HSCL0327 = RPROC
        HSCL0302 = MEM
        HSCL0301 = POD
        """
        cmd = 'lscod -t hist -m {0}'.format(managed_system_name)

        cmd_result = self.execute_remote_command([cmd])

        if not cmd_result.get('status') or not cmd_result.get('exit_code') == 0:
            if not cmd_result.get('status'):
                return {'status': False,
                        'msg': cmd_result.get('msg'),
                        'history': []}
            elif not cmd_result.get('exit_code') == 0 and (cmd_result.get('stderr') or cmd_result.get('stdout')):
                if cmd_result.get('stderr'):
                    return {'status': False,
                            'msg': cmd_result.get('stderr').strip('\n'),
                            'history': []}
                else:
                    return {'status': False,
                            'msg': cmd_result.get('stdout').strip('\n'),
                            'history': []}
            else:
                return {'status': False,
                        'msg': u"Failed to get CoD code history unknown reason.",
                        'history': []}

        if 'No results were found' in cmd_result.get('stdout'):
            return {'status': False,
                    'msg': u"No results were found.",
                    'history': []}

        stdout = cmd_result.get('stdout').rstrip('\n').split('\n')

        add_processor_regex = 'HSCL0301'
        add_memory_regex = 'HSCL0302'
        remove_processor_regex = 'HSCL0327'
        remove_memory_regex = 'HSCL0328'

        history = []
        for line in stdout:
            temp_dict = {}
            if re.search(add_processor_regex, line):
                temp_list = line.split(',"')
                temp_dict['timestamp'] = parser.parse(temp_list[0].replace('"', '').replace(',', '').strip('time_stamp='))
                temp_dict['type'] = 'pod'
                temp_dict['number'] = int(temp_list[1].split('index:')[0].split(':')[1].strip(' ').strip(','))
                history.append(temp_dict)
            if re.search(add_memory_regex, line):
                temp_list = line.split(',"')
                temp_dict['timestamp'] = parser.parse(temp_list[0].replace('"', '').replace(',', '').strip('time_stamp='))
                temp_dict['type'] = 'mem'
                temp_dict['number'] = int(temp_list[1].split('index:')[0].split(':')[1].strip(' ').strip(','))
                history.append(temp_dict)
            if re.search(remove_processor_regex, line):
                temp_list = line.split(',"')
                temp_dict['timestamp'] = parser.parse(temp_list[0].replace('"', '').replace(',', '').strip('time_stamp='))
                temp_dict['type'] = 'rproc'
                temp_dict['number'] = int(temp_list[1].split('index:')[0].split(':')[1].strip(' ').strip(','))
                history.append(temp_dict)
            if re.search(remove_memory_regex, line):
                temp_list = line.split(',"')
                temp_dict['timestamp'] = parser.parse(temp_list[0].replace('"', '').replace(',', '').strip('time_stamp='))
                temp_dict['type'] = 'rmem'
                temp_dict['number'] = int(temp_list[1].split('index:')[0].split(':')[1].strip(' ').strip(','))
                history.append(temp_dict)
        return {'status': True,
                'msg': u"Successfully retrieved code history!",
                'history': history}