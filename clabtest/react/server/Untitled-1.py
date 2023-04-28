def validatepw(password):
      a=0
      b=0
      c=0
      d=0
      if len(password)<8 or len(password)>20:
         return False
      for i in password:
         if i.isupper():
            a+=1
         elif i.islower():
            b+=1
         elif i in '"!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~"':
            c+=1
         elif i.isdigit():
            d+=1
      if a>=1 and b>=1 and c>=1 and d>=1 and a+b+c+d==len(password):
        return 1
      else:
         return 0

print(validatepw('Bearsbears'))
print(validatepw('Charger$'))
print(validatepw('Packer$123'))
print(validatepw('Charegrshug#$$!12'))
print(validatepw('ThiS^is@#$A&^Pass3rword&^@'))