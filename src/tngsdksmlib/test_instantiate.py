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

import consume_mano
import datetime as dt
import yaml
import time
import psutil

cm = consume_mano.ManoConsumer(broker_host='amqp://guest:guest@localhost:5672/%2F', broker_exchange='son-kernel')

results = {'time':{}, 'memory':{}}
results['time']['no-sm'] = {}
results['time']['sm'] = {}
results['time']['no-sm']['instantiation'] = {}
results['time']['no-sm']['termination'] = {}
results['time']['sm']['instantiation'] = {}
results['time']['sm']['termination'] = {}

results['memory']['no-sm'] = {}
results['memory']['sm'] = {}
results['memory']['no-sm']['instantiation'] = {}
results['memory']['sm']['instantiation'] = {}

# Instantiation and termination
for sm_tag in ['no-sm', 'sm']:
    for i in range(1,101):
        results['time'][sm_tag]['instantiation'][i] = []
        results['time'][sm_tag]['termination'][i] = []
        results['memory'][sm_tag]['instantiation'][i] = []
        package_path = 'packages-' + sm_tag + '/eu.5gtango.cnf-' + str(i) + '-' + sm_tag + '.0.1.tgo'
        for j in range(1, 5):
            mem = psutil.virtual_memory()
            print(mem)
            memory_in = (mem.total - mem.available)
            time_in = dt.datetime.now()
            instantiation = cm.instantiate_service(package_path)
            print("instantiation requested")
            time_out = dt.datetime.now()
            mem = psutil.virtual_memory()
            memory_out = (mem.total - mem.available)
            if instantiation[0]:
                print("deployment " + str(i) + ' ' + str(j) + " successful")
                results['time'][sm_tag]['instantiation'][i].append((time_out - time_in).total_seconds())
                results['memory'][sm_tag]['instantiation'][i].append(memory_out - memory_in)
                print(str((time_out - time_in).total_seconds()))
                # Termination
                time.sleep(1)
                time_in = dt.datetime.now()
                termination = cm.terminate_service(instantiation[1])
                time_out = dt.datetime.now()
                if termination[0]:
                    print("Termination " + str(i) + ' ' + str(j) + " successful")
                    results['time'][sm_tag]['termination'][i].append((time_out - time_in).total_seconds())
                    print(str((time_out - time_in).total_seconds()))
                else:
                    print("Termination " + str(i) + ' ' + str(j) + " failed")
            else:
                print("deployment " + str(i) + ' ' + str(j) + " failed")

        # temp write results to file
        print(yaml.dump(results))
        results_file = open('results.yaml', 'w')
        yaml.dump(results, results_file, default_flow_style=False)
        results_file.close()