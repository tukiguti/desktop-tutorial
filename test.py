# -*- coding: utf-8 -*-
import sys

# Ensure stdout is using UTF-8 encoding
if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return "エラー: ゼロで割ることはできません"  # Error: Cannot divide by zero
    return a / b

def power(a, b):
    return a ** b

def modulus(a, b):
    if b == 0:
        return "エラー: ゼロで割ることはできません"  # Error: Cannot divide by zero
    return a % b

def calculator():
    print("簡単な計算機へようこそ！")  # Welcome to the simple calculator!
    print("終了するには 'q' を入力してください")  # Enter 'q' to quit
    
    while True:
        print("\n計算式を入力してください (例: 5 + 3, 10 * 2, 2 ^ 3, 10 % 3):")  # Enter calculation formula
        user_input = input("> ")
        
        if user_input.lower() == 'q':
            print("計算機を終了します")  # Exiting calculator
            break
        
        try:
            # Split the input into operands and operator
            parts = user_input.split()
            if len(parts) != 3:
                print("無効な入力です。'数値 演算子 数値' の形式で入力してください")  # Invalid input
                continue
                
            a = float(parts[0])
            op = parts[1]
            b = float(parts[2])
            
            # Perform the calculation
            if op == '+':
                result = add(a, b)
            elif op == '-':
                result = subtract(a, b)
            elif op == '*':
                result = multiply(a, b)
            elif op == '/':
                result = divide(a, b)
            elif op == '^':
                result = power(a, b)
            elif op == '%':
                result = modulus(a, b)
            else:
                print("無効な演算子です。+, -, *, /, ^, % のいずれかを使用してください")  # Invalid operator
                continue
                
            print(f"結果: {result}")  # Result
            
        except ValueError:
            print("無効な数値です。もう一度試してください")  # Invalid number
        except Exception as e:
            print(f"エラー: {e}")  # Error
    
# Run the calculator
if __name__ == "__main__":
    calculator()