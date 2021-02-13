from datetime import timedelta
import re


class InvalidDataType(Exception):
    pass


class InvalidArgument(Exception):
    pass


class SumTime:
    def __init__(self, time_string: [str, None] = None):
        """:param time_string(:type: str, None,)
                            Desired input type:
                                --> 00 00 00 interpreted as 0 hrs 0 Minutes 0 seconds\n
                                --> 00 00 interpreted as 0 minutes 0 seconds
        """
        if not time_string:
            time_string = ""

        temp = self.to_sumtime(time_string, suppress=True,
                               return_type='str')  # match with regex to see if entered time_string is flagged or not
        if temp:
            self.time_string = temp
        else:
            self.time_string = time_string

        self.hrs, self.mins, self.secs = self.get_hrs(), self.get_minutes(), self.get_secs()
        self.getters = [self.get_hrs, self.get_minutes, self.get_secs]

    @staticmethod
    def to_sumtime(time_string: str, suppress: bool = False, return_type='obj') -> [None, 'SumTime']:
        """
                :param return_type: specifies the return type for the function, obj --> class instance
                                                                                list --> :type: List
                                                                                str --> :type: str
                :param time_string 	Allowed 00hrs<separator>00mins<separator>00secs
                                    example: 01hrs 20mins 00secs, 1hrs 10mins, 21mins, 10secs, 21hrs
                                    All examples mentioned above are valid time strings

                :param suppress pass True to stop printing if mismatched"""

        args_pattern = r"(?P<value>\d+)(?P<flag>hrs|mins|secs)"
        args_regex = re.compile(args_pattern)

        def time_string_to_dict():
            """
            utility function to convert string to dictionary of specific time-flags
            :return:
            """
            d = dict()
            match_list = re.findall(args_regex, time_string)
            for match in match_list:
                flag, value = match[1], match[0]
                d.update({flag: int(value)})
            return d

        match_dict = time_string_to_dict()
        if match_dict:
            hrs, mins, secs = match_dict.get('hrs'), match_dict.get('mins'), match_dict.get('secs')
            if return_type == 'obj':
                s_temp = SumTime(f"{(0 if not hrs else hrs)} {(0 if not mins else mins)} {(0 if not secs else secs)}")
                return s_temp
            elif return_type == 'str':
                return f"{(0 if not hrs else hrs)} {(0 if not mins else mins)} {(0 if not secs else secs)}"
            elif return_type == 'list':
                return [hrs, mins, secs]
            else:
                raise InvalidArgument("possible return_type (:type: str)--> [str, list, obj]")
        else:
            if not suppress:
                print(f"{time_string} isn't valid, allowed formats are:\n"
                      f"00hrs<separator>00mins<separator>00secs\n"
                      f"Examples: 01hrs 20mins 00secs, 1hrs 10mins, 21mins, 10secs, 21hrs\n"
                      f"Note: In place of separators you can use any non-alphabetic character.")
            return None

    def get_hrs(self) -> int:
        if len(self.time_string.split(' ')) == 2:
            return int(self.time_string.split(' ')[-2])
        elif len(self.time_string.split(' ')) == 3:
            return int(self.time_string.split(' ')[-3])
        else:
            return 0

    def get_minutes(self) -> int:
        if len(self.time_string.split(' ')) == 2:
            return int(self.time_string.split(' ')[-1])
        elif len(self.time_string.split(' ')) == 3:
            return int(self.time_string.split(' ')[-2])
        else:
            return 0

    def get_secs(self) -> int:
        if len(self.time_string.split(' ')) == 2:
            return 0
        elif len(self.time_string.split(' ')) == 3:
            return int(self.time_string.split(' ')[-1])
        else:
            return 0

    def to_timedelta(self) -> 'timedelta':
        """":param
        :return datetime.timedelta object for current hrs, mins, secs"""

        td_obj = timedelta(hours=self.hrs, minutes=self.mins, seconds=self.secs)
        return td_obj

    def __str__(self):
        hr_str = str(self.hrs) + 'hrs' if self.hrs else ''
        min_str = str(self.mins) + 'mins' if self.mins else ''
        secs_str = str(self.secs) + 'secs' if self.secs else ''
        return ' '.join([_ for _ in [hr_str, min_str, secs_str] if _])

    def __repr__(self):
        return f"{__class__.__name__}('{self.hrs} {self.mins} {self.secs}')"

    def __add__(self, other):
        """
        time calculation (addition of hrs mins secs) a + b
        :param other:
        :return:
        """
        if isinstance(self, type(other)):
            tot_hrs, tot_min, tot_secs = self.add_time(self, other)
            return SumTime(f"{tot_hrs} {tot_min} {tot_secs}")

        elif type(other) == str:
            other_obj = self.to_sumtime(other, suppress=True)
            if other_obj:
                s_temp = other_obj
            else:
                s_temp = SumTime(other)
            tot_hrs, tot_min, tot_secs = self.add_time(self, s_temp)
            return SumTime(f"{tot_hrs} {tot_min} {tot_secs}")
        if type(other) == list:
            s_temp = SumTime(self.to_sumtime(str(self), suppress=True, return_type="str"))
            for i in other:
                if type(i) == str:
                    temp_obj = SumTime(i)
                elif type(i) == SumTime:
                    temp_obj = i
                else:
                    raise InvalidDataType(f"Addition between SumTime and {type(i)} is not supported.")
                s_temp.hrs, s_temp.mins, s_temp.secs = self.add_time(s_temp, temp_obj)
            return s_temp
        else:
            raise InvalidDataType(f"{other} doesn't match class instance")

    def __radd__(self, other):
        """
        addition of time, a += b
        :param other:
        :return:
        """
        time_obj = self.__add__(other)
        return time_obj  # return new class instance

    def __iadd__(self, other):
        time_sum = self
        if type(other) == list:
            for i in other:
                if type(i) == str:
                    temp_obj = SumTime(i)
                elif type(i) == SumTime:
                    temp_obj = i
                else:
                    raise InvalidDataType(f"Addition between SumTime and {type(i)} is not supported.")
                time_sum.hrs, time_sum.mins, time_sum.secs = self.add_time(time_sum, temp_obj)
        elif type(other) == str:
            time_sum.hrs, time_sum.mins, time_sum.secs = self.add_time(time_sum, self.to_sumtime(other, suppress=True,
                                                                                                 return_type='obj'))

        elif type(other) == SumTime:
            time_sum.hrs, time_sum.mins, time_sum.secs = self.add_time(time_sum, other)

        return time_sum

    @staticmethod
    def add_time(obj1, obj2):
        hrs = obj1.hrs + obj2.hrs

        mins = obj1.mins + obj2.mins

        secs = obj1.secs + obj2.secs

        rs = secs // 60
        mins += rs
        secs -= 60 * rs

        rm = mins // 60
        hrs += rm
        mins -= 60 * rm
        return hrs, mins, secs


