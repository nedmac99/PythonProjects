def main():
    print("Welcome to my Calculator!")
    print("Choose selection below\n------------------")
    list_of_nums = []
    choice = input("1. Addition\n2. Subtraction\n3. Multiplication\n4. Division\n5. Exit\n")
    if choice == "1":
        nums = input("Enter numbers to add separated by a space: ").split(" ")
        for i in nums:
            list_of_nums.append(int(i)) 
        print("Equals:", add(list_of_nums))
    elif choice == "2":
        ...
    elif choice == "3":
        ...
    elif choice == "4":
        ...
    elif choice == "5":
        ...
    else:
        print("Invalid choice")




def add(nums_to_add):
    answer = 0
    for i in nums_to_add:
        answer += i
    return answer

def subtrat():
    ...

def multiply():
    ...

def divide():
    ...

if __name__ == "__main__":
    main()