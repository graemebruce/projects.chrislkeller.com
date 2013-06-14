from django.core.management.base import BaseCommand
from parking.models import Garage
import requests
import lxml
from lxml import html
import time, datetime
from django.utils.encoding import smart_str, smart_unicode

class Command(BaseCommand):
    help = 'Scrapes Madison Parking Garage data'

    def handle(self, *args, **options):
        self.stdout.write('\nScraping finished at %s\n' % str(datetime.datetime.now()))

    #search URL and assign to variable r
    r = requests.get('http://www.cityofmadison.com/parkingUtility/garagesLots/availability/')

    #create variable tree from r's content
    tree = lxml.html.fromstring(r.content)

    #search the tree for the given element
    elements = tree.cssselect("div.dataRow")

    #for each element in the variable
    for div in elements:

        #select inner divs
        divs = div.cssselect('div')

        #set variables
        name = divs[1].text_content().strip()
        spots = divs[2].text_content().strip()
        time = datetime.datetime.now()
            
        try:
            obj = Garage.objects.get(name=name)
            obj.spots = spots
            obj.time = time
            obj.save()
        except Garage.DoesNotExist:
            obj = Garage(name=name, spots=spots, time=time)
            obj.save()