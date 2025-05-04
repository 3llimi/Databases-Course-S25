        
from pymongo import MongoClient
from bson.objectid import ObjectId
import json


def insert_operation(collection):
    with open('single.json') as f:
        data1 = json.load(f)
    
    result1 = collection.insert_one(data1)
    print(f"Inserted single document with ID: {result1.inserted_id}")
    
    with open('multi.json') as f:
        data2 = json.load(f)
    
    result2 = collection.insert_many(data2)
    print(f"Inserted {len(result2.inserted_ids)} documents with IDs: {result2.inserted_ids}")
    
def find_operation(collection):
    query1 = {"couponUsed": True}
    results1 = collection.find(query1)
    print("\nDocuments where coupon was used:")
    for doc in results1:
        print(doc)
    
    query2 = {"storeLocation": "Denver"}
    results2 = collection.find(query2)
    print("\nDocuments with storeLocation in Denver:")
    for doc in results2:
        print(doc)
    
    query3 = {"customer.satisfaction": {"$lt": 4}}
    results3 = collection.find(query3)
    print("\nDocuments where customer satisfaction < 4:")
    for doc in results3:
        print(doc)
        
def delete_operation(collection):
    specific_id = "5bd761dcae323e45a93ccff4"
    try:
        result1 = collection.delete_one({"_id": ObjectId(specific_id)})
        print(f"\nDeleted {result1.deleted_count} document with ID {specific_id}")
    except:
        print(f"\nNo document found with ID {specific_id} (may not exist in this dataset)")
    
    result2 = collection.delete_many({"storeLocation": "Seattle"})
    print(f"Deleted {result2.deleted_count} documents with storeLocation Seattle")

def update_operation(collection):
    specific_id = "5bd761dcae323e45a93ccff3"
    try:
        result = collection.update_one(
            {"_id": ObjectId(specific_id)},
            {"$set": {"customer.satisfaction": 5}}
        )
        print(f"\nUpdated {result.modified_count} document's satisfaction (ID: {specific_id})")
    except:
        print(f"\nNo document found with ID {specific_id} (may not exist in this dataset)")

def main():
    client = MongoClient("mongodb://localhost:27017/")
    db = client['lab11']
    
    collection = db['supplies']
    
        
    print("=== Exercise 1: Insert Operations ===")
    insert_operation(collection)
    
    print("\n=== Exercise 2: Find Operations ===")
    find_operation(collection)
    
    print("\n=== Exercise 3: Delete Operations ===")
    delete_operation(collection)
    
    print("\n=== Exercise 4: Update Operation ===")
    update_operation(collection)

if __name__ == '__main__':
    main()