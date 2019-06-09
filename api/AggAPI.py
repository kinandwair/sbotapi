import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from api.documents import PropertyDocument
from elasticsearch_dsl import Q
from elasticsearch_dsl import A


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


@csrf_exempt
@api_view(['GET'])
def averagePricePerArea(request, format=None):
    cities = request.GET["cities"]
    numberOfMonths = request.GET["numberOfMonths"] or 30
    priceGreaterThanOrEqual = request.GET["priceFrom"] or None
    priceLessThanOrEqual = request.GET["priceTo"] or None
    if "propertyTypes" in request.GET:
        propertyTypes = request.GET["propertyTypes"] or None
    else:
        propertyTypes = "rent"
    s = PropertyDocument.search()
    if cities is not None:
        citiesValues = cities.split(',')
        citiesshouldlist = list()
        for city in citiesValues:
            buildingshouldmatchitem = Q('match', city=city)
            citiesshouldlist.append(buildingshouldmatchitem)
        q = Q('bool', should=citiesshouldlist)
        s = s.query(q)
        if priceGreaterThanOrEqual is not None:
            if priceLessThanOrEqual is not None:
                s = s.filter('range', **{"price": {"from": priceGreaterThanOrEqual, "to": priceLessThanOrEqual}})
            else:
                s = s.filter('range', **{"price": {"from": priceGreaterThanOrEqual}})
        elif priceLessThanOrEqual is not None:
            s = s.filter('range', **{"price": {"to": priceLessThanOrEqual}})
        if numberOfMonths is not None:
            s = s.filter('range', **{"posting_date": {"from": "now-" + numberOfMonths + "d"}})

        s = s[0:0]
        a = A('terms', field='city.raw', size=100)
        a1 = A('terms', field='area.raw', size=100, exclude="NA|na")
        a2 = A('terms', field='bedrooms', size=10000, exclude=[-1], order={"_term": "asc"})
        a3 = A('percentiles', field='price')#
        s.aggs.bucket('CityAgg', a).bucket('AreaAgg', a1).bucket('BedroomAgg', a2).bucket('PriceAgg', a3)
        s = s.doc_type("_doc")
        response = s.execute()
        return HttpResponse(json.dumps(response.to_dict()))
    else:
        return HttpResponse(status=500,
                            content="requested data is wrong ")  # <--- this response is only returned


@csrf_exempt
@api_view(['GET'])
def averagePricePerBuildingForSpecificAreaAndSize(request, format=None):
    cities = request.GET["cities"]
    numberOfMonths = request.GET["numberOfMonths"] or 30
    priceGreaterThanOrEqual = request.GET["priceFrom"] or None
    priceLessThanOrEqual = request.GET["priceTo"] or None
    if "propertyTypes" in request.GET:
        propertyTypes = request.GET["propertyTypes"] or None
    else:
        propertyTypes = "rent"
    area = request.GET["area"] or None
    size = request.GET["size"] or None
    s = PropertyDocument.search()
    if cities is not None:
        citiesValues = cities.split(',')
        citiesshouldlist = list()
        for city in citiesValues:
            buildingshouldmatchitem = Q('match', city=city)
            citiesshouldlist.append(buildingshouldmatchitem)
        q = Q('bool', should=citiesshouldlist)
        s = s.query(q)
        if area is not None:
            areaValues = area.split(',')
            areashouldlist = list()
            for onearea in areaValues:
                areashouldmatchitem = Q('match', area=onearea)
                areashouldlist.append(areashouldmatchitem)
            q = Q('bool', should=areashouldlist)
            s = s.query(q)
        if priceGreaterThanOrEqual is not None:
            if priceLessThanOrEqual is not None:
                s = s.filter('range', **{"price": {"from": priceGreaterThanOrEqual, "to": priceLessThanOrEqual}})
            else:
                s = s.filter('range', **{"price": {"from": priceGreaterThanOrEqual}})
        elif priceLessThanOrEqual is not None:
            s = s.filter('range', **{"price": {"to": priceLessThanOrEqual}})
        if numberOfMonths is not None:
            s = s.filter('range', **{"posting_date": {"from": "now-" + numberOfMonths + "d"}})

        if size is not None:
            s = s.filter('term', bedrooms=size)

        a = A('terms', field='building.raw', size=100)
        a3 = A('percentiles', field='price')
        s.aggs.bucket('BuildingAgg', a).bucket('PriceAgg', a3)
        s = s.doc_type("_doc")
        response = s.execute()
        return HttpResponse(json.dumps(response.to_dict()))
    else:
        return HttpResponse(status=500,
                            content="requested data is wrong ")  # <--- this response is only returned


