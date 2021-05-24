
import mysql.connector
from sklearn import tree

cnx = mysql.connector.connect(user='root', password='',
                              host='127.0.0.1',
                              database='mldb')
carsInfo = []

cursor = cnx.cursor()
query = "select * from carinfo"
cursor.execute(query)
for (name, year, mile, price) in cursor:
    carsInfo.append([name, year, mile, price])

cursor.close()
cnx.close()

# print(carsInfo)
# starting fitting inputs and outputs for machine learning
x = []
y = []

for i in range(len(carsInfo)):
    x.append(carsInfo[i][1:4])
    y.append(carsInfo[i][0])

# classification based on tree
clf = tree.DecisionTreeClassifier()
clf = clf.fit(x, y)

# Enter year of production , mileage and price to get the name of your car;
new_data = [[2012, 100000, 6500], [2020, 50000, 50000], [2010, 5000, 1000000],[2010, 1000, 1000]]
answer = clf.predict(new_data)

for carname in answer:
    print(carname)



