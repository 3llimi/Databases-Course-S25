CREATE TABLE ProjectEmployees (
    ProjectCode VARCHAR(10),
    ProjectName VARCHAR(50),
    ProjectManager VARCHAR(50),
    ProjectBudget INT,
    EmployeeNo INT,
    EmployeeName VARCHAR(50),
    DepartmentNo VARCHAR(10),
    DepartmentName VARCHAR(50),
    HourlyRate DECIMAL(5,2),
    PRIMARY KEY (ProjectCode, EmployeeNo) -- To Ensure uniqueness and atomicity
);

INSERT INTO ProjectEmployees VALUES
('PC010', 'Reservation System', 'Mr. Ajay', 120500, 100, 'Mohan', 'D03', 'Database', 21.00),
('PC010', 'Reservation System', 'Mr. Ajay', 120500, 101, 'Vipul', 'D02', 'Testing', 16.50),
('PC010', 'Reservation System', 'Mr. Ajay', 120500, 102, 'Riyaz', 'D01', 'IT', 22.00),
('PC011', 'HR System', 'Mrs. Charu', 500500, 105, 'Pavel', 'D03', 'Database', 18.50),
('PC011', 'HR System', 'Mrs. Charu', 500500, 103, 'Jack', 'D02', 'Testing', 17.00),
('PC011', 'HR System', 'Mrs. Charu', 500500, 104, 'James', 'D01', 'IT', 23.50),
('PC012', 'Attendance System', 'Mr. Rajesh', 710700, 315, 'Raul', 'D03', 'Database', 21.50),
('PC012', 'Attendance System', 'Mr. Rajesh', 710700, 218, 'Alex', 'D02', 'Testing', 15.50),
('PC012', 'Attendance System', 'Mr. Rajesh', 710700, 109, 'Victor', 'D01', 'IT', 20.50);