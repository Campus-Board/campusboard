__author__ = 'mac'

TAXONOMY_LEN = 16

def default_profile():
    return [0.5]*TAXONOMY_LEN

def cs_profile():
    profile =  [0.0]*TAXONOMY_LEN
    for i in range(12,TAXONOMY_LEN):
        profile[i] = 1
    return profile

def cs_and_artist_profile():
    profile = [0.0]*TAXONOMY_LEN
    for i in range(0, 5):
        profile[i] = 1
    for i in range(12,TAXONOMY_LEN):
        profile[i] = 1
    return profile