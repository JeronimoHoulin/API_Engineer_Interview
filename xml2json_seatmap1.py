"""
Created on Mon Oct 11 17:47:48 2021

@author: Jerónimo Houlin
"""

#Seatmap Exercise for Gordian Software
#XML to JSON parsing 


import os
from xml.etree import ElementTree as ET
import json

### Seat Map 1 ##
file_name = 'seatmap1.xml'
full_file_name = os.path.abspath(os.path.join('Desktop\APIEngineerTechnicalExercise_v2', file_name))
dom = ET.parse(full_file_name)  #for reading the XML file



#print(dom)  where in our memory we have the XML element
root = dom.getroot()
#print(root.tag) 
ET.dump(dom)  #We get the print of the XML

for child in root.iter():
   print(child.tag, child.attrib)
   
   

###########################The flights Info
flight_info = []

for elem in root.findall(".//{*}FlightSegmentInfo"): 
    #print(elem.attrib)
    flight_info.append(elem.attrib)
    
###########################The rows Info
flight_rows = []

for elem in root.findall(".//{*}RowInfo"): 
    #print(elem.attrib)
    flight_rows.append(elem.attrib)


#Pop unnesecary info
for i in range(0,len(flight_rows)):
    del flight_rows[i]["OperableInd"]

###########################Each seat info
seat_info = []

for each in root.findall('.//{http://www.opentravel.org/OTA/2003/05/common/}SeatInfo'):
    seatinfo = each.find('.//{http://www.opentravel.org/OTA/2003/05/common/}Summary')
    
    if seatinfo.attrib:
        #print(seatinfo.attrib)
        seat_info.append(seatinfo.attrib)
    
#Pop unnesecary info
for i in range(0,len(seat_info)):
    del seat_info[i]["InoperativeInd"]
    del seat_info[i]["OccupiedInd"]
    seat_info[i]["Available"] = seat_info[i].pop("AvailableInd")
    
###########################Additional seat info
###########################Features

feature_info = []

for each in root.findall('.//{http://www.opentravel.org/OTA/2003/05/common/}SeatInfo'):
    feature = each.find('.//{http://www.opentravel.org/OTA/2003/05/common/}Features')
    if feature.text:
        #print(feature.text)
        feature_info.append(feature.text)
    
#Check if seat info = features_info (length)
#print(len(seat_info))
#print(len(feature_info))

###########################Price
#Icouldnt get the price tag out of the nesting, so I added them as a separate array.. (Because I realized the last rows all had prices/ not the first)

price_info = [] 

for fee in root.findall('.//{http://www.opentravel.org/OTA/2003/05/common/}Fee'):
    #print(fee.attrib)
    price_info.append(fee.attrib)

#print(len(price_info))

price_info = [0] * (len(seat_info) - len(price_info)) + price_info


print(len(price_info))
#Which is the same as 
print(len(seat_info))
print(len(feature_info))

#Pop unnesecary info
for i in range(66,len(price_info)):
    del price_info[i]["CurrencyCode"]
    del price_info[i]["DecimalPlaces"]
    price_info[i]["USDPrice"] = price_info[i].pop("Amount")



#We get our output:
print(flight_info)
print(flight_rows)
print(len(flight_rows))
print(seat_info)
print(feature_info)
print(price_info)



"""
Create the Dictionary DF arranged accordingly
"""


data = {}


for n in range(0,len(flight_rows)):
    #29 rows
    data[f'row{n}'] = {}
    
    if n < 2:
        for i in range(0,4):
            data[f'row{n}'][f'seat{i}'] = {}
            data[f'row{n}'][f'seat{i}'][f'feature{i}'] = {}
            data[f'row{n}'][f'seat{i}'][f'price{i}'] = {}

            
    #we hace created our first class rows
    
    else:
        for i in range(8,14):
            data[f'row{n}'][f'seat{i}'] = {}
            data[f'row{n}'][f'seat{i}'][f'feature{i}'] = {}
            data[f'row{n}'][f'seat{i}'][f'price{i}'] = {}





#NOW WE FILL UP OUR PLACES

