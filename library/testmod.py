#!/usr/bin/python3

ANSIBLE_METADATA = {
        'metadata+version': '1.1',
        'status': ['preview'],
        'supported_by': 'rzfeeser'
    }

DOCUMENTATION = '''
---
module: testmod
short_description: THis module is being designed so we can observe the minimum required config for an Ansible module.
description:
    - user passes a param called 'name' <str> <required>
    - user passes a param called 'argument' <bool>
    - if argument: true then ansible returns name + additional string as well as indicating a YELLOW CHANGE in the play recap
    - if argument: false then ansible returns name sring and indicates GREEN OK in the play recap
    - if "name: fail me" then ansible returns FAILED in play recap
author:
    - billy.piper@cox.com
'''

EXAMPLE = '''
# pass in a name
- name: requesting a GREEN OK from our new module
  testmod:
    name: Zach
    argument: false

- name: requesting a YELLOW CHANGE from our new module
  testmod:
    name: Zach
    argument: true

- name: requesting a RED FAIL from our new module
  testmod:
    name: fail me
'''

RETURN = '''
original_message:
    description: The name parameter that was originally passed by the user
    type: str
message:
    description: the name parameter changed or argument in some fashion
    type: str
'''

from ansible.module_utils.basic import AnsibleModule

def run_module():
    """module logic"""
    module_args = dict(
            name=dict(type='str', required=True),
            argument=dict(type='bool', required=False)
        )

    ## seed the result dictionary object
    ## we primarily care about the change and state
    ## change is the module effectively modified the target
    ## result contains all of the KEYS you want to return after your module completes
    result = dict(
            changed=False,
            original_message='',
            message='')

    module = AnsibleModule(
            argument_spec=module_args,
            supports_check_mode=True)

    if module.check_mode:
        return result

    result['original_message'] = module.params['name']

    if module.params['argument'] == False:
        result['message'] = module.params['name']
    else:
        result['message'] = module.params['name'] + " is a wild and crazy guy!! or so says Dan Akroyd."
        result['changed'] = True

    if module.params['name'] == 'fail me':
        module.fail_json(msg="You requested me to fail!", **result)

    module.exit_json(**result)

def main():
    run_module()

if __name__ == "__main__":
    main()


