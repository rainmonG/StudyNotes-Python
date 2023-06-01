from abc import abstractmethod

# 基类
class Item:
    def __init__(self, src) -> None:
        self.source = src

    @abstractmethod
    def out(self):
        pass

# 计数器类
class Counter(Item):
    def __init__(self, v) -> None:
        super().__init__(0)
        self.value = v

    def out(self):
        self.value += 1
        return self.value-1

# 过滤器
class Filter(Item):
    def __init__(self, src, f) -> None:
        super().__init__(src)
        self.factor = f

    def out(self):
        """ while True:
            n = self.source.out()
            if n % self.factor:
                return n """
        n = self.source.out()
        while not n % self.factor:
            n = self.source.out()
        return n

# 筛子类
class Sieve(Item):
    def __init__(self, src) -> None:
        super().__init__(src)

    def out(self):
        n = self.source.out()
        self.source = Filter(self.source, n)
        return n

# 主函数
def main():
    c = Counter(2)
    s = Sieve(c)
    n = int(input('输入上限：'))
    res = s.out()
    while n >= res:
        print(res, end=' ')
        res = s.out()
    """ while True:
        next = s.out()
        if next > n:
            break
        print(next, end=' ') """

main()