def getCurrentSemesterUgradEndDateWrapper (self):
    try:
        return self.getCurrentSemesterUgradEndDate()
    except TypeError:
        return "getCurrentSemesterUgradEndDate raised a TypeError exception"
    except:
        return self.getCurrentSemesterUgradEndDate()
