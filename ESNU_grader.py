import math

# static vars for grading scheme
# grades are defined as integers that increment by thirds of letter grades
# AKA the indices in the following list:
letter_grades = ['F', 'D', 'D+', 'C-', 'C', 'C+', 'B-', 'B', 'B+', 'A-', 'A']

# Can edit weighting scheme for exams
midterm_weight = 0.4
final_exam_weight = 0.6

# Given the number of tasks completed, returns the task adjustment score
def get_task_adj(tasks_completed):
    return -1 if (tasks_completed < 3) else 0

# Given midterm and final scores as integers out of 100 points, returns
# a pair of the exam adjustment score and a "Max D+" bool 
def get_exam_adj(midterm, final_exam):
    max_dplus = False
    adj = 0
    weighted_score = math.ceil((midterm_weight * midterm) + (final_exam_weight * final_exam))
    if weighted_score < 35:
        max_dplus = True
    elif weighted_score <= 49:
        adj = -2
    elif weighted_score <= 64:
        adj = -1
    elif weighted_score <= 74:
        adj = 0
    elif weighted_score <= 89:
        adj = 1
    else:
        adj = 2
    return (adj, max_dplus)


# Given proof and non_proof scores [#E, #S, #N, #U], returns a pair of the
# pset adjustment score and a "Max D+" bool
def get_pset_adj(proofs, non_proofs):
    E_proofs = proofs[0]
    SE_non_proofs = non_proofs[0] + non_proofs[1]
    U_all = proofs[3] + non_proofs[3]
    adj = 0
    max_dplus = False

    # Es on proofs
    if E_proofs >= 4:
        if E_proofs <= 7:
            adj += 1
        elif E_proofs <= 11:
            adj += 2
        else:
            adj += 3
    
    # Ss and Es on non-proofs 
    if SE_non_proofs < 6:
        adj -= 1
    elif SE_non_proofs >= 10:
        adj += 1

    # Us on any problems in the psets
    if U_all >= 4:
        if U_all <= 6:
            adj -= 1
        elif U_all <= 9:
            adj -= 2
        else:
            max_dplus = True

    return (adj, max_dplus)

# Takes proof scores [#E, #S, #N, #U], and returns a pair of the baseline grade and 
# a "Max D+" bool
def get_baseline_grade(proofs):
    SE_proofs = proofs[0] + proofs[1]
    baseline = 0
    max_dplus = False
    if SE_proofs < 6:
        baseline = 2   # max D+
        max_dplus = True
    elif SE_proofs <= 7:
        baseline = 2    # normal D+
    elif SE_proofs <= 9:
        baseline = 3    # C-
    elif SE_proofs <= 11:
        baseline = 4    # C
    elif SE_proofs <= 13:
        baseline = 5    # C+
    elif SE_proofs <= 15:
        baseline = 6    # B-
    else:
        baseline = 7    # B
    return (baseline, max_dplus)

# Takes ESNU values as input:  
# proofs [#E, #S, #N, #U], non_proofs [#E, #S, #N, #U],
# midterm (X points / 100), final_exam (X points / 100), #tasks_completed
# Outputs final grade according to syllabus for CMSC 28400, Fall 2022
def get_ESNUgrade(proofs, non_proofs, midterm, final_exam, tasks_completed):
    baseline = get_baseline_grade(proofs)
    pset_adj = get_pset_adj(proofs, non_proofs)
    exam_adj = get_exam_adj(midterm, final_exam)
    task_adj = get_task_adj(tasks_completed)    # No "Max D+" flag here
    
    total_adj = pset_adj[0] + exam_adj[0] + task_adj

    # if "Max D+" is ever true, then set baseline to D+ and only count negative adjustments
    corrected_baseline = baseline[0]
    if baseline[1] or pset_adj[1] or exam_adj[1]:
        corrected_baseline = 2
        total_adj = min(total_adj, 0)

    # Calculate final grade
    grade = corrected_baseline + total_adj 
    grade = max(grade, 0) # Can't get worse than an F
    grade = min(grade, len(letter_grades) - 1) # Can't do better than A (at UChicago)

    return letter_grades[grade]

def main():
    print("Welcome to the ESNU grader for CMSC 28400.")
    loop_inp = ''
    score_inp = ''
    loop_inp = input("Enter 'q' to quit, 'i' for input formatting information, or any other character to proceed:\n")
    while loop_inp != 'q':
        if loop_inp == 'i':
            print("\nINPUT FORMATTING INFORMATION")
            print("--------------------------------------------------------------------------------")
            print("The scoring information of a single student should be entered in this format: ")
            print("Scores on proof problems on psets: #Ep, #Sp, #Np, #Up (as comma-separated ints)")
            print("Scores on non_proof problems on psets: #Enp, #Snp, #Nnp, #Unp (as comma-separated ints)")
            print("Midterm and final exam scores: X / 100 (as an int score out of 100)")
            print("Tasks completed: # of tasks completed (as an int)")
            print("\nThe above values should be comma-separated, with no whitespace, and inputted in one line:")
            print("#Ep,#Sp,#Np,#Up,#Enp,#Snp,#Nnp,#Unp,midterm,final,tasks\n")
        else:
            score_inp = input("Enter the scoring information for a single student (or 'q' to skip):\n")
            all_int_inp = True
            grade = ''
            score_info = []
            if score_inp != 'q':
                score_info = score_inp.split(',')
                if len(score_info) != 11:
                    print("Improper number of values in input.")
                else:
                    for i, x in enumerate(score_info):
                        try:
                            x = x.strip()
                            if (x.isdigit()):
                                score_info[i] = int(x)
                            else:
                                raise ValueError
                        except ValueError as ex:
                            print("One inputted value was not an integer value, make sure all inputted characters are digits or commas.")
                            all_int_inp = False
                            break
                    if all_int_inp:
                        grade = get_ESNUgrade(score_info[0:4], score_info[4:8], score_info[8], score_info[9], score_info[10])
                        print("\nThis student's grade is:", grade)

        loop_inp = input("\nEnter 'q' to quit, 'i' for input formatting information, or any other character to proceed:\n")
    return 0

if __name__ == "__main__":
    main()
