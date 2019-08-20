import pandas as pd
import os
from datetime import date

def make_table(exercise, num_sets, num_reps, weight, data=None,
               date=date.today().strftime('%m-%d-%y')):
    '''
    Function to input workout data and output results in pandas DataFrame.
    ------------------
    exercise : string : name of exercise
    num_sets : integer: number of sets
    num_reps : integer: number of reps in each set
    weight   : integer: weight of lift
    
    data (optional) : pandas DataFrame : use current DataFrame to add on to
    fail (optional) : boolean : use =True if fail on any set
    data (optional) : string: uses curernt date in format ` '08-14-19' `
    ------------------
    If fail=True, you will be asked to input more data, starting with the set you failed on.
    '''
    df = pd.DataFrame()
    df = df.append([[date, exercise,num_sets,num_reps,weight]])
    df.columns = ['date', 'exercise','num_sets','num_reps','weight']

    try:
        if len(data) != 0:
            data = data.append(df)
            return data.reset_index().drop(['index'],axis=1)
    except TypeError:
        pass
    
    return df.reset_index().drop(['index'],axis=1)

def populate_table(day_of_week, skip_all=True, exercises_skipped=None, exercises_added=None, 
                   date=date.today().strftime('%m-%d-%y')):
    '''
    Function used to help automate the make_table function.
    
    -----------
    Parameters
    -----------
    
    day_of_week : string : Pass in 'c' for chest day (or 'c2'), 'b' for back day, or 'l' for leg day
    exercises_skipped : list : Pass in a list of all exercises you skipped. You MUST use form as denoted below:
    exercises_added : list : Pass in a list of all exercises added
    skip_all : bool : Set to False to use default exercises. Use in conjunction with exercises_added
        for a custom list
    date : string : Date of exercise. Default is today's date in format '08-16-19'.
        
    **Example** exercises_skipped = ['Bench', 'Overhead Press']
                exercises_added = ['Decline Bench','Facepulls']
                
    **Usage Example**
    populate_table('b',skip_all=True,exercises_added=['Row','Facepulls'])
    
    This creates a table with only Rows and Facepulls as the exercises.
        
    Names of Exercises you can skip: (there are more for day 2 variants)
    
    Chest day:
        ['Bench','Overhead Press','Dips','Incline DB Press','Cable Raise(side)','Overhead Tricep Extension','Cable Fly(across)','Front Raise']
    
    Chest day 2:
        ['Bench','Overhead Press','Dips','Incline DB Press','Cable Raise(front)','Tricep Pulldown','Cable Fly(down)','Front Raise']
    
    Back day:
        ['Pullup','Deadlift','Seated Curl','Rows','Lat Fly','Hammer Curl','Lat Pulldown']
   
    Leg day:
        ['Squat, Seated Calf Raise','Leg Curl','Standing Calf Raise','Leg Press','Forearm','Trap']
    '''
    day_of_week = day_of_week.lower() 

    if day_of_week=='c':
        exercises_list = ['Bench','Overhead Press','Dips','Incline DB Press','Cable Raise(side)','Overhead Tricep Extension','Cable Fly(across)','Front Raise']
    elif day_of_week=='b':
        exercises_list = ['Pullup','Deadlift','Seated Curl','Rows','Lat Fly','Hammer Curl','Lat Pulldown']
    elif day_of_week=='l':
        exercises_list = ['Squat, Seated Calf Raise','Leg Curl','Standing Calf Raise','Leg Press','Forearm','Trap']
    elif day_of_week=='c2':
        exercises_list = ['Bench','Overhead Press','Dips','Incline DB Press','Cable Raise(front)','Tricep Pulldown','Cable Fly(down)','Front Raise']
    else:
        return 'Invalid Day. Choose from C, C2, B, or L.'
    
    skiplist = []
    if exercises_skipped:
        for name_skip in exercises_skipped:
            skiplist.append(name_skip)
    
    new_ex_list = []
    for e in exercises_list:
        if e not in tuple(skiplist):
            new_ex_list.append(e)
    exercises_list = new_ex_list
    
    if skip_all: exercises_list = []
    
    if exercises_added:
        for item in exercises_added:
            exercises_list.append(item)
        
    counter = 0
    for exercise in exercises_list:
        print(f'Exercise: {exercise}')
        set_num = int(input('Number of Sets?'))
        num_reps = int(input('Number of Reps?'))
        weight = int(input('Weight?'))
        if counter == 0:
            table = make_table(exercise,set_num,num_reps,weight,date=date)
        else:
            table = make_table(exercise,set_num,num_reps,weight,data=table,date=date)
        counter+=1
        
    return table


def make_file(df, name_of_file='Lift Numbers.csv'):
    with open(name_of_file, 'a', newline='') as file:

        #if file is empty, add header. else, don't
        if os.path.getsize(name_of_file) == 0:
            file.write(df.to_csv(index=False, header=True))
        else:
            file.write(df.to_csv(index=False, header=False))
