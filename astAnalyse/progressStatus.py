import time
import progressbar

class ProgressStatus:
    def __init__(self):
        self.start_time = time.time()
        self.amount_of_tasks = 0
        self.current_task = 0
        self.bar = None

    def addAmountOfTasks(self, amount):
        self.amount_of_tasks += amount
        self.bar = progressbar.ProgressBar(max_value=self.amount_of_tasks, widgets=self.get_widgets())

    def increaseCounter(self, amount):
        self.current_task += amount
        self.bar.update(self.current_task)

    def get_widgets(self):
        return [
            'Progress: ', progressbar.Percentage(),
            ' | Time Elapsed: ', progressbar.Timer(),
            ' | Estimated Time Left: ', progressbar.AdaptiveETA(),
            ' | Task: ', progressbar.SimpleProgress(),
            ' ', progressbar.Bar(),
        ]

    def format_time(self, seconds):
        hours, remainder = divmod(int(seconds), 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def printProgress(self, message):
        if self.bar is not None:
            self.bar.update(self.current_task)
            print(f" | {message}", end='\r', flush=True)
