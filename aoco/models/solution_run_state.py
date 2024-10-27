class SolutionRunState:
    def __init__(self, part: str, is_test: bool, has_done: bool):
        self.part = part
        self.is_test = is_test
        self.has_done = has_done

    def advance_part(self):
        match self.part:
            case "1":
                self.part = "2"
                self.is_test = True
                self.has_done = False
            case "2":
                self.has_done = True

    def advance_subpart(self):
        self.is_test = False
