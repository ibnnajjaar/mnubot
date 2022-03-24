from prettytable import PrettyTable, ALL


def create_subjects_prettytable(subjects):
    subject_table = PrettyTable()
    subject_table.hrules=ALL
    subject_table.field_names = ["Subjects"]
    for subject in subjects:
        subject_table.add_row([
            subject.name + "(" + subject.code + ")\n" +
            "by: " + subject.lecturer
        ])
    subject_table.align["Subjects"] = "l"
    return subject_table