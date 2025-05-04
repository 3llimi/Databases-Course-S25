from pymongo import MongoClient
import csv

# Connect to the local MongoDB instance
client = MongoClient('mongodb://mongo:27017')
db = client['university_db']

pipeline = [
    {
        "$lookup": {
            "from": "prereq",
            "localField": "course_id",
            "foreignField": "course_id",
            "as": "prereqs"
        }
    },
    {
        "$match": {
            "prereqs": {"$ne": []}
        }
    },
    {
        "$lookup": {
            "from": "department",
            "localField": "dept_name",
            "foreignField": "dept_name",
            "as": "dept_info"
        }
    },
    {"$unwind": "$dept_info"},
    {
        "$lookup": {
            "from": "section",
            "let": {"course_id": "$course_id"},
            "pipeline": [
                {
                    "$match": {
                        "$expr": {"$eq": ["$course_id", "$$course_id"]},
                        "semester": "Spring",
                        "year": 2023
                    }
                },
                {
                    "$lookup": {
                        "from": "takes",
                        "let": {
                            "sec_course_id": "$course_id",
                            "sec_id": "$sec_id",
                            "semester": "$semester",
                            "year": "$year"
                        },
                        "pipeline": [
                            {
                                "$match": {
                                    "$expr": {
                                        "$and": [
                                            {"$eq": ["$course_id", "$$sec_course_id"]},
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
                    "$project": {
                        "enrollment_count": {"$size": "$enrollments"}
                    }
                }
            ],
            "as": "sections"
        }
    },
    {
        "$addFields": {
            "total_enrollment": {
                "$sum": "$sections.enrollment_count"
            }
        }
    },
    {
        "$addFields": {
            "prerequisites": {
                "$reduce": {
                    "input": "$prereqs.prereq_id",
                    "initialValue": "",
                    "in": {
                        "$cond": [
                            {"$eq": ["$$value", ""]},
                            "$$this",
                            {"$concat": ["$$value", ", ", "$$this"]}
                        ]
                    }
                }
            }
        }
    },
    {
        "$project": {
            "dept_name": 1,
            "course_id": 1,
            "title": 1,
            "prerequisites": 1,
            "total_enrollment": {"$ifNull": ["$total_enrollment", 0]},
            "_id": 0
        }
    },
    {
        "$sort": {
            "dept_name": 1,
            "course_id": 1
        }
    }
]

results = db.course.aggregate(pipeline)

with open("q3.csv", "w", newline='') as csvfile:
    fieldnames = ['dept_name', 'course_id', 'title', 'prerequisites', 'total_enrollment']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for result in results:
        writer.writerow(result)

print("CSV output generated as 'q3.csv'.")