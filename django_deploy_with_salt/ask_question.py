class AskQuestion:

    def __init__(self, question, choices=None, default=None):
        self.answer = None
        self.question = question
        self.choices = choices
        self.default = default

    def __call__(self, *args, **kwargs):
        output = self.get_output()
        raw = raw_input(output)
        answer = self.validate_answer(raw)
        try:
            self.output_selected(answer)
        except ValueError:
            raise Exception('Invalid answer')
        return answer

    def output_selected(self, answer):
        print "You selected: " + str(answer)

    def get_output(self):
        output = self.question + '\n'
        if self.default is not None:
            output += '[0] Default:' + str(self.default) + '\n'
        y = 1
        if self.choices:
            for choice in self.choices:
                output += '[' + str(y) + '] ' + choice + '\n'
                y += 1
        output += 'Your answer:'
        return output

    def validate_answer(self, raw):
        if not self.choices:
            if raw.strip() == '' and self.default:
                return self.default
            else:
                return raw
        else:
            if raw.strip() == '':
                raw = 0
            answer_int = int(raw)
            if answer_int == 0:
                if self.default is None:
                    raise Exception("Invalid answer.")
                else:
                    return self.default
            elif 0 < answer_int <= len(self.choices):
                return self.choices[answer_int - 1]
            else:
                raise Exception("Invalid answer for '" + self.question + "'")