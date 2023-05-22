from services.route_finder import dijkstras, astar
from utils.utils import *
import unittest
from models.route import Route
import osmnx as ox


def load_graph():
    graph = pickle.load(open('./graphs/test.pickle', 'rb'))
    return graph

class TestRouteFinder(unittest.TestCase):
    '''
    #UTILS TESTS
    #Positive TC to check whether all inputs are correct
    def test_validate_for_errors_POS(self):
        elevation_type = 'max'
        percent_increase = 30
        mode = 'bike'
        source = "147 Brittany Manor Drive"
        dest = "UMass Amherst"
        error, error_msg = validate_for_errors(source, dest, elevation_type, percent_increase, mode)
        self.assertEqual(error, False)

    #Negative TC when mode type is wrong
    def test_validate_for_errors_NEG_MODE(self):
        elevation_type = 'max'
        percent_increase = 20
        mode = 'car'
        source = "147 Brittany Manor Drive"
        dest = "UMass Amherst"
        error, error_msg = validate_for_errors(source, dest, elevation_type, percent_increase, mode)
        self.assertEqual(error, True)
        self.assertIn(error_msg,'True Mode of transport is incorrect. Please select either walking or biking')

    #Negative TC when precentage increase is wrong
    def test_validate_for_errors_NEG_PERCENTAGE_INC(self):
        elevation_type = 'max'
        percent_increase = 200
        mode = 'walk'
        source = "147 Brittany Manor Drive"
        dest = "UMass Amherst"
        error, error_msg = validate_for_errors(source, dest, elevation_type, percent_increase, mode)
        self.assertEqual(error, True)
        self.assertIn(error_msg,'Percentage increase in the shortest route is greater than 100. Please select a value between 0-100')
    
    #POSITIVE TC to get node from given coordinates
    def test_get_node_from_coordinates(self):
        source = "147, Brittany Manor Drive, The Boulders, Mill Valley, Amherst, Hampshire County, Massachusetts, 01002"
        graph = load_graph()
        result = get_node_from_coordinates(graph, ox.geocode(source))
        self.assertEqual(1439024846, result)
    
    def test_get_elevation_data(self):
        graph = load_graph()
        result = get_elevation_data(graph)
        expected_result = [{'elevation': 65.0}, {'elevation': 61.0}, {'elevation': 63.0}, {'elevation': 72.0}, {'elevation': 72.0}, {'elevation': 68.0}, {'elevation': 67.0}, {'elevation': 65.0}, {'elevation': 66.0}, {'elevation': 57.0}, {'elevation': 58.0}, {'elevation': 62.0}, {'elevation': 68.0}, {'elevation': 72.0}, {'elevation': 74.0}, {'elevation': 69.0}, {'elevation': 69.0}, {'elevation': 69.0}, {'elevation': 67.0}, {'elevation': 61.0}, {'elevation': 58.0}, {'elevation': 60.0}, {'elevation': 59.0}, {'elevation': 59.0}]
        self.assertEqual(expected_result, result)
      
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
        graph = load_graph()
        route = Route(source_coordinates, destination_coordinates, elevation_type, percent_increase, mode, city, state)
        result = add_elevation_data(graph)
        
    def test_get_place_mode_graph(self):
        mode = 'walk'
        city = 'Amherst'
        state = 'Massachusetts'
        result = get_place_mode_graph(city,state,mode)
        self.assertIn(str(result),'MultiDiGraph with 7280 nodes and 20300 edges')
            

    def test_make_graph(self):
        mode = 'walk'
        source = "147, Brittany Manor Drive, The Boulders, Mill Valley, Amherst, Hampshire County, Massachusetts, 01002"
        result = make_graph(source,mode)
        self.assertIn(str(result),"MultiDiGraph with 32309 nodes and 86984 edges")
        
    #ROUTE_FINDER TESTS
    #Test dijsktras for shortest path 
    def test_dijskstras(self):
        elevation_type = 'max'
        percent_increase = 20
        mode = 'bike'
        source = "147, Brittany Manor Drive, The Boulders, Mill Valley, Amherst, Hampshire County, Massachusetts, 01002"
        destination = "Puffers Pond, Amherst"
        city = "Amherst"
        state = "Massachusetts"
        route = Route(source, destination, elevation_type, percent_increase, mode, city, state)
        expected_result = {'elevation': -29.0, 'distance': 8314.775000000001, 'path': [7058913917, 7058913916, 66656988, 66643538, 6655624009, 6655623989, 6655624004, 6655623992, 6655623986, 6655623985, 66641424, 66667006, 6655623965, 66723660, 6655623958, 6655623931, 6655623929, 6655623928, 6655623901, 6655623902, 7148671786, 9065016058, 9065016059, 9065016054, 66631944, 66751010, 6655623924, 66715414, 8320860424, 8320860420, 66646853, 3033372899, 66652025, 66591361, 6775672007, 66721706, 66713678, 3271341815, 66704925, 3271344786, 66745361, 3271344801, 6302552893, 66704169, 6302552856, 66686920, 6312825848, 3033372907, 66593243, 6302553059, 6302552850, 4919132556, 6302552836, 66618152, 66613374, 6302552831, 6346197783, 6302552462, 5869847103, 6757293529, 6302552392, 6302552453, 66714028, 6302552451, 8530933989, 6312825851, 66696544, 6312825856, 6050584821, 6744652172, 6302552397, 6050584833, 6336753691, 66672799, 9052567912, 6744652169, 6346197711, 6346197718, 6744652168, 66766087, 4829289747, 5489277570, 66767773, 6744493013, 6744481746, 6744481752, 6744481753, 6744493019, 6744481781, 6744481776, 6205848223, 66692123, 6304679368, 66768883, 66743313, 66619622, 9057689664, 66773834, 6304679589, 66717133, 66599020, 66775470, 9050970126, 66763147, 6313650221, 66612825, 66655982, 6313650218, 6765025817, 66764005, 6951510799, 9076976982, 9079037074, 6988996104, 5261586177, 8454885986, 66739703, 4594428780, 66702095, 8320513042, 66597142, 8631420487, 8191010069, 66680313, 66712389, 66654462, 66760756, 66701447, 66745889, 9076367307, 8320513038, 9050356671, 9050356669, 2111347918, 66611431, 66691893, 66746572, 1843788747, 66732034, 1669520735, 1669520769]}
        result_dijkstras = dijkstras(route.graph, route.source_node, route.destination_node)
        self.assertDictEqual(expected_result, result_dijkstras)

    #Test astar for shortest path 
    def test_astar(self):
        elevation_type = 'max'
        percent_increase = 20
        mode = 'bike'
        source = "147, Brittany Manor Drive, The Boulders, Mill Valley, Amherst, Hampshire County, Massachusetts, 01002"
        destination = "Puffers Pond, Amherst"
        city = "Amherst"
        state = "Massachusetts"
        route = Route(source, destination, elevation_type, percent_increase, mode, city, state)
        expected_result = {'elevation': -29.0, 'distance': 8314.775000000001, 'path': [7058913917, 7058913916, 66656988, 66643538, 6655624009, 6655623989, 6655624004, 6655623992, 6655623986, 6655623985, 66641424, 66667006, 6655623965, 66723660, 6655623958, 6655623931, 6655623929, 6655623928, 6655623901, 6655623902, 7148671786, 9065016058, 9065016059, 9065016054, 66631944, 66751010, 6655623924, 66715414, 8320860424, 8320860420, 66646853, 3033372899, 66652025, 66591361, 6775672007, 66721706, 66713678, 3271341815, 66704925, 3271344786, 66745361, 3271344801, 6302552893, 66704169, 6302552856, 66686920, 6312825848, 3033372907, 66593243, 6302553059, 6302552850, 4919132556, 6302552836, 66618152, 66613374, 6302552831, 6346197783, 6302552462, 5869847103, 6757293529, 6302552392, 6302552453, 66714028, 6302552451, 8530933989, 6312825851, 66696544, 6312825856, 6050584821, 6744652172, 6302552397, 6050584833, 6336753691, 66672799, 9052567912, 6744652169, 6346197711, 6346197718, 6744652168, 66766087, 4829289747, 5489277570, 66767773, 6744493013, 6744481746, 6744481752, 6744481753, 6744493019, 6744481781, 6744481776, 6205848223, 66692123, 6304679368, 66768883, 66743313, 66619622, 9057689664, 66773834, 6304679589, 66717133, 66599020, 66775470, 9050970126, 66763147, 6313650221, 66612825, 66655982, 6313650218, 6765025817, 66764005, 6951510799, 9076976982, 9079037074, 6988996104, 5261586177, 8454885986, 66739703, 4594428780, 66702095, 8320513042, 66597142, 8631420487, 8191010069, 66680313, 66712389, 66654462, 66760756, 66701447, 66745889, 9076367307, 8320513038, 9050356671, 9050356669, 2111347918, 66611431, 66691893, 66746572, 1843788747, 66732034, 1669520735, 1669520769]}
        result_astar = astar(route.graph, route.source_node, route.destination_node)
        self.assertDictEqual(expected_result, result_astar)
    '''


if __name__ == '__main__':
    unittest.main()

