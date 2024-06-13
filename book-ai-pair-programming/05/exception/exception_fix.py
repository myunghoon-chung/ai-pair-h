def main():
    try:
        divisor = 1
        x = 1 / divisor
    except ZeroDivisionError as e:
        print("Error: Division by zero")
    except Exception as e:
        print("Error:", e)
    
    try:
        my_dict = {'name': 'Alice'}
        age = my_dict['name']
    except KeyError as e:
        print("Error: Key 'age' not found in dictionary")
    except Exception as e:
        print("Error:", e)

    try:
        int('1')  # ValueError
    except Exception as e:
        print("Error", e)

if __name__ == "__main__":
    main()
