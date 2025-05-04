from pymongo import MongoClient
import csv

# Connect to the local MongoDB instance
client = MongoClient('mongodb://mongo:27017')
db = client['university_db']

GRADE_POINTS = {
    'A': 4.0,
    'A-': 3.7,
    'B+': 3.3,
    'B': 3.0,
    'B-': 2.7,
    'C+': 2.3,
    'C': 2.0,
    'C-': 1.7,
    'D+': 1.3,
    'D': 1.0,
    'F': 0.0
}

def calculate_grade_value(grade):
    return GRADE_POINTS.get(grade, None)

section_grades = []
for section in db.section.find({"semester": "Spring", "year": 2022}):
    takes = db.takes.find({
        "course_id": section["course_id"],
        "sec_id": section["sec_id"],
        "semester": section["semester"],
        "year": section["year"]
    })
    
    for take in takes:
        section_grades.append({
            "course_id": section["course_id"],
            "sec_id": section["sec_id"],
            "student_id": take["ID"],
            "grade": take.get("grade"),
            "grade_value": calculate_grade_value(take.get("grade"))
        })

course_summaries = {}
for record in section_grades:
    course_id = record["course_id"]
    if course_id not in course_summaries:
        course_summaries[course_id] = {
            "total_enrollment": 0,
            "sum_grade_values": 0,
            "count_grades": 0,
            "count_a": 0,
            "count_b": 0,
            "count_c": 0
        }
    
    stats = course_summaries[course_id]
    stats["total_enrollment"] += 1
    
    if record["grade_value"] is not None:
        stats["sum_grade_values"] += record["grade_value"]
        stats["count_grades"] += 1
    
    if record["grade"] == 'A':
        stats["count_a"] += 1
    elif record["grade"] == 'B':
        stats["count_b"] += 1
    elif record["grade"] == 'C':
        stats["count_c"] += 1

course_summaries = {k: v for k, v in course_summaries.items() if v["total_enrollment"] >= 2}

for course_id, stats in course_summaries.items():
    stats["avg_grade"] = stats["sum_grade_values"] / stats["count_grades"] if stats["count_grades"] > 0 else None

instructor_stats = {}
for section in db.section.find({"semester": "Spring", "year": 2022}):
    teaches = db.teaches.find_one({
        "course_id": section["course_id"],
        "sec_id": section["sec_id"],
        "semester": section["semester"],
        "year": section["year"]
    })
    
    if not teaches:
        continue
    
    instructor_id = teaches["ID"]
    enrollment = db.takes.count_documents({
        "course_id": section["course_id"],
        "sec_id": section["sec_id"],
        "semester": section["semester"],
        "year": section["year"]
    })
    
    if section["course_id"] not in instructor_stats:
        instructor_stats[section["course_id"]] = {}
    
    if instructor_id in instructor_stats[section["course_id"]]:
        instructor_stats[section["course_id"]][instructor_id] += enrollment
    else:
        instructor_stats[section["course_id"]][instructor_id] = enrollment

best_instructors = {}
for course_id, instructors in instructor_stats.items():
    if instructors:
        best_instructor = max(instructors.items(), key=lambda x: x[1])
        best_instructors[course_id] = {
            "instructor_id": best_instructor[0],
            "instructor_enrollment": best_instructor[1]
        }

results = []
for course_id, stats in course_summaries.items():
    course = db.course.find_one({"course_id": course_id})
    if not course:
        continue
    
    dept = db.department.find_one({"dept_name": course["dept_name"]})
    if not dept:
        continue
    
    results.append({
        "course_id": course_id,
        "title": course["title"],
        "dept_name": course["dept_name"],
        "total_enrollment": stats["total_enrollment"],
        "avg_grade": round(stats["avg_grade"], 2) if stats["avg_grade"] is not None else None,
        "count_a": stats["count_a"],
        "count_b": stats["count_b"],
        "count_c": stats["count_c"],
        "best_instructor_id": best_instructors.get(course_id, {}).get("instructor_id"),
        "best_instructor_enrollment": best_instructors.get(course_id, {}).get("instructor_enrollment", 0)
    })

dept_rankings = {}
for dept in db.department.find():
    dept_courses = [r for r in results if r["dept_name"] == dept["dept_name"]]
    dept_courses_sorted = sorted(dept_courses, key=lambda x: x["avg_grade"] or 0, reverse=True)
    
    for rank, course in enumerate(dept_courses_sorted, 1):
        course["dept_course_rank"] = rank

final_results = sorted(
    results,
    key=lambda x: (x["dept_name"], x["dept_course_rank"])
)

with open("q5.csv", "w", newline='') as csvfile:
    fieldnames = [
        'dept_name', 'course_id', 'title', 'total_enrollment', 'avg_grade',
        'count_a', 'count_b', 'count_c', 'best_instructor_id',
        'best_instructor_enrollment', 'dept_course_rank'
    ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for result in final_results:
        writer.writerow(result)

print("CSV output generated as 'q5.csv'.")