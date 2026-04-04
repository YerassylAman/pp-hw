with open("demofile.txt", "a") as f:
  f.write("Now the file has more content!")
f.close()

#open and read the file after the appending:
with open("demofile.txt") as f:
  print(f.read()) 
f.close()
with open("demofile.txt", "w") as f:
  f.write("Woops! I have deleted the content!")
f.close()

#open and read the file after the overwriting:
with open("demofile.txt") as f:
  print(f.read()) 
f.close()

#Create a new file called "myfile.txt":
f = open("myfile.txt", "x") 



f = open("demofile.txt")
print(f.read()) 

# Using the with keyword:
with open("demofile.txt") as f:
  print(f.read()) 
f.close() 

# Return the 5 first characters of the file:
with open("demofile.txt") as f:
  print(f.read(5)) 

# Read one line of the file:
with open("demofile.txt") as f:
  print(f.readline()) 



import os
os.remove("demofile.txt") 

# Check if file exists, then delete it:
import os
if os.path.exists("demofile.txt"):
  os.remove("demofile.txt")
else:
  print("The file does not exist") 

# Remove the folder "myfolder":
import os
os.rmdir("myfolder") 