@csrf_exempt
@api_view(['GET'])
def averagePricePerSizeForSecificArea(request, format=None):
    cities = request.GET["cities"]
    numberOfMonths = request.GET["numberOfMonths"] or 30
    priceGreaterThanOrEqual = request.GET["priceFrom"] or None
    priceLessThanOrEqual = request.GET["priceTo"] or None
    if "propertyTypes" in request.GET:
        propertyTypes = request.GET["propertyTypes"] or None
    else:
        propertyTypes = "rent"
    area = request.GET["area"] or None
    s = PropertyDocument.search()
    if cities is not None:
        citiesValues = cities.split(',')
        citiesshouldlist = list()
        for city in citiesValues:
            buildingshouldmatchitem = Q('match', city=city)
            citiesshouldlist.append(buildingshouldmatchitem)
        q = Q('bool', should=citiesshouldlist)
        s = s.query(q)
        if area is not None:
            areaValues = area.split(',')
            areashouldlist = list()
            for onearea in areaValues:
                areashouldmatchitem = Q('match', area=onearea)
                areashouldlist.append(areashouldmatchitem)
            q = Q('bool', should=areashouldlist)
            s = s.query(q)

        if priceGreaterThanOrEqual is not None:
            if priceLessThanOrEqual is not None:
                s = s.filter('range', **{"price": {"from": priceGreaterThanOrEqual, "to": priceLessThanOrEqual}})
            else:
                s = s.filter('range', **{"price": {"from": priceGreaterThanOrEqual}})
        elif priceLessThanOrEqual is not None:
            s = s.filter('range', **{"price": {"to": priceLessThanOrEqual}})
        if numberOfMonths is not None:
            s = s.filter('range', **{"posting_date": {"from": "now-" + numberOfMonths + "d"}})

        a = A('terms', field='bedrooms', exclude=[-1], order={"_term": "asc"}, size=10000)
        a3 = A('percentiles', field='price')
        s.aggs.bucket('SizeAgg', a).bucket('PriceAgg', a3)
        s = s.doc_type("_doc")
        response = s.execute()
        return HttpResponse(json.dumps(response.to_dict()))
    else:
        return HttpResponse(status=500,
                            content="requested data is wrong ")  # <--- this response is only returned


@csrf_exempt
@api_view(['GET'])
def averagePricesPerAreaPerSizeForSpecificCoordinates(request, format=None):
    numberOfMonths = request.GET["numberOfMonths"] or 30
    latitude = request.GET["latitude"] or None
    longitude = request.GET["longitude"] or None
    if "propertyTypes" in request.GET:
        propertyTypes = request.GET["propertyTypes"] or None
    else:
        propertyTypes = "rent"
    distance = request.GET["distance"] or None
    s = PropertyDocument.search()

    if numberOfMonths is not None:
        s = s.filter('range', **{"posting_date": {"from": "now-" + numberOfMonths + "d"}})

    s = s.filter(
        'geo_distance', distance='{}m'.format(distance), location={"lat": latitude, "lon": longitude}
    )

    a = A('terms', field='bedrooms', exclude=[-1], order={"_term": "asc"}, size=10000)
    a3 = A('percentiles', field='price')
    s.aggs.bucket('SizeAgg', a).bucket('PriceAgg', a3)
    s = s.doc_type("_doc")
    response = s.execute()
    return HttpResponse(json.dumps(response.to_dict()))


@csrf_exempt
@api_view(['GET'])
def whatAreTheAveragePricesInSpecificBuilding(request, format=None):
    city = request.GET["city"]
    priceGreaterThanOrEqual = request.GET["priceGreaterThanOrEqual"] or None
    priceLessThanOrEqual = request.GET["priceLessThanOrEqual"] or None
    if "propertyTypes" in request.GET:
        propertyTypes = request.GET["propertyTypes"] or None
    else:
        propertyTypes = "rent"
    area = request.GET["area"] or None
    building = request.GET["building"] or None
    s = PropertyDocument.search()

    if priceGreaterThanOrEqual is not None:
        if priceLessThanOrEqual is not None:
            s = s.filter('range', **{"price": {"from": priceGreaterThanOrEqual, "to": priceLessThanOrEqual}})
        else:
            s = s.filter('range', **{"price": {"from": priceGreaterThanOrEqual}})
    elif priceLessThanOrEqual is not None:
        s = s.filter('range', **{"price": {"to": priceLessThanOrEqual}})
    if city is not None:
        s = s.filter('term', city=city)
    if area is not None:
        s = s.filter('term', area=area)
    if building is not None:
        s = s.filter('term', building=building)

    a = A('terms', field='bedrooms', size=1000)
    a3 = A('percentiles', field='price')
    s.aggs.bucket('BedroomAgg', a).bucket('PriceAgg', a3)
    s = s.doc_type("_doc")
    response = s.execute()
    return HttpResponse(json.dumps(response.to_dict()))


