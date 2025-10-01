import os
import unittest

class PollReader():
    """
    A class for reading and analyzing polling data.
    """
    def __init__(self, filename):
        """
        The constructor. Opens up the specified file, reads in the data,
        closes the file handler, and sets up the data dictionary that will be
        populated with build_data_dict().

        We have implemented this for you. You should not need to modify it.
        """

        # this is used to get the base path that this Python file is in in an
        # OS agnostic way since Windows and Mac/Linux use different formats
        # for file paths, the os library allows us to write code that works
        # well on any operating system
        self.base_path = os.path.abspath(os.path.dirname(__file__))

        # join the base path with the passed filename
        self.full_path = os.path.join(self.base_path, filename)

        # open up the file handler
        self.file_obj = open(self.full_path, 'r')

        # read in each line of the file to a list
        self.raw_data = self.file_obj.readlines()

        # close the file handler
        self.file_obj.close()

        # set up the data dict that we will fill in later
        self.data_dict = {
            'month': [],
            'date': [],
            'sample': [],
            'sample type': [],
            'Harris result': [],
            'Trump result': []
        }

    def build_data_dict(self):
        """
        Reads all of the raw data from the CSV and builds a dictionary where
        each key is the name of a column in the CSV, and each value is a list
        containing the data for each row under that column heading.

        There may be a couple bugs in this that you will need to fix.
        Remember that the first row of a CSV contains all of the column names,
        and each value in a CSV is seperated by a comma.
        """

        # iterate through each row of the data
        for line in self.raw_data[1:]:
            line = line.strip()
            if not line:
                continue

          
            separated = line.split(',')
            # The CSV file has 5 columns, so we must check for 5.
            if len(separated) != 5:
                continue

            # map each part of the row to the correct column
            self.data_dict['month'].append(separated[0].strip())
            self.data_dict['date'].append(int(separated[1].strip()))

            # The 'sample' column (index 2) contains both size and type, e.g., "1880 LV"
            # We need to split it to get both pieces of information.
            sample_info = separated[2].strip().split(' ')
            self.data_dict['sample'].append(int(sample_info[0]))
            if len(sample_info) > 1:
                self.data_dict['sample type'].append(sample_info[1])
            else:
                self.data_dict['sample type'].append(None) # Handle cases with no sample type

            # Harris and Trump results are at index 3 and 4 now
            self.data_dict['Harris result'].append(float(separated[3].strip().replace('%', '')))
            self.data_dict['Trump result'].append(float(separated[4].strip().replace('%', '')))



    def highest_polling_candidate(self):
        """
        This method should iterate through the result columns and return
        the name of the candidate with the highest single polling percentage
        alongside the highest single polling percentage.
        If equal, return the highest single polling percentage and "EVEN".

        Returns:
            str: A string indicating the candidate with the highest polling percentage or EVEN,
             and the highest polling percentage.
        """
        h = self.data_dict["Harris result"]
        t = self.data_dict["Trump result"]

        if not h or not t:
            return "No data available"

        h_max = max(h)
        t_max = max(t)

        if h_max > t_max:
            return f"Harris with {h_max:.1%}"
        elif t_max > h_max:
            return f"Trump with {t_max:.1%}"
        else:
            return f"EVEN with {h_max:.1%}"

    def likely_voter_polling_average(self):
        
        """
        Calculate the average polling percentage for each candidate among likely voters.

        Returns:
            tuple: A tuple containing the average polling percentages for Harris and Trump
                   among likely voters, in that order.
        """
        type_list = self.data_dict['sample type']
        h = self.data_dict["Harris result"]
        t = self.data_dict["Trump result"]

        hsum = 0.0
        tsum = 0.0
        cnt = 0

        for i in range(len(type_list)):
            # Check if sample type is 'LV'
            if type_list[i] and 'LV' in str(type_list[i]).upper():
                hsum += h[i]
                tsum += t[i]
                cnt += 1

        if cnt == 0:
            return (0.0, 0.0)

        return (hsum / cnt, tsum / cnt)


        


    def polling_history_change(self):
        """
        Calculate the change in polling averages between the earliest and latest polls.

        This method calculates the average result for each candidate in the earliest 30 polls
        and the latest 30 polls, then returns the net change.

        Returns:
            tuple: A tuple containing the net change for Harris and Trump, in that order.
                   Positive values indicate an increase, negative values indicate a decrease.
        """

        h = self.data_dict["Harris result"]
        t = self.data_dict["Trump result"]

        if len(h) < 60:
            return (0.0, 0.0)

        latest_harris   = h[:30]
        earliest_harris = h[-30:]
        avg_latest_harris   = sum(latest_harris) / 30.0
        avg_earliest_harris = sum(earliest_harris) / 30.0
        harris_change = avg_latest_harris - avg_earliest_harris

        latest_trump   = t[:30]
        earliest_trump = t[-30:]
        avg_latest_trump   = sum(latest_trump) / 30.0
        avg_earliest_trump = sum(earliest_trump) / 30.0
        trump_change = avg_latest_trump - avg_earliest_trump

        return (harris_change, trump_change)
    # 0–100 → 0–1
        return (harris_change, trump_change)

