"""
Places orders and requests the status from a server.
"""
from urllib           import urlencode
from urllib2          import HTTPDigestAuthHandler, build_opener
from HTTPDigestServer import realm
from Order            import Order

class RestClient(object):
    """
    Handles all contact with a server.
    """

    def __init__(self, address, user, password):
        """
        Constructor. Any operations performed with an
        instance of a client are directed to the server with the
        given address, using the given login data.

        @type  address: str
        @param address: The base url of the server.
        @type  user: str
        @param user: The login name on the server.
        @type  password: str
        @param password: The password of the user.
        """
        self.address = 'http://' + address
        self.handler = HTTPDigestAuthHandler()
        self.opener  = build_opener(self.handler)
        self.handler.add_password(realm  = realm,
                                  uri    = self.address,
                                  user   = user,
                                  passwd = password)

    def place_order(self, order):
        """
        Sends the given order to the server, and updates the status
        of the order accordingly.

        @type  order: Order
        @param order: The order that is placed.
        """
        if order.status != 'new':
            msg = 'order status is "%s", should be "new"' % order.status
            raise ValueError(msg)
        if not order.is_valid():
            raise ValueError('incomplete or invalid order')

        order.status = 'accepted'
        url          = self.address + '/order/'
        xml          = order.toxml()
        result       = self.opener.open(url, xml)
        if result.getcode() != '100':
            raise Exception(result.read())

    def get_order_from_id(self, order_id):
        """
        Returns the order with the given id.

        @type  order_id: str
        @param order_id: The id of the order.
        @rtype:  Order
        @return: The order if it exists, None otherwise.
        """
        raise NotImplementedError()

    def get_order_status_from_id(self, order_id):
        """
        Returns the status of the order with the given id if it
        exists. Returns 'not-found' otherwise.

        @type  order_id: str
        @param order_id: The id of the order.
        @rtype:  str
        @return: The status of the order.
        """
        raise NotImplementedError()

if __name__ == '__main__':
    import sys, time
    if len(sys.argv) == 5:
        address     = sys.argv[1]
        user        = sys.argv[2]
        password    = sys.argv[3]
        order       = Order.from_xml_file(sys.argv[4])
    else:
        sys.stderr.write('Syntax: ip[:port] user password order\n')
        sys.exit(1)

    client = RestClient(address, user, password)
    #print "Status:", client.get_order_status_from_id(order.id)
    client.place_order(order)
    print "Placed order", order.id
    sys.exit()
    #status = client.get_order_status_from_id(order.id)

    while status != 'completed':
        print "Status:", status
        time.sleep(.1)
        status = client.get_order_status_from_id(order.id)

    print "Status:", status