import  pymongo

# create a mongo client
client = pymongo.MongoClient()
# create a database called e_vote
db =  client['e_vote']
# vores collection
voters_collection = db['voters']
# voters_collection.create_index([("idNumber", pymongo.ASCENDING)], unique=True)
# candidates collection
candidates_collection = db['candidates']
geo = db['geo']

places = [
        {'county': 'Mombasa', 'constituencies': ['Kisauni', 'Likoni', 'Kashani']},
        {'county': 'Nairobi', 'constituencies': ['Mwiki', 'CBD']}
        ]

voters = [
        {'idNumber': 1, 'serialNumber': 1, 'name': 'Brian Mokua', 'county': 'Mombasa', 'constituency': 'Kisauni'},
        {'idNumber': 2, 'serialNumber': 2, 'name': 'Johnstone Kahindi', 'county': 'Kilifi', 'constituency': 'Kilifi-poly'},
        {'idNumber': 3, 'serialNumber': 3, 'name': 'Sylvetser Onyango', 'county': 'Kajiado', 'constituency': 'Kiserian'}
]
candidates = [
    {'position': 'president', 'name': 'Raila Odinga', 'party': 'ODM'},
    {'position': 'president', 'name': 'Uhuru Kenyatta', 'party': 'Jubilee'},
    {'position': 'president', 'name': 'Kalonzo Musyoka', 'party': 'Wiper'},
    {'position': 'president', 'name': 'Brian Oyaro', 'party': 'gen-Z'},

    {'position': 'governor', 'name': 'Bosobori Onyancha', 'party': 'ODM', 'county': 'Mombasa'},
    {'position': 'governor', 'name': 'Kim Wanjala', 'party': 'Jubilee', 'county': 'Mombasa'},
    {'position': 'governor', 'name': 'Sharon Mwai', 'party': 'wiper', 'county': 'Mombasa'},

    {'position': 'MP', 'name': 'Samuel Mrefu', 'party': 'gen-Z', 'constituency': 'Kisauni'},
    {'position': 'MP', 'name': 'Belinda Atieno', 'party': 'ODM', 'constituency': 'Kisauni'}
]
# places storage
geo.delete_many({})
for place in places:
    geo.insert_one(place)
# voter storage
voters_collection.delete_many({})
for voter in voters:
    voters_collection.insert_one(voter)
# candidates storage
candidates_collection.delete_many({})
for candidate in candidates:
    candidates_collection.insert_one(candidate)

# user = voters_collection.find_one({'idNumber': 1, 'serialNumber': 1})
# print(voters_collection.index_information())
# voters_collection.update_one({'idNumber': 1}, {'$set': {'updatedCounty': 'London'}})
# print(voters_collection.find_one({'idNumber': 1}).get('updatedCounty'))
# presidents = [x for x in candidates_collection.find({'position': 'president'}, {'_id': 0, 'position': 0, 'party': 0})]
# print(presidents)
# print({'name': 'Raila Odinga'} in presidents)
