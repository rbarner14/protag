from model import connect_to_db, db, Producer, Performer, Song, Album, ProduceSong 
from server import app

def quantify_performer_similarity(p1_id, p2_id):

    p1_producers = set(Performer.query.get(p1_id).producers)
    p2_producers = set(Performer.query.get(p2_id).producers)

    total_producers = len(p1_producers) + len(p2_producers)

    overlapping_producers = len(p1_producers & p2_producers)

    similarity_score = (overlapping_producers * 2) / total_producers

    return similarity_score


def generate_producer_vector():

    # create list of producers
    producers = Producer.query.order_by("producer_id")
    producer_ids = []

    for producer in producers:
        producer_ids.append(producer.producer_id)

    return producer_ids


def generate_performer_vector():

    # create list of performers
    performers = Performer.query.order_by("performer_id")
    performer_ids = []

    for performer in performers:
        performer_ids.append(performer.performer_id)

    return performer_ids


def generate_performer_vectors(performer_id):

    producers = generate_producer_vector()
    performer_vector = []

    for producer in producers:
        if ProduceSong.query.filter_by(producer)


if __name__ == "__main__":
    # Added for module interactive convenience to work directly with database.
    
    from server import app
    connect_to_db(app)
    print("Connected to DB.")
