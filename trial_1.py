from datetime import datetime
def get_date_from_week_no(week_no,weekday=6,month_no=0):

    min_day=7*(week_no-1)+1
    max_day=7*(week_no)+1

    for day in range(min_day,max_day):
        date_str=str(2018)+"-"+str(month_no)+"-"+str(day)
        date=datetime.strptime(date_str,"%Y-%m-%d")
        if date.weekday()==weekday:
            return date.date()
        else:
            continue




print(get_date_from_week_no(2,0,2))