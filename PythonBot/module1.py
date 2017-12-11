if __name__ == '__main__':
    def do(l, c):
        if c[0] == "insert":
            return l.insert(int(c[1]), int(c[2])
        if c[0] == "print":
            print(l)
            return l
        if c[0] == "remove":
            list.remove(int(c[1])
            return list
        if c[0] == "append":
            list.append(int(c[1])
            return list
        print("Command not found")
        return list
                    
    N = int(raw_input())
    list = []
    for i in range(N):
        command = raw_input().split(' ')
        list = do(list, command)