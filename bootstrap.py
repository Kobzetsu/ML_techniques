
def bootstrap(nums, K):
    N = len(nums)
    ans = []
    temp = []
    for i in range(0, N):
        temp.append(nums[i])
        if (((i + 1) % K) == 0):
            ans.append(temp.copy())
            temp.clear()

    # Если последняя группа недостаточного размера
    # добавляем элементы 0 до нужного размера
    if (len(temp) != 0):
        a = len(temp)
        while (a != K):
            temp.append(0)
            a += 1

        ans.append(temp)

    return ans
