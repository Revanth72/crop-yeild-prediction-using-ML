from rdflib import Graph, Namespace, Literal, URIRef
import pandas as pd

# Define namespaces
ex = Namespace("http://example.org/")
rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")

# Create an RDF graph
g = Graph()

# Bind namespaces
g.bind("ex", ex)
g.bind("rdf", rdf)
g.bind("rdfs", rdfs)

# Create a super-node
agriculture_node = URIRef(ex + "Agriculture")

# Create main nodes
planting_location_node = URIRef(ex + "PlantingLocation")
weather_conditions_node = URIRef(ex + "WeatherConditions")
crop_type_node = URIRef(ex + "CropTypes")
yield_node = URIRef(ex + "Yields")
soil_conditions_node = URIRef(ex + "SoilConditions")
external_resources_node = URIRef(ex + "ExternalResources")

g.add((planting_location_node, rdf.type, ex.PlantingLocation0))
g.add((weather_conditions_node, rdf.type, ex.WeatherConditions0))
g.add((crop_type_node, rdf.type, ex.CropTypes0))
g.add((yield_node, rdf.type, ex.Yields0))
g.add((soil_conditions_node, rdf.type, ex.SoilConditions0))
g.add((external_resources_node, rdf.type, ex.ExternalResources0))

# Add relationships from the super-node to the main nodes
g.add((agriculture_node, ex.hasSubNode, planting_location_node))
g.add((agriculture_node, ex.hasSubNode, weather_conditions_node))
g.add((agriculture_node, ex.hasSubNode, crop_type_node))
g.add((agriculture_node, ex.hasSubNode, yield_node))
g.add((agriculture_node, ex.hasSubNode, soil_conditions_node))
g.add((agriculture_node, ex.hasSubNode, external_resources_node))


# Read CSV data for Data1
df1 = pd.read_csv('C:\\Users\\AVITA\\GraphDBandFDA\\food.csv')

for index, row in df1.iterrows():
    # Create sub-nodes for each main node
    india_node1 = URIRef(ex + "India")
    india_node2= URIRef(ex + "Weather_India")
    india_node3=URIRef(ex+"Soil_India")
    india_node4=URIRef(ex+"Indian_crops")
    india_node5=URIRef(ex+"India_Crop_Production")
    g.add((india_node1, rdf.type, ex.Country))
    g.add((india_node2, rdf.type, ex.CountryWeather))
    g.add((india_node3, rdf.type, ex.CountrySoil))
    g.add((india_node4, rdf.type, ex.CountryCrop))
    g.add((india_node5, rdf.type, ex.CountryYield))
    #Location
    g.add((planting_location_node, ex.hasCountry, india_node1))
    planting_location_subnode = URIRef(ex + "PlantingLocation_R/")
    state_node = URIRef(ex + str(row['State']))
    g.add((state_node, rdf.type, ex.State1))
    g.add((planting_location_subnode,ex.hasState,state_node))

    weather_conditions_subnode = URIRef(ex + "WeatherConditions_R/")
    season=URIRef(ex+str("Season"))
    season_node=URIRef(ex+str(row['Season']))
    g.add((season_node, rdf.type, ex.Season1))
    g.add((weather_conditions_subnode,ex.hasSeason,season))
    g.add((season,ex.hasSeason,season_node))

    year=URIRef(str("Year"))
    year_node=URIRef(ex+ str(row['Year']))
    g.add((year_node, rdf.type, ex.Year1))
    g.add((weather_conditions_subnode,ex.hasYear,year))
    g.add((year,ex.hasYears,year_node))

    rainfall = URIRef(str("Rainfall"))
    rainfall_node = URIRef(ex+str(row['Rainfall']))
    g.add((rainfall_node, rdf.type, ex.Rainfall1))
    g.add((weather_conditions_subnode, ex.hasRainfall, rainfall))
    g.add((rainfall, ex.hasRainfalls, rainfall_node))
    
    soil_conditions_subnode = URIRef(ex + "SoilConditions_R/")
    area = URIRef(str("Area"))
    area_node = URIRef(ex+str(row['Area']))
    g.add((area_node, rdf.type, ex.Area1))
    g.add((soil_conditions_subnode, ex.hasArea, area))
    g.add((area, ex.hasAreas, area_node))
    
    crop_type_subnode = URIRef(ex + "CropTypes_R/")
    crop = URIRef(str("Crop"))
    crop_node = URIRef(ex+ str(row['Crop']))
    g.add((crop_node, rdf.type, ex.Crop1))
    g.add((crop_type_subnode, ex.hasCrop, crop))
    g.add((crop, ex.hasCrops, crop_node))
    
    yield_subnode = URIRef(ex + "Yields_R/")
    production = URIRef(str("Production"))
    production_node = URIRef(ex+ str(row['Production']))
    g.add((production_node, rdf.type, ex.Production1))
    g.add((yield_subnode, ex.hasProduction, production))
    g.add((production, ex.hasProductions, production_node))
    #Adding types for all subnodes
    g.add((planting_location_subnode, rdf.type, ex.PlantingLocation1))
    g.add((weather_conditions_subnode, rdf.type, ex.WeatherConditions1))
    g.add((soil_conditions_subnode, rdf.type, ex.SoilConditions1))
    g.add((crop_type_subnode, rdf.type, ex.CropTypes1))
    g.add((yield_subnode, rdf.type, ex.Yields1))
    # Add relationships from the main nodes to the sub-nodes
    g.add((india_node1, ex.hasSubNode, planting_location_subnode))
    g.add((weather_conditions_node, ex.hasCountry, india_node2))
    g.add((india_node2, ex.hasSubNode, weather_conditions_subnode))
    g.add((soil_conditions_node, ex.hasSubNode, india_node3))
    g.add((india_node3, ex.hasSubNode, soil_conditions_subnode))
    g.add((crop_type_node, ex.hasSubNode, india_node4))
    g.add((india_node4, ex.hasSubNode, crop_type_subnode))
    g.add((yield_node, ex.hasSubNode, india_node5))
    g.add((india_node5, ex.hasSubNode, yield_subnode))

