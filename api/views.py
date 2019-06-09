import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from api.documents import PropertyDocument
from elasticsearch_dsl import Q


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


@csrf_exempt
@api_view(['POST'])
def search(request, format=None):
    try:
        data = request.POST["data"]
        data = json.loads(data)
        s = PropertyDocument.search()
        if "area" in data:
            areaValues = data["area"].split(';')
            areashouldlist = list()
            for area in areaValues:
                areashouldmatchitem = Q('match', area=area)
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
            s = s.filter("term", city=data["city"].lower())
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
        if "action" in data:
            if data["action"] == "rent":
                s = s.doc_type("property_rent")
            else:
                s = s.doc_type("property_sale")
        else:
            s = s.doc_type("_doc")
        response = s.execute()  #to_dict() #
        # response = s.doc_type("property_rent")
        return HttpResponse(json.dumps(response.to_dict()))
        # return HttpResponse('total {}'.format(response))
    except UnicodeError as e:
        return HttpResponse(status=500,
                            content="requested data is wrong {}".format(e))  # <--- this response is only returned
    except Exception as ex:
        return HttpResponse(status=500,
                            content="unhandled exception {}".format(ex))  # <--- this response is only returned


@csrf_exempt
@api_view(['POST'])
def carsearch(request, format=None):
    try:
        data = request.POST["data"]
        data = json.loads(data)
        s = PropertyDocument.search()
        if "city" in data:
            s = s.filter("term", city=data["city"].lower())

        if "make" in data:
            s = s.filter("term", city=data["make"].lower())
        if "model" in data:
            s = s.filter("term", city=data["model"].lower())
        if "model" in data:
            s = s.filter("term", city=data["model"].lower())
        if "model" in data:
            s = s.filter("term", city=data["model"].lower())
        if "priceGt" in data:
            if "priceLt" in data:
                s = s.filter('range', **{"price": {"from": data["priceGt"], "to": data["priceLt"]}})
            else:
                s = s.filter('range', **{"price": {"from": data["priceGt"]}})
        elif "priceLt" in data:
            s = s.filter('range', **{"price": {"to": data["priceLt"]}})

        if "yearGt" in data:
            if "yearLt" in data:
                s = s.filter('range', **{"year": {"from": data["yearGt"], "to": data["yearLt"]}})
            else:
                s = s.filter('range', **{"year": {"from": data["yearGt"]}})
        elif "yearLt" in data:
            s = s.filter('range', **{"year": {"to": data["yearLt"]}})

        if "kmGt" in data:
            if "kmLt" in data:
                s = s.filter('range', **{"km": {"from": data["kmGt"], "to": data["kmLt"]}})
            else:
                s = s.filter('range', **{"km": {"from": data["kmGt"]}})
        elif "kmLt" in data:
            s = s.filter('range', **{"km": {"to": data["kmLt"]}})

        if "bodyStyle" in data:
            s = s.filter("term", city=data["body_style"].lower())
        if "doors" in data:
            s = s.filter("term", city=data["doors"].lower())

        if "driverType" in data:
            s = s.filter("term", city=data["drive_type"].lower())
        if "numCylinders" in data:
            s = s.filter("term", city=data["num_cylinders"].lower())

        if "from" in data and "size" in data:
            s = s[data["from"]:data["size"] + data["from"]]
        s = s.sort({"posting_date": {"order": "desc"}})

        response = s.execute()  # to_dict()
        # response = s.doc_type("property_rent")
        return HttpResponse('total {}'.format(response.hits.hits))
        # return HttpResponse('total {}'.format(response))
    except UnicodeError as e:
        return HttpResponse(status=500,
                            content="requested data is wrong {}".format(e))  # <--- this response is only returned
    except Exception as ex:
        return HttpResponse(status=500,
                            content="unhandled exception {}".format(ex))  # <--- this response is only returned
