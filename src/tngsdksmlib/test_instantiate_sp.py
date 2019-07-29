# Copyright (c) 2015 SONATA-NFV, 2017 5GTANGO
# ALL RIGHTS RESERVED.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Neither the name of the SONATA-NFV, 5GTANGO
# nor the names of its contributors may be used to endorse or promote
# products derived from this software without specific prior written
# permission.
#
# This work has been performed in the framework of the SONATA project,
# funded by the European Commission under Grant number 671517 through
# the Horizon 2020 and 5G-PPP programmes. The authors would like to
# acknowledge the contributions of their colleagues of the SONATA
# partner consortium (www.sonata-nfv.eu).
#
# This work has been performed in the framework of the 5GTANGO project,
# funded by the European Commission under Grant number 761493 through
# the Horizon 2020 and 5G-PPP programmes. The authors would like to
# acknowledge the contributions of their colleagues of the 5GTANGO
# partner consortium (www.5gtango.eu).

import tnglib
import datetime as dt
import yaml
import time
import os

tnglib.set_sp_path(os.environ.get("SP_PATH"))

print(tnglib.get_sp_path())

tnglib.remove_all_packages()

results = {'time':{}}
results['time']['no-sm'] = {}
results['time']['sm'] = {}
results['time']['no-sm']['instantiation'] = {}
results['time']['no-sm']['termination'] = {}
results['time']['sm']['instantiation'] = {}
results['time']['sm']['termination'] = {}

# Instantiation and termination
for sm_tag in ['no-sm', 'sm']:
    for i in range(1,101):
        results['time'][sm_tag]['instantiation'][i] = []
        results['time'][sm_tag]['termination'][i] = []
        package_path = 'packages-' + sm_tag + '/eu.5gtango.cnf-' + str(i) + '-' + sm_tag + '.0.1.tgo'
        package_uuid = tnglib.upload_package(package_path)[1]
        service_uuid = tnglib.map_package_on_service(package_uuid)[1]
        for j in range(1, 6):
            time_in = dt.datetime.now()
            inst_req = tnglib.service_instantiate(service_uuid)
            status = tnglib.get_request(inst_req[1])[1]['status']

            counter = 0
            while status not in ['READY', 'ERROR']:
                counter += 2
                if counter > 300:
                    print("instantiation took longer than five minutes, aborting")
                    break 
                time.sleep(2)
                status = tnglib.get_request(inst_req[1])[1]['status']
            inst_id = tnglib.get_request(inst_req[1])[1]['instance_uuid']
            time_out = dt.datetime.now()
            if status == 'READY':
                print("deployment " + str(i) + ' ' + str(j) + " successful")
                results['time'][sm_tag]['instantiation'][i].append((time_out - time_in).total_seconds())
                print(str((time_out - time_in).total_seconds()))
                # Termination
                time.sleep(1)
                time_in = dt.datetime.now()
                term_req = tnglib.service_terminate(inst_id)
                status = tnglib.get_request(term_req[1])[1]['status']

                counter = 0
                while status not in ['READY', 'ERROR']:
                    counter += 2
                    if counter > 120:
                        print("termination took longer than two minutes, aborting")
                        break 
                    time.sleep(2)
                    status = tnglib.get_request(term_req[1])[1]['status']

                time_out = dt.datetime.now()
                if status == 'READY':
                    print("Termination " + str(i) + ' ' + str(j) + " successful")
                    results['time'][sm_tag]['termination'][i].append((time_out - time_in).total_seconds())
                    print(str((time_out - time_in).total_seconds()))
                else:
                    print("Termination " + str(i) + ' ' + str(j) + " failed")
            else:
                print("deployment " + str(i) + ' ' + str(j) + " failed")
        tnglib.remove_package(package_uuid)
        # temp write results to file
        print(yaml.dump(results))
        results_file = open('results_sp.yaml', 'w')
        yaml.dump(results, results_file, default_flow_style=False)
        results_file.close()
