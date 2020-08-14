# import dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, render_template, redirect, jsonify

#database setup
connection_string = "curitirfxmwgst:0b6553d1d2876fe8d3850d9dc9090b9d4d156e0307b6923703277aef3d140eea@ec2-54-159-138-67.compute-1.amazonaws.com:5432/dfvj0ivhcpion9"
engine = create_engine(f'postgresql://{connection_string}')
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
combined_table = Base.classes.usetravelapp
amusement_table = Base.classes.amusementpark
aquarium_table = Base.classes.aquarium
beach_table = Base.classes.beaches
campsite_table = Base.classes.campsite
casino_table = Base.classes.casinos
festival_table = Base.classes.festival
mall_table = Base.classes.malls
park_table = Base.classes.nationalpark
zoo_table = Base.classes.zoo

# Flask Setup
app = Flask(__name__)

# Flask Routes

# home page to render index.html
@app.route("/")
def home():
    return render_template("index.html")

# api route to obtain the name and overall ranking of each state
@app.route("/rank")
def rank():
    session = Session(engine)

    # query to obtain state name and rank
    ranking = session.query(combined_table.state, combined_table.rank_number).all()
    session.close()

    # adds data into a dictionary to be jsonified
    rank_list = []
    for state_name, rank in ranking:
        rank_list_dict = {}
        rank_list_dict["name"] = state_name
        rank_list_dict["rank"] = rank
        rank_list.append(rank_list_dict)
    
    return jsonify(rank_list)


# dynamic state page
# api route to obtain detailed information for each state, depending on which state is passed into the  url
@app.route("/<state>")
def dynamic(state):
    # Create a session
    session = Session(engine)

    # query to obtain overall data of the state, such as amount of each type of attraction
    travel_num = session.query(combined_table.state, combined_table.abbr, combined_table.states_value, combined_table.count_amusement_park, combined_table.count_aquarium, combined_table.count_beach, combined_table.count_casino, combined_table.count_festival, combined_table.count_hotelratings, combined_table.count_malls, combined_table.count_parks, combined_table.count_campsite, combined_table.count_zoo, combined_table.airfare_rank, combined_table.passenger_rank, combined_table.rank_number, combined_table.airfare_value, combined_table.passenger_value, combined_table.hotel_ratings, combined_table.state_value_rank).\
        filter(combined_table.state == state).all()
    session.close()

    # query to obtain all the amusement parks in the state
    amusement_query = session.query(amusement_table.amusementpark_name).\
        filter(amusement_table.state == state).all()
    session.close()
    # query to obtain all the aquariums in the state
    aquarium_query = session.query(aquarium_table.aquarium_name).\
        filter(aquarium_table.state == state).all()
    session.close()
    # query to obtain all the beaches in the state
    beach_query = session.query(beach_table.beach_name).\
        filter(beach_table.state == state).all()
    session.close()
    # query to obtain all the campsites in the state
    campsite_query = session.query(campsite_table.name).\
        filter(campsite_table.state == state).all()
    session.close()
    # query to obtain all the casinos in the state
    casino_query = session.query(casino_table.casino).\
        filter(casino_table.state == state).all()
    session.close()
    # query to obtain all the festivals in the state
    festival_query = session.query(festival_table.festival_name).\
        filter(festival_table.state == state).all()
    session.close()
    # query to obtain all the malls in the state
    mall_query = session.query(mall_table.shoppingmall_name).\
        filter(mall_table.state == state).all()
    session.close()
    # query to obtain all the parks in the state
    park_query = session.query(park_table.national_park_name).\
        filter(park_table.state == state).all()
    session.close()
    # query to obtain all the zoos in the state
    zoo_query = session.query(zoo_table.zoo_name).\
        filter(zoo_table.state == state).all()
    session.close()

     # add all data into a list to be jsonified
    start_list = []
    # start_list_dict = {}
    for state, abbr, dollar, amusement_num, aquarium_num, beach_num, casino_num, festival_num, hotel_rank, mall_num, park_num, campsite_num, zoo_num, airfare_rank, passenger_rank, rank, airfare, passenger, rating, dollar_rank in travel_num:
        start_list_dict = {}
        start_list_dict["state"] = state
        start_list_dict["abbreviation"] = abbr
        start_list_dict["dollar_value"] = dollar
        start_list_dict["amusement_park_num"] = amusement_num
        start_list_dict["aquarium_num"] = aquarium_num
        start_list_dict["beach_num"] = beach_num
        start_list_dict["casino_num"] = casino_num
        start_list_dict["festival_num"] = festival_num
        start_list_dict["hotel_ratings_rank"] = hotel_rank
        start_list_dict["mall_num"] = mall_num
        start_list_dict["national_park_num"] = park_num
        start_list_dict["campsite_num"] = campsite_num
        start_list_dict["zoo_num"] = zoo_num
        start_list_dict["airfare_rank"] = airfare_rank
        start_list_dict["passenger_rank"] = passenger_rank
        start_list_dict["overall_rank"] = rank
        start_list_dict["average_airfare"] = airfare
        start_list_dict["amount_passengers"] = passenger
        start_list_dict["average_hotel_rating"] = rating
        start_list_dict["dollar_value_rank"] = dollar_rank
        start_list.append(start_list_dict)
    
    amusement_list = []
    aquarium_list = []
    beach_list = []
    campsite_list = []
    casino_list = []
    festival_list = []
    mall_list = []
    park_list = []
    zoo_list = []

    attraction_dict = {}

    # for each type of attraction, if the state contains any of that type, add it to a list and then a dictionary,
    if amusement_query:
        for amusement in amusement_query:
            for item in amusement:
                amusement_list.append(item)
            attraction_dict["amusement_park_list"] = amusement_list

    if aquarium_query:
        for aquarium in aquarium_query:
            for item in aquarium:
                aquarium_list.append(item)
            attraction_dict["aquarium_list"] = aquarium_list

    if beach_query:
        for beach in beach_query:
            for item in beach:
                beach_list.append(item)
            attraction_dict["beach_list"] = beach_list

    if campsite_query:
        for campsite in campsite_query:
            for item in campsite:
                campsite_list.append(item)
            attraction_dict["campsite_list"] = campsite_list

    if casino_query:
        for casino in casino_query:
            for item in casino:
                casino_list.append(item)
            attraction_dict["casino_list"] = casino_list

    if festival_query:
        for festival in festival_query:
            for item in festival:
                festival_list.append(item)
            attraction_dict["festival_list"] = festival_list

    if mall_query:
        for mall in mall_query:
            for item in mall:
                mall_list.append(item)
            attraction_dict["mall_list"] = mall_list

    if park_query:
        for park in park_query:
            for item in park:
                park_list.append(item)
            attraction_dict["national_park_list"] = park_list

    if zoo_query:
        for zoo in zoo_query:
            for item in zoo:
                zoo_list.append(item)
            attraction_dict["zoo_list"] = zoo_list
    # add the dictionary to the same list that was previously used
    start_list.append(attraction_dict)
    # return the jsonified verision of the list when 
    return jsonify(start_list)

if __name__ == "__main__":
    app.run(debug=True)
