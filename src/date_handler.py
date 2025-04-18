import json
import os
from datetime import datetime


class DateHandler:
    def __init__(self, file_path: str = "./data/dates.json") -> None:
        self.data_path: str = file_path
        if not os.path.exists(self.data_path):
            with open(self.data_path, "w") as f:
                json.dump({}, f, indent=2)
        # set self.current_date str
        self.current_date = ""
        self.SetCurrentDate()

        # set self.data dict
        self.dates: dict[str, int] = {}
        self.UpdateDatesObject()
        self.SortDates()

        # if data is empty set last_date to current date and write to file
        if self.dates.get(self.current_date) is None:
            self.WriteToDate(0)

        self.last_date = self.GetLastNonEmptyDate()

    def GetLastNonEmptyDate(self) -> str:
        i: int = -2
        try:
            while True:
                date: str = list(self.dates.keys())[i]
                if self.dates.get(date, 0) > 0:
                    return date
                else:
                    i -= 1
        except IndexError:
            return self.current_date

    def SetCurrentDate(self) -> bool:
        """sets self.current_date to todays date in the format **YYYY-MM-DD**

        Returns:
            bool: True if date changed else False
        """
        now: str = datetime.today().strftime("%Y-%m-%d")
        if now > self.current_date:
            self.current_date = now
            return True
        elif now == self.current_date:
            return False
        else:
            raise ValueError("Date is in the past")

    def UpdateDatesFile(self) -> None:
        with open(self.data_path, "w") as f:
            json.dump(self.dates, f, indent=2)

    def UpdateDatesObject(self) -> None:
        with open(self.data_path, "r") as f:
            self.dates = json.load(f)

    def SortDates(self) -> None:
        """Sorts the self.data dict by date and returns it"""
        self.dates = dict(sorted(self.dates.items()))
        self.UpdateDatesFile()

    def ReadDate(self, date: str | None = None) -> tuple[str, int]:
        # if date is empty set to current date
        if not date:
            date = self.current_date
        # return the date and associated number
        self.UpdateDatesObject()
        return date, self.dates[date]

    def WriteToDate(self, data: int, date: str | None = None) -> None:
        """Writes the *data* and the associated date to self.data and updates the data file

        Args:
            date (str): date to write
            data (int): number of finished sessions in the date
        """
        # if date is empty set to current date
        if not date:
            date = self.current_date
        # update the data dict
        self.dates.update({date: data})
        print(self.dates)
        self.UpdateDatesFile()


if __name__ == "__main__":
    dh = DateHandler()
