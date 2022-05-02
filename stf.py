import hashlib
import copy

import setting
import rpc

def subchain_stf(state, msg):
    new_state = copy.deepcopy(state)
    if msg.get('type') == 'folder_storage':
        folder = msg.get('name')
        assert folder
        new_state.setdefault('folder_storage', {})
        current_folder = new_state['folder_storage'].setdefault(folder, {})
        # print('current folder', current_folder)
        if 'remove' in msg:
            remove_dict = msg['remove']
            for path, info in remove_dict.items():
                # print('remove', path, info)
                assert path in current_folder and info == current_folder[path]
                del current_folder[path]

        if 'add' in msg:
            add_dict = msg['add']
            for path, info in add_dict.items():
                # print('add', path, info)
                assert path not in current_folder
                current_folder[path] = info
        # print('fullstate dict', fullstate_dict)

    return new_state

def chain_stf(state, data):
    new_state = {}

    subchains = state.get('subchains', {})
    subchains.update(data.get('subchains', {}))
    new_state['subchains'] = subchains

    shares = state.get('shares', {})
    if setting.POS_MASTER_ADDRESS not in shares:
        shares[setting.POS_MASTER_ADDRESS] = setting.POS_SHARES
    new_state['shares'] = shares

    return new_state

def chain_block_validator(block, new_block):
    pass
