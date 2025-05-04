from pymongo import MongoClient
import csv

# Connect to the local MongoDB instance
client = MongoClient('mongodb://mongo:27017')
db = client['university_db']

pipeline = [
    {
        "$match": {
            "semester": "Summer",
            "year": 2023
        }
    },
    {
        "$lookup": {
            "from": "teaches",
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
            "as": "teaching_info"
        }
    },
    {"$unwind": "$teaching_info"},
    {
        "$lookup": {
            "from": "instructor",
            "localField": "teaching_info.ID",
            "foreignField": "ID",
            "as": "instructor_info"
        }
    },
    {"$unwind": "$instructor_info"},
    {
        "$match": {
            "instructor_info.dept_name": "Biology"
        }
    },
    {
        "$lookup": {
            "from": "course",
            "localField": "course_id",
            "foreignField": "course_id",
            "as": "course_info"
        }
    },
    {"$unwind": "$course_info"},
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
                },
                {
                    "$group": {
                        "_id": None,
                        "enroll_count": {"$sum": 1}
                    }
                }
            ],
            "as": "enrollment_stats"
        }
    },
    {"$unwind": "$enrollment_stats"},
    {
        "$group": {
            "_id": "$instructor_info.ID",
            "name": {"$first": "$instructor_info.name"},
            "dept_name": {"$first": "$instructor_info.dept_name"},
            "total_credits_taught": {
                "$sum": {
                    "$multiply": ["$course_info.credits", "$enrollment_stats.enroll_count"]
                }
            },
            "total_enrollments": {"$sum": "$enrollment_stats.enroll_count"}
        }
    },
    {
        "$sort": {"total_credits_taught": -1}
    },
    {
        "$limit": 3
    },
    {
        "$project": {
            "id": "$_id",
            "name": 1,
            "dept_name": 1,
            "total_credits_taught": 1,
            "total_enrollments": 1,
            "_id": 0
        }
    }
]

results = db.section.aggregate(pipeline)

with open("q2.csv", "w", newline='') as csvfile:
    fieldnames = ['id', 'name', 'dept_name', 'total_credits_taught', 'total_enrollments']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for result in results:
        writer.writerow(result)

print("CSV output generated as 'q2.csv'.")