class TestPollReader(unittest.TestCase):
    """
    Test cases for the PollReader class.
    """
    def setUp(self):
        self.poll_reader = PollReader('polling_data.csv')
        self.poll_reader.build_data_dict()

    def test_build_data_dict(self):
        self.assertEqual(len(self.poll_reader.data_dict['date']), len(self.poll_reader.data_dict['sample']))
        self.assertTrue(all(isinstance(x, int) for x in self.poll_reader.data_dict['date']))
        self.assertTrue(all(isinstance(x, int) for x in self.poll_reader.data_dict['sample']))
        self.assertTrue(all(isinstance(x, str) for x in self.poll_reader.data_dict['sample type']))
        self.assertTrue(all(isinstance(x, float) for x in self.poll_reader.data_dict['Harris result']))
        self.assertTrue(all(isinstance(x, float) for x in self.poll_reader.data_dict['Trump result']))

    def test_highest_polling_candidate(self):
        result = self.poll_reader.highest_polling_candidate()
        self.assertTrue(isinstance(result, str))
        self.assertTrue("Harris" in result)
        self.assertTrue("57.0%" in result)

    def test_likely_voter_polling_average(self):
        harris_avg, trump_avg = self.poll_reader.likely_voter_polling_average()
        self.assertTrue(isinstance(harris_avg, float))
        self.assertTrue(isinstance(trump_avg, float))
        self.assertTrue(f"{harris_avg:.2%}" == "49.34%")
        self.assertTrue(f"{trump_avg:.2%}" == "46.04%")

    def test_polling_history_change(self):
        harris_change, trump_change = self.poll_reader.polling_history_change()
        self.assertTrue(isinstance(harris_change, float))
        self.assertTrue(isinstance(trump_change, float))
        self.assertTrue(f"{harris_change:+.2%}" == "+1.53%")
        self.assertTrue(f"{trump_change:+.2%}" == "+2.07%")


def main():
    poll_reader = PollReader('polling_data.csv')
    poll_reader.build_data_dict()

    highest_polling = poll_reader.highest_polling_candidate()
    print(f"Highest Polling Candidate: {highest_polling}")
    
    harris_avg, trump_avg = poll_reader.likely_voter_polling_average()
    print(f"Likely Voter Polling Average:")
    print(f"  Harris: {harris_avg:.2%}")
    print(f"  Trump: {trump_avg:.2%}")
    
    harris_change, trump_change = poll_reader.polling_history_change()
    print(f"Polling History Change:")
    print(f"  Harris: {harris_change:+.2%}")
    print(f"  Trump: {trump_change:+.2%}")



if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)