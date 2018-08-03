# Copyright (c) 2015 SONATA-NFV, 2017 5GTANGO
# ALL RIGHTS RESERVED.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Neither the name of the SONATA-NFV, 5GTANGO
# nor the names of its contributors may be used to endorse or promote
# products derived from this software without specific prior written
# permission.

# This work has been performed in the framework of the SONATA project,
# funded by the European Commission under Grant number 671517 through
# the Horizon 2020 and 5G-PPP programmes. The authors would like to
# acknowledge the contributions of their colleagues of the SONATA
# partner consortium (www.sonata-nfv.eu).

# This work has been performed in the framework of the 5GTANGO project,
# funded by the European Commission under Grant number 761493 through
# the Horizon 2020 and 5G-PPP programmes. The authors would like to
# acknowledge the contributions of their colleagues of the 5GTANGO
# partner consortium (www.5gtango.eu).

#!/bin/bash
set -e

echo "-------------"
echo "Create an FSM"
echo "-------------"

export TNG_SM_PWD=`pwd`; ./go/bin/tng-sm new --type fsm test

echo "----------------------"
echo "Evaluate if FSM exists"
echo "----------------------"

if [ ! -d "test-fsm" ]; then
	echo "FSM directory not existing"
	exit 1
fi

echo "--------------------------"
echo "Evaluate if FSM is correct"
echo "--------------------------"

if [ ! -e "test-fsm/test/ssh.py" ]; then
	echo "FSM not correct"
	exit 1
fi

echo "-------------"
echo "Create an SSM"
echo "-------------"

export TNG_SM_PWD=`pwd`; ./go/bin/tng-sm new --type ssm test

echo "----------------------"
echo "Evaluate if SSM exists"
echo "----------------------"

if [ ! -d "test-ssm" ]; then
	echo "SSM directory not existing"
	exit 1
fi

echo "--------------------------"
echo "Evaluate if SSM is correct"
echo "--------------------------"

if [ -e "test-ssm/test/ssh.py" ]; then
	echo "SSM not correct"
	exit 1
fi
