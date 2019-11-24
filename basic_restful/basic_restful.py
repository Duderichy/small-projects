from flask import Flask, g
from flask_restful import Resource, Api, reqparse
import shelve

app = Flask(__name__)
api = Api(app)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = shelve.open("gps_data.db")
    return db

@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

#################################################
# Interview code
#################################################

def store_gps_list(list_gps_data):
    shelf = get_db()
    if 'gps_data' not in shelf:
        shelf['gps_data'] = []
    data_list = shelf['gps_data']
    for packet in list_gps_data:
        data_list.append(packet)
    shelf['gps_data'] = data_list

def get_gps_list():
    shelf = get_db()
    return shelf['gps_data']

def get_db_time_range(time_start, time_end):
    shelf = get_db()
    db_data = shelf['gps_data']
    data_in_range = []
    for data_packet in db_data:
        if time_start < data_packet['time_unix_epoch'] \
            and data_packet['time_unix_epoch'] < time_end:
            data_in_range.append(data_packet)
    return data_in_range

def collect_field(data_list, field_accessor):
    return list(map(field_accessor, data_list))

def get_db_aggregate(time_start, time_end, aggregate_type):
    data_in_range = get_db_time_range(time_start, time_end)
    field_accessor = lambda x: x['speed']
    field_values = collect_field(data_in_range, field_accessor)
    return aggregate_type(field_values)
        

class SeeData(Resource):
    def get(self):
        shelf = get_db()
        # print(shelf['gps_data'])
        return shelf['gps_data']

# Request structure for posting data to /store_list
# {
# 'data' :
#  [
#    {
#        "horizontal_accuracy": 30.0,
#        "latitude": 37.60609370534149,
#        "longitude": -122.38603492222053,
#        "speed": 12.2001953125,
#        "time_unix_epoch": 1498073665.3378906
#    },
#    {
#        "horizontal_accuracy": 30.0,
#        "latitude": 37.606027165839485,
#        "longitude": -122.38593305914674,
#        "speed": 12.16015625,
#        "time_unix_epoch": 1498073666.0454102
#    } 
#  ] 
# }

# expects request with 'data' field to be stored in db
# data field should be a list of gps data to be stored
class StoreList(Resource):
    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('data', required=True, location='json', type=list)

        args = parser.parse_args()

        shelf = get_db()

        data = args['data']

        store_gps_list(data)

        return {'message': 'gps data added to db', 'data' : args['data']} , 201

class GetList(Resource):
    def get(self):
        parser = reqparse.RequestParser()

        parser.add_argument('time_start', required=True, type=float)
        parser.add_argument('time_end', required=True, type=float)

        args = parser.parse_args()
        start_time = args['time_start']
        end_time = args['time_end']

        data = get_db_time_range(start_time, end_time)

        return {'message' : 'Data retrieved', 'data' : data} , 200

def average(values):
    return sum(values) / len(values)

def median(values):
    if not values:
        return None
    list_len = len(values)
    if len(values) % 2 == 0:
        return (values[list_len // 2] + values[list_len // 2 + 1]) / 2
    else:
        return values[list_len // 2]

def distance_traveled(avg_speeds, durations):
    return sum(speed * duration
        for speed, duration in zip(avg_speeds, durations))

def time_length(sorted_times):
    prev = None
    time_intervals = []
    for time in sorted_times:
        if prev:
            time_intervals.append(time - prev)
        prev = time
    return time_intervals

def midpoint_speeds(speed_list):
    prev = None
    speed_intervals = []
    for speed in speed_list:
        if prev:
            speed_intervals.append((speed + prev) / 2)
        prev = speed
    return speed_intervals

class GetAggregate(Resource):
    aggregate_type_functions = {
    'max' : max,
    'min' : min,
    'average' : average,
    'median' : median
    }

    def get(self):
        parser = reqparse.RequestParser()

        parser.add_argument('time_start', required=True, type=float)
        parser.add_argument('time_end', required=True, type=float)
        parser.add_argument('aggregate_type', required=True)

        args = parser.parse_args()

        start_time = args['time_start']
        end_time = args['time_end']
        aggregate_type = args['aggregate_type']
        func = self.aggregate_type_functions[aggregate_type]

        return_value = get_db_aggregate(start_time, end_time, func)

        return {'message' : 'Aggregate Calculated', 'data' : return_value} , 200

class GetDistanceTraveled(Resource):
    def get(self):
        gps_list = get_gps_list()
        gps_list_sorted = sorted(gps_list, key = \
            lambda data_dict: data_dict['time_unix_epoch'])
        time_list = [gps_point['time_unix_epoch']
            for gps_point in gps_list_sorted]
        interval_list = time_length(time_list)
        midpoint_speed_list = midpoint_speeds([gps_point['speed']
            for gps_point in gps_list_sorted])
        aprox_distance = distance_traveled(midpoint_speed_list, interval_list)
        return {'message' : 'Aproximate distance traveled calculated',
                'data' : aprox_distance}, 200

api.add_resource(StoreList, '/store_list')

api.add_resource(GetList, '/get_list')

api.add_resource(GetAggregate, '/get_aggregate')

api.add_resource(GetDistanceTraveled, '/get_distance_traveled')

# DEBUG
api.add_resource(SeeData, '/see_data')


if __name__=='__main__':
    app.run(debug=True)