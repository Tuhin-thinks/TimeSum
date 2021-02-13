## What is the use of SumTime?

- Adds time strings
- can convert/add time strings from a wide variety of input options
- Flexible time additions and assignment
- Convert to datetime.timedelta object
- A handy tool for quick time calculations!

## Import class from file


```python
from ArithTime import SumTime as st
```

## declare SumTime object


```python
# declaring st("1hrs 20mins") is equivalent to st("1 20")
s1 = st("1hrs 20mins")

s_blank = st()
s_blank_2 = st('')

print(s_blank.get_hrs(), s_blank.get_minutes(), s_blank.get_secs(), "s_blank =>", s_blank)
print(s_blank_2.get_hrs(), s_blank_2.get_minutes(), s_blank_2.get_secs(), "s_blank_2 =>",s_blank_2)
```

    0 0 0 s_blank => 
    0 0 0 s_blank_2 => 


<h2> Addition with valid time strings </h2>

    [time_value][flag]<separator>[time_value][flag]
    
    - time_value = \d or any Integer
    - flag = hrs | mins | secs
    - <separator> = not compulsory, can be any character.


```python
# perform addition of time strings
s1 = st("1 00")
print(s1)
s1 += ["20mins" ,"1hrs 10mins" , "50mins"] + ["10mins" , "0hrs-60secs" , "10mins"]
print(s1)

s_mins = st("1hrs 10mins")
print(s_mins, 'repr=>',repr(s_mins))
```

    1hrs
    3hrs 41mins
    1hrs 10mins repr=> SumTime('1 10 0')


## convert to datetime.timedelta object


```python
td = s1.to_timedelta()
print(type(td))
print(td.seconds)
```

    <class 'datetime.timedelta'>
    13260


## Addition on SumTime object

__Other than adding 2 SumTime objects
adding strings with SumTime object is also possible (as shown above)__

## Possible operations all together!


```python
s2 = st("0 59")  # 0hrs 59 minutes (read definition in init to know more possible input types)

# perform SumTime object addition
print(f"s1={s1}")
s3 = s1 + s2
print(f"s3={s3}\n")

# get individual time flags
print(16*'---')
print("Printing hrs, mins, secs individually:")
print(s3.get_hrs(), 'hrs')
print(s3.get_minutes(), 'mins')
print(s3.get_secs(), 'secs')

# print SumTime object
print("s3 as a whole =>",s3)
print(16*'---')


#store in string format
s3_str_fmt = str(s3)
print("store in string format:", type(s3_str_fmt), s3_str_fmt,'\n\n')

# format conversions
sum_time_obj = st.to_sumtime(str(s3), return_type='obj')  # return as SumTime object
time_list = st.to_sumtime(str(s3), return_type='list')  # return list[hrs, mins, secs]
time_string = st.to_sumtime(str(s3), return_type='str')  # return as str format, (this can be use to create a new instance of class)

print(f"object:{sum_time_obj}\nlist_return:{time_list}\nstring_return:{time_string}\n{16*'---'}")

new_inst = st(time_string)
print("New instance:",repr(new_inst))

print("SumTime object:", type(sum_time_obj), sum_time_obj)
```

    s1=3hrs 41mins
    s3=4hrs 40mins
    
    ------------------------------------------------
    Printing hrs, mins, secs individually:
    4 hrs
    40 mins
    0 secs
    s3 as a whole => 4hrs 40mins
    ------------------------------------------------
    store in string format: <class 'str'> 4hrs 40mins 
    
    
    object:4hrs 40mins
    list_return:[4, 40, None]
    string_return:4 40 0
    ------------------------------------------------
    New instance: SumTime('4 40 0')
    SumTime object: <class 'ArithTime.SumTime'> 4hrs 40mins

