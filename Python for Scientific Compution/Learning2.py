""" This code was written to answer Free Code Camps 2nd project in
Scientific Calculation with python: Time Calculator // 29/03/2022"""

start = "11:55 AM"
end = "3:12"
date = 'wednesday'

def add_time(start, duration, Day = " "):
    def get_num(some_string):
        emp_list = []
        for tmp in some_string.split(':'):
            if tmp.isdigit():
                emp_list.append(tmp)
            if not tmp.isdigit():
                for tmp2 in tmp.split(' '):
                    if tmp2.isdigit():
                        emp_list.append(tmp2)
                    else:
                        emp_list.append(tmp2)


        return emp_list

    def day(multi_h):
        if multi_h == 1:
            disp_str = "(next day)"
        else:
            disp_str = "(" + str(multi_h) + " days later)"
        return disp_str

    start_nums = get_num(start)
    added_nums = get_num(duration)
    h_0 = int(start_nums[0])
    if start_nums[2] == "PM":
        h_0 = h_0+12

    m_0 = int(start_nums[1])
    h_1 = int(added_nums[0])
    m_1 = int(added_nums[1])

    # Get minutes and addes hours
    m_2 = m_0 + m_1
    multi_m = int(m_2 / 60)  # Number of hours added
    m_2 = str(m_2 % 60)  # Minutes
    if len(m_2) <= 1:
        m_2 = "0" + m_2

    h_2_h24 = h_0 + h_1 + multi_m

    multi_h = int(h_2_h24 / 24)  # Number of days added
    h_2_h24 = h_2_h24 % 24  # hours

    h_2 = h_2_h24 % 12
    if h_2 == 0:
        h_2 = 12
    if h_2_h24 >= 12:
        time = "PM"
    else:
        time = "AM"

    nb_days = day(multi_h)
    if nb_days =="(0 days later)":
        new_time = str(h_2) + ":" + m_2 + " " + time
    else:
        new_time = str(h_2) + ":" + m_2 + " " + time + " " + nb_days
    if Day != " ":
        Day = str(Day)
        week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        Day = Day.lower()
        i = week.index(Day)
        i = (i + multi_h) % 7
        Week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        Day = Week[i]
        if nb_days == "(0 days later)":
            new_time = str(h_2) + ":" + m_2 + " " + time + ", " + Day
        else:
            new_time = str(h_2) + ":" + m_2 + " " + time + ", " + Day + " " + nb_days


    return new_time

print(add_time(start, end))