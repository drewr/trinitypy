'''
Campaign Monitor API class - Version 2.0

Contributors: Juan Pablo Di Lelle, Jonathan Vanasco, Grant Young

This source code is released under the GNU Lesser General Public License:
http://creativecommons.org/licenses/LGPL/2.1/
'''

from xml.dom import minidom
import urllib2



class CampaignMonitorApi(object):
    '''Provides a wrapper for core functions of the Campaign Monitor API.'''
    
    class CampaignMonitorApiException(Exception):
        '''Exception thrown when Campaign Monitor returns an exception.'''
        pass
    
    
    api_key = "" # the Campaign Monitor API Key (found in the Account settings of Campaign Monitor)
    client_id = "" # the Campaign Monitor Client ID (found in the Client settings of Campaign Monitor)
    _api_namespace = "http://api.createsend.com/api/" # the Campaign Monitor SOAP namespace
    _api_url = "http://api.createsend.com/api/api.asmx" # the URL to the Campaign Monitor API
    debug_soap_requests = False # set True to print the XML sent to the server
    debug_soap_responses = False # set True to print the XML received from the server
    
    __DEVELOPER_DEBUG = False # just for development debug testing
    


    # The following four methods have been deprecated, but are provided for backwards compatibility
    def add(self, list_id, email, name, custom_fields={}):
        return self.subscriber_add( list_id, email, name, custom_fields )

    def unsubscribe(self, list_id, email):
        return self.subscriber_unsubscribe(list_id, email)

    def get_is_subscribed(self, list_id, email):
        return self.subscribers_get_is_subscribed(list_id, email)
        
    def add_and_resubscribe(self, list_id, email, name, custom_fields={}):
        return self.subscriber_add_and_resubscribe(list_id, email, name)
    ## END deprecated methods



    def __init__(self, api_key, client_id):
        '''
        Constructor method.
        
        Keyword arguments:
        - api_key: the Campaign Monitor API Key string (found in the Account settings of Campaign Monitor)
        - client_id: the Campaign Monitor Client ID integer (found in the Client settings of Campaign Monitor)
        '''
        
        self.api_key = api_key
        self.client_id = client_id


    def client_get_lists(self, client_id=None):
        '''
        Maps to the Client.GetLists API method.
        
        Keyword arguments:
        - None
        
        Returns True or False on success (depending on the return value).  Raises CampaignMonitorApiException on errors reported by the API or HttpException if the underlying request fails. Note: "500 Server errors" are raised as a HTTPError exception.
        '''
        
        if not client_id:
            client_id = self.client_id
        
        if not client_id:
            raise CampaignMonitorApi.CampaignMonitorApiException("No ClientID")
        
        method = "Client.GetLists"
        params = self._append_api_key({
            "ClientID" : client_id,
        })
        
        soap_resp = self._soap_api_call(method, params)
        is_error, code, msg = self._soap_is_error(method, soap_resp)
        if is_error:
            raise CampaignMonitorApi.CampaignMonitorApiException(msg)
            
        val = self._parse_soap_multi_value(method, soap_resp)
        return val[method]


    def client_get_supression_list(self, client_id=None):
        '''
        Maps to the Client.GetSuppressionList API method.
        
        Keyword arguments:
        - None
        
        Returns True or False on success (depending on the return value).  Raises CampaignMonitorApiException on errors reported by the API or HttpException if the underlying request fails. Note: "500 Server errors" are raised as a HTTPError exception.
        '''
        
        if not client_id:
            client_id = self.client_id
        
        if not client_id:
            raise CampaignMonitorApi.CampaignMonitorApiException("No ClientID")
        
        method = "Client.GetSuppressionList"
        params = self._append_api_key({
            "ClientID" : client_id,
        })
        
        soap_resp = self._soap_api_call(method, params)
        is_error, code, msg = self._soap_is_error(method, soap_resp)
        if is_error:
            raise CampaignMonitorApi.CampaignMonitorApiException(msg)
            
        val = self._parse_soap_multi_value(method, soap_resp)
        return val[method]


    def subscriber_add(self, list_id, email, name, custom_fields={}):
        '''
        Adds the subscriber only if they have not previously unsubscribed.  Maps to the Subscribers.Add API method.
        
        Keyword arguments:
        - list_id: the integer List ID to add the subscriber to (found in the List settings of Campaign Monitor)
        - email: the email address of the subscriber
        - name: the full name of the subscriber (note: if you need to store Given/First name and Surname/Family name separately you must do this using custom fields as Campaign Monitor does not support this)
        - custom_fields: a dictionary of custom fields to add to the subscriber record
        
        Returns True on success.  Raises CampaignMonitorApiException on errors reported by the API or HttpException if the underlying request fails. Note: "500 Server errors" are raised as a HTTPError exception.
        '''
        
        method = "Subscriber.Add"
        params = self._append_api_key({
            "ListID" : list_id,
            "Email" : email,
            "Name": name
        })
        
        if len(custom_fields) > 0:
            method += "WithCustomFields"
            params["CustomFields"] = self._add_prepare_custom_fields(custom_fields)
        
        soap_resp = self._soap_api_call(method, params)
        is_error, code, msg = self._soap_is_error(method, soap_resp)
        if is_error and code != 0:
            raise CampaignMonitorApi.CampaignMonitorApiException(msg)
        
        return True


    def subscriber_add_and_resubscribe(self, list_id, email, name, custom_fields={}):
        '''
        Adds the subscriber regardless of whether or not they've previously unsubscribed.  Maps to the Subscribers.AddAndResubscribe API method.
        
        Keyword arguments:
        - list_id: the integer List ID to add the subscriber to (found in the List settings of Campaign Monitor)
        - email: the email address of the subscriber
        - name: the full name of the subscriber (note: if you need to store Given/First name and Surname/Family name separately you must do this using custom fields as Campaign Monitor does not support this)
        - custom_fields: a dictionary of custom fields to add to the subscriber record
        
        Returns True on success.  Raises CampaignMonitorApiException on errors reported by the API or HttpException if the underlying request fails. Note: "500 Server errors" are raised as a HTTPError exception.
        '''
        
        method = "Subscriber.AddAndResubscribe"
        params = self._append_api_key({
            "ListID" : list_id,
            "Email" : email,
            "Name": name
        })
        
        if len(custom_fields) > 0:
            method += "WithCustomFields"
            params["CustomFields"] = self._add_prepare_custom_fields(custom_fields)
        
        soap_resp = self._soap_api_call(method, params)
        is_error, code, msg = self._soap_is_error(method, soap_resp)
        if is_error and code != 0:
            raise CampaignMonitorApi.CampaignMonitorApiException(msg)
        
        return True


    def subscriber_unsubscribe(self, list_id, email):
        '''
        Unsubscribes (removes) the subscriber from the list.  Maps to the Subscribers.Unsubscribe API method.
        
        Keyword arguments:
        - list_id: the integer List ID to add the subscriber to (found in the List settings of Campaign Monitor)
        - email: the email address of the subscriber
        
        Returns True on success.  Raises CampaignMonitorApiException on errors reported by the API or HttpException if the underlying request fails. Note: "500 Server errors" are raised as a HTTPError exception.
        '''
        
        method = "Subscriber.Unsubscribe"
        params = self._append_api_key({
            "ListID" : list_id,
            "Email" : email,
        })
        
        soap_resp = self._soap_api_call(method, params)
        is_error, code, msg = self._soap_is_error(method, soap_resp)
        if is_error and code != 202: # 202 errors can be handled silently
            raise CampaignMonitorApi.CampaignMonitorApiException(msg)
        
        return True


    def subscribers_get_active(self, list_id, date_string='1970-01-01 01:01:01'):
        '''
        Maps to the Subscribers.GetActive API method.
        
        Keyword arguments:
        - list_id
        - date_string='1970-01-01 01:01:01'
        
        Returns a list of subscriber data dicts
        '''
        
        method = "Subscribers.GetActive"
        params = self._append_api_key({
            "ListID" : list_id,
            "Date": date_string
        })
        
        soap_resp = self._soap_api_call(method, params)
        is_error, code, msg = self._soap_is_error(method, soap_resp)
        if is_error:
            raise CampaignMonitorApi.CampaignMonitorApiException(msg)
            
        val = self._parse_soap_multi_value(method, soap_resp)
        return val[method]


    def subscribers_get_bounced(self, list_id, date_string='1970-01-01 01:01:01'):
        '''
        Maps to the Subscribers.GetBounced API method.
        
        Keyword arguments:
        - list_id
        - date_string='1970-01-01 01:01:01'
        
        Returns a list of subscriber data dicts
        '''
        
        method = "Subscribers.GetBounced"
        params = self._append_api_key({
            "ListID" : list_id,
            "Date": date_string
        })
        
        soap_resp = self._soap_api_call(method, params)
        is_error, code, msg = self._soap_is_error(method, soap_resp)
        if is_error:
            raise CampaignMonitorApi.CampaignMonitorApiException(msg)
            
        val = self._parse_soap_multi_value(method, soap_resp)
        return val[method]


    def subscribers_get_unsubscribed(self, list_id, date_string='1970-01-01 01:01:01'):
        '''
        Maps to the Subscribers.GetUnsubscribed API method.
        
        Keyword arguments:
        - list_id
        - date_string='1970-01-01 01:01:01'
        
        Returns a list of subscriber data dicts
        '''
        
        method = "Subscribers.GetUnsubscribed"
        params = self._append_api_key({
            "ListID" : list_id,
            "Date": date_string
        })
        
        soap_resp = self._soap_api_call(method, params)
        is_error, code, msg = self._soap_is_error(method, soap_resp)
        if is_error:
            raise CampaignMonitorApi.CampaignMonitorApiException(msg)
        
        val = self._parse_soap_multi_value(method, soap_resp)
        return val[method]


    def subscribers_get_is_subscribed(self, list_id, email):
        '''
        Determines if the user is subscribed to the list.  Maps to the Subscribers.Unsubscribe API method.
        
        Keyword arguments:
        - list_id: the integer List ID to add the subscriber to (found in the List settings of Campaign Monitor)
        - email: the email address of the subscriber
        
        Returns True or False on success (depending on the return value).  Raises CampaignMonitorApiException on errors reported by the API or HttpException if the underlying request fails. Note: "500 Server errors" are raised as a HTTPError exception.
        '''
        
        method = "Subscribers.GetIsSubscribed"
        params = self._append_api_key({
            "ListID" : list_id,
            "Email" : email
        })
        
        soap_resp = self._soap_api_call(method, params)
        is_error, code, msg = self._soap_is_error(method, soap_resp)
        if is_error:
            raise CampaignMonitorApi.CampaignMonitorApiException(msg)
        
        val = self._parse_soap_single_value(method, soap_resp)
        
        return (val == "True")


    def subscribers_get_single_subscriber(self, list_id, email):
        '''
        Maps to the Subscribers.GetSingleSubscriber API method.
        
        Keyword arguments:
        - list_id: the integer List ID to which the subscriber belongs (found in the List settings of Campaign Monitor)
        - email: the email address of the subscriber
        
        Returns dict
        '''
        
        method = "Subscribers.GetSingleSubscriber"
        params = self._append_api_key({
            "ListID" : list_id ,
            "EmailAddress" : email ,
        })
        
        soap_resp = self._soap_api_call(method, params)
        is_error, code, msg = self._soap_is_error(method, soap_resp)
        if is_error:
            raise CampaignMonitorApi.CampaignMonitorApiException(msg)
        
        val = self._parse_soap_multi_value(method, soap_resp)
        return val


    # 'private' methods
    def _add_prepare_custom_fields(self, custom_fields):
        '''Supporting method for add and add_and_resubscribe.  Creates the XML for custom fields.
        
        Keyword arguments:
        - custom_fields: a dictionary of fields to generate XML for.
        
        Returns fields in format:
        <SubscriberCustomField>
            <Key>string</Key>
            <Value>string</Value>
        </SubscriberCustomField>'''
        
        if custom_fields == None or len(custom_fields) == 0:
            return ""
        
        resp = ""
        for k, v in custom_fields.items():
            resp += self._soap_xmlise_dict({ "SubscriberCustomField" : { "Key": k, "Value": v } })
        
        return resp


    def _append_api_key(self, data):
        '''
        Appends the ApiKey entry to the supplied data dictionary.
        
        Keyword arguments:
        - data: the dictionary to add the API Key to
        '''
        data["ApiKey"] = self.api_key
        return data


    def _soap_api_call(self, method, params):
        '''
        Accesses the API using SOAP.
        
        Keyword arguments:
        - method: the API method to call.
        - params: a dictionary of parameters to insert
        '''
        soap_params = self._soap_xmlise_dict(params)
        
        variables = {
            "method" : method,
            "namespace" : self._api_namespace,
            "params" : soap_params
        }
        
        env = '''<?xml version="1.0" encoding="utf-8"?>
        <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xmlns:xsd="http://www.w3.org/2001/XMLSchema"
          xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
          <soap:Body>
            <%(method)s xmlns="%(namespace)s">
              %(params)s
            </%(method)s>
          </soap:Body>
        </soap:Envelope>''' % variables
        
        soap_action = self._api_namespace+method
        
        if self.debug_soap_requests:
            print "Request %s (SOAPAction: %s):" % (self._api_url, soap_action)
            print env
        
        req = urllib2.Request(self._api_url, env)
        req.add_header('Content-Type', 'text/xml')
        req.add_header('SOAPAction', soap_action)
        try:
            hndl = urllib2.urlopen(req)
        except urllib2.HTTPError, ex:
            if self.debug_soap_responses:
                print "Response:"
                print ex.read()
            raise ex
        
        resp = hndl.read()
        if self.debug_soap_responses:
            print "Response:"
            print resp
        
        return resp


    def _soap_xmlise_dict(self, items):
        '''
        Supporting method for _soap_api_call.  Converts the dictionary into an XML string to be inserted into the SOAP envelope.
        
        Keyword arguments:
        - items: dictionary of items to convert to XML.
        '''
        if items == None or len(items) == 0:
            return ""
        
        if type(items) != dict:
            raise Exception("This method only supports dictionary types")
        
        resp = ""
        tmpl = "<%(k)s>%(v)s</%(k)s>\n"
        for k, v in items.items():
            if (type(v) == dict):
                resp += tmpl % { "k":k, "v": self._soap_xmlise_dict(v) }
            else:
                resp += tmpl % { "k":k, "v": str(v) }
        
        return resp


    def _soap_is_error(self, method, soap_resp):
        '''
        The Campaign Monitor API returns some results in the format:
        <soap:Body>
            <{{method}}Response xmlns="http://app.campaignmonitor.com/api/">
            
              <{{method}}Result>
                <Code>int</Code>
                <Message>string</Message>
              </{{method}}Result>
            </{{method}}Response>
        
        This method parses the supplied SOAP response and returns the code and message.
        
        Keyword arguments:
        - soap_resp: the SOAP response to parse
        - method: the original method called
        
        Returns (is_error, code, message) - is_error = True/False - true if != 0, code = int, message = string
        '''
        doc = minidom.parseString(soap_resp)
        
        if doc.hasChildNodes:
            code_nodes = doc.getElementsByTagName("Code")
            if len(code_nodes) != 0:
                code = code_nodes[0].firstChild.nodeValue
                if code != "0":
                    message_nodes = doc.getElementsByTagName("Message")
                    msg = ""
                    if len(message_nodes) != 0:
                        msg = message_nodes[0].firstChild.nodeValue
                    
                    return (True, int(code), msg)
        
        return (False, 0, "")


    def _parse_soap_single_value(self, method, soap_resp):
        '''
        The Campaign Monitor API returns some values in the format:
        <soap:Body>
            <{{method}}Response xmlns="http://app.campaignmonitor.com/api/">
              <{{method}}Result>string</{{method}}Result>
            </{{method}}Response>
          </soap:Body>
        
        This method parses such responses and returns the enclosed value.
        
        Keyword arguments:
        - soap_resp: the SOAP response to parse
        
        Returns the string value of the response.  You will need to coerce in the required type if not a string.
        '''
        doc = minidom.parseString(soap_resp)
        if doc.hasChildNodes:
            result_nodes = doc.getElementsByTagName(method+"Result")
            if len(result_nodes) == 1:
                node = result_nodes[0]
                if node.hasChildNodes:
                    return node.firstChild.nodeValue
        
        return None


    def _parse_soap_multi_value(self, method, soap_resp):
        '''
        The Campaign Monitor API returns some values in the format:
        
        <soap:Body>
            <{{method}}Response xmlns="http://api.createsend.com/api/">
                <{{method}}Result xsi:type="ArrayOfList">
                    <List>
                        <ListID>string</ListID>
                        <Name>string</Name>
                    </List>
                    <List>
                </{{method}}Result>
            </{{method}}Response>
        </soap:Body>
        
        This method tries to parse such responses and returns the enclosed values as something that is easier to work with.
        
        Keyword arguments:
        - method
        - soap_resp: the SOAP response to parse
        '''
        
        rval= {}
        doc = minidom.parseString(soap_resp)
        if doc.hasChildNodes:
            result_nodes = doc.getElementsByTagName(method+"Result")
            if len(result_nodes) == 1:
                node = result_nodes[0]
                rtype = node._attrs['xsi:type'].value
                if self.__DEVELOPER_DEBUG:
                    print rtype
                if rtype == 'ArrayOfList':
                    rval[method] = []
                    if not node.hasChildNodes:
                        raise ValueError('No child nodes?')
                    for node_list in node.childNodes:
                        node_info = {}
                        for i in node_list.childNodes:
                            node_info[i.nodeName] = i.firstChild.nodeValue
                        rval[method].append(node_info)
                elif rtype == 'ArrayOfSubscriber':
                    rval[method] = []
                    if not node.hasChildNodes:
                        raise ValueError('No child nodes?')
                    for node_subscriber in node.childNodes:
                        node_info = self._parse_soap__subscriber_node(node_subscriber)
                        rval[method].append(node_info)
                elif rtype == 'Subscriber':
                    rval[method] = []
                    node_subscriber = result_nodes[0]
                    node_info = self._parse_soap__subscriber_node(node_subscriber)
                    rval[method].append(node_info)
                else:
                   raise CampaignMonitorApiException("Unsupported xsi:type in results node")
        return rval


    def _parse_soap__subscriber_node(self, node_list):
        '''
        Supporting method for _parse_soap_multi_value function.
        '''
        
        node_info= {}
        for i in node_list.childNodes:
            if i.nodeName != 'CustomFields':
                value = None
                if i.hasChildNodes and i.firstChild :
                    value = i.firstChild.nodeValue
                node_info[i.nodeName] = value
            else:
                cnode_info = {}
                for ii in i.childNodes: # this is called u'SubscriberCustomField'
                    if ii.hasChildNodes:
                        c_key = None
                        c_value = None
                        for iii in ii.childNodes:
                            if iii.nodeName == 'Key':
                                c_key = iii.firstChild.nodeValue
                            elif iii.nodeName == 'Value':
                                c_value = iii.firstChild.nodeValue
                        if c_key :
                            cnode_info[c_key] = c_value
                node_info[i.nodeName] = cnode_info
        return node_info