@csrf_exempt
@api_view(['GET'])
def propertiesInCityPerBudget(request, format=None):
    cities = request.GET["cities"]
    priceGreaterThanOrEqual = request.GET["budgetFrom"] or None
    priceLessThanOrEqual = request.GET["budgetTo"] or None
    if "propertyTypes" in request.GET:
        propertyTypes = request.GET["propertyTypes"] or None
    else:
        propertyTypes = "rent"
    numberOfMonths = request.GET["numberOfMonths"] or 30
    s = PropertyDocument.search()
    if cities is not None:
        citiesValues = cities.split(',')
        citiesshouldlist = list()
        for city in citiesValues:
            buildingshouldmatchitem = Q('match', city=city)
            citiesshouldlist.append(buildingshouldmatchitem)
        q = Q('bool', should=citiesshouldlist)
        s = s.query(q)
    if priceGreaterThanOrEqual is not None:
        if priceLessThanOrEqual is not None:
            s = s.filter('range', **{"price": {"from": priceGreaterThanOrEqual, "to": priceLessThanOrEqual}})
        else:
            s = s.filter('range', **{"price": {"from": priceGreaterThanOrEqual}})
    elif priceLessThanOrEqual is not None:
        s = s.filter('range', **{"price": {"to": priceLessThanOrEqual}})
    if numberOfMonths is not None:
        s = s.filter('range', **{"posting_date": {"from": "now-" + numberOfMonths + "d"}})


    a = A('terms', field='area.raw', size=1000, exclude="NA|na")
    a1 = A('terms', field='bedrooms', size=1000, exclude=[-1], order={"_term": "asc"})
    a3 = A('percentiles', field='price')
    s.aggs.bucket('AreaAgg', a).bucket('SizeAgg', a1).bucket('PriceAgg', a3)
    s = s.doc_type("_doc")
    response = s.execute()
    return HttpResponse(json.dumps(response.to_dict()))


@csrf_exempt
@api_view(['GET'])
def averagePricePerAreaForSpecificSize(request, format=None):
    cities = request.GET["cities"]
    numberOfMonths = request.GET["numberOfMonths"] or 30
    priceGreaterThanOrEqual = request.GET["priceFrom"] or None
    priceLessThanOrEqual = request.GET["priceTo"] or None
    if "propertyTypes" in request.GET:
        propertyTypes = request.GET["propertyTypes"] or None
    else:
        propertyTypes = "rent"
    size = request.GET["size"] or None
    s = PropertyDocument.search()
    if cities is not None:
        citiesValues = cities.split(',')
        citiesshouldlist = list()
        for city in citiesValues:
            buildingshouldmatchitem = Q('match', city=city)
            citiesshouldlist.append(buildingshouldmatchitem)
        q = Q('bool', should=citiesshouldlist)
        s = s.query(q)
        if priceGreaterThanOrEqual is not None:
            if priceLessThanOrEqual is not None:
                s = s.filter('range', **{"price": {"from": priceGreaterThanOrEqual, "to": priceLessThanOrEqual}})
            else:
                s = s.filter('range', **{"price": {"from": priceGreaterThanOrEqual}})
        elif priceLessThanOrEqual is not None:
            s = s.filter('range', **{"price": {"to": priceLessThanOrEqual}})
        if numberOfMonths is not None:
            s = s.filter('range', **{"posting_date": {"from": "now-" + numberOfMonths + "d"}})

        if size is not None:
            s = s.filter('term', bedrooms=size)

        a = A('terms', field='area.raw', size=100)
        a3 = A('percentiles', field='price')
        s.aggs.bucket('AreaAgg', a).bucket('PriceAgg', a3)
        s = s.doc_type("_doc")
        response = s.execute()
        return HttpResponse(json.dumps(response.to_dict()))
    else:
        return HttpResponse(status=500,
                            content="requested data is wrong ")  # <--- this response is only returned
