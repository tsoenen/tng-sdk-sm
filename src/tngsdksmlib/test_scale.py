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

cm = consume_mano.ManoConsumer(broker_host='amqp://guest:guest@localhost:5672/%2F', broker_exchange='son-kernel')

# Scaling
scale_results = {}
scale_results['scale_out'] = {}
scale_results['scale_in'] = {}
package_path = 'packages-no-sm/eu.5gtango.cnf-1-no-sm.0.1.tgo'
instantiation = cm.instantiate_service(package_path)
print("deployment successful")
print(yaml.dump(instantiation[2]))
vnfd_uuid = instantiation[2]['data']['vnfrs'][0]['descriptor_reference']
if instantiation[0]:
    for i in range(1, 51):
        scale_results['scale_out'][i] = []
        scale_results['scale_in'][i] = []
        for j in range(5):
            # Scale out
            time_in = dt.datetime.now()
            scale_out = cm.scale_out_service(instantiation[1], vnfd_uuid, i)
            time_out = dt.datetime.now()
            if scale_out[0]:
                print("scale out in " + str((time_out - time_in).total_seconds()))
                scale_results['scale_out'][i].append((time_out - time_in).total_seconds())
            # Scale in
            time_in = dt.datetime.now()
            scale_in = cm.scale_in_service_vnfd(instantiation[1], vnfd_uuid, i)
            time_out = dt.datetime.now()
            if scale_in[0]:
                print("scale in in " + str((time_out - time_in).total_seconds()))
                scale_results['scale_in'][i].append((time_out - time_in).total_seconds())

        print(yaml.dump(scale_results))
        results_file = open('scale_results.yaml', 'w')
        yaml.dump(scale_results, results_file, default_flow_style=False)
        results_file.close()

termination = cm.terminate_service(instantiation[1])
