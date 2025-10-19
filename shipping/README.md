# NUS CS4226 Programming Assignment 1

In this assignment, you will build a virtual network using Mininet and implement two controller-side application using Ryu.

All the scripts in this folder assume full installations of Ryu, its dependencies, and Mininet.
The scripts require user python version <= 3.9 and access to the `python3` command under root.
If you want to run the code in your own environment, make sure your OS is Linux-based, supports Open vSwitch, and has the dependencies with correct version installed.

## Deadline
October 24th, 2025 23:59 (Week 10 Friday)

## Folder structure
The folder structure is as follows.
You will need to edit the following three files to complete this assignment: `topology.py`, `simple_switch.py`, and `stp_switch.py`.
```
.
├── checkers
│   ├── check_stp_switch.py
│   ├── check_topo.py
│   ├── stp_switch_checker.py
│   └── topo_checker.py
├── CS4226_PA1_handout.pdf
├── packer.sh
├── README.md
├── ring.in
├── ring_tiny.in
├── simple_switch.py
├── star.in
├── star_tiny.in
├── stp_switch.py
└── topology.py
```

## Task Descriptions
There are four tasks in this assignment.
- Task 1 involves completing `topology.py`
- Task 2 involves completing `simple_switch.py`
- Task 3 & 4 involve completing `stp_switch.py`

The places where your action is needed are preceded by a `# TODO` tag.
There are also descriptions and links left as comments in those files; you are highly encouraged to read those, especially the ones that starts with a`# CHECK_THIS_OUT` flag.

The detail of these tasks can be found in the `CS4226_PA1_handout.pdf`.

## Checkers
A few checkers have been provided in the `checkers/` folder.
The checkers assume the root directory (of the project) as working directory (so use them by `python checkers/XXX_checker.py` instead of `cd`ing into the `checkers` folder).

For Task 1: provided `topo_checker.py` will check the implementation of `topology.py`.
It will look for switches, hosts, and links in the Mininet network namespace,
and check whether the devices found matches the expected specified in the input file.

For Task 2: You need to test the implementation of `simple_switch.py`.
You may want to test the implementation on an acyclic network topology.
You may want to check the connectivity of the network and look for installed flow rules on the switches to make sure after the initial learning process, packets should no longer be sent to the controller for processing.

For Task 3: provided `stp_switch_checker.py` will check the implementation of `stp_switch.py`.
It will test the implementation on a cyclic network topology.
It will check the connectivity of the network to make sure the network operates correctly in the presence of loops and look for installed flow rules on the switches to make sure after the initial learning process, packets should no longer be sent to the controller for processing.

For Task 4: You need to check the fault-tolerance of `stp_switch.py`.
You may want to test the implementation on a cyclic network topology.
You may want to first perform the same checks as `stp_switch_checkers.py` to ensure basic functionality operates correctly, then invoke a topology change on the network, verify the flow tables have been flushed, and re-check the connectivity.

If you want any of the checkers to run on a customized topology provided by you, you can change the variable storing the input file name around the start of the corresponding `check_XXX.py` script (note that these are not the `XXX_checker.py` scripts).

## Submission
You need to submit a zip file directly containing the three files you edited.
You can create such zip using the script `packer.sh`.
The zip file should be named with your student number (e.g. `A1234567X.zip`).

Please follow the requirements on folder structure and naming above closely as your submission will be graded using a script.
Failing to comply might result in penalties in mark (if the script cannot automatically process your submission) and even a 0 mark (if human-intervention cannot process your submission as well).

## Grading
Your submission will be graded on the same VM environment we distributed, by scripts similar to the checkers provided.

The grading script will have longer timeouts than the provided checkers and will not bail out on the first error seen.
We will also use a version of `topology.py` implemented by the teaching team for grading the Ryu applications so that you can still receive grades even if some previous sections failed.

DO NOT attempt to attack the testing infrastructure in your code.
Doing so will result in academic penalties.

## Copyright and Academic Integrity
You are prohibited from sharing, publishing, or distributing any original course materials to any third party, including but not limited to other students or GitHub, without the explicit permission from the NUS CS4226 teaching team.

While some assignments in this course may involve using code licensed under the Apache License 2.0, and you are therefore legally allowed to share and redistribute this code under the terms of that license, you are expected to submit original work and complete assignments independently unless otherwise specified.

Collaboration or sharing of solutions is prohibited unless explicitly allowed as part of the assignment. Violations of this rule will be treated as breaches of academic integrity and may result in academic penalties, even if the sharing of code is legally permissible under the Apache 2.0 License.