class University:

    def __init__(self):
        self.applicants = []
        self.departments = "Biotech", "Chemistry", "Engineering", "Mathematics", "Physics"
        self.courses = "physics", "chemistry", "math", "computer science"
        self.departments_applicants = \
            {self.departments[0]: {"students": [], "score_col_index": (3, 2)},
             self.departments[1]: {"students": [], "score_col_index": (3,)},
             self.departments[2]: {"students": [], "score_col_index": (5, 4)},
             self.departments[3]: {"students": [], "score_col_index": (4,)},
             self.departments[4]: {"students": [], "score_col_index": (2, 4)}}
        self.max_students_per_department = None

    def load_applicants_from_file(self):
        with open("applicants.txt", "r") as file:
            for line in file.readlines():
                self.applicants.append(line.split())

    def get_applicants_by_departments(self, applicants, department, priority_col_index):
        return list(filter(lambda x: x[priority_col_index] == department, applicants))

    def calculate_best_scores(self, applicants, score_col_index):
        for applicant in applicants:
            scores = []
            if len(score_col_index) == 1:
                scores.append(float(applicant[score_col_index[0]]))
            else:
                scores.append((float(applicant[score_col_index[0]]) + float(applicant[score_col_index[1]])) / 2)
            scores.append(float(applicant[6]))
            applicant.insert(7, max(scores))

    def get_applicants_sorted_by_score(self, applicants):
        return sorted(applicants, key=lambda x: (-x[7], x[0], x[1]))

    def move_applicants_to_departments(self, priority_col_index):
        for department, values in self.departments_applicants.items():
            applicants = self.get_applicants_by_departments(self.applicants, department, priority_col_index)
            self.calculate_best_scores(applicants, values["score_col_index"])
            applicants = self.get_applicants_sorted_by_score(applicants)
            applicants = applicants[:self.max_students_per_department - len(values["students"])]
            self.departments_applicants[department]["students"].extend(applicants)
            for i in range(len(applicants)):
                self.applicants.remove((applicants[i]))

    def sort_applicants_departments_by_score(self):
        for department, values in self.departments_applicants.items():
            self.departments_applicants[department]["students"].sort(key=lambda x: (-x[7], x[0], x[1]))

    def write_accepted_applicants_to_file(self):
        for department, values in self.departments_applicants.items():
            with open(f"{department}.txt", "w") as file:
                for student in values["students"]:
                    file.write(f"{student[0]} {student[1]} {student[7]}\n")

    def start(self):
        self.max_students_per_department = int(input())
        self.load_applicants_from_file()
        for i in range(-3, 0):
            self.move_applicants_to_departments(i)
            self.sort_applicants_departments_by_score()
        self.write_accepted_applicants_to_file()


def main():
    university = University()
    university.start()


if __name__ == "__main__":
    main()
