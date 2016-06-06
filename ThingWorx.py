import json
import requests
from requests.auth import HTTPBasicAuth


class ThingWorx:
    def __init__(self, app_key=None, user_name=None, user_pass=None, base_url=None):
        self.request = requests
        if app_key is None:
            self.appKey = "e5ced0ce-637f-4b33-a4d3-cc3597af0b71"
            self.base_url = "http://52.202.207.237/Thingworx"
            self.user_name = "smerkousdavid@gmail.com"
            self.user_pass = "holycrap"
        else:
            self.appKey = app_key
            self.base_url = base_url
            self.user_name = user_name
            self.user_pass = user_pass

        self.selected_thing = "RobotData"
        self.encoding = "UTF-8"

        self.headers = {'Connection': 'keep-alive',
                        'X-Requested-With': 'XMLHttpRequest',
                        'Content-Type': 'application/json',
                        'DNT': '1',
                        'Accept-Encoding': 'gzip, deflate',
                        'appKey': self.appKey,
                        'Accept': 'application/json, application/json-compressed, text/javascript, */*, q=0.01'}

    def set_thing(self, thing_name):
        self.selected_thing = str(thing_name)

    def put_property(self, property_name, value="", thing=None):
        props_path = "%s/Things/%s/Properties/*" % (self.base_url, self.selected_thing if thing is None else thing)
        # if isinstance(property_name, dict):
        formulated = property_name
        # else:
        # formulated = {property_name: value}
        try:
            req = self.request.put(props_path, auth=HTTPBasicAuth(self.user_name, self.user_pass), headers=self.headers,
                                   data=json.dumps(formulated))
            try:
                print "Request body %s" % req.content
            except (TypeError, ValueError):
                pass
            return req.status_code
        except (ValueError, IOError, TypeError), err:
            print "Failed put request: %s" % str(err)
            return 400

    '''
    def delete_property(self, property_name, value, thing=None):
        props_path = "%s/Things/%s/PropertyDefinitions/%s" % (self.base_url,
                                                              self.selected_thing if thing is None else thing,
                                                              property_name)
        #formulated = {property_name: value}
        try:
            req = self.request.delete(props_path, auth=HTTPBasicAuth(self.user_name, self.user_pass),
                                      headers=self.headers)#, data=json.dumps(formulated))
            return req.status_code
        except (ValueError, IOError, TypeError), err:
            print "Failed put request: %s" % str(err)
            return 400
    '''

    def get_property(self, property_name=None, thing=None):
        props_path = "%s/Things/%s/Properties/" % (self.base_url, self.selected_thing if thing is None else thing)  # ,
        # property_name)
        try:
            req = self.request.get(props_path, auth=HTTPBasicAuth(self.user_name, self.user_pass), headers=self.headers)
            jsons = json.loads(req.text)
            rows = jsons[u'rows']
            '''
            if len(rows) > 1:
                for num in range(0, len(rows)):
                    rows[num] = str(rows[num][u'%s' % property_name])
                    print rows[num]
                return rows
            '''
            if property_name is not None:
                value = rows[0][u'%s' % property_name]
                return str(value)
            else:
                return rows[0]
        except (ValueError, IOError, TypeError), err:
            print "Failed get request: %s" % str(err)
            return None
