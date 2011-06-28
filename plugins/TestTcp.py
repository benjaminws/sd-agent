import socket

"""
An TCP check plugin for ServerDensity
"""

OK = 0
NOT_OK = 1

class TestTcp(object):

    def __init__(self, agent_config=None, checks_logger=None, raw_config=None):
        self.agent_config = agent_config
        self.checks_logger = checks_logger
        self.raw_config = raw_config

    def tcp_check(self):

        try:
            host = self.raw_config.get('Main', 'tcp_check_host')
            self.checks_logger.debug('Got host: %s' % host)
        except ConfigParser.NoOptionError:
            self.checks_logger.error('No host defined for tcp checks')

        try:
            ports = self.raw_config.get('Main', 'tcp_check_ports')
            self.checks_logger.debug('Got ports: %s' % ports)
        except ConfigParser.NoOptionError:
            self.checks_logger.error('No ports defined for tcp checks')
            
        status = {}
        for port in ports.split(','):
            self.checks_logger.debug('Trying to connect to %s:%s' %(host, port))
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                s.connect((host, int(port)))
                s.shutdown(2)
                status[port] = OK
                self.checks_logger.info('Successfully connected to %s:%s' %(host, port))
            except Exception, e:
                status[port] = NOT_OK
                self.checks_logger.warn('Failed connecting to %s:%s' %(host, port))
                self.checks_logger.warn('Error: %s' % e)
        return status

    def run(self):
        return self.tcp_check()

if __name__ == '__main__':
    tcp = TestTcp(None, None, None)
    tcp.run()
