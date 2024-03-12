#test
passwordFile = open('новый 1.txt')
secretPassword = passwordFile.read()
print('введите пароль')
typedPassword = input()
if typedPassword == secretPassword:
    print('welcome')
    if typedPassword == '12345':
        print('password error!')
else:
    print('acces denied!')