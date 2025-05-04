
CREATE TABLE Projects (
    ProjectCode VARCHAR(10) PRIMARY KEY,
    ProjectName VARCHAR(50),
    ProjectManager VARCHAR(50),
    ProjectBudget INT
);

CREATE TABLE Employees (
    EmployeeNo INT PRIMARY KEY,
    EmployeeName VARCHAR(50),
    DepartmentNo VARCHAR(10),
    DepartmentName VARCHAR(50),
    HourlyRate DECIMAL(5,2)
);

CREATE TABLE ProjectEmployees (
    ProjectCode VARCHAR(10),
    EmployeeNo INT,
    PRIMARY KEY (ProjectCode, EmployeeNo),
    FOREIGN KEY (ProjectCode) REFERENCES Projects(ProjectCode),
    FOREIGN KEY (EmployeeNo) REFERENCES Employees(EmployeeNo)
);

INSERT INTO Projects VALUES
('PC010', 'Reservation System', 'Mr. Ajay', 120500),
('PC011', 'HR System', 'Mrs. Charu', 500500),
('PC012', 'Attendance System', 'Mr. Rajesh', 710700);

INSERT INTO Employees VALUES
(100, 'Mohan', 'D03', 'Database', 21.00),
(101, 'Vipul', 'D02', 'Testing', 16.50),
(102, 'Riyaz', 'D01', 'IT', 22.00),
(105, 'Pavel', 'D03', 'Database', 18.50),
(103, 'Jack', 'D02', 'Testing', 17.00),
(104, 'James', 'D01', 'IT', 23.50),
(315, 'Raul', 'D03', 'Database', 21.50),
(218, 'Alex', 'D02', 'Testing', 15.50),
(109, 'Victor', 'D01', 'IT', 20.50);

INSERT INTO ProjectEmployees VALUES
('PC010', 100),
('PC010', 101),
('PC010', 102),
('PC011', 105),
('PC011', 103),
('PC011', 104),
('PC012', 315),
('PC012', 218),
('PC012', 109);