america_node1 = URIRef(ex + "America")
america_node2 = URIRef(ex + "Weather_America")
america_node3 = URIRef(ex + "Soil_America")
america_node4 = URIRef(ex + "American_crops")
america_node5 = URIRef(ex + "America_Crop_Production")
g.add((america_node1, rdf.type, ex.Country))
g.add((america_node2, rdf.type, ex.CountryWeather))
g.add((america_node3, rdf.type, ex.CountrySoil))
g.add((america_node4, rdf.type, ex.CountryCrop))
g.add((america_node5, rdf.type, ex.CountryYield))


g.add((planting_location_node, ex.hasCountry, america_node1))
g.add((weather_conditions_node, ex.hasCountry, america_node2))
g.add((soil_conditions_node, ex.hasCountry, america_node3))
g.add((crop_type_node, ex.hasCountry, america_node4))
g.add((yield_node, ex.hasCountry, america_node5))
# Read CSV data for Data2
df2 = pd.read_csv('C:\\Users\\AVITA\\GraphDBandFDA\\srikdata.csv')

for index, row in df2.iterrows():
    # Create sub-nodes for each main node
    planting_location_subnode = URIRef(ex + "PlantingLocation_S/")
    city=URIRef(ex+str('Manhattan_S'))
    g.add((city, rdf.type, ex.City2))
    g.add((planting_location_subnode,ex.hasCity,city))

    weather_conditions_subnode = URIRef(ex + "WeatherConditions_S/")  # Assuming index represents different weather conditions
    humi=URIRef(ex+str('RelativeHumidity'))
    humi_node=URIRef(ex+str(row['RelativeHumidity_avg(%)']))
    g.add((humi_node, rdf.type, ex.Humidity2))
    g.add((weather_conditions_subnode, ex.hasrelhumidity, humi))
    g.add((humi, ex.hasRelhumidities, humi_node))

    temp_max = URIRef(ex + 'TemperatureMax')
    temp_max_node = URIRef(ex + str(row['AirTemperature_max(°F)']))
    g.add((temp_max_node, rdf.type, ex.TempMax2))
    g.add((weather_conditions_subnode, ex.hasTemperatureMax, temp_max))
    g.add((temp_max, ex.hasTemperatureMaxs, temp_max_node))

    temp_min = URIRef(ex + 'TemperatureMin')
    temp_min_node = URIRef(ex + str(row['AirTemperature_min(°F)']))
    g.add((temp_min_node, rdf.type, ex.TempMin2))
    g.add((weather_conditions_subnode, ex.hasTemperatureMin, temp_min))
    g.add((temp_min, ex.hasTemperatureMins, temp_min_node))

    precipitation = URIRef(ex + 'Precipitation')
    precipitation_node = URIRef(ex + str(row['Precipitation_total(inches)']))
    g.add((precipitation_node, rdf.type, ex.Precipitation2))
    g.add((weather_conditions_subnode, ex.hasPrecipitation, precipitation))
    g.add((precipitation, ex.hasPrecipitations, precipitation_node))

    wind_speed_avg = URIRef(ex + 'WindSpeedAvg')
    wind_speed_avg_node = URIRef(ex + str(row['WindSpeed_avg(mph)']))
    g.add((wind_speed_avg_node, rdf.type, ex.WindSpeedAvg2))
    g.add((weather_conditions_subnode, ex.hasWindSpeedAvg, wind_speed_avg))
    g.add((wind_speed_avg, ex.hasWindSpeedAvgs, wind_speed_avg_node))

    wind_speed_max = URIRef(ex + 'WindSpeedMax')
    wind_speed_max_node = URIRef(ex + str(row['WindSpeed_max(mph)']))
    g.add((wind_speed_max_node, rdf.type, ex.WindSpeedMax2))
    g.add((weather_conditions_subnode, ex.hasWindSpeedMax, wind_speed_max))
    g.add((wind_speed_max, ex.hasWindSpeedMaxs, wind_speed_max_node))

    solar_radiation = URIRef(ex + 'SolarRadiation')
    solar_radiation_node = URIRef(ex + str(row['SolarRadiation_total(ly)']))
    g.add((solar_radiation_node, rdf.type, ex.SolarRadiation2))
    g.add((weather_conditions_subnode, ex.hasSolarRadiation, solar_radiation))
    g.add((solar_radiation, ex.hasSolarRadiations, solar_radiation_node))
    
    # Create soil conditions node
    soil_conditions_subnode = URIRef(ex + "SoilConditions_S/")
    soil_temp_max = URIRef(ex + 'SoilTemperatureMax')
    soil_temp_max_node = URIRef(ex + str(row['SoilTemperature_2"_max(°F)']))
    g.add((soil_temp_max_node, rdf.type, ex.SoilTempMax2))
    g.add((soil_conditions_subnode, ex.hasSoilTemperatureMax, soil_temp_max))
    g.add((soil_temp_max, ex.hasSoilTemperatureMaxs, soil_temp_max_node))

    soil_temp_min = URIRef(ex + 'SoilTemperatureMin')
    soil_temp_min_node = URIRef(ex + str(row['SoilTemperature_2"_min(°F)']))
    g.add((soil_temp_min_node, rdf.type, ex.SoilTempMin2))
    g.add((soil_conditions_subnode, ex.hasSoilTemperatureMin, soil_temp_min))
    g.add((soil_temp_min, ex.hasSoilTemperatureMins, soil_temp_min_node))

    soil_temp_4inches_min = URIRef(ex + 'SoilTemperature4inchesMin')
    soil_temp_4inches_min_node = URIRef(ex + str(row['SoilTemperature_4"_min(°F)']))
    g.add((soil_temp_4inches_min_node, rdf.type, ex.SoilTempMin2))
    g.add((soil_conditions_subnode, ex.hasSoilTemperature4inchesMin, soil_temp_4inches_min))
    g.add((soil_temp_4inches_min, ex.hasSoilTemperature4inchesMins, soil_temp_4inches_min_node))

    soil_temp_4inches_max = URIRef(ex + 'SoilTemperature4inchesMax')
    soil_temp_4inches_max_node = URIRef(ex + str(row['SoilTemperature_4"_max(°F)']))
    g.add((soil_temp_4inches_max_node, rdf.type, ex.SoilTempMax2))
    g.add((soil_conditions_subnode, ex.hasSoilTemperature4inchesMax, soil_temp_4inches_max))
    g.add((soil_temp_4inches_max, ex.hasSoilTemperature4inchesMaxs, soil_temp_4inches_max_node))
    
    crop_type_subnode = URIRef(ex + "CropTypes_S/")
    crop_type = URIRef(ex + 'CropType')
    crop_type_node = URIRef(ex + str(row['Crop type']))
    g.add((crop_type_node, rdf.type, ex.CropType2))
    g.add((crop_type_subnode, ex.hasCrop, crop_type))
    g.add((crop_type, ex.hasCropnodes, crop_type_node))

    yield_subnode = URIRef(ex + "Yields_S/")
    yield_ = URIRef(ex + 'Yield')
    yield_node = URIRef(ex + str(row['Wheat-BU/Acre']))
    g.add((yield_node, rdf.type, ex.Yield2))
    g.add((yield_subnode, ex.hasYield, yield_))
    g.add((yield_, ex.hasYields, yield_node))

    g.add((planting_location_subnode, rdf.type, ex.PlantingLocation2))
    g.add((weather_conditions_subnode, rdf.type, ex.WeatherConditions2))
    g.add((soil_conditions_subnode, rdf.type, ex.SoilConditions2))
    g.add((crop_type_subnode, rdf.type, ex.CropTypes2))
    g.add((yield_subnode, rdf.type, ex.Yields2))
    # Add relationships from the main nodes to the sub-nodes
    g.add((america_node1, ex.hasSubNode, planting_location_subnode))
    g.add((america_node2, ex.hasSubNode, weather_conditions_subnode))
    g.add((america_node3, ex.hasSubNode, soil_conditions_subnode))
    g.add((america_node4, ex.hasSubNode, crop_type_subnode))
    g.add((america_node5, ex.hasSubNode, yield_subnode))

