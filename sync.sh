export ansible_lib="/usr/local/lib/python3.7/site-packages/ansible"
cp -r /workspaces/fortios_facts/lib/ansible/* $ansible_lib/
ls -l $ansible_lib/modules/network/fortios/fortios_facts.py
ls -lR $ansible_lib/module_utils/network/fortios/*
code $ansible_lib/modules/network/fortios/fortios_facts.py