for n in range(0,len(flight_rows)):
    #29 rows
    data[f'row{n}'] = flight_rows[n]

    if n < 2:
        for i in range(0,4):
            data[f'row{n}'][f'seat{i}'] = seat_info[i]
            data[f'row{n}'][f'seat{i}'][f'feature{i}'] = feature_info[i]
            data[f'row{n}'][f'seat{i}'][f'price{i}'] = price_info[i]

            
    else:
        for i in range(8,14):
            data[f'row{n}'][f'seat{i}'] = seat_info[i]
            data[f'row{n}'][f'seat{i}'][f'feature{i}'] = feature_info[i]
            data[f'row{n}'][f'seat{i}'][f'price{i}'] = price_info[i]



Data = {}
Data['Flight Information'] = {}
Data['Seat Map'] = {}


#we pass on the flight info
Data['Seat Map'] = data
Data['Flight Information'] = flight_info


"""
Create the JSON File
"""


def write2json(path, filename, data):
    filePathNameWExt =  path + '/' + filename + '.json'
    with open(filePathNameWExt, 'w') as fp:
        json.dump(data, fp)


# Path
path = full_file_name.replace("\\seatmap1.xml", "")
filename = 'Seatmap1_parsed'



#print(json.dumps(Data))


write2json(path, filename, Data)






















