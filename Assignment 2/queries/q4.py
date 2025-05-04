from pymongo import MongoClient
import csv

# Connect to the local MongoDB instance
client = MongoClient('mongodb://mongo:27017')
db = client['university_db']

course_stats = []
for course in db.course.find():
    sections = db.section.find({
        "course_id": course["course_id"],
        "semester": "Spring",
        "year": 2022
    })
    
    total_enrollment = 0
    count_a = 0
    
    for section in sections:
        takes = db.takes.find({
            "course_id": section["course_id"],
            "sec_id": section["sec_id"],
            "semester": section["semester"],
            "year": section["year"]
        })
        
        for take in takes:
            total_enrollment += 1
            if take.get("grade") == "A":
                count_a += 1
    
    if total_enrollment > 0:
        course_stats.append({
            "course_id": course["course_id"],
            "title": course["title"],
            "dept_name": course["dept_name"],
            "total_enrollment": total_enrollment,
            "count_a": count_a
        })

dept_rankings = {}
for dept in db.department.find():
    dept_courses = [cs for cs in course_stats if cs["dept_name"] == dept["dept_name"]]
    dept_courses_sorted = sorted(dept_courses, key=lambda x: x["total_enrollment"], reverse=True)
    
    for rank, course in enumerate(dept_courses_sorted, 1):
        course["dept_rank"] = rank

for course in course_stats:
    sections = db.section.find({
        "course_id": course["course_id"],
        "semester": "Spring",
        "year": 2022
    })
    
    instructor_enrollments = {}
    
    for section in sections:
        teaches = db.teaches.find_one({
            "course_id": section["course_id"],
            "sec_id": section["sec_id"],
            "semester": section["semester"],
            "year": section["year"]
        })
        
        if teaches:
            instructor_id = teaches["ID"]
            enrollment = db.takes.count_documents({
                "course_id": section["course_id"],
                "sec_id": section["sec_id"],
                "semester": section["semester"],
                "year": section["year"]
            })
            
            if instructor_id in instructor_enrollments:
                instructor_enrollments[instructor_id] += enrollment
            else:
                instructor_enrollments[instructor_id] = enrollment
    
    if instructor_enrollments:
        best_instructor = max(instructor_enrollments.items(), key=lambda x: x[1])
        course["instructor_id"] = best_instructor[0]
    else:
        course["instructor_id"] = None

final_results = sorted(
    course_stats,
    key=lambda x: (x["dept_name"], x["dept_rank"])
)

with open("q4.csv", "w", newline='') as csvfile:
    fieldnames = [
        'dept_name', 'course_id', 'title', 
        'total_enrollment', 'count_a', 
        'dept_rank', 'instructor_id'
    ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for result in final_results:
        writer.writerow({
            "dept_name": result["dept_name"],
            "course_id": result["course_id"],
            "title": result["title"],
            "total_enrollment": result["total_enrollment"],
            "count_a": result["count_a"],
            "dept_rank": result["dept_rank"],
            "instructor_id": result.get("instructor_id", "")
        })

print("CSV output generated as 'q4.csv'.")