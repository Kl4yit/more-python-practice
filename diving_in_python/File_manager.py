import os.path
import tempfile
import uuid


class File:
    def __init__(self, path_to_file: str):
        self.desctr = None
        self.path_to_file = path_to_file
        if not os.path.exists(path_to_file):
            self.write('')

    def read(self):
        with open(self.path_to_file, 'r') as f:
            raw = f.read()
        return raw

    def write(self, new_content: str):
        with open(self.path_to_file, 'w') as f:
            n = f.write(new_content)
        return n

    def __add__(self, other):
        path_for_result = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))
        new_obj = File(path_for_result)
        new_obj.write(self.read() + other.read())
        return new_obj

    def __str__(self):
        return os.path.abspath(self.path_to_file)

    def __iter__(self):
        return self

    def __next__(self):
        if not self.desctr:
                self.desctr = open(self.path_to_file, 'r')
        try:
            return next(self.desctr)
        except StopIteration:
            self.desctr.close()
            self.desctr = None
            raise StopIteration