# Read CSV data for Data3
df3 = pd.read_csv('C:\\Users\\AVITA\\GraphDBandFDA\\Crop_recommendation.csv')

for index, row in df3.iterrows():
    # Create sub-nodes for each main node
    planting_location_subnode = URIRef(ex + "PlantingLocation_A/")
    city=URIRef(ex+str('Manhattan_A'))
    g.add((city, rdf.type, ex.City3))
    g.add((planting_location_subnode,ex.hasCity,city))
    #Weather
    weather_conditions_subnode = URIRef(ex + "WeatherConditions_A/" )
    humidity = URIRef(ex + 'Humidity')
    humidity_node = URIRef(ex + str(row['humidity']))
    g.add((humidity_node, rdf.type, ex.Humidity3))
    g.add((weather_conditions_subnode, ex.hasHumidity, humidity))
    g.add((humidity, ex.hasHumidities, humidity_node))

    temperature = URIRef(ex + 'Temperature')
    temperature_node = URIRef(ex + str(row['temperature']))
    g.add((temperature_node, rdf.type, ex.Temperature3))
    g.add((weather_conditions_subnode, ex.hasTemperature, temperature))
    g.add((temperature, ex.hasTemperatures, temperature_node))

    rainfall = URIRef(ex + 'Rainfall')
    rainfall_node = URIRef(ex + str(row['rainfall']))
    g.add((rainfall_node, rdf.type, ex.Rainfall3))
    g.add((weather_conditions_subnode, ex.hasRain, rainfall))
    g.add((rainfall, ex.hasRainvaluess, rainfall_node))
    #Soil
    soil_conditions_subnode = URIRef(ex + "SoilConditions_A/")
    ph = URIRef(ex + 'PH')
    ph_node = URIRef(ex + str(row['ph']))
    g.add((ph_node, rdf.type, ex.PH3))
    g.add((soil_conditions_subnode, ex.hasPH, ph))
    g.add((ph, ex.Phs, ph_node))
    #Crops
    crop_type_subnode = URIRef(ex + "CropTypes_A/")
    crop_type = URIRef(ex + 'Crops')
    crop_type_node = URIRef(ex + str(row['Crops']))
    g.add((crop_type_node, rdf.type, ex.Crops3))
    g.add((crop_type_subnode, ex.hasCropType, crop_type))
    g.add((crop_type, ex.hasCropTypes, crop_type_node))

    yield_subnode = URIRef(ex + "Yields_A/")
    Nitro = URIRef(ex + 'Nitrogen')
    Nitro_node = URIRef(ex + str(row['Nitrogen']))
    g.add((Nitro_node, rdf.type, ex.Nitrogen))
    g.add((yield_subnode, ex.hasNitrogen,Nitro))
    g.add((Nitro, ex.hasNitrogens, Nitro_node))

    phosphorus = URIRef(ex + 'Phosphorus')
    phosphorus_node = URIRef(ex + str(row['phosphorus']))
    g.add((phosphorus_node, rdf.type, ex.phosphorus))
    g.add((yield_subnode, ex.hasPhosphorus,phosphorus))
    g.add((phosphorus, ex.hasPhosphoruses, phosphorus_node))

    potassium = URIRef(ex + 'Potassium')
    potassium_node = URIRef(ex + str(row['potassium']))
    g.add((potassium_node, rdf.type, ex.potassium))
    g.add((yield_subnode, ex.hasPotassiums,potassium))
    g.add((potassium, ex.hasPotassiums, potassium_node))



    external_resources_subnode = URIRef(ex + "ExternalResources_A/")
    g.add((external_resources_subnode,ex.hasFertilizers,Literal('Nitrogen')))
    g.add((external_resources_subnode,ex.hasFertilizers,Literal('Phosphorus')))
    g.add((external_resources_subnode,ex.hasFertilizers,Literal('Pottassium')))

    g.add((planting_location_subnode, rdf.type, ex.PlantingLocation3))
    g.add((weather_conditions_subnode, rdf.type, ex.WeatherConditions3))
    g.add((soil_conditions_subnode, rdf.type, ex.SoilConditions3))
    g.add((crop_type_subnode, rdf.type, ex.CropTypes3))
    g.add((external_resources_subnode, rdf.type, ex.ExternalResources1))
    # Add relationships from the main nodes to the sub-nodes
    g.add((america_node1, ex.hasSubNode, planting_location_subnode))
    g.add((america_node2, ex.hasSubNode, weather_conditions_subnode))
    g.add((america_node3, ex.hasSubNode, soil_conditions_subnode))
    g.add((america_node4, ex.hasSubNode, crop_type_subnode))
    g.add((america_node5,ex.hasSubNode,yield_subnode))
    g.add((external_resources_node, ex.hasSubNode, external_resources_subnode))

# Save RDF data to a file
g.serialize('Combined.rdf', format='xml')