from pymongo import MongoClient
import csv

# Connect to the local MongoDB instance
client = MongoClient('mongodb://mongo:27017')
db = client['university_db']

pipeline = [
    {
        "$match": {
            "semester": "Fall",
            "year": 2022
        }
    },
    {
        "$lookup": {
            "from": "takes",
            "let": {
                "course_id": "$course_id",
                "sec_id": "$sec_id",
                "semester": "$semester",
                "year": "$year"
            },
            "pipeline": [
                {
                    "$match": {
                        "$expr": {
                            "$and": [
                                {"$eq": ["$course_id", "$$course_id"]},
                                {"$eq": ["$sec_id", "$$sec_id"]},
                                {"$eq": ["$semester", "$$semester"]},
                                {"$eq": ["$year", "$$year"]}
                            ]
                        }
                    }
                }
            ],
            "as": "enrollments"
        }
    },
    {
        "$unwind": "$enrollments"
    },
    {
        "$lookup": {
            "from": "course",
            "localField": "course_id",
            "foreignField": "course_id",
            "as": "course_info"
        }
    },
    {
        "$unwind": "$course_info"
    },
    {
        "$group": {
            "_id": "$course_info.dept_name",
            "total_enrolled_credits": {"$sum": "$course_info.credits"}
        }
    },
    {
        "$project": {
            "dept_name": "$_id",
            "total_enrolled_credits": 1,
            "_id": 0
        }
    },
    {
        "$sort": {"dept_name": 1}
    }
]

results = db.section.aggregate(pipeline)

with open("q1.csv", "w", newline='') as csvfile:
    fieldnames = ['dept_name', 'total_enrolled_credits']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for result in results:
        writer.writerow(result)

print("CSV output generated as 'q1.csv'.")