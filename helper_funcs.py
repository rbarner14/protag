from model import connect_to_db, db, Producer, Performer, Song, Album, ProduceSong 

def get_performer_id(desired_performer_id):

    return Performer.query.get(desired_performer_id)

def quantify_performer_similarity(performer_id_1, performer_id_2):

    performer_1_producers = get_performer_id(performer_id_1).producers
    performer_2_producers = get_performer_id(performer_id_2).producers

    performer_1_producer_count = len(performer_1_producers)
    performer_2_producer_count = len(performer_2_producers)

    total_producers = performer_1_producer_count + performer_2_producer_count

    performer_1_producer_set = set(performer_1_producers)
    performer_1_producer_set = set(performer_1_producers)