"""
OTHER CRACKS AT IT








for elem in root.findall("."): #Check https://docs.python.org/3/library/xml.etree.elementtree.html for supported XPath wyntax
    print(elem.tag)

#So
#{http://schemas.xmlsoap.org/soap/envelope/}Envelope
#is our root tag


length_children = 0
for elem in root.findall(".//"): 
    #print(elem.attrib)
    length_children += 1
    
print(length_children)



##The flights Info
flight_info = []
for elem in root.findall(".//{*}FlightSegmentInfo"): 
    print(elem.attrib)
    flight_info.append(elem.attrib)



##Only the info for class First, Row 1 & 2
flight_rows = []
for elem in root.findall(".//{*}CabinClass[@Layout = 'AB EF']/"): 
    if elem.attrib:
        print(elem.attrib)
        flight_rows.append(elem.attrib)
        
        
        
##Only the info for class First, Row 7 to 39 with 5 missing rows between First and Eco.
for elem in root.findall(".//{*}CabinClass[@Layout = 'ABC DEF']/"): 
    if elem.attrib:
        flight_rows.append(elem.attrib)
        print(elem.attrib)




for i in range(0,len(flight_rows)):
    d = flight_rows[i]
    row = d['RowNumber']
    #print(row)
    
    #Add First class info
    if int(row) < 3:
        xpath = ".//*[@Layout = 'AB EF']/*[@RowNumber = '"
        xpath += str(row)
        xpath += "']/{*}RowInfo/"
        
        for elem in root.findall(xpath):
            if elem.attrib:
                print(elem.attrib)
                d['RowInfo']=elem.attrib
        
    #Add Economy class info
    if int(row) > 3: 
        #print(row)
        xpath = ".//*[@Layout = 'ABC DEF']/*[@RowNumber = '"
        xpath += str(row)
        xpath += "']/{*}RowInfo/"
        
        for elem in root.findall(str(xpath)):
            if elem.attrib:
                #print(elem.attrib)
                d['RowInfo']=elem.attrib
                
    #Delete unnesesary info
    print(flight_rows[i]['RowInfo'])
    del flight_rows[i]['RowInfo']["OperableInd"]
    del flight_rows[i]['RowInfo']["InoperativeInd"]
    del flight_rows[i]['RowInfo']["OccupiedInd"]







##LO MISMO CON EL FEE Y TOY.











i = [1,2,3]
#Row 1 seat ids (4 seats, Only missing is Seat Price)
for elem in root.findall(".//*[@Layout = 'AB EF']/*[@RowNumber = 'i']/{*}SeatInfo/"):
    if elem.attrib: 
        print(elem.attrib)


array = 0
for elem in root.findall(".//*[@Layout = 'ABC DEF']/*{*}SeatInfo/"):
    if elem.attrib:
        print(elem.attrib)
    array+=1
print(array)



array = 0
for elem in root.findall(".//*[@Layout = 'ABC DEF']/*[@RowNumber = '7']/{*}SeatInfo/"): 
    print(elem.attrib)
    array+=1
print(array)

#Rows 7 - 39 seat ids (6 seats)

array = 0
for elem in root.findall(".//{*}Fee"): 
    if elem.attrib:
        print(elem.attrib)
    array+=1
print(array)

#Seat Price




################### Flight to JSON
dictionary1 = flight_info[0]

flight_details_json = json.dumps(dictionary1, indent = 4) 



################### Flight Rows to JSON

flight_rows_json = json.dumps(flight_rows)


################### Flight seats to JSON

flight_seats_json = json.dumps(seat_info)


################### Flight features to JSON

flight_features_json = json.dumps(feature_info)
    
################### Flight price to JSON

flight_price_json = json.dumps(price_info)   
    













x = 0
i = 0
n = 0

flight_rows = {}
flight_rows[f'rows{x}'] = {}
flight_rows[f'rows{x}'][f'seat{i}'] = {}
flight_rows[f'rows{x}'][f'seat{i}'][f'info{n}'] = {}
no_data = {}

add_info = []
add_seat = []


for child in root.findall('.//{http://www.opentravel.org/OTA/2003/05/common/}RowInfo//'):
    #print(len(child.attrib))
    #print(child.attrib)
    add_info.append(child.attrib)



for y in range(0,len(add_info)):

    flight_rows[f'rows{x}'][f'seat{i}'][f'info{n}'] = add_info[y]
    
    n+=1
    
    if len(add_info[y]) == 0:
        #print(n)
        #print("Its an empty dict")
        #arr = range(0,n-1)
        #print(arr)
        #print(add_info[0])
        
        add_seat.append(add_info[0:y])
        print(add_seat)
        
        for xx in range(0,y):
            add_info.pop(xx)
        n+=1
        
    
    
    flight_rows[f'rows{x}'][f'seat{i}'] = add_seat
        
    i+=1
    
    add_seat = []
    


    
    
    flight_rows[f'rows{x}'][f'seat{i}'][f'info{n}'] = child.attrib
    n+=1
    
    print(flight_rows[f'rows{x}'][f'seat{i}'][f'info{n-1}'])
    
    if flight_rows[f'rows{x}'][f'seat{i}'][f'info{n}'] == "{}":
        print("done")
        
        flight_rows[f'rows{x}'][f'seat{i}'][f'info{n}'] = child.attrib
        no_data = flight_rows[f'rows{x}'][f'seat{i}'][f'info{n}']
        
        
        for y in range(0, n):
            flight_rows[f'rows{x}'][f'seat{i}'] = flight_rows[f'rows{x}'][f'seat{i}'][f'info{y}']
            #print(flight_rows[f'rows{x}'][f'seat{i}'][f'info{y}'])
            
            i+=1
        n+=1
        
        if i == 4: 
            flight_rows[f'rows{x}'] = flight_rows[f'rows{x}'][f'seat{i}']
            
            x+=1
        
        if i == 8: 
            flight_rows[f'rows{x}'] = flight_rows[f'rows{x}'][f'seat{i}']
            
            x+=1
            
            
            
        for z in range(14, 27, 6):
            if i == z:
                flight_rows[f'rows{z}'] = flight_rows[f'rows{x}'][f'seat{i}']
                
                x+=1
        
        
    

#Pop unnesecary info
for i in range(0,len(flight_rows)):
    del flight_rows[i]["OperableInd"]





a = 0
b= 0

while a < 28:
    for x in range(a, a+1):
        Data['Details']['Rows'] = flight_rows[x]
        

    while b < 8:
        for y in range(b, b+4):
            Data['Details']['Rows']['Seats'] = seat_info[y]

    while b > 8 and b < 170:
        for y in range(b, b+6):
            Data['Details']['Rows']['Seats'] = seat_info[y]

        a += 1
        b += 1



Data['Details'] = flight_info                    








    
        

print(json.dumps(Data))


write2json('./','file-name',data)







"""
