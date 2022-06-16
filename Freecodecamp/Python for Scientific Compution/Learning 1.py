""" This code was written to answer Free Code Camps 1st project in
Scientific Calculation with python: Arithmetic Formatter // 27/03/2022"""

def arithmetic_arranger(problems, calc=bool):
    # Checks if number of problems is OK
    if len(problems) > 5:
      return "Error: Too many problems."

    emp_list = []  # List of numbers
    op_list = []  # List of operators

    for x in problems:
        for tmp in x.split():
            if tmp.isdigit():
                if len(tmp) > 4: # error flag
                    return "Error: Numbers cannot be more than four digits."
                emp_list.append(tmp)
            if not tmp.isdigit():
                if tmp == "*" or tmp == "/" or tmp == "^":  # error flag
                    return "Error: Operator must be '+' or '-'."
                if not (tmp == "+" or tmp == "-"):  # error flag
                    return "Error: Numbers must only contain digits."
                op_list.append(tmp)  # if no error conserve operator

    chunks = [emp_list[x:x + 2] for x in range(0, len(emp_list), 2)]

    line1 = ""
    line2 = ""
    line3 = ""
    line4 = ""
    for couple in chunks:
        res = 0
        i = 0
        len_m = len(max(couple, key=len))
        len_min = len(min(couple, key=len))
        tmp2 = (len_m + 2) * "-"
        ending = tmp2
        line3 = line3 + ending + 4 * " "  # + len_m*" "
        rshift = 2 + len_m
        for tmp in couple:

            if len(couple[0]) <= len(couple[1]):  # top number is shorted than 2nd number
                if (i % 2) == 1:
                    index = chunks.index(couple)
                    num2 = op_list[index] + " " + tmp
                    num2 = num2.rjust(rshift, " ")

                else:
                    r_tmp = tmp.rjust(len_m + 2, " ")
                    num1 = r_tmp
                    num1 = num1.rjust(rshift, " ")

                i = i + 1
                tmp2 = (len_m + 1) * "-"
                ending = tmp2.rjust(len_m + 1, " ")

            else:  # top number is longer than 1st number
                if (i % 2) == 1:
                    index = chunks.index(couple)
                    num2 = op_list[index] + (len_m-len_min+1)*" " + tmp
                    num2 = num2.rjust(rshift, " ")

                    # print(num2)
                else:
                    r_tmp = tmp.rjust(2, " ")
                    num1 = r_tmp
                    num1 = num1.rjust(rshift, " ")

                i = i + 1

            if calc == True and (i % 2) == 1:
                index = chunks.index(couple)
                if op_list[index] == "-":
                    res = int(couple[0]) - int(couple[1])
                else:
                    res = int(couple[0]) + int(couple[1])
                res = str(res).rjust(rshift, " ")
                line4 = line4 + res + 4 * " "


        line1 = line1 + num1 + 4 * " "
        line2 = line2 + num2 + 4 * " "

    line1 = line1[:-4]
    line2 = line2[:-4]
    line3 = line3[:-4]
    if calc == True:
        line4 = line4[:-4]
        arranged_problems = (line1 + "\n" + line2 + "\n" + line3 + "\n" + line4)
    else:
        arranged_problems = (line1 + "\n" + line2 + "\n" + line3)
    return arranged_problems

