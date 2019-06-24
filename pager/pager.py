class Pager:
    def __init__(self, count_per_page, count_per_block, total_count, current_page):
        self.count_per_page = count_per_page
        self.count_per_block = count_per_block
        self.total_count = total_count
        self.current_page = current_page

        self.total_page_count = int((self.total_count + self.count_per_page - 1) / self.count_per_page)
        self.total_block_count = int((self.total_page_count + self.count_per_block - 1) / self.count_per_block)
        self.current_block = int(self.current_page / self.count_per_block)
        self.preview_page = int(0 if (self.current_block == 0) else (self.current_block - 1) * self.count_per_block)
        self.next_page = int(self.total_page_count - 1 if (((self.current_block + 1) * self.count_per_block) + 1 > self.total_page_count) else ((self.current_block + 1) * self.count_per_block))
        self.start_block = int(self.current_block * self.count_per_block + 1)
        self.end_block = int(self.current_block * self.count_per_block + self.count_per_block)
