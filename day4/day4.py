from typing import List


class Table:
    def __init__(self, lines: List[str]) -> None:
        self.cells = [ int(num) for line in lines for num in line.split() ]
        assert len(self.cells) == 25
        self.marks = [ False for _ in range(0, len(self.cells))]
        self.won = False

    def __repr__(self) -> str:
        return f"Table(cells: {self.cells}, marks: {self.marks})"

    def mark(self, num):
        if self.won:
            return None
        try:
            self.marks[self.cells.index(num)] = True
            if self.check():
                self.won = True
                return num * sum(self.unmarked())
            else:
                return None
        except ValueError:
            return None

    def rows(self):
        rows = [self.marks[start_index:start_index+5] for start_index in [0, 5, 10, 15, 20]]
        #print(f"Rows: {rows}")
        return rows

    def cols(self):
        cols_indices = [[ start_index + row_index*5 for row_index in range(5)] for start_index in range(5) ]
        #print(f"Col indices: {cols_indices}")
        cols = [[mark for index, mark in enumerate(self.marks) if index in col_indices] for col_indices in cols_indices]
        #print(f"Cols: {cols}")
        return cols

    def check(self):
        col_check = self.check_cols()
        row_check = self.check_rows()
        #print(f"Row check: {row_check}, col check: {col_check}")
        return self.check_cols() or self.check_rows()

    def check_rows(self):
        return any(all(row) for row in self.rows())

    def check_cols(self):
        return any(all(col) for col in self.cols())

    def unmarked(self):
        return [ item for index, item in enumerate(self.cells) if not self.marks[index]]

def parse_input():
    with open("day4/input") as input:
        drawn_numbers = [ int(num) for num in next(input).split(",")]
        next(input)
        table_lines = input.readlines()
        tables = [ Table(table_lines[table_start:table_start+5]) for table_start in range(0, len(table_lines), 6) ]
        #print(f"tables: {tables}")
        return drawn_numbers, tables

def part1():
    drawn_numbers, tables = parse_input()

    for drawn_number in drawn_numbers:
        for table in tables:
            result = table.mark(drawn_number)
            if result is not None:
                print(f"Part1: {result}")
                return

#part1()

def part2():
    drawn_numbers, tables = parse_input()

    results = []
    for drawn_number in drawn_numbers:
        for table in tables:
            result = table.mark(drawn_number)
            if result is not None:
                results += [result]

    print(f"Part2: {results}")

part2()