# --------------------UNCOMMENT THE TEST SNIPPETS AND RUN THE FILE TO TEST THE WORKING------------------
# Test snippets

# # testing declaration
# s1 = SumTime(time_string="10 00")
# s2 = SumTime("1 30")
# print(f"-->s1 => {s1}, s2 => {s2}")
#
# # testing __radd__
# s3 = ['1hrs', '10mins', '30secs', '1hrs50mins30secs'] + s1
# print("s3 = ['1hrs', '10mins', '30secs', '1hrs5mins30secs'] + s1 =>", s3)
#
# # testing __add__
# s3 = s1 + s2
# print("-->s3 = s1+s2 =>", s3)
#
# # testing __iadd__
# s3 += s2 + "1 00"
# print(f"-->s3 += s2 + \"1 00\"=>", s3)
#
# # testing __str__
# # print("-->To String:", str(s3))
#
# # testing @staticmethod to_sumtime()
# print("-->to sumtime:", type(SumTime.to_sumtime(str(s3))))
#
# # testing overall test cases
# # -> perform addition of time strings
#
# s1 = SumTime("1 20")
# print(f's1 = SumTime("1 20")={s1}')
# s1 += ["20mins", "1hrs 10mins", "50mins"]  # expected 3hrs 40mins
# print(f's1 += ["20mins", "1hrs 10mins", "50mins"]={s1}')
#
# s1 = s1 + ['20mins']
# print(f"s1 = s1 + [\"20mins\"]={s1}")  # expected 4hrs
#
# s1 += '10mins'
# print(f"s1 += '10mins'=", s1)
#
# td = s1.to_timedelta()
# print(f"td = s1.to_timedelta() =>{td.seconds} seconds , type:({type(td)})")
