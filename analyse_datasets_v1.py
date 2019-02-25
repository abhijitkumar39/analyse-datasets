import json

file1 = open('y.json', 'r')
file2 = open('t.json', 'r')
priceChanges = open('price_changes.json', 'w')
priceNormalized = open('price_normalized.json', 'a')
count = 0
urlSet = []
matchedUrls = []
categories = []
priceDict = {}
catDict = {}
priceNormalizedDict = {}
fullCategory = []
nonOverLappingCategories = []
for contents1 in file1:
    yesterday = json.loads(contents1)
    urlSet.append(yesterday)
    category1 = yesterday['category']
    categories.append(category1)
    subcategory1 = yesterday['subcategory']
    fullCategory1 = category1 + " > " + subcategory1
    fullCategory.append(fullCategory1)
    # print(fullCategory1)
    #-- Normalizing prices for first file
    priceRaw = yesterday['available_price']
    if (priceRaw is None or priceRaw == 0):
        priceRaw = "NA"
        yesterday['available_price'] = priceRaw
        normalizedPriceJson = json.dumps(yesterday) + "\n"
        priceNormalized.write(normalizedPriceJson)
    else:
        normalizedPriceJson = json.dumps(yesterday) + "\n"
        priceNormalized.write(normalizedPriceJson)

for contents2 in file2:
    today = json.loads(contents2)
    urlh = today['urlh']
    category2 = today['category']
    subcategory2 = today['subcategory']
    fullCategory2 = category2 + " > " + subcategory2
    fullCategory.append(fullCategory2)
    categories.append(category2)
    #-- Normalizing prices for second file
    priceRaw2 = today['available_price']
    if (priceRaw2 is None or priceRaw2 == 0):
        priceRaw2 = "NA"
        today['available_price'] = priceRaw2
        normalizedPriceJson2 = json.dumps(today) + "\n"
        priceNormalized.write(normalizedPriceJson2)
    else:
        normalizedPriceJson2 = json.dumps(today) + "\n"
        priceNormalized.write(normalizedPriceJson2)
    for lines in urlSet:
        if lines['urlh'] == urlh:
            print(urlh)
            status1 = lines['http_status']
            status2 = today['http_status']
            if (status1 == status2 and lines['available_price'] is not None and today['available_price'] is not None and lines['available_price'] != "NA" and today['available_price'] != "NA"):
                price1 = float(lines['available_price'])
                price2 = float(today['available_price'])
                # print(price1)
                # print(price2)
                matchedUrls.append(urlh)
                priceDiff = price2 - price1
                priceDict["urlh"] = urlh
                priceDict["price_difference"] = priceDiff
                print(priceDict)
                matchingJson = json.dumps(priceDict) + "\n"
                #--JSON File where all the price difference and matching URLs are stored
                priceChanges.write(matchingJson)

        #-- Checking non overlapping categories
        if lines['category'] != category2:
            #print("Not Matched")
            nonOverLappingCategories.append(lines['category'])


#-- Get the number of overlapping URLs
numberOfOverlappingUrls = len(matchedUrls)
print("Number of overlapping URLs : " + str(matchedUrls))

#-- Stats to generate number of unique categories
numberOfUniqueCategories = len(list(dict.fromkeys(categories)))
print("Number of unique Categories : " + str(numberOfUniqueCategories))

#-- Get number of non overlapping categories
numberOfNonOverlappingCategories = len(nonOverLappingCategories)
print("Number of non overlapping categories : " + str(numberOfNonOverlappingCategories))

#-- Stats generation for all the taxonomies
for item in fullCategory:
    if item in catDict:
        catDict[item] = catDict.get(item) + 1
    else:
        catDict[item] = 1

for k, v in catDict.items():
    print(str(k) + ':' + str(v))
