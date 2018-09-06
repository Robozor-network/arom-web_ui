from handler.base import BaseHandler
import glob
import json
import rospy


class pymlabBase(BaseHandler):
    def get(self, path = None):
        print('OK')
        file = rospy.get_param('/arom/node/pymlab_node/feature/pymlab_structure/cfg')
        self.render('modules/features/pymlab.hbs', current_file = file)

    def post(self, path = None):
        operation = self.get_argument('operation', 'get_json')
        print('operation>>', self.get_argument('operation', 'XXX'))
        if operation == 'get_json':
            filename = self.get_argument('file', False)
            print(filename)
            if filename and filename != 'false':
                file = filename
            else:
                file = glob.glob("/home/odroid/robozor/station/pymlab_presets/*.json")[0]
                file = rospy.get_param('/arom/node/pymlab_node/feature/pymlab_structure/cfg')
            json_data = json.load(open(file))

            self.write(json_data)

        elif operation == 'push_json':
            filename = self.get_argument('file')
            data = json.loads(self.get_argument('data'))
            print(filename, data)

            if True: #TODO: overeni spravne cesty....
                with open(filename, 'w') as f:
                    json.dump(data, f)

            self.write('OK')