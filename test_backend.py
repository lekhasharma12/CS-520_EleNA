from services.route_finder import dijkstras, astar
from utils.utils import *
import unittest
from models.route import Route
import osmnx as ox


class TestRouteFinder(unittest.TestCase):
    #Positive TC to check whether all inputs are correct
    def test_validate_for_errors_POS(self):
        elevation_type = 'max'
        percent_increase = 30
        mode = 'bike'
        error, error_msg = validate_for_errors(elevation_type, percent_increase, mode)
        self.assertEqual(error, False)

    #Negative TC when mode type is wrong
    def test_validate_for_errors_NEG_MODE(self):
        elevation_type = 'max'
        percent_increase = 20
        mode = 'car'
        error, error_msg = validate_for_errors(elevation_type, percent_increase, mode)
        self.assertEqual(error, True)
        self.assertIn(error_msg,'True Mode of transport is incorrect. Please select either walking or biking')

    #Negative TC when precentage increase is wrong
    def test_validate_for_errors_NEG_PERCENTAGE_INC(self):
        elevation_type = 'max'
        percent_increase = 200
        mode = 'walk'
        error, error_msg = validate_for_errors(elevation_type, percent_increase, mode)
        self.assertEqual(error, True)
        self.assertIn(error_msg,'Percentage increase in the shortest route is greater than 100. Please select a value between 0-100')

    #Test dijsktras for shortest path 
    def test_dijskstras(self):
        elevation_type = 'max'
        percent_increase = 20
        mode = 'bike'
        source = "147, Brittany Manor Drive, The Boulders, Mill Valley, Amherst, Hampshire County, Massachusetts, 01002"
        destination = "Puffers Pond, Amherst"
        city = "Amherst"
        state = "Massachusetts"
        source_coordinates = ox.geocode(source)
        destination_coordinates = ox.geocode(destination)
        route = Route(source_coordinates, destination_coordinates, elevation_type, percent_increase, mode, city, state)
        expected_result = {'elevation': -29.0, 'distance': 8581.726999999999, 'path': [7058913917, 7058913916, 66656988, 66643538, 66730551, 66770901, 66641424, 66667006, 66723660, 66626867, 7161863590, 9079116515, 66767206, 66764057, 7148671787, 9065016052, 9065016054, 66631944, 66751010, 66715414, 8320860424, 8320860420, 66646853, 3033372899, 66652025, 3023092508, 66591361, 6775672007, 66721706, 66713678, 66704925, 66745361, 66704169, 66686920, 6312825848, 3033372907, 66593243, 6302553059, 4919132556, 66618152, 66613374, 6346197783, 5869847103, 6757293529, 6302552392, 66714028, 8530933989, 6312825851, 66696544, 6312825856, 6050584821, 6302552397, 6050584833, 6336753691, 66672799, 9052567912, 6346197711, 6346197718, 66766087, 4829289747, 5489277570, 66767773, 6744481746, 6744481752, 6744481753, 6744481781, 6744481776, 6205848223, 66692123, 66768883, 66743313, 66619622, 9057689664, 66773834, 66717133, 66599020, 66775470, 9050970126, 66763147, 6313650221, 66612825, 66655982, 6313650218, 66764005, 6951510799, 9076976982, 9079037074, 6988996104, 5261586177, 8454885986, 66739703, 4594428780, 66702095, 8320513042, 66597142, 8631420487, 8191010069, 66680313, 66712389, 66654462, 66760756, 66745889, 9076367307, 8320513038, 9050356671, 9050356669, 2111347918, 66611431, 66691893, 66615687, 66750271, 66686901, 1669520735, 1669520769]}
        result_dijkstras = dijkstras(route.graph, route.source_node, route.destination_node)
        self.assertDictEqual(expected_result, result_dijkstras)

    #POSITIVE TC to get node from given coordinates
    def test_get_node_from_coordinates(self):
        elevation_type = 'max'
        percent_increase = 20
        mode = 'bike'
        source = "147, Brittany Manor Drive, The Boulders, Mill Valley, Amherst, Hampshire County, Massachusetts, 01002"
        destination = "Puffers Pond, Amherst"
        city = "Amherst"
        state = "Massachusetts"
        source_coordinates = ox.geocode(source)
        destination_coordinates = ox.geocode(destination)
        route = Route(source_coordinates, destination_coordinates, elevation_type, percent_increase, mode, city, state)
        result = get_node_from_coordinates(route.graph, source_coordinates)
        self.assertEqual(7058913917,result)

    def test_get_elevation_data(self):
        elevation_type = 'max'
        percent_increase = 20
        mode = 'bike'
        source = "147, Brittany Manor Drive, The Boulders, Mill Valley, Amherst, Hampshire County, Massachusetts, 01002"
        destination = "Puffers Pond, Amherst"
        city = "Amherst"
        state = "Massachusetts"
        source_coordinates = ox.geocode(source)
        destination_coordinates = ox.geocode(destination)
        route = Route(source_coordinates, destination_coordinates, elevation_type, percent_increase, mode, city, state)
        result = get_elevation_data(route.graph)
        print("result of get ele data",result)

        '''
    def test_add_elevation_data(self):
        elevation_type = 'max'
        percent_increase = 20
        mode = 'bike'
        source = "147, Brittany Manor Drive, The Boulders, Mill Valley, Amherst, Hampshire County, Massachusetts, 01002"
        destination = "Puffers Pond, Amherst"
        city = "Amherst"
        state = "Massachusetts"
        source_coordinates = ox.geocode(source)
        destination_coordinates = ox.geocode(destination)
        route = Route(source_coordinates, destination_coordinates, elevation_type, percent_increase, mode, city, state)
        result = add_elevation_data(route.graph)
        self.assertIn(result,'MultiDiGraph with 4219 nodes and 10608 edges')
        '''
if __name__ == '__main__':
    unittest.main()
