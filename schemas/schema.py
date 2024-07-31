def individual_serialise_1(obj)->dict:
    return{
        "id":str(obj['_id']),
        "sentence":obj['sentence'],
        "label": obj['label']
    }

def individual_serialise_2(obj)->dict:
    return{
        "id":str(obj['_id']),
        "label_class":obj['label_class']
    }