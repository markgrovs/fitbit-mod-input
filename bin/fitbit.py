#!/usr/bin/env python

from splunklib.modularinput import *
from splunklib.client import Inputs, Service

import fitbit
import sys, urllib2, json, datetime, time



try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

class Fitbit_Data(Script):
    def get_scheme(self):
        scheme = Scheme("Fitbit Data")
        scheme.use_single_instance = False

        client_key_arg = Argument("client_key")
        client_key_arg.data_type = Argument.data_type_string
        client_key_arg.description = "Client (Consumer) Key"
        client_key_arg.required_on_create = True
        scheme.add_argument(client_key_arg)

        client_secret_arg = Argument("client_secret")
        client_secret_arg.data_type = Argument.data_type_string
        client_secret_arg.description = "Client (Consumer) Secret"
        client_secret_arg.required_on_create = True
        scheme.add_argument(client_secret_arg)

        resource_owner_key_arg = Argument("resource_owner_key")
        resource_owner_key_arg.data_type = Argument.data_type_string
        resource_owner_key_arg.description = "Resource Owner Key"
        resource_owner_key_arg.required_on_create = True
        scheme.add_argument(resource_owner_key_arg)

        resource_owner_secret_arg = Argument("resource_owner_secret")
        resource_owner_secret_arg.data_type = Argument.data_type_string
        resource_owner_secret_arg.description = "Resource Owner Secret"
        resource_owner_secret_arg.required_on_create = True
        scheme.add_argument(resource_owner_secret_arg)


        return scheme

    def stream_events(self, inputs, ew):
        try:
            for input_name, input_item in inputs.inputs.iteritems():
                client_key = str(input_item["client_key"])
                client_secret = str(input_item["client_secret"])
                resource_owner_key = str(input_item["resource_owner_key"])
                resource_owner_secret = str(input_item["resource_owner_secret"])

                client = fitbit.Fitbit(client_key, client_secret, resource_owner_key=resource_owner_key, resource_owner_secret=resource_owner_secret)
                
                date = datetime.date(2014, 8, 1)
                # result = client.get_sleep(date)
                result = client.time_series('activities/tracker/steps', base_date='2014-08-01', period=None, end_date='2014-08-01')

                event = Event()
                event.stanza = input_name
                event.data = json.dumps(result, sort_keys = True)
                t = datetime.datetime(2014, 8, 1)
                event.time = time.mktime(t.timetuple())
                ew.write_event(event)
        except Exception as e:
            sys.stderr.write(str(e) + "\n")


if __name__ == "__main__":
    sys.exit(Fitbit_Data().run(sys.argv))