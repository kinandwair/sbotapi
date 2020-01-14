from flask import Flask, escape, request

import json
from elasticsearch_dsl import Q
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
import certifi
from flask_cors import CORS  # This is the magic


app = Flask(__name__)
CORS(app)
application = app # our hosting requires application in passenger_wsgi
client = Elasticsearch(['host_name'],port=9243,http_auth=("username", "password"), use_ssl=True, ca_certs=certifi.where())


@app.route("/")
def hello():
    return "Worked!\n"



@app.route("/searchsort",methods=['POST'])
def search():
    # try:
    data = request.json
    client = Elasticsearch(['host_name'],port=9243,http_auth=("username", "password"), use_ssl=True, ca_certs=certifi.where())
    if "action" in data:
        if data["action"] == "rent":
            s = Search(using=client, index="a_property_rent")
        else:
            s = Search(using=client, index="a_property_sale")
    else:
        s = Search(using=client, index="a_property_rent")

    if "area" in data and data["area"] != "":
        areaValues = data["area"].split(';')
        areashouldlist = list()
        for area in areaValues:
            #areashouldmatchitem = Q('match', area=area)
            areashouldmatchitem = Q('match', **{'area.raw': area.lower()})
             
            areashouldlist.append(areashouldmatchitem)
        q = Q('bool', should=areashouldlist)
        s = s.query(q)

    if "building" in data:
        buildingValues = data["building"].split(';')
        buildingshouldlist = list()
        for building in buildingValues:
            buildingshouldmatchitem = Q('match', building=building)
            buildingshouldlist.append(buildingshouldmatchitem)
        q = Q('bool', should=buildingshouldlist)
        s = s.query(q)
    if "amenities" in data:
        s = s.query("multi_match", query=data["amenities"], fields=['amenities', 'description'])


    if "city" in data:
        s = s.filter("term", **{'city.raw': data["city"].lower()})

    #return s.to_dict()
    if "priceGt" in data:
        if "priceLte" in data:
            s = s.filter('range', **{"price": {"from": data["priceGt"], "to": data["priceLte"]}})
        else:
            s = s.filter('range', **{"price": {"from": data["priceGt"]}})
    elif "priceLte" in data:
        s = s.filter('range', **{"price": {"to": data["priceLte"]}})
    if "bedrooms" in data:
        s = s.filter("term", bedrooms=data["bedrooms"])
    if "from" in data and "size" in data:
        s = s[data["from"]:data["size"] + data["from"]]
    s = s.sort({"posting_date" : {"order" : "desc"}})
    
    response = s.execute() 
    return response.to_dict()

@app.route("/searchcarsort",methods=['POST'])
def carsearch():
    try:
        data = request.json
        client = Elasticsearch(['host_name'],port=9243,http_auth=("username", "password"), use_ssl=True, ca_certs=certifi.where())
        s = Search(using=client, index="a_carsindex")
        if "city" in data and data["city"] != "":
            s = s.filter("term", **{'city.raw': data["city"].lower()})

        if "make" in data and data["make"] != "":
            s = s.filter("term", make=data["make"].lower())
        if "model" in data and data["model"] != "":
            s = s.filter("term",**{'model.raw': data["model"].lower()})
        if "priceGt" in data and data["priceGt"]!=0:
            if "priceLt" in data  and data["priceLt"]!=0:
                s = s.filter('range', **{"price": {"from": data["priceGt"], "to": data["priceLt"]}})
            else:
                s = s.filter('range', **{"price": {"from": data["priceGt"]}})
        elif "priceLt" in data and data["priceLt"]!=0:
            s = s.filter('range', **{"price": {"to": data["priceLt"]}})

        if "yearGt" in data and data["yearGt"]!=0:
            if "yearLt" in data and data["yearLt"] != 0 :
                s = s.filter('range', **{"year": {"from": data["yearGt"], "to": data["yearLt"]}})
            else:
                s = s.filter('range', **{"year": {"from": data["yearGt"]}})
        elif "yearLt" in data and data["yearLt"] != 0:
            s = s.filter('range', **{"year": {"to": data["yearLt"]}})

        if "kmGt" in data and data["kmGt"]!= 0:
            if "kmLt" in data and  data["kmLt"]!= 0:
                s = s.filter('range', **{"km": {"from": data["kmGt"], "to": data["kmLt"]}})
            else:
                s = s.filter('range', **{"km": {"from": data["kmGt"]}})
        elif "kmLt" in data and data["kmLt"]!= 0:
            s = s.filter('range', **{"km": {"to": data["kmLt"]}})

        if "bodyStyle" in data:
            s = s.filter("term", bodyStyle=data["body_style"].lower())
        if "doors" in data:
            s = s.filter("term", doors=data["doors"].lower())

        if "driverType" in data:
            s = s.filter("term", driverType=data["drive_type"].lower())
        if "numCylinders" in data:
            s = s.filter("term", numCylinders=data["num_cylinders"].lower())

        if "from" in data and "size" in data:
            s = s[data["from"]:data["size"] + data["from"]]
        s = s.sort({"posting_date": {"order": "desc"}})
        response = s.execute() 
        return response.to_dict()
    except Exception as ex:
        return ex



@app.route("/autocomplete")
def autocomplete():
    text = request.args.get('text')
    type = request.args.get('type')
    s = Search(using=client, index="autocomplete")
    s = s.suggest('autocomplete', text, completion={'field': type,'fuzzy': True,"skip_duplicates": True})
    s = s[0:0]
    response = s.execute()  # 
    return response.to_dict()
    response = s.execute()  # 

if __name__ == "__main__":
    app.debug = True
    app.run()
    