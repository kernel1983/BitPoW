
import tornado.escape


class address(str):pass
class uint256(int):pass


CONTRACT_ADDRESS = '0x0000000000000000000000000000000000000001'

contract_address = CONTRACT_ADDRESS


class State:
    def __init__(self, db):
        self.db = db
        self.block_number = 0
        self.pending_state = {}

    # def __setitem__(self, key, value):
    def put(self, key, value):
        value_json = tornado.escape.json_encode(value)
        print('globalstate_%s_%s_%s' % (contract_address, key, str(10**15 - self.block_number).zfill(16)), value_json)
        #self.db.put(('globalstate_%s_%s_%s_%s' % (contract_address, key, str(10**15 - self.block_number).zfill(16), self.block_hash)).encode('utf8'), value_json.encode('utf8'))
        self.pending_state['globalstate_%s_%s_%s' % (contract_address, key, self.block_number)] = value_json

    # def __getitem__(self, key):
    def get(self, key, default):
        value = default
        print(self.pending_state)
        k = 'globalstate_%s_%s_%s' % (contract_address, key, self.block_number)
        print(k)
        if k in self.pending_state:
            value_json = self.pending_state[k]
            value = tornado.escape.json_decode(value_json)
            return value

        try:
            it = self.db.iteritems()
            it.seek(('globalstate_%s_%s' % (contract_address, key)).encode('utf8'))

            # value_json = _trie.get(b'state_%s_%s' % (contract_address, key.encode('utf8')))
            for k, value_json in it:
                if k.startswith(('globalstate_%s_%s' % (contract_address, key)).encode('utf8')):
                    # block_number = 10**15 - int(k.replace(b'%s_%s_' % (contract_address, key.encode('utf8')), b''))
                    value = tornado.escape.json_decode(value_json)
                break

        except:
            